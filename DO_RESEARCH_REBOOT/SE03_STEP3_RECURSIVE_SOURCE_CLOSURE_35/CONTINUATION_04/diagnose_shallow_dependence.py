"""Check an exact proposed representation of the existing debt, not JR35."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def main():
    n=json.loads((B/'native10_source_actions.json').read_text());m=json.loads((F/'active_a10_model.json').read_text())
    with (F/'active_a10_05.pkl').open('rb') as f:z=pickle.load(f)
    assert z['status']=='COMPLETE';marks={v:i for i,v in enumerate(m['mark_ranks'])}
    def mask(t):
        if isinstance(t,str):return 0
        return ((1<<marks[t[0]]) if t[0] in marks else 0)|mask(t[1])|mask(t[2])
    def sig(t,depth):
        if isinstance(t,str):return ('gap',)
        if depth<0:return ('opaque',mask(t))
        return (('M',marks[t[0]]) if t[0] in marks else ('U',),sig(t[1],depth-1),sig(t[2],depth-1))
    rows={id(r):r for r in z['level']};answers=[]
    for depth in (1,2,3,4):
        groups=collections.defaultdict(list);features=[]
        for a,t in enumerate(n['trees']):
            key=sig(t,depth);groups[key].append(a);features.append(key)
        witness=None
        for row in rows.values():
            seen={}
            for a,v in row.items():
                key=features[a]
                if key in seen:
                    prior,pv,count=seen[key]
                    if pv!=v:witness={'A1':prior,'D1':pv,'A2':a,'D2':v,'kind':'different_positive_values'};break
                    seen[key]=(prior,pv,count+1)
                else:seen[key]=(a,v,1)
            if witness:break
            for key,(a,v,count) in seen.items():
                if count<len(groups[key]):
                    other=next(k for k in groups[key] if k not in row)
                    witness={'A1':a,'D1':v,'A2':other,'D2':0,'kind':'same_feature_hidden_zero'};break
            if witness:
                witness['B_column']=next(b for b,r in enumerate(z['level']) if r is row)
                witness['A1_tree']=n['trees'][witness['A1']];witness['A2_tree']=n['trees'][witness['A2']]
                break
        answers.append({'visible_depth':depth,'feature_count':len(groups),'exact_debt_factors':witness is None,'witness':witness})
        if time.process_time()-START>CAP-3:break
    report={'status':'EXACT_REPRESENTATION_DIAGNOSIS','results':answers,
       'feature':'full visible ordered prefix to specified depth; M label identity, U kind; below-prefix marked masks; all external gaps retained',
       'source_scope':'completed specified A10/core13 class only',
       'negative_meaning':'the existing minimal debt does not factor through this feature; does NOT rule out another debt or refute JR35',
       'positive_meaning':'factorization on this exact class only, not arbitrary-source lifting',
       'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
       'input_sha256':{'active_a10_05.pkl':hashlib.sha256((F/'active_a10_05.pkl').read_bytes()).hexdigest()}}
    with (F/'shallow_dependence_diagnosis.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('results','input_sha256')}),flush=True)
    print(json.dumps([{k:v for k,v in a.items() if k!='witness'} for a in answers]),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof206_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
