"""Final integrity after exact-original-common-set eligibility audit."""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base_integrity11',B/'audit_seal.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    e=json.loads((B/'eligibility_exchange_audit.json').read_text())
    r=json.loads((B/'run_eligibility_result.json').read_text())
    assert r['status']=='PASS' and e['cases']==5256
    assert e['all_old_successful_paths_identical'] and e['licensed_full_exchange_equals_one_pair_extension']
    assert e['branches']=={'p_equals_r':1512,'empty':3024,'blocked_other_at_common_r':720}
    assert 'original licensed COMPLETE h/l exchange' in (B/'FULL_PROOF.md').read_text()
    def finalout(n,v):
        if n=='seal_audit.json':v.update({'original_common_exchange_eligibility':'PASS_ALL_OLD_SUCCESSFUL_PATHS_STABLE',
            'eligibility_map_regression_cases':5256,'final_seal_version':2})
        out(n.replace('.json','2.json'),v)
    m.out=finalout;m.main()
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
