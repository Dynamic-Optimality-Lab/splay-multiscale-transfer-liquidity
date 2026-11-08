"""Complete protected-spine corpus and range-relevant signed supergraph."""
import sys,json,time,itertools
from pathlib import Path
from collections import defaultdict,Counter
from array import array
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_GAP01')
from core_refinement_v2 import S,V,PORT,collapse,shadow,rho,visible
BASE=Path('DO_RESEARCH_REBOOT/M3_GAP01')
def compositions(total,n):
    if n==0:
        if total==0:yield ()
        return
    for first in range(total+1):
        for tail in compositions(total-first,n-1):yield (first,)+tail
def spine_length(t):
    d=0
    while t[1]!=0:t=t[2];d+=1
    return d
def decorate(t,counts):
    levels=iter(counts);number=iter(range(-sum(counts),0))
    def go(n):
        if n[1]==0:return S.node(0,PORT,collapse(n[3]))
        c=next(levels);keys=[next(number) for _ in range(c)];left=go(n[2])
        for k in reversed(keys):left=S.node(k,PORT,left)
        return S.node(n[1],left,collapse(n[3]))
    return go(t)
def models(bt,kmax,exact=False):
    for bi,t in enumerate(bt):
        d=spine_length(t)
        for k in ((kmax,) if exact else range(kmax+1)):
            for vec in compositions(k,d):yield bi,vec,decorate(t,vec)
def options(t):
    for x,h in visible(t):
        if x>=0:yield 1,x,collapse(S.trace(t,x)[0]),[['K',x]],[h]
    for f,h in visible(t):
        if f>=0:continue
        pre=S.trace(t,f)[0]
        for x,hh in visible(pre):
            if x<0 or x in (0,t[1]):continue # all such B kernels have w>=2
            yield 2,x,collapse(S.trace(pre,x)[0]),[['K',f],['K',x]],[h,hh]
