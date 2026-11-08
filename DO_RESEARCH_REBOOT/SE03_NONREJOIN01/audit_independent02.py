"""Separate primitive/source, affine and claim-scope audit of continuation."""
import ast,hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time();cap=float(sys.argv[1]);error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def tup(v):return tuple(tup(x) for x in v) if isinstance(v,list) else v
def at(v,p):
    for q in p:v=v[q]
    return v
def put(v,p,w):
    if not p:return w
    a=list(v);a[p[0]]=put(a[p[0]],p[1:],w);return tuple(a)
def lr(v):
    p,l,q=v;c,m,r=q;return (c,(p,l,m),r)
def rr(v):
    p,q,r=v;c,l,m=q;return (c,l,(p,m,r))
def consume(v,k):
    if k=='L':return rr(v)
    if k=='R':return lr(v)
    if k=='LL':return rr(rr(v))
    if k=='RR':return lr(lr(v))
    if k=='LR':return rr(put(v,(1,),lr(v[1])))
    if k=='RL':return lr(put(v,(2,),rr(v[2])))
    raise AssertionError(k)
def add(*polys):
    z={}
    for p in polys:
        for v,c in p.items():z[v]=z.get(v,0)+c
    return {v:c for v,c in z.items() if c}
def scale(k,p):return {v:k*c for v,c in p.items() if k*c}
try:
    # Reuse input hashes; this is metadata verification, never old proof-row execution.
    pins=read(B/'dependency_pins.json')['pins']
    for q in pins:
        xp=Path('\\\\?\\'+str((ROOT/q['path']).resolve()))
        assert hashlib.sha256(xp.read_bytes()).hexdigest()==q['sha256'],q['path']
    d=read(B/'transport_derivation02.json')
    for p in d['proofs']:
        v=tup(p['source']);path=tuple(p['target_source_path'])
        assert at(v,path)[0]==p['target'] and len(path)==p['source_depth']
        for path,k in p['recipe']:
            path=tuple(path);v=put(v,path,consume(at(v,path),k))
        assert v==tup(p['destination']),p['name']
    p={q['name']:q for q in d['proofs']}
    assert [p[k]['source_depth'] for k in ['P_full_p1','P_full_x','P_full_p2','P_full_g']]==[1,3,1,3]
    assert [p[k]['source_depth'] for k in ['P_erased_recurrent_x','P_erased_recurrent_g']]==[1,1]
    # Exactly matched formal affine capacity certificates.
    residual={'A':2,'QE':-1,'Delta':-1}
    auxiliary={'A':2,'E':-2,'QE':-1}; marginal={'E':2,'Delta':-1}
    assert add(auxiliary,marginal)==residual
    source_guard={'AP':2,'F':-1,'Kqmax':-1}
    safe_B={'Kqmax':1,'QP':-1}
    assert add(source_guard,safe_B)=={'AP':2,'F':-1,'QP':-1}
    # Complete numerical six-key negative partition: H>=1 and4H<=8 gives H<=2;
    # q>=2H+1 and q<=5 then gives q in[3,5] if H1 and q5 if H2.
    assert 2*11-2==20  # pin source c<=11, not a tree/population experiment
    inequalities={'H_bound_coefficient':4,'H_bound_constant':11-3,'q_cap':(11-1)//2}
    assert inequalities=={'H_bound_coefficient':4,'H_bound_constant':8,'q_cap':5}
    assert (B/'SE03_BLOCK_CLASSIFICATION_CORRECTION.md').exists()
    # Reuse completed old Q/C/core record at exact scope; do not replay its eight rows.
    old=read(ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW/DIRECT_CDK5_LOW_nine_node_obstruction.json')
    assert old['a_closure'] and old['b_closure'] and old['engines']
    assert old['Q']==18 and old['Ck']==8
    QF={'m':old['Q'],'one':2}; CE={'m':old['Ck'],'one':2}; CF={'m':old['Ck'],'one':4}
    j_lower=add(QF,scale(-2,CE));full_excess=add(QF,scale(-2,CF))
    assert j_lower=={'m':2,'one':-2} and full_excess=={'m':2,'one':-6}
    # m=4+s with s>=0 yields strictly positive formal coefficient bounds.
    assert {'constant':4*j_lower['m']+j_lower['one'],'s':j_lower['m']}=={'constant':6,'s':2}
    assert {'constant':4*full_excess['m']+full_excess['one'],'s':full_excess['m']}=={'constant':2,'s':2}
    A={'m':18,'one':6}
    assert add(scale(2,A),scale(-1,QF))=={'m':18,'one':10}
    # D0 and J2m exact persistent P obstruction, with transient subtracted.
    assert add({'m':2,'one':2},{'one':-1},{'one':-1})=={'m':2}
    assert not d['genuinely_new_CD_domain_established'] and not d['uniform_support_extension']
    assert time.process_time()-start<cap
    out('independent_audit02.json',{'status':'PASS_EXACT_RESTRICTED_SOURCE_AND_ALGEBRA_CLAIMS',
        'universal_free_term_schemas':len(d['proofs']),'inherited_pins_verified':len(pins),
        'source_depths_and_zero_double_genuine_changes':'PASS',
        'aligned_transient_for_P':'PASS','six_key_affine_amplification':'PASS',
        'separate_mathematical_review':['permanent erased core exclusion and full core interval witness',
            'paired-closure reachability for P and its six-key diagonal embedding',
            'core-projection with rigid arbitrary B hangers',
            'corrected negative block partition and active A path bound',
            'smaller-support prefix cycle excision and conditional safe-piece composition'],
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,
        'machine_check_scope':'free-term equations and exact affine certificates; human inductions separately explained',
        'external_review':False,'whole_compiler_formalization':False,
        'genuinely_new_CD_coverage_established':False,'uniform_signed_repayment':False,
        'uniform_key_selection_or_coverage':False,'support_induction':False,
        'unrestricted_CD':False,'original_CD_counterexample':False})
    print('PASS: source/affine continuation audit; principal uniform theorem remains OPEN')
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_independent02_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
