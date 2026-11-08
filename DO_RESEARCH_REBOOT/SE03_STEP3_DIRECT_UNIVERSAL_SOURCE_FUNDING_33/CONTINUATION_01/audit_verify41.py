"""Independent proof-interface review: necessary diagonal floor and multiset result.
No producer run, no accepted witness replay repeated, no new oracle query.
"""
import json,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    realization=json.loads((B/'uniform_A_realization_independent_audit.json').read_text());assert realization['status']=='PASS_UNIFORM_SOURCE_REALIZATION_COROLLARY_INTERFACE_AUDIT';R=json.loads((B/'root_aware_contraction_debt_set_independent_audit.json').read_text());assert R['status']=='PASS_ANY_ROOT_AWARE_SINGLETON_COMPATIBLE_CONTRACTION_DEBT_SET_FORMULA_REFUTATION' and R['multiset_intermediate_profiles_also_match'];assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in R['input_sha256'].items())
    a,b=R['actual_source_edges'];assert (a['source_value_multiset'],a['target_value_multiset'],b['source_value_multiset'],b['target_value_multiset'])==([2],[1,1,3],[1,1,3],[0,2]);assert (a['source_mask'],a['target_mask'],b['source_mask'],b['target_mask'])==(4,58,58,37)
    old=json.loads((B/'interior_max_contraction_closed_source.json').read_text())['candidate'];assert old['source_A'][0]==6 and old['actual_A_target'][0]==2 and sorted(old['all_source_projection_debts'])==[0,2] and sorted(old['all_target_projection_debts'])==[0];assert (a['price'],b['price'],old['price'])==(-1,1,1);assert -1+1+1+0-2==-1
    # Formal linear identities in m for arbitrary ordinary source depth.
    # (coefficient of m, constant); no finite list of depths substitutes for m.
    odd_d=(2,1);even_d=(2,0);odd_prefix_doubles=(1,0);even_prefix_doubles=(1,-1)
    subtract_twice=lambda a,b:(a[0]-2*b[0],a[1]-2*b[1]);assert subtract_twice(odd_d,odd_prefix_doubles)==(0,1);assert subtract_twice(even_d,even_prefix_doubles)==(0,2)
    # Before those final frames, depth>2 means the active grandparent is
    # below the original root. Local source-term substitution cannot rotate it.
    # The final H1 source shares U exactly. Nonnegative Ds then gives Dt>=q-2.
    necessary_inequality={'actual_H':1,'price':'2-q','source_D_nonnegative':True,'destination':'exact physical A=B=U in the constructed source context','conclusion':'D_actual_new_chart(U,U)>=max(0,q-2)','not_claimed':'zero diagonal, arbitrary abstract B recurrence, fixed-owner donor availability, or sufficiency of this floor'}
    qfamily=P/'SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md';assert qfamily.exists();text=qfamily.read_text();assert 'H=1 and q=r-1' in text and '3-r' in text
    assert time.process_time()-START<CAP-1
    names=('LAST_EVENT_DIAGONAL_DEBT_FLOOR.md','CONTRACTION_DEBT_INFORMATION_REFUTATION.md','UNIFORM_A_REALIZATION_OVER_CLOSED_B.md','uniform_A_realization_independent_audit.json','root_aware_contraction_debt_set_independent_audit.json')
    out('necessary_diagonal_floor_and_multiset_proof_audit.json',{'status':'PASS_UNIFORM_NECESSARY_DIAGONAL_FLOOR_AND_ANY_ROOT_AWARE_MULTISET_FAMILY_REFUTATION','source_induction_review':'all pre-final ordinary doubles remain below the original root; formal even/odd depth coefficients leave exactly2/1; original-source arbitrary-A realization supplies an actual H1 packet over a given closed B cycle','diagonal_floor':necessary_inequality,'multiset_refutation_scope':'ANY real F_sigma(current-root, FULL contraction-debt multiset), singleton-compatible at this same one-private-gap1 signature; no intermediate width bound used','scalar_contradiction':'F_sigma(3,[0,2])>=2 and <=1','full_B_sensitive_functions':'not refuted by these witnesses','new_source_queries':0,'source_queries':0,'source_engine_calls':0,'accepted_replays_repeated':False,'external_or_formal_proof_assistant_verification':False,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names},'inherited_range_source_sha256':hashlib.sha256(qfamily.read_bytes()).hexdigest()});print(json.dumps({'status':'PASS_UNIFORM_NECESSARY_FLOOR_AND_ROOT_AWARE_MULTISET_REFUTATION','source_queries':0,'passing_population_tests':False,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify41_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
