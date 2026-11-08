"""Regenerate pinned11 necessary source grammar without changing its code."""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
spec=importlib.util.spec_from_file_location('sealed11_geometry12',B.parent/'SE03_STEP2_CORE7_SINGLE_EXCESS_11/audit_geometry.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def main():
    m.B=B;m.out=out;m.main()
    a=json.loads((B/'geometry_certificate.json').read_text())
    old=json.loads((B.parent/'SE03_STEP2_CORE7_SINGLE_EXCESS_11/geometry_certificate.json').read_text())
    assert a==old
    out('geometry_reuse_receipt.json',{'status':'PASS_EXACT_SAME_SOURCE_GRAMMAR',
        'two_slot_extension':'cyclic predecessor map is injective on two critical indices; their Q<=1 predecessors are not critical',
        'no_abstract_path_realization_assumed':True,'source_engine_calls':m.calls})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_geometry_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':m.calls,'new_finite_tests':0})
