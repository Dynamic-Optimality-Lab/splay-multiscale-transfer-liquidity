"""Full A branch quotient sufficient certificate on first core9 mask.
LOW is complete active-frame grammar; wider HIGH is conservative.
Adverse quotient paths are not presumed to compose in original histories.
"""
import collections,json,sys,time
from array import array
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
started=time.process_time();LIMIT=float(sys.argv[1])-3
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    G=json.loads((B/'branch_grammar.json').read_text());bf=json.loads((OLD/'bf9_comparison.json').read_text());summary=bf['mask_summaries'][0]
    nB=summary['states'];nA=len(G['states']);size=nA*nB;assert size<2000000
    marks=summary['marks'];rank={x:i+1 for i,x in enumerate(marks)};ar=collections.defaultdict(list)
    for a,t in enumerate(G['states']):ar[t[0]//1000].append(a)
    adjB=[[] for _ in range(nB)]
    for s,t,x,Q in bf['edges']:
        if s<nB:adjB[s].append((t,rank[x],Q))
    adjA=[collections.defaultdict(list) for a in range(nA)]
    for H,name in ((1,'H1'),(2,'H2')):
        for a,x,b in G[name]:adjA[a][x].append((b,H))
    valid=[a*nB+b for b,t in enumerate(bf['trees'][:nB]) for a in ar[rank[t[0]]]]
    assert len(valid)<2000000
    def solve(K,high):
        d=array('b',[-9])*size;proof=array('i',[-1])*size;inside=bytearray(size);ql=collections.deque(valid);nodes=[]
        maximum=[0]*nB;maxnode=[-1]*nB;hq=collections.deque();hset=set();updates=0;stop=None
        for s in valid:d[s]=0;inside[s]=1
        def raise_to(dst,new,src,meta):
            nonlocal updates,stop
            if new<=d[dst]:return
            rec={'source':src,'target':dst,'source_value':d[src],'required':new,'parent':proof[src],'edge':meta};nodes.append(rec);j=len(nodes)-1
            if new>K:
                path=[]
                while j>=0:path.append(nodes[j]);j=nodes[j]['parent']
                path.reverse();walk=[path[0]['source']]+[z['target'] for z in path];total=0;previous={walk[0]:(0,0)};cycle=None
                for i,z in enumerate(path,1):
                    total+=z['edge']['Q']-2*z['edge']['H'];v=z['target']
                    if v in previous and total>previous[v][1]:cycle=path[previous[v][0]:i];break
                    if v not in previous:previous[v]=(i,total)
                stop={'kind':'BOUND_EXCEEDED','required':new,'bound':K,'path':path,'positive_cycle':cycle,
                    'scope':'sufficient comparison only; no original path realization assumed'};return
            if len(nodes)>=3900000:stop={'kind':'DAG_RESERVE_STOP','updates':updates};return
            d[dst]=new;proof[dst]=len(nodes)-1;updates+=1
            if not inside[dst]:ql.append(dst);inside[dst]=1
            b=dst%nB
            if new>maximum[b]:
                maximum[b]=new;maxnode[b]=dst
                if high and b not in hset:hq.append(b);hset.add(b)
        while (ql or hq) and stop is None:
            if time.process_time()-started>LIMIT:stop={'kind':'CPU_RESERVE_STOP','updates':updates};break
            if high and hq:
                s=hq.popleft();hset.remove(s)
                for b,x,Q in adjB[s]:
                    lower=maximum[s]+Q-6
                    if lower<=0:continue
                    for a in ar[x]:
                        raise_to(a*nB+b,lower,maxnode[s],{'H':3,'Q':Q,'x':x,'HIGH':True})
                        if stop:break
                    if stop:break
                continue
            sid=ql.popleft();inside[sid]=0;a,b=divmod(sid,nB);ds=d[sid]
            for bb,x,Q in adjB[b]:
                for aa,H in adjA[a].get(x,()):
                    raise_to(aa*nB+bb,ds+Q-2*H,sid,{'H':H,'Q':Q,'x':x,'HIGH':False})
                    if stop:break
                if stop:break
        r={'bound':K,'HIGH_included':high,'status':'FEASIBLE_EXACT' if stop is None else 'CANDIDATE_NOT_CERTIFIED',
            'stop':stop,'updates':updates,'DAG_nodes':len(nodes)}
        if stop is None:
            checked=0
            for sid in valid:
                a,b=divmod(sid,nB)
                for bb,x,Q in adjB[b]:
                    for aa,H in adjA[a].get(x,()):assert 2*H-Q+d[aa*nB+bb]-d[sid]>=0;checked+=1
            if high:
                minimum=[min(d[a*nB+b] for a in ar[rank[t[0]]]) for b,t in enumerate(bf['trees'][:nB])]
                for b in range(nB):
                    for bb,x,Q in adjB[b]:assert 6-Q+minimum[bb]-maximum[b]>=0
            r.update({'valid_states':valid,'debt':[d[s] for s in valid],'max_debt':max(d),'LOW_rows_verified':checked})
        return r
    attempts=[]
    for K,high in ((2,False),(21,True)):
        r=solve(K,high);attempts.append(r)
        if r['status']=='FEASIBLE_EXACT' or r['stop']['kind'].endswith('STOP'):break
    result={'status':'FULL_A_QUOTIENT_CANDIDATE_FOUND' if attempts[-1]['status']=='FEASIBLE_EXACT' else 'FULL_A_QUOTIENT_REQUIRES_FURTHER_WORK',
        'core':9,'BF_marks':marks,'A_branch_states':nA,'BF_states':nB,'valid_pair_states':len(valid),'attempts':attempts,
        'scope':'complete source-frame sufficient projection, first core9 mask; not all21 masks or other cores',
        'source_engine_calls':0,'no_CD_refutation':'quotient may forget unary configurations; paths not source-realized'}
    out('branch9_candidate.json',result)
    print(json.dumps({'status':result['status'],'states':len(valid),'attempts':[{'bound':a['bound'],'HIGH':a['HIGH_included'],'status':a['status'],
        'Dmax':a.get('max_debt'),'stop':a['stop']['kind'] if a['stop'] else None,
        'cycle':bool(a['stop'] and a['stop'].get('positive_cycle'))} for a in attempts]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_branch9_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})
