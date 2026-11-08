"""Regenerate all physical options and B projections, then audit every relevant edge."""
import sys,json,time,hashlib
from pathlib import Path
from array import array
from collections import Counter
from build_v2 import BASE,load,S,V
def main():
    out=BASE/'edge_audit.json';assert not out.exists();start=time.process_time();c,a=load();p=array('i');p.frombytes((BASE/'potential.bin').read_bytes())
    if c['byteorder']!=sys.byteorder:p.byteswap()
    pc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/graph_catalog.json').read_text());ats=[V.from_serial(t) for t in pc['A_trees']]
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']];bid={t:i for i,t in enumerate(bt)}
    sid={tuple(tuple(r) for r in x):i for i,x in enumerate(c['shadows'])};queries=0
    for ai,group in enumerate(pc['A_groups']):
        if not c['shadows'][ai][0][1]:assert not c['low_options'][ai];continue
        expected=set()
        for tid in group:
            t=ats[tid]
            for x in range(9):
                queries+=1;h=S.lookup(t,x)[1]
                if h in (1,2):expected.add((1,x,sid[tuple(tuple(r) for r in V.shadow(S.trace(t,x)[0]))]))
            queries+=1;h=S.lookup(t,-1)[1]
            if h in (1,2):
                t0=S.trace(t,-1)[0]
                for x in range(9):
                    queries+=1;hh=S.lookup(t0,x)[1]
                    if hh in (1,2):expected.add((2,x,sid[tuple(tuple(r) for r in V.shadow(S.trace(t0,x)[0]))]))
        got={(o['H'],o['target'],o['destination_shadow']) for o in c['low_options'][ai]};assert got==expected
        for o in c['low_options'][ai]:
            t=ats[o['A_tree']];assert sid[tuple(tuple(r) for r in V.shadow(t))]==ai
            depths=[]
            for mode,x in o['word']:depths.append(S.lookup(t,x)[1]);t=S.trace(t,x)[0]
            assert depths==o['A_depths'] and all(h in (1,2) for h in depths)
            assert sid[tuple(tuple(r) for r in V.shadow(t))]==o['destination_shadow']
        assert time.process_time()-start<120
    depth=[];dest=[];h2={};retained=0
    def strip(t):
        if t==S.LEAF:return t
        if t[1]==-1:assert t[2:]==(S.LEAF,S.LEAF);return S.LEAF
        return S.node(t[1],strip(t[2]),strip(t[3]))
    def find(t,x):
        while t[1]!=x:t=t[2] if x<t[1] else t[3]
        return t
    for bi,b in enumerate(bt):
        ds=[];vs=[];b0=S.trace(V.insert(b,-1),-1)[0]
        for x in range(9):
            queries+=2;ds.append(S.lookup(b,x)[1]);vs.append(bid[S.trace(b,x)[0]])
            q=S.lookup(b0,x)[1]//2;bb=S.trace(b0,x)[0];g=find(bb,-1)
            if g[2:]==(S.LEAF,S.LEAF):h2[(bi,x)]=(bid[strip(bb)],q);retained+=1
        depth.append(ds);dest.append(vs)
    assert retained==16842
    local={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])};cnt=Counter();hist=Counter();samples={};checked=0;safe=Counter();minimum=99
    assert len(p)==c['nodes'] and len(a['targets'])==c['edges'] and a['offsets'][-1]==c['edges']
    for u,(bi,ai) in enumerate(zip(a['ordinary_b'],a['ordinary_a'])):
        assert c['shadows'][ai][0]==[0,1,bt[bi][1]] and -2<=p[u]<=-c['psi'][bi]<=0
        ee=a['offsets'][u]
        for j,o in enumerate(c['low_options'][ai]):
            x=o['target'];H=o['H']
            if H==1:
                h=depth[bi][x]
                if h==0:continue
                bj,q=dest[bi][x],h//2
            else:
                if (bi,x) not in h2:continue
                bj,q=h2[(bi,x)]
            w=2*H-q
            if w>=2:safe[(H,w)]+=1;continue
            v=c['B_bases'][bj]+local[o['destination_shadow']]
            assert ee<a['offsets'][u+1] and a['meta'][ee]==j and a['targets'][ee]==v and a['weights'][ee]==w
            residual=w+p[u]-p[v];assert residual>=0,(u,ee,residual)
            minimum=min(minimum,residual);hist[residual]+=1;cnt[(H,w)]+=1;checked+=1
            if (H,w) not in samples:samples[(H,w)]={'node':u,'edge':ee,'source_B':bi,'source_shadow':ai,'q':q,'w':w,**o}
            ee+=1
        assert ee==a['offsets'][u+1]
        if u%8192==0:assert time.process_time()-start<120,'UNKNOWN independent edge cap'
    assert checked==c['edges'];assert [{'H':H,'w':w,'count':n} for (H,w),n in sorted(cnt.items())]==c['relevant_counts']
    assert [{'H':H,'w':w,'count':n} for (H,w),n in sorted(safe.items())]==c['range_safe_omitted_counts']
    result={'status':'FINITE_EXACT_VERIFIED','nodes':len(p),'edges_independently_regenerated':checked,
      'source_case_queries':queries,'range':[min(p),max(p)],'destination_debt_floor':True,'minimum_residual':minimum,
      'residual_histogram':dict(hist),'H2_retained_kernel_cases':retained,'all_range_safe_edges_covered':sum(safe.values()),
      'potential_sha256':hashlib.sha256((BASE/'potential.bin').read_bytes()).hexdigest(),
      'samples':list(samples.values()),'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2),flush=True)
if __name__=='__main__':main()
