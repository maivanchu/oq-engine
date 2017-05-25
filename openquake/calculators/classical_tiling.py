# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2014-2017 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import logging
import operator
from functools import partial
import numpy

from openquake.baselib import parallel
from openquake.baselib.general import AccumDict
from openquake.hazardlib.calc.hazard_curve import (
    pmap_from_grp, ProbabilityMap)
from openquake.commonlib import datastore, source
from openquake.calculators import base

U16 = numpy.uint16
F32 = numpy.float32
F64 = numpy.float64


def classical_tiling(sources, src_filter, gsims, param, monitor):
    """
    :param sources:
        a non-empty sequence of sources of homogeneous tectonic region type
    :param src_filter:
        source filter
    :param gsims:
        a list of GSIMs for the current tectonic region type
    :param param:
        a dictionary of parameters
    :param monitor:
        a monitor instance
    :returns:
        an AccumDict rlz -> curves
    """
    truncation_level = monitor.truncation_level
    imtls = monitor.imtls
    src_group_id = sources[0].src_group_id
    # sanity check: the src_group must be the same for all sources
    for src in sources[1:]:
        assert src.src_group_id == src_group_id
    pmap = pmap_from_grp(
        sources, src_filter, imtls, gsims, truncation_level,
        bbs=[], monitor=monitor)
    pmap.grp_id = src_group_id
    return pmap


@base.calculators.add('classical_tiling')
class ClassicalTilingCalculator(base.HazardCalculator):
    """
    Classical PSHA calculator
    """
    core_task = classical_tiling
    source_info = datastore.persistent_attribute('source_info')

    def agg_dicts(self, acc, pmap):
        """
        Aggregate dictionaries of hazard curves by updating the accumulator.

        :param acc: accumulator dictionary
        :param pmap: a ProbabilityMap
        """
        with self.monitor('aggregate curves', autoflush=True):
            for src_id, nsites, calc_time in pmap.calc_times:
                src_id = src_id.split(':', 1)[0]
                info = self.csm.infos[pmap.grp_id, src_id]
                info.calc_time += calc_time
                info.num_sites = max(info.num_sites, nsites)
                info.num_split += 1
            acc.eff_ruptures += pmap.eff_ruptures
            for bb in getattr(pmap, 'bbs', []):  # for disaggregation
                acc.bb_dict[bb.lt_model_id, bb.site_id].update_bb(bb)
            acc[pmap.grp_id] |= pmap
        self.datastore.flush()
        return acc

    def zerodict(self):
        """
        Initial accumulator, a dict grp_id -> ProbabilityMap(L, G)
        """
        zd = AccumDict()
        num_levels = len(self.oqparam.imtls.array)
        for grp in self.csm.src_groups:
            num_gsims = len(self.rlzs_assoc.gsims_by_grp_id[grp.id])
            zd[grp.id] = ProbabilityMap(num_levels, num_gsims)
        zd.calc_times = []
        zd.eff_ruptures = AccumDict()  # grp_id -> eff_ruptures
        return zd

    def execute(self):
        """
        Run in parallel `core_task(sources, sitecol, monitor)`, by
        parallelizing on the sources according to their weight and
        tectonic region type.
        """
        monitor = self.monitor(self.core_task.__name__)
        with self.monitor('managing sources', autoflush=True):
            iterargs = self.gen_args(self.csm, monitor)
            ires = parallel.Starmap(
                self.core_task.__func__, iterargs).submit_all()
        acc = ires.reduce(self.agg_dicts, self.zerodict())
        with self.monitor('store source_info', autoflush=True):
            self.store_source_info(self.csm.infos, acc)
        return acc

    def gen_args(self, csm, monitor):
        """
        Used in the case of large source model logic trees.

        :param csm: a CompositeSourceModel instance
        :param monitor: a :class:`openquake.baselib.performance.Monitor`
        :yields: (sources, sites, gsims, monitor) tuples
        """
        oq = self.oqparam
        maxweight = self.csm.get_maxweight(oq.concurrent_tasks)
        logging.info('Using a maxweight of %d', maxweight)
        ngroups = sum(len(sm.src_groups) for sm in csm.source_models)
        for sm in csm.source_models:
            for sg in sm.src_groups:
                logging.info('Sending source group #%d of %d (%s, %d sources)',
                             sg.id + 1, ngroups, sg.trt, len(sg.sources))
                gsims = self.rlzs_assoc.gsims_by_grp_id[sg.id]
                if oq.poes_disagg or oq.iml_disagg:  # only for disaggregation
                    monitor.sm_id = self.rlzs_assoc.sm_ids[sg.id]
                param = dict(
                    samples=sm.samples, seed=oq.ses_seed,
                    ses_per_logic_tree_path=oq.ses_per_logic_tree_path)
                if sg.src_interdep == 'mutex':  # do not split the group
                    self.csm.add_infos(sg.sources)
                    yield sg, self.src_filter, gsims, param, monitor
                else:
                    for block in self.csm.split_sources(
                            sg.sources, self.src_filter, maxweight):
                        yield block, self.src_filter, gsims, param, monitor

    def store_source_info(self, infos, acc):
        # save the calculation times per each source
        if infos:
            rows = sorted(
                infos.values(),
                key=operator.attrgetter('calc_time'),
                reverse=True)
            array = numpy.zeros(len(rows), source.SourceInfo.dt)
            for i, row in enumerate(rows):
                for name in array.dtype.names:
                    array[i][name] = getattr(row, name)
            self.source_info = array
            infos.clear()
        self.rlzs_assoc = self.csm.info.get_rlzs_assoc(
            partial(self.count_eff_ruptures, acc))
        self.datastore['csm_info'] = self.csm.info
        self.datastore['csm_info/assoc_by_grp'] = array = (
            self.rlzs_assoc.get_assoc_by_grp())
        # computing properly the length in bytes of a variable length array
        nbytes = array.nbytes + sum(rec['rlzis'].nbytes for rec in array)
        self.datastore.set_attrs('csm_info/assoc_by_grp', nbytes=nbytes)
        self.datastore.flush()

    def post_execute(self, pmap_by_grp_id):
        """
        Collect the hazard curves by realization and export them.

        :param pmap_by_grp_id:
            a dictionary grp_id -> hazard curves
        """
        if pmap_by_grp_id.bb_dict:
            self.datastore['bb_dict'] = pmap_by_grp_id.bb_dict
        grp_trt = self.csm.info.grp_trt()
        with self.monitor('saving probability maps', autoflush=True):
            for grp_id, pmap in pmap_by_grp_id.items():
                if pmap:  # pmap can be missing if the group is filtered away
                    key = 'poes/grp-%02d' % grp_id
                    self.datastore[key] = pmap
                    self.datastore.set_attrs(key, trt=grp_trt[grp_id])
            if 'poes' in self.datastore:
                self.datastore.set_nbytes('poes')
