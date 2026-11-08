"""Complete signature-independent marked-root B-core proof supergraph."""
import sys,json,time,itertools
from pathlib import Path
from array import array
from collections import Counter
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
BASE=Path('DO_RESEARCH_REBOOT/M3_CHIB01')
def main():
    out=BASE/'catalog.json';assert not out.exists();start=time.process_time();bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']];bid={t:i for i,t in enumerate(bt)}
    templates=[];byB=[[] for _ in bt];queries=0
    def add(bi,bj,x,q,H,kind,y=None):
        w=2*H-q
        if w>=2:return
        req=(1<<bt[bi][1])|(1<<x);forbid=0 if y is None else 1<<y
        if req&forbid:return
        j=len(templates);byB[bi].append(j);templates.append({'source_B':bi,'destination_B':bj,'target':x,'q':q,'H':H,'w':w,
          'kind':kind,'intermediate':y,'required_mask':req,'forbidden_mask':forbid})
    for bi,b in enumerate(bt):
        for x in range(9):
            queries+=1;h=S.lookup(b,x)[1]
            if h:add(bi,bid[S.trace(b,x)[0]],x,h//2,1,'H1')
        for y in range(9):
            if y==b[1]:continue
            pre=S.trace(b,y)[0]
            for x in range(9):
                queries+=1;h=S.lookup(pre,x)[1];add(bi,bid[S.trace(pre,x)[0]],x,h//2,2,'H2_CORE',y)
        assert queries<1000000 and time.process_time()-start<120
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    for r in kernel['rows']:
        if r['gap0_childless_at_exit']:add(r['entry_core'],r['exit_core'],r['target'],r['q'],2,'H2_GAP0')
    masks=[sum(1<<k for k in ks) for ks in itertools.combinations(range(9),5)];muarr=array('H');barr=array('H');nodes=[]
    for mu in masks:
        ids=[-1]*len(bt)
        for bi,b in enumerate(bt):
            if mu>>b[1]&1:ids[bi]=len(muarr);muarr.append(mu);barr.append(bi)
        nodes.append(ids)
    assert len(muarr)==340340 and len(muarr)<2000000
    off=array('I',[0]);dst=array('I');weights=array('b');meta=array('I');cnt=Counter();dominated=0
    for mi,mu in enumerate(masks):
        ids=nodes[mi]
        for bi,u in enumerate(ids):
            if u<0:continue
            best={}
            for j in byB[bi]:
                t=templates[j]
                if mu&t['required_mask']!=t['required_mask'] or mu&t['forbidden_mask']:continue
                v=ids[t['destination_B']];assert v>=0
                if v not in best or t['w']<best[v][0]:
                    if v in best:dominated+=1
                    best[v]=(t['w'],j)
                else:dominated+=1
            assert u==len(off)-1
            for v,(w,j) in best.items():
                if len(dst)==5000000:raise RuntimeError('UNKNOWN edge cap before append')
                dst.append(v);weights.append(w);meta.append(j);cnt[(templates[j]['kind'],w)]+=1
            off.append(len(dst))
        assert time.process_time()-start<120
    for n,a in {'ordinary_mu':muarr,'ordinary_b':barr,'offsets':off,'targets':dst,'weights':weights,'meta':meta}.items():
        with (BASE/(n+'.bin')).open('xb') as f:a.tofile(f)
    c={'status':'BUILT_UNAUDITED','byteorder':sys.byteorder,'masks':masks,'nodes':len(muarr),'edges':len(dst),'templates':templates,
      'source_case_queries':queries,'dominated_rows':dominated,'counts':[{'kind':k,'w':w,'count':n} for (k,w),n in sorted(cnt.items())],
      'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(c,f,indent=2)
    print(json.dumps({k:v for k,v in c.items() if k not in ('masks','templates')},indent=2),flush=True)
def load():
    c=json.loads((BASE/'catalog.json').read_text());a={}
    for n,typ in {'ordinary_mu':'H','ordinary_b':'H','offsets':'I','targets':'I','weights':'b','meta':'I'}.items():
        x=array(typ);x.frombytes((BASE/(n+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder:x.byteswap()
        a[n]=x
    return c,a
def edge_info(c,a,u,e):return {'source':u,'destination':a['targets'][e],'mu':a['ordinary_mu'][u],'csr_edge':e,'template':a['meta'][e],**c['templates'][a['meta'][e]]}
if __name__=='__main__':main()
