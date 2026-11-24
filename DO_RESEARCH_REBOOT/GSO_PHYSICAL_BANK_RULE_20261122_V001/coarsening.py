"""Symbolic local transfer obstruction and finite physical role validation.

The arbitrary-support source proof must establish the displayed old H comb
recurrence and nested interior windows. No recurrence interpolation is used.
"""
import sys
import math
from collections import Counter
import z3
sys.dont_write_bytecode=True
import bank_rule as B


def lanes(mass,H):return tuple(min(H,max(0,mass-j*H)) for j in range(6))


def local_step(carry,a,b,H):
    mass=sum(carry)+2*a+b;out=lanes(max(0,mass-1),H)
    return (out[0],out[1],out[4]),{'a_new':out[5],'b_new':out[2],'retired':out[3],'paid':int(mass>0),'lanes':out}


def local_fixed(a,b,H):
    c=(H,H,H);history=[]
    for t in range(3*H+1):
        new,r=local_step(c,a,b,H);assert all(x<=y for x,y in zip(new,c));history.append([list(c),list(new)])
        if new==c:break
        assert sum(new)<sum(c);c=new
    else:raise AssertionError('upper carry descent did not stop')
    if 2*a+b:
        assert r['paid']==1 and 2*r['a_new']+r['b_new']<=2*a+b-1
        assert r['a_new']==max(0,2*a+b-2*H-1) and r['b_new']==min(H,2*a+b-1)
    else:assert c==(0,0,0) and not r['paid']
    return c,r,history


def symbolic():
    H,a,b,t,p,r=z3.Ints('H a b t p r');I=2*a+b;mass=t+p+r+I-1
    def clamp(v):return z3.If(v<=0,0,z3.If(v>=H,H,v))
    out=[clamp(mass-j*H) for j in range(6)]
    bounds=[H>=1,a>=0,a<=H,b>=0,b<=H,t>=0,t<=H,p>=0,p<=H,r>=0,r<=H,I>=1]
    fixed=[t==out[0],p==out[1],r==out[4]]
    questions={'weighted_drop':2*out[5]+out[2]<=I-1,'priority_retired_at_least_persistent':out[3]>=out[5],
               'closed_form_a':out[5]==z3.If(I-2*H-1>0,I-2*H-1,0),'closed_form_b':out[2]==z3.If(I-1<H,I-1,H)}
    checked=[]
    for name,claim in questions.items():
        solver=z3.Solver();solver.add(*bounds,*fixed,z3.Not(claim));assert solver.check()==z3.unsat,(name,solver.model());checked.append(name)
    # One lane is monotone for any offset. This proves whole-step
    # monotonicity regardless of footprint dimension or input-bank order.
    x,y,offset=z3.Ints('x y offset');s=z3.Solver();s.add(H>=1,x<=y,clamp(x-offset)>clamp(y-offset));assert s.check()==z3.unsat
    # Exact nested-window bound: if u >=2*T-2*burn-3, then the next
    # floor-halved upper bound remains >=T-2*burn-3.
    u,T,burn,lo=z3.Ints('u T burn lo');s=z3.Solver();s.add(burn>=1,u>=2*T-2*burn-3,u/2-burn<T-2*burn-3);assert s.check()==z3.unsat
    s=z3.Solver();s.add(lo>=1,lo<=4,z3.Or((lo+3)/2+1<1,(lo+3)/2+1>4));assert s.check()==z3.unsat
    return {'status':'PROVED_SYMBOLIC_INTEGER_TRANSFER_AND_WINDOW_IDENTITIES','Z3_unsat_queries':checked+['lane_monotonicity','nested_window_upper_bound','nested_window_lower_bound'],
            'carry':['target','current_parent_from_previous_external','previous_parent'],
            'fresh_inputs':['external_old_spine:a','demoted_grandparent_old_spine:a','left_subtree_root:b'],
            'ordered_output_lanes':['target','external','grandparent','old_left_root_retired','current_parent','previous_parent_persistent'],
            'fixed_mass_identity':'2a+b =1+a_new+b_new+retired',
            'priority_leak':'retired>=a_new',
            'weighted_drop':'2*a_new+b_new <=2*a+b-1',
            'closed_form':['a_new=max(0,2a+b-2H-1)','b_new=min(H,2a+b-1)'],
            'source_proof_needed':'Actual H comb roles, no A replenishment in the nested good windows, and actual U/Pi eligibility are proved in the mathematical manuscript and independently bound on complete witnesses.'}


