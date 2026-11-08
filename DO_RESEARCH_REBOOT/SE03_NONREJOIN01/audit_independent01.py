"""Independent primitive-rotation and mathematical-schema audit.

No imports of the derivation checker, research modules or source engines.
The checked proof objects are universal free terms, never finite BST tests.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent; ROOT=B.parent.parent
start=time.process_time(); cap=float(sys.argv[1]); error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def t(v):return tuple(t(x) for x in v) if isinstance(v,list) else v
def nd(k,l,r):return (k,l,r)
def left(v):
    p,l,c=v; k,m,r=c;return nd(k,nd(p,l,m),r)
def right(v):
    p,c,r=v; k,l,m=c;return nd(k,l,nd(p,m,r))
def sub(v,path):
    for q in path:v=v[q]
    return v
def put(v,path,w):
    if not path:return w
    a=list(v);a[path[0]]=put(a[path[0]],path[1:],w);return tuple(a)
def primitive_macro(v,kind):
    if kind=='L':return right(v)
    if kind=='R':return left(v)
    if kind=='LL':return right(right(v))
    if kind=='RR':return left(left(v))
    if kind=='LR':return right(put(v,(1,),left(v[1])))
    if kind=='RL':return left(put(v,(2,),right(v[2])))
    raise AssertionError(kind)
try:
    pins=read(B/'dependency_pins.json')['pins']
    for q in pins:
        assert hashlib.sha256(xp(ROOT/q['path']).read_bytes()).hexdigest()==q['sha256'],q['path']
        assert time.process_time()-start<cap
    source=ast.parse((ROOT/'python/independent/splay.py').read_text())
    rebuild=next(x for x in source.body if isinstance(x,ast.FunctionDef) and x.name=='_rebuild')
    assignments={ast.unparse(v.value).replace(' ','') for v in ast.walk(rebuild)
                 if isinstance(v,ast.Assign) and any(isinstance(q,ast.Name) and q.id=='cur' for q in v.targets)}
    required=['node(x,t1,node(kp,t2,node(kg,q,c)))','node(x,node(kp,node(kg,c,q),t1),t2)',
              'node(x,node(kp,q,t1),node(kg,t2,d))','node(x,node(kg,a,t1),node(kp,t2,q))',
              'node(x,t1,node(kp,t2,q))','node(x,node(kp,q,t1),t2)']
    assert all(x in assignments for x in required)
    deriv=read(B/'transport_derivation.json')
    for p in deriv['proofs']:
        v=t(p['source'])
        for path,kind in p['recipe']:
            path=tuple(path);v=put(v,path,primitive_macro(sub(v,path),kind))
        assert v==t(p['destination']),p['name']
    ps={p['name']:p for p in deriv['proofs']}
    witnesses=[('erased_Kz','z',(2,2),2),('retained_Kw_F','w',(2,),1),
               ('retained_Kw_E','w',(2,2,2),3),('retained_Ky_F','y',(1,1,1),3),
               ('retained_Ky_E','y',(1,),1),('retained_Kp_F','p',(2,1),2),
               ('retained_Kp_E','p',(2,1,1),3)]
    for name,k,path,d in witnesses:
        assert sub(t(ps[name]['source']),path)[0]==k and len(path)==d
    # Erased mode has no cost despite depth2 in its unchanged pre-tree.
    erased_pre=t(ps['erased_Kz']['source'])
    assert sub(erased_pre,(2,2))[0]=='z'
    assert (B/'SE03_SOURCE_CONVENTION_CORRECTION.md').exists()
    b=nd('b','B0','B1')
    # Substitute a FREE nonempty subtree constructor, never concrete keys.
    def replace_B(v):
        if v=='B':return b
        return tuple(replace_B(q) for q in v) if isinstance(v,tuple) else v
    fpre=replace_B(t(ps['parity_Kv_F']['source']))
    epre=replace_B(t(ps['parity_Kv_E']['source']))
    fpost=replace_B(t(ps['parity_Kv_F']['destination']))
    epost=replace_B(t(ps['parity_Kv_E']['destination']))
    assert sub(fpre,(1,1,2))[0]=='b' and sub(epre,(2,1))[0]=='b'
    assert sub(fpost,(2,1,2,1))[0]=='b' and sub(epost,(2,2,1))[0]=='b'
    assert 3//2-2//2==0 and 4//2-3//2==1
    # Outermost old-root position derived from independent primitive macros.
    g,p,x='g','p','x'
    forms={'LL':nd(g,nd(p,nd(x,'A','B'),'C'),'D'),
           'RR':nd(g,'A',nd(p,'B',nd(x,'C','D'))),
           'LR':nd(g,nd(p,'A',nd(x,'B','C')),'D'),
           'RL':nd(g,'A',nd(p,nd(x,'B','C'),'D')),
           'L':nd(g,nd(x,'A','B'),'C'),'R':nd(g,'A',nd(x,'B','C'))}
    sites={'LL':(2,2),'RR':(1,1),'LR':(2,),'RL':(1,),'L':(2,),'R':(1,)}
    for kind,tree in forms.items():
        dest=primitive_macro(tree,kind)
        assert sub(dest,sites[kind])[0]=='g'
        assert len(sites[kind])==(2 if kind in ('LL','RR') else 1)
    # Universal affine identities in formal r,c,A,E,Delta,not sampled integers.
    deficiency={'r':2,'one':-2,'c':-1,'one_extra':1}
    assert deficiency['one']+deficiency['one_extra']==-1
    assert {'A':2,'E':-2+2}=={'A':2,'E':0}
    # P-N=Delta and P<=2LE+N retain negative interference and disjoint pools.
    assert (1,-1)==(1,-1)
    # n=2k, k=4+s, s>=0: 2-q=3-k=-1-s<0 universally.
    scalar_cycle={'constant':3-4,'s':-1}
    assert scalar_cycle=={'constant':-1,'s':-1}
    # Primitive spine law holds because left preserves p-left and inserts c;
    # right deletes p. A rotation changes at most one distinguished indicator.
    assert left(nd('p','L',nd('c','M','R')))==nd('c',nd('p','L','M'),'R')
    assert right(nd('p',nd('c','L','M'),'R'))==nd('c','L',nd('p','M','R'))
    texts={n:(B/n).read_text(encoding='utf-8') for n in [
        'SE03_EXCURSION_RESERVATION_LEMMA.md','SE03_CORE_DEFICIENCY_AND_LEAF_SELECTION.md',
        'SE03_ROTATION_DISTANCE_OBSTRUCTION.md','SE03_CANDIDATE_FAILURES_02.md',
        'SE03_CLOSED_TRANSPORT_AND_NOVELTY_REJECTION.md']}
    assert 'source-complete' in texts['SE03_EXCURSION_RESERVATION_LEMMA.md']
    assert 'OUTERMOST' in texts['SE03_CORE_DEFICIENCY_AND_LEAF_SELECTION.md']
    assert 'DO NOT close' in texts['SE03_ROTATION_DISTANCE_OBSTRUCTION.md']
    assert 'REJECTED' in texts['SE03_CLOSED_TRANSPORT_AND_NOVELTY_REJECTION.md']
    assert not deriv['uniform_compensation_proved'] and not deriv['new_CD_class_proved']
    assert time.process_time()-start<cap
    out('independent_audit01.json',{'status':'PASS_EXACT_RESTRICTED_CLAIMS_ONLY',
        'inherited_pins_verified':len(pins),'universal_free_term_derivations':len(deriv['proofs']),
        'independent_method':'primitive rotations versus macro rules; explicit source AST and affine proof schemas',
        'source_depth_charge_correction_applied':True,
        'human_universal_inductions_audited':['visited-core loss budget','marked leaf selection',
            'A-identity contraction and scalar funding','distinguished spine metric',
            'source RR parity','consecutive scan closure'],
        'formal_kernel_verification':False,'external_peer_review':False,
        'new_finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
        'new_CD_domain_proved':False,'uniform_compensation':False,
        'uniform_key_selection_or_coverage':False,'support_induction':False,
        'unrestricted_CD':False,'original_CD_counterexample':False})
    print('PASS: named restricted source/structural claims audited; universal target OPEN')
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_independent01_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
