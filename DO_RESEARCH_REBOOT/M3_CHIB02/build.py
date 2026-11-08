import sys,json,time,itertools
from pathlib import Path
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
BASE=Path('DO_RESEARCH_REBOOT/M3_CHIB02')
def main():
    assert not (BASE/'catalog.json').exists();start=time.process_time();bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']];bid={t:i for i,t in enumerate(bt)}
    table=[];queries=0
    for b in bt:
        row=[]
        for x in range(9):row.append([bid[S.trace(b,x)[0]],S.lookup(b,x)[1]]);queries+=1
        table.append(row)
    masks=[sum(1<<k for k in z) for z in itertools.combinations(range(9),5)];N=len(masks)*4862;off=array('I',[0]);dst=array('I');w=array('b');meta=array('B')
    for mi,mu in enumerate(masks):
        for bi,b in enumerate(bt):
            for x,(bj,h) in enumerate(table[bi]):
                if h==0:continue
                dst.append(mi*4862+bj);w.append(2-h//2 if mu>>x&1 else 2);meta.append(x)
            off.append(len(dst))
        assert len(dst)<=5000000 and time.process_time()-start<120
    for name,a in {'offsets':off,'targets':dst,'weights':w,'meta':meta}.items():
        with (BASE/(name+'.bin')).open('xb') as f:a.tofile(f)
    c={'status':'BUILT_UNAUDITED','byteorder':sys.byteorder,'nodes':N,'edges':len(dst),'masks':masks,'core_access_table':table,'source_case_queries':queries,'cpu_seconds':round(time.process_time()-start,3)}
    with (BASE/'catalog.json').open('x',encoding='utf-8') as f:json.dump(c,f,indent=2)
    print(json.dumps({k:v for k,v in c.items() if k not in ('masks','core_access_table')},indent=2))
def load():
    c=json.loads((BASE/'catalog.json').read_text());a={}
    for name,typ in {'offsets':'I','targets':'I','weights':'b','meta':'B'}.items():
        z=array(typ);z.frombytes((BASE/(name+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder and z.itemsize>1:z.byteswap()
        a[name]=z
    return c,a
def edge_info(c,a,u,e):
    mu=c['masks'][u//4862];x=a['meta'][e];h=c['core_access_table'][u%4862][x][1]
    return {'source':u,'destination':a['targets'][e],'mu':mu,'source_B':u%4862,'destination_B':a['targets'][e]%4862,'target':x,
      'marked':bool(mu>>x&1),'h':h,'q':h//2 if mu>>x&1 else 0,'w':a['weights'][e],'edge':e}
if __name__=='__main__':main()
