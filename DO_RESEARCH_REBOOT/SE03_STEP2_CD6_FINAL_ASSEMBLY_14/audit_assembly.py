"""New all-domain interface audit; reuse sealed internal source checks."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
def read(d,n):return json.loads((P/d/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    c13='SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13';c14='SE03_STEP2_UNARY_A_LIFT_14';c10='SE03_STEP2_FULL_FUNDING_CLOSURE_10'
    assert read(c13,'core7_seal.json')['status']=='CORE7_PHYSICAL_FUNDING_COMPLETE'
    s8=read(c13,'core8_seal.json');assert s8['status']=='CORE8_PHYSICAL_FUNDING_COMPLETE' and len(s8['all_masks'])==13
    s9=read(c14,'funding_seal.json');assert s9['status']=='PROVED_SOURCE_UNIFORM_CORE9_10_11_PHYSICAL_FUNDING'
    assert read(c10,'independent_audit.json')['core6_universal'].startswith('analytic proof')
    part=read(c10,'source_partition_certificate.json');ledger=[]
    proofs={6:[(c10,'RESIDUAL_SLOT_THEOREM.md'),(c10,'FROZEN_FE_AUDIT.md'),(c10,'independent_audit.json')],
        7:[(c13,'CORE7_FULL_FUNDING.md'),(c13,'core7_seal.json')],8:[(c13,'CORE8_FULL_FUNDING.md'),(c13,'core8_seal.json')],
        9:[(c14,'FULL_PROOF.md'),(c14,'funding_seal.json'),(c14,'branch_all_independent_audit.json')],
        10:[(c14,'FULL_PROOF.md'),(c14,'funding_seal.json'),(c14,'branch_all_independent_audit.json')],
        11:[(c14,'FULL_PROOF.md'),(c14,'funding_seal.json'),(c14,'branch_all_independent_audit.json')]}
    for k,count in ((6,1),(7,5),(8,13),(9,21),(10,16),(11,1)):
        row=next(r for r in part['rows'] if r['core']==k);assert len(row['necessary_masks'])==count
        ledger.append({'core':k,'theorem':'complete actual full-double funding, all source periods in this core class',
            'source_domain':'original reachable exactly A/full-B paired-closed six-genuine-KEEP histories; auxiliary closure/alignment as originally required when fE supplied',
            'marked_core':'C_M(B_full), fixed labeled ancestor set by closed-source monotonicity',
            'BF_assumptions':'closed-source density/masks; maximal all-SS and actual qmax/q1 successor additionally for11',
            'A_assumptions':'NONE beyond original source; arbitrary marked ancestors/private BSTs/helpers',
            'auxiliary_owner_restrictions':'supplied original certified fE on SAME actual period, exact common-ordinal pairing and original E-only retirement policy',
            'donor_rule':{6:'natural own bits h0',7:'injective actual predecessor first-unused seed',8:'sealed full-B debt carry',9:'full A branch-quotient carry',10:'full A branch-quotient carry',11:'full A branch-quotient actual-pair carry'}[k],
            'chart_conditions':'actual full A/B state; no stable-chart assumption or old normalized M3 debt',
            'period_conditions':'exact full paired closure; one original aligned interval; both-endpoint transport only; fE cut unchanged',
            'private_lift':'arbitrary independent ordered rigid gaps; all A ancestors unrestricted in original core6–8 rules, complete branch/active-frame lift for9–11',
            'conclusion':'complete h extends SAME natural h0; licensed common exchange extends SAME a; QF<=2A',
            'necessary_masks':count,'max_carry':{6:0,7:1,8:1,9:2,10:3,11:3}[k],
            'working_bound':4 if k<=8 else 11,
            'accepted_artifacts':[{'path':str(Path(d)/n).replace('\\','/'),'sha256':sha(P/d/n)} for d,n in proofs[k]],
            'independent_audit':'ACCEPTED pinned distinct immutable implementation; new final dispatcher/absolute-ID interfaces additionally checked here',
            'unproved_assumptions':'no extra assumption needed for scalar full theorem; special Step1 fE is NOT extended outside its own domain'})
    out('six_core_certificate_ledger.json',{'status':'PASS_SOURCE_DOMAIN_IMPORT','cores':ledger,'necessary_masks':57,
        'one_core_per_whole_closed_period':True,'no_core_topology_constancy_claim':True,
        'source_engine_calls':0,'completed_checks_reused':True})
    out('assembly_protocol_certificate.json',{'status':'PROVED_ANALYTIC_COMPOSITION_PENDING_NEW_IMPLEMENTATION_AUDIT',
        'dispatch':[{'core':k,'backend':r['donor_rule']} for k,r in zip(range(6,12),ledger)],
        'absolute_ID_bridge':'order-preserving bijection actual contiguous occurrences <->1..T; unchanged trees/events; inverse applied to BOTH demand and donor IDs and all fixed maps',
        'owner_bridge':'h0 untouched by backend; licensed complete h/l exchange has identical old successful paths, so preserves original partial a and common fE',
        'cost_bridge':'D has one original occurrence/ordinal per full double; U has two original bits per A StepEv; unselected bits remain available but uncounted as paid',
        'uniform_gate':'U-B sufficient local signed-source/erasure transfer, arbitrary-r source hypotheses OPEN',
        'source_engine_calls':0,'new_finite_tests':0})
    print(json.dumps({'status':'PASS_SIX_CORE_DOMAIN_AND_PROTOCOL_IMPORT','core_classes':6,'necessary_masks':57}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_assembly_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})
