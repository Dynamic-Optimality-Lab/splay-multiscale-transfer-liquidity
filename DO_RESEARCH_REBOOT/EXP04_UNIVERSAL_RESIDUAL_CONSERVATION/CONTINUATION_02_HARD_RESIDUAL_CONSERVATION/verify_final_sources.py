from delivery_support import *
from independent_path_audit import check
from fast_physics import physical_replay,path_hull,Tree


if __name__=='__main__':
    meter=Meter('final_source_audit')
    sources,scopes,_=source_archive();rows=[];grammar=[]
    for s in sources:
        z=check(s)
        M={x for tag,x in s['operations'] if tag=='K'}
        S=path_hull(Tree(s['initial_B']),M)
        assert len(S)==len(s['initial_B']['children'])
        assert s['initial_A']==s['initial_B'] and not s.get('reaching_prefix')
        z.update(original_S_is_full_physical_population=True,common_diagonal_reachability=True)
        rows.append(z);write('FINAL_COMPLETE_SOURCE_VERIFICATION.json',rows)
        if 'adaptive' in s['name']:
            f=physical_replay(s)
            prefix=s.get('prefix_length',129)
            body=s.get('body_length',len(s['unclosed_active_word']) if 'unclosed_active_word' in s else 0)
            core=f['rows'][prefix:body];rest=f['rows'][body:]
            maxq=max((r['q'] for r in core),default=0)
            assert maxq<=4
            actual_restoration_A=sum(r['a'] for r in rest)
            assert actual_restoration_A>=len(S)
            assert all(tag=='K' for tag,x in s['operations'][:prefix])
            assert all(f['rows'][i]['q']<=f['rows'][i]['a'] for i in range(prefix))
            grammar.append({'source':s['name'],'body_first_operation':prefix+1,
                'body_last_operation':body,'maximum_original_body_q_B':maxq,
                'actual_restoration_A':actual_restoration_A,'population':len(S),
                'q_cap_and_restoration_A_lower_bound_verified':True})
        if s['name']=='C02_missing_root_coupling_control':
            f=physical_replay(s);assert not any(r['guard_G'] for r in f['rows'])
        print('PASS full original physical source',s['name'],flush=True)
    write('RESTRICTED_GRAMMAR_VERIFICATION.json',grammar)
    meter.success=True;meter.details.update(full_original_sources=len(rows),restricted_grammar_sources=len(grammar))
