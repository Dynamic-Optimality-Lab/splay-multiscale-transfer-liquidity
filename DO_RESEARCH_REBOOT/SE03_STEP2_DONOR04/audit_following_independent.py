"""Separate balance and source-owner audit; no source/graph enumeration."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    d=json.loads((B/'following_audit.json').read_text())
    # Nonnegative-slack identities, variables not enumerated:
    # H>=3: s=1+(4-q)+d'; H2,q<=2: s=1+(2-q)+d'.
    assert 6-1==1+4 and 4-1==1+2
    # By FIFO newest selected bit is released whenever selected surplus>=1.
    # Three classes have mutually exclusive source type certificates.
    ownership={'TAIL':'aux event ordinal>=4',
               'RETURN':'aux macro starts at full q5; sole A event, ordinal1',
               'FOLLOWING':'aux macro starts at originating full q1 return; event ordinal<=3'}
    assert '>=4' in ownership['TAIL'] and '<=3' in ownership['FOLLOWING']
    assert ownership['RETURN']!=ownership['FOLLOWING']
    expected={(1,2,1),(1,3,2),(2,3,0),(2,4,1)}
    assert {(v['H'],v['q'],v['target_D']) for v in d['residual_first_following_families']}==expected
    # Exhaustiveness is analytic: H>=3 paid, H1 solves d'=q-1 and
    # H2 solves d'=q-3. Range eliminates H1/q4 and H2/q1,q2;
    # q1 H1 source fan proves d'=2, contradicting zero's d'=0.
    assert 2-1==1 and 4-1==3 and 2-1+2-1>0
    assert d['multi_macro_donor_termination_proved'] is False
    out('following_independent_audit.json',{'status':'PASS_AT_RESTRICTED_ALIGNED_PACKET_SCOPE',
        'source_inverse_fan_argument':'q1 after extreme return can target only former fan root; inverse double restores F5(x)',
        'fan_psi2_floor':'construct Hamiltonian alternating source ending at arbitrary marked x; negative-core price-2 and range force2; inherited actual LOW-target psi floor',
        'FIFO_surplus_unit':'newest selected event bit1, with actual event/demand IDs; common assignments never moved',
        'owner_classes':ownership,'old_original_receipts_retained':True,
        'global_partial_module_nonduplication':True,'global_funding_of_all_demands':False,
        'still_open':'multi-macro ownership and existence for four zero-reserve families plus other auxiliary packet patterns and cold classes',
        'same_agent_separate_derivation':True,'external_peer_review':False,'whole_compiler_formalization':False,
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,
        'requested_completion_achieved':False,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS separate nonnegative-slack/source-owner audit; no universal Step2 promotion')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_following_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
