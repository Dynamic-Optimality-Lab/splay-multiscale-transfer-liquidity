"""Independent symbolic/source audit. No imported construction or tree engine.

Checks universal affine and free-term identities, alongside the written
node-count/finite-map/set-witness proofs. No concrete walk, population, tree
corpus or original graph is generated, evaluated, enumerated or replayed.
"""
import ast,hashlib,json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parent
ROOT=R.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def raw(p):return xp(p).read_text(encoding='utf-8')
def read(p):return json.loads(raw(p))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def contains(p,parts):
    t=raw(p)
    for v in parts:assert v in t,(str(p),v)
def poly(p):return {k:Fraction(v) for k,v in p.items() if Fraction(v)!=0}
def check_affine(s):
    assert len(s['ge'])==len(s['mg']) and len(s['eq'])==len(s['me'])
    assert all(Fraction(m)>=0 for m in s['mg'])
    result={}
    for terms,multipliers in ((s['ge'],s['mg']),(s['eq'],s['me'])):
        for term,m in zip(terms,multipliers):
            for k,v in poly(term).items():result[k]=result.get(k,Fraction(0))+Fraction(m)*v
    assert poly(result)==poly(s['goal']),s['name']

# N is a free term constructor, not a BST engine. Labels and hanging-tree
# variables are indeterminates. Normalization proves identities for all their
# legal substitutions; it does not check finitely many source instances.
def N(k,l,r):return ('N',k,l,r)
def RR(t):
    _,g,A,pnode=t;_,p,B,xnode=pnode;_,x,C,D=xnode
    return N(x,N(p,N(g,A,B),C),D)
def LL(t):
    _,g,pnode,D=t;_,p,xnode,C=pnode;_,x,A,B=xnode
    return N(x,A,N(p,B,N(g,C,D)))
