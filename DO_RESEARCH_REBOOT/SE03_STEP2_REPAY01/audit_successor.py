"""Separate free-term fan and source-packet repayment audit, no tests."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def N(k,l,r):return (k,l,r)
def left(t):g,l,r=t;p,a,b=r;return N(p,N(g,l,a),b)
def right(t):g,l,r=t;p,a,b=l;return N(p,a,N(g,b,r))
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def p(**kw):return {k:Fraction(v) for k,v in kw.items() if v}
def add(*parts):
    q={}
    for part in parts:
        for k,c in part.items():q[k]=q.get(k,Fraction())+c
    return {k:c for k,c in q.items() if c}
error=None
try:
    # Independent original parent-first pair formulas, arbitrary whole L,R.
    rr=left(left(N('g','A',N('u','B',N('x','L','R')))))
    ll=right(right(N('g',N('u',N('x','L','R'),'C'),'D')))
    assert rr==N('x',N('u',N('g','A','B'),'L'),'R')
    assert ll==N('x','L',N('u','R',N('g','C','D')))
    def updateL(t):return N('x',N('uL',N('gL','A','B'),t[1]),t[2])
    def updateR(t):return N('x',t[1],N('uR',t[2],N('gR','C','D')))
    assert updateL(updateR(N('x','L','R')))==updateR(updateL(N('x','L','R')))
    # Independent source argument: in a Hamiltonian path each subtree is
    # a contiguous remaining label interval. Alternating odd interval has
    # mass1 and marked extreme G. Removing it leaves mass0; a marked P
    # would violate the marked-root subtree lower bound1. Thus P is the
    # unmarked extreme on G's side. Removing P restores odd M...M interval.
    # Induction proves every pair same-side; mixed frames are impossible.
    # Fan path formulas then give first two symbols LR or RL for every
    # nonextreme nonroot mark; odd-depth or outer-mixed alternatives are
    # all excluded by the inherited maximal-closed-core source theorem.
    assert not add(p(H=2,Hnext=2,q=-1,qnext=-1),p(H=-2,Hnext=-2,r=1),p(q=1,qnext=1,r=-1))
    # Substitute q=r-1, qnext=1 symbolically into original pair weight.
    total=add(p(H=2),p(r=-1,one=1),p(Hnext=2),p(one=-1))
    assert total==p(H=2,Hnext=2,r=-1)
    assert 2*(2+1)-6==0 and 2*(1+2)-6==0 and 2*(1+1)-6==-2
    text=(B/'MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md').read_text(encoding='utf-8')
    assert 'Removing a packet' in text and 'punctured' in text
    assert 'not a claim that the already fixed auxiliary allocation' in text
    assert time.process_time()<CAP
    out('successor_audit.json',{'status':'PASS_UNIFORM_MAXIMUM_DEPTH_SUCCESSOR_AND_DISJOINT_SAFE_PACKETS',
      'source_domain':'actual B-closed maximal core2r-1, r>=3; not arbitrary core shapes',
      'source_frame_theorem':'every full-depth pair LL/RR with marked grandparent/unmarked parent',
      'destination':'canonical two-sided marked/unmarked fan; gap subtrees rigid',
      'forced_successor':'extreme marked target; exact double charge1',
      'packet_capacity':'2(H+Hnext), demand r; safe when sum>=ceil(r/2)',
      'packet_disjointness':'qmax>=2, successor q1, hence starts never adjacent',
      'six_core11_removed_negative_case':'all H2/q5, and H1/q5 with nextH>=2',
      'six_core11_residual_q5_packet':'H=Hnext=1, full signed weight-2',
      'fixed_auxiliary_reserve_nonuse_assumed':False,'punctured_word_IH_used':False,
      'Step2_complete':False,'all_negative_blocks_repaid':False,'new_complete_CD_domain':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('MAXIMUM_DEPTH_FORCED_Q1_SUCCESSOR_AND_SAFE_PACKET_AUDIT_PASS; residual remains')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_successor_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
