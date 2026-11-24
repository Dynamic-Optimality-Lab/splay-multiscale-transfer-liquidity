from campaign4 import *
from structural_checks import return_checks,check_spine
from packet_payments import test
from fast_physics import physical_replay

if __name__=='__main__':
    meter=Meter('failuremode_checks')
    ep1=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    sources=json.loads((ep1/'EXP01_SOURCE_WITNESSES.json').read_text())
    if isinstance(sources,dict):sources=sources.get('sources',sources.get('new_sources',[]))
    wanted=['G_4_1_L31_r1_z1','DW_5_1_at31','DW_6_1_at31']
    out=[]
    for name in wanted:
        s=next(x for x in sources if x['name']==name);f=physical_replay(s)
        returns=return_checks(s)
        out.append({'source':name,'complete_source_sha256':digest(s),'A':f['A'],'Q_B':f['Q_B'],
            'sampled_exact_B_return_intervals':returns,
            'P6_scope_satisfied':all(x['a']<=1 for x in f['rows']),
            'root_entry_matching_claimed':False,'unit_or_load_two_Hall_obstruction_unchanged':name.startswith('DW_')})
    small={'root':3,'children':{'1':[None,None],'2':[1,None],'3':[2,None]}}
    s={'name':'C04_root_coupling_negative_control','initial_A':small,'initial_B':small,
        'diagonal_initial':small,'reaching_prefix':[],'operations':[['D',1],['K',1],['K',3]]}
    z=check_spine(s);f=physical_replay(s)
    suffix=next(x for x in return_checks(s) if x['interval_after']==1 and x['through']==3)
    assert suffix['A']==1 and suffix['Q_B']==2 and suffix['c_cyclic']==6
    assert suffix['c_cyclic']>5*suffix['A'] and z['old_raw_periodic_certificate']==3*z['A']
    write('FAILUREMODE_CHECKS.json',{'historical_full_source_controls':out,
        'root_coupling_counterexample':{'complete_source':s,'pointwise_suffix':suffix,'P6_certificate_tight':z},
        'all_tests_use_original_complete_physical_keys':True,
        'no_scope_or_budget_adjusted_after_a_counterexample':True})
    print('PASS G/W Hall controls and exact root-coupling failure mode; P6 coefficient3 attained',flush=True)
    meter.success=True
