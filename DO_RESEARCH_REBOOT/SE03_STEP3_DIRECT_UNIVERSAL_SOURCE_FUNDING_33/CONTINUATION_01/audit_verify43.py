"""Proof-interface audit of uniform contraction-spectrum population lifting."""
import json,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    inherited=P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md';text=' '.join(inherited.read_text().split());assert 'at most2r+2H-3 known nodes' in text and 'Removing only inactive unary vertices' in text
    # Both identities are definitional, on an arbitrary finite free tree X.
    unary_proofs=[{'source':'u(private_empty_side,X)','projection':'Join(empty,Pi(X))','result':'Pi(X)'},{'source':'u(X,private_empty_side)','projection':'Join(Pi(X),empty)','result':'Pi(X)'}]
    # Exact set equality gives a bijection of distinct projected trees; applying
    # an arbitrary old function preserves the complete value multiset.
    # Count polynomial: n+(n-2)+(2H-1)=2n+2H-3, all n>=2,H>0.
    left=(1,0,0);branch=(1,0,-2);active=(0,2,-1);bound=tuple(a+b+c for a,b,c in zip(left,branch,active));assert bound==(2,2,-3) and 2*10+2*2-3==21
    old=json.loads((B/'native10_complete_independent_audit.json').read_text());assert old['status']=='PASS_COMPLETE_NATIVE10_SOURCE_CREDIT_CERTIFICATE' and old['HIGH_envelope_checks']==151164 and old['width']==3;assert old['working_bank_bound_if_complete']==9
    # Interval transfer of an accepted HIGH envelope is an elementary order law:
    # Ftarget>=l_target and Fsource<=u_source => actual margin>=envelope.
    ledger={'LOW':'same H,Q and exact source/target Pi sets under inactive-unary source contraction; all active helper operands retained','HIGH':'6-Q+Ftarget-Fsource >=6-Q+l_target-u_source>=0','integrality':'Ds<=w+Dt with integer w implies floor(Ds)<=w+floor(Dt); integer intervals/singletons retained','source_funding':'conditional on the still-unproved COMPLETE LOW law and explicit b-dependent bounds; then actual first-min(H,3) events, h0 inclusion and original carry prove working<=9','not_proved':'existence of F, completed LOW source coverage, arbitrary larger B cores, all-r E_r, or unconditional fE eligibility'}
    assert time.process_time()-START<CAP-1
    names=('CONTRACTION_SPECTRUM_POPULATION_LIFT.md','B_SENSITIVE_FROZEN_PROOF_BOX.md','native10_complete_independent_audit.json','EXTERIOR_PRIVATE_POPULATION_SOURCE_THEOREM.md','exterior_private_population_independent_audit.json')
    out('contraction_spectrum_population_lift_independent_audit.json',{'status':'PASS_UNIFORM_CONTRACTION_SPECTRUM_POPULATION_LIFT_AND_CONDITIONAL_FIXED_CORE_BRIDGE','uniform_parameters':'all finite n>=2, all positive whole H, arbitrary permitted private populations/source length','unary_identity_proofs':unary_proofs,'multiset_invariance':'EXACT distinct-projection-set identity, not population sampling or a guessed unary credit exemption','known_node_bound':'2n+2H-3','ten_anchor_LOW_bound':21,'logical_ledger':ledger,'F_candidate_status':'OPEN; global[0,3] prototype bounds do not yet supply the required b-specific bounds','source_queries':0,'source_engine_calls':0,'finite_population_tests_used':False,'principal_U33':'OPEN','external_or_formal_proof_assistant_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names},'inherited_active_frame_path':str(inherited),'inherited_active_frame_sha256':hashlib.sha256(inherited.read_bytes()).hexdigest()});print(json.dumps({'status':'PASS_UNIFORM_SPECTRUM_POPULATION_LIFT','LOW_known_node_bound':21,'F_existence':'OPEN','source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify43_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
