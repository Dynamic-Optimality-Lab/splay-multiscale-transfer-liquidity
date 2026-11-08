"""Derived count partition and natural-compatible hybrid normalization.
Count cases are necessary symbolic parameters, never a finite BST proof.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C28_reduction',OLD/'audit_construct.py')
def peak(a):
    ee=[]
    for d,u in a.items():ee.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    live=set();ans=0
    for t,d in sorted(ee):
        if d in live:live.remove(d)
        else:live.add(d);ans=max(ans,len(live))
    return ans
def main():
    c=json.loads((B/'catchment_forcing_countercertificate.json').read_text());hy=json.loads((B/'hybrid_partition_receipt.json').read_text());rows=[dict(r,before=tuple(r['before']),after=tuple(r['after'])) for r in c['rows']]
    raw={};normalization=[];ownall={}
    for block in hy['blocks']:
        lo,hi=block['interval'];rr=[r for r in rows if lo<=r['occurrence']<=hi];mm=C.L.macros(rr);own={d:u for m in mm for d,u in zip(m['demands'],m['units'])};D={d for m in mm for d in m['demands']};U={u for m in mm for u in m['units']}
        h=mp(block['source_comparison']);ans=dict(own);inverse={u:d for d,u in own.items()}
        for root in sorted(D-set(own)):
            d=root;seen=set()
            while True:
                assert d not in seen;seen.add(d);u=h[d]
                if u not in inverse:break
                d=inverse[u]
            ans[root]=u
        assert set(ans)==D and len(set(ans.values()))==len(D) and all(ans[d]==u for d,u in own.items())
        raw.update(ans);ownall.update(own);normalization.append({'kind':block['kind'],'interval':[lo,hi],
            'H_normalized':pack(ans),'own_h0':pack(own),'cut_peak':peak(ans)})
    assert peak(raw)<=13 and all(raw[d]==u for d,u in ownall.items())
    neg=[]
    for Q in range(1,7):
        for beta in range(Q+1):
            for z in (0,1):
                if Q+1+beta+(1-z)>7:continue
                if 2-beta-z<0:neg.append({'H':1,'Q':Q,'beta':beta,'z':z,'residual':2-beta-z})
    assert [(z['Q'],z['beta'],z['z'],z['residual']) for z in neg]==[(2,2,1,-1),(3,2,1,-1),(3,3,1,-2),(4,2,1,-1)]
    out('branch_reduction_and_normalization.json',{'status':'DERIVED_SOURCE_COUNT_CLASSIFICATION_AND_NATURAL_OWNER_NORMALIZATION',
        'source_lemma':'r>=Q+1+beta+(1-z) by disjoint off-path marked witnesses',
        'negative_H1_classes':neg,'H_ge2_argument':'beta+z<=4, so2min(H,3)-beta-z>=0; H>=3 gives>=2',
        'leaf_potential':'D_leaf=L-1 in[0,5]','identity':'2min(H,3)-Q+Delta D_leaf=2min(H,3)-beta-z',
        'new_J_proved':False,'candidate_J_range':[0,14],'candidate_total_working_bound':25,
        'normalized_hybrid_comparison':pack(raw),'all_natural_values_kept':True,'normalized_cut_peak':peak(raw),
        'block_normalizations':normalization,'universal_source_coverage':False})
    print(json.dumps({'status':'COUNT_REDUCTION_AND_NATIVE_NORMALIZATION_PASS','negative_classes':neg,'raw_natural_compatible_peak':peak(raw)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_reduction_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
