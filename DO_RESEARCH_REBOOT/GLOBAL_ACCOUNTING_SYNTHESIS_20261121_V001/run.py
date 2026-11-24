"""Proof-guided global potential pruning and complete original-source audits.

Universal constraints are derived symbolically before finite fitting. Once they
exclude the declared grammar, finite-state/CEGIS fits are cancelled, not promoted.
"""
import gzip
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import sympy as sp
sys.dont_write_bytecode=True
from model import HERE,ROOT,OLD,SRC,NAMES,features,step,H,family,F4,compressed
START=time.process_time();TOTAL=SNAPS=0


def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2),encoding='utf-8')


def symbolic_constraints():
    # All equations have source-uniform physical derivations in the ledger.
    # They are NOT inferred from the finite numerical rows below.
    eqs=[[0]*10 for _ in range(5)]
    eqs[0][2]=1
    eqs[1][9]=1
    eqs[2][3]=1
    eqs[3][0]=eqs[3][1]=1
    eqs[4][0]=1;eqs[4][1]=-1
    M=sp.Matrix(eqs);rref,pivots=M.rref()
    assert pivots==(0,1,2,3,9)
    # Remaining Mersenne coefficient mu must satisfy both whole-source
    # parametric limits. C is unrestricted finite and disappears in the limits.
    a1=[0]*11;a1[8]=2
    a2=[0]*11;a2[8]=-1
    ae=[row+[0] for row in eqs]
    lp=linprog(np.zeros(11),A_ub=np.array([a1,a2],float),b_ub=np.array([-1,-1],float),
               A_eq=np.array(ae,float),b_eq=np.zeros(5),bounds=[(None,None)]*10+[(0,None)],
               method='highs',options={'time_limit':45})
    assert lp.status==2
    combined=[Fraction(a1[i])+2*Fraction(a2[i]) for i in range(11)]
    rhs=Fraction(-1)+2*Fraction(-1)
    assert combined==[0]*11 and rhs==-3
    q,t=sp.symbols('q t',positive=True)
    even_delta=sp.Rational(10,3)*(t-1)-(2*q+1)*t+3
    odd_delta=sp.Rational(5,3)*t-sp.Rational(10,3)+(4*q-1)*t-(2*q+1)*t+2
    assert sp.expand(-even_delta-((6*q-7)*t+1)/3)==0
    assert sp.expand(-odd_delta-((1-6*q)*t+4)/3)==0
    out={'status':'REFUTED—EXACT, declared whole-operation linear potential grammar only',
         'variables':NAMES+['C'],'mandatory_equations':eqs,'rref':[[str(z) for z in row] for row in rref.tolist()],
         'eliminated_feature_indices':list(pivots),'remaining_indices':[4,5,6,7,8],
         'necessary_limit_inequalities':[{'lhs':a1,'rhs':-1,'source':'H_(p,5) first KEEP3, p->infinity after the parity constraint'},{'lhs':a2,'rhs':-1,'source':'compressed H_(3,q) final critical KEEP, q->infinity'}],
         'exact_Farkas_multipliers':['1','2'],'combined_lhs':[str(z) for z in combined],'combined_rhs':str(rhs),
         'contradiction':'0 <= -3','floating_solver_status':int(lp.status),
         'floating_solver_role':'Search cross-check only; exact rational row sum is the infeasibility certificate.',
         'pruned_grammars':['cross_core','ancestry_linear','extended'],
         'cancelled_jobs':['finite-state graph fitting through support6','free state-potential teachers','up to16 finite CEGIS fits per grammar'],
         'cancellation_reason':'The source-uniform necessary constraints already exclude the complete declared span. Finite fits cannot rescue it.',
         'universal_CD':'OPEN','all_other_global_accounting_architectures':'Not refuted.'}
    write('SYMBOLIC_SYNTHESIS_CERTIFICATE.json',out)
    return out


def splay(tree,x,actor,op,save):
    global TOTAL
    path=tree.path(x);depth=len(path)-1;records=[];j=0
    while tree.parent[x] is not None:
        j+=1;p=tree.parent[x];g=tree.parent[p]
        pivots=[x] if g is None else [p,x] if (p<g)==(x<p) else [x,x]
        typ='ZIG' if g is None else ('L' if p<g else 'R')+('L' if x<p else 'R')
        for bit,u in enumerate(pivots):
            oldparent=tree.parent[u];oldspan=[tree.lo[u],tree.hi[u]]
            tree.rotate(u);TOTAL+=1
            if save:records.append({'id':[actor,op,j,bit],'type':typ,'promoted':u,'demoted':oldparent,'old_child_span':oldspan,'new_demoted_span':[tree.lo[oldparent],tree.hi[oldparent]]})
            assert TOTAL<=3000000 and time.process_time()-START<=360
    return depth,records


