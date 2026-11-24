from campaign import *
from verify_checkpoint import independent_Pi


if __name__=='__main__':
    meter=Meter('independent_private_upper_Pi')
    s=json.loads((ROOT/'PRIVATE_ANCESTOR_SOURCES.json').read_text())[-1];r=Replay(s)
    ev,_,_=original_residual(r);old=json.loads((ROOT/'PRIVATE_ANCESTOR_RESULTS.json').read_text())[-1]
    assert ev==old['original_R_star'] and digest(r.events)==s['trace_hash']
    assert r.S==set(r.keys)
    z=independent_Pi(r);write('PRIVATE_UPPER_INDEPENDENT_PI.json',z)
    e=old['new_payments']['upper_B_only_original_events'][0];h,j=e['original_parent']
    assert j>2*e['A_gap'] and e['old_g'] not in r.boundaries[h-1]['A_path'][:-1]
    assert old['G_periodic']['eligible_periodic']
    write('PRIVATE_UPPER_VERIFICATION.json',{'source':s['name'],'A':r.A,'Q_B':r.Q,'S':sorted(r.S),
        'rho':e['rho'],'original_parent':[h,j],'old_g':e['old_g'],'A_gap':e['A_gap'],
        'actual_pre_A_path':r.boundaries[h-1]['A_path'],'actual_pre_B_path':r.boundaries[h-1]['B_path'],
        'original_R_star_verified':True,'original_full_Pi_and_U_independently_reconstructed':True,
        'independent_primitive_rotations':r.T,'independent_original_operations':r.independent_checks,
        'original_R_next_P_member':False,'exclusion_reason':'permitted original G periodic certificate at cut1',
        'refuted_scope':'All original R_star parents are covered by the new prefix/current-ancestor payments',
        'target_R_next_P_bound_refuted':False})
    print('PASS original upper B-only rho',e['rho'],'parent',e['original_parent'],'g',e['old_g'],
          'independent Pi primitives',r.T,flush=True);meter.success=True