def constant_profile_validation():
    cases=0
    for H in range(1,17):
        for a in range(H+1):
            for b in range(H+1):local_fixed(a,b,H);cases+=1
    return cases


def validate_roles(z,H,bulk_only=False):
    s=z['source'];N=len(s['initial_A']['children']);p=s['p'];q=s['q'];owner={x:i for i,block in enumerate(z['blocks']) for x in block};ev=B.events(z)
    critical={N-1+2**j:j for j in range(p+1)};types={tuple(st['id']):st['type'] for st in z['steps']}
    if bulk_only:
        ev=[dict(e,original_q=e['q'],q=int(e['id'][0]=='B' and critical.get(e['id'][1],-1)>=4 and types[tuple(e['id'])]=='RR')) for e in ev]
    stock=[H]*len(z['blocks']);after={};before={};steps_by_id={tuple(st['id']):st for st in z['steps']};roles=0;fail=[]
    for e in ev:
        actor=e['id'][0];op=e['id'][1];j=critical.get(op)
        if actor=='B' and j is not None and op not in before:before[op]=stock.copy()
        if actor=='B' and j is not None and j>=4 and types[tuple(e['id'])]=='RR':
            st=steps_by_id[tuple(e['id'])];first,second=st['bits'];x=e['target'];P=first['promoted'];g=first['demoted'];w=first['grandparent'];h1=first['middle'];h2=second['middle'];spacing=2**j
            assert g==P-spacing and w==P-2*spacing and h1==P-spacing//2
            assert w<g<h1<P<h2<x
            assert len({owner[k] for k in (x,w,g,h1,P,h2)})==6
            assert e['priority']==[owner[k] for k in (x,w,g,h1,P,h2)] and set(e['scope'])=={owner[k] for k in (x,w,g,h1,P,h2)}
            roles+=1
        r=B.update(stock,e,H)
        if r['unpaid']:fail.append(e['id'])
        if actor=='B' and j is not None:after[j]=stock.copy()
    assert after[3]
    a=b=H;l=1;u=2**(p-3)*(q+1)-3;burn=3*H+1;windows=[]
    for j in range(4,p+1):
        if u<l:break
        spacing=2**j;op=N-1+2**j
        for k in range(l,u+1):
            v=2+spacing*k
            assert after[j-1][owner[v]]<=a and after[j-1][owner[v-spacing//2]]<=b
            assert before[op][owner[v]]==after[j-1][owner[v]] and before[op][owner[v-spacing//2]]==after[j-1][owner[v-spacing//2]]
        carry,result,history=local_fixed(a,b,H);nl=(l+3)//2+1;nu=u//2-burn;aa=result['a_new'];bb=result['b_new']
        for k in range(nl,nu+1):
            v=2+2*spacing*k
            assert after[j][owner[v]]<=aa and after[j][owner[v-spacing]]<=bb,(j,k,after[j][owner[v]],aa,after[j][owner[v-spacing]],bb)
        windows.append({'phase':j,'old_a':a,'old_b':b,'old_lower':l,'old_upper':u,'new_a':aa,'new_b':bb,'new_lower':nl,'new_upper':nu,'weighted_before':2*a+b,'weighted_after':2*aa+bb,'local_carry_iterations':len(history)})
        a,b,l,u=aa,bb,nl,nu
    return {'source':s['name'],'H':H,'bulk_only_relaxation':bulk_only,'exact_six_role_RR_steps':roles,'interior_windows':windows,'all_failed_original_ids':fail,'status':'FINITE_PHYSICAL_BINDING_VERIFIED'}


def main():
    cert=symbolic();cert['finite_constant_profile_crosschecks']=constant_profile_validation();B.write('SYMBOLIC_COARSENING_CERTIFICATE.json',cert)
    z=B.K.load(B.HERE/'scaling_001/trace_08.json.gz')
    records=[validate_roles(z,H,bulk) for H in (5,8,16) for bulk in (False,True)]
    B.write('COARSENING_PHYSICAL_BINDING.json',{'cases':records,'scope':'Exact finite role/window validation; arbitrary-parameter theorem requires the complete physical comb and interval proof.'})
    print({'symbolic':cert['status'],'finite_profiles':cert['finite_constant_profile_crosschecks'],'role_checks':sum(r['exact_six_role_RR_steps'] for r in records),'cases':[(r['H'],r['bulk_only_relaxation'],len(r['all_failed_original_ids'])) for r in records]})


if __name__=='__main__':main()
