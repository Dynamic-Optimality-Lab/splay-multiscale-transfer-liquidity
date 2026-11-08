"""One bounded global source-pool falsification batch, accepted rows only."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import retirement_pools as R
CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    results=[]
    for case in R.cases():
        assert time.process_time()-START<CAP-2
        model=R.build(case['rows']);record={k:case[k] for k in ('name','path','receipt','input_sha256','receipt_sha256')};record.update(scope=model['scope'],r=model['r'],core=model['core'])
        if model['scope']!='MAXIMAL_CORE':results.append(record);continue
        record.update(macros=model['macros'],source_rows=case['rows'],D=len(model['D']),U=len(model['U']),raw_pool=R.cover(model))
        if case['current_owner'] is not None:
            a=case['current_owner'];record['current_owner_count']=len(a);record['current_unpaid']=sorted(model['D']-set(a));record['current_pool_owner_test']=R.cover(model,a)
        if 'archive_prior' in case:
            a=case['archive_prior'];record['archived32_control']=R.cover(model,a);record['archived32_control']['scope']='archived construction receipt only; current all36 owners are retained'
            record['accepted_four_endpoint_test']=R.cover(model,a,set(case['accepted_additions'].values()))
            record.update(owners_path=case['owners_path'],owners_sha256=case['owners_sha256'])
        results.append(record)
        print(json.dumps({'source':case['name'],'D':len(model['D']),'U':len(model['U']),'raw_pool_complete':record['raw_pool']['complete'],'current_unpaid':len(record.get('current_unpaid',[]))}),flush=True)
    out('pooled_source_results.json',{'status':'PRODUCER_GROUPED_POOL_GLOBAL_COUNTING_TESTS','cases':results,'fresh_source_queries':0,'source_engine_calls':0,'universal_expansion_proved':False,'JIO34':'OPEN','schema_sha256':R.pin(F/'retirement_pools.py')})
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof168_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
