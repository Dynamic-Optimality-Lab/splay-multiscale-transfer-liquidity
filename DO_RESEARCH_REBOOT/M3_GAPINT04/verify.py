import sys
sys.path.append('DO_RESEARCH_REBOOT/M3_GAPINT01')
"""Independent complete single-gap grammar and row/debt/reflection audit."""
import json,time,hashlib
from pathlib import Path
from array import array
from collections import Counter
from build_v2 import BASE,load
from framework_v2 import grammar,iscore,visible,collapse,shadow,rho,decode,S,V,reflect_tree
def main():
    out=BASE/'edge_audit.json';assert not out.exists();start=time.process_time();c,a=load();g=c['gap'];p=array('i');p.frombytes((BASE/'potential.bin').read_bytes())
    import sys
    if c['byteorder']!=sys.byteorder:p.byteswap()
    sid={tuple(tuple(r) for r in s):i for i,s in enumerate(c['shadows'])};expected=[set() for _ in sid];models=queries=0;tr=grammar(g)
    for m in range(4):
        for t in tr(0,8,m):
            if not iscore(t[1]):continue
            models+=1;ai=sid[shadow(t)];assert rho(shadow(t),g)==shadow(t)
            for x,h in visible(t):queries+=1;aj=sid[shadow(collapse(S.trace(t,x)[0]))];expected[ai].add((x//16,aj))
        assert queries<1000000 and time.process_time()-start<120
    tr.cache_clear()
    for ai,os in enumerate(c['low_options']):
        assert expected[ai]=={(o['target'],o['destination_shadow']) for o in os}
        for o in os:
            t=decode(c['witnesses'][o['witness']]);x=16*o['target'];assert shadow(t)==tuple(tuple(r) for r in c['shadows'][ai])
            assert S.lookup(t,x)[1]==o['A_depth'] in (1,2)
            assert shadow(collapse(S.trace(t,x)[0]))==tuple(tuple(r) for r in c['shadows'][o['destination_shadow']])
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']];bid={t:i for i,t in enumerate(bt)}
    depth=[];dest=[]
    for b in bt:depth.append([S.lookup(b,x)[1] for x in range(9)]);dest.append([bid[S.trace(b,x)[0]] for x in range(9)]);queries+=9
    local={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])};cnt=Counter();safe=0;debt=Counter();hist=Counter();samples={};checked=0
    for u,(bi,ai) in enumerate(zip(a['ordinary_b'],a['ordinary_a'])):
        assert -2<=p[u]<=-c['psi'][bi]<=0;ee=a['offsets'][u]
        for j,o in enumerate(c['low_options'][ai]):
            x=o['target'];h=depth[bi][x]
            if h==0:continue
            bj=dest[bi][x];w=2-h//2
            if w>=2:safe+=1;continue
            if (w==1 and c['psi'][bj]>=1) or (w==0 and c['psi'][bj]==2):debt[w]+=1;continue
            v=c['B_bases'][bj]+local[o['destination_shadow']]
            assert ee<a['offsets'][u+1] and a['targets'][ee]==v and a['weights'][ee]==w and a['meta'][ee]==j
            residual=w+p[u]-p[v];assert residual>=0;cnt[w]+=1;hist[residual]+=1;checked+=1
            r={'node':u,'source_B':bi,'source_shadow':ai,'w':w,'q':h//2,**o};samples.setdefault('w'+str(w),r)
            s=c['shadows'][ai]
            if s[1][0:2]==[0,0] and s[3][0:2]==[0,0] and s[4][0:2]==[0,0]:samples.setdefault('three_fringe_fork_w'+str(w),r)
            ee+=1
        assert ee==a['offsets'][u+1]
        if u%8192==0:assert time.process_time()-start<120
    assert checked==c['edges'] and dict(cnt)=={int(k):v for k,v in c['counts'].items()} and safe==c['range_safe'] and dict(debt)=={int(k):v for k,v in c['debt_safe'].items()}
    mirrors=[bid[reflect_tree(t)] for t in bt];sym=sum(c['psi'][i]!=c['psi'][j] for i,j in enumerate(mirrors))
    result={'status':'FINITE_EXACT_VERIFIED','gap':g,'reflected_gap':9-g,'models':models,'source_case_queries':queries,
      'states':len(p),'edges_independently_regenerated':checked,'range':[min(p),max(p)],'destination_debt_floor':True,
      'minimum_residual':min(hist),'residual_histogram':dict(hist),'range_safe_rows':safe,'debt_safe_rows':dict(debt),
      'core_reflection_debt_mismatches':sym,'potential_sha256':hashlib.sha256((BASE/'potential.bin').read_bytes()).hexdigest(),
      'cpu_seconds':round(time.process_time()-start,3),'samples':samples}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2),flush=True)
if __name__=='__main__':main()
