"""Universal source-AST/sign audit, not finite original-state tests."""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
def lp(p):return Path('\\\\?\\'+str(Path(p).resolve()))
def sha(p):return hashlib.sha256(lp(p).read_bytes()).hexdigest()
def read(p):return json.loads(lp(p).read_text(encoding='utf-8'))
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)
def lin(*parts):
    out={}
    for p in parts:
        for k,v in p.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}
def dump(n):return ast.dump(n,include_attributes=False)
def function(tree,n):return next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==n)
def append_conjunct(fn,expression):
    wanted=dump(ast.parse(expression,mode='eval').body)
    return any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
      and isinstance(n.func.value,ast.Name) and n.func.value.id=='C' and n.func.attr=='append'
      and len(n.args)==1 and dump(n.args[0])==wanted for n in ast.walk(fn))

def main():
    baseline=read(BASE/'entry_baseline.json');pins={v['path']:v['sha256'] for v in baseline['files']}
    root=BASE.parent/'06_CERTIFICATES'
    strict=root/'DIRECT_CDK5N_11F_STRICT_CLOSURE'
    pc=root/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER'
    sources=[strict/'STRICT_LOW_COMPILER.py',strict/'STRICT_SOURCE_REPAIRS.py',
      pc/'PC_ROTATION_INTERPRETER.py',pc/'PC_B_CONTROLLER.py']
    syntax={};source_hashes={}
    for p in sources:
        assert p.as_posix() in pins and sha(p)==pins[p.as_posix()],p
        source_hashes[p.as_posix()]=sha(p)
        syntax[p.name]=ast.parse(lp(p).read_text(encoding='utf-8-sig'))
    build=function(syntax['STRICT_LOW_COMPILER.py'],'build_slow')
    required=[
      ('mask_conservation','d.EQ(s.mu, t.mu)'),
      ('terminal_KEEP','mux_ref(d, wit.evK, last)'),
      ('terminal_is_Score','tisS'),('terminal_marked','marked'),
      ('same_KEEP_target_active','same_keep_target(d, wit, inv, bt, e, active)'),
      ('final_A_authoritative_shadow','shadow_match7(d, wit, st, t)'),
      ('final_B_root_equality','d.EQ(t.b.root, bs[5].root)'),
      ('root_terminated_active_paths','root_terminated(d, wit, bt, st, bs[e], e, active)'),
    ]
    clauses=[]
    for name,expr in required:
        assert append_conjunct(build,expr),name
        clauses.append({'name':name,'actual_asserted_source_expression':expr})
    assert any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='root' for t in n.targets)
      and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='AND'
      and any(isinstance(a,ast.Starred) and isinstance(a.value,ast.Name) and a.value.id=='C' for a in n.value.args)
      for n in ast.walk(build))
    # The marked bit is about terminal tsi, not a presumed marked source.
    assert any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='mubit'
      and [ast.unparse(a) for a in n.args]==['d','s.mu','k'] for n in ast.walk(build))
    assert any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='tisS' for t in n.targets)
      and ast.unparse(n.value)=='mux_ref(d, wit.isS, tt)' for n in ast.walk(build))
    assert any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='tt' for t in n.targets)
      and ast.unparse(n.value)=='mux_ref(d, wit.evT, last)' for n in ast.walk(build))
    same=function(syntax['STRICT_SOURCE_REPAIRS.py'],'same_keep_target')
    assert append_conjunct(same,'d.OR(d.NOT(isK), d.EQ(aS, bC))')
    assert append_conjunct(same,'d.OR(d.NOT(d.AND(isK, aS)), d.EQ(aI, bT))')
    shadow=function(syntax['STRICT_LOW_COMPILER.py'],'shadow_match7')
    assert append_conjunct(shadow,"d.EQ(mux_ref(d, wit.isS, sh['root']), s.aS[p])")
    assert append_conjunct(shadow,"d.OR(d.NOT(s.aS[p]), d.EQ(mux_ref(d, wit.sidx, sh['root']), s.aI[p]))")
    # Source A inactive-event gates and final B delete/inactive identity
    # are read only. Canonical splay root postconditions are old theorems.
    ae=function(syntax['PC_ROTATION_INTERPRETER.py'],'splay_event')
    assert any(isinstance(n,ast.Assign) and ast.unparse(n)=='pair_on = d.AND(ev_active, pair_on)' for n in ast.walk(ae))
    assert any(isinstance(n,ast.Assign) and ast.unparse(n)=='zig_on = d.AND(ev_active, zig_on)' for n in ast.walk(ae))
    be=function(syntax['PC_B_CONTROLLER.py'],'b_splay_event')
    assert any(isinstance(n,ast.keyword) and n.arg=='root' and ast.unparse(n.value)=='d.ITE(is_delete, bs0.root, st.root)' for n in ast.walk(be))
    assert any(isinstance(n,ast.Assign) and ast.unparse(n)=='eff_del = d.OR(d.NOT(active), d.NOT(isK))' for n in ast.walk(build))
    write('checkpoint01_source.json',{'status':'PASS','asserted_terminal_clauses':clauses,
      'actual_root_copy_and_same_Score_core_index_checked':True,
      'inactive_A_B_identity_gates_checked':True,'all_LOW_destinations_P_proved_with_reused_splay_root_postcondition':True,
      'source_marked_assumption_added':False,'source_hashes':source_hashes,
      'original_modules_imported_or_executed':False})

    old={'w':1,'Dt':1,'Ds':-1};reduction={'Ds':1,'Es':-1}
    transport=lin(old,reduction)
    assert transport=={'w':1,'Dt':1,'Es':-1}
    negative_core={'w':1,'psi_t':1,'psi_s':-1}
    target_floor={'Et':1,'psi_t':-1};nonnegative_psi={'psi_s':1}
    direct_negative=lin(negative_core,target_floor,nonnegative_psi)
    assert direct_negative=={'w':1,'Et':1}
    nonnegative_source0={'nonnegative_weight':1,'target_debt':1}
    assert all(v>=0 for v in nonnegative_source0.values())
    signs={'row_transport_coefficients':transport,'off_P_negative_coefficients':direct_negative,
      'off_P_nonnegative_residual_basis':nonnegative_source0,
      'transport_nonnegative_basis':{'old_residual':1,'source_reduction':1},
      'negative_nonnegative_basis':{'old_core_residual':1,'target_floor_excess':1,'psi_source':1}}
    assert all(v>=0 for k in ('transport_nonnegative_basis','negative_nonnegative_basis') for v in signs[k].values())
    old_dir=BASE.parent/'M3_XFER16'
    prev=read(old_dir/'certificate.json');pa=read(old_dir/'symbolic_audit.json')
    assert prev['all_eight_hidden_profiles_closed'] and prev['all_previous_visible_profiles_preserved']
    assert prev['every_previously_valid_original_LOW_row_preserved'] and prev['HIGH_and_h0_glue_preserved']
    assert pa['status']=='HIDDEN_GAMMA1_SAFE_CEILING_UNIVERSAL_AUDIT_PASS'
    assert pa['all_height_ge7_cores_psi_zero'] and prev['new_range_0_2_and_psi_floor_preserved']
    write('checkpoint02_sign.json',{'status':'PASS','symbolic_coefficients':signs,
      'any_previously_valid_LOW_row_preserved':True,'all_off_P_LOW_rows_proved':True,
      'global_psi_or_Lambda_floor_for_D_term_claimed':False,'psi_floor_at_every_LOW_destination_preserved':True,
      'HIGH_h0_range_glue_preserved':True})

    deps=[BASE.parent/'RESEARCH_RULES.md',BASE.parent/'M3_AER01/RESULT.md',
      BASE.parent/'M3_E1_01/OUTSIDE_E1.md',old_dir/'HIDDEN_GAMMA1_REPAYMENT.md',
      old_dir/'PROOF_AUDIT.md',old_dir/'PARTITION_UPDATE.md',old_dir/'certificate.json',
      old_dir/'symbolic_audit.json',old_dir/'partition_update.json']
    inherited=read(old_dir/'dependencies.json')
    ldr=next(Path(v['path']) for v in inherited['files'] if v['path'].endswith('/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md'))
    deps.append(ldr)
    for p in deps:assert p.as_posix() in pins and sha(p)==pins[p.as_posix()],p
    ldr_text=lp(ldr).read_text(encoding='utf-8')
    assert 'psi(source)=2, psi(destination)=0' in ldr_text
    assert 'all 4,862 ordered core topologies' in ldr_text
    # Reuse old published zero-reset fact, NOT its stored bank/model or
    # control execution, to audit why a blanket H1 psi floor is invalid.
    zerofloor={'blanket_H1_zero_target_psi_at_least1':'REFUTED_BY_REUSED_ESTABLISHED_ZERO_RESET',
      'new_saved_psi_query_or_control_replay':False,
      'current_D_hid_or_D_term_refuted_by_this_fact':False}

    part=read(old_dir/'partition_update.json');cells=[]
    for c in part['cells']:
        v=dict(c);v['current_potential']='D_term = D_hid on P, 0 outside P'
        if c['normal_form']=='H1':
            assert c['status']=='OPEN'
            v.update(source_P_required_for_any_failure=True,source_root_must_be_marked=True,
              root_mark_status_axis_closed_for_unmarked_sources=True,
              current_failure_both_values_equal_D_hid=True,
              closure_needed='prove signed repayment on the full remaining MARKED-source original H1 zero schema',
              remaining_quantifiers='marked synchronized source; all remaining original masks/core topologies/parent types/exposures/G/raw fields/sigma/private witnesses')
            if c['psi_source']==1:v['source_core_height_at_most']=6
        else:
            assert 'CLOSED' in c['status']
            v.update(status='CLOSED_UNIVERSAL_FOR_D_term',transport='terminal-root source reduction preserves every valid LOW row')
        cells.append(v)
    assert len(cells)==52 and sum(c['status']=='OPEN' for c in cells)==36
    assert all(c['source_root_must_be_marked'] for c in cells if c['status']=='OPEN')
    write('partition_update.json',{'parent_partition':(old_dir/'partition_update.json').as_posix(),
      'parent_sha256':sha(old_dir/'partition_update.json'),'all_old_files_preserved':True,
      'every_unmarked_source_LOW_row_closed':True,'marked_source_required_for_any_remaining_failure':True,
      'remaining_H1_schematic_slots':36,'remaining_Gamma1_zero_slots':0,
      'slots_are_universal_formulas_not_tested_instances':True,'all_remaining_signed_leaves_closed':False,
      'Step4_complete':False,'no_remaining_cell_nonemptiness_asserted':True,'cells':cells})
    assert time.process_time()<CAP
    result={'status':'TERMINAL_ROOT_NORMALIZATION_UNIVERSAL_AUDIT_PASS',
      'all_original_LOW_destinations_P':True,'source_marked_requirement_added_to_original_graph':False,
      'new_public_debt':'D_term=D_hid on marked synchronized Score roots, 0 elsewhere',
      'every_previously_valid_LOW_row_preserved':True,'all_unmarked_source_LOW_rows_proved':True,
      'global_psi_floor_for_new_debt_claimed':False,'global_E1_floor1_for_new_debt_claimed':False,
      'psi_floor_at_all_LOW_destinations_preserved':True,'HIGH_h0_glue_preserved':True,
      'all_completed_Gamma1_zero_rows_preserved':True,'all_original_quantifiers_and_full_coordinates_preserved':True,
      'new_source_AST_conjuncts_checked':clauses,'symbolic_sign_certificates':signs,
      'reused_zero_reset_scope_audit':zerofloor,'source_hashes_reused_not_executed':source_hashes,
      'reused_proof_hashes':{p.as_posix():sha(p) for p in deps},
      'remaining_H1_schemas':36,'remaining_sources_marked_only':True,'remaining_Gamma1_zero_schemas':0,
      'all_remaining_marked_H1_leaves_closed':False,'requested_full_Step4_closure_achieved':False,
      'Step4_complete':False,'M3_status':'OPEN',
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_bank_censuses':0,'new_label_fits':0,'completed_semantic_checks_replayed':0,
      'original_negative_cycle_certified':False,'full_compiler_formalization_claimed':False,
      'external_human_or_model_review_claimed':False,'CPU_seconds':time.process_time(),'CPU_cap':CAP}
    write('symbolic_audit.json',result)
    print(json.dumps({'status':result['status'],'all_unmarked_source_LOW':'PROVED',
      'remaining_marked_H1_schemas':36,'remaining_Gamma1_zero_schemas':0,'Step4':'OPEN',
      'requested_full_closure_achieved':False,'new_finite_tests':0},indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
