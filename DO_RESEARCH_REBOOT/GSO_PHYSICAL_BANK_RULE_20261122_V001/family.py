"""Complete all-capacity obstruction recipe; materialize only bounded instances.

Old H source definition includes every physical key, operation and both counted
restoration sweeps. No symbolic subtree stands for omitted physical cost.
"""
import sys
sys.dont_write_bytecode=True
import bank_rule as B
import fast_trace as F
import coarsening as C


def parameters(H):
    assert type(H)==int and H>=1
    p=3*H+4;q=12*H+32;N=2**(p+1)*(q+1)+1
    return {'H':H,'p':p,'q':q,'N':N,'burn_in':3*H+1,'base_phase':3,'zero_profile_by_phase':3+3*H,'forced_failure_phase':4+3*H,'original_A':4*(N-1),'original_operations':4*N-2}


def bulk_events(z):
    N=len(z['source']['initial_A']['children']);p=z['source']['p'];critical={N-1+2**j:j for j in range(p+1)};types={tuple(s['id']):s['type'] for s in z['steps']};ev=[]
    for e in B.events(z):
        original=e['q'];pay=int(e['id'][0]=='B' and critical.get(e['id'][1],-1)>=4 and types[tuple(e['id'])]=='RR')
        ev.append(dict(e,original_q=original,q=pay))
    return ev


def symbolic_recipe():
    return {'source_family':'W_H = original complete H_(p,q), p=3H+4, q=12H+32, H any positive integer','N':'2^(p+1)*(q+1)+1','initial_pair':'Both complete right vines on every rank1,...,N; empty reaching prefix','period':['DELETE2,...,N','Access N,...,1, KEEP exactly at N+1-2^j for0<=j<=p, DELETE elsewhere','KEEP1,...,N','KEEP N-1,...,1'],
            'closure':'The actual adjacent A sweeps close A. Counted increasing/decreasing KEEP restoration closes both full trees. All ranks are genuine; source valid for every p,q.','bank_demand_relaxation':'Only original RR doubles at critical phases j>=4 cost one; every other original B step costs zero in the accounting diagnostic. Original algorithm, full Q_B and all predicates remain unchanged. These charged RR IDs are genuine original U_int.','coarse_bound':'After base phase3 take uniform upper bounds a=b=H on old spine and old left-root banks. Burn 3H+1 RR steps per coarsening interior. At stationary upper carry, 2a_new+b_new <=2a+b-1.','windows':'Initial l=1,u=2^(p-3)*(q+1)-3; next l=ceil((l+2)/2)+1<=4 and u=floor(u/2)-(3H+1). Uniformly u_r>=2^(p-3-r)*(q+1)-2(3H+1)-3.','forced_failure':'By phase p-1=3+3H the interior fresh-input bounds are zero. Phase p has at least3H+1 consecutive valid interior RR steps. At entry its three carry banks contain at most3H credits. No fresh input occurs, so at least one original U demand is unpaid.','scope':'All finite integer capacities for this frozen target-first/increasing-order transfer law, even with maximal A/KEEP replenishment and arbitrary initial balances. Not arbitrary redistribution or Universal CD.'}


def run():
    B.write('ALL_CAPACITY_SOURCE_RECIPE.json',symbolic_recipe())
    # Complete larger-capacity original witness, already physically compiled.
    z=B.K.load(B.HERE/'scaling_001/trace_08.json.gz');r=B.cyclic(z,8,True);assert len(r['failures'])==2
    B.write('counter_001/H8_H9q5_policy.json.gz',r)
    # One fully materialized member of the universal symbolic recipe.
    par=parameters(1);assert par['N']<=12000
    src=B.K.PARAM.H(par['p'],par['q']);z=F.compile_source(src);B.write('counter_001/W_H1_complete_trace.json.gz',z)
    ev=bulk_events(z);r=B.cyclic_events(z,ev,1,True,'only_original_critical_RR_at_phases_ge4; other_B_costs_free')
    assert r['failures'] and r['paid']<r['demand'];B.write('counter_001/W_H1_relaxed_policy.json.gz',r)
    binding=C.validate_roles(z,1,True);assert binding['all_failed_original_ids'];B.write('counter_001/W_H1_coarsening_binding.json',binding)
    B.write('counter_001/SUMMARY.json',{'H8_source':'scaling_001/trace_08.json.gz','H8_policy':'counter_001/H8_H9q5_policy.json.gz','W_H1_parameters':par,'W_H1_demand':r['demand'],'W_H1_paid':r['paid'],'W_H1_failures':len(r['failures']),'all_capacity_proof':'Complete source recipe plus physical role/window and monotone-carry proof; not inferred from finite witnesses.','root_status':'OPEN'})
    print({'H8_original_unpaid':2,'W_H1':par,'relaxed_demand':r['demand'],'relaxed_paid':r['paid'],'unpaid':len(r['failures'])})


if __name__=='__main__':run()
