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
import numpy

from openquake.hazardlib.calc.hazard_curve import pmap_from_grp, SourceFilter
from openquake.calculators import base, classical

U16 = numpy.uint16
F32 = numpy.float32
F64 = numpy.float64


def classical_tiling(csm, tile, gsims_by_grp, param, monitor):
    """
    :param csm:
        a CompositeSourceModel instance
    :param tile:
        a SiteCollection instance
    :param gsims_by_grp:
        a dictionary src_group_id -> gsims
    :param param:
        a dictionary of parameters (imtls, truncation_level, maximum_distance)
    :param monitor:
        a monitor instance
    :returns:
        a dictionary src_group_id -> ProbabilityMap
    """
    imtls = param['imtls']
    truncation_level = param['truncation_level']
    src_filter = SourceFilter(tile, param['maximum_distance'], use_rtree=False)
    pmap_by_grp = {}
    for group in csm.src_groups:
        if len(group):
            pmap_by_grp[group.id] = pmap_from_grp(
                group, src_filter, imtls, gsims_by_grp[group.id],
                truncation_level)
    return pmap_by_grp


@base.calculators.add('psha_tiling')
class PSHATilingCalculator(classical.PSHACalculator):
    """
    Classical PSHA tiling calculator
    """
    core_task = classical_tiling

    def gen_args(self, csm, monitor):
        """
        :param csm: a CompositeSourceModel instance
        :param monitor: a :class:`openquake.baselib.performance.Monitor`
        :yields: (csm, tile, gsims_by_grp, param, monitor) tuples
        """
        oq = self.oqparam
        gsims_by_grp = self.rlzs_assoc.gsims_by_grp_id
        param = dict(
            imtls=oq.imtls,
            truncation_level=oq.truncation_level,
            maximum_distance=oq.maximum_distance)
        logging.info('Populating source_info and splitting in tiles')
        csm.add_infos(csm.get_sources())
        for tile in self.sitecol.split_in_tiles(oq.concurrent_tasks):
            yield csm, tile, gsims_by_grp, param, monitor

    def saving_sources_by_task(self, iterargs):
        """Do nothing"""
        return iterargs


@base.calculators.add('classical_tiling')
class ClassicalTilingCalculator(classical.ClassicalCalculator):
    """
    Classical PSHA tiling calculator
    """
    pre_calculator = 'psha_tiling'
