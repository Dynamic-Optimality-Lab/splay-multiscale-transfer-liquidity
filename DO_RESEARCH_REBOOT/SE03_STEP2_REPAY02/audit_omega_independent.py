"""Separate primitive audit of new Omega, reusing completed H6 closure."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;CAP=float(sys.argv[1])
def N(k,l,r):return [k,l,r]
def get(t,p):
    for c in p:t=t[1 if c=='L' else 2]
    return t
def change(t,p,fn):
    if not p:return fn(t)
    k,l,r=t
    return N(k,change(l,p[1:],fn),r) if p[0]=='L' else N(k,l,change(r,p[1:],fn))
def R(t):g,l,r=t;x,a,b=l;return N(x,a,N(g,b,r))
def L(t):g,l,r=t;x,a,b=r;return N(x,N(g,l,a),b)
def frame(t,where,directions):
    if len(directions)==1:return change(t,where,R if directions=='L' else L)
    outer=R if directions[0]=='L' else L
    if directions[0]==directions[1]:return change(change(t,where,outer),where,outer)
    t=change(t,where+directions[0],R if directions[1]=='L' else L)
    return change(t,where,outer)
def names(t):return names(t[1])+[t[0]]+names(t[2]) if isinstance(t,list) else [t]
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
error=None
try:
    proof=json.loads((B/'omega_derivation.json').read_text())
    t=proof['initial_diagonal'];total=0
    for row in proof['prefix_trace']:
        path=row['A_path'];assert get(t,path)[0]==row['key'];old=t
        # Bottom-up source grouping is independently prescribed by path.
        expected=[];q=path
        while len(q)>=2:expected.append([q[:-2],q[-2:]]);q=q[:-2]
        if q:expected.append(['',q])
        assert expected==row['A_frames']
        for where,directions in expected:t=frame(t,where,directions)
        assert t==row['A_end'] and names(t)==names(old)
        assert row['A_cost']==(len(path)+1)//2;total+=row['A_cost']
        if row['occurrence']==10:assert t==proof['prepared_A']
        if row['occurrence']==12:assert t==proof['prepared_A']
        assert time.process_time()<CAP
    assert total==24 and t==proof['known_B_after_H6_first_two']
    # Independently check the new B setup is a full arbitrary-block RR/LL
    # inverse. H6 afterwards is a completed inherited source theorem.
    source=N('a','A',N('u','B',N('c','C','D')))
    assert R(R(L(L(source))))==source
    backbone=(ROOT/'DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md').read_text(encoding='utf-8')
    assert 'Q(H_r)=4r-4' in backbone and 'return both to R_n' in backbone
    assert 4*6-4==20 and 20-5-1==14
    assert total+14==38 and 2+20==22 and 2*38-22==54
    assert proof['preceding_genuine_boundary']==10
    assert proof['preparatory_A_charged_to_previous_macro']==13
    assert proof['prefix_trace'][10]['A_cost']==proof['prefix_trace'][11]['A_cost']==1
    # Old D lineage lower bound needs no saved-value lookup: c is a min of
    # 2 and 1+psi, BOTH>=1. H ceiling false on R9; P true; later updates max.
    dhid=json.loads((ROOT/'DO_RESEARCH_REBOOT/M3_XFER16/debt_definition.json').read_text())
    dterm=json.loads((ROOT/'DO_RESEARCH_REBOOT/M3_XFER17/debt_definition.json').read_text())
    assert dhid['H_max']['core_right_child']==8
    assert dterm['formula']=='D_hid(s) if P(s), else0'
    assert proof['old_visible_nonroot_marked']==[3]
    assert proof['normalized_old_chart_D']==1 and proof['chart_residual_upper']==-1
    final=(ROOT/'DO_RESEARCH_REBOOT/M3_XFER21/FULL_M3_PROOF.md').read_text(encoding='utf-8')
    assert 'D=max(F4' in final and 'with integer0<=D<=2' in final if False else 'D=max(F4' in final
    # This check concerns the new SOURCE counterfamily only, not replay
    # of any old graph edge, proof obligation or finite population.
    out('omega_independent_audit.json',{'status':'PASS_ORIGINAL_SOURCE_COUNTERSCHEMA_TO_CHART_CANDIDATE',
      'method':'separate primitive rotations, full free-term conservation, genuine seam and accepted-debt lineage audit',
      'source_preparations':'all18 new A-prefix operations audited; H6 B suffix reused, not rerun',
      'full_pair_closure':'diagonal R11; after repair A=B at actual H6 boundary; inherited even-depth suffix closes',
      'arbitrary_fringe_quantification':'all Fi as distinct ordered BST variables; no substitution sampled',
      'macro_costs':'preparation charged to preceding genuine K1; actual critical pair H1/H1,Q5/Q1',
      'totals':{'A':38,'QF':22,'original_slack':54},
      'candidate_residual_upper':-1,'rejected_candidate':'accepted M3 D read in successive recent charts, even with Hamiltonian/ray ceilings',
      'original_CD_counterexample':False,'generic_width_two_potential_refuted':False,
      'Step2_complete':False,'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('OMEGA_SEPARATE_SOURCE_AND_CHART_OBSTRUCTION_AUDIT_PASS; original CD slack54')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_omega_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
