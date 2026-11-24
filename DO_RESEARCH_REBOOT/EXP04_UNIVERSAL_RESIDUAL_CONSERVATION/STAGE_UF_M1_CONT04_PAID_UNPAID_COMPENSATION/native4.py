from base4 import *
from adapterc import adapter

def original_star(r):
    import exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core
    for mod in (exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core):mod.ROOT=ROOT
    c=exp03_core.current_classification(r,save=True)
    old=exp04_core.restart_module.restart_analysis(r,c['unhandled'],exp04_core.actual_mismatch_episodes(r))
    paid={digest(e['rho']) for e in old['paid_original_gaps']}
    return [e for e in c['unhandled'] if digest(e['rho']) not in paid]