def main():
    assert not (BASE/'catalog.json').exists();start=time.process_time()
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']];psi=[r['psi'] for r in bc['nodes']]
    kern=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text());h2={(r['entry_core'],r['target']):r for r in kern['rows'] if r['gap0_childless_at_exit']}
    max0=max(r['q'] for (bi,x),r in h2.items() if x==0);maxroot=max(r['q'] for (bi,x),r in h2.items() if x==bt[bi][1]);assert max0<=2 and maxroot<=2
    shadows=[];sid={};families=[];opts=[];seen=[];queries=0
    def identify(a):
        if a not in sid:sid[a]=len(shadows);shadows.append(a);opts.append([]);seen.append(set())
        return sid[a]
    for bi,vec,t in models(bt,3):
        mid=len(families);families.append({'core':bi,'counts':vec});sa=shadow(t);assert rho(sa)==sa;ai=identify(sa)
        for H,x,dst,word,depths in options(t):
            queries+=1;aa=shadow(dst);assert rho(aa)==aa;aj=identify(aa);key=(H,x,aj)
            if key not in seen[ai]:
                seen[ai].add(key);opts[ai].append({'H':H,'target':x,'destination_shadow':aj,'model':mid,'word':word,'A_depths':depths})
        assert queries<1000000 and time.process_time()-start<120,'UNKNOWN seed cap'
    seed_queries=queries;four_count=0;missing=[]
    for bi,vec,t in models(bt,4,True):
        four_count+=1;sa=shadow(t);ai=sid.get(sa)
        for H,x,dst,word,depths in options(t):
            queries+=1;aa=shadow(dst);aj=sid.get(aa)
            if ai is None or aj is None or (H,x,aj) not in seen[ai]:
                missing.append({'core':bi,'counts':vec,'H':H,'target':x,'word':word,'source_alpha':sa,'destination_alpha':aa})
                break
        if missing:break
        assert queries<1000000 and time.process_time()-start<120,'UNKNOWN fourth corpus cap'
    profile={'status':'PROFILE_COVERAGE_REFUTED_EXACT' if missing else 'FINITE_EXACT_VERIFIED',
      'seed_models':len(families),'fourth_node_models':four_count,'seed_queries':seed_queries,'total_queries':queries,
      'shadow_classes':len(shadows),'max_q_terminal0':max0,'max_q_terminal_entry_root':maxroot,'missing':missing,
      'cpu_seconds':round(time.process_time()-start,3)}
    with (BASE/'profiles.json').open('x',encoding='utf-8') as f:json.dump(profile,f,indent=2)
    print(json.dumps(profile),flush=True)
    if missing:return
    byroot={r:[i for i,s in enumerate(shadows) if s[0]==(0,1,r)] for r in range(9)};local={ai:j for r in range(9) for j,ai in enumerate(byroot[r])}
    ob=array('H');aa=array('H');bases=[]
    for bi,b in enumerate(bt):
        bases.append(len(ob))
        for ai in byroot[b[1]]:ob.append(bi);aa.append(ai)
    assert len(ob)<=2000000 and len(shadows)<65536,'UNKNOWN state cap'
    census=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text())
    arrays={'offsets':array('I',[0]),'targets':array('I'),'weights':array('b'),'meta':array('I')};cnt=Counter();safe=Counter()
    for u,(bi,ai) in enumerate(zip(ob,aa)):
        for j,o in enumerate(opts[ai]):
            H=o['H'];x=o['target']
            if H==1:
                h=census['B_depth'][bi][x]
                if h==0:continue
                bj=census['B_destination'][bi][x];q=h//2
            else:
                r=h2.get((bi,x))
                if r is None:continue
                bj=r['exit_core'];q=r['q']
            w=2*H-q
            if w>=2:safe[(H,w)]+=1;continue
            if len(arrays['targets'])==5000000:raise RuntimeError('UNKNOWN: edge cap before appending')
            v=bases[bj]+local[o['destination_shadow']]
            arrays['targets'].append(v);arrays['weights'].append(w);arrays['meta'].append(j);cnt[(H,w)]+=1
        arrays['offsets'].append(len(arrays['targets']))
        if u%8192==0:assert time.process_time()-start<120,'UNKNOWN graph CPU cap'
    arrays.update(ordinary_a=aa,ordinary_b=ob)
    for name,a in arrays.items():
        with (BASE/(name+'.bin')).open('xb') as f:a.tofile(f)
    c={'status':'BUILT_UNAUDITED','byteorder':sys.byteorder,'nodes':len(ob),'edges':len(arrays['targets']),
      'shadows':shadows,'shadows_by_root':byroot,'low_options':opts,'models':families,'B_bases':bases,'psi':psi,
      'counts':[{'H':H,'w':w,'count':n} for (H,w),n in sorted(cnt.items())],
      'range_safe':[{'H':H,'w':w,'count':n} for (H,w),n in sorted(safe.items())],
      'source_queries':queries,'cpu_seconds':round(time.process_time()-start,3)}
    with (BASE/'catalog.json').open('x',encoding='utf-8') as f:json.dump(c,f,indent=2)
    print(json.dumps({k:v for k,v in c.items() if k not in ('models','shadows','shadows_by_root','low_options','B_bases','psi')},indent=2),flush=True)
def load():
    c=json.loads((BASE/'catalog.json').read_text());a={}
    for n,typ in {'ordinary_a':'H','ordinary_b':'H','offsets':'I','targets':'I','weights':'b','meta':'I'}.items():
        z=array(typ);z.frombytes((BASE/(n+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder and z.itemsize>1:z.byteswap()
        a[n]=z
    return c,a
def edge_info(c,a,u,e):
    ai=a['ordinary_a'][u]
    return {'source':u,'destination':a['targets'][e],'source_B':a['ordinary_b'][u],
      'destination_B':a['ordinary_b'][a['targets'][e]],'source_shadow':ai,'csr_edge':e,
      'w':a['weights'][e],**c['low_options'][ai][a['meta'][e]]}
if __name__=='__main__':main()
