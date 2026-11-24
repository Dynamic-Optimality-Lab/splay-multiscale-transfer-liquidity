"""Joint anonymous-port potential teacher and exact cyclic bank teacher.

These are discovery/obstruction tools, not an oracle for the unbounded proof.
All floating potential fits are checked afterwards over rational numbers.
All bank certificates use exact integer capacities and original occurrence IDs.
"""
from fractions import Fraction
from collections import Counter,defaultdict
import math
import networkx as nx
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import trace as X


def potential_rows(traces):
    return [{'id':[z['source']['name'],r['id']],'delta':r['delta'],'a':r['a'],'q':r['q'],'k':r['k']} for z in traces for r in z['operations']]


def synthesize(rows):
    states=sorted({s for r in rows for s in r['delta']});idx={s:i for i,s in enumerate(states)};n=len(states)
    rr=[];cc=[];vv=[]
    for j,r in enumerate(rows):
        for s,v in r['delta'].items():rr.append(j);cc.append(idx[s]);vv.append(v)
        rr.extend((j,j));cc.extend((n,n+1));vv.extend((-r['a'],-r['k']))
    matrix=coo_matrix((vv,(rr,cc)),shape=(len(rows),n+2)).tocsr()
    objective=np.zeros(n+2);objective[-2:]=1
    lp=linprog(objective,A_ub=matrix,b_ub=-np.asarray([r['q'] for r in rows]),bounds=[(None,None)]*n+[(0,None)]*2,method='highs',options={'time_limit':60})
    if lp.status!=0:return {'status':'OPEN_NUMERICAL_OR_INFEASIBLE','message':lp.message,'rows':len(rows),'states':n,'universal':'OPEN'}
    p=[Fraction(float(v)).limit_denominator(2**20) for v in lp.x];slack=[]
    for r in rows:
        slack.append(Fraction(r['q'])+sum(v*p[idx[s]] for s,v in r['delta'].items())-p[n]*r['a']-p[n+1]*r['k'])
    result={'status':'FINITE_EXACT' if max(slack,default=0)<=0 else 'NUMERICAL_RATIONAL_RECOVERY_FAILED','c':str(p[n]),'d':str(p[n+1]),'c_plus_d':str(p[n]+p[n+1]),'values':{s:str(p[i]) for s,i in idx.items()},'rows':len(rows),'observer_states':n,'max_exact_slack':str(max(slack,default=0)),'worst_original_id':rows[max(range(len(rows)),key=lambda i:slack[i])]['id'] if rows else None,'universal':'OPEN','missing_contract':'Universal A/B loop induction, including unseen external-port pairings, not finite training accuracy.'}
    return result


def verify_potential(rows,cert):
    assert cert['status']=='FINITE_EXACT'
    p={s:Fraction(v) for s,v in cert['values'].items()};c=Fraction(cert['c']);d=Fraction(cert['d'])
    assert c>=0 and d>=0
    assert all(Fraction(r['q'])+sum(v*p[s] for s,v in r['delta'].items())<=c*r['a']+d*r['k'] for r in rows)
    return True


def events(z):
    """Keep voucher at most once per actual nontrivial original B access."""
    owner={x:i for i,p in enumerate(z['blocks']) for x in p};out=[]
    for r in z['operations']:
        if r['k']:out.append({'id':['K',r['id']],'a':0,'q':0,'k':1,'scope':[owner[r['target']]]})
        for s in z['steps'][r['steps'][0]:r['steps'][1]]:out.append({k:s[k] for k in ('id','a','q','k','scope')})
    return out


def bank_network(z,c,d,capacity):
    """Compressed time-expanded local bank network, including the cyclic seam.

    One shared source edge issues c per actual A StepEv. B cannot issue credit.
    Each event can transfer only among its physical four-endpoint footprints.
    Every block has capacity H; no credit comes from the reaching prefix.
    """
    assert all(isinstance(v,int) and v>=0 for v in (c,d,capacity))
    ev=events(z);demand=z['Q_B'];inf=demand+c*z['A']+d*z['K_B']+1
    g=nx.DiGraph();g.add_nodes_from(('s','t'));initial={i:f'b{i}:0' for i in range(len(z['blocks']))};last=initial.copy();sequence=Counter();issuance=[];payments=[]
    for j,e in enumerate(ev):
        hub=f'e{j}';g.add_node(hub)
        for i in e['scope']:
            g.add_edge(last[i],hub,capacity=inf)
            sequence[i]+=1;nxt=f'b{i}:{sequence[i]}'
            g.add_edge(hub,nxt,capacity=capacity);last[i]=nxt
        supply=c*e['a']+d*e['k']
        if supply:g.add_edge('s',hub,capacity=supply);issuance.append([j,supply])
        if e['q']:g.add_edge(hub,'t',capacity=e['q']);payments.append(j)
    for i in initial:
        # A never-touched block cannot pay anything, and needs no self loop.
        if last[i]!=initial[i]:g.add_edge(last[i],initial[i],capacity=capacity)
    return g,ev,issuance,payments


