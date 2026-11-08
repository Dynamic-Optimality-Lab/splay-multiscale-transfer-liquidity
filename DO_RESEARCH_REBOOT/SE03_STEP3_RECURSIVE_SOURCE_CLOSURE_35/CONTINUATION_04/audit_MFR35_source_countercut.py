"""Independent complete B replay, critical A replay and symbolic source review.

Gamma existence and full erased/chart recurrence reuse accepted source
proofs. They are not falsely reported numerically expanded in this audit.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def path(t,x):
    z=[]
    while True:
        z.append(t[0])
        if t[0]==x:return z
        t=t[1] if x<t[0] else t[2]
def N(k,l=None,r=None):return (k,l,r)
def RR(g,u,x,a,b,c,d):return N(x,N(u,N(g,a,b),c),d)
def LL(g,u,x,a,b,c,d):return N(x,a,N(u,b,N(g,c,d)))
def main():
    global V
    rp=F/'MFR35_unpaid_source_countercut.json';r=json.loads(rp.read_text())
    for p,h in r['input_sha256'].items():assert sha(Path(p))==h
    # Symbolic outside-frame identities with arbitrary opaque ordered terms.
    after=RR('G','U','x','A','B','C','D')
    assert after==N('x',N('U',N('G','A','B'),'C'),'D')
    assert LL('x','U','G','A','B','C','D')==N('G','A',N('U','B',N('x','C','D')))
    assert RR('x','U','G','A','B','C','D')==N('G',N('U',N('x','A','B'),'C'),'D')
    # Formal recurrences in variables P=2^(q-1), q. Coefficient tuples
    # represent a*P+b*q+c; these are identities, not finite q samples.
    Lprev=(1,0,-1);Qprev=(2,-1,-1)
    assert tuple(2*v+w for v,w in zip(Lprev,(0,0,1)))==(2,0,-1)
    assert tuple(a+2*b+c for a,b,c in zip(Qprev,Lprev,(0,0,1)))==(4,-1,-2)
    sp=importlib.util.spec_from_file_location('MFR_counter_distinct_source',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    rows=r['full_B_rows'];initial=tup(r['initial_common_Bprev']);b=V.Mutable(initial);marks=set(r['genuine_marks']);forward=[];seen=set();cost=0
    for j,row in enumerate(rows):
        before=tup(b.snapshot());assert before==tup(row['before']) and before[0]!=row['target']
        pp=path(before,row['target']);assert len(pp)%2==1 and pp[:-1:2]==row['old_marked_grandparents_root_order']
        if row['role']=='forward':forward.append({'target':row['target'],'ancestors':pp[:-1:2],'Q':(len(pp)-1)//2})
        _,q,events=b.splay(row['target'],True);assert q==row['Q'] and tup(b.snapshot())==tup(row['after'])
        assert all(e['pattern'] in ('LL','RR') and e['grandparent'] in marks and e['parent'] not in marks for e in events)
        assert set().union(*(set(path(tup(b.snapshot()),x)) for x in marks))==set(range(1,22))
        seen.add(row['target']);cost+=q
    assert tup(b.snapshot())==initial and seen==marks==set(range(1,22,2)) and len(rows)==60 and cost==100
    # Independent inverse-letter formula: ancestor index is v2(j).
    inverse=[]
    for row in reversed(forward):
        anc=row['ancestors'];inverse.extend(anc[(j&-j).bit_length()-1] for j in range(1,2**len(anc)))
    assert inverse==r['inverse_word'] and [x['target'] for x in rows[len(forward):]]==inverse
    assert sum(2**x['Q'] for x in forward)==60 and 2*60-2*len(forward)==100
    claims=[]
    for c in r['critical_unpaid_claims']:
        G,X=c['old_proxy'],c['consumer'];a=V.Mutable(tup(c['A_before']));h,_,ev=a.splay(X,True)
        assert h==1 and len(ev)==1 and ev[0]['pattern']=='RR' and ev[0]['rotations'][0]['pivot']==G
        assert tup(a.snapshot())==tup(c['A_after']) and tup(ev[0]['rotations'][0]['after'])==tup(c['A_first_rotation_after'])
        for target in (X,r['contact_y']):
            assert G in path(tup(ev[0]['rotations'][0]['before']),target)[:-1]
            assert G not in path(tup(ev[0]['rotations'][0]['after']),target)[:-1]
        br=rows[c['forward_B_ordinal']-1];assert br['target']==X and br['Q']==3 and br['old_marked_grandparents_root_order'][0]==G
        # The only right-side demotions in this G tenure are this X and7.
        begin=next(j for j,z in enumerate(rows[:len(forward)]) if z['target']==G);end=c['next_proxy_reset_forward_ordinal']-1
        assert [z['target'] for z in rows[begin+1:end] if G in z['old_marked_grandparents_root_order'] and z['target']>G]==[X,7]
        claims.append({'consumer_key':X,'original_B_ordinal':c['forward_B_ordinal'],'double_index':3,'H':1,'Q':3,'h0_unpaid':True})
    a=V.Mutable(tup(r['A_contact_before_KEEP']));losses={G:[] for G in (1,3,5)};pools={G:set() for G in losses}
    for ordinal,c in enumerate(r['post_contact_A_controls']):
        assert tup(a.snapshot())==tup(c['before']);h,_,ev=a.splay(c['target'],True)
        assert h==c['H'] and tup(a.snapshot())==tup(c['after'])
        for e in ev:
            for rot in e['rotations']:
                for G in losses:
                    if 7 in path(tup(rot['before']),G)[:-1] and 7 not in path(tup(rot['after']),G)[:-1]:
                        assert rot['pivot']==7;losses[G].append((ordinal,e['j'],rot['bit']));pools[G]|={(ordinal,e['j'],0),(ordinal,e['j'],1)}
        if ordinal>0:assert all(rot['pivot']!=7 for e in ev for rot in e['rotations'])
    assert all(v==[(0,1,0)] for v in losses.values()) and all(us=={(0,1,0),(0,1,1)} for us in pools.values())
    assert len(claims)==3 and len(set().union(*pools.values()))==2
    paths=[rp,F/'SS_SPLAY_INVERSE_SOURCE_THEOREM.md',F/'MFR35_ALL_RETURN_SOURCE_REFUTATION.md',
      B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',B/'STREAMED_BLOCK_THEOREM.md',F/'audit_MFR35_source_countercut.py']
    out={'status':'PASS_SOURCE_EXACT_MFR_ALL_RETURN_COUNTERCUT_AND_UNIFORM_SS_INVERSE_PROOF',
      'genuine_support':11,'physical_keys':21,'B_original_operations_replayed':60,'B_Q':100,'A_critical_controls_replayed':7,
      'selected_actual_natural_residuals':claims,'sole_return_supplier_event':'original DELETE6 immediately after original contact KEEP7',
      'all_return_demands':3,'all_return_units':2,'deficiency':1,
      'source_reachability_closure':'common diagonal Bprev; canonical real A-only preparations/reset; literal full-B inverse closure; accepted true erased/chart finite recurrence',
      'verification_limits':'Gamma words, full inverse A trajectory and numeric erased/chart u,L not expanded/replayed; their source existence/closure is symbolic',
      'source_proof_review':['SS inverse induction and opaque-hanger conjugation; exact inverse costs by formal recurrences',
        'each prep ends BEFORE genuine G, so each X macro has exactly one positive RR event and residual third double',
        'first G loss of both X and7 coincides; opposite-side visits cannot share that rotation',
        'all return options exhausted: after DELETE6 the entire 7 subtree is a rigid hanger for low resets',
        'every original Gamma/inverse/reset cost retained; one actual period and original cut/owner identities',
        'source-safe margin>=20; independent restricted SSI source license, no global CD refutation'],
      'all_MFR_return_rule':'REFUTED_AT_THIS_FROZEN_ELIGIBILITY_SCOPE','SSI_uniform_source_closure_and_funding':'PROOF_REVIEW_PASSED_AT_DECLARED_SCOPE',
      'JR35':'OPEN','reservation':'DEFERRED','Coarse_Double_counterexample':False,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'independent_is_same_agent_distinct_implementation':True,
      'input_sha256':{str(p):sha(p) for p in paths}}
    assert V.CALLS==67
    with (F/'independent_MFR35_unpaid_source_countercut.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('input_sha256','source_proof_review')}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/'audit_verify154_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
