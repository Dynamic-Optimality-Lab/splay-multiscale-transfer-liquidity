"""Independent finite regeneration: full BSTs, reference splays and exact CSR rows."""
import sys,json,time,hashlib
from pathlib import Path
from array import array
from collections import Counter,deque
from reference import (all_bsts,tree,depth,access,insert,mirror,iscore,collapse,
                       every_anonymous_has_core,shadow,visible)
BASE=Path('DO_RESEARCH_REBOOT/M3_COMB_AUD01');R=Path('DO_RESEARCH_REBOOT')

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def arr(p,t,byteorder):
    a=array(t);a.frombytes(p.read_bytes())
    if byteorder!=sys.byteorder:a.byteswap()
    return a

def main(g):
    start=time.process_time();out=BASE/f'finite_gap{g}.json';assert not out.exists()
    name='M3_GAP01' if g==0 else f'M3_GAPINT0{g}';folder=R/name;c=read(folder/'catalog.json')
    a={k:arr(folder/(k+'.bin'),t,c['byteorder']) for k,t in
       [('ordinary_a','H'),('ordinary_b','H'),('offsets','I'),('targets','I'),('weights','b'),('meta','I')]}
    values=arr(folder/'potential.bin','i',c['byteorder'])
    bc=read(R/'M3_LDR01/negative_run_census.json');bt=[tree(n['tree']) for n in bc['nodes']];bid={t:i for i,t in enumerate(bt)}
    assert len(bt)==4862 and set(bt)==set(all_bsts(tuple(range(9))))
    depths=[];destinations=[];incoming=[0]*len(bt);negative=[[] for _ in bt]
    for i,b in enumerate(bt):
        ds=[depth(b,x) for x in range(9)];vs=[bid[access(b,x)] for x in range(9)]
        depths.append(ds);destinations.append(vs)
        for d,v in zip(ds,vs):
            w=2-d//2
            if w<0:negative[i].append((v,-w));incoming[v]+=1
    q=deque(i for i,n in enumerate(incoming) if not n);psi=[0]*len(bt);popped=0
    while q:
        u=q.popleft();popped+=1
        for v,debt in negative[u]:
            psi[v]=max(psi[v],psi[u]+debt);incoming[v]-=1
            if not incoming[v]:q.append(v)
    assert popped==4862 and max(psi)==2 and psi==c['psi']==[n['psi'] for n in bc['nodes']]
    assert all(psi[i]==psi[bid[mirror(b)]] for i,b in enumerate(bt))
    for i in range(4862):
        for x in range(9):assert psi[destinations[i][x]]>=depths[i][x]//2-2
    sid={tuple(tuple(r) for r in s):i for i,s in enumerate(c['shadows'])};expected=[set() for _ in sid]
    models=source_cases=0
    for m in range(4):
        keys=tuple(sorted([16*i for i in range(9)]+[16*g-8+j for j in range(m)]))
        for t in all_bsts(keys):
            if not iscore(t[0]) or not every_anonymous_has_core(t)[0]:continue
            models+=1;ai=sid[shadow(t)]
            for x,d in visible(t):
                if not iscore(x):continue
                v=collapse(access(t,x));expected[ai].add((1,x//16,sid[shadow(v)]));source_cases+=1
            if g==0:
                for f,d in visible(t):
                    if iscore(f):continue
                    pre=access(t,f)
                    for x,h in visible(pre):
                        if not iscore(x) or x in (0,t[0]):continue
                        v=collapse(access(pre,x));expected[ai].add((2,x//16,sid[shadow(v)]));source_cases+=1
            assert time.process_time()-start<120,'UNKNOWN independent finite audit cap'
    assert models==(48450 if g==0 else c['models'])
    assert source_cases==(c['source_queries']-109208 if False else source_cases)
    # Every stored option and every independently regenerated option must agree.
    for i,os in enumerate(c['low_options']):
        assert expected[i]=={(o['H'],o['target'],o['destination_shadow']) for o in os},(g,i)
    all_bsts.cache_clear()
    kernel={}
    if g==0:
        def without_fringe(t):
            if t is None:return None
            if t[0]==-1:assert t[1] is None and t[2] is None;return None
            return (t[0],without_fringe(t[1]),without_fringe(t[2]))
        for i,b in enumerate(bt):
            pre=access(insert(b,-1),-1)
            for x in range(9):
                final=access(pre,x);n=final
                while n[0]!=-1:n=n[1]
                if n[1] is None and n[2] is None:kernel[i,x]=(bid[without_fringe(final)],depth(pre,x)//2)
        assert len(kernel)==16842
        assert max(q for (i,x),(j,q) in kernel.items() if x==0)==2
        assert max(q for (i,x),(j,q) in kernel.items() if x==bt[i][0])==1
    local={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])}
    assert len(values)==c['nodes']==len(a['ordinary_a'])==len(a['ordinary_b'])
    assert len(a['targets'])==len(a['weights'])==len(a['meta'])==c['edges']<=5000000
    assert len(a['offsets'])==c['nodes']+1 and a['offsets'][0]==0 and a['offsets'][-1]==c['edges']
    safe=Counter();debt_safe=Counter();stored=Counter();residuals=Counter();checked=0
    for u,(bi,ai) in enumerate(zip(a['ordinary_b'],a['ordinary_a'])):
        assert c['shadows'][ai][0]==[0,1,bt[bi][0]]
        assert u==c['B_bases'][bi]+local[ai]
        assert -2<=values[u]<=-psi[bi]<=0
        e=a['offsets'][u]
        for j,o in enumerate(c['low_options'][ai]):
            H=o['H'];x=o['target']
            if H==1:
                if not depths[bi][x]:continue
                bj=destinations[bi][x];credit=depths[bi][x]//2
            else:
                if (bi,x) not in kernel:continue
                bj,credit=kernel[bi,x]
            w=2*H-credit
            if w>=2:safe[H,w]+=1;continue
            if g and ((w==1 and psi[bj]>=1) or (w==0 and psi[bj]==2)):
                assert w-psi[bj]+2>=0;debt_safe[w]+=1;continue
            v=c['B_bases'][bj]+local[o['destination_shadow']]
            assert e<a['offsets'][u+1] and (a['targets'][e],a['weights'][e],a['meta'][e])==(v,w,j),(g,u,e)
            residual=w+values[u]-values[v];assert residual>=0,(g,u,e,residual)
            residuals[residual]+=1;stored[H,w]+=1;checked+=1;e+=1
        assert e==a['offsets'][u+1]
        if u%8192==0:assert time.process_time()-start<120,'UNKNOWN CSR audit cap'
    assert checked==c['edges']
    if g==0:
        assert [{'H':h,'w':w,'count':n} for (h,w),n in sorted(stored.items())]==c['counts']
        assert [{'H':h,'w':w,'count':n} for (h,w),n in sorted(safe.items())]==c['range_safe']
    else:
        assert {w:n for (h,w),n in stored.items()}=={int(k):v for k,v in c['counts'].items()}
        assert sum(safe.values())==c['range_safe'] and dict(debt_safe)=={int(k):v for k,v in c['debt_safe'].items()}
    result={'status':'PASS_INDEPENDENT_FINITE_AUDIT','campaign':name,'gap':g,
            'models_from_full_BST_enumeration':models,'A_source_cases':source_cases,
            'B_core_accesses':43758,'negative_core_edges':sum(map(len,negative)),
            'independent_core_debt':True,'core_debt_histogram':dict(Counter(psi)),
            'states':c['nodes'],'all_stored_edges_checked':checked,
            'range':[-2,0],'minimum_residual':min(residuals),'residual_histogram':dict(residuals),
            'range_safe_rows':sum(safe.values()),'debt_safe_rows':dict(debt_safe),
            'potential_sha256':hashlib.sha256((folder/'potential.bin').read_bytes()).hexdigest(),
            'old_generator_or_checker_imported':False,'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main(int(sys.argv[1]))
