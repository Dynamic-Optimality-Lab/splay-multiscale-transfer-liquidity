"""Read-only syntactic analysis of saved clauses, not semantic rechecking."""
import collections,hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time();cap=float(sys.argv[1]);error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
try:
    p=ROOT/'DO_RESEARCH_REBOOT/M3_XFER21/M3_CERTIFICATE.json'
    data=p.read_bytes();d=json.loads(data);sections={}
    for name,clauses in [('Step4',d['parent_Step4_certificate']['clauses']),('completion',d['completion_clauses'])]:
        hist=collections.Counter();nhist=collections.Counter();sat=[];negative=[]
        for i,q in enumerate(clauses):
            marks=q.get('marks',[]); nonmarks=q.get('nonmarks',[])
            hist[len(set(marks))]+=1;nhist[len(set(nonmarks))]+=1
            if len(set(marks))>=5 and len(sat)<2:sat.append({'index':i,'clause':q})
            if nonmarks and len(negative)<2:negative.append({'index':i,'clause':q})
            assert time.process_time()-start<cap
        sections[name]={'clauses':len(clauses),'positive_literal_count_histogram':dict(hist),
            'negative_literal_count_histogram':dict(nhist),'saturated_positive_examples':sat,'negative_examples':negative}
    out('subset_clause_syntax.json',{'status':'PASS_SYNTAX_ONLY_NO_OLD_ROW_REPLAY',
        'source_sha256':hashlib.sha256(data).hexdigest(),'sections':sections,
        'baseline_D0_analyzed':False,'universal_source_witness_padding_proved':False,
        'semantic_debt_evaluations':0,'new_masks_tested':0,'new_finite_tests':0,'source_engine_calls':0})
    print(json.dumps(sections,indent=2))
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_subset_syntax_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
