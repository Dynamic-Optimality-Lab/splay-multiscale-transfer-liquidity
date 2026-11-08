"""MD35 source-event loss graph using accepted original rotation records."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def subtree(t,x):
    while t is not None and t[0]!=x:t=t[1] if x<t[0] else t[2]
    return t
def marked(t,M):
    if t is None:return set()
    return ({t[0]}&M)|marked(t[1],M)|marked(t[2],M)
def maximum(graph):
    owner={};match={}
    def add(d,seen):
        for u in sorted(graph[d]):
            if u in seen:continue
            seen.add(u)
            if u not in owner or add(owner[u],seen):owner[u]=d;match[d]=u;return True
        return False
    for d in sorted(graph):add(d,set())
    T=set(graph)-set(match);todo=list(T);N=set()
    while todo:
        for u in graph[todo.pop()]:
            N.add(u);assert u in owner
            if owner[u] not in T:T.add(owner[u]);todo.append(owner[u])
    assert len(T)-len(N)==len(graph)-len(match)
    return {'size':len(match),'matching':[{'demand':d,'unit':u} for d,u in sorted(match.items())],
      'cut':{'demands':sorted(T),'neighborhood':sorted(N),'deficiency':len(T)-len(N)}}
def main():
    pins=[F/'TOP_INTERVAL_AND_MARKED_DEMOTION.md',F/'independent_core_sector_neutral.json']
    ann=json.loads(pins[-1].read_text());results=[]
    for name,path in [('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'),('CCR',F/'cluster_collateral_closed_source.json')]:
        assert ann['input_sha256'][str(path)]==sha(path);pins.append(path)
        src=json.loads(path.read_text());rows=src['period_rows'];by={r['t']:i for i,r in enumerate(rows)}
        ctrl=next(a for a in ann['controls'] if a['source']==name);M=set(ctrl['M']);assert len(ctrl['S'])==2*len(M)-1
        candidate={};local={};h0={};info={};first=collections.defaultdict(list);last=collections.defaultdict(list);seen=collections.defaultdict(list)
        ends=[i for i,r in enumerate(rows) if r['genuine_F']]
        def segment(a,b):
            a=(a+1)%len(rows)
            return rows[a:b+1] if a<=b else rows[a:]+rows[:b+1]
        for k,e in enumerate(ends):
            r=rows[e];x=r['key'];t=r['t'];node=r['BF_before'];pathkeys=[]
            while True:
                pathkeys.append(node[0])
                if node[0]==x:break
                node=node[1] if x<node[0] else node[2]
            q=r['qF'];assert len(pathkeys)==2*q+1
            seg=segment(ends[k-1],e)
            own=[(w['t'],j,b) for w in seg for j in range(1,w['a']+1) for b in (0,1)]
            dd=[(t,j) for j in range(1,q+1)];h0.update(zip(dd,own))
            for j,d in enumerate(dd,1):
                G,P=pathkeys[-2*j-1:-2*j+1];assert G in M and P not in M and (x<P<G or G<P<x)
                gs=next(ends[(k-z)%len(ends)] for z in range(1,len(ends)) if rows[ends[(k-z)%len(ends)]]['key']==G)
                assert rows[gs]['A_after'][0]==G
                loss=[]
                for v in segment(gs,e):
                    for ev in v['A_events']:
                        for a in ev['rotations']:
                            if a['pivot']!=G:continue
                            before=marked(subtree(a['before'],G),M);after=marked(subtree(a['after'],G),M)
                            if x in before-after:loss.append((v['t'],ev['j'],a['bit']))
                assert loss
                candidate[d]={(v,j,b) for v,j,_ in loss for b in (0,1)};local[d]=set(own)
                info[d]={'demand':d,'x':x,'G':G,'P':P,'prior_genuine_G_t':rows[gs]['t'],'loss_rotations':loss}
                first[loss[0]].append(d);last[loss[-1]].append(d)
                seen[(G,rows[gs]['t'],x>G)].append(d)
        for (G,s,right),ds in seen.items():
            ordered=sorted(ds,key=lambda d:(by[d[0]]-by[s])%len(rows));xs=[info[d]['x'] for d in ordered]
            assert len(set(xs))==len(xs) and xs==sorted(xs,reverse=right)
        for select in (first,last):
            for u,ds in select.items():
                assert len({(info[d]['G'],info[d]['prior_genuine_G_t'],info[d]['x']>info[d]['G']) for d in ds})==1
        def load(select):
            c=collections.Counter()
            for u,ds in select.items():c[u[:2]]+=len(ds)
            return max(c.values(),default=0)
        fixed=src.get('h0',src.get('funding',{}).get('h0'));assert h0=={tuple(z['demand']):tuple(z['unit']) for z in fixed}
        gp={tuple(z['demand']):tuple(z['actual_bit']) for z in ctrl['g_plus']}
        variants={'all_loss_bits':candidate,
          'all_loss_and_local_bits':{d:candidate[d]|local[d] for d in candidate},
          'all_loss_local_and_ND_bits':{d:candidate[d]|local[d]|({gp[d]} if d in gp else set()) for d in candidate}}
        comparisons={k:maximum(g) for k,g in variants.items()}
        results.append({'source':name,'Q':len(candidate),'fixed_h0_preserved':len(h0),
          'first_loss_peak_event_load':load(first),'last_loss_peak_event_load':load(last),
          'source_demands':[info[d] for d in sorted(info)],'comparisons':comparisons,
          'old_owners_changed':False,'new_Bank25_or_fE_license_claimed':False})
    r={'status':'EXACT_MD35_CONTROL_RELATIONS','source_engine_calls':0,'source_queries':0,'controls':results,
      'JR35':'OPEN','input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'marked_demotion_relation.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({'status':r['status'],'controls':[{'source':z['source'],'Q':z['Q'],'first_peak':z['first_loss_peak_event_load'],
      'last_peak':z['last_loss_peak_event_load'],'comparisons':{k:{'size':v['size'],'cut':v['cut']} for k,v in z['comparisons'].items()}} for z in results]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
