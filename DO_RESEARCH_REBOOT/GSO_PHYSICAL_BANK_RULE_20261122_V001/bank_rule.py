"""Frozen saturated target-first physical bank, with exact cyclic completion.

The clipped map is a diagnostic completion of a PARTIAL payment rule. Any
underfunded B step is reported as failure, never silently counted as paid.
"""
import sys
import json
import gzip
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'GSO_TRACE_ENGINE_20261122_V001'
sys.path.insert(0,str(PREV));import trace as X;sys.path.pop(0)
K=X.K


def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists(),'sealed output'
    p=HERE/name;assert not p.exists(),'use a fresh artifact name';K.dump(p,value)


def events(z):
    owner={x:i for i,p in enumerate(z['blocks']) for x in p};out=[]
    for r in z['operations']:
        if r['k']:out.append({'id':['K',r['id']],'a':0,'q':0,'k':1,'target':r['target'],'scope':[owner[r['target']]],'priority':[owner[r['target']]]})
        for s in z['steps'][r['steps'][0]:r['steps'][1]]:
            target_block=owner[s['target']];scope=s['scope'];assert target_block in scope and len(scope)<=8
            order=[target_block]+[i for i in sorted(scope) if i!=target_block]
            out.append({k:s[k] for k in ('id','a','q','k','target','scope')}|{'priority':order})
    assert sum(e['a'] for e in out)==z['A'] and sum(e['q'] for e in out)==z['Q_B'] and sum(e['k'] for e in out)==z['K_B']
    return out


def update(stock,e,H):
    before=[stock[i] for i in e['priority']];mass=sum(before)
    if e['a'] or e['k']:
        for i in e['priority']:stock[i]=H
        issued=len(e['priority'])*H-mass;paid=0;unpaid=0
        assert 0<=issued<=(8*H if e['a'] else H)
    else:
        paid=min(mass,e['q']);unpaid=e['q']-paid;remaining=mass-paid;issued=0
        for i in e['priority']:
            stock[i]=min(H,remaining);remaining-=stock[i]
        assert remaining==0
    after=[stock[i] for i in e['priority']]
    assert sum(after)-mass==issued-paid and min(after,default=0)>=0 and max(after,default=0)<=H
    return {'before':before,'after':after,'issued':issued,'paid':paid,'unpaid':unpaid}


def sweep(initial,ev,H,record=False):
    stock=list(initial);paid=issued=0;fail=[];rows=[]
    assert min(stock,default=0)>=0 and max(stock,default=0)<=H
    for j,e in enumerate(ev):
        r=update(stock,e,H);paid+=r['paid'];issued+=r['issued']
        if r['unpaid']:fail.append({'event':j,'id':e['id'],'target':e['target'],'scope':e['scope'],'priority':e['priority'],'before':r['before'],'q':e['q'],'unpaid':r['unpaid']})
        if record:rows.append({'event':j,'id':e['id'],'priority':e['priority']}|r)
    assert sum(stock)-sum(initial)==issued-paid
    return stock,{'paid':paid,'issued':issued,'failures':fail,'rows':rows}


def cyclic(z,H,record=False):
    return cyclic_events(z,events(z),H,record,'all_original_B_doubles')


def cyclic_events(z,ev,H,record=False,demand_mode='explicit_relaxation'):
    assert type(H)==int and H>=1
    demand=sum(e['q'] for e in ev);m=len(z['blocks']);state=[H]*m;passes=[]
    for lap in range(m*H+1):
        new,r=sweep(state,ev,H)
        assert all(a<=b for a,b in zip(new,state)),'monotone descending upper chain violated'
        passes.append({'pass':lap,'mass_before':sum(state),'mass_after':sum(new),'unpaid':demand-r['paid']})
        if new==state:break
        assert sum(new)<sum(state);state=new
    else:raise AssertionError('finite integer descent bound violated')
    final,r=sweep(state,ev,H,record);assert final==state and r['issued']==r['paid']
    Aissued=sum(row['issued'] for row,e in zip(r['rows'],ev) if e['a']) if record else None
    return {'policy':'saturated_target_first_then_increasing_block','source':z['source']['name'],'demand_mode':demand_mode,'demand':demand,'H':H,'C_sufficient_if_universal':9*H,'status':'FUNDED_CLOSED_POLICY_ON_THIS_SOURCE' if not r['failures'] else 'EXACT_POLICY_OBSTRUCTION_AT_THIS_CAPACITY','A':z['A'],'Q_B':z['Q_B'],'K_B':z['K_B'],'blocks':m,'initial_greatest_fixed_point':state,'period_passes':passes,'paid':r['paid'],'issued':r['issued'],'failures':r['failures'],'rows':r['rows'],'A_issued':Aissued,'cyclic_seam_closed':True,'all_initial_balances_scope':'If this greatest clipped orbit fails a guard, no funded closed orbit for the SAME policy and capacity exists.','universal_CD':'OPEN'}


def audit():
    summary=[]
    for i in range(18):
        z=K.load(PREV/f'run_001/trace_{i:02d}.json.gz')
        for H in (1,2,5,8,16):
            r=cyclic(z,H,record=False);name=f'audit_001/source_{i:02d}_H{H}.json.gz';write(name,r)
            row={k:r[k] for k in ('source','H','status','A','Q_B','paid','issued','blocks')};row['index']=i;row['failures']=len(r['failures']);row['passes']=len(r['period_passes']);summary.append(row)
            print(json.dumps(row),flush=True)
    write('audit_001/SUMMARY.json',{'policy':'saturated_target_first_then_increasing_block','cases':summary,'scope':'Fixed named physical policy on complete original sources. No finite audit is a universal payment proof.','root_status':'OPEN'})


if __name__=='__main__':audit()
