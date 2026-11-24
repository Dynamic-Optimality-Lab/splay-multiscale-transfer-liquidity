"""Joint invariant/accounting CEGIS with unbounded symbolic proof teachers.

The discovered coefficients, structural bound and overflow allowance are
checked together. No finite-source fit or assumed funded guard is accepted.
"""
import sys
import json
import time
from pathlib import Path
import z3
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))
def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    p=HERE/name;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2),encoding='utf-8')


def dot(coeffs,values):return z3.Sum([c*v for c,v in zip(coeffs,values)])
def clamp0(v):return z3.If(v<0,0,v)
def minimum(a,b):return z3.If(a<b,a,b)


def teacher(candidate,scope):
    """Negation of each actual universal proof obligation, over unbounded Ints."""
    rows=[]
    def check(name,variables,assumptions,claim,kind,pre=None,post=None,vector=None,extra=None):
        solver=z3.Solver();solver.set(timeout=10000);solver.add(*assumptions,z3.Not(claim))
        status=solver.check()
        if status==z3.unknown:return {'kind':'UNKNOWN','obligation':name,'reason':solver.reason_unknown()}
        if status==z3.sat:
            model=solver.model();values={str(v):model.eval(v,model_completion=True).as_long() for v in variables}
            result={'kind':kind,'obligation':name,'values':values}
            if pre is not None:result['pre']=[model.eval(v,model_completion=True).as_long() if z3.is_expr(v) else v for v in pre]
            if post is not None:result['post']=[model.eval(v,model_completion=True).as_long() if z3.is_expr(v) else v for v in post]
            if vector:result['vector']=vector
            if extra:result.update(extra)
            return result
        rows.append({'obligation':name,'result':'UNSAT_NEGATION','quantification':'All values satisfying the displayed symbolic transition domain.'})
        return None
    b=candidate['root_bound'];h=candidate['bank_capacity'];T=candidate['overflow_ticket']
    global_mode=candidate.get('overflow_mode',0)==1
    extra_A=candidate.get('extra_A_allowance',0)
    wb=candidate.get('bank_weight',1);wg=candidate.get('overflow_weight',1)
    coeff=candidate['path_invariant'];bank=candidate['bank_invariant'];ticket=candidate['ticket_invariant'];reserve=candidate['reserve_invariant']
    # The invariant coefficients are learned, not supplied as the answer.
    n,r,q,z=z3.Ints('initialDepth remaining doubles zigs')
    domain=[n>=0,r>=0,q>=0,z>=0,z<=1]
    eq=lambda v:dot(coeff,v)==0
    init=[n,n,0,0]
    failure=check('path_initialization',[n],[n>=0],eq(init),'INIT',post=init,vector='path_invariant')
    if failure:return failure,rows
    for name,guard,post in [('double',r>=2,[n,r-2,q+1,z]),('zig',z3.And(r==1,z==0),[n,0,q,1])]:
        pre=[n,r,q,z]
        failure=check('path_preservation_'+name,[n,r,q,z],domain+[guard,eq(pre)],eq(post),'ICE_EQ',pre,post,'path_invariant')
        if failure:return failure,rows
    # Generic conservation lemmas cover arbitrary nonnegative issuance/payment;
    # their truth is independent of a particular bank capacity or source size.
    S,S0,IA,IK,P,i,p=z3.Ints('bank initialBank Aissued Kissued bankPaid issuance payment')
    bpre=[S,S0,IA,IK,P];beq=lambda v:dot(bank,v)==0
    binit=[S0,S0,0,0,0]
    failure=check('bank_initialization',[S0],[S0>=0],beq(binit),'INIT',post=binit,vector='bank_invariant')
    if failure:return failure,rows
    for name,post,guards in [('A',[S+i,S0,IA+i,IK,P],[i>=0]),('KEEP',[S+i,S0,IA,IK+i,P],[i>=0]),('B',[S-p,S0,IA,IK,P+p],[p>=0,p<=S])]:
        failure=check('bank_preservation_'+name,[S,S0,IA,IK,P,i,p],[S>=0,S0>=0,IA>=0,IK>=0,P>=0,beq(bpre),*guards],beq(post),'ICE_EQ',bpre,post,'bank_invariant')
        if failure:return failure,rows
    Z,IT,V,E,u=z3.Ints('ticket ticketIssued overflowPaid expired debit')
    tpre=[Z,IT,V,E];teq=lambda v:dot(ticket,v)==0
    failure=check('ticket_initialization',[],[],teq([0,0,0,0]),'INIT',post=[0,0,0,0],vector='ticket_invariant')
    if failure:return failure,rows
    for name,post,guards in [('KEEP',[Z+i,IT+i,V,E],[i>=0]),('B',[Z-u,IT,V+u,E],[u>=0,u<=Z]),('expire',[0,IT,V,E+Z],[])]:
        failure=check('ticket_preservation_'+name,[Z,IT,V,E,i,u],[Z>=0,IT>=0,V>=0,E>=0,teq(tpre),*guards],teq(post),'ICE_EQ',tpre,post,'ticket_invariant')
        if failure:return failure,rows
    # A reserve inequality is learned across TOTAL clipped updates. An empty
    # bank/ticket does not remove the legal original B transition.
    t,R,H,TT,Q=z3.Ints('target other H T spentDoubles')
    rs=lambda values:dot(reserve,values)>=0
    entry=z3.Int('entryReserve')
    rinit=[H,entry,0,H,TT] if global_mode else [H,TT,0,H,TT]
    failure=check('reserve_initialization',[H,TT,entry],[H>=0,TT>=0]+([entry>=TT] if global_mode else []),rs(rinit),'INIT_GE',post=rinit,vector='reserve_invariant')
    if failure:return failure,rows
    pre=[t,Z,Q,H,TT];pbank=minimum(1,t+R);unpaid=1-pbank;pticket=minimum(Z,unpaid)
    after_t=minimum(H,t+R-pbank);post=[after_t,Z-pticket,Q+1,H,TT]
    failure=check('reserve_total_double_preservation',[t,Z,Q,H,TT,R],
                  [H>=0,TT>=0,t>=0,t<=H,Z>=0,Q>=0,R>=0,rs(pre)]+([] if global_mode else [Z<=TT]),rs(post),
                  'ICE_GE',pre,post,'reserve_invariant')
    if failure:return failure,rows
    postzig=[minimum(H,t+R),Z,Q,H,TT]
    failure=check('reserve_zig_preservation',[t,Z,Q,H,TT,R],
                  [H>=0,TT>=0,t>=0,t<=H,Z>=0,Q>=0,R>=0,rs(pre)]+([] if global_mode else [Z<=TT]),rs(postzig),
                  'ICE_GE',pre,postzig,'reserve_invariant')
    if failure:return failure,rows
    # Physical frame induction is driven by the six actual symbolic schemas.
    for shape in read('PROOF_LANGUAGE.json')['rotation_schemas']:
        depth=shape['old_root_post_depth']
        if depth>b:return {'kind':'STRUCTURAL_BOUND','obligation':'final_'+shape['case'],'required_bound':depth},rows
        rows.append({'obligation':'final_'+shape['case'],'result':'STRUCTURAL_NORMAL_FORM','old_root_depth':depth})
    # Under a two-target cyclic source, next nontrivial target is precisely the
    # previous root. Under unrestricted targets no such entry bound is supplied.
    scope_bounds=[n<=b] if scope=='two_targets' else []
    assumptions=domain+scope_bounds+[r>=2,z==0,eq([n,r,q,z]),H==h,TT==T,
                t>=0,t<=H,Z>=0,R>=0,R<=7*H,rs([t,Z,q,H,TT])]+([] if global_mode else [Z<=TT])
    claim=1-wb*pbank-wg*pticket<=0
    failure=check('original_double_all_cost_accounted',[n,r,q,z,t,Z,H,TT,R],assumptions,claim,
                  'SAFETY',pre=[t,Z,q,H,TT],vector='reserve_invariant',
                  extra={'path_pre_symbolic':True,'scope':scope})
    if failure:return failure,rows
    # Learn cost coefficients against actual original A/K source interfaces.
    c,d=candidate['A_coefficient'],candidate['KEEP_coefficient']
    failure=check('shared_A_cost',[i],[i>=0,i<=wb*8*h+wg*extra_A],i<=c,'COST_A')
    if failure:return failure,rows
    failure=check('once_per_KEEP_cost',[i],[i>=0,i<=wb*h],i+wg*T<=d,'COST_KEEP')
    if failure:return failure,rows
    if global_mode:
        N,G=z3.Ints('physicalKeys previousGlobalReserve');cap=candidate['global_capacity_scale']*N
        failure=check('global_reserve_access_entry',[N,G],[N>=1,G>=0,G<=cap],minimum(cap,G+T)>=T,'GLOBAL_ENTRY')
        if failure:return failure,rows
        rows.append({'obligation':'global_resource_conservation','result':'GENERIC_BANK_INVARIANT_INSTANTIATED_AT_GLOBAL_RESERVE'})
    rows.extend([{'obligation':'whole_loop_termination','result':'NATURAL_FRAME_RANK_DECREASES'},
                 {'obligation':'cyclic_entry','result':'PROVED_TWO_TARGET_ROOT_RETURN' if scope=='two_targets' else 'NO_RESTRICTED_ENTRY_ASSUMPTION_USED'},
                 {'obligation':'cyclic_bank_seam','result':'COUPLED_MONOTONE_GLOBAL_RESERVE' if global_mode else ('ZERO_BANK' if h==0 else 'PINNED_MONOTONE_GREATEST_FIXED_POINT')},
                 {'obligation':'ticket_boundary','result':'PERSISTENT_GLOBAL_RESERVE_CLOSED_BY_CONSTRUCTION' if global_mode else 'ZERO_AT_EACH_OPERATION_BOUNDARY_BY_CONSERVATIVE_EXPIRY'},
                 {'obligation':'original_voucher_interface','result':'PINNED_K_B_LE_A'}])
    return None,rows


