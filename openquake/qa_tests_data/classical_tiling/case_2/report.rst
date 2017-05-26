Classical Tiling for Turkey reduced
===================================

================================================ ========================
tstation.gem.lan:/mnt/ssd/oqdata/calc_22443.hdf5 Fri May 26 05:37:23 2017
engine_version                                   2.5.0-git4bd15be        
hazardlib_version                                0.25.0-git9fb9c52       
================================================ ========================

num_sites = 83, sitecol = 5.13 KB

Parameters
----------
=============================== ==================
calculation_mode                'classical_tiling'
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 100.0}
investigation_time              10.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            15.0              
complex_fault_mesh_spacing      15.0              
width_of_mfd_bin                0.1               
area_source_discretization      25.0              
ground_motion_correlation_model None              
random_seed                     323               
master_seed                     0                 
=============================== ==================

Input files
-----------
======================== ==========================================================================
Name                     File                                                                      
======================== ==========================================================================
gsim_logic_tree          `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                              
job_ini                  `job.ini <job.ini>`_                                                      
site_model               `site_model.xml <site_model.xml>`_                                        
source                   `as_model.xml <as_model.xml>`_                                            
source                   `fsbg_model.xml <fsbg_model.xml>`_                                        
source                   `ss_model.xml <ss_model.xml>`_                                            
source_model_logic_tree  `source_model_logic_tree.xml <source_model_logic_tree.xml>`_              
structural_vulnerability `structural_vulnerability_model.xml <structural_vulnerability_model.xml>`_
======================== ==========================================================================

Composite source model
----------------------
======================== ====== ======================================================== ====================== ================
smlt_path                weight source_model_file                                        gsim_logic_tree        num_realizations
======================== ====== ======================================================== ====================== ================
AreaSource               0.500  `models/src/as_model.xml <models/src/as_model.xml>`_     complex(5,4,2,4,4,1,0) 4/4             
FaultSourceAndBackground 0.200  `models/src/fsbg_model.xml <models/src/fsbg_model.xml>`_ complex(5,4,2,4,4,1,0) 4/4             
SeiFaCrust               0.300  `models/src/ss_model.xml <models/src/ss_model.xml>`_     complex(5,4,2,4,4,1,0) 0/0             
======================== ====== ======================================================== ====================== ================

Required parameters per tectonic region type
--------------------------------------------
====== ========================================================================== ================= ======================= ============================
grp_id gsims                                                                      distances         siteparams              ruptparams                  
====== ========================================================================== ================= ======================= ============================
4      AkkarBommer2010() CauzziFaccioli2008() ChiouYoungs2008() ZhaoEtAl2006Asc() rhypo rjb rrup rx vs30 vs30measured z1pt0 dip hypo_depth mag rake ztor
9      AkkarBommer2010() CauzziFaccioli2008() ChiouYoungs2008() ZhaoEtAl2006Asc() rhypo rjb rrup rx vs30 vs30measured z1pt0 dip hypo_depth mag rake ztor
====== ========================================================================== ================= ======================= ============================

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=8, rlzs=8)
  4,AkkarBommer2010(): ['<0,AreaSource~AkkarBommer2010asc_@_@_@_@_@_@,w=0.24999999893563138>']
  4,CauzziFaccioli2008(): ['<1,AreaSource~CauzziFaccioli2008asc_@_@_@_@_@_@,w=0.24999999893563138>']
  4,ChiouYoungs2008(): ['<2,AreaSource~ChiouYoungs2008asc_@_@_@_@_@_@,w=0.14285714224893223>']
  4,ZhaoEtAl2006Asc(): ['<3,AreaSource~ZhaoEtAl2006Ascasc_@_@_@_@_@_@,w=0.07142857112446611>']
  9,AkkarBommer2010(): ['<4,FaultSourceAndBackground~AkkarBommer2010asc_@_@_@_@_@_@,w=0.10000000106436867>']
  9,CauzziFaccioli2008(): ['<5,FaultSourceAndBackground~CauzziFaccioli2008asc_@_@_@_@_@_@,w=0.10000000106436867>']
  9,ChiouYoungs2008(): ['<6,FaultSourceAndBackground~ChiouYoungs2008asc_@_@_@_@_@_@,w=0.05714285775106781>']
  9,ZhaoEtAl2006Asc(): ['<7,FaultSourceAndBackground~ZhaoEtAl2006Ascasc_@_@_@_@_@_@,w=0.028571428875533905>']>

Number of ruptures per tectonic region type
-------------------------------------------
========================= ====== ==================== =========== ============ ============
source_model              grp_id trt                  num_sources eff_ruptures tot_ruptures
========================= ====== ==================== =========== ============ ============
models/src/as_model.xml   4      Active Shallow Crust 3           3635         32,481      
models/src/fsbg_model.xml 9      Active Shallow Crust 13          1915         16,635      
========================= ====== ==================== =========== ============ ============

============= ======
#TRT models   2     
#sources      16    
#eff_ruptures 5,550 
#tot_ruptures 49,116
#tot_weight   13,439
============= ======

Informational data
------------------
============================ =================================================================================
classical_tiling.received    tot 121.02 KB, max_per_task 44.82 KB                                             
classical_tiling.sent        csm 218.84 KB, tile 7.18 KB, gsims_by_grp 6.07 KB, param 5.19 KB, monitor 1.21 KB
hazard.input_weight          13,439                                                                           
hazard.n_imts                2 B                                                                              
hazard.n_levels              91 B                                                                             
hazard.n_realizations        3.75 KB                                                                          
hazard.n_sites               83 B                                                                             
hazard.n_sources             31 B                                                                             
hazard.output_weight         7,553                                                                            
hostname                     tstation.gem.lan                                                                 
require_epsilons             0 B                                                                              
============================ =================================================================================

Slowest sources
---------------
====== ============ ============ ============ ========= ========= =========
grp_id source_id    source_class num_ruptures calc_time num_sites num_split
====== ============ ============ ============ ========= ========= =========
4      AS_GEAS343   AreaSource   3,876        13        10        4        
9      FSBG_TRBG103 AreaSource   1,755        4.087     8         2        
9      FSBG_ARAS462 AreaSource   306          0.172     4         1        
9      FSBG_YUBG128 AreaSource   1,809        0.0       0         0        
9      FSBG_ESBG038 AreaSource   675          0.0       0         0        
3      V_CZAS080    AreaSource   14           0.0       0         0        
8      FSBG_PLAS982 AreaSource   1,044        0.0       0         0        
9      FSBG_HUAS132 AreaSource   630          0.0       0         0        
9      FSBG_ITAS307 AreaSource   867          0.0       0         0        
9      FSBG_BGBG090 AreaSource   486          0.0       0         0        
7      V_CZAS127    AreaSource   42           0.0       0         0        
5      AS_IEAS021   AreaSource   16,668       0.0       0         0        
9      FSBG_CHAS098 AreaSource   429          0.0       0         0        
5      AS_ITAS306   AreaSource   6,408        0.0       0         0        
9      FSBG_HRAS215 AreaSource   357          0.0       0         0        
6      AS_FIAS032   AreaSource   20,124       0.0       0         0        
5      AS_BEAS177   AreaSource   1,638        0.0       0         0        
0      AS_SEAS033   AreaSource   2,808        0.0       0         0        
9      FSBG_ESAS971 AreaSource   2,436        0.0       0         0        
8      FSBG_DEAS972 AreaSource   528          0.0       0         0        
====== ============ ============ ============ ========= ========= =========

Computation times by source typology
------------------------------------
================== ========= ======
source_class       calc_time counts
================== ========= ======
AreaSource         17        29    
ComplexFaultSource 0.0       1     
PointSource        0.0       1     
================== ========= ======

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
classical_tiling   4.462 1.358  3.300 6.365 4        
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
total classical_tiling         17        5.645     4     
reading composite source model 0.879     0.0       1     
store source_info              0.073     0.0       1     
managing sources               0.017     0.0       1     
reading site collection        0.006     0.0       1     
saving probability maps        0.005     0.0       1     
aggregate pmaps                5.209E-04 0.0       4     
============================== ========= ========= ======