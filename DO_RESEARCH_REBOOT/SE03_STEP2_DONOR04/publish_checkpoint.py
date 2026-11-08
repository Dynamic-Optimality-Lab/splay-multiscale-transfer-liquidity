"""Append-only unfinished research checkpoint. No universal completion claim."""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;start=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def prose(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def main():
    e=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    assert len(pins)==e['pins_verified']==1283
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==e['head']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
    attempts=[];extra={g:0 for g in e['inherited_group_CPU']}
    for p in sorted(B.glob('run_*_result.json')):
        r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
        assert r['status']=='PASS' and r['termination'] is None and not c['error']
        assert r['new_finite_tests']==r['source_engine_calls']==r['old_semantic_rows_replayed']==0
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];extra[r['group']]+=charge
        attempts.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'child_CPU':r['child_CPU'],
            'controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,
            'allocated_child_cap':r['allocated_child_cap'],'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed']})
    assert {a['phase'] for a in attempts}=={'derivation','independent','witness','witness_independent','following','following_independent'}
    new=sum(extra.values());total=e['prior_uniform_CPU']+new
    groups={g:{'inherited_CPU':e['inherited_group_CPU'][g],'new_CPU':v,'combined_CPU':e['inherited_group_CPU'][g]+v,'cap':e['group_caps'][g]} for g,v in extra.items()}
    assert total<7200-5 and all(q['combined_CPU']<q['cap'] for q in groups.values())
    for f in B.glob('audit_*.py'):
        t=ast.parse(f.read_text());imports={n.module for n in ast.walk(t) if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(t) if isinstance(n,ast.Import) for a in n.names}
        assert imports<={'json','time','pathlib'},f
    assert read(B/'independent_audit.json')['requested_universal_completion_achieved'] is False
    assert read(B/'witness_independent_audit.json')['requested_universal_completion_achieved'] is False
    assert read(B/'following_independent_audit.json')['requested_completion_achieved'] is False
    out('resources_checkpoint.json',{'prior_uniform_CPU':e['prior_uniform_CPU'],'new_CPU_all_children_and_whole_controllers':new,
        'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
        'original_SE03_phase_groups':groups,'attempts':attempts,'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,
        'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
        'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'old_signature_ledger_unchanged':7195.203125,
        'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True})
    out('OWNER_RULES.json',{'kind':'partial source owner rules, not full ownership coverage',
        'fixed_common':'fE(C), unchanged','legacy_tail':'Gamma, Omega+, Xi and guarded receipts: unchanged auxiliary ordinals>=4',
        'negative_release_receipts':'unchanged fE(N) image units, disjoint from U',
        'RETURN':'still-unfunded aligned packet with finalD2 -> sole return A event bit1',
        'FOLLOWING':'still-unfunded aligned packet with finalD1 and positive selected next-macro surplus -> c-th next A event bit1, c=min(H,3)',
        'cross_RETURN_FOLLOWING_exclusion':'aux macro entry full q5 versus full q1',
        'candidate_leaf_pools':'reference only; no units spent or certified unused',
        'Psi_full_receipt':'standalone alternative from fE(C); not overlaid on prior guarded receipt',
        'all_original_demands_have_owners':False})
    out('PARTIAL_CERTIFICATE.json',{'status':'PARTIAL_RESULTS_ONLY_REQUESTED_COMPLETION_NOT_ACHIEVED',
        'all_unguarded_core11_packets_closed':False,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN',
        'new_proved_results':['DIRECT_RETURN_SURPLUS.md','FOLLOWING_SURPLUS_AND_RESIDUAL.md','LEAF_ACTIVATION_BARRIER.md','RETURN_BRANCH_SOURCE_WITNESS.md'],
        'aligned_subclass':'full H2/q5,1 with actual auxiliary H1/q4 then H1/q1, retained targets',
        'remaining_within_aligned_subclass':read(B/'following_audit.json')['residual_first_following_families'],
        'other_open':['other actual auxiliary packet patterns','multi-macro source donor termination','ownership against accompanying erased/cold demands','core10 misses','other cold singletons','zero/+1 interactions','repeated nonreturning claims'],
        'old_allocations_changed':False,'normalized_chart_potential_reused':False,'negative_source_cycle_certified':False,
        'inherited_pins_verified':1283,'head':e['head'],'Bank25':25,'R1_R4_preserved':True,
        'no_finite_tests':True,'independent_audit':'same-agent separate derivations; no external peer review or complete compiler formalization',
        'resource_checkpoint':'resources_checkpoint.json'})
    prose('CHECKPOINT.md',f'''# Step2 remains OPEN; this request is not completed

The user requested closure of all unguarded core11 H2/q5,1 donors and
universal Step2. That outcome has NOT been proved. No Step2 promotion,
unrestricted CD claim or certified negative source cycle is made.

New source-exact PARTIAL results:

1. DIRECT_RETURN_SURPLUS.md: in the aligned auxiliary H1/q4,H1/q1
subclass, final debt2 releases the return A event bit1. It pays the one
unmatched fifth full double, without a preparation guard. Global partial
ownership is proved against existing tail/common/released-demand receipts.

2. FOLLOWING_SURPLUS_AND_RESIDUAL.md: at final debt1, positive selected
surplus of the next auxiliary macro releases its newest selected bit.
H>=3 and H2/q<=2 guarantee this. Actual source fan/psi structure also
pays H1/q1. RETURN and FOLLOWING owner classes are mutually disjoint;
neither spends old tail units. The first-following zero-reserve residual
is exactly H1/q2/targetD1, H1/q3/targetD2, H2/q3/targetD0, H2/q4/targetD1.
This is an exhaustive LOCAL residual within this aligned subclass,
not four cases remaining in all of Step2.

3. LEAF_ACTIVATION_BARRIER.md: after each maximal-core packet, precisely
r-2 marks are core leaves. Before the next maximum-depth access, all
except possibly its target must be accessed. For six keys this forces
at least3 distinct genuine first visits (4 if the next target is the
old target/return). Their actual A events give distinct candidate pools,
but their exclusion from old owners is NOT proved; they are not spent.

4. RETURN_BRANCH_SOURCE_WITNESS.md: the debt2 branch is actually realized
by Psi=W6^- D1 D11 D1 K1 H6 for ALL arbitrary ordered Fi. Reuse exact
old identities, no old semantic replay. Full paired closure, A32,QF30,
QE24,D3=5,J3=1,N0, and a six-unit full receipt are proved. This family
also has preparation tails; no guard-failing or novel-domain claim.

The zero-reserve families still require a source-derived MULTI-MACRO
donor rule with global ownership against other claims and their own
erased/cold demands. Other auxiliary comparisons of H2/q5,1 packets,
core10 misses, cold singletons and their repeated interactions remain.
No later unit can be declared free merely because it is a candidate,
a carried bank bit, or a positive chart residual. Do not replace the
desired injection with its equivalent global cardinality inequality.

All1283 inherited pins verify. HEAD {e['head']}, branch coarse-double-branch,
tracked tree clean. R1-R4, Bank25=25, original two sorts/midpoints, signed
weights, h0, source semantics, private scopes and existing allocations
remain. Completed hit/pulse/auxiliary/M3 proofs are reused. No normalized
M3 debt is reinstated as a global chart-switching potential.

All6 new bounded local derivation/audit phases PASS at their stated
restricted scopes. INDEPENDENT_AUDIT.md explains the separate same-agent
source, ownership and scope audit; it is not external review or a whole
compiler formalization. There were no finite tests, source-engine calls,
old semantic row replays, solver runs or graph modifications.

CPU {total:.6f}/7200, remaining {7200-total:.6f} including reserve5.
Original groups symbolic {groups['symbolic']['combined_CPU']:.6f}/120,
independent {groups['independent']['combined_CPU']:.6f}/300. Every proof
child and whole controller is charged. No cap was reached, raised or
reset; budget exhaustion is not the explanation for the missing proof.
The2-million-query and other inherited limits remain unchanged.

PARTIAL_CERTIFICATE.json records incomplete coverage. OWNER_RULES.json
is a partial rule specification, not a declaration that every demand
has an owner. Step2, Step3 and Universal CD remain OPEN.
''')
    out('final_integrity.json',{'status':'PASS_PINS_RESOURCES_AND_HONEST_INCOMPLETE_STATUS','pins_verified':1283,
        'tracked_tree_clean':True,'head':e['head'],'Bank25':25,'R1_R4_preserved':True,'existing_allocations_unchanged':True,
        'new_phases':6,'new_phase_failures':0,'requested_completion_achieved':False,'metadata_CPU_excluded':time.process_time()-start})
    files=sorted(p for p in B.iterdir() if p.is_file())
    out('checkpoint_manifest.json',{'kind':'unfinished research checkpoint; NOT a Step2 seal',
        'files':[{'file':p.name,'sha256':sha(p)} for p in files],
        'inherited_pin_file':'dependency_pins.json','Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print(json.dumps({'status':'PARTIAL_CHECKPOINT_ONLY','requested_completion_achieved':False,
        'inherited_pins_verified':1283,'new_files_pinned':len(files),'cumulative_CPU':total,'Step2':'OPEN'}))
if __name__=='__main__':main()
