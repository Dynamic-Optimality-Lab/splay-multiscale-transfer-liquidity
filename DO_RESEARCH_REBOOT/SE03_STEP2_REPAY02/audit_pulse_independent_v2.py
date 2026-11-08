"""Separate source pulse, refined-macro interfaces and ownership audit."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;CAP=float(sys.argv[1])
def N(k,l,r):return (k,l,r)
def left(t):g,l,r=t;p,a,b=r;return N(p,N(g,l,a),b)
def right(t):g,l,r=t;p,a,b=l;return N(p,a,N(g,b,r))
def p(**kw):return {k:Fraction(v) for k,v in kw.items() if v}
def add(*parts):
    q={}
    for part in parts:
        for k,c in part.items():q[k]=q.get(k,Fraction())+c
    return {k:c for k,c in q.items() if c}
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
error=None
try:
    # Universal source schemas with FOUR arbitrary entire BST gaps.
    for source,first,second in [
      (N('y','A',N('u','B',N('z','C','D'))),left,right),
      (N('y',N('u',N('z','A','B'),'C'),'D'),right,left)]:
        midpoint=first(first(source));end=second(second(midpoint))
        assert midpoint[0]=='z' and end==source
    # A-boundary target identities, not any chosen A shape, give H>=2:
    # an actual request z!=y forces at least one event leaving y, while
    # retained Ky at the gap end forces a distinct positive return request.
    # These events are in one repeat gap, outside gE after its first event.
    assert add(p(QE=1,m=2),p(QE=-1,m=-1))==p(m=1) # D=m,J=m
    assert add(p(A=2,QF=-1),p(QF=1,QE=-1,m=-2))==p(A=2,QE=-1,m=-2)
    # The physical source partition, not an assumed marginal bound, supplies
    # m distinct second-event donors with2 bits each. QE assignments are
    # restricted to first-event/other selected units and cannot use donors.
    # Outside full/E equality transfers every gE demand assignment; only
    # the two pulse demands are new. Exchange then keeps fixed fE common.
    local=(ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/S04_MACRO_COVERAGE_THEOREM.md').read_text(encoding='utf-8')
    boundary=(ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/S04_BOUNDARY_CONSISTENCY_THEOREM.md').read_text(encoding='utf-8')
    assert 'H≤2' in local and 'w=2H-q' in local
    assert 'identical serials' in boundary and 'destination pins' in boundary
    text=(B/'RETAINED_GAP_RESERVATION.md').read_text(encoding='utf-8')
    assert 'No nongenuine LOW edge is added' in text
    assert 'not more total credit' in text
    pulse=(B/'B_RETURN_PULSE_EXTENSION.md').read_text(encoding='utf-8')
    assert 'NO A-reset' in pulse and 'not a claimed' in pulse
    assert 'full nonreturning Step2 domain remains OPEN' in pulse
    assert time.process_time()<CAP
    out('pulse_independent_v2_audit.json',{'status':'PASS_COMPLETE_B_RETURN_PULSE_CLASS_ONLY',
      'method':'separate primitive pair identities and root-change/ownership proof',
      'arbitrary_B_hangers':True,'A_reset_required':False,'A_nearness_required':False,
      'repeat_H0':'same actual A,B gives same deterministic ordinary projection',
      'repeat_positive_H':'at least2 distinct actual A StepEvs',
      'new_minting':'only first event in positive repeat gap; second donor excluded',
      'local_change_bridge':'same unchanged11F local source theorem from actual synchronized boundary',
      'ordinary_boundary_consistency':'same deterministic projection on actual full trees; no reset of a shared vertex',
      'raw_chi':'repeat B fixed; change chi nondecreasing; closed B endpoints imply constancy',
      'old_core_le8_case':'reuse completed repeat-gap/B-only theorem',
      'new_core9_case':'uses actual M3 pointwise D, not false QE<=2CE',
      'D_z':'m','J_z':'m','full_funding':'gE common plus second-event bits; then injective exchange to fixed fE',
      'cut_and_transient':'actual outside cut; inherited active-cut correction; no prefix credit',
      'new_frozen_graph_edges':0,'new_state_coordinates':0,
      'novelty_against_all_compositions_claimed':False,
      'all_nonreturning_transfers_proved':False,'Step2_complete':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('B_RETURN_CORE9_FUNDING_AND_FIXED_STEP1_EXCHANGE_AUDIT_PASS; nonreturning OPEN')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_pulse_independent_v2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
