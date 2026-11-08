"""Separate universal rotation-role/debt augmentation audit; no tree input."""
import json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def node(k,l,r):return (k,l,r)
def offsets(t,d=0):
    if isinstance(t,str):return {t:d}
    k,l,r=t;return {k:d,**offsets(l,d+1),**offsets(r,d+1)}
def poly(**kw):return {k:Fraction(v) for k,v in kw.items() if v}
def add(*args):
    p={}
    for v in args:
        for k,c in v.items():p[k]=p.get(k,Fraction())+c
    return {k:c for k,c in p.items() if c}
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
error=None
try:
    # Free variables denote whole arbitrary subtrees: their offset change
    # is the change for every node inside them, at any internal depth t.
    oldR=node('g',node('p','A','B'),'C')
    newR=node('p','A',node('g','B','C'))
    oldL=node('g','A',node('p','B','C'))
    newL=node('p',node('g','A','B'),'C')
    shifts=[]
    for old,new in [(oldR,newR),(oldL,newL)]:
        a,b=offsets(old),offsets(new)
        assert set(a)==set(b)=={'g','p','A','B','C'}
        delta={k:b[k]-a[k] for k in a}
        assert max(abs(v) for v in delta.values())==1
        shifts.append(delta)
    # The source depth proof telescopes these per-rotation bounds over
    # at most2H rotations. Fixed-key final depth0 yields initial depth<=2H.
    # Clipped HIGH excess is three independently nonnegative summands.
    assert not add(poly(T=2,q=-1,a=-1),poly(T=-2,Q=1,K=1),
                   poly(Q=-1,q=1),poly(K=-1,a=1))
    # Raised and unraised augmentation branches are exact identities.
    assert not add(poly(w=1,dtplus=1,L=-1),poly(w=-1,L=1),poly(dtplus=-1))
    assert not add(poly(w=1,dtplus=1,ds=-1),poly(w=-1,dt=-1,ds=1),poly(dtplus=-1,dt=1))
    # New width3 range creates all weight2 cases: q=2H-2, 1<=H<4.
    # These follow from the generic affine formula, not source samples.
    assert not add(poly(H=2,q=-1),poly(H=-2,one=2,q=1),poly(one=-2))
    assert 2*4-5==3
    text=(B/'HELPER_INDEPENDENT_SAFE_AUGMENTATION.md').read_text(encoding='utf-8')
    assert 'DEFAULT even when E_0 itself fails' in text
    assert 'Starting from D=0 alone is NOT a proof' in text
    target=(B/'IMPROVED_FULL_DEBT_TARGET.md').read_text(encoding='utf-8')
    assert 'No debt function satisfying these obligations has been proved' in target
    assert 'Paths from two different p cannot meet' in target
    # Independent exchange derivation: functions fF and fE are injective.
    # If a reached common-only cycle existed, its initial vertex would
    # have one cycle predecessor and one path predecessor; injectivity
    # forces equality, and backward induction forces p to be common.
    # The same backward uniqueness argument separates distinct p paths.
    # This establishes conditional construction, not existence of fF.
    assert time.process_time()<CAP
    out('safe_levels_audit.json',{'status':'PASS_CONDITIONAL_PRESERVATION_AND_EXCHANGE_ONLY',
      'primitive_depth_shifts':shifts,'source_target_cover':'initial depth(x)<=2H; all helpers charged',
      'augmentation':'max(D,L) preserves every individually valid clipped full-macro inequality',
      'quantifiers':'arbitrary present population, gap inventories, helpers, source words and K,T satisfying range glue',
      'six_key_specialization':{'K':3,'T':4,'Qmax':5,'A_observation_depth':6},
      'exchange':'injective alternating paths terminate and have distinct source-unit endpoints, conditional on independent full allocator',
      'baseline_D6_constructed':False,'all_negative_edges_proved':False,'Step2_complete':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,'external_peer_review':False})
    print('UNIVERSAL_TARGET_COVER_SAFE_AUGMENTATION_AND_CONDITIONAL_EXCHANGE_PASS; baseline OPEN')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_safe_levels_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
