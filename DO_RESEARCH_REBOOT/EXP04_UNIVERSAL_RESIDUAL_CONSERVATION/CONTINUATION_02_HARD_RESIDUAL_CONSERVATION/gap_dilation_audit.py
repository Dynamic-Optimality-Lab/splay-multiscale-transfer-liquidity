from source_search import common_dilated
from new_payments import actual_payments,compact_trace,intern_original_states
from fast_physics import *


def dilated(base,stride,copies=3):
    k=len(base['initial_B']['children']);diag,active=common_dilated(k,stride);n=len(diag['children'])
    phi=lambda x:1+(x-1)*stride
    V=[[tag,phi(x)] for tag,x in base['operations']]
    restore=ops('K',range(1,n+1))+ops('K',active[-2::-1])
    return {'name':f'C02_dilate_{k}_stride{stride}_copies{copies}','family':'fixed_active_source_gap_refinement',
        'initial_A':diag,'initial_B':diag,'diagonal_initial':diag,'reaching_prefix':[],
        'operations':V*copies+restore,'active_keys':active,'stride':stride,'copies':copies,'V_length':len(V),
        'base_source':base['name'],'restoration':restore,'reachability':'complete common diagonal, empty prefix',
        'full_S_reason':'physical increasing restoration followed by the active minimum; every physical key genuine'}


if __name__=='__main__':
    meter=Meter('gap_dilation_localization_audit');out=[];sources=[]
    base=next(s for s in json.loads((ROOT/'HELPER_SOURCES.json').read_text()) if 'helper5_' in s['name'])
    for stride in (9,129):
        s=dilated(base,stride);f=physical_replay(s)
        # A single certificate already falsifies the candidate's B3/B4 escape.
        globalG=skeleton_cost(f,variant='G');globalH=skeleton_cost(f,variant='H')
        v=len(base['operations']);begin=v;end=2*v
        local={'source':{**s,'operations':s['operations'][begin:end]},'rows':f['rows'][begin:end],
               'A':sum(r['a'] for r in f['rows'][begin:end]),'Q_B':sum(r['q'] for r in f['rows'][begin:end])}
        # Each row operation position remains original; cut0 means local B
        # pre-state = local last post-state, since this actual block is closed.
        localG=skeleton_cost(local,variant='G');D=localG['J_size']+len(skeleton_indices(local,variant='G'))
        targets=[]
        for i in skeleton_indices(local,variant='G'):
            x=local['rows'][i]['x']
            if not targets or targets[-1]!=x:targets.append(x)
        st=decode(local['rows'][-1]['B_code'],len(s['initial_B']['children']));J=path_hull(Tree(st),targets)
        ranks={x:i for i,x in enumerate(sorted(J))};L=sum(abs(ranks[y]-ranks[x]).bit_length() for x,y in zip(targets,targets[1:]))
        D=len(J)+len(targets)+L
        assert D==658 and local['A']==1546
        row={'source':s['name'],'population':len(s['initial_B']['children']),'operations':len(s['operations']),
             'A':f['A'],'Q_B':f['Q_B'],'G_periodic':globalG,'H_periodic':globalH,
             'middle_copy_local_G':{'first_operation':begin+1,'last_operation':end,'D':D,'A':local['A'],
                 'J_size':len(J),'integer_rank_travel':L,'eligible_5A':D<=5*local['A']},
             'physical_complete_closure':True,'original_Pi_status':'not yet run'}
        s.update(A=f['A'],Q_B=f['Q_B'],closing_A=s['initial_A'],closing_B=s['initial_B'])
        sources.append(s);out.append(row);write('DILATED_SOURCES.json',sources);write('DILATED_RESULTS.json',out)
        print(s['name'],'N',row['population'],'A',f['A'],'local G D',D,'A',local['A'],
              'global G',globalG['B_cyclic'],'global H',globalH['B_cyclic'],flush=True)
        del f
        if stride==9:
            pool=intern_original_states();r=Replay(s);ev,_,_=original_residual(r)
            row['original_R_star']=ev;row['original_R6']=[p for p in r.pairs if p['class']=='R6']
            row['independent_original_operations']=r.independent_checks;row['original_Pi_status']='full original Pi/U/cohorts/R6 and R_* classified'
            h=v+646;row['middle_target_consumers']=[e for e in ev if e['consumer']==h]
            row['middle_hard_gap']=keep_gaps(r)[h]
            row['middle_B_parent_certificates']=[r.U[tuple(e['original_parent'])] for e in row['middle_target_consumers']]
            assert row['middle_target_consumers'] and row['middle_hard_gap']['Q_at_KEEP']==4 and row['middle_hard_gap']['A']==1
            row['trace_file']='DILATED_FULL_ORIGINAL_TRACE.json';compact_trace(r,ev,row['trace_file'])
            write('DILATED_RESULTS.json',out);del r;pool.clear()
    meter.success=True;meter.details['new_complete_original_sources']=len(sources)