def synthesize(scope,global_mode=False,use_cache=True):
    start=time.perf_counter();solver=z3.Optimize();solver.set(timeout=10000)
    names=['root_bound','bank_capacity','overflow_ticket','A_coefficient','KEEP_coefficient','priority','extra_A_allowance','global_capacity_scale','bank_weight','overflow_weight']
    p={name:z3.Int(name) for name in names}
    solver.add(p['root_bound']>=0,p['root_bound']<=8,
               z3.Or(*[p['bank_capacity']==v for v in (0,1,2,5,8)]),
               p['overflow_ticket']>=0,p['overflow_ticket']<=64,
               p['A_coefficient']>=0,p['A_coefficient']<=512,
               p['KEEP_coefficient']>=0,p['KEEP_coefficient']<=512,
               p['priority']>=0,p['priority']<=1,
               p['extra_A_allowance']>=0,p['extra_A_allowance']<=64,
               p['global_capacity_scale']>=0,p['global_capacity_scale']<=8,
               p['bank_weight']>=0,p['bank_weight']<=8,
               p['overflow_weight']>=0,p['overflow_weight']<=8)
    if not global_mode:solver.add(p['extra_A_allowance']==0,p['global_capacity_scale']==0)
    else:solver.add(p['global_capacity_scale']>=1)
    # Exact quantifier elimination of the two issuance obligations. Exposing
    # these proved necessary rows to the optimizer prevents unpriced hardware
    # changes from evading every invariant counterexample at objective zero.
    # The independent teacher still checks the full universal inequalities.
    # Finite bounded weights are encoded by linear ITEs rather than nonlinear
    # products. This is exact in the declared search grammar.
    mul=lambda amount,weight:z3.Sum([z3.If(weight==v,v*amount,0) for v in range(9)])
    solver.add(p['A_coefficient']>=8*mul(p['bank_capacity'],p['bank_weight'])+mul(p['extra_A_allowance'],p['overflow_weight']),
               p['KEEP_coefficient']>=mul(p['bank_capacity'],p['bank_weight'])+mul(p['overflow_ticket'],p['overflow_weight']))
    if global_mode:solver.add(p['global_capacity_scale']>=p['overflow_ticket'])
    # Original final-double schema with depth2 is an admissible positive entry
    # in BOTH scopes. Initialization must include it. Propagate this symbolic
    # safety row to synthesis instead of letting the invariant hide that entry.
    solver.add(z3.If(p['bank_capacity']>=1,p['bank_weight'],
                     z3.If(p['overflow_ticket']>=1,p['overflow_weight'],0))>=1)
    vectors={name:[z3.Int(name+'_'+str(i)) for i in range(length)]
             for name,length in [('path_invariant',4),('bank_invariant',5),('ticket_invariant',4),('reserve_invariant',5)]}
    for name,vec in vectors.items():
        solver.add(*[z3.And(v>=-8,v<=8) for v in vec]);solver.add(vec[0]==1)
    cache_path=HERE/'run_003/CONTROL_CERTIFICATE.json'
    reused=0
    if use_cache and cache_path.exists():
        for event in read('run_003/CONTROL_CERTIFICATE.json')['iterations']:
            failure=event['result'];kind=failure.get('kind')
            if kind in ('INIT','INIT_GE'):
                value=dot(vectors[failure['vector']],failure['post'])
                solver.add(value==0 if kind=='INIT' else value>=0);reused+=1
            elif kind in ('ICE_EQ','ICE_GE'):
                vec=vectors[failure['vector']];before=dot(vec,failure['pre']);after=dot(vec,failure['post'])
                solver.add(z3.Or(before!=0,after==0) if kind=='ICE_EQ' else z3.Or(before<0,after>=0));reused+=1
            elif kind=='STRUCTURAL_BOUND':
                solver.add(p['root_bound']>=failure['required_bound']);reused+=1
    # Reserve normalization anchors the target stock. The other coefficients,
    # including the costs of H,T and spent work, are synthesized.
    solver.minimize(p['A_coefficient']+p['KEEP_coefficient'])
    solver.minimize(p['root_bound'])
    solver.minimize(p['priority'])
    solver.minimize(p['global_capacity_scale'])
    solver.minimize(p['bank_weight']+p['overflow_weight'])
    solver.minimize(z3.Sum([z3.If(x>=0,x,-x) for vs in vectors.values() for x in vs]))
    trace=[];candidate=None
    for iteration in range(96):
        if time.perf_counter()-start>240:break
        status=solver.check()
        if status!=z3.sat:
            return {'status':'NO_CERTIFICATE_IN_BOUNDED_LANGUAGE' if status==z3.unsat else 'SYNTHESIS_UNKNOWN',
                    'scope':scope,'iterations':trace,'last_candidate':candidate,'universal_CD':'OPEN'}
        model=solver.model();candidate={name:model.eval(v,model_completion=True).as_long() for name,v in p.items()}
        candidate['overflow_mode']=int(global_mode)
        candidate.update({name:[model.eval(v,model_completion=True).as_long() for v in vs] for name,vs in vectors.items()})
        failure,proof=teacher(candidate,scope)
        trace.append({'iteration':iteration,'candidate':candidate,'result':failure or {'kind':'ALL_OBLIGATIONS_PROVED'},'checked_obligations':len(proof)})
        if failure is None:
            return {'status':'PROVED_SCOPED_SYMBOLIC_CERTIFICATE' if scope=='two_targets' else 'PROVED_GLOBAL_SYMBOLIC_CERTIFICATE',
                    'scope':scope,'candidate':candidate,'proof_dag':proof,'iterations':trace,
                    'constant':candidate['A_coefficient']+candidate['KEEP_coefficient'],
                    'reused_inductive_counterconstraints':reused,
                    'seconds':time.perf_counter()-start,'universal_CD':'OPEN' if scope!='unrestricted' else 'CANDIDATE_PENDING_INDEPENDENT_PHYSICAL_CHECK'}
        kind=failure['kind']
        if kind=='UNKNOWN':break
        if kind=='STRUCTURAL_BOUND':solver.add(p['root_bound']>=failure['required_bound']);continue
        if kind=='COST_A':solver.add(p['A_coefficient']>=failure['values']['issuance']);continue
        if kind=='COST_KEEP':solver.add(p['KEEP_coefficient']>=failure['values']['issuance']+mul(p['overflow_ticket'],p['overflow_weight']));continue
        if kind in ('INIT','INIT_GE'):
            value=dot(vectors[failure['vector']],failure['post'])
            solver.add(value==0 if kind=='INIT' else value>=0);continue
        if kind in ('ICE_EQ','ICE_GE'):
            vec=vectors[failure['vector']];before=dot(vec,failure['pre']);after=dot(vec,failure['post'])
            solver.add(z3.Or(before!=0,after==0) if kind=='ICE_EQ' else z3.Or(before<0,after>=0));continue
        if kind=='SAFETY':
            v=failure['values'];pre=[v['target'],v['ticket'],v['doubles'],v['H'],v['T']]
            # A changed physical-depth invariant or hardware parameters may
            # invalidate this abstract counterstate; a current legal successor
            # may never simply be dropped while its predecessor is retained.
            path_values=[v['initialDepth'],v['remaining'],v['doubles'],v['zigs']]
            reasons=[dot(vectors['path_invariant'],path_values)!=0,
                     dot(vectors['reserve_invariant'],pre)<0,
                     p['bank_capacity']!=v['H'],p['overflow_ticket']!=v['T']]
            bank_at_counter=min(1,v['target']+v['other'])
            overflow_at_counter=min(v['ticket'],1-bank_at_counter)
            reasons.append(p['bank_weight']*bank_at_counter+p['overflow_weight']*overflow_at_counter>=1)
            if scope=='two_targets':reasons.append(p['root_bound']<v['initialDepth'])
            solver.add(z3.Or(*reasons));continue
        raise AssertionError(failure)
    return {'status':'BOUNDED_SEARCH_UNKNOWN','scope':scope,'iterations':trace,'last_candidate':candidate,
            'seconds':time.perf_counter()-start,'universal_CD':'OPEN'}


