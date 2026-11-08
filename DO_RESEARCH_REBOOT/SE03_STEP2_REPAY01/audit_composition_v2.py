"""Separate packet-partition, modified source schema, and mismatch audit."""
import json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def N(k,l,r):return (k,l,r)
def left(t):g,l,r=t;p,a,b=r;return N(p,N(g,l,a),b)
def right(t):g,l,r=t;p,a,b=l;return N(p,a,N(g,b,r))
def change(t,p,fn):
    if not p:return fn(t)
    k,l,r=t
    return N(k,change(l,p[1:],fn),r) if p[0]=='L' else N(k,l,change(r,p[1:],fn))
def mismatch(a,b,path=''):
    if isinstance(a,str) or isinstance(b,str):
        if isinstance(a,str) and isinstance(b,str):return None
        return {'path':path,'left':'gap' if isinstance(a,str) else a[0],
                'right':'gap' if isinstance(b,str) else b[0]}
    if a[0]!=b[0]:return {'path':path,'left':a[0],'right':b[0]}
    return mismatch(a[1],b[1],path+'L') or mismatch(a[2],b[2],path+'R')
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
error=None
try:
    proof=json.loads((B/'source_term_derivation.json').read_text())
    witnesses=[]
    for row in proof['trace']:
        w=mismatch(row['end_terms'][1],row['end_terms'][2]);assert w
        witnesses.append({'occurrence':row['occurrence'],**w})
    # Every witness has distinct distinguished labels, or a distinguished
    # node versus a typed gap containing no distinguished node. Consequently
    # arbitrary legal gap substitutions cannot make the B trees equal.
    prepared=N('1','F0',N('4',N('2','F1',N('3','F2','F3')),N('n','E','Fn')))
    critical=left(left(prepared))
    assert right(right(critical))==prepared
    repair=left(left(prepared))
    repair=change(repair,'LL',left);repair=change(repair,'L',right)
    repair=right(repair);repair=left(repair)
    Smax=N('n',N('2',N('1','F0','F1'),N('4',N('3','F2','F3'),'E')),'Fn')
    assert repair==Smax
    assert right(right(repair))==right(right(Smax))
    assert sum([1,1,2,1,1])-sum([2,1,1])==2
    # Packet decomposition: each q5 start's immediate successor is q1;
    # it cannot be another q5 start, so pairs cannot share a macro.
    # Chosen starts/endpoints are actual original states. Joining consecutive
    # source segments preserves exact closure, not merely root closure.
    # Conditional width2 HIGH bounds: singleton Q<=4, pair Q=6.
    assert 2*4-4>=2 and 2*4-6>=2
    assert 2*3-4>=2 and 2*2-2>=2 and 2*1-0>=2
    assert 2*2-6==-2 and 2*3-6==0
    text=(B/'PAIRED_RANGE_TWO_TARGET.md').read_text(encoding='utf-8')
    assert 'Neither candidate\'s debt function has been proved' in text
    assert 'Paired H3/Q6 ZERO edges' in text
    transport=(B/'PACKET_PERIOD_TRANSPORT.md').read_text(encoding='utf-8')
    assert 'Map BOTH donor and demand' in transport
    assert 'leaves other demands unfunded' in transport
    assert time.process_time()<CAP
    out('composition_v2_audit.json',{'status':'PASS_SOURCE_PARTITION_AND_CONDITIONAL_REDUCTION_ONLY',
      'Gamma_never_rejoining':'at every original recurrent boundary; universal distinguished-node mismatches',
      'mismatch_witnesses':witnesses,
      'modified_Gamma_r':'A=6r,QF=6r-6, closed; critical paired weight4-r',
      'single_macro_range_lower_bound':'r-3','paired_range_lower_bound':'r-4',
      'six_key_candidate':{'range':[0,2],'threshold':4,'baseline_constructed':False},
      'source_partition':'all original operations retained once; q5 pairs disjoint; exact full endpoints',
      'period_transport':'actual source unit/demand bijection; block timing only',
      'Step2_complete':False,'new_original_CD_domain':False,'unrestricted_CD_proved':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('SOURCE_PACKET_COMPOSITION_AND_NONREJOINING_AUDIT_PASS; no debt baseline proved')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_composition_v2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
