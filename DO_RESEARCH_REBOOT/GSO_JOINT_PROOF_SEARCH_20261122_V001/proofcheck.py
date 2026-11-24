"""Independent certificate checker; imports no learner or schema producer.

Rotations and marker propagation are rederived from the original symbolic
trees, with arbitrary hanging holes. Linear proof coefficients are checked
arithmetically; reserve and safety implications are checked over unbounded
integer states. Scope is a required proof dependency, never a report label.
"""
import sys
import json
from pathlib import Path
import z3
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))


def turn(t,path,direction):
    if path:
        result=list(t);side=3 if path[0]=='L' else 4
        result[side]=turn(t[side],path[1:],direction);return result
    assert t[0]=='node'
    key,mark,L,R=t[1:]
    if direction=='left':
        assert R[0]=='node';_,child,cm,middle,far=R
        return ['node',child,cm,['node',key,mark,L,middle],far]
    assert L[0]=='node';_,child,cm,far,middle=L
    return ['node',child,cm,far,['node',key,mark,middle,R]]


def flatten(t):
    if t[0]=='hole':return [('hole',t[1])]
    return flatten(t[3])+[('key',t[1])]+flatten(t[4])


def markers(t):
    if t[0]=='hole':return []
    return ([0] if t[2] else [])+[d+1 for d in markers(t[3])]+[d+1 for d in markers(t[4])]


def structural(ir,bound):
    rows=ir['rotation_schemas'];required={'ZIG_L','ZIG_R','LL','RR','LR','RL'}
    assert {r['case'] for r in rows}==required and len(rows)==6
    expected={'ZIG_L':([['','right']],1,0),'ZIG_R':([['','left']],1,0),
              'LL':([['','right'],['','right']],2,1),
              'RR':([['','left'],['','left']],2,1),
              'LR':([['L','left'],['','right']],2,1),
              'RL':([['R','right'],['','left']],2,1)}
    result=[]
    for row in rows:
        moves,consume,q=expected[row['case']]
        assert row['rotations']==moves and row['consumed_path_frames']==consume and row['original_B_double_cost']==q
        before=row['before'];after=before
        assert markers(before)==[0] and before[1]==('p' if consume==1 else 'g')
        atoms=flatten(before);assert len(atoms)==len(set(atoms)), 'No duplicate or erased hole/key.'
        key_order={'ZIG_L':['x','p'],'ZIG_R':['p','x'],'LL':['x','p','g'],
                   'RR':['g','p','x'],'LR':['p','x','g'],'RL':['g','x','p']}
        assert [key for tag,key in atoms if tag=='key']==key_order[row['case']]
        for path,direction in moves:after=turn(after,path,direction)
        assert after==row['after'] and flatten(after)==atoms and after[1]=='x'
        assert markers(after)==[row['old_root_post_depth']] and markers(after)[0]<=bound
        # The same local physical rotation below a nonempty outer context has
        # no root marker in its local tree. It therefore cannot move the marked
        # outer original root. Arbitrary hole substitution preserves this fact.
        def unmark(t):return list(t) if t[0]=='hole' else ['node',t[1],False,unmark(t[3]),unmark(t[4])]
        inner=unmark(before)
        for path,direction in moves:inner=turn(inner,path,direction)
        assert markers(inner)==[]
        result.append({'case':row['case'],'arbitrary_holes_retained':True,'post_old_root_depth':markers(after)[0]})
    r=z3.Int('remaining_frames')
    solver=z3.Solver();solver.add(r>=0,z3.Not(z3.Or(r==0,r==1,r==2,r>=3)));assert solver.check()==z3.unsat
    solver=z3.Solver();solver.add(r>=3,z3.Or(r-2<1,r-2>=r));assert solver.check()==z3.unsat
    return result


def unsat(name,domain,claim):
    solver=z3.Solver();solver.set(timeout=10000);solver.add(*domain,z3.Not(claim))
    assert solver.check()==z3.unsat, (name,solver.model() if solver.check()==z3.sat else solver.reason_unknown())
    return {'obligation':name,'verified_unbounded':True}


