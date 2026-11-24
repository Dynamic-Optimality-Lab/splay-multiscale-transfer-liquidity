"""Bounded CEGIS in frozen nonlinear physical feature grammars; exact row teacher."""
import math
import time
from fractions import Fraction
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from kernel import dump,FEATURE_NAMES


def candidate(theta,C,grammar):
    return {'grammar':grammar,'theta':[str(Fraction(t)) for t in theta],'C':str(Fraction(C)),
            'potential':'Single-valued function of original physical pair; arbitrary fixed signed coefficients.',
            'invariant':'Well-formed same-key BST pair; finite reachable-state teacher is separate from universal structural proof.',
            'contracts':{'initialization':'STRUCTURAL_ROTATION_CERTIFICATE_REQUIRED','A_loop':'AFFINE_COUNTER_AND_ROTATION_PROOF_REQUIRED','B_loop':'AFFINE_COUNTER_AND_ROTATION_PROOF_REQUIRED','whole_operation_cost':'OPEN until a universal symbolic proof is checked','boundary':'Equal physical pair implies equal physical feature potential'},
            'universal_CD':'OPEN'}


def exact_slack(matrix,a,q,program):
    theta=list(map(Fraction,program['theta']));C=Fraction(program['C']);den=math.lcm(C.denominator,*(t.denominator for t in theta));weights=[int(t*den) for t in theta];c=int(C*den)
    limit=max([1,*map(abs,weights),abs(c),den])*max(1,int(abs(matrix).max()),int(a.max()),int(q.max()))*(matrix.shape[1]+2)
    dtype=np.int64 if limit<2**60 else object
    return matrix.astype(dtype)@np.asarray(weights,dtype=dtype)+den*q.astype(dtype)-c*a.astype(dtype),den


def recover_vertex(matrix,a,q,active,float_theta,C):
    """Recover a small exact LP basis, rather than rounding each coefficient."""
    support=[i for i,z in enumerate(float_theta) if abs(z)>1e-8]
    if not support:return [Fraction(0)]*len(float_theta)
    equations=[];rhs=[];rank=0
    residual=matrix[active]@float_theta-C*a[active]+q[active]
    for j in sorted(range(len(active)),key=lambda j:abs(residual[j])):
        if abs(residual[j])>1e-6:continue
        i=active[j];row=[int(matrix[i,k]) for k in support];trial=sp.Matrix(equations+[row]);r=trial.rank()
        if r==rank:continue
        equations.append(row);rhs.append(C*int(a[i])-int(q[i]));rank=r
        if rank==len(support):break
    if rank!=len(support):return None
    exact=sp.Matrix(equations).inv()*sp.Matrix(rhs);theta=[Fraction(0)]*len(float_theta)
    for k,z in zip(support,exact):theta[k]=Fraction(int(sp.numer(z)),int(sp.denom(z)))
    return theta


def fit(rows,columns,grammar,out):
    start=time.process_time();matrix=np.asarray([r['delta'][:columns] for r in rows],dtype=np.int64);a=np.asarray([r['a'] for r in rows],dtype=np.int64);q=np.asarray([r['q'] for r in rows],dtype=np.int64)
    # Deterministic diversity: different original rows, never synthetic credit.
    active=[];seen=set()
    for i,r in enumerate(rows):
        if r['id'][0]=='graph' and r['id'][1]>4:continue
        signature=tuple(r['delta'][:columns])+ (r['a'],r['q'])
        if signature not in seen:seen.add(signature);active.append(i)
    history=[];last=None
    for round_id in range(24):
        x=matrix[active].astype(float);aa=a[active].astype(float);qq=q[active].astype(float)
        # theta = positive-negative split; choose any finite C, then prefer a
        # compact coefficient certificate at a relaxed integer C ceiling.
        constraints=np.column_stack([x,-x,-aa]);objective=np.zeros(2*columns+1);objective[-1]=1
        lp=linprog(objective,A_ub=constraints,b_ub=-qq,bounds=[(0,None)]*(2*columns+1),method='highs',options={'time_limit':45})
        if lp.status!=0:
            return {'status':'OPEN_LP_FAILURE','LP_status':int(lp.status),'grammar':grammar,'history':history,'message':lp.message}
        cap=math.ceil(float(lp.x[-1])-1e-8);bounds=[(0,None)]*(2*columns)+[(cap,cap)]
        objective=np.ones(2*columns+1);objective[-1]=0
        compact=linprog(objective,A_ub=constraints,b_ub=-qq,bounds=bounds,method='highs',options={'time_limit':45})
        sol=compact if compact.status==0 else lp
        floats=sol.x[:columns]-sol.x[columns:2*columns]
        theta=recover_vertex(matrix,a,q,active,floats,cap) if compact.status==0 else None
        if theta is None:theta=[Fraction(float(v)).limit_denominator(65536) for v in floats]
        program=candidate(theta,Fraction(float(sol.x[-1])).limit_denominator(65536),grammar);slack,den=exact_slack(matrix,a,q,program)
        worst=int(np.argmax(slack));positive=np.flatnonzero(slack>0)
        record={'round':round_id,'active_original_rows':len(active),'C':program['C'],'theta':program['theta'],'worst_exact_slack':str(Fraction(int(slack[worst]),den)),'worst_row':rows[worst]['id'],'violating_rows':len(positive)}
        history.append(record);last=program
        print(grammar,round_id,record['C'],record['worst_exact_slack'],record['worst_row'],flush=True)
        if not len(positive):
            return {'status':'FINITE_EXACT_CANDIDATE','grammar':grammar,'candidate':program,'history':history,'checked_original_rows':len(rows),'cpu_seconds':time.process_time()-start,'universal_cost_contract':'OPEN'}
        # Add the strongest actual failures; keep event provenance. If a float
        # solution violates its own active rational rows, report it honestly.
        active_set=set(active)
        if any(i in active_set for i in positive):return {'status':'OPEN_RATIONAL_RECOVERY','grammar':grammar,'candidate':program,'history':history}
        order=sorted(map(int,positive),key=lambda i:int(slack[i]),reverse=True)
        added=0
        for i in order:
            signature=tuple(matrix[i])+(int(a[i]),int(q[i]))
            if signature not in seen:seen.add(signature);active.append(i);added+=1
            if added>=64:break
        assert added and time.process_time()-start<=360
    return {'status':'OPEN_CEGIS_BUDGET','grammar':grammar,'candidate':last,'history':history}


def evaluate_seed(rows):
    program=candidate([0,0,0,0,1,0],4,'frontier3');m=np.asarray([r['delta'][:6] for r in rows],dtype=np.int64);a=np.asarray([r['a'] for r in rows]);q=np.asarray([r['q'] for r in rows]);slack,den=exact_slack(m,a,q,program);i=int(np.argmax(slack))
    return {'candidate':program,'max_exact_slack':str(Fraction(int(slack[i]),den)),'worst_original_row':rows[i],'status':'REFUTED—EXACT candidate only' if slack[i]>0 else 'FINITE-EXACT only'}
