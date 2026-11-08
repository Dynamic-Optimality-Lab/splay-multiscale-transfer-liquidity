"""Exact source-level Farkas certificate, distinct features and splay kernel."""
import json,time,sys,hashlib,importlib.util,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0;F=fractions.Fraction
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def vectors(tree):
    depth={};sub={};parent={}
    def visit(t,d,p):
        if isinstance(t,str):return set()
        k,l,r=t;depth[k]=d;parent[k]=p;sub[k]={k}|visit(l,d+1,k)|visit(r,d+1,k);return sub[k]
    visit(tree,0,0);size={k:len(v) for k,v in sub.items()};rank={k:v.bit_length()-1 for k,v in size.items()};return depth,sub,parent,size,rank
def features(A,B):
    da,ma,pa,sa,ra=vectors(A);db,mb,pb,sb,rb=vectors(B);K=range(1,11);ans=[]
    for va,vb in ((da,db),({k:v*v for k,v in da.items()},{k:v*v for k,v in db.items()}),({k:v*v for k,v in sa.items()},{k:v*v for k,v in sb.items()}),(ra,rb)):ans.extend((sum(va.values()),sum(vb.values())))
    ans.extend((sum(pa[k]==pb[k] for k in K),sum(ma[k]==mb[k] for k in K),sum(len(ma[k]&mb[k]) for k in K),sum(abs(da[k]-db[k]) for k in K),sum(da[k]*db[k] for k in K),sum(sa[k]*sb[k] for k in K),sum(min(sa[k],sb[k]) for k in K),sum(ra[k]*rb[k] for k in K),sum(abs(ra[k]-rb[k]) for k in K),sum(da[k]==db[k] for k in K),sum(da[k]<db[k] for k in K),sum(sa[k]==sb[k] for k in K)));assert len(ans)==20;return ans
def main():
    global queries
    z=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text());dual=json.loads((B/'uniform_feature_exact_dual.json').read_text())['certificate'];assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in z['input_sha256'].items());sp=importlib.util.spec_from_file_location('independent_feature_source33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_CAP')
        queries+=1
    I.tick=tick
    def shape(t):
        def dump(v,hi):return 'F'+str(hi) if v is None else (v.key,dump(v.left,v.key-1),dump(v.right,hi))
        return dump(t.root,10)
    weighted=[F(0)]*20;price=F(0);total=F(0);summary=[]
    for number,zs in enumerate(z['witnesses']):
        assert zs['dual_edge_number']==number and zs['dual_coefficient']==dual['weights'][number];weight=F(zs['dual_coefficient']);assert weight>0;total+=weight;tt=[I.Tree(fr(zs['initial_diagonal'])) for _ in range(3)];rows={r['occurrence']:r for r in zs['rows']};lru=[];elru=[];start=None;encountered=[]
        for t,(mode,x) in enumerate(zs['reaching_prefix']+zs['word']*zs['L'],1):
            if t==zs['period'][0]:start=(lru[:],elru[:])
            before=tuple(shape(v) for v in tt);pa,ea=tt[0].access(x);pb=pe='';eb=ee=[]
            if mode=='K':pb,eb=tt[1].access(x)
            if mode=='K' and x!=10:pe,ee=tt[2].access(x)
            after=tuple(shape(v) for v in tt)
            if mode=='K':
                if x in lru:lru.remove(x)
                lru.insert(0,x)
                if x!=10:
                    if x in elru:elru.remove(x)
                    elru.insert(0,x)
            if t in rows:
                r=rows[t];encountered.append(t);assert (mode,x)==(r['mode'],r['target']) and before==fr(r['before']) and after==fr(r['after']) and (pa,pb,pe)==(r['A_path'],r['BF_path'],r['BE_path']) and (ea,eb,ee)==(r['A_events'],r['BF_events'],r['BE_events']);assert (len(ea),len(pb)//2,len(pe)//2)==(r['a'],r['qF'],r['qE']) and r['genuine_F']==(mode=='K' and before[1][0]!=x)
        assert encountered==list(rows) and start==(lru,elru) and fr(zs['rows'][0]['before'])==fr(zs['rows'][-1]['after']);assert {r['target'] for r in zs['rows'] if r['genuine_F']}==set(range(1,11));lo,hi=zs['natural_packet'];assert lo==hi and rows[lo-1]['genuine_F'] and rows[lo]['genuine_F'];hit=rows[lo];H,Q=hit['a'],hit['qF'];assert H==1 and Q==zs['packet_Q'];before=features(*fr(hit['before'][:2]));after=features(*fr(hit['after'][:2]));delta=[a-b for a,b in zip(after,before)];weighted=[v+weight*d for v,d in zip(weighted,delta)];price+=weight*(2*H-Q);A=sum(r['a'] for r in zs['rows']);QF=sum(r['qF'] for r in zs['rows']);assert 2*A-QF>=0;summary.append({'edge':number,'natural_occurrence':lo,'period':zs['period'],'Q':Q,'CD_margin':2*A-QF,'weight':str(weight),'feature_change':delta})
    assert total==1 and not any(weighted) and price==F(dual['weighted_price'])<0
    result={'status':'PASS_SOURCE_EXACT_TWENTY_FEATURE_LINEAR_FAMILY_REFUTATION','scope':'ANY real linear coefficients at fixed native-ten support, on EVERY natural packet, no chart supplemental term; not general nonlinear debts or regrouped funding','source_histories':20,'weighted_price':str(price),'weighted_feature_change':list(map(str,weighted)),'all_weights_positive_sum_one':True,'all_source_and_chart_seams_closed':True,'all_periods_CD_safe':True,'new_source_queries':queries,'not_an_actual_negative_source_cycle':True,'no_coarse_double_refutation':True,'principal_U33':'OPEN','external_or_formal_verification':False,'source_summary':summary,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('uniform_feature_dual_source_certificate.json','uniform_feature_exact_dual.json','uniform_feature_basis.py')}};out('uniform_feature_dual_independent_audit.json',result);print(json.dumps({k:result[k] for k in ('status','source_histories','weighted_price','new_source_queries','principal_U33')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify23_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