def audit(source,selected,label,expect=None):
    global SNAPS,TOTAL
    cached=HERE/(label+'.json.gz')
    if cached.exists():
        with gzip.open(cached,'rt',encoding='utf-8') as file:previous=json.load(file)
        assert previous['source']==source
        assert {z['op'] for z in previous['rows']}==selected
        if expect is not None:expect(previous['rows'])
        result=previous['result'];TOTAL+=result['period_real_rotations'];SNAPS+=2*len(previous['rows'])
        assert TOTAL<=3000000
        print(json.dumps({'resumed_complete_witness':label}),flush=True)
        return result
    keys=sorted(map(int,source['initial_A']['children']))
    trees={a:OLD.Tree(source['initial_'+a],keys) for a in ('A','B')}
    diagonal=source.get('diagonal')
    if diagonal is None:
        assert source['initial_A']==source['initial_B'] and not source.get('prefix')
        diagonal=source['initial_A']
    reaching={a:OLD.Tree(diagonal,keys) for a in ('A','B')}
    for mode,x in source.get('prefix',[]):
        OLD.plain(reaching['A'],x)
        if mode=='K':OLD.plain(reaching['B'],x)
    assert all(reaching[a].state()==source['initial_'+a] for a in ('A','B'))
    rows=[];A=Q=0;rotation_start=TOTAL
    for op,(mode,x) in enumerate(source['operations'],1):
        take=op in selected
        if take:f=features(trees['A'],trees['B']);SNAPS+=1
        da,ea=splay(trees['A'],x,'A',op,take)
        if mode=='K':db,eb=splay(trees['B'],x,'B',op,take)
        else:db=0;eb=[]
        A+=(da+1)//2;Q+=db//2
        if take:
            f2=features(trees['A'],trees['B']);SNAPS+=1
            rows.append({'op':op,'mode':mode,'target':x,'a':(da+1)//2,'q_B':db//2,'before':f,'after':f2,'delta':[v-u for u,v in zip(f,f2)],'bits':ea+eb})
    assert all(trees[a].state()==source['initial_'+a] for a in ('A','B'))
    if source.get('expected_A') is not None:assert A==source['expected_A']
    if source.get('expected_Q') is not None:assert Q==source['expected_Q']
    if expect is not None:expect(rows)
    result={'name':source['name'],'label':label,'N':len(keys),'length':len(source['operations']),'A':A,'Q_B':Q,'period_real_rotations':TOTAL-rotation_start,'selected_operation_count':len(rows),'complete_pair_closure':True,'reaching_prefix_checked':True}
    full={'source':source,'result':result,'rows':rows}
    with gzip.open(HERE/(label+'.json.gz'),'wt',encoding='utf-8') as file:json.dump(full,file,separators=(',',':'))
    print(json.dumps(result),flush=True)
    return result


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    certificate=symbolic_constraints();results=[];validation=[]
    for power in (2,5):
        h=2**power
        for name in ('F1','F2','F3'):
            s=family(power,name)
            d={'F1':[-1,-1,-h,0,-1,-1,-1,-1,0,-1],
               'F2':[1,1,-h,0,1,1,1,1,0,h+1],
               'F3':[0,0,-h,-h,0,0,0,0,0,0]}[name]
            def check(rows,d=d):
                assert rows[0]['delta']==d and rows[1]['delta']==[-x for x in d]
                assert all(z['a']==1 and z['q_B']==0 for z in rows)
            results.append(audit(s,{1,2},s['name'],check))
        s=F4(power);k=s['k'];d=[k-1,k-1,-1,0,1,1,1,1,0,k]
        def check4(rows,d=d):
            assert rows[0]['delta']==d and rows[1]['delta']==[-x for x in d]
            assert all(z['a']==1 and z['q_B']==0 for z in rows)
        results.append(audit(s,{1,2},s['name'],check4))
    params=[(p,5) for p in range(1,11)]+[(3,q) for q in (1,17,65)]
    for p,q in params:
        s=H(p,q);n=len(s['initial_A']['children']);restore=2*n+2
        selected={n,n-1+2**p,restore}
        def checkH(rows,p=p,q=q,n=n,restore=restore):
            r=next(z for z in rows if z['op']==restore);t=2**p
            expected=((6*q-7)*t+1)//3 if p%2==0 else ((1-6*q)*t+4)//3
            assert r['delta'][0]-r['delta'][1]==expected
            assert r['a']==1 and r['q_B']==(p+3)//2 and r['delta'][4:6]==[0,0]
            assert r['delta'][6]==(-2 if p%2==0 else -1) and r['delta'][7]==0
            # The frozen Mersenne restoration theorem is H_(p,5), not all q.
            if q==5:assert r['delta'][8]==p
            initial=next(z for z in rows if z['op']==n);m=(n-1)//2
            assert initial['a']==0 and initial['q_B']==m and initial['delta'][0]==-m*(m+2)
            validation.append({'family':'H','p':p,'q':q,'restoration_skew':expected,'raw_energy_first_B_drop':m*(m+2),'raw_global_credit_over_A_lower':str(Fraction(n+3,16))})
        results.append(audit(s,selected,s['name'],checkH))
    for q in (1,5,17):
        s=compressed(q);n=len(s['initial_A']['children']);target=n+3
        def checkC(rows,q=q):
            r=rows[0]
            assert r['a']==2 and r['q_B']==q+1 and r['delta'][4:6]==[0,0]
            assert abs(r['delta'][6])<=18 and abs(r['delta'][7])<=26 and abs(r['delta'][8]+q)<=16
            validation.append({'family':'compressed','q':q,'delta':r['delta']})
        results.append(audit(s,{target},s['name'],checkC))
    assert len(results)==24
    # Genuine interleaved/private controls are validation of the new state
    # quantities, not acceptance evidence for a disproved universal grammar.
    refs=SRC.references()
    wanted=['W_2_1','W_star','G_4_1_L31_r4_z1','nested_DH_d5_tail63_helpers1',
            'sparseH_p5_hits5-3-7_holeNone','J_p3_q1_d1_m2_altered_restore',
            'I_p1_q1_d2_m2_mirror_helpers','H3_rho2_Y1_copies2','H5_rho4_Y1_copies2']
    chosen=[r for r in refs if r['name'] in wanted]
    assert len(chosen)==len(wanted),(len(chosen),[r['name'] for r in chosen])
    for i,ref in enumerate(chosen):
        s=SRC.canonical(ref);m=len(s['operations']);selected={1,m}
        selected.update(1+j*(m-1)//15 for j in range(16))
        if ref['kind']=='sealed':
            raw=SRC.read(ROOT/ref['path'])
            selected.update(z['op'] for z in raw.get('result',{}).get('probe_certificates',[]))
        result=audit(s,selected,f'control_{i:02d}');result['source_ref']=ref;results.append(result)
    write('UNBOUNDED_FAMILY_FORMULA_CHECKS.json',validation)
    write('AUDIT_RESULTS.json',{'cases':results,'source_count':len(results),'parameterized_sources':24,'historical_controls':len(chosen),
                              'period_real_rotations':TOTAL,'feature_snapshots':SNAPS,'resume_attempt_cpu_seconds':time.process_time()-START,
                              'first_attempt_cpu_seconds':'Not retained after its q=1 validation assertion; bounded by its enforced 360-second limit.',
                              'status':'Formula validation only; universality comes from symbolic source derivations.'})
    write('PROOF_SEARCH_LEDGER.json',{'root':'Universal finite-C Coarse Double','root_status':'OPEN',
          'chosen_architecture':'Whole-operation fixed linear full-pair potential in ten declared features',
          'chosen_grammar_status':'REFUTED—EXACT for every finite C and fixed finite signed coefficients',
          'hard_constraint_sequence':['tail F1 eliminates depthA','tail F2 eliminates weighted defect','diagonal F3 eliminates depthB','A root-walk F4 makes cross coefficients opposite','restoration parity eliminates remaining cross coefficient','restoration p requires mu<=-1/2','compressed burst q requires mu>=1'],
          'exact_terminal_certificate':'0 <= -3','general_potentials':'OPEN; outside declared span not refuted',
          'cancelled_finite_fits':certificate['cancelled_jobs'],'no_new_universal_payment':True})
    print(json.dumps({'sources':len(results),'rotations':TOTAL,'snapshots':SNAPS,'cpu_seconds':time.process_time()-START,'root':'OPEN','declared_grammar':'REFUTED—EXACT'}),flush=True)


if __name__=='__main__':main()
