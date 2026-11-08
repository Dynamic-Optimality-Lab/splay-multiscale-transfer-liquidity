"""Exhaustive six-key integer core/mask/cost partition, no BST sampling."""
import itertools,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    rows=[]
    for c in range(6,12):
        delta=11-c;masks=[]
        for mid in itertools.combinations(range(2,c),4):
            M=(1,)+mid+(c,);P=[(j-1)-(k-j) for j,k in enumerate(M,1)]
            if P[0]==0 and P[-1]==delta and all(0<=p<=delta for p in P):
                masks.append({'marks':M,'P':P})
        assert masks
        qmax=(c-1)//2
        negative=[{'H':1,'Q':q,'slots':q-2} for q in range(3,min(qmax,4)+1)]
        if c==11:negative.append({'H':2,'Q':6,'slots':2,'class':'actual q5/q1 pair'})
        rows.append({'core':c,'deficiency':delta,'necessary_masks':masks,
            'recent5_core_interval':[max(5,c-2),min(9,c)],
            'natural_q_max':qmax,'negative_physical_classes':negative,
            'all_masks_realizable':'NOT_CLAIMED','full_labeled_core':'constant on actual closed period'})
    assert len(rows[0]['necessary_masks'])==1 and len(rows[-1]['necessary_masks'])==1 and len(rows[-2]['necessary_masks'])==16
    out('source_partition_certificate.json',{'status':'COMPLETE_NECESSARY_SOURCE_PARTITION_NOT_FUNDING_CLOSURE',
        'rows':rows,'full_core_size_transitions':'none on any actual closed period; shapes and recent charts may change',
        'auxiliary_core_sizes':[5,6,7,8,9],'auxiliary_core_size_transitions':'none on the recurrent aligned closed auxiliary period',
        'new_finite_tests':0,'source_engine_calls':0})
    print(json.dumps({'status':'PASS_SOURCE_CLASSIFICATION','mask_counts':[(v['core'],len(v['necessary_masks'])) for v in rows],
        'source_engine_calls':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_classification_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
