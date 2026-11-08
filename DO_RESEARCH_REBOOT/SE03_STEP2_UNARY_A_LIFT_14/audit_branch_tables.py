"""Independent BF state/source replay and ALL signed table constraints.
Immutable rotation implementation; no call to construction solver/prepare.
"""
import collections,functools,hashlib,itertools,json,time
from pathlib import Path
from audit_branch_independent2 import trace,freeze
B=Path(__file__).resolve().parent;calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
@functools.lru_cache(None)
def trees(lo,hi):
    if lo>hi:return ('F'+str(hi),)
    return tuple((x,l,r) for x in range(lo,hi+1) for l in trees(lo,x-1) for r in trees(x+1,hi))
def mass_valid(t,M):
    if isinstance(t,str):return True,0
    a,ma=mass_valid(t[1],M);b,mb=mass_valid(t[2],M);mass=ma+mb+(1 if t[0] in M else -1)
    return a and b and mass>=int(t[0] in M),mass
def main():
    global calls
    G=json.loads((B/'branch_grammar2.json').read_text());summary=json.loads((B/'branch_all_construction.json').read_text())
    assert summary['status']=='ALL_CANDIDATES_CONSTRUCTED'
    assert json.loads((B/'branch_independent_audit2.json').read_text())['status']=='PASS_COMPLETE_REVISED_ACTIVE_FRAME_RELATION'
    root=collections.defaultdict(list)
    for a,t in enumerate(G['states']):root[t[0]//1000].append(a)
    trans=[collections.defaultdict(list) for _ in G['states']]
    for H,key in ((1,'H1'),(2,'H2')):
        for a,x,t in G[key]:trans[a][x].append((t,H))
    receipts=[];certified={}
    for k in (9,10,11):
        delta=11-k
        masks={M for M in itertools.combinations(range(1,k+1),6) if M[0]==1 and M[-1]==k and all(0<=2*j-1-x<=delta for j,x in enumerate(M,1))}
        rows=[r for r in summary['reports'] if r['core']==k]
        assert {tuple(r['marks']) for r in rows}==masks and len(rows)==len(masks)
        for row in rows:
            M=tuple(row['marks']);mirror=tuple(sorted(k+1-x for x in M))
            if row['status']=='MIRROR_TRANSPORT':
                assert M>mirror and (k,mirror) in certified
                receipts.append({'core':k,'marks':M,'status':'PROVED_BY_ORDER_REVERSAL','representative':mirror});continue
            assert row['status']=='CANDIDATE_COMPLETE'
            cert=json.loads((B/row['file']).read_text());ts=tuple(t for t in trees(1,k) if t[0] in M and mass_valid(t,set(M))[0]);ids={t:i for i,t in enumerate(ts)}
            assert ts==tuple(map(freeze,cert['BF_trees']));edges=[];adj=collections.defaultdict(list);rank={x:j+1 for j,x in enumerate(M)}
            for b,t in enumerate(ts):
                for x in M:
                    if x==t[0]:continue
                    dest,path,events=trace(t,x);calls+=1;assert calls<2000000
                    if dest not in ids:continue
                    if k==11 and any(e['kind']!='DOUBLE' or e['case'] not in ('LL','RR') or e['G'] not in M or e['P'] in M for e in events):continue
                    q=sum(e['kind']=='DOUBLE' for e in events);e=(b,ids[dest],x,q);edges.append(e);adj[b].append(e)
            assert edges==list(map(tuple,cert['BF_relation']))
            offsets=[];indexpos={a:j for aa in root.values() for j,a in enumerate(aa)};N=0
            for t in ts:offsets.append(N);N+=len(root[rank[t[0]]])
            d=cert['debt'];assert N==len(d)==cert['states'] and N<2000000
            assert min(d)==0 and max(d)==cert['max_debt'] and max(d)<=3
            get=lambda a,b:d[offsets[b]+indexpos[a]]
            maximum=[max(d[offsets[b]:offsets[b]+len(root[rank[t[0]]])]) for b,t in enumerate(ts)]
            minimum=[min(d[offsets[b]:offsets[b]+len(root[rank[t[0]]])]) for b,t in enumerate(ts)]
            checked=collections.Counter();high=set();sectors=0
            for s,t,x,q in edges:
                if q<=4:
                    high.add((s,t,6-q));xx=rank[x]
                    for a in root[rank[ts[s][0]]]:
                        ds=get(a,s)
                        for dest,H in trans[a].get(xx,()):
                            assert 2*H-q+get(dest,t)-ds>=0,(k,M,a,s,x,H)
                            checked['singleton_H'+str(H)]+=1
                else:
                    assert k==11 and q==5
                    for _,end,y,q1 in adj[t]:
                        if q1!=1 or y not in (M[0],M[-1]):continue
                        sectors+=1;high.add((s,end,2));xx,yy=rank[x],rank[y]
                        for a in root[rank[ts[s][0]]]:
                            ds=get(a,s)
                            for mid,h1 in trans[a].get(xx,()):
                                for dest,h2 in trans[mid].get(yy,()):
                                    if h1+h2>3:continue
                                    assert 2*(h1+h2)-6+get(dest,end)-ds>=0,(k,a,s,x,y,h1,h2)
                                    checked['pair_'+str(h1)+str(h2)]+=1
            for s,t,w in high:assert w+minimum[t]-maximum[s]>=0,(k,M,s,t,w)
            r={'core':k,'marks':M,'status':'PASS_ALL_SOURCE_SIGNED_CONSTRAINTS','file':row['file'],
                'sha256':hashlib.sha256((B/row['file']).read_bytes()).hexdigest(),'A_quotient_states':974,'BF_states':len(ts),'BF_edges':len(edges),
                'synchronized_states':N,'max_debt':max(d),'LOW_rows':dict(checked),'HIGH_hyperedges':len(high),'q5_q1_sectors':sectors,
                'working_bank_bound':8+max(d),'source_engine_calls':5*len(ts)}
            out('audit_'+row['file'],r);receipts.append(r);certified[k,M]=r
    out('branch_all_independent_audit.json',{'status':'PASS_ALL_38_MASKS_BY_23_DIRECT_CERTIFICATES_AND_MIRRORS','receipts':receipts,
        'source_engine_calls':calls,'trust':'same agent; independent immutable rotations, all-BST density enumeration, mask derivation and signed arithmetic; shared audited active-frame grammar'})
    print(json.dumps({'status':'PASS_ALL_CORE9_10_11_TABLES','masks':len(receipts),'direct_certificates':len(certified),'calls':calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_branch_tables_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
