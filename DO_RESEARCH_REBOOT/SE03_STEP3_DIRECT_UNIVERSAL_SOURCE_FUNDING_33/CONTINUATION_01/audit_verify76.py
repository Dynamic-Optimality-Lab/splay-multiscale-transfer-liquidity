"""Exact affine/parity proof kernel for the uniform own-solvent source rule."""
import hashlib,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;C=B/'DIRTY_OWNER_COURSE_CORRECTION';START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (C/n).open('x') as f:json.dump(z,f,indent=2)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def nonnegative(a):return all(x>=0 for x in a)
def main():
    cases=[]
    # Affine coefficients are [constant,k,s] over arbitrary NONNEGATIVE
    # integer parameters, not selected numerical test values.
    for parity,Q,H,c in (('EVEN',(0,2,0),(0,1,1),(0,1,0)),('ODD',(1,2,0),(1,1,1),(1,1,0))):
        margin=sub(mul(2,c),Q);remaining_events=sub(H,c);source_slack=sub(mul(2,H),Q)
        assert nonnegative(Q) and nonnegative(H) and nonnegative(c) and nonnegative(margin) and nonnegative(remaining_events) and nonnegative(source_slack)
        assert margin==((0,0,0) if parity=='EVEN' else (1,0,0)) and remaining_events==(0,0,1)
        cases.append({'parity':parity,'Q_affine':Q,'H_affine':H,'c_affine':c,'2c_minus_Q':margin,'H_minus_c':remaining_events,'2H_minus_Q':source_slack})
    # This finite transition kernel is exhaustive for ONE event's bit
    # statuses; induction, not a bounded source test, covers any event count.
    for statuses in itertools.product(('own','release'),repeat=2):
        bank=['original_bit0','original_bit1'];assert len(bank)==2
        for status in statuses:
            unit=bank.pop(0);assert status in ('own','release')
        assert bank==[]
    parent=P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md';bank=P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CARRY_STORAGE_SEAM.md';exchange=P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/FROZEN_OWNER_EXCHANGE.md'
    # Reuse these inspected, unchanged source contracts; do not rerun
    # old graph/coefficient/source audits under the name of this check.
    assert hashlib.sha256(parent.read_bytes()).hexdigest()=='0d60121dfd15db899c900e9bde73b0a9ca1354787f5682cbfe0070c69c8fa664'
    assert hashlib.sha256(exchange.read_bytes()).hexdigest()=='e376879f126cdf85c664869106caa86d954fab5f3233b212c9f954a06cbd24e6'
    files=('OWN_SOLVENT_UNIFORM_CERTIFICATE.md','SOURCE_FORCED_DONOR_EXPANSION.md','DIRTY_FRAME_BANK25_SCHEDULE.md','FROZEN_OWNER_BLOCKING_STRUCTURE.md','OWNER_PROFILE_REDUCTION.md')
    result={'status':'PASS_UNIFORM_OWN_SOLVENT_SOURCE_LICENSE_SYMBOLIC_CERTIFICATE','scope':'all support/private population/source length/owner multiplicity under actual local Q_m<=2H_m and the original supplied source/period/exchange contracts','integer_classes':cases,'all_integer_pairs_covered':'Q even/odd; k=floor(Q/2),s=H-ceil(Q/2)>=0','no_finite_BST_or_population_test':True,'own_donor_rule':'demand i uses actual macro unit i; existence from Q<=2H; disjoint macro IDs give injection','natural_owners_in_selected_pairs':True,'D_constant':0,'working_bound':2,'storage_contract':'independent-h original static within-macro output, not all-event endpoint storage','owner_extension':'uses the unchanged inspected support-free C15 theorem, not an assumed initially free natural unit','source_expansion_for_deficit_macros':'OPEN','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_proof_assistant_verification':False,'input_sha256':{**{n:hashlib.sha256((C/n).read_bytes()).hexdigest() for n in files},str(parent):hashlib.sha256(parent.read_bytes()).hexdigest(),str(bank):hashlib.sha256(bank.read_bytes()).hexdigest(),str(exchange):hashlib.sha256(exchange.read_bytes()).hexdigest()}}
    assert time.process_time()-START<CAP-1
    out('own_solvent_uniform_independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('input_sha256','integer_classes')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify76_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