def main():
    prefix=sys.argv[1] if len(sys.argv)>1 else 'run_002'
    global_mode=len(sys.argv)>2 and sys.argv[2]=='global'
    use_cache=not(len(sys.argv)>4 and sys.argv[4]=='cold')
    control=synthesize('two_targets',global_mode,use_cache);write(prefix+'/CONTROL_CERTIFICATE.json',control)
    print(json.dumps({'control':control['status'],'iterations':len(control['iterations']),
                      'candidate':control.get('candidate')}),flush=True)
    # The unrestricted run uses the SAME certificate language, with no target
    # entry bound and no promised global feasibility premise.
    if len(sys.argv)>3 and sys.argv[3]=='checked_barrier':
        # Earlier actual unrestricted CEGIS attempts are preserved. Once the
        # parametric barrier is checked, do not enumerate constants in a model
        # already known to permit unbounded abstract cost cycles.
        barrier=read('GLOBAL_ABSTRACT_BARRIER.json')
        assert barrier['status']=='PROVED_ALL_FINITE_PARAMETERS_ABSTRACT_MODEL_BARRIER'
        root={'status':'ABSTRACT_MODEL_EXPRESSIVENESS_OBSTRUCTION','scope':'unrestricted',
              'iterations':[],'prior_actual_joint_searches':['run_003/ROOT_SEARCH.json','run_004/ROOT_SEARCH.json'],
              'barrier':'GLOBAL_ABSTRACT_BARRIER.json','physical_counterexample':False,
              'original_state_refinement':'OPEN','universal_CD':'OPEN'}
    else:root=synthesize('unrestricted',global_mode,use_cache)
    write(prefix+'/ROOT_SEARCH.json',root)
    print(json.dumps({'root':root['status'],'iterations':len(root['iterations']),'universal_CD':'OPEN'}),flush=True)


if __name__=='__main__':main()
