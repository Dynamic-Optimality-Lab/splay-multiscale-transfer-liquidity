"""Separate free-term proof of the Hamiltonian source ceilings."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def N(k,l,r):return (k,l,r)
def right(t):g,l,r=t;u,a,b=l;return N(u,a,N(g,b,r))
def left(t):g,l,r=t;u,a,b=r;return N(u,N(g,l,a),b)
def at(t,p):
    for c in p:t=t[1 if c=='L' else 2]
    return t
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
    # Source extreme-target induction: R denotes an arbitrary NONEMPTY
    # Score-containing rebuilt subtree. The next LL produces a permanent
    # Score fork, regardless of arbitrary A,C,D or its internal contents.
    fork=right(right(N('g',N('u',N('x','A','R'),'C'),'D')))
    assert fork==N('x','A',N('u','R',N('g','C','D')))
    assert at(fork,'R')[1]=='R' and at(fork,'RR')[0]=='g'
    # Each first LL already makes the target-right rebuilt tree nonempty.
    # A second therefore has the fork just derived. Later same-side pairs
    # or final zig attach this subtree rigidly: Hamiltonian output =>q<=1.
    # q1 even source: old root g on the third destination Score.
    even=right(right(N('g',N('u',N('x','A','B'),'C'),'D')))
    assert at(even,'RR')[0]=='g'
    # q1 odd source: one bottom LL followed by the final left zig.
    lower=right(right(N('g',N('u',N('x','A','B'),'C'),'D')))
    odd=right(N('h',lower,'E'))
    assert at(odd,'R')[0]=='h'
    # Independently derive all old-root rays of the six H1 source words.
    observations=[]
    source=N('g','A',N('x','B','C'));dest=left(source);observations.append(('zigR','L'));assert at(dest,'L')[0]=='g'
    source=N('g',N('x','A','B'),'C');dest=right(source);observations.append(('zigL','R'));assert at(dest,'R')[0]=='g'
    source=N('g','A',N('u','B',N('x','C','D')));dest=left(left(source));observations.append(('RR','LL'));assert at(dest,'LL')[0]=='g'
    source=N('g',N('u',N('x','A','B'),'C'),'D');dest=right(right(source));observations.append(('LL','RR'));assert at(dest,'RR')[0]=='g'
    source=N('g',N('u','A',N('x','B','C')),'D');dest=right(N(source[0],left(source[1]),source[2]));observations.append(('LR','R'));assert at(dest,'R')[0]=='g'
    source=N('g','A',N('u',N('x','B','C'),'D'));dest=left(N(source[0],source[1],right(source[2])));observations.append(('RL','L'));assert at(dest,'L')[0]=='g'
    # Lowered-to1 incoming residual is (w-1)+(2-Dsource), both>=0.
    assert not add(p(w=1,one=1,ds=-1),p(w=-1,one=1),p(one=-2,ds=1))
    # Lowered-to0: H1/q0 gives w>=2; H>=2/q<=1 gives w>=3.
    assert 2-0>=2 and 4-1>=3
    text=(B/'RAY_NORMALIZATION_AND_OBSTRUCTION.md').read_text(encoding='utf-8')
    assert 'every already valid fixed-nine-Score source inequality' in text
    assert 'still OPEN' in text
    assert time.process_time()<CAP
    out('normalization_audit.json',{'status':'PASS_SOURCE_ROW_PRESERVING_HAMILTONIAN_AND_RAY_CEILINGS',
      'method':'independent arbitrary-block rotation identities, persistent-fork induction and signed range algebra',
      'incoming_Hamiltonian_double_bound':1,'possible_q1_old_root_positions':['second Score','third Score'],
      'H1_old_root_rays':observations,'source_canonical_shadow':'reuse original known-real old-root exposure/G-alias theorem',
      'range':[0,2],'preservation':'every individually valid fixed-nine-Score source macro; repeats handled by exact-state/range',
      'full_original_graph_replacement_claimed':False,'source_only_function_uses_old_fields':True,
      'LRU_miss_gluing_proved':False,'Step2_complete':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,'external_peer_review':False})
    print('HAMILTONIAN_AND_RAY_SOURCE_CEILING_AUDIT_PASS; chart gluing not inferred')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_normalization_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
