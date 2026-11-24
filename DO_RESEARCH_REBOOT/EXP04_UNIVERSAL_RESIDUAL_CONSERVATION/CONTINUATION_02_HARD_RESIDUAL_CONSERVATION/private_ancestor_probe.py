from source_search import common_dilated
from new_payments import actual_payments,compact_trace
from fast_physics import *


if __name__=='__main__':
    meter=Meter('private_B_ancestor_upper_parent_probe');sources=[];out=[]
    base=json.loads((C1/'OWNERSHIP_SOURCES.json').read_text())[0]
    for stride in (3,5,9,17):
        diag,active=common_dilated(65,stride);n=len(diag['children']);phi=lambda x:1+(x-1)*stride
        private=phi(5)-1;body=[[tag,phi(x)] for tag,x in base['operations']]
        body=body[:643]+[['D',private]]+body[643:];assert body[645]==['K',phi(5)]
        body[645]=['K',private]
        restore=ops('K',range(1,n+1))+ops('K',active[-2::-1])
        s={'name':f'C02_private_h_stride{stride}','family':'private_gap_first_hit_with_A_shortcut',
           'initial_A':diag,'initial_B':diag,'diagonal_initial':diag,'reaching_prefix':[],
           'operations':body+restore,'active_keys':active,'private_hit':private,
           'target_consumer':646,'stride':stride,'real_full_restoration':restore,
           'reachability':'complete common diagonal, empty prefix'}
        f=physical_replay(s);r=Replay(s);ev,_,_=original_residual(r);payments=actual_payments(r,ev)
        G=skeleton_cost(f,variant='G');H=skeleton_cost(f,variant='H')
        s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
        row={'source':s['name'],'A':r.A,'Q_B':r.Q,'population':n,'original_R_star':ev,
             'new_payments':payments,'G_periodic':G,'H_periodic':H,
             'independent_original_operations':r.independent_checks,
             'target_A_path':r.boundaries[645]['A_path'],'target_B_path':r.boundaries[645]['B_path'],
             'target_A_gap':keep_gaps(r)[646]}
        upper=payments['upper_B_only_original_events']
        if upper:
            row['trace_file']='PRIVATE_UPPER_FULL_TRACE.json';compact_trace(r,ev,row['trace_file'])
            row['upper_U_certificates']=[{'event':e,'U':r.U[tuple(e['original_parent'])]} for e in upper]
        out.append(row);sources.append(s);write('PRIVATE_ANCESTOR_SOURCES.json',sources);write('PRIVATE_ANCESTOR_RESULTS.json',out)
        print('stride',stride,'N',n,'R*',len(ev),'upper B-only',len(upper),
              'target q',r.boundaries[645]['q'],'A_gap',row['target_A_gap']['A'],
              'periodic G funded',G['eligible_periodic'],flush=True)
        if upper:break
    meter.success=True;meter.details['complete_original_sources']=len(sources)
