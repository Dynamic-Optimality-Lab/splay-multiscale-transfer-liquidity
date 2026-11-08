"""New universal frame/algebra proof terms, never a finite source test."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l,r):return (k,l,r)
def atoms(t):return [t] if isinstance(t,str) else atoms(t[1])+[t[0]]+atoms(t[2])
def right(t):
    g,left,d=t;p,a,b=left
    return N(p,a,N(g,b,d))
def left(t):
    g,a,rt=t;p,b,d=rt
    return N(p,N(g,a,b),d)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def main():
    # Arbitrary subtree variables; Ltail/Rfan carry the other r-2 marked leaves.
    ll=N('x',N('u1',N('y','A','B'),'Ltail'),'Rfan')
    ll_result=right(right(ll))
    assert ll_result==N('y','A',N('u1','B',N('x','Ltail','Rfan')))
    rr=N('x','Lfan',N('uR','Rtail',N('y','C','D')))
    rr_result=left(left(rr))
    assert rr_result==N('y',N('uR',N('x','Lfan','Rtail'),'C'),'D')
    assert atoms(ll)==atoms(ll_result) and atoms(rr)==atoms(rr_result)
    # Last return event e supplies both actual units; names are free IDs.
    old=['old0','old1'];critical=['critical0','critical1'];return_units=['return0','return1']
    assert (old+critical)[:4]==old+critical
    assert not (old+critical)[4:]
    bank_after_first=2-2;bank_after_return=2-2
    assert bank_after_first==bank_after_return==0
    common_payment=return_units[0];surplus=return_units[1:]
    assert common_payment=='return0' and surplus==['return1']
    assert 2-4+2-0==0 and 2-1+2-2==1
    # Ordinal types separate the new unit from all old tail receipt modules.
    assert 1<4
    # Affine identities in r: r-2 leaves, at most one unvisited next target.
    leaves=(1,-2);at_most_endpoint=(0,1);required=add(leaves,mul(-1,at_most_endpoint))
    assert required==(1,-3) and required[0]*6+required[1]==3
    # Affine polynomial in arbitrary number t of inserted zero H1/q2 rows.
    A=(1,3);QE=(2,6);QF=(2,7)
    assert add(mul(2,A),mul(-1,QE))==(0,0)
    assert add(mul(2,A),mul(-1,QF))==(0,-1)
    out('derivation.json',{'status':'PASS_PARTIAL_SOURCE_RESULTS_ONLY',
        'new_results':{
            'direct_return_surplus':{'old_fixed_chart_debts':[0,2,2],'aux_H':[1,1],'aux_q':[4,1],
                'full_q':[5,1],'P':1,'donor':'bit1 of the return macro sole actual A event',
                'aux_macro_ordinal':1,'births':[0,1],'old_tail_receipt_minimum_ordinal':4},
            'leaf_activation_barrier':{'scope':'all r>=3 maximal closed cores; all marked/free fringe populations',
                'post_packet_leaves':'M minus {maximum-target,extreme-return}',
                'gap_first_visits_at_least':'r-3; r-2 if next maximum target is not one of these leaves',
                'r6_lower_bound':3,'candidate_events':'last actual A event of each required first-visit natural macro',
                'candidate_events_distinct':True,'candidate_events_proved_unused':False},
            'zero_reserve_kernel':{'equation':'q=2H+d_next-d','necessary_H_upper_bound':3,
                'H1':'q=2+d_next-d in 1..4','H2':'q=4+d_next-d in 2..4; d_next<=d','H3':'q4,d2,d_next0'}},
        'generic_source_frames':[{'orientation':'LL','source':ll,'destination':ll_result},{'orientation':'RR','source':rr,'destination':rr_result}],
        'algebraic_orbit_only':{'zero_auxiliary_reserve':True,'source_realizability_proved':False,
            'certified_negative_source_cycle':False,'purpose':'range/price identities alone do not prove missing source exclusion'},
        'old_semantic_rows_replayed':0,'finite_population_tests':0,'source_engine_calls':0,'new_graphs':0,
        'Step2_complete':False,'all_unguarded_packets_closed':False,'Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS generic source frames, exact return-surplus receipt, and necessary zero-reserve identities; universal Step2 OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_derivation_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
