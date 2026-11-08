"""Bounded exact-weight helper search with shared shadows and private A witnesses."""
import sys,json,time
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
sys.path[:0]=['python/independent','DO_RESEARCH_REBOOT/M3_PHI01']
import splay as S
from verify_full_mixed import from_serial,serial
OUT=Path('DO_RESEARCH_REBOOT/M3_LDR01/helper_search.json');M=(0,2,4,6,8)
class Limit(Exception):pass
@lru_cache(None)
def sig(t):
    def key(n):return None if n==S.LEAF else n[1]
    return (key(t),key(t[2]),key(t[3]),key(t[2][2]) if t[2]!=S.LEAF else None,
            key(t[2][3]) if t[2]!=S.LEAF else None,key(t[3][2]) if t[3]!=S.LEAF else None,
            key(t[3][3]) if t[3]!=S.LEAF else None)
@lru_cache(None)
def step(t,x):return S.lookup(t,x)[1],S.trace(t,x)[0]
def child_tree(r,x):
    if x<r:return S.node(r,S.node(x,S.balanced(range(x)),S.balanced(range(x+1,r))),S.balanced(range(r+1,9)))
    return S.node(r,S.balanced(range(r)),S.node(x,S.balanced(range(r+1,x)),S.balanced(range(x+1,9))))
def main():
    assert not OUT.exists();start=time.process_time();c=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    trees=[from_serial(n['tree']) for n in c['nodes']];groups=defaultdict(list)
    for t in trees:groups[sig(t)].append(t)
    transitions={}
    for a,variants in groups.items():
        options={}
        for t in variants:
            for x in M:
                da,an=step(t,x)
                if not 1<=da<=4:continue
                H=(da+1)//2;key=(x,H,sig(an))
                if key not in options:options[key]=(t,da)
        transitions[a]=[(x,H,an,t,da) for (x,H,an),(t,da) in options.items()]
    prior=json.loads(Path('DO_RESEARCH_REBOOT/M3_PHI01/mixed_search.json').read_text())['most_negative_low_edge']
    seeds=[{'A':from_serial(prior['A']),'B':from_serial(prior['B']),'target':prior['leg']['target'],'label':'prior_minus2'}]
    selected={}
    for e in sorted(c['edges'],key=lambda e:(-e['depth'],e['source'],e['target'])):
        b=trees[e['source']];r=b[1];x=e['target']
        if r not in M or x not in M:continue
        key=(r,x)
        if key not in selected:selected[key]=(b,x)
    for (r,x),(b,_) in list(selected.items())[:7]:
        seeds.append({'A':child_tree(r,x),'B':b,'target':x,'label':f'root{r}_target{x}'})
    assert len(seeds)==8
    extensions=state_occurrences=return_tests=closed=hard_closed=completed=0
    minima={};best={};hard_prefix=None;progress=[];reason=None
    def record(seed,legs,B,total,DL,PL):
        return {'seed':seed['label'],'A0':serial(seed['A']),'B0':serial(seed['B']),
                'low_legs':legs,'B_before_high':serial(B),'low_weight':total,'D_L':DL,'P_L':PL,
                'mask':list(M),'chi8':True,'private_A_witnesses_share_only_abstract_shadows':True}
    try:
        for seed in seeds:
            a0=seed['A'];b0=seed['B'];r=b0[1];x0=seed['target']
            layer={(b0,sig(a0)):(0,0,0,[])}
            for depth in range(1,7):
                nxt={}
                for (b,a),(u,DL,PL,legs) in layer.items():
                    for x,H,an,t,da in transitions[a]:
                        if depth==1 and (x!=x0 or H!=1):continue
                        if extensions>=1000000:raise Limit('extension cap')
                        if time.process_time()-start>=120:raise Limit('CPU cap')
                        extensions+=1;db,bn=step(b,x)
                        if db==0:continue
                        w=2*H-db//2;v=u+w;dn=DL+max(0,-w);pn=PL+max(0,w)
                        leg={'A_source':serial(t),'target':x,'dA':da,'dB':db,'H':H,'q':db//2,'w':w}
                        path=legs+[leg];key=(bn,an)
                        old=nxt.get(key)
                        if old is None or (v,-dn)<(old[0],-old[1]):nxt[key]=(v,dn,pn,path)
                layer=nxt;state_occurrences+=len(layer)
                if state_occurrences>2000000:raise Limit('state cap')
                for (b,a),(u,DL,PL,legs) in layer.items():
                    if DL>2 and (hard_prefix is None or (len(legs),u)<(len(hard_prefix['low_legs']),hard_prefix['low_weight'])):
                        hard_prefix=record(seed,legs,b,u,DL,PL)
                    return_tests+=1;dh,back=step(b,r)
                    if dh==0 or back!=b0:continue
                    closed+=1;wh=6-dh//2;weight=u+wh
                    labels=['all']+(['D_L_gt_2'] if DL>2 else [])
                    hard_closed+=int(DL>2)
                    for label in labels:
                        if label not in minima or weight<minima[label]:
                            minima[label]=weight;rec=record(seed,legs,b,u,DL,PL)
                            rec.update(high_target=r,high_d=dh,high_q=dh//2,high_w=wh,total_weight=weight)
                            best[label]=rec
                row={'seed':seed['label'],'depth':depth,'layer_states':len(layer),
                     'extensions':extensions,'closed_candidates':closed,'hard_closed':hard_closed,
                     'minima':dict(minima),'cpu_seconds':round(time.process_time()-start,3)}
                progress.append(row);print(json.dumps(row),flush=True)
                if not layer:break
            completed+=1
    except Limit as e:reason=str(e)
    result={'status':'COMPLETE' if reason is None else 'UNKNOWN_CAP','cap_reason':reason,
            'A_core_trees':len(trees),'A_shadow_classes':len(groups),
            'A_shadow_transition_options':sum(len(v) for v in transitions.values()),
            'seeds_registered':len(seeds),'seeds_completed':completed,'max_low_edges':6,
            'extensions':extensions,'state_occurrences':state_occurrences,'return_tests':return_tests,
            'closed_candidates':closed,'hard_closed_candidates':hard_closed,'minima':minima,
            'best_candidates':best,'shortest_hard_prefix':hard_prefix,
            'progress':progress,'cpu_seconds':round(time.process_time()-start,3),
            'scope':'bounded zero-gap fixed-mask, six fused low steps then one canonical high return; A witnesses reset only within identical complete alpha7; no global absence claim'}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('best_candidates','shortest_hard_prefix','progress')}),flush=True)
if __name__=='__main__':main()
