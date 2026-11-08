"""Static binding audit of the OLD rejection; no original root replay."""
import ast,json,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def main():
    start=time.process_time();old=BASE.parent/'M3_UNIFORM02/original_lift.py';tree=ast.parse(old.read_text());tags=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='build_slow':tags.append(ast.literal_eval(n.args[1]))
    assert tags==['UNIFL']
    factory=ast.parse((BASE.parent/'M3_GAPINT01/interior_original.py').read_text());low=next(n for n in factory.body if isinstance(n,ast.FunctionDef) and n.name=='low');strings={n.value for n in ast.walk(low) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
    assert {'MXLw','MXLv','MXLbt','MXL_H','MXL_w'}<=strings
    oldrec=read(BASE.parent/'M3_UNIFORM02/case_000/original_attempt.json');e=oldrec['environment']
    assert e['UNIFLw_nev']==0 and e['UNIFL_H']==0 and not e['UNIFLw_p0'] and oldrec['root'] is False
    assert not any(k.startswith('MXLw') for k in e)
    result={'status':'EXACT_OLD_ADAPTER_BINDING_MISMATCH_CONFIRMED','old_compiler_tag':'UNIFL','fixture_private_field_prefix':'MXL','old_actual_nev':0,'old_actual_H':0,'old_actual_root_slot_present':False,'old_recorded_root':False,'old_root_replayed':False,'reason_false_is_decisive':'The original LOW predicate requires slot0 present and nev>0. The old stored environment has neither because the intended MXL fields were not the compiled UNIFL fields.','old_completion_rejection_is_not_a_realizability_result':True,'old_formula_matrix_audits_affected':False,'old_signature_source_controls_affected':False,'new_correct_adapter_tag':'MXL','CPU_seconds':time.process_time()-start}
    with (BASE/'binding_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:
        with (BASE/'binding_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'CPU_cap':120,'error':error},f,indent=2)
