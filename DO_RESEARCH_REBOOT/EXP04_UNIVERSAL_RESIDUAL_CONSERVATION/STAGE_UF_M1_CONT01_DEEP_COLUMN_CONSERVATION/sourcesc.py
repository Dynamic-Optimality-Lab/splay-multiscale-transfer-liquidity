from basec import *
from cohortc import decode_state
from coercion import coerce,advance,finish_pair,from_tuple,ind,L
import copy

def opposite_parent(x,enclose):
    old=load(M0/'SOURCE_CATALOG.json')[5]['source'];b0=old['initial_B']
    tail=L
    for k in range(10,x,-1):tail=ind.node(k,L,tail)
    low=ind.node(x,ind.balanced(range(1,x)),tail)
    a0=from_tuple(ind.node(23,ind.node(11,low,ind.balanced(range(12,23))),ind.node(24,L,L)))
    reach,rs=coerce(b0,a0)
    body=[['K',23],['K',11],['K',x]]+([['K',12]] if enclose else [])
    a,_=advance(a0,[v for tag,v in body]);b,_=advance(b0,[v for tag,v in body])
    reset,rest=finish_pair(a,b,a0,b0)
    return {'name':f'M1C1_opposite_parent_x{x}_enclose{int(enclose)}','family':'opposite_parent_frame_birth',
        'initial_A':a0,'initial_B':b0,'diagonal_initial':b0,'reaching_prefix':[['D',v] for v in reach],
        'operations':body+reset,'critical_consumer_operation':3,'critical_old_g':10,
        'critical_birth_operation':2,'expected_birth_output':[3,10],
        'prefix_stats':rs,'measured_restoration':rest}

def exposure_loop(order,at):
    s=copy.deepcopy(load(M0/'SOURCE_CATALOG.json')[6]['source']);phys=load(M0/'PHYS_06.json')
    st=decode_state(phys,phys['boundaries'][at-1]['pre_A_state'])
    mid,_=advance(st,order);repair,rs=coerce(mid,st)
    loop=[['D',v] for v in list(order)+list(repair)]
    assert len(loop)<20000
    s['name']=f'M1C1_frame_exposure_order{order[0]}_{order[1]}_at{at}'
    s['family']='A_only_exact_loop_before_original_creator'
    s['base_source_sha256']=digest(load(M0/'SOURCE_CATALOG.json')[6]['source'])
    s['operations']=s['operations'][:at-1]+loop+s['operations'][at-1:]
    s['inserted_exact_A_loop']=loop;s['loop_repair_stats']=rs;s['original_creator_operation']=646
    s['new_creator_operation']=646+len(loop);s['new_consumer_operation']=653+len(loop)
    for k in ('A','Q_B','trace_hash','closing_A','closing_B'):s.pop(k,None)
    return s

def fresh_sources():
    out=[opposite_parent(x,e) for x in (3,5,6,8) for e in (False,True)]
    for at in (645,646):
        for order in ((10,298),(298,10)):out.append(exposure_loop(order,at))
    assert len(out)==12
    return out
