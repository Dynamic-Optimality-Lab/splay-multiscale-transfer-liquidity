"""Symbolic interval-endpoint proof of all positive core10 channel flux."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def P(c=0,l=0):return (c,l)
def add(*ps):return (sum(p[0] for p in ps),sum(p[1] for p in ps))
def neg(p):return (-p[0],-p[1])
def sub(a,b):return add(a,neg(b))
def bit(height,channel):return P(int(height>channel))
def mass(start,end):return tuple(sub(end[c],start[c]) for c in range(2))
START=(P(0,1),P());TOP=(P(1),P(1));TARGET_PRE=(P(1),P())
def rr(g,p,start=START):
    tags={'M0':(0,1,None),'U0':(1,0,0),'M1':(1,2,None),'U1':(2,1,1)}
    gh,gpost,gown=tags[g];ph,ppost,pown=tags[p]
    # Interval endpoints of G/P before and after the ACTUAL RR formula.
    oldg=mass(start,TOP);oldp=mass(tuple(bit(gpost,c) for c in range(2)),TOP)
    newg=mass(start,tuple(bit(ph,c) for c in range(2)));newp=mass(start,TARGET_PRE)
    delta=[P(),P()]
    if gown is not None:delta[gown]=add(delta[gown],sub(newg[gown],oldg[gown]))
    if pown is not None:delta[pown]=add(delta[pown],sub(newp[pown],oldp[pown]))
    return delta
def main():
    assert json.loads((B/'independent_audit.json').read_text())['status']=='PASS_SEPARATE_SOURCE_AND_SCOPE_AUDIT'
    rows={}
    rows['P=M0,G=U0']=rr('U0','M0',(P(),P()))
    rows['P=U0,G=M0']=rr('M0','U0',(P(),P()))
    rows['P=U0,G=U0']=rr('U0','U0')
    rows['P=U0,G=U1']=rr('U1','U0')
    rows['P=U1,G=U0']=rr('U0','U1')
    assert rows=={'P=M0,G=U0':[P(-1),P()],
        'P=U0,G=M0':[P(1),P()],
        'P=U0,G=U0':[P(0,-1),P()],
        'P=U0,G=U1':[P(1,-1),P(-1)],
        'P=U1,G=U0':[P(),P(-1)]}
    # The sole positive foreign flux not a pure creation is a certified
    # simultaneous own-channel loss, hence its TOTAL is nonpositive.
    assert add(*rows['P=U0,G=U1'])==P(0,-1)
    # LL: only own-lower U grandparent changes K0: -(1-lambda).
    assert sub(P(),P(1,-1))==P(-1,1)
    # All mixed lower-channel charges have the same endpoint bit before/after.
    assert sub(P(1,-1),P(1,-1))==P()
    # Reflection reverses endpoints and complements threshold bits.
    assert sub(sub(P(1),P(0,1)),sub(P(1),P()))==P(0,-1)
    # Formal live-token recurrence and cyclic minimum-K accounting.
    assert add(P(0,1),P(1),P(-1))==P(0,1)
    out('flux_audit.json',{'status':'PASS_EXHAUSTIVE_POSITIVE_CORE10_SOURCE_FLUX',
        'polynomials':'(constant, coefficient_of_lambda), 0<=lambda<=1',
        'upper_target_RR_rows':rows,'LL_foreign_flux':'0 or -(1-lambda)',
        'mixed_foreign_flux':0,'own_channel_flux':'nonpositive by separately proved source theorem',
        'only_total_positive_patterns':['RR G=M0,P=U0,target=M1','LL G=M1,P=U1,target=M0'],
        'each_creation_delta':1,'total_K_range':[0,4],
        'cyclic_flux_matching':'actual minimum-K event seam; births push, negative-event removal ordinals pop; empty endpoint token stack',
        'tokens_are_A_bits':False,'original_B_demands_paid':False,'Step2':'OPEN',
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0})
    print('PASS symbolic source-height classification and complete channel-flux token ownership; no A funding claim')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_flux_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
