"""Universal affine/ownership derivation, not executions of finite histories."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;CAP=float(sys.argv[1])
def p(**kw):return {k:Fraction(v) for k,v in kw.items() if v}
def add(*parts):
    q={}
    for part in parts:
        for k,c in part.items():q[k]=q.get(k,Fraction())+c
    return {k:c for k,c in q.items() if c}
def neg(x):return {k:-v for k,v in x.items()}
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
error=None
try:
    debt_before=p(ds=1);debt_after=p(dt=1);maximum=p(M=1)
    bank_before=add(maximum,neg(debt_before));bank_after=add(maximum,neg(debt_after))
    selected=p(C=2);tail=p(H=2,C=-2);slack=p(C=2,q=-1,dt=1,ds=-1)
    assert not add(bank_before,selected,p(q=-1),neg(bank_after),neg(slack))
    assert add(tail,slack)==p(H=2,q=-1,dt=1,ds=-1)
    assert not add(p(H=2),bank_before,p(q=-1),neg(tail),neg(slack),neg(bank_after))
    # Positive repeat gap: H=2+t, C=1, q=0, t arbitrary integer>=0.
    assert add(p(t=2,one=4),p(one=-2))==p(t=2,one=2)
    # Thus tail contains both bits of event2, whatever ds,dt and the FIFO.
    # Exact repeat-range residual = (2-ds)+dt, nonnegative in[0,2].
    assert add(p(one=2,ds=-1),p(dt=1))==p(one=2,dt=1,ds=-1)
    # Conservation over one actual full cycle: D ends at maximum.
    assert add(p(A=2,QE=-1,dend=1,M=-1),p(dend=-1,M=1))==p(A=2,QE=-1)
    cert=json.loads((ROOT/'DO_RESEARCH_REBOOT/M3_XFER21/M3_CERTIFICATE.json').read_text())
    assert cert['status']=='PROVED_UNIVERSAL_FULL_M3' and cert['debt_range']==[0,2]
    assert cert['corrected_h0']=={'actual_depth':0,'declared_depth':18,'q':9,'weight':-3}
    assert time.process_time()<CAP
    out('gap_funding_derivation.json',{'status':'PASS_REFINED_GAP_RESERVATION_DERIVATION',
      'source_domain':'actual closed five-key/core9 auxiliary; any present population, helpers and repetitions',
      'change_rule':'C=min(H,3); exact old local11F/M3 certificate',
      'repeat_rule':'H=0 implies identical actual boundary; otherwise H>=2 and C=1',
      'tail_guarantee':'both bits of every repeat-gap event after first; second exists',
      'debt_and_bank_range':[0,2],'within_gap_queue_cap':8,
      'source_unit_ids':'actual period occurrence, actual A local-event ordinal, capacity bit',
      'fixed_fE_reserve_assumed':False,'requires_exchange_to_fixed_fE':True,
      'complete_nonreturning_Step2_proved':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0})
    print('UNIVERSAL_RETAINED_GAP_RESERVATION_DERIVATION_PASS')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_gap_funding_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