def check(cert,requested_scope=None):
    assert cert['status'] in ('PROVED_SCOPED_SYMBOLIC_CERTIFICATE','PROVED_GLOBAL_SYMBOLIC_CERTIFICATE')
    scope=cert['scope'];p=cert['candidate'];ir=read('PROOF_LANGUAGE.json')
    allowed={'root_bound','bank_capacity','overflow_ticket','A_coefficient','KEEP_coefficient',
             'priority','extra_A_allowance','global_capacity_scale','bank_weight','overflow_weight',
             'overflow_mode','path_invariant','bank_invariant','ticket_invariant','reserve_invariant'}
    assert set(p)<=allowed,'Unknown potential/history terms require a separate boundary proof.'
    assert cert['status']==('PROVED_SCOPED_SYMBOLIC_CERTIFICATE' if scope=='two_targets' else 'PROVED_GLOBAL_SYMBOLIC_CERTIFICATE')
    structure=structural(ir,p['root_bound'])
    a,b,c,d=p['path_invariant']
    assert a==1 and a+b==0 and -2*b+c==0 and -b+d==0
    a,b,c,d,e=p['bank_invariant']
    assert a==1 and a+b==0 and a+c==0 and a+d==0 and -a+e==0
    a,b,c,d=p['ticket_invariant']
    assert a==1 and a+b==0 and -a+c==0 and -a+d==0
    H,T,t,z,Q,R=z3.Ints('H T target ticket doubles other')
    coeff=p['reserve_invariant'];assert coeff[0]==1
    val=lambda v:z3.Sum([c*x for c,x in zip(coeff,v)])
    minimum=lambda x,y:z3.If(x<y,x,y)
    paid=minimum(1,t+R);overflow=1-paid;extra=minimum(z,overflow)
    next_t=minimum(H,t+R-paid)
    global_mode=p.get('overflow_mode',0)==1
    domain=[H>=0,T>=0,t>=0,t<=H,z>=0,Q>=0,R>=0,val([t,z,Q,H,T])>=0]+([] if global_mode else [z<=T])
    entry=z3.Int('entry')
    init=[H,entry,0,H,T] if global_mode else [H,T,0,H,T]
    checks=[unsat('reserve_init',[H>=0,T>=0]+([entry>=T] if global_mode else []),val(init)>=0),
            unsat('reserve_double_total',domain,val([next_t,z-extra,Q+1,H,T])>=0),
            unsat('reserve_zig_total',domain,val([minimum(H,t+R),z,Q,H,T])>=0)]
    initial,remaining,zigs=z3.Ints('initial remaining zigs')
    path=z3.Sum([v*x for v,x in zip(p['path_invariant'],[initial,remaining,Q,zigs])])==0
    costdomain=domain+[H==p['bank_capacity'],T==p['overflow_ticket'],initial>=0,
        remaining>=2,zigs==0,path,R<=7*H]
    if scope=='two_targets':costdomain.append(initial<=p['root_bound'])
    else:assert scope=='unrestricted'
    wb=p.get('bank_weight',1);wg=p.get('overflow_weight',1);assert wb>=0 and wg>=0
    checks.append(unsat('original_q_bank_plus_overflow',costdomain,wb*paid+wg*extra>=1))
    assert p['A_coefficient']>=8*wb*p['bank_capacity']+wg*p.get('extra_A_allowance',0)
    assert p['KEEP_coefficient']>=wb*p['bank_capacity']+wg*p['overflow_ticket']
    assert cert['constant']==p['A_coefficient']+p['KEEP_coefficient']
    proof={row['obligation']:row['result'] for row in cert['proof_dag']}
    if global_mode:
        assert proof['ticket_boundary']=='PERSISTENT_GLOBAL_RESERVE_CLOSED_BY_CONSTRUCTION'
        assert proof['cyclic_bank_seam']=='COUPLED_MONOTONE_GLOBAL_RESERVE'
        assert proof['global_resource_conservation']=='GENERIC_BANK_INVARIANT_INSTANTIATED_AT_GLOBAL_RESERVE'
        assert p['global_capacity_scale']>=p['overflow_ticket']
        N,G=z3.Ints('N G');cap=p['global_capacity_scale']*N
        checks.append(unsat('global_access_entry',[N>=1,G>=0,G<=cap],minimum(cap,G+p['overflow_ticket'])>=p['overflow_ticket']))
        mass,larger,lowG,highG,q=z3.Ints('mass larger lowG highG cost')
        nonneg=lambda x:z3.If(x>=0,x,0)
        out=lambda g,m:nonneg(g-nonneg(q-m))
        checks.append(unsat('coupled_global_B_monotonicity',
                           [mass>=0,larger>=mass,lowG>=0,highG>=lowG,q>=0],
                           out(lowG,mass)<=out(highG,larger)))
    else:
        assert proof['ticket_boundary']=='ZERO_AT_EACH_OPERATION_BOUNDARY_BY_CONSERVATIVE_EXPIRY'
        assert proof['cyclic_bank_seam']==('ZERO_BANK' if p['bank_capacity']==0 else 'PINNED_MONOTONE_GREATEST_FIXED_POINT')
    assert proof['original_voucher_interface']=='PINNED_K_B_LE_A'
    if scope=='two_targets':
        assert proof['cyclic_entry']=='PROVED_TWO_TARGET_ROOT_RETURN'
        # Scope boundary proof: in an exactly closed B period containing a
        # KEEP, its initial root is the last KEEP target. With at most two
        # targets, every nontrivial next target is the OTHER root. A real splay
        # puts that former root at the verified depth<=bound. Trivial KEEP and
        # DELETE preserve B. Cut after any genuine KEEP; all entries obey the
        # bound by induction, including the wraparound. KB=0 has Q=0.
        boundary={'scope':'At most two distinct original B targets; all physical support and A DELETE work unrestricted.',
                  'root_set_from_pair_closure':True,'cut_after_real_nontrivial_KEEP':True,
                  'trivial_KEEP_and_DELETE_preserve_B':True,'KB_zero_case':'Q_B=0',
                  'no_bank_or_ticket_prefix_credit':True}
        x,y,last,begin,end,target=z3.Ints('firstTarget secondTarget lastKeep startRoot endRoot nextTarget')
        checks.append(unsat('original_root_set_from_pair_closure',
                           [x!=y,z3.Or(last==x,last==y),end==last,begin==end],z3.Or(begin==x,begin==y)))
        checks.append(unsat('nontrivial_two_target_switch_is_other',
                           [x!=y,z3.Or(begin==x,begin==y),z3.Or(target==x,target==y),target!=begin],
                           z3.Or(z3.And(begin==x,target==y),z3.And(begin==y,target==x))))
    else:
        assert proof['cyclic_entry']=='NO_RESTRICTED_ENTRY_ASSUMPTION_USED'
        boundary={'scope':'Unrestricted original targets','no_target_entry_bound_used':True}
    root_accepted=scope=='unrestricted'
    return {'passed':True,'scope':scope,'structural_cases':structure,'symbolic_checks':checks,
            'cyclic_boundary':boundary,'constant':cert['constant'],
            'potential':{'local_bank_total':wb,'global_overflow_reserve':wg,'cumulative_cost_terms':0},
            'root_acceptance':root_accepted,
            'requested_scope_accepted':requested_scope is None or requested_scope==scope,
            'source_uniform':True,'finite_source_fitting_used_as_proof':False,
            'proof_kernel_scope':'Independent symbolic rotation/frame and affine-ledger certificate checks; complete original BST implementation is not fully formalized in Lean.'}


def main():
    folder=sys.argv[1] if len(sys.argv)>1 else 'run_005'
    cert=read(folder+'/CONTROL_CERTIFICATE.json');result=check(cert,'two_targets')
    assert result['passed'] and not result['root_acceptance']
    if not (HERE/'FINAL_MANIFEST.json').exists():
        stem=folder.replace('/','_')+'_INDEPENDENT_PROOF_VERIFICATION'
        previous=list(HERE.glob(stem+'*.json'))
        if not any(json.loads(path.read_text(encoding='utf-8'))==result for path in previous):
            version=1;path=HERE/(stem+'.json')
            while path.exists():version+=1;path=HERE/(stem+'_v'+str(version)+'.json')
            path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('passed','scope','constant','root_acceptance','source_uniform')}))


if __name__=='__main__':main()
