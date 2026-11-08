"""Independent free-term checks of induction steps, never instantiate r."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def N(k,l,r):return (k,l,r)
def replace(t,p,fn):
    if not p:return fn(t)
    a,l,r=t
    return N(a,replace(l,p[1:],fn),r) if p[0]=='L' else N(a,l,replace(r,p[1:],fn))
def right(t):a,l,r=t;b,x,y=l;return N(b,x,N(a,y,r))
def left(t):a,l,r=t;b,x,y=r;return N(b,N(a,l,x),y)
def p(**x):return {k:Fraction(v) for k,v in x.items() if v}
def sum_p(*parts):
    q={}
    for part in parts:
        for k,c in part.items():q[k]=q.get(k,Fraction())+c
    return {k:c for k,c in q.items() if c}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
error=None
try:
    # Neighbor scan and maximum-vine induction: A,B,C,D are arbitrary
    # whole subtrees. The maximum suffix has already normalized by IH.
    original=N('a','A',N('b','B',N('x','C','D')))
    forward=left(left(original))
    assert forward==N('x',N('b',N('a','A','B'),'C'),'D')
    assert right(right(forward))==original
    # The arbitrary ascending H_r induction step is RRLL at the next x.
    original=N('a','L',N('b','B',N('n',N('c',N('x','C','D'),'E'),'F')))
    after=replace(original,'RR',lambda t:right(right(t)))
    after=left(left(after))
    assert after==N('x',N('b',N('a','L','B'),'C'),N('c','D',N('n','E','F')))
    # General preparation normal forms: tail E may contain arbitrarily
    # many higher distinguished nodes and arbitrary hanging BSTs.
    start=N('n',N('4',N('3',N('2',N('1','F0','F1'),'F2'),'F3'),'E'),'Fn')
    prepared=replace(start,'LL',lambda t:right(right(t)))
    prepared=right(right(prepared))
    expected=N('1','F0',N('4',N('2','F1',N('3','F2','F3')),N('n','E','Fn')))
    assert prepared==expected
    critical=left(left(prepared))
    assert critical==N('n',N('4',N('1','F0',N('2','F1',N('3','F2','F3'))),'E'),'Fn')
    repaired=replace(critical,'LL',left)
    repaired=replace(repaired,'L',right)
    repaired=right(repaired)
    repaired=left(repaired)
    assert repaired==N('n',N('2',N('1','F0','F1'),N('4',N('3','F2','F3'),'E')),'Fn')
    # Warm/steady erased K5 is the same free term with suffix V>=6.
    warm=N('1','F0',N('2','F1',N('3','F2',N('4','F3',N('5','F4','V')))))
    warm=replace(warm,'RR',lambda t:left(left(t)));warm=left(left(warm))
    steady=N('1','F0',N('2','F1',N('5',N('4',N('3','F2','F3'),'F4'),'V')))
    steady=left(left(steady))
    assert warm==steady
    # Affine cost identities in r. No list/range of integer r is tried.
    A=sum_p(p(r=2,one=-3),p(r=1,one=-2),p(one=2),p(one=1),p(one=3),p(r=3,one=-3))
    Q=sum_p(p(r=2,one=-2),p(r=4,one=-4))
    QE=sum_p(p(r=2,one=-4),p(r=4,one=-8))
    assert A==p(r=6,one=-2) and Q==p(r=6,one=-6) and QE==p(r=6,one=-12)
    assert sum_p(Q,{k:-v for k,v in QE.items()})==p(one=6)
    assert sum_p({k:2*v for k,v in A.items()},{k:-v for k,v in Q.items()})==p(r=6,one=2)
    critical_weight=sum_p(p(one=2),p(r=-1,one=1))
    assert critical_weight==p(r=-1,one=3)
    assert time.process_time()<CAP
    out('induction_audit.json',{'status':'PASS_NECESSARY_RANGE_THEOREM_ONLY',
      'method':'independent primitive free-term induction steps and rational affine identities',
      'r_quantification':'all integers r>=3; no r instantiated or enumerated',
      'fringe_quantification':'all ordered BST gap variables; suffix E arbitrary',
      'source_induction_steps':['neighbor_RR_LL_inverse','maximum_vine_RR_step','ascending_RRLL_step',
                                 'preparation_LLLL','critical_RR','repair_LLR_then_R','warm_steady_erasure_join'],
      'totals':{'A':'6r-2','QF':'6r-6','QE_recurrent':'6r-12','QF-QE':'6','full_slack':'6r+2'},
      'potential_range_necessary':'K>=r-3','range_sufficient_proved':False,
      'Step2_complete':False,'uniform_induction_proved':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,'external_peer_review':False})
    print('UNIFORM_INDUCTION_IDENTITIES_AND_NECESSARY_RANGE_PASS; no sufficiency theorem')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_induction_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
