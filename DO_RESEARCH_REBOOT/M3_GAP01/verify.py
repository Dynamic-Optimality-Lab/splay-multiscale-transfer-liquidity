"""Independent regeneration of A profiles/B splays and every signed row."""
import json,time,hashlib
from array import array
from pathlib import Path
from collections import Counter
from build import BASE,load,models,decorate,options,S,V
from core_refinement_v2 import shadow,rho
def main():
    out=BASE/'edge_audit.json';assert not out.exists();start=time.process_time();c,a=load();p=array('i');p.frombytes((BASE/'potential.bin').read_bytes())
    import sys
    if c['byteorder']!=sys.byteorder:p.byteswap()
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']];bid={t:i for i,t in enumerate(bt)}
    sid={tuple(tuple(r) for r in s):i for i,s in enumerate(c['shadows'])};expected=[set() for _ in sid];queries=0;mc=0
    for bi,vec,t in models(bt,3):
        ai=sid[shadow(t)];assert rho(shadow(t))==shadow(t);mc+=1
        for H,x,tt,word,depths in options(t):queries+=1;expected[ai].add((H,x,sid[shadow(tt)]))
    for ai,os in enumerate(c['low_options']):assert expected[ai]=={(o['H'],o['target'],o['destination_shadow']) for o in os}
    four=0
    for bi,vec,t in models(bt,4,True):
        ai=sid[shadow(t)];four+=1
        for H,x,tt,word,depths in options(t):queries+=1;assert (H,x,sid[shadow(tt)]) in expected[ai]
    # Verify every option's explicit stored representative and word.
    for ai,os in enumerate(c['low_options']):
        for o in os:
            m=c['models'][o['model']];t=decorate(bt[m['core']],m['counts']);assert shadow(t)==tuple(tuple(r) for r in c['shadows'][ai])
            t2=t;depths=[]
            from core_refinement_v2 import collapse
            for mode,x in o['word']:depths.append(S.lookup(t2,x)[1]);t2=S.trace(t2,x)[0]
            assert depths==o['A_depths'] and all(h in (1,2) for h in depths)
            assert shadow(collapse(t2))==tuple(tuple(r) for r in c['shadows'][o['destination_shadow']])
    depth=[];dest=[];kernel={}
    def find(t,k):
        while t[1]!=k:t=t[2] if k<t[1] else t[3]
        return t
    def strip(t):
        if t==S.LEAF:return t
        if t[1]==-1:assert t[2:]==(S.LEAF,S.LEAF);return S.LEAF
        return S.node(t[1],strip(t[2]),strip(t[3]))
    for bi,b in enumerate(bt):
        depth.append([S.lookup(b,x)[1] for x in range(9)]);dest.append([bid[S.trace(b,x)[0]] for x in range(9)])
        pre=S.trace(V.insert(b,-1),-1)[0]
        for x in range(9):
            queries+=2;dd=S.lookup(pre,x)[1];outtree=S.trace(pre,x)[0]
            if find(outtree,-1)[2:]==(S.LEAF,S.LEAF):kernel[(bi,x)]=(bid[strip(outtree)],dd//2)
    assert len(kernel)==16842
    assert max(q for (bi,x),(bj,q) in kernel.items() if x==0)==2
    assert max(q for (bi,x),(bj,q) in kernel.items() if x==bt[bi][1])==1
    local={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])};counts=Counter();safe=Counter();hist=Counter();samples={};checked=0
    for u,(bi,ai) in enumerate(zip(a['ordinary_b'],a['ordinary_a'])):
        assert -2<=p[u]<=-c['psi'][bi]<=0;ee=a['offsets'][u]
        for j,o in enumerate(c['low_options'][ai]):
            H=o['H'];x=o['target']
            if H==1:
                if depth[bi][x]==0:continue
                bj,q=dest[bi][x],depth[bi][x]//2
            else:
                if (bi,x) not in kernel:continue
                bj,q=kernel[(bi,x)]
            w=2*H-q
            if w>=2:safe[(H,w)]+=1;continue
            v=c['B_bases'][bj]+local[o['destination_shadow']]
            assert ee<a['offsets'][u+1] and a['targets'][ee]==v and a['weights'][ee]==w and a['meta'][ee]==j
            r=w+p[u]-p[v];assert r>=0,(u,ee,r);counts[(H,w)]+=1;hist[r]+=1;checked+=1
            row={'node':u,'edge':ee,'source_B':bi,'q':q,'w':w,'source_shadow':ai,**o}
            samples.setdefault('H'+str(H)+'w'+str(w),row)
            m=c['models'][o['model']]
            if H==2 and w in (0,1) and sum(m['counts'])==3:samples.setdefault('three_anonymous_H2_w'+str(w),row)
            if c['shadows'][ai][1][0:2]==[0,0] and c['shadows'][ai][4][0:2]==[0,0]:samples.setdefault('double_anonymous_source_H'+str(H)+'w'+str(w),row)
            ee+=1
        assert ee==a['offsets'][u+1]
        if u%8192==0:assert time.process_time()-start<120,'UNKNOWN independent audit cap'
    assert checked==c['edges'];assert [{'H':H,'w':w,'count':n} for (H,w),n in sorted(counts.items())]==c['counts']
    assert [{'H':H,'w':w,'count':n} for (H,w),n in sorted(safe.items())]==c['range_safe']
    result={'status':'FINITE_EXACT_VERIFIED','states':c['nodes'],'edges_independently_regenerated':checked,
      'seed_models':mc,'four_node_models':four,'source_case_queries':queries,'range':[min(p),max(p)],'residual_histogram':dict(hist),
      'minimum_residual':min(hist),'range_safe_rows':sum(safe.values()),'potential_sha256':hashlib.sha256((BASE/'potential.bin').read_bytes()).hexdigest(),
      'cpu_seconds':round(time.process_time()-start,3),'samples':samples}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2),flush=True)
if __name__=='__main__':main()
