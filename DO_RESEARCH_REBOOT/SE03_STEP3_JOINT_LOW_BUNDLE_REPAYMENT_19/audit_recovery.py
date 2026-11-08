"""Producer profiles of a source-derived B-leaf recovery barrier.
New source quantities from stored rows, no rotations/independent audit.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def main():
    sp=importlib.util.spec_from_file_location('C19_recovery_channels',P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py')
    L=importlib.util.module_from_spec(sp);sp.loader.exec_module(L);reports=[]
    for label,name in (('A80','rr7_source_candidate.json'),('B82','overfull_source_result.json')):
        rows=read(OLD/name)['rows'];M={t['target'] for t in rows if t['genuine_F']};v=L.build(rows,M);mm=v['macros']
        zero=lambda m:(m['H'],m['Q'],len(m['branch']),len(m['unary']),m['z'])==(1,2,2,0,1)
        starts=[i for i,m in enumerate(mm) if zero(m) and not zero(mm[(i-1)%len(mm)])];runs=[]
        for i in starts:
            seq=[];j=i
            while zero(mm[j]):
                seq.append(j);j=(j+1)%len(mm);assert len(seq)<len(mm)
            assert len(seq)<=len(M)-3
            runs.append({'macros':seq,'length':len(seq),'leaf_before':len(mm[i]['leaf_before']),
              'leaf_after':len(mm[seq[-1]]['leaf_after'])})
        assert sum(len(m['unary'])-m['z'] for m in mm)==0
        recovery=[{'macro':m['macro'],'H':m['H'],'Q':m['Q'],'leaf_gain':len(m['unary'])-m['z'],
          'comparison_unused_own_count':2*m['H']-min(2*m['H'],len(m['branch'])+m['z'])}
          for m in mm if len(m['unary'])>m['z']]
        reports.append({'source':label,'consecutive_zero_runs':runs,'positive_leaf_recovery':recovery})
    out('leaf_recovery_barrier_profiles.json',{'status':'SOURCE_DERIVATION_AUDIT_PENDING','reports':reports,
      'uniform_lemma':'A chronological run of H1/Q2,beta2,z1 zero macros has length<=r-3. The recovery of B leaves does not force equally many unused A bits.',
      'universal_LOW_supply':'OPEN','source_engine_calls':0})
    print(json.dumps({'status':'SOURCE_LEAF_RECOVERY_BARRIER_PASS','profiles':reports}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_recovery_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
      'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
