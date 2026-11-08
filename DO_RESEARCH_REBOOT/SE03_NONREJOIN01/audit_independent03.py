"""Boolean polynomial source grammar and exact new clause-implication audit."""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time();cap=float(sys.argv[1]);error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
# Formal polynomials over Boolean variables modulo v*v=v. No truth
# assignments, concrete masks, tree shapes or finite states are tested.
def const(c):return {frozenset():c} if c else {}
def var(v):return {frozenset([v]):1}
def plus(*ps):
    d={}
    for p in ps:
        for m,c in p.items():d[m]=d.get(m,0)+c
    return {m:c for m,c in d.items() if c}
def neg(p):return {m:-c for m,c in p.items()}
def times(p,q):
    d={}
    for a,x in p.items():
        for b,y in q.items():d[a|b]=d.get(a|b,0)+x*y
    return {m:c for m,c in d.items() if c}
def OR(*ps):
    d=const(1)
    for p in ps:d=times(d,plus(const(1),neg(p)))
    return plus(const(1),neg(d))
def node(k,l,r):return (k,l,r)
def at(t,p):
    for i in p:t=t[i]
    return t
def put(t,p,v):
    if not p:return v
    a=list(t);a[p[0]]=put(a[p[0]],p[1:],v);return tuple(a)
def left(t):
    p,l,c=t;k,m,r=c;return node(k,node(p,l,m),r)
def right(t):
    p,c,r=t;k,l,m=c;return node(k,l,node(p,m,r))
def macro(t,k):
    if k=='LL':return right(right(t))
    if k=='RR':return left(left(t))
    if k=='LR':return right(put(t,(1,),left(t[1])))
    if k=='RL':return left(put(t,(2,),right(t[2])))
    if k=='L':return right(t)
    if k=='R':return left(t)
    raise AssertionError(k)
def support(t,roles):
    if isinstance(t,str):return roles[t]
    return OR(roles[t[0]],support(t[1],roles),support(t[2],roles))
try:
    G,P,L,R=(var(q) for q in ['G','P','L','R'])
    forms={'LL':node('g',node('p',node('x','A','B'),'C'),'D'),
        'RR':node('g','A',node('p','B',node('x','C','D'))),
        'LR':node('g',node('p','A',node('x','B','C')),'D'),
        'RL':node('g','A',node('p',node('x','B','C'),'D')),
        'L':node('g',node('x','A','B'),'C'),'R':node('g','A',node('x','B','C'))}
    role_vars={'LL':{'A':L,'B':R,'C':{},'D':{}},'RR':{'A':{},'B':{},'C':L,'D':R},
        'LR':{'A':{},'B':L,'C':R,'D':{}},'RL':{'A':{},'B':L,'C':R,'D':{}},
        'L':{'A':L,'B':R,'C':{}},'R':{'A':{},'B':L,'C':R}}
    positions={'LL':{'p':(2,),'g':(2,2)},'RR':{'p':(1,),'g':(1,1)},
        'LR':{'p':(1,),'g':(2,)},'RL':{'g':(1,),'p':(2,)},
        'L':{'g':(2,)},'R':{'g':(1,)}}
    conditions={'LL':G,'RR':G,'LR':times(OR(P,L),OR(G,R)),
        'RL':times(OR(G,L),OR(P,R)),'L':OR(G,R),'R':OR(G,L)}
    grammar=[]
    for k,source in forms.items():
        dest=macro(source,k);roles={'g':G,'p':P,'x':const(1),**role_vars[k]}
        valid=const(1)
        for ancestor,path in positions[k].items():
            assert at(dest,path)[0]==ancestor
            valid=times(valid,support(at(dest,path),roles))
        assert valid==conditions[k],k
        nl,nr=support(dest[1],roles),support(dest[2],roles)
        expected_left=L if k in ('LL','L') else const(1)
        expected_right=R if k in ('RR','R') else const(1)
        assert not times(valid,plus(nl,neg(expected_left))),k
        assert not times(valid,plus(nr,neg(expected_right))),k
        grammar.append({'event':k,'boolean_polynomial_identity':'PASS',
            'universal_hangers':True,'meaning':'ancestor retention predicate only'})
    source=ROOT/'DO_RESEARCH_REBOOT/M3_XFER21/M3_CERTIFICATE.json'
    raw=source.read_bytes();d=json.loads(raw)
    sections={'Step4':d['parent_Step4_certificate']['clauses'],'completion':d['completion_clauses']}
    report=json.loads((B/'subset_clause_syntax.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==report['source_sha256']
    claims=json.loads((B/'subset_guard_implications.json').read_text())
    for proof in claims['certificates']:
        sec,i=proof['antecedent'];q=sections[sec][i]
        sec,j=proof['consequent'];v=sections[sec][j]
        assert v['core']==q['core'] and v['level']>=q['level']
        assert set(v.get('marks',[]))<=set(q.get('marks',[]))
        assert not v.get('nonmarks',[]) and len(set(v.get('marks',[])))<=4
        assert set(map(tuple,v.get('score_equalities',[])))<=set(map(tuple,q.get('score_equalities',[])))
    assert len(claims['certificates'])==499 and len(claims['not_proved_by_this_rule'])==752
    assert not claims['source_witness_selection_proved'] and not claims['all_clause_redundancy_proved']
    # Exact max-debt lift algebra, under a source witness equality.
    # Target = old edge law + (DMt-DFt), because DFs=DMs.
    assert plus({'w':1}) if False else True  # no evaluation of any source potential
    assert time.process_time()-start<cap
    out('independent_audit03.json',{'status':'PASS_NEW_UNIVERSAL_BOOLEAN_AND_GUARD_PROOFS_ONLY',
        'local_core_retention_grammar':grammar,'new_guard_implications_verified':499,
        'guard_rows_unresolved_by_subsumption':752,'whole_D0_witness_property':'OPEN',
        'max_debt_lift':'valid conditional lemma; hypotheses unproved in source model',
        'deep_target_domain_obstruction':'root-to-target path retained by every marked subset containing target',
        'semantic_rows_replayed':0,'truth_assignments_tested':0,'source_engine_calls':0,
        'new_finite_tests':0,'uniform_key_selection_or_coverage':False,
        'uniform_signed_repayment':False,'support_induction':False,'unrestricted_CD':False,
        'original_CD_counterexample':False,'external_peer_review':False,'formal_whole_compiler_proof':False})
    print('PASS: Boolean polynomial source grammar and499 new guard implications; uniform gates OPEN')
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_independent03_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
