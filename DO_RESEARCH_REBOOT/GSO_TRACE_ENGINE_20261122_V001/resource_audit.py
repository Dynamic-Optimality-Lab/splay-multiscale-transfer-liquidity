"""Literal original-unit vouchers and path-decomposed finite bank funding."""
import sys
from collections import Counter,defaultdict,deque
sys.dont_write_bytecode=True
import trace as X
import trace_teacher as T


def vouchers(z):
    genuine=[r['id'] for r in z['operations'] if r['k']];n=len(z['operations']);out={};seen=set()
    for at,op in enumerate(genuine):
        previous=genuine[at-1];gap=list(range(previous+1,op+1)) if previous<op else list(range(previous+1,n+1))+list(range(1,op+1))
        eligible=[s['id'] for k in gap for s in z['steps'][z['operations'][k-1]['steps'][0]:z['operations'][k-1]['steps'][1]] if s['a']]
        assert eligible,'Distinct consecutive B roots force an actual A root change in the incoming gap.'
        chosen=tuple(eligible[0]);assert chosen not in seen;seen.add(chosen);out[op]=list(chosen)
    assert len(out)==z['K_B']<=z['A']
    return out


def decompose(z,cert):
    T.verify_bank(z,cert);ev=T.events(z);v=vouchers(z);flow={(u,w):amt for u,w,amt in cert['positive_flows']};adj=defaultdict(list)
    for u,w in flow:adj[u].append(w)
    assignments=[];loads=Counter();byhub={f'e{i}':e for i,e in enumerate(ev)}
    # Decompose the source-to-sink portion of exact integer flow. Any unused
    # pure circulation is ignored and cannot supply a demand in this map.
    while any(amt>0 for (u,w),amt in flow.items() if u=='s'):
        queue=deque(['s']);parent={'s':None}
        while queue and 't' not in parent:
            u=queue.popleft()
            for w in adj[u]:
                if flow[u,w]>0 and w not in parent:parent[w]=u;queue.append(w)
        assert 't' in parent
        path=[];at='t'
        while parent[at] is not None:path.append((parent[at],at));at=parent[at]
        path.reverse();supply=byhub[path[0][1]];consumer=byhub[path[-1][0]]
        assert consumer['q']==1
        donor=supply['id'] if supply['a'] else v[supply['id'][1]]
        assert supply['a'] or supply['k'];assert donor[0]=='A'
        for edge in path:flow[edge]-=1
        loads[tuple(donor)]+=1;assignments.append({'original_B_double':consumer['id'],'original_A_unit':donor,'via_KEEP_voucher':bool(supply['k']),'path_nodes':[path[0][0]]+[w for _,w in path]})
    assert len(assignments)==cert['paid'] and len({tuple(a['original_B_double']) for a in assignments})==cert['paid']
    assert max(loads.values(),default=0)<=cert['c']+cert['d']
    if cert['status']=='FINITE_EXACT_BANK':assert len(assignments)==z['Q_B']
    return {'status':'FINITE_EXACT_RESOURCE_ASSIGNMENT','name':z['source']['name'],'paid':cert['paid'],'Q_B':z['Q_B'],'c':cert['c'],'d':cert['d'],'maximum_actual_A_load':max(loads.values(),default=0),'voucher_original_A_units':{str(k):vv for k,vv in v.items()},'assignments':assignments,'prefix_credit':0,'virtual_credit':0,'universal':'OPEN'}


def main():
    out=[]
    for i in range(18):
        z=X.K.load(X.HERE/f'run_001/trace_{i:02d}.json.gz');b=X.K.load(X.HERE/f'run_001/bank_{i:02d}.json.gz');r=decompose(z,b);X.write(f'resources_001/source_{i:02d}.json.gz',r)
        out.append({k:v for k,v in r.items() if k not in ('assignments','voucher_original_A_units')})
    X.write('resources_001/SUMMARY.json',{'cases':out,'universal_CD':'OPEN','scope':'Exact resource provenance on finite complete sources. No source-uniform bank policy has been proved.'});print({'finite_assignments':sum(r['paid'] for r in out),'sources':len(out)})


if __name__=='__main__':main()