def bank(z,c=4,d=0,capacity=4):
    g,ev,issued,payments=bank_network(z,c,d,capacity)
    value,flow=nx.maximum_flow(g,'s','t',flow_func=nx.algorithms.flow.preflow_push)
    positive=[[u,v,int(vv)] for u,vs in flow.items() for v,vv in vs.items() if vv]
    result={'status':'FINITE_EXACT_BANK' if value==z['Q_B'] else 'EXACT_GRAMMAR_MINCUT','name':z['source']['name'],'c':c,'d':d,'capacity':capacity,'demand':z['Q_B'],'paid':int(value),'network_nodes':len(g),'network_edges':g.number_of_edges(),'positive_flows':positive,'issued_credit':sum(flow['s'].values()),'all_A_issuance_capacity':c*z['A'],'all_KEEP_issuance_capacity':d*z['K_B'],'universal':'OPEN','scope':'This complete original source and this storage/transfer grammar. Feasibility is not a universal physical policy.'}
    if value!=z['Q_B']:
        cut,(left,right)=nx.minimum_cut(g,'s','t',flow_func=nx.algorithms.flow.preflow_push)
        edges=[[u,v,data['capacity']] for u,v,data in g.edges(data=True) if u in left and v in right]
        assert sum(e[2] for e in edges)==cut==value
        result['cut']={'capacity':int(cut),'edges':edges,'left':sorted(left),'right':sorted(right)}
    verify_bank(z,result)
    return result


def verify_bank(z,cert):
    g,ev,issued,payments=bank_network(z,cert['c'],cert['d'],cert['capacity']);flow={(u,v):v0 for u,v,v0 in cert['positive_flows']}
    assert len(flow)==len(cert['positive_flows'])
    ins=Counter();outs=Counter()
    for (u,v),w in flow.items():
        assert g.has_edge(u,v) and 0<w<=g[u][v]['capacity'];outs[u]+=w;ins[v]+=w
    assert all(ins[v]==outs[v] for v in g if v not in ('s','t'))
    assert outs['s']==ins['t']==cert['paid'] and cert['issued_credit']==outs['s']
    if cert['status']=='FINITE_EXACT_BANK':assert cert['paid']==z['Q_B']
    else:
        cut=cert['cut'];left=set(cut['left']);right=set(cut['right']);assert left|right==set(g) and not left&right and 's' in left and 't' in right
        assert sum(data['capacity'] for u,v,data in g.edges(data=True) if u in left and v in right)==cut['capacity']==cert['paid']<z['Q_B']
    return True


def induction_contract():
    return {'acceptance':'q_t + Phi_after - Phi_before <= c*a_t + d*k_t','state':'Exact named physical boundary ports plus local projected A/B trees, target, actor, mode, original StepEv/pairing state; optionally explicit signed bank balances.','required_proofs':['Initialization on every admissible diagonal-reaching source without period prefix credit','A-phase loop preservation with globally shared issuance, not credit per incident block','B-phase loop preservation including zero/one/two retained-bit cases and external-pivot pairing','Every original B double consumed once','Conservative transfers and no credit when ancestry is recreated','A symbolic whole-operation inequality for arbitrary depths and all hanging subtrees','Physical-state closure, or a separately constructed closed history-bank seam','Original K_B voucher injection into disjoint incoming A gaps'], 'not_acceptable':['Finite fitting accuracy','Unrestricted cycle feasibility asserted for all sources','An invariant classifier that excludes a legal successor of an included predecessor','Assuming history-bank closure from physical pair closure','Counting port update incidence as a paid B budget'],'status':'OPEN_UNTIL_ALL_CONTRACTS_HAVE_PROOFS'}


if __name__=='__main__':
    z=X.K.load(X.HERE/'bootstrap/trace_noncommutation.json.gz');r=bank(z);X.write('bootstrap/bank.json',r);X.write('INDUCTION_INTERFACE.json',induction_contract());p=synthesize(potential_rows([z]));verify_potential(potential_rows([z]),p);X.write('bootstrap/potential.json',p)
    print({'bank':r['status'],'potential':p['status'],'universal':'OPEN'})
