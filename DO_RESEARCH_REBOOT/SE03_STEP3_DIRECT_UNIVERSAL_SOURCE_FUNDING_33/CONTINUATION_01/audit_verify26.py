"""Independent physical source + comparison features + rational zero-edge margin."""
import json,time,sys,hashlib,importlib.util,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0;F=fractions.Fraction
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    sp=importlib.util.spec_from_file_location('independent_diagonal_zero_source33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('AUDIT_LIMIT')
        queries+=1
    I.tick=tick;fp=importlib.util.spec_from_file_location('set_comparison_features33',B/'audit_verify23.py');M=importlib.util.module_from_spec(fp);fp.loader.exec_module(M);z=json.loads((B/'diagonal_zero_source_countercertificate.json').read_text());fail=json.loads((B/'diagonal_zero_vine_adversary.json').read_text());tt=[I.Tree(fr(z['initial_diagonal'])) for _ in range(3)];rows={r['occurrence']:r for r in z['rows']};lru=[];elru=[];boundary=None
    def shape(t):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,v.key-1),walk(v.right,hi))
        return walk(t.root,10)
    for t,(mode,x) in enumerate(z['reaching_prefix']+z['word']*z['L'],1):
        if t==z['period'][0]:boundary=(lru[:],elru[:])
        before=tuple(shape(v) for v in tt);pa,ea=tt[0].access(x);pf=pe='';ef=ee=[]
        if mode=='K':pf,ef=tt[1].access(x)
        if mode=='K' and x!=10:pe,ee=tt[2].access(x)
        after=tuple(shape(v) for v in tt)
        if mode=='K':
            if x in lru:lru.remove(x)
            lru.insert(0,x)
            if x!=10:
                if x in elru:elru.remove(x)
                elru.insert(0,x)
        if t in rows:
            r=rows[t];assert before==fr(r['before']) and after==fr(r['after']) and (pa,pf,pe)==(r['A_path'],r['BF_path'],r['BE_path']) and (ea,ef,ee)==(r['A_events'],r['BF_events'],r['BE_events']);assert (len(ea),len(pf)//2,len(pe)//2)==(r['a'],r['qF'],r['qE'])
    assert boundary==(lru,elru) and fr(z['rows'][0]['before'])==fr(z['rows'][-1]['after']);assert {r['target'] for r in z['rows'] if r['genuine_F']}==set(range(1,11));lo,hi=z['natural_packet'];assert lo==hi and rows[lo-1]['genuine_F'] and rows[lo]['genuine_F'];hit=rows[lo];before=M.features(*fr(hit['before'][:2]));after=M.features(*fr(hit['after'][:2]));assert before==fail['feature_before'] and after==fail['feature_after']
    def transform(v):return [v[0]-v[1],v[2]-v[3],v[4]-v[5],v[6]-v[7],10-v[8],10-v[9],v[0]+v[1]+20-2*v[10],v[11],v[2]+v[3]-2*v[12],v[4]+v[5]-2*v[13],v[0]+v[1]+20-2*v[14],v[16],10-v[17],v[18],10-v[19]]
    def q(v):v=transform(v);return v+[v[i]*v[j] for i in range(15) for j in range(i,15)]
    coeff=list(map(F,fail['formula_exact_coefficients']));margin=F(2*hit['a']-hit['qF'])+sum(c*(a-b) for c,a,b in zip(coeff,q(after),q(before)));assert (hit['a'],hit['qF'])==(2,4) and margin==F(z['candidate_exact_margin'])<0;A=sum(r['a'] for r in z['rows']);Q=sum(r['qF'] for r in z['rows']);assert 2*A-Q==69
    out('diagonal_zero_source_independent_refutation.json',{'status':'PASS_ORIGINAL_ZERO_PRICE_DIAGONAL_ZERO_FORMULA_REFUTATION','period':z['period'],'natural_packet':z['natural_packet'],'H':2,'Q':4,'price':0,'exact_margin':str(margin),'A':A,'QF':Q,'CD_margin':69,'full_erased_and_chart_seams_closed':True,'all_ten_genuine_KEEP_keys':True,'source_queries':queries,'only_frozen_formula_refuted':True,'all_quadratic_comparison_debts_refuted':False,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('diagonal_zero_source_countercertificate.json','diagonal_zero_vine_adversary.json','diagonal_zero_result_02.json')}});print(json.dumps({'status':'PASS_SOURCE_EXACT_ZERO_TRANSFER_REFUTATION','packet':[lo,hi],'H':2,'Q':4,'margin':str(margin),'source_queries':queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify26_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
