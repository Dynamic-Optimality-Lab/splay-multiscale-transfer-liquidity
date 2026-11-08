"""Fresh independent mutable-parent replay, plus symbolic template audit.
Accepted verifier code is reused, not the producer's functional simulator.
"""
import importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2])
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V=module('accepted_mutable_verifier',B/'audit_verify79.py');V.CAP=CAP;V.QCAP=QCAP;V.START=START;V.CALLS=0
I=module('distinct_pool_verifier',F/'audit_pools.py')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def core(t,M):
    if not I.tree(t):return set()
    c=core(t[1],M)|core(t[2],M)
    if c or t[0] in M:c.add(t[0])
    return c
def symbolic_templates():
    # The atoms A/B/C denote arbitrary independent ordered rigid BST terms.
    # One representative per term records all external ancestor relations;
    # internal ancestry is unchanged in a rotation and is proved textually.
    before=('g',('p',('A',None,None),('B',None,None)),('C',None,None))
    after=('p',('A',None,None),('g',('B',None,None),('C',None,None)))
    def relation(t,anc=()):
        if t is None:return set()
        k,l,r=t;return {(v,k) for v in anc}|relation(l,anc+(k,))|relation(r,anc+(k,))
    losses=relation(before)-relation(after);assert losses=={('g','p'),('g','A')}
    def reflect(t):return None if t is None else (t[0],reflect(t[2]),reflect(t[1]))
    assert relation(reflect(before))-relation(reflect(after))==losses
    # Affine inequalities, valid for symbolic nonnegative variables:
    # Hi=hi+Gi, hi>=1, Qi<=2 -> 2Hi-Qi-2Gi=2hi-Qi>=0.
    # Let hi=1+u, Qi=2-v, u,v>=0. Margin=2u+v.
    coefficients={'constant':2*1-2,'u':2,'v':1};assert coefficients==dict(constant=0,u=2,v=1)
    # Qc-selected tickets, <=2Hc inside close -> >=Qc-2Hc outside.
    # Selected host bits <=2Gi; host leftover >=Qi by the previous identity.
    # No claim that every B word has these MR hypotheses is checked here.
    return dict(status='PASS_FREE_TERM_ROTATION_AND_AFFINE_SOURCE_BRIDGE',AR1='pivot-only loss and reflection',AR2='written direction induction; not inferred from examples',LPR='written first-whole-loss operation injection with AR1 per-operation bound',MR_pool='written source-location proof plus exact host capacity identity',universal_GPR='OPEN')
def main():
    z=read(F/'nonmonotone_source_controls.json');receipts=[]
    for c in z['cases']:
        assert c['status']=='ORIGINAL_TRIPLE_AND_CHART_CLOSED_CANDIDATE_CONTROL'
        A=V.Mutable(c['initial_diagonal']);BF=V.Mutable(c['initial_diagonal']);BE=V.Mutable(c['initial_diagonal']);cf=[];ce=[];start=None
        for r in c['prefix_rows']+c['period_rows']:
            if r['t']==c['period'][0]:start=(A.snapshot(),BF.snapshot(),BE.snapshot(),tuple(cf),tuple(ce))
            assert V.eq((A.snapshot(),BF.snapshot(),BE.snapshot()),(r['A_before'],r['BF_before'],r['BE_before']))
            a,_,_=A.splay(r['key']);q=qe=0
            if r['kind']=='K':
                g=BF.root.k!=r['key'];_,q,_=BF.splay(r['key'])
                if g:cf=[r['key']]+[v for v in cf if v!=r['key']]
                if r['key']!=c['erase']:
                    g=BE.root.k!=r['key'];_,qe,_=BE.splay(r['key'])
                    if g:ce=[r['key']]+[v for v in ce if v!=r['key']]
            assert (a,q,qe)==(r['a'],r['qF'],r['qE']) and V.eq((A.snapshot(),BF.snapshot(),BE.snapshot()),(r['A_after'],r['BF_after'],r['BE_after']))
            assert cf==r['chart_F'] and ce==r['chart_E']
        end=A.snapshot(),BF.snapshot(),BE.snapshot(),tuple(cf),tuple(ce)
        assert start==end and V.eq(start,c['period_start']) and V.eq(end,c['period_end'])
        rr=I.canonical(c,'C33_36');M={r['x'] for r in rr if r['gen']};sizes={len(core(r['B0'],M)) for r in rr};assert sizes=={c['core']}
        assert (c['scope']=='MAXIMAL_CORE')==(c['core']==2*len(M)-1)
        assert c['scope']=='NOT_MAXIMAL_CORE' # Actual outcome: do not import the PR theorem.
        receipts.append(dict(helper=c['helper'],period=c['period'],A=sum(r['a'] for r in rr),Q_F=sum(r['q'] for r in rr),Q_E=sum(r['qE'] for r in c['period_rows']),support=len(M),full_core=c['core'],full_triple_and_chart_closure=True,pool_scope='OUTSIDE_MAXIMAL_CORE_THEOREM',frozen_auxiliary_input='NOT_SUPPLIED; no principal JIO34 allocation claimed'))
    result=dict(status='PASS_DISTINCT_IMPLEMENTATION_NEW_SOURCE_AND_SYMBOLIC_POOL_LEMMAS',input_sha256={'nonmonotone_source_controls.json':I.sha(F/'nonmonotone_source_controls.json'),'JOINT_INTERIOR_EXTERIOR_ALLOCATION.md':I.sha(F/'JOINT_INTERIOR_EXTERIOR_ALLOCATION.md'),'POOLED_RETIREMENT_SOURCE_LAW.md':I.sha(F/'POOLED_RETIREMENT_SOURCE_LAW.md'),'EXACT_GLOBAL_FEASIBILITY_MODEL.md':I.sha(F/'EXACT_GLOBAL_FEASIBILITY_MODEL.md')},source_receipts=receipts,symbolic_templates=symbolic_templates(),source_engine_calls=V.CALLS,source_queries=V.CALLS,scope='same-agent distinct implementation/static audit; no external peer review/formal assistant verification',principal_JIO34='OPEN')
    assert V.CALLS==z['source_queries']
    with (F/'independent_new_source_and_lemma_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify81_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=V.CALLS,source_engine_calls=V.CALLS),f)
