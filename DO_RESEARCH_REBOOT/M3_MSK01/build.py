"""Complete all-core-target physical supergraph, one fixed gap0 key."""
import sys,json,time
from pathlib import Path
from collections import Counter
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_AER01','DO_RESEARCH_REBOOT/M3_H1F01']
from empty_interval_potential import S,V,OneGapPotential
BASE=Path('DO_RESEARCH_REBOOT/M3_MSK01')
def main():
    out=BASE/'catalog.json';assert not out.exists();start=time.process_time();old=OneGapPotential();pc=old.c
    ats=[V.from_serial(t) for t in pc['A_trees']];shadows=pc['shadows'];sid={tuple(tuple(x) for x in s):i for i,s in enumerate(shadows)}
    opts=[[] for _ in shadows];queries=0
    for ai,group in enumerate(pc['A_groups']):
        if not shadows[ai][0][1]:continue
        choices={}
        for tid in group:
            t=ats[tid]
            for x in range(9):
                queries+=1;h=S.lookup(t,x)[1]
                if h in (1,2):
                    dest=sid[tuple(tuple(r) for r in V.shadow(S.trace(t,x)[0]))];key=(1,x,dest)
                    choices.setdefault(key,{'H':1,'target':x,'destination_shadow':dest,'A_tree':tid,'A_depths':[h],'word':[['K',x]]})
            h0=S.lookup(t,-1)[1]
            if h0 in (1,2):
                pre=S.trace(t,-1)[0]
                for x in range(9):
                    queries+=1;h=S.lookup(pre,x)[1]
                    if h in (1,2):
                        dest=sid[tuple(tuple(r) for r in V.shadow(S.trace(pre,x)[0]))];key=(2,x,dest)
                        choices.setdefault(key,{'H':2,'target':x,'destination_shadow':dest,'A_tree':tid,'A_depths':[h0,h],'word':[['K',-1],['K',x]]})
        opts[ai]=list(choices.values());assert queries<1000000 and time.process_time()-start<120,'UNKNOWN option cap'
    bt=old.old.old.trees;byroot=pc['shadows_by_root'];local={ai:j for r in range(9) for j,ai in enumerate(byroot[str(r)])}
    ob=array('H');aa=array('H');bases=[]
    for bi,b in enumerate(bt):
        bases.append(len(ob))
        for ai in byroot[str(b[1])]:ob.append(bi);aa.append(ai)
    assert len(ob)<=2000000
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text())
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    h2={(r['entry_core'],r['target']):r for r in kernel['rows'] if r['gap0_childless_at_exit']}
    offsets=array('I',[0]);targets=array('I');weights=array('b');meta=array('I');counts=Counter();omitted=Counter()
    for u,(bi,ai) in enumerate(zip(ob,aa)):
        for j,o in enumerate(opts[ai]):
            x=o['target'];H=o['H']
            if H==1:
                h=bc['B_depth'][bi][x]
                if h==0:continue
                bj=bc['B_destination'][bi][x];q=h//2
            else:
                row=h2.get((bi,x))
                if row is None:continue
                bj=row['exit_core'];q=row['q']
            w=2*H-q
            if w>=2:omitted[(H,w)]+=1;continue
            v=bases[bj]+local[o['destination_shadow']]
            assert ob[v]==bj and aa[v]==o['destination_shadow']
            targets.append(v);weights.append(w);meta.append(j);counts[(H,w)]+=1
            assert len(targets)<=5000000,'UNKNOWN relevant edge cap'
        offsets.append(len(targets))
        if u%8192==0:assert time.process_time()-start<120,'UNKNOWN graph cap'
    arrays={'ordinary_b':ob,'ordinary_a':aa,'offsets':offsets,'targets':targets,'weights':weights,'meta':meta}
    for name,a in arrays.items():
        with (BASE/(name+'.bin')).open('xb') as f:a.tofile(f)
    cat={'status':'BUILT_UNAUDITED','byteorder':sys.byteorder,'nodes':len(ob),'edges':len(targets),'B_bases':bases,
      'shadows':shadows,'shadows_by_root':byroot,'low_options':opts,'psi':pc['psi'],
      'A_queries':queries,'physical_A_trees':len(ats),'ordinary_A_trees':sum(len(pc['A_groups'][i]) for i,s in enumerate(shadows) if s[0][1]),
      'relevant_counts':[{'H':H,'w':w,'count':n} for (H,w),n in sorted(counts.items())],
      'range_safe_omitted_counts':[{'H':H,'w':w,'count':n} for (H,w),n in sorted(omitted.items())],
      'initial_label':'-psi(coreB)','cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(cat,f,indent=2)
    print(json.dumps({k:v for k,v in cat.items() if k not in ('B_bases','shadows','shadows_by_root','low_options','psi')},indent=2),flush=True)
def load():
    c=json.loads((BASE/'catalog.json').read_text());a={}
    for name,typ in {'ordinary_b':'H','ordinary_a':'H','offsets':'I','targets':'I','weights':'b','meta':'I'}.items():
        z=array(typ);z.frombytes((BASE/(name+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder and z.itemsize>1:z.byteswap()
        a[name]=z
    return c,a
def edge_info(c,a,u,e):
    ai=a['ordinary_a'][u]
    return {'source':u,'destination':a['targets'][e],'source_B':a['ordinary_b'][u],
      'destination_B':a['ordinary_b'][a['targets'][e]],'source_shadow':ai,'csr_edge':e,
      'w':a['weights'][e],**c['low_options'][ai][a['meta'][e]]}
if __name__=='__main__':main()
