"""Regenerate physical A options and all CSR inequalities independently of label correction."""
import json,sys,time,hashlib
from array import array
from collections import defaultdict,Counter
from build_fragment import BASE,M,load,trees,alpha,edge_info,S,V
from compensated_potential import CompensatedPotential
OUT=BASE/'edge_audit.json'
def main():
    assert not OUT.exists();start=time.process_time();c,a=load();P=CompensatedPotential()
    assert c['nodes']==len(a['ordinary_b'])==len(a['ordinary_a']) and c['edges']==len(a['targets'])
    labels=array('i');labels.frombytes((BASE/'potential.bin').read_bytes())
    if c['byteorder']!=sys.byteorder:labels.byteswap()
    assert len(labels)==c['nodes']
    ats=[V.from_serial(t) for t in c['A_trees']]
    assert len(ats)==16796 and set(ats)==set(trees(-1,9))
    shadows=[tuple(tuple(r) for r in s) for s in c['shadows']];sid={s:i for i,s in enumerate(shadows)}
    assert len(sid)==1188
    groups=defaultdict(list)
    for i,t in enumerate(ats):groups[sid[alpha(t)]].append(i)
    assert [groups[i] for i in range(len(shadows))]==c['A_groups']
    byroot={r:[i for i,s in enumerate(shadows) if s[0][1] and s[0][2]==r] for r in range(9)}
    local={ai:j for r in range(9) for j,ai in enumerate(byroot[r])}
    regenerated=[];option_checks=0
    for ai in range(len(shadows)):
        expected=set()
        for i in groups[ai]:
            t=ats[i]
            for x in M:
                h=S.lookup(t,x)[1]
                if h in (1,2):expected.add((1,x,sid[alpha(S.trace(t,x)[0])]))
            h0=S.lookup(t,-1)[1]
            if h0 in (1,2):
                pre=S.trace(t,-1)[0]
                for x in M:
                    h=S.lookup(pre,x)[1]
                    if h in (1,2):expected.add((2,x,sid[alpha(S.trace(pre,x)[0])]))
        actual={(o['H'],o['target'],o['destination_shadow']) for o in c['low_options'][ai]}
        assert expected==actual and len(actual)==len(c['low_options'][ai])
        for o in c['low_options'][ai]:
            t=ats[o['A_tree']];assert alpha(t)==shadows[ai]
            depths=[]
            for mode,x in o['word']:
                assert mode=='K';h=S.lookup(t,x)[1];assert h in (1,2);depths.append(h);t=S.trace(t,x)[0]
            assert depths==o['A_depths'] and len(depths)==o['H'] and alpha(t)==shadows[o['destination_shadow']]
            option_checks+=1
        regenerated.append(actual)
    bdest=[];bdepth=[];h2={}
    from fringe_kernel import gap_leaf,erase
    for bi,b in enumerate(P.old.trees):
        bdest.append([P.old.ids[S.trace(b,x)[0]] for x in range(9)])
        bdepth.append([S.lookup(b,x)[1] for x in range(9)])
        pre=S.trace(V.insert(b,-1),-1)[0]
        for x in M:
            dst=S.trace(pre,x)[0]
            if gap_leaf(dst):h2[(bi,x)]=(P.old.ids[erase(dst)],S.lookup(pre,x)[1]//2)
    hist=Counter();badold=Counter();samples={};edges=0;changed=0
    off=a['offsets'];dst=a['targets'];w=a['weights'];meta=a['meta'];ob=a['ordinary_b'];oa=a['ordinary_a']
    for u in range(c['nodes']):
        bi=ob[u];ai=oa[u];assert P.old.trees[bi][1] in M
        assert u==c['B_bases'][bi]+local[ai]
        init=-P.old.psi[bi]-int(bi in P.R)
        assert -2<=labels[u]<=init<=0 and labels[u]<=-P.old.psi[bi]
        changed+=labels[u]!=init
        expected=[]
        for j,o in enumerate(c['low_options'][ai]):
            x=o['target'];H=o['H']
            if H==1:
                h=bdepth[bi][x]
                if not h:continue
                bj=bdest[bi][x];q=h//2
            else:
                z=h2.get((bi,x))
                if z is None:continue
                bj,q=z
            v=c['B_bases'][bj]+local[o['destination_shadow']]
            expected.append((v,2*H-q,j))
        actual=[(dst[e],w[e],meta[e]) for e in range(off[u],off[u+1])]
        assert actual==expected
        for e in range(off[u],off[u+1]):
            v=dst[e];red=w[e]+labels[u]-labels[v];assert red>=0,(u,e,red)
            H=c['low_options'][ai][meta[e]]['H'];bj=ob[v]
            oldred=w[e]+init-(-P.old.psi[bj]-int(bj in P.R));hist[red]+=1;edges+=1
            if oldred<0:
                assert H==1 and w[e] in (0,1) and bi not in P.R
                badold[(w[e],oldred)]+=1
                key='H1_w'+str(w[e])+'_oldr'+str(oldred)
                if key not in samples:samples[key]=edge_info(c,a,u,e)
            if H==2 and w[e] in (0,1):
                key='H2_w'+str(w[e])
                if key not in samples:samples[key]=edge_info(c,a,u,e)
            if H==2 and bi==952 and c['low_options'][ai][meta[e]]['target']==2:
                samples.setdefault('FRC_exception_952',edge_info(c,a,u,e))
        if u%8192==0:assert time.process_time()-start<120,'UNKNOWN: independent audit cap'
    assert edges==1915587 and changed==7439
    result={'status':'FINITE_EXACT_VERIFIED','nodes':c['nodes'],'edges_regenerated_and_checked':edges,
            'physical_A_trees':16796,'physical_A_shadows':1188,'physical_options_checked':option_checks,
            'potential_range':[min(labels),max(labels)],'potential_below_corrected_and_negative_psi':True,
            'changed_states':changed,'cheap_old_failures_repaired':[{'w':z,'old_residual':r,'edges':n} for (z,r),n in sorted(badold.items())],
            'minimum_new_residual':min(hist),'residual_histogram':dict(hist),'sample_edges':samples,
            'source_case_queries_upper_bound':43758+16796*15+4862*14,
            'potential_sha256':hashlib.sha256((BASE/'potential.bin').read_bytes()).hexdigest(),
            'cpu_seconds':round(time.process_time()-start,3),'scope':'fixed mu341 sigma gap0=1, physical A10 completions; low physical H1 and two-KEEP H2; original high by range'}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('sample_edges','residual_histogram')},indent=2),flush=True)
if __name__=='__main__':main()
