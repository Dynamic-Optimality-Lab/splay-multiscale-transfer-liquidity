from epoch_payment import *
from exp04_monotone import monotone_analysis
from fast_physics import physical_replay,skeleton_cost


def audit(r,star):
    eps,_=psi_episodes(r);carrier=comparisons(r,star,eps)
    cids={digest(e['rho']) for e in carrier['paid']}
    after=[e for e in star if digest(e['rho']) not in cids]
    mono=monotone_analysis(r,after,eps);mids={digest(e['rho']) for e in mono['paid']}
    after=[e for e in after if digest(e['rho']) not in mids]
    gaps=keep_gaps(r);prefix=[e for e in after if e['original_parent'][1]<=2*gaps[e['consumer']]['A']]
    pids={digest(e['rho']) for e in prefix};C=[e for e in after if digest(e['rho']) not in pids]
    own=[e for e in C if r.U[tuple(e['original_parent'])]['g'] in r.boundaries[e['consumer']-1]['A_path'][:-1]]
    oids={digest(e['rho']) for e in own};afterown=[e for e in C if digest(e['rho']) not in oids]
    renewal=from_replay(r,C);eids={digest(e['rho']) for e in renewal['selected_original_gaps']}
    assert oids<=eids
    assert r.S==set(r.keys)
    f=physical_replay(r.source);variants=[skeleton_cost(f,variant=v) for v in ('raw','G','H')]
    positive=next((z for z in variants if z['eligible_periodic']),None)
    if positive:upper=[];renew=[];hybrid=afterown
    elif not afterown:upper=[];renew=[];hybrid=[]
    else:upper=None;renew=None;hybrid=None
    # Missing a tested positive cut alone is never a full periodic/local negative certificate.
    assigned=[carrier['paid'],mono['paid'],prefix,own]+([hybrid] if hybrid is not None else [])
    ids=[digest(e['rho']) for block in assigned for e in block];assert len(ids)==len(set(ids))
    if upper is not None:assert set(ids)=={digest(e['rho']) for e in star}
    return {'source':r.source['name'],'A':r.A,'Q_B':r.Q,'original_R_star':star,
        'ordered_original_assignments':{'1_frozen_carrier':carrier['paid'],'2_frozen_skipped_rank':mono['paid'],
            '3_original_B_prefix':prefix,'4_pre_A_path_old_g':own,'5_old_hybrid':hybrid},
        'C_after_frozen_and_prefix':C,'first_use_E_C':renewal,
        'strict_new_E_C_minus_own':[e for e in renewal['selected_original_gaps'] if digest(e['rho']) not in oids],
        'positive_old_periodic_certificate':positive,
        'tested_cut1_variants':[{k:v for k,v in z.items() if k!='retained_original_operations'} for z in variants],
        'literal_requested_R_upper':upper,'literal_R_renew':renew,
        'unknown_if_no_positive_cut_and_unfinished_local_enumeration':upper is None,
        'disjoint_assignment_verified':True,'exact_Q_coefficient':'47+48 C_seq+102 C_DF'}


if __name__=='__main__':
    meter=Meter('ordered_accounting')
    s=json.loads((C2/'PRIVATE_ANCESTOR_SOURCES.json').read_text())[0]
    r=Replay(s);star,_,_=original_residual(r);z=audit(r,star)
    write('PRIVATE_ORDERED_ACCOUNTING.json',z)
    print('private193 C after frozen/prefix',len(z['C_after_frozen_and_prefix']),
          'new E minus own',len(z['strict_new_E_C_minus_own']),
          'old hybrid funded',z['positive_old_periodic_certificate'] is not None,flush=True)
    meter.success=True
