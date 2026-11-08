"""Test a new, explicitly sufficient source-peeling lemma on accepted graphs.
Zero fresh original splays. Never retries the unaccepted optional N85 word.
"""
import hashlib,itertools,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;C=P/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pop(x):return x.bit_count()
def main():
    z=json.loads((C/'pooled_source_results.json').read_text());entry=json.loads((F/'dependency_manifest.json').read_text());assert sha(C/'pooled_source_results.json')==entry['C34_artifacts']['pooled_source_results.json']
    results=[];witnesses={}
    for case in z['cases']:
        mm=case['macros'];allunits=sorted({tuple(u) for m in mm for u in m['N']});pos={u:i for i,u in enumerate(allunits)};masks=[sum(1<<pos[tuple(u)] for u in m['N']) for m in mm];marked=sorted({r['x'] for r in case['source_rows'] if r['gen']});tested=0
        found={}
        for k in (2,3):
            for inds in itertools.combinations(range(len(mm)),k):
                tested+=1
                if tested%1000==0:assert time.process_time()-START<CAP-2
                union=0
                for i in inds:union|=masks[i]
                private=[]
                for i in inds:
                    rest=0
                    for j in inds:
                        if j!=i:rest|=masks[j]
                    private.append(pop(masks[i]&~rest))
                if not all(v<mm[i]['Q'] for i,v in zip(inds,private)):continue
                deficit=sum(mm[i]['Q'] for i in inds)-pop(union);assert deficit<=0 # Accepted full covers imply every subcoalition passes GPR.
                restricted=any(marked[0]<mm[i]['target']<marked[-1] for i in inds) and any(mm[i]['Q']>2*mm[i]['H'] for i in inds)
                rec=dict(source=case['name'],source_path=case['path'],source_sha256=case['input_sha256'],accepted_primitive_receipt=case['receipt'],receipt_sha256=case['receipt_sha256'],indices=inds,macros=[mm[i] for i in inds],private_capacities=private,union_bits=pop(union),total_demand=sum(mm[i]['Q'] for i in inds),deficit=deficit,interior_and_excess=restricted,conclusion='counterexample to unconditional private-capacity peeling only; not SI34',fresh_source_queries=0)
                if 'general' not in found:found['general']=rec
                if restricted and 'localized' not in found:found['localized']=rec
                if 'general' in found and 'localized' in found:break
            if 'general' in found and 'localized' in found:break
        results.append(dict(source=case['name'],tested_coalitions=tested,found={key:rec['indices'] for key,rec in found.items()}));witnesses.update({case['name']+'_'+key:rec for key,rec in found.items()})
        print(json.dumps(results[-1]),flush=True)
    result=dict(status='BOUNDED_NEW_PEELING_RULE_FALSIFICATION',input_sha256={'C34/pooled_source_results.json':sha(C/'pooled_source_results.json')},results=results,witnesses=witnesses,source_queries=0,source_engine_calls=0,SI34='ACTIVE',positive_test_not_universal_proof=True)
    with (F/'peeling_rule_source_witnesses.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof170_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
