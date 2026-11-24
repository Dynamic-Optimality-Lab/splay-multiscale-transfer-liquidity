from campaign4 import *
from packed_states import install,materialize
from width_attack import construct

if __name__=='__main__':
    meter=Meter('storage_check');out=[]
    for p in (3,4):
        s=construct(p,left=3,right=3);r=Replay(s)
        baseline={'events':digest(r.events),'U':digest({str(k):v for k,v in r.U.items()}),
            'pairs':digest(r.pairs),'boundaries':r.boundaries,'A':r.A,'Q':r.Q,
            'original_R_star':original_residual(r)[0]}
        pool,restore=install(Tree)
        try:
            t=Replay(s)
            assert digest(t.events)==baseline['events']
            assert digest({str(k):v for k,v in t.U.items()})==baseline['U']
            assert digest(t.pairs)==baseline['pairs'] and (t.A,t.Q)==(r.A,r.Q)
            assert original_residual(t)[0]==baseline['original_R_star']
            for x,y in zip(r.boundaries,t.boundaries):
                assert x==y
                for field in ('pre_A','pre_B','post_A','post_B'):
                    assert x[field]==materialize(y[field])
                    assert digest(x[field])==digest(y[field])
            out.append({'source':s['name'],'all_complete_operation_states_identical':True,
                'all_original_primitive_events_SET_Pi_U_pairs_identical':True,'operations':len(s['operations']),
                'primitive_event_sha256':digest(t.events)})
        finally:restore()
    write('STORAGE_CHECK.json',out);print('PASS lossless storage against unchanged dense original replay',flush=True)
    meter.success=True
