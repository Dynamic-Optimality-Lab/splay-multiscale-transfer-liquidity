"""Complete two-sort fixed-sector core fragment, with exact physical A-shadow witnesses."""
import sys,json,time,hashlib
from pathlib import Path
from collections import defaultdict,Counter
from array import array
sys.path[:0]=['python/independent','DO_RESEARCH_REBOOT/M3_LDR01','DO_RESEARCH_REBOOT/M3_PHI01']
import splay as S
from search_helpers import sig
from verify_full_mixed import from_serial
M=(0,2,4,6,8);BASE=Path('DO_RESEARCH_REBOOT/M3_CHR01')
CATALOG=Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json')
class Budget(Exception):pass

def build():
    start=time.process_time();c=json.loads(CATALOG.read_text());ts=[from_serial(n['tree']) for n in c['nodes']]
    ids={t:i for i,t in enumerate(ts)};groups=defaultdict(list);shadows=[];sid={}
    for i,t in enumerate(ts):
        a=sig(t)
        if a not in sid:sid[a]=len(shadows);shadows.append(a)
        groups[sid[a]].append(i)
    byroot={r:[i for i,a in enumerate(shadows) if a[0]==r] for r in range(9)}
    local={a:j for r in range(9) for j,a in enumerate(byroot[r])}
    options=[]
    for a in range(len(shadows)):
        opts={}
        for tid in groups[a]:
            t=ts[tid]
            for x in M:
                h=S.lookup(t,x)[1]
                if h not in (1,2):continue
                dest=sid[sig(S.trace(t,x)[0])];key=(x,dest)
                if key not in opts:opts[key]={'target':x,'destination_shadow':dest,'A_witness_tree':tid,'A_depth':h}
        options.append(list(opts.values()))
    bdest=[];bdepth=[]
    for b in ts:
        bdest.append([ids[S.trace(b,x)[0]] for x in range(9)])
        bdepth.append([S.lookup(b,x)[1] for x in range(9)])
    ob=array('H');oa=array('H');base=[-1]*len(ts);mb=[]
    for bi,b in enumerate(ts):
        if b[1] not in M:continue
        base[bi]=len(ob);mb.append(bi)
        for ai in byroot[b[1]]:ob.append(bi);oa.append(ai)
    no=len(ob);N=no+len(mb)
    if N>2000000:raise Budget('state cap')
    mids={b:no+i for i,b in enumerate(mb)}
    offsets=array('I',[0]);dest=array('I');weight=array('b');meta=array('H');counts=Counter()
    def add(v,w,k,kind):
        if len(dest)>=5000000:raise Budget('edge cap')
        dest.append(v);weight.append(w);meta.append(k);counts[(kind,w)]+=1
    for u in range(N):
        if u%4096==0:
            if time.process_time()-start>=120:raise Budget('construction CPU cap')
        if u<no:
            bi=ob[u];ai=oa[u]
            for j,opt in enumerate(options[ai]):
                x=opt['target'];h=bdepth[bi][x]
                if not h:continue
                bj=bdest[bi][x];aj=opt['destination_shadow'];v=base[bj]+local[aj]
                add(v,2-h//2,j,'LOW')
            for x in M:
                h=bdepth[bi][x]
                if not h:continue
                add(mids[bdest[bi][x]],6-h//2,10000+x,'OM')
        else:
            bi=mb[u-no]
            for aj in byroot[ts[bi][1]]:add(base[bi]+local[aj],0,20000,'MO')
        offsets.append(len(dest))
    catalog={'format':'CHR01-CSR-v1','byteorder':sys.byteorder,'tree_catalog':str(CATALOG).replace('\\','/'),
             'tree_catalog_sha256':hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
             'mask':list(M),'mu':sum(1<<i for i in M),'sigma':[0]*10,'chi8':True,
             'core_trees':len(ts),'physical_A_shadows':len(shadows),'ordinary_nodes':no,
             'midpoint_nodes':len(mb),'nodes':N,'edges':len(dest),'shadows':shadows,
             'A_groups':[groups[i] for i in range(len(shadows))],'shadows_by_root':byroot,
             'low_options':options,'B_bases':base,'M_B_indices':mb,'B_destination':bdest,
             'B_depth':bdepth,'psi':[n['psi'] for n in c['nodes']],
             'edge_counts':[{'kind':k,'weight':w,'count':n} for (k,w),n in sorted(counts.items())],
             'construction_cpu_seconds':round(time.process_time()-start,3)}
    return catalog,{'offsets':offsets,'targets':dest,'weights':weight,'meta':meta,'ordinary_b':ob,'ordinary_a':oa}

def save(catalog,arrays):
    for name,a in arrays.items():
        path=BASE/(name+'.bin')
        with path.open('xb') as f:a.tofile(f)
    with (BASE/'graph_catalog.json').open('x',encoding='utf-8') as f:json.dump(catalog,f,indent=2)

def load():
    c=json.loads((BASE/'graph_catalog.json').read_text());a={}
    for name,typ in {'offsets':'I','targets':'I','weights':'b','meta':'H','ordinary_b':'H','ordinary_a':'H'}.items():
        x=array(typ);x.frombytes((BASE/(name+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder and x.itemsize>1:x.byteswap()
        a[name]=x
    return c,a

def edge_info(c,a,u,e):
    v=a['targets'][e];kind=a['meta'][e];no=c['ordinary_nodes']
    row={'source':u,'destination':v,'weight':a['weights'][e],'csr_edge':e}
    if kind==20000:row.update(kind='MO')
    elif kind>=10000:row.update(kind='OM',target=kind-10000)
    else:
        ai=a['ordinary_a'][u];row.update(kind='LOW',option=kind,**c['low_options'][ai][kind])
    return row

if __name__=='__main__':
    assert not (BASE/'graph_catalog.json').exists()
    c,a=build();save(c,a)
    print(json.dumps({k:c[k] for k in ('ordinary_nodes','midpoint_nodes','nodes','edges','edge_counts','construction_cpu_seconds')}),flush=True)
