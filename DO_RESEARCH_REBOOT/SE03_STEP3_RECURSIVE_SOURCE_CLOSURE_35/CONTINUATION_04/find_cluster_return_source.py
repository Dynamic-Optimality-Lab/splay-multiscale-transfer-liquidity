"""Compose accepted native7 source actions along the exact closed B word."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def main():
    model=json.loads((F/'complete_product_model_k0.json').read_text());diag=json.loads((F/'high2_source_work_diagnosis.json').read_text())
    word=[r['KEEP_key'] for r in diag['steps_forward']];marks=model['A_keys'];columns=[marks.index(x) for x in word]
    fixed=[];matching=[]
    def clusters(t,out):
        if t is None:return 0
        bits=(1<<(t[0]-1))|clusters(t[1],out)|clusters(t[2],out);out.add(bits);return bits
    for start in range(429):
        states=[start];H=[];a=start
        for k in columns:H.append(model['A_H'][a][k]);a=model['A_destination'][a][k];states.append(a)
        if a!=start:continue
        fixed.append({'start_A_index':start,'states':states,'H':H})
        if all(h==1 for i,h in enumerate(H) if i%4) and all(H[i]>=3 for i in (0,4)):
            gaps=[]
            for i in (0,4):
                before=set();after=set();clusters(model['A_trees'][states[i]],before);clusters(model['A_trees'][states[i+1]],after)
                gaps.append({'lost':len(before-after),'gained':len(after-before)})
            if all(g['lost']>=5 for g in gaps):matching.append({'start_A_index':start,'states':states,'H':H,'cluster_changes':gaps})
    result={'status':'CACHED_SOURCE_RETURN_COMPOSITION','word':word,'all_fixed_native7_sources':fixed,
      'matching_MC35_blocks':matching,'matching_count':len(matching),'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'meaning':'new source control only if fixed source returned; no old primitive replay',
      'source_B_start_index':diag['steps_forward'][0]['source_B'],
      'input_sha256':{p:hashlib.sha256((F/p).read_bytes()).hexdigest() for p in ('complete_product_model_k0.json','high2_source_work_diagnosis.json')}}
    with (F/'cluster_return_source_composition.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'word':word,'fixed_sources':len(fixed),'matching_sources':len(matching),'matches':matching}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof212_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
