"""Complete physical one-gap A10 low fragment; source-witness metadata for every edge."""
import sys,json,time,hashlib
from pathlib import Path
from functools import lru_cache
from collections import defaultdict,Counter
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_FRC01','DO_RESEARCH_REBOOT/M3_H2R01',
             'DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
from compensated_potential import CompensatedPotential
BASE=Path('DO_RESEARCH_REBOOT/M3_H1F01');M=(0,2,4,6,8)
@lru_cache(None)
def trees(a,b):
    if a==b:return (S.LEAF,)
    return tuple(S.node(k,l,r) for k in range(a,b) for l in trees(a,k) for r in trees(k+1,b))
def alpha(t):return tuple(tuple(r) for r in V.shadow(t))
def main():
    assert not (BASE/'graph_catalog.json').exists();start=time.process_time();P=CompensatedPotential()
    bt=P.old.trees;bid=P.old.ids;psi=P.old.psi;R=P.R;init=[-p-int(i in R) for i,p in enumerate(psi)]
    bdest=[];bdepth=[];bad=[];counts=Counter()
    for u,t in enumerate(bt):
        ds=[];hs=[]
        for x in range(9):
            h=S.lookup(t,x)[1];v=bid[S.trace(t,x)[0]];w=2-h//2;r=w-init[v]+init[u]
            ds.append(v);hs.append(h);counts[(w,r)]+=1
            if w in (0,1) and r<0:bad.append({'source':u,'target':x,'destination':v,'h':h,'w':w,'residual':r,'source_in_R':u in R})
            if w<0:assert r>=0
        bdest.append(ds);bdepth.append(hs)
    assert all(not r['source_in_R'] for r in bad)
    census={'status':'COMPLETE','positive_signature_scope':'sigma[0]>0 so corrected Q is B-only',
            'access_queries':4862*9,'bad_cheap_edges':len(bad),'counts':[{'w':w,'residual':r,'count':n} for (w,r),n in sorted(counts.items())],
            'failures':bad,'B_destination':bdest,'B_depth':bdepth,'initial_by_B':init,
            'cpu_seconds':round(time.process_time()-start,3)}
    with (BASE/'cheap_census.json').open('x',encoding='utf-8') as f:json.dump(census,f,indent=2)
    print(json.dumps({k:census[k] for k in ('access_queries','bad_cheap_edges','counts','cpu_seconds')}),flush=True)
    ats=trees(-1,9);assert len(ats)==16796
    shadows=[];sid={};groups=defaultdict(list)
    for i,t in enumerate(ats):
        a=alpha(t)
        if a not in sid:sid[a]=len(shadows);shadows.append(a)
        groups[sid[a]].append(i)
    byroot={r:[i for i,a in enumerate(shadows) if a[0][1] and a[0][2]==r] for r in range(9)}
    local={a:j for r in range(9) for j,a in enumerate(byroot[r])}
    options=[]
    for ai in range(len(shadows)):
        opts={}
        for i in groups[ai]:
            t=ats[i]
            for x in M:
                h=S.lookup(t,x)[1]
                if h in (1,2):
                    aj=sid[alpha(S.trace(t,x)[0])];key=(1,x,aj)
                    opts.setdefault(key,{'H':1,'target':x,'destination_shadow':aj,'A_tree':i,'A_depths':[h],'word':[['K',x]]})
            h0=S.lookup(t,-1)[1]
            if h0 in (1,2):
                pre=S.trace(t,-1)[0]
                for x in M:
                    h=S.lookup(pre,x)[1]
                    if h in (1,2):
                        aj=sid[alpha(S.trace(pre,x)[0])];key=(2,x,aj)
                        opts.setdefault(key,{'H':2,'target':x,'destination_shadow':aj,'A_tree':i,'A_depths':[h0,h],'word':[['K',-1],['K',x]]})
        options.append(list(opts.values()))
        assert time.process_time()-start<120,'UNKNOWN: A option CPU cap'
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    h2={ (r['entry_core'],r['target']):r for r in kernel['rows'] if r['gap0_childless_at_exit'] }
    ob=array('H');oa=array('H');bases=[-1]*4862
    for bi,t in enumerate(bt):
        if t[1] not in M:continue
        bases[bi]=len(ob)
        for ai in byroot[t[1]]:ob.append(bi);oa.append(ai)
    assert len(shadows)<65536 and len(ob)<=2000000,'UNKNOWN: state/representation cap'
    offsets=array('I',[0]);targets=array('I');weights=array('b');meta=array('I');edgecounts=Counter()
    for u,(bi,ai) in enumerate(zip(ob,oa)):
        for j,o in enumerate(options[ai]):
            x=o['target'];H=o['H']
            if H==1:
                h=bdepth[bi][x]
                if h==0:continue
                bj=bdest[bi][x];q=h//2
            else:
                row=h2.get((bi,x))
                if row is None:continue
                bj=row['exit_core'];q=row['q']
            aj=o['destination_shadow'];v=bases[bj]+local[aj];w=2*H-q
            assert bases[bj]>=0 and 0<=v<len(ob)
            targets.append(v);weights.append(w);meta.append(j);edgecounts[(H,w)]+=1
            assert len(targets)<=5000000,'UNKNOWN: edge cap'
        offsets.append(len(targets))
        if u%8192==0:
            assert time.process_time()-start<120,'UNKNOWN: construction CPU cap'
    arrays={'ordinary_b':ob,'ordinary_a':oa,'offsets':offsets,'targets':targets,'weights':weights,'meta':meta}
    for name,a in arrays.items():
        with (BASE/(name+'.bin')).open('xb') as f:a.tofile(f)
    cat={'format':'H1F01-CSR-v1','byteorder':sys.byteorder,'mu':341,'mask':M,'sigma':[1]+[0]*9,'chi8':True,
         'ordinary_nodes':len(ob),'nodes':len(ob),'edges':len(targets),'physical_A_trees':16796,
         'physical_A_shadows':len(shadows),'shadows':shadows,'A_groups':[groups[i] for i in range(len(shadows))],
         'A_trees':[V.serial(t) for t in ats],'shadows_by_root':byroot,'B_bases':bases,'low_options':options,
         'initial_by_B':init,'psi':psi,'edge_counts':[{'H':H,'w':w,'count':n} for (H,w),n in sorted(edgecounts.items())],
         'high':'not materialized; all original chi8 legs use range [-2,0], midpoint zero',
         'construction_cpu_seconds':round(time.process_time()-start,3)}
    with (BASE/'graph_catalog.json').open('x',encoding='utf-8') as f:json.dump(cat,f,indent=2)
    print(json.dumps({k:cat[k] for k in ('nodes','edges','physical_A_trees','physical_A_shadows','edge_counts','construction_cpu_seconds')}),flush=True)
def load():
    c=json.loads((BASE/'graph_catalog.json').read_text());a={}
    for name,typ in {'ordinary_b':'H','ordinary_a':'H','offsets':'I','targets':'I','weights':'b','meta':'I'}.items():
        x=array(typ);x.frombytes((BASE/(name+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder and x.itemsize>1:x.byteswap()
        a[name]=x
    return c,a
def edge_info(c,a,u,e):
    ai=a['ordinary_a'][u];o=c['low_options'][ai][a['meta'][e]]
    return {'source':u,'destination':a['targets'][e],'csr_edge':e,'weight':a['weights'][e],**o,
            'source_B':a['ordinary_b'][u],'destination_B':a['ordinary_b'][a['targets'][e]],
            'source_shadow':ai}
if __name__=='__main__':main()
