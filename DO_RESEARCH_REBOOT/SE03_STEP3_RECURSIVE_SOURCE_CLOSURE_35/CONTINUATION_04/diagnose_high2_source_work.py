import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def main():
    a=json.loads((F/'branch_H1_r7.json').read_text());m=json.loads((F/'active_a10_model.json').read_text());c=json.loads((F/'branch_high2_02.json').read_text())['cycle'];na=len(a['A_branch_trees'])
    def clusters(t,out):
        if t is None:return 0
        bits=clusters(t[1],out)|clusters(t[2],out)
        if t[0]%1000==0:bits|=1<<(t[0]//1000-1)
        if bits:out.add(bits)
        return bits
    rows=[]
    for e in reversed(c['steps']):
        sb,sa=divmod(e['source_code'],na);tb,ta=divmod(e['target_code'],na)
        before=a['A_branch_trees'][sa];after=a['A_branch_trees'][ta];s=set();t=set();clusters(before,s);clusters(after,t)
        lost=len(s-t);gained=len(t-s);bound=(max(lost,gained)+1)//2
        v=dict(e);v.update({'source_B':sb,'source_A':sa,'target_B':tb,'target_A':ta,
          'KEEP_key':m['B_edges'][e['B_edge_index']]['key'],'marked_clusters_lost':lost,'marked_clusters_gained':gained,
          'source_H_lower_bound':bound,'H2_excluded_by_MC35':e['H']==2 and bound>2,
          'source_A_tree':before,'target_A_tree':after})
        rows.append(v)
    out={'status':'EXACT_HIGH2_SOURCE_WORK_DIAGNOSIS','steps_forward':rows,'abstract_cycle_weight':c['weight'],
      'any_HIGH2_excluded_by_MC35':any(r['H2_excluded_by_MC35'] for r in rows),
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'meaning':'necessary original-source bound, not an independent full-source negative cycle',
      'input_sha256':{p:hashlib.sha256((F/p).read_bytes()).hexdigest() for p in ('branch_H1_r7.json','branch_high2_02.json','MARKED_CLUSTER_WORK_LOWER_BOUND.md')}}
    with (F/'high2_source_work_diagnosis.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'steps':[{k:r[k] for k in ('H','q','KEEP_key','source_H_lower_bound','H2_excluded_by_MC35')} for r in rows]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof211_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
