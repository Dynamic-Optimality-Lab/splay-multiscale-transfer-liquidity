from source_search import common_dilated
from fast_physics import *


if __name__=='__main__':
    meter=Meter('large_nonrecurrent_adaptive_lift')
    p=next(s for s in json.loads((ROOT/'ADAPTIVE_SOURCES.json').read_text()) if s['name']=='C02_adaptive_n129_seed1')
    stride=127;diag,active=common_dilated(129,stride);n=len(diag['children']);phi=lambda x:1+(x-1)*stride
    body=[[tag,phi(x)] for tag,x in p['unclosed_active_word']]
    restore=ops('K',range(1,n+1))+ops('K',active[-2::-1])
    s={'name':'C02_adaptive_nonclosed_129_stride127','family':'nonrecurrent_A_shallow_B_four_double_body_with_real_full_restoration',
        'initial_A':diag,'initial_B':diag,'diagonal_initial':diag,'reaching_prefix':[],
        'operations':body+restore,'body_length':len(body),'active_keys':active,'stride':stride,
        'full_S_reason':'physical increasing restoration plus final active minimum',
        'reachability':'common diagonal, empty prefix'}
    f=physical_replay(s);s.update(A=f['A'],Q_B=f['Q_B'],closing_A=diag,closing_B=diag)
    write('ADAPTIVE_LIFT_SOURCE.json',s)
    results=[]
    for variant in ('raw','G','H'):
        indices=skeleton_indices(f,variant=variant);targets=[];seq=[]
        for i in indices:
            x=f['rows'][i]['x']
            if not targets or targets[-1]!=x:targets.append(x);seq.append(i)
        J=path_hull(Tree(diag),targets);ranks={x:i for i,x in enumerate(sorted(J))}
        cost=periodic_cost(targets,J)
        bodyL=sum(abs(ranks[targets[k]]-ranks[targets[k-1]]).bit_length()
                   for k in range(1,len(targets)) if seq[k]<len(body) and seq[k-1]<len(body))
        bodyM=sum(i<len(body) for i in seq)
        result={'variant':variant,**cost,'A':f['A'],'eligible_periodic':cost['B_cyclic']<=10*f['A'],
                'initial_path_union_size':len(J),'retained_original_operations':[i+1 for i in indices],
                'retained_body_blocks':bodyM,'retained_body_integer_rank_travel':bodyL,
                'actual_body_A':sum(r['a'] for r in f['rows'][:len(body)]),
                'guard_count':sum(r.get('guard_'+variant,False) for r in f['rows'])}
        results.append(result)
        print(variant,'J',len(J),'cost',cost['B_cyclic'],'A',f['A'],'funded',result['eligible_periodic'],
              'body cost',bodyM+bodyL,'body A',result['actual_body_A'],flush=True)
    write('ADAPTIVE_LIFT_RESULTS.json',{'source':s['name'],'population':n,'operations':len(s['operations']),
        'A':f['A'],'Q_B':f['Q_B'],'physical_complete_paired_closure':True,'variants':results,
        'original_Pi_status':'not run unless all necessary periodic alternatives survive',
        'simultaneous_escape_claimed':False})
    meter.success=True;meter.details.update(new_complete_original_sources=1,
        distinct_complete_B_states=f['distinct_full_B_codes'])