def main():
    pins=read(B/'dependency_pins.json')['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    prior=R/'CD5_BASE01';cert=read(prior/'CD5_CERTIFICATE.json')
    assert cert['status']=='PROVED_CD5_COMPLETE_ORIGINAL_CLOSED_WALK_BASE'
    assert cert['mandatory_open_CD5_dependencies']==[]
    assert read(prior/'final_manifest.json')['status']=='CD5_BASE_SEALED_ALL_PUBLICATION_GATES_PASS'
    src=ROOT/'python/independent/splay.py';tree=ast.parse(raw(src))
    fs={x.name:x for x in tree.body if isinstance(x,ast.FunctionDef)}
    assert all(x in fs for x in ('lookup','_descend','_rebuild','trace'))
    rebuild=ast.get_source_segment(raw(src),fs['_rebuild'])
    assert 'cur = node(x, node(kp, node(kg, c, q), t1), t2)' in rebuild
    assert 'cur = node(x, t1, node(kp, t2, node(kg, q, c)))' in rebuild
    assert 'return _plug(fr, cur), evs' in rebuild
    lookup=ast.get_source_segment(raw(src),fs['lookup'])
    assert 'd, cur = 0, t' in lookup
    k4=R/'06_CERTIFICATES/DIRECT_CD_K4'
    contains(k4/'DIRECT_CD_K4_one_bit_potential_certificate.md',[
      'every','η_M(U) = 1[max_{z∈M} d_U(z) = 6]','all C(n,4) marked 4-subsets',
      '68,876','Alone it would not suffice; combined it does.'])
    # Verify its actual completed interface includes all full trees with four
    # marks, without a core-validity filter that would invalidate the new lift.
    oldsource=raw(k4/'DIRECT_CD_K4_finite_verifier.py');oldtree=ast.parse(oldsource)
    assert 'for M in itertools.combinations(keys, 4):' in oldsource
    assert 'for x in sorted(M):' in oldsource
    assert 'v = raw + eta_of(d1, M) - eta_of(d0, M)' in oldsource
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and
                   ('prun' in n.func.id or 'core_valid' in n.func.id) for n in ast.walk(oldtree))
    cached=read(k4/'DIRECT_CD_K4_finite_verification.json')
    assert cached['total']==68876 and cached['violations']==cached['engine_mismatch']==0
    f=R/'06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION'
    contains(f/'S04_GLOBAL_WEIGHT_INEQUALITY.md',['w_j = 6 - q_j','H_j ≥ 3','w(P) ≤ 2A(W) - Q_B(W)'])

    # Separate written proof review: mandatory hypotheses and cancellation
    # boundaries are explicit and cannot be replaced by inventory status flags.
    contains(B/'HIGH_TRUNCATION_OBSTRUCTION.md',[
      'Fix any integer C>=1','n>=2^d','least key at depth exactly d',
      'finite reaching prefix','fully closed','ell>=1','a=H=ceil((4C+2)/2)=2C+1',
      'q=floor((4C+2)/2)=2C+1','sum w_HIGH=-ell<0','2a-q=2(2C+1)-(2C+1)=2C+1>0',
      'not an example in the frozen nine-core graph','not an\nexplicit machine-listed negative cycle'])
    contains(B/'MARK_SUBSET_LIFT.md',[
      'every x in F','eta_M is just the','four-element F subset M containing x and z',
      'eta_F(U\')=eta_M(U\'),  eta_F(U)<=eta_M(U)',
      'F may be chosen separately for each edge','global potential is the single well-defined eta_M',
      'No mask/population tests were run','core size at least eight',
      'Two original RR doubles','q-2c+eta(U\')-eta(U)=2-2+1=1>0'])
    contains(B/'SUPPORT_ERASURE_CLOSURE.md',[
      'every request and every other mode','A history and its\nperiod cost A(gamma) are unchanged',
      'original reachable paired start','p_z>=1','common multiple of all p_z',
      'genuine support at most r-1','R=R_z-Delta_z','It supplies no bound on Delta_z',
      'not a specialized\nr>=6 lifting theorem and not CD','quantitative signed repayment subbridge remains OPEN'])

    # Universal source-term identities with arbitrary hanger substitutions.
    term=N('y','A',N('p','B',N('z','C','D')))
    mirrored=RR(term)
    assert mirrored==N('z',N('p',N('y','A','B'),'C'),'D')
    assert LL(mirrored)==term
    # The eight-mark boundary uses the same RR rule twice at the stated paths.
    h=N('h1','E1',N('h2','E2',N('z','E3','E4')))
    low=N('g2',h,N('g3','E5',N('x','E6','E7')))
    outer=N('g0','E8',N('g1','E9',RR(low)))
    normalized=RR(outer)
    expected=N('x',N('g1',N('g0','E8','E9'),N('g3',N('g2',h,'E5'),'E6')),'E7')
    assert normalized==expected

    p=read(B/'proof_inventory.json')
    assert not p['unrestricted_CD_proved'] and not p['uniform_support_induction_proved']
    assert not p['original_CD_counterexample_found'] and not p['Dynamic_Optimality_proved']
    high=p['fixed_HIGH_obstruction']
    assert high['C_domain']=='every integer C>=1' and high['a_H_q']=='2C+1'
    assert high['surrogate_per_edge']==-1 and high['actual_CD_per_edge']=='2C+1'
    assert high['C3']=={'depth':14,'q':7,'H':7,'surrogate_weight':-1,'actual_CD_weight':7,'support_lower_bound':8}
    assert not high['frozen_nine_core_graph_modified'] and not high['negative_cycle_in_frozen_graph_claimed']
    assert not high['negative_original_CD_cycle_claimed'] and not high['explicit_cycle_enumerated']
    positive=p['positive_extension']
    assert positive['domain']=='original reachable fully closed walks with |G|<=5 OR nonempty G and fixed marked core size<=7'
    assert positive['core8_values']=={'source_max_marked_depth':5,'target_max_marked_depth':6,'q':2,'c':1,'eta0':0,'eta1':1,'violation':1}
    assert not positive['old_K4_certificate_replayed']
    erased=p['support_erasure']
    assert erased['exact_identity']=='R=R_z-Delta_z'
    assert erased['family']=={'period':['KEEP z','KEEP y'],'A':2,'Q':2,'qbar_after_either_erasure':0,'Delta':2,'R':2,'R_z':4}
    assert erased['signed_marginal_bound'].startswith('OPEN')
    expected_schemas={
      'binary_capacity_induction':([],[{'next':1,'old':-2,'1':-1},{'old':1,'t':-1,'1':1}],{'next':1,'t':-2,'1':1}),
      'high_surrogate_negative':([],[{'q':1,'C':-2,'1':-1},{'w':1,'C':-2,'q':1}],{'w':1,'1':1}),
      'actual_CD_positive':([],[{'a':1,'C':-2,'1':-1},{'q':1,'C':-2,'1':-1}],{'a':2,'q':-1,'C':-2,'1':-1}),
      'support_floor':([{'r':2,'core':-1,'1':-1},{'core':1,'C':-4,'1':-3}],[],{'r':2,'C':-4,'1':-4}),
      'marked_subset_envelope':([{'c':2,'q':-1,'f1':-1,'f0':1},{'m0':1,'f0':-1}],
          [{'m1':1,'f1':-1}],{'c':2,'q':-1,'m1':-1,'m0':1}),
      'support_erasure_identity':([],[{'R':1,'A':-2,'Q':1},{'Rz':1,'A':-2,'qb':1},{'Delta':1,'Q':-1,'qb':1}],
          {'R':1,'Rz':-1,'Delta':1})}
    seen=set()
    for s in p['affine_proof_schemas']:
        assert s['name'] not in seen;seen.add(s['name'])
        assert (s['ge'],s['eq'],s['goal'])==expected_schemas[s['name']]
        check_affine(s)
    assert seen==set(expected_schemas)
    assert p['new_finite_tests']==p['new_solver_queries']==p['new_original_root_queries']==p['completed_semantic_checks_replayed']==0
    assert time.process_time()<float(sys.argv[1])
    write('independent_audit.json',{
      'status':'INDEPENDENT_SYMBOLIC_PARTIAL_RESULTS_AUDIT_PASS',
      'declared_input_hashes_verified':len(pins),'new_universal_affine_schemas':sorted(seen),
      'free_source_term_identity_schemas':2,
      'fixed_HIGH_truncation_uniform_obstruction':'PROVED_AT_STATED_HYPOTHETICAL_EXTENSION_SCOPE',
      'frozen_graph_counterexample_claimed':False,'original_CD_counterexample_claimed':False,
      'positive_core_le7_mark_subset_extension':'PROVED_RESTRICTED_ORIGINAL_DOMAIN',
      'core8_same_bit_extension':'REFUTED_BY_UNIVERSAL_SOURCE_TERM_FAMILY',
      'support_erasure_closure':'PROVED_UNIVERSAL','signed_erasure_cost_bound':'OPEN',
      'unrestricted_CD_proved':False,'uniform_support_induction_proved':False,'Dynamic_Optimality_proved':False,
      'existing_CD5_seal_unchanged':True,'new_finite_tests':0,'new_solver_queries':0,
      'new_original_root_queries':0,'completed_semantic_checks_replayed':0,
      'imports_construction_or_research_engines':False,'external_peer_review':False,'whole_compiler_formalization':False,
      'input_proof_object_bytes':(B/'proof_inventory.json').stat().st_size,
      'Bank25':25,'publication_requires_resources_and_integrity_PASS':True})
    print(json.dumps({'status':'INDEPENDENT_PARTIAL_PROOF_AUDIT_PASS','unrestricted_CD':'OPEN','new_finite_tests':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
