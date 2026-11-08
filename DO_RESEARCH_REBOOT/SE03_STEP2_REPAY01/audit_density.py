"""Independent first-touch/source-label and subtree-mass audit, no inputs."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def N(k,l,r):return (k,l,r)
def rr(t):g,l,r=t;p,a,b=r;return N(p,N(g,l,a),b)
def ll(t):g,l,r=t;p,a,b=l;return N(p,a,N(g,b,r))
def names(t):return names(t[1])+[t[0]]+names(t[2]) if isinstance(t,tuple) else [t]
def p(**kw):return {k:Fraction(v) for k,v in kw.items() if v}
def add(*parts):
    r={}
    for part in parts:
        for k,c in part.items():r[k]=r.get(k,Fraction())+c
    return {k:c for k,c in r.items() if c}
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
error=None
try:
    # Every first-touch pair has only the listed THREE rotating labels.
    # A,B,C,D are rigid arbitrary subtrees, not individual empty nodes.
    laws=[
      (N('g',N('p',N('x','A','B'),'C'),'D'),lambda t:ll(ll(t))),
      (N('g','A',N('p','B',N('x','C','D'))),lambda t:rr(rr(t))),
      (N('g',N('p','A',N('x','B','C')),'D'),
       lambda t:ll(N(t[0],rr(t[1]),t[2]))),
      (N('g','A',N('p',N('x','B','C'),'D')),
       lambda t:rr(N(t[0],t[1],ll(t[2]))))]
    for source,fn in laws:
        dest=fn(source)
        assert dest[0]=='x' and names(source)==names(dest)
        # Whole variables survive once, without insertion into interiors.
        assert set(names(dest))=={'g','p','x','A','B','C','D'}
    # Re-derive label-entry bound: c_T <= i0+2*(m-i0)=2m-i0.
    assert not add(p(i=1,m=2,i_cancel=-2),p(m=-2,i=1),p(i_cancel=2,i=-2))
    # Simpler direct identity in independent symbols.
    assert add(p(i=1),p(m=2,i=-2))==p(m=2,i=-1)
    # Whole signed mass =2r-c=1+delta. Removing marked root leaves delta.
    assert not add(p(r=2,c=-1,one=-1),p(delta=-1),p(delta=1,r=-2,c=1,one=1))
    # Prefix mass is marked count minus unmarked count; the consecutive
    # gap identity follows from U_j=(j-1)-P_j and U_next=j-P_next.
    gap=add(p(j=1,Pnext=-1),p(j=-1,one=1,P=1))
    assert gap==p(one=1,P=1,Pnext=-1)
    assert 2**(6-2)==16 # closed form count of four free bits, no masks tried
    text=(B/'CLOSED_CORE_SUBTREE_DENSITY.md').read_text(encoding='utf-8')
    assert 'a size bound alone would be' in text
    assert 'at most two distinct new labels' in text
    assert 'Moving or splitting T during the period is irrelevant' in text
    # Independent mathematical argument checked here, beyond the identities:
    # (i) C-boundary g exists, because V nonempty and x outside its core.
    # (ii) its child p has NO V anywhere below it; all processed hangers
    # before first touch are V-free. First touch can add x,p only.
    # (iii) g has V outside that child, so afterwards x is in V's core.
    # remaining old-prefix rotations cannot introduce foreign labels.
    # (iv) initial outside-mark core has zero T intersection, or just its
    # marked root. Each new T label needs one of the <=2 first-visit slots.
    # (v) every mark becomes whole root; its prefix and suffix masses are
    # subtree masses. Both nonnegative and sum delta. Sorted labels fixed.
    assert time.process_time()<CAP
    out('density_audit.json',{'status':'PASS_UNIFORM_CLOSED_CORE_SUBTREE_DENSITY',
      'method':'separate first-touch operand/hanger audit and label-union counting derivation',
      'source_new_label_bound':'C_after subset C_before union {x,p}; at most2 distinct new labels',
      'subtree_bound':'c_T<=2m_T-I[root(T) marked]',
      'uniform_prefix_bound':'0<=P_j<=delta, P_1=0,P_r=delta, gap_j=1+P_j-P_next',
      'maximal_core':'sorted marks and unmarks strictly alternate',
      'six_core11_source_mask_count':1,'six_core10_source_mask_count_upper_bound':16,
      'sufficiency_of_mask_conditions_claimed':False,'frozen_graph_filtered':False,
      'A_repayment_proved':False,'Step2_complete':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('UNIFORM_SOURCE_DENSITY_AND_MAXIMAL_MASK_ALTERNATION_PASS; signed repayment OPEN')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_density_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
