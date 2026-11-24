"""Actually synthesize local/interface values AND bounded cyclic banks together.

Finite full original histories only. A history table is not a physical policy
or a source-uniform induction. Exact rational checks decide finite acceptance.
"""
import sys
import math
import json
from collections import Counter
from fractions import Fraction
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
sys.dont_write_bytecode=True
import trace as X
import trace_teacher as T


def source_events(z):
    out=[]
    for r in z['operations']:
        if r['k']:
            owner=next(i for i,p in enumerate(z['blocks']) if r['target'] in p)
            out.append({'id':['K',r['id']],'a':0,'q':0,'k':1,'scope':[owner],'delta':{}})
        for s in z['steps'][r['steps'][0]:r['steps'][1]]:
            diff=Counter(s['signature_after'].values());diff.subtract(s['signature_before'].values())
            out.append({k:s[k] for k in ('id','a','q','k','scope')}|{'delta':{k:v for k,v in diff.items() if v}})
    return out


def run():
    indices=[0,1,2,6,8,17];traces=[X.K.load(X.HERE/f'run_001/trace_{i:02d}.json.gz') for i in indices];event_lists=[source_events(z) for z in traces]
    states=sorted({s for ev in event_lists for e in ev for s in e['delta']});names=['phi:'+s for s in states]+['c','d','H'];idx={n:i for i,n in enumerate(names)};num=len(names)
    rr=[];cc=[];vv=[];rhs=[];eqr=[];eqc=[];eqv=[];eqrhs=[];layouts=[];bankcols=[]
    def variable(name):
        nonlocal num
        col=num;num+=1;bankcols.append(col);return col
    def row(coefs,b):
        j=len(rhs);rhs.append(b)
        for col,v in coefs.items():rr.append(j);cc.append(col);vv.append(v)
    for i,z,ev in zip(indices,traces,event_lists):
        initial={b:variable(f'{i}:{b}:0') for b in range(len(z['blocks']))};last=initial.copy();steps=[]
        for e in ev:
            after={b:variable('') for b in e['scope']};coefs={idx['phi:'+s]:v for s,v in e['delta'].items()};coefs[idx['c']]=-e['a'];coefs[idx['d']]=-e['k']
            for b in e['scope']:coefs[after[b]]=coefs.get(after[b],0)+1;coefs[last[b]]=coefs.get(last[b],0)-1
            # A strict rational margin on B steps makes rounding safe. This
            # is a stronger finite search condition, never extra source work.
            eps=1/32 if e['id'][0]=='B' else 0
            row(coefs,-e['q']-eps);steps.append({'event':e,'before':{b:last[b] for b in e['scope']},'after':after});last.update(after)
        for b in initial:
            if last[b]!=initial[b]:
                j=len(eqrhs);eqrhs.append(0);eqr.extend((j,j));eqc.extend((last[b],initial[b]));eqv.extend((1,-1))
        layouts.append({'index':i,'initial':initial,'last':last,'steps':steps})
    for col in bankcols:row({col:1,idx['H']:-1},0)
    matrix=coo_matrix((vv,(rr,cc)),shape=(len(rhs),num)).tocsr();eq=coo_matrix((eqv,(eqr,eqc)),shape=(len(eqrhs),num)).tocsr()
    objective=np.zeros(num);objective[idx['c']]=objective[idx['d']]=1;objective[idx['H']]=0.00001
    bounds=[(None,None)]*len(states)+[(0,None)]*3+[(0,None)]*len(bankcols)
    lp=linprog(objective,A_ub=matrix,b_ub=np.asarray(rhs),A_eq=eq,b_eq=np.asarray(eqrhs),bounds=bounds,method='highs',options={'time_limit':45})
    if lp.status!=0:
        out={'status':'OPEN_NUMERICAL_OR_TIME_LIMIT','message':lp.message,'variables':num,'rows':len(rhs),'root_status':'OPEN'};X.write('joint_001/CERTIFICATE.json',out);print(out);return
    vals=[Fraction(float(v)).limit_denominator(65536) for v in lp.x]
    vals[idx['c']]=Fraction(math.ceil(lp.x[idx['c']])+1);vals[idx['d']]=Fraction(math.ceil(lp.x[idx['d']])+1);vals[idx['H']]=Fraction(math.ceil(lp.x[idx['H']])+1)
    for col in bankcols:vals[col]=max(Fraction(0),vals[col])
    histories=[];worst=Fraction(-10**20)
    for layout in layouts:
        events=[]
        for saved in layout['steps']:
            e=saved['event'];delta=sum(v*vals[idx['phi:'+s]] for s,v in e['delta'].items());delta+=sum(vals[col] for col in saved['after'].values())-sum(vals[col] for col in saved['before'].values());slack=e['q']+delta-vals[idx['c']]*e['a']-vals[idx['d']]*e['k'];worst=max(worst,slack)
            events.append({'id':e['id'],'before':{str(b):str(vals[col]) for b,col in saved['before'].items()},'after':{str(b):str(vals[col]) for b,col in saved['after'].items()}})
        assert all(vals[layout['last'][b]]==vals[col] for b,col in layout['initial'].items())
        histories.append({'index':layout['index'],'initial':{str(b):str(vals[col]) for b,col in layout['initial'].items()},'events':events})
    assert all(0<=vals[col]<=vals[idx['H']] for col in bankcols)
    out={'status':'FINITE_EXACT_JOINT' if worst<=0 else 'NUMERICAL_RATIONAL_RECOVERY_FAILED','c':str(vals[idx['c']]),'d':str(vals[idx['d']]),'H':str(vals[idx['H']]),'values':{s:str(vals[idx['phi:'+s]]) for s in states},'histories':histories,'original_source_indices':indices,'variables':num,'inequality_rows':len(rhs),'seam_equations':len(eqrhs),'max_exact_slack':str(worst),'bank_policy':'Per-source finite cyclic table, NOT a rule on arbitrary histories.','universal_CD':'OPEN','missing_induction_guard':'Construct a source-uniform physical bank update rule that always funds the next B step and closes cyclically.'}
    X.write('joint_001/CERTIFICATE.json.gz',out);X.write('joint_001/SUMMARY.json',{k:v for k,v in out.items() if k not in ('values','histories')});print({k:v for k,v in out.items() if k not in ('values','histories')})


if __name__=='__main__':run()
