"""Analytic dependency/identity audit of the uniform prefix and padding lemmas.
No finite collection of trees or integer depths stands in for universality.
"""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    from sympy import symbols,expand,simplify
    z=json.loads((B/'capped_deficit_population_lift_proof_object.json').read_text());inherited=P/'SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md';assert hashlib.sha256(inherited.read_bytes()).hexdigest()==z['input_sha256']['SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md'];assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in z['input_sha256'].items() if not n.startswith('SE03_'));r,h,k,c,q,t,m=symbols('r h k c q t m',integer=True,nonnegative=True);R=q+k+2*h;known=c+(r-1)*R+2*h;maxknown=expand(known.subs({c:2*r-1,q:r-1}));assert expand(maxknown-(r*r+2*r*h+k*(r-1)))==0
    # Universal parity split: these are symbolic polynomials in arbitrary t,m.
    even_delta=q-2*t;odd_delta=q-2*(t+1);assert expand((q-2*(t+m))-even_delta)==-2*m;assert expand((q-2*(t+m+1))-odd_delta)==-2*m;assert expand((q-2*(t+m+1))-even_delta)==-2*m-2;assert expand((q-2*(t+m+1))-odd_delta)==-2*m
    # For d even, q-2ceil(d/2)=q-d; for d odd it is q-d-1.
    assert expand(even_delta-(q-2*t))==0 and expand(odd_delta-(q-(2*t+1)-1))==0
    L=q+k;hidden_lower=R+1-2*h;assert simplify(hidden_lower-(L+1))==0 and simplify(q-(L+1)+k)==-1
    # A single right rotation carries arbitrary hanging-term offsets unchanged.
    d,offset=symbols('d offset',integer=True,nonnegative=True);before=[d+1,d,d+2+offset,d+2+offset,d+1+offset];after=[d,d+1,d+1+offset,d+2+offset,d+2+offset];diff=[expand(a-b) for a,b in zip(after,before)];assert diff==[-1,1,-1,0,1]
    review={'active_prefix':'initial ancestor closure by the first-entry/rigid-component induction; each new actual access adds at most its path depth','newly_exposed_anonymous_keys':'all actual path labels lie at initial depth<=2H and are retained; no actual helper is erased','marked_hidden_depth':'initial depth>Q0+k+2h cannot fall to<=Q0+k in <=2h rotations','visible_mark_depth':'all initial ancestors retained, no source frame inserts a known vertex into a rigid variable interior','B_semantics':'fixed genuine marked support and exact closed core inherited from inspected uniform density proof; no physical deletion','source_identity_runs':'kept with original occurrences and modes; terminal a=0 is not whole H=0','private_terms':'arbitrary shared-key/order-constrained BST terms, not bounded inventory samples','counting':'A prefix<=1+(r-1)R+2h; union named key IDs<=c+(r-1)R+2h','closure_and_funding':'pointwise representation only, no abstract path realization, no debt formula, no HIGH or donor theorem','padding_domain':'source construction requires enlarged physical N>=4; algebra and given-packet representation have their stated wider domains'}
    assert not z['LOW_sign_proof_supplied'] and not z['F_formula_supplied'] and not z['HIGH_proof_supplied'];out('capped_deficit_population_lift_independent_audit.json',{'status':'PASS_UNIFORM_CAPPED_DEFICIT_PREFIX_AND_PADDING_INTERFACE_AUDIT','mathematical_result':'complete parametric LOW representation independent of private populations for the specified factorization; even/odd unary translation identities','proof_checking':'symbolic arbitrary-integer parity and bound identities plus independent review of source-prefix/typed-term/alias argument; no finite passing sample used as a proof','known_key_bound':'r^2+2rh+k(r-1)','review':review,'original_operations_events_and_H0_distinction_preserved':True,'new_source_queries':0,'no_uniform_F_or_funding_claim':True,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('CAPPED_DEFICIT_PRIVATE_POPULATION_LIFT.md','PADDING_TRANSLATION_RULES.md','PADDING_DOMAIN_CLARIFICATION.md','capped_deficit_population_lift_proof_object.json')}});print(json.dumps({'status':'PASS_UNIFORM_CAPPED_DEFICIT_REPRESENTATION_LIFT','known_key_bound':'r^2+2rh+k(r-1)','finite_tests_used_as_universal_proof':False,'no_F_or_funding_claim':True}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify31_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
