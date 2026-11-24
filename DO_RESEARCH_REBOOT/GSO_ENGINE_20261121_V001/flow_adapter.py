"""Working adapter to the frozen original-U exact flow and independent checker."""
import sys
from kernel import ROOT,OLD,SOURCES,readonly_module,dump


def run(out):
    # The old module imports these names. Both bindings are sealed read-only
    # helpers; no prior writer or main routine is invoked.
    sys.modules['replay']=OLD;sys.modules['sources']=SOURCES
    flow=readonly_module('gso_pinned_exact_flow',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_PIVOT_DONOR_20261121_V001/flow.py')
    checker=readonly_module('gso_pinned_independent_flow_checker',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_PIVOT_DONOR_20261121_V001/verify.py')
    wanted={'W_2_1','G_4_1_L31_r4_z1','H3_rho2_Y1_copies2'};refs=[r for r in SOURCES.references() if r['name'] in wanted];assert len(refs)==3
    results=[]
    for i,ref in enumerate(refs):
        s=SOURCES.canonical(ref);rep=OLD.replay(s);allocation=flow.optimize(rep);interval=flow.interval_cut(rep,1)
        saved={'index':i,'ref':ref,'name':s['name'],'physical_keys':rep['keys'],'S':rep['S'],'full_carrier':rep['full_carrier'],
               'root_rotations_only':rep['root_rotations_only'],'A':rep['A'],'Q_B':rep['Q_B'],'original_ops':len(s['operations']),
               'period_rotations':rep['rotations'],'prefix_rotations':rep['reach_rotations'],'period_clock':rep['period_clock'],
               'demands':rep['demands'],'allocation':allocation,'split_pivot_interval_test':interval}
        path=out/f'flow_case_{i}.json';dump(path,saved);verified=checker.validate(path);results.append(verified)
    result={'status':'FINITE-EXACT legacy-rule integration; no new universal theta_1 budget','cases':results,'independent_original_Pi_and_LCA_checks':True}
    dump(out/'FLOW_ADAPTER_VERIFICATION.json',result);return result
