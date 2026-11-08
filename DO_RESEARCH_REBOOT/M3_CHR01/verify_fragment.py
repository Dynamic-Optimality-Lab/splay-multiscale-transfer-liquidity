"""Independent complete fragment generation and exact integer edge-certificate audit."""
import sys,json,time,hashlib,argparse,ast
from collections import defaultdict,Counter
from array import array
from functools import lru_cache
from pathlib import Path
sys.path[:0]=['python/independent','DO_RESEARCH_REBOOT/M3_PHI01']
import splay as S
import verify_full_mixed as V
from fragment_graph import load,BASE,CATALOG
OUT=BASE/'edge_audit.json'

def native(p):return Path(chr(92)*2+'?'+chr(92)+str(p.absolute())) if sys.platform=='win32' else p
def digest(p):return hashlib.sha256(native(p).read_bytes()).hexdigest()
@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (S.LEAF,)
    return tuple(S.node(r,l,t) for r in range(lo,hi) for l in trees(lo,r) for t in trees(r+1,hi))
def alpha(t):return tuple(None if k==2 else i for k,s,i in V.shadow(t))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--save',action='store_true');ap.add_argument('--hash-only',action='store_true');args=ap.parse_args()
    root=BASE.resolve().parents[1];hashes=0
    if (BASE/'manifest.json').exists():
        m=json.loads((BASE/'manifest.json').read_text())
        for section in ('files','frozen_dependencies','baseline_preservation'):
            for row in m[section]:assert digest(root/row['path'])==row['sha256'],row['path'];hashes+=1
    if args.hash_only:
        assert hashes;print(json.dumps({'status':'PASS','manifest_hashes_checked':hashes}));return
    if args.save:assert not OUT.exists()
    start=time.process_time();c,a=load();ts=trees(0,9);tid={t:i for i,t in enumerate(ts)}
    old=json.loads(CATALOG.read_text());assert [V.from_serial(n['tree']) for n in old['nodes']]==list(ts)
    assert digest(CATALOG)==c['tree_catalog_sha256']
    groups=defaultdict(list);sh=[];sid={}
    for i,t in enumerate(ts):
        key=alpha(t)
        if key not in sid:sid[key]=len(sh);sh.append(key)
        groups[sid[key]].append(i)
    assert [list(t) for t in sh]==c['shadows'] and len(sh)==634
    assert [groups[i] for i in range(634)]==c['A_groups']
    M=(0,2,4,6,8);byroot={r:[i for i,s in enumerate(sh) if s[0]==r] for r in range(9)}
    assert {str(r):v for r,v in byroot.items()}==c['shadows_by_root']
    options=[]
    for ai in range(634):
        opts={}
        for ti in groups[ai]:
            t=ts[ti]
            for x in M:
                h=S.lookup(t,x)[1]
                if h not in (1,2):continue
                aj=sid[alpha(S.trace(t,x)[0])]
                opts.setdefault((x,aj),{'target':x,'destination_shadow':aj,'A_witness_tree':ti,'A_depth':h})
        options.append(list(opts.values()))
    assert options==c['low_options']
    bd=[[S.lookup(t,x)[1] for x in range(9)] for t in ts]
    bn=[[tid[S.trace(t,x)[0]] for x in range(9)] for t in ts]
    assert bd==c['B_depth'] and bn==c['B_destination']
    ob=[];oa=[];bases=[-1]*4862;mb=[]
    for bi,t in enumerate(ts):
        if t[1] not in M:continue
        bases[bi]=len(ob);mb.append(bi)
        for ai in byroot[t[1]]:ob.append(bi);oa.append(ai)
    assert list(a['ordinary_b'])==ob and list(a['ordinary_a'])==oa
    assert bases==c['B_bases'] and mb==c['M_B_indices']
    no=len(ob);N=no+len(mb);assert no==251480 and N==255064 and len(mb)==3584
    mid={b:no+i for i,b in enumerate(mb)};local={ai:j for r in range(9) for j,ai in enumerate(byroot[r])}
    potential=array('i');potential.frombytes((BASE/'potential.bin').read_bytes())
    if c['byteorder']!=sys.byteorder:potential.byteswap()
    assert len(potential)==N and min(potential)==-2 and max(potential)==0
    offsets=a['offsets'];dst=a['targets'];ws=a['weights'];met=a['meta'];counts=Counter();resid=Counter();ext_min=100
    assert len(offsets)==N+1 and offsets[0]==0 and offsets[-1]==len(dst)==len(ws)==len(met)==2309760
    for u in range(N):
        expected=[]
        if u<no:
            bi=ob[u];ai=oa[u]
            for j,opt in enumerate(options[ai]):
                x=opt['target'];h=bd[bi][x]
                if h:expected.append((bases[bn[bi][x]]+local[opt['destination_shadow']],2-h//2,j,'LOW'))
            for x in M:
                h=bd[bi][x]
                if h:expected.append((mid[bn[bi][x]],6-h//2,10000+x,'OM'))
        else:
            bi=mb[u-no]
            expected=[(bases[bi]+local[aj],0,20000,'MO') for aj in byroot[ts[bi][1]]]
        assert offsets[u+1]-offsets[u]==len(expected)
        for e,(v,w,m,kind) in zip(range(offsets[u],offsets[u+1]),expected):
            assert (dst[e],ws[e],met[e])==(v,w,m),(u,e)
            residual=w+potential[u]-potential[v];assert residual>=0;resid[residual]+=1;counts[(kind,w)]+=1
            # Stronger range extension: all midpoint labels are replaced by zero.
            pu=potential[u] if u<no else 0;pv=potential[v] if v<no else 0
            ext=w+pu-pv;assert ext>=0;ext_min=min(ext_min,ext)
        assert time.process_time()-start<120,'UNKNOWN: independent graph audit cap'
    assert [{'kind':k,'weight':w,'count':n} for (k,w),n in sorted(counts.items())]==c['edge_counts']
    result=json.loads((BASE/'fragment_result.json').read_text());assert result['status']=='POTENTIAL_VERIFIED'
    assert {str(k):v for k,v in resid.items()}==result['residual_histogram']
    parsed=0
    for p in BASE.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'));parsed+=1
    summary={'status':'PASS','scope':'complete registered fragment; all vertices/options/edges regenerated independently',
             'nodes':N,'ordinary_nodes':no,'midpoint_nodes':len(mb),'edges':len(dst),
             'low_edges':sum(n for (k,w),n in counts.items() if k=='LOW'),
             'cheap_low_edges':sum(n for (k,w),n in counts.items() if k=='LOW' and w in (0,1)),
             'minimum_original_residual':min(resid),'potential_range':[-2,0],
             'minimum_extended_midpoint_residual':ext_min,'residual_histogram':dict(resid),
             'cpu_seconds':round(time.process_time()-start,3),'python_files_parsed':parsed,
             'manifest_hashes_checked':hashes}
    if args.save:
        with OUT.open('x',encoding='utf-8') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
