"""Source-ID receipts on the actual inherited core7 one-slot family.
Adversarial paid-owner fixtures are explicitly NOT invented frozen fE.
Universal preservation quantifies every supplied certified owner map.
"""
import importlib.util,itertools,json,sys,time
from pathlib import Path
from single_slot_allocator import independent_full,extend_one
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('source01',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def reflected(t):
    if isinstance(t,str):return 'F'+str(7-int(t[1:]))
    return (8-t[0],reflected(t[2]),reflected(t[1]))
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def serial(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v
def main():
    old=json.loads((B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/deficient_source_schemas.json').read_text())
    fam=next(v for v in old['families'] if v['core']==7);base=freeze(fam['initial_A_BF']);receipts=[]
    for mirror in (False,True):
        R=reflected(base) if mirror else base;word=[(m,8-x if mirror else x) for m,x in fam['word']]
        rows,end=p.replay(R,word);assert end[0]==end[1]==R
        build=independent_full(rows);D,U,h=build['D'],build['U'],build['h'];dd=sorted(D)
        fixtures=[]
        for missing in (build['R'],dd[0]):
            ordered=[missing]+[d for d in dd if d!=missing]
            paid={ordered[i]:h[ordered[i-1]] for i in range(1,len(ordered))}
            ex=extend_one(D,U,paid,h)
            assert ex['missing']==missing and len(ex['path'])==len(D)
            fixtures.append({'kind':'adversarial actual-ID paid-map fixture, not a numerical sealed fE receipt',
                'paid':pack(paid),'path':ex['path'],'new_unit':ex['unit'],'missing':missing,'final':pack(ex['allocation'])})
        simple={d:u for d,u in h.items() if d!=build['R']};ex=extend_one(D,U,simple,h)
        fixtures.append({'kind':'direct free-terminal fixture','paid':pack(simple),'missing':build['R'],
            'path':ex['path'],'new_unit':ex['unit'],'final':pack(ex['allocation'])})
        empty=extend_one(D,U,h,h);assert empty['unit'] is None and empty['allocation']==h
        receipts.append({'reflected':mirror,'initial_A_BF':R,'word':word,'rows':rows,
            'macros':build['macros'],'critical_macro':build['critical_macro'],'preceding_macro':build['preceding_macro'],
            'R':build['R'],'positive_surplus':build['source_positive_surplus'],'seed_spare_macro':build['seed_spare_macro'],
            'seed_spare':build['seed_spare'],'independent_h':pack(h),'physical_units':U,'fixtures':fixtures,
            'paid_empty_residual':'map preserved exactly','frozen_actual_fE':'universal input parameter, not guessed from fixtures'})
    out('physical_receipts.json',{'status':'PASS_ACTUAL_SOURCE_IDS_AND_ONE_HOLE_RECEIPTS',
        'families':serial(receipts),'source_family_scope':'two reflected copies of the specified arbitrary-gap source identity',
        'universal_proof':'separate source geometry and all-paid free-terminal theorem, not extrapolation from these fixtures',
        'Step2':'OPEN','source_engine_calls':2*len(fam['word'])*3,'new_finite_tests':6})
    print(json.dumps({'status':'PASS','source_families':2,'paid_fixtures':6,'demands_each':len(D)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_construction_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'new_finite_tests':6})
