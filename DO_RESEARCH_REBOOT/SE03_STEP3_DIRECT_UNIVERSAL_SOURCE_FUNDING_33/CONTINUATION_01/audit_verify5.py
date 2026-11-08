"""Independent full sparse nine-anchor certificate checker.
Reuses accepted BF source rows; only NEW ordinary actions are replayed.
"""
import json,time,sys,importlib.util,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def rd(p):return json.loads(p.read_text())
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    source=rd(B/'nine_label_native_action_cache.json');cert=rd(B/'native9_sparse_debt_certificate.json');assert hashlib.sha256((B/'nine_label_native_action_cache.json').read_bytes()).hexdigest()==cert['source_cache_sha256']
    T=list(map(fr,source['trees']));N=len(T);index={t:i for i,t in enumerate(T)};assert N==4862 and len(index)==N
    catalan=[1]
    for n in range(1,10):catalan.append(sum(catalan[k]*catalan[n-k-1] for k in range(n)))
    assert catalan[9]==N
    depth=[]
    def grammar(t,lo,hi,d,result):
        if lo>hi:assert t=='F'+str(hi);return
        assert isinstance(t,tuple) and len(t)==3;k,l,r=t;assert lo<=k<=hi;result[k]=d;grammar(l,lo,k-1,d+1,result);grammar(r,k+1,hi,d+1,result)
    for t in T:dd={};grammar(t,1,9,0,dd);depth.append(dd)
    known={};pins={};old=P/'SE03_STEP2_UNARY_A_LIFT_14';receipts=rd(old/'branch_all_independent_audit.json');assert receipts['status']=='PASS_ALL_38_MASKS_BY_23_DIRECT_CERTIFICATES_AND_MIRRORS';receipt_by_name={v['file']:v for v in receipts['receipts']}
    for name,sha in source['reused_certificate_sha256'].items():
        path=old/name;assert hashlib.sha256(path.read_bytes()).hexdigest()==sha and receipt_by_name[name]['sha256']==sha
        r=rd(path);ii=[index[fr(t)] for t in r['BF_trees']]
        for s,t,x,q in r['BF_relation']:
            key=(ii[s],x);v=(ii[t],q);assert key not in known or known[key]==v;known[key]=v
        pins[name]=sha
    reused=len(known)
    for s,t in enumerate(T):known[s,t[0]]=(s,0)
    sp=importlib.util.spec_from_file_location('distinct_native9_verify33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_NATIVE9_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def walk(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,lo,v.key-1),walk(v.right,v.key+1,hi))
        return walk(tree.root,1,9)
    fresh=0
    for s,x,t,q in source['new_source_rows']:
        assert (s,x) not in known;tree=I.Tree(T[s]);path,ev=tree.access(x);assert shape(tree)==T[t] and sum(e['kind']=='DOUBLE' for e in ev)==q and len(ev)==(len(path)+1)//2
        known[s,x]=(t,q);fresh+=1
    assert len(known)==N*9 and fresh==source['new_source_queries']==19805
    D=source['destination'];H=source['H'];Q=source['Q'];mirror=cert['mirror']
    def reflect(t):return 'F'+str(9-int(t[1:])) if isinstance(t,str) else (10-t[0],reflect(t[2]),reflect(t[1]))
    for a,t in enumerate(T):
        assert mirror[a]==index[reflect(t)]
        for x in range(9):assert known[a,x+1]==(D[a][x],Q[a][x]) and H[a][x]==(depth[a][x+1]+1)//2 and Q[a][x]==depth[a][x+1]//2
    table=dict(cert['nonzero_debt']);assert len(table)==len(cert['nonzero_debt'])==123228 and set(table.values())=={1,2}
    def canon(a,b):return min(a*N+b,mirror[a]*N+mirror[b])
    def debt(a,b):return table.get(canon(a,b),0)
    for code,v in table.items():a,b=divmod(code,N);assert T[a][0]==T[b][0] and code==canon(a,b)
    cheap=collections.defaultdict(list)
    for a,t in enumerate(T):
        for x in range(9):
            if H[a][x]==1:cheap[t[0],x].append(a)
    negative=positive=0;minimum=99
    def edge(a,b,at,bt,w):
        nonlocal minimum
        margin=w+debt(at,bt)-debt(a,b);assert margin>=0,(a,b,at,bt,w,margin);minimum=min(minimum,margin)
    # Complete negative-price syntax from ALL zero or positive sources,
    # including the724k pair cells absent from the earlier exploration.
    for b,t in enumerate(T):
        for x in range(9):
            if Q[b][x]>=3:
                for a in cheap[t[0],x]:edge(a,b,D[a][x],D[b][x],2-Q[b][x]);negative+=1
    # At a zero source every remaining LOW weight is nonnegative. At a
    # positive source explicitly regenerate every exact H1/H2 macro frame.
    for code,v in table.items():
        a,b=divmod(code,N);root=T[b][0]-1
        for x in range(9):
            if x!=root and H[a][x]<=2:edge(a,b,D[a][x],D[b][x],2*H[a][x]-Q[b][x]);positive+=1
        for y in range(9):
            if H[a][y]!=1:continue
            at=D[a][y]
            for x in range(9):
                if x!=root and H[at][x]==1:edge(a,b,D[at][x],D[b][x],4-Q[b][x]);positive+=1
    assert max(table.values())==2 and max(max(v) for v in Q)==4
    # HIGH ANY-endpoint inequality is literal6-Q+Dt-Ds>=2-2=0.
    assert all(2*c-min(2*h,q)>=0 for h in (1,2,3,4,20) for q in range(5) for c in (min(h,3),))
    result={'status':'PASS_COMPLETE_NINE_ANCHOR_SOURCE_CERTIFICATE','native_shapes':N,'implicit_reflection_pair_states':2362043,'sparse_nonzero_coefficients':len(table),'width':2,'all_negative_LOW_rows':negative,'all_positive_source_LOW_rows':positive,'minimum_checked_margin':minimum,'HIGH_endpoint_proof':'Q<=4, selected c=3, all debt values0..2, so6-Q+Dt-Ds>=0 for EVERY endpoint','working_bank_bound':8,'new_source_queries':queries,'accepted_source_rows_reused':reused,'all_original_ID_h0_interface':'source-induction proof in NATIVE_NINE_SOURCE_THEOREM.md; no fE replaced','scope':'fixed9 operand anchors; arbitrary full original source words and rigid unaccessed ordered gaps; all marked subsets','anonymous_A_operand_lift':False,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native9_sparse_debt_certificate.json','nine_label_native_action_cache.json','NATIVE_NINE_SOURCE_THEOREM.md')},'reused_receipt_sha256':hashlib.sha256((old/'branch_all_independent_audit.json').read_bytes()).hexdigest()}
    out('native9_sparse_independent_audit.json',result);print(json.dumps({k:result[k] for k in ('status','sparse_nonzero_coefficients','width','all_negative_LOW_rows','all_positive_source_LOW_rows','working_bank_bound','new_source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify5_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
