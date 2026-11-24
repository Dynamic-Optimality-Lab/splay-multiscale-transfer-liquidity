from core import *
from types import SimpleNamespace
from verify_checkpoint import compressed_domain_check


if __name__=='__main__':
    meter=Meter('CONT01_lossless_large_source_verification')
    z=json.loads((ROOT/'INTRINSIC5_RESULTS.json').read_text());tr=json.loads((ROOT/z['trace_file']).read_text());s=tr['source']
    assert digest(tr['events'])==s['trace_hash']
    for sha,st in tr['states'].items():assert digest(st)==sha
    rows=[]
    for b in tr['boundaries']:
        bb={k:v for k,v in b.items() if not k.endswith('_state_sha256')}
        for k in ('pre_A','pre_B','post_A','post_B'):bb[k]=tr['states'][b[k+'_state_sha256']]
        rows.append(bb)
    assert [[r['tag'],r['x']] for r in rows]==s['operations']
    for i,row in enumerate(rows):
        for actor in ('A','B'):assert row['pre_'+actor]==rows[i-1]['post_'+actor]
        if row['tag']=='D':assert row['pre_B']==row['post_B']
    assert rows[0]['pre_A']==rows[-1]['post_A']==s['initial_A']==s['closing_A']
    assert rows[0]['pre_B']==rows[-1]['post_B']==s['initial_B']==s['closing_B']
    assert sum(r['a'] for r in rows)==s['A']==z['A']
    assert sum(r['q'] for r in rows)==s['Q_B']==z['Q_B']
    sys.path.insert(0,str(ROOT.parents[2]/'python'))
    from independent import splay as ind
    r=SimpleNamespace(boundaries=rows,ind=ind)
    r.as_tuple=lambda tree:Replay.as_tuple(r,tree)
    counts={}
    for name,key in [('G','normalized'),('H','hard_normalized')]:
        n=z[key];counts[name]=compressed_domain_check(r,n)
        assert n['initial_B']==n['ending_B']
        assert all(e['consumer'] in n['retained_KEEP'] for e in z['R_star'])
    result={'source':s['name'],'complete_original_operation_states_linked':len(rows),
        'original_trace_hash_verified':True,'paired_closure_verified':True,
        'full_state_pool_hashes_verified':len(tr['states']),'original_R_star_count':len(z['R_star']),
        'all_original_R_star_consumers_retained_in_G_and_H':True,
        'compressed_domain_immutable_accesses':counts,
        'full_original_tuple_operations_previously_verified':z['independent_operations'],
        'qualification':'New full primitive independent Pi/U check is on the65-key witness only; this large source retains the pinned original Pi/U certification and independent complete-operation tuple checks.'}
    write('LARGE_SOURCE_VERIFICATION.json',result);meter.success=True
    print('PASS',len(rows),'original states; all',len(z['R_star']),'original residual gaps retained;',counts,flush=True)
