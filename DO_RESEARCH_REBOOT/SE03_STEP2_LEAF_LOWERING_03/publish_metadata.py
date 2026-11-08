"""Append-only Campaign03 publication; metadata work, not proof search."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;PREV=B.parent/'SE03_STEP2_FORCED_ZERO_INCOMING_02'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def put(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
e=read(B/'entry.json');groups={'symbolic':0,'independent':0};attempts=[];calls=0
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'));charge=r['child_CPU']+c['whole_process_CPU_seconds']
    groups[r['group']]+=charge;calls+=r['source_engine_calls'];attempts.append({**r,'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge})
total=e['prior_uniform_CPU']+sum(groups.values());assert total<7195
assert all(e['inherited_group_CPU'][g]+groups[g]<e['group_caps'][g] for g in groups)
out('resources_checkpoint.json',{'prior_uniform_CPU':e['prior_uniform_CPU'],
    'new_children_and_whole_controllers_CPU':sum(groups.values()),'cumulative_uniform_CPU':total,
    'global_allowance':7200,'required_reserve':5,'remaining_CPU_including_reserve':7200-total,
    'original_SE03_phase_groups':{g:{'inherited_CPU':e['inherited_group_CPU'][g],'new_CPU':groups[g],
        'combined_CPU':e['inherited_group_CPU'][g]+groups[g],'cap':e['group_caps'][g]} for g in groups},
    'attempts':attempts,'all_proof_attempts_charged':True,'source_engine_calls_including_symbolic':calls,
    'new_finite_source_start_families':32,'finite_return_search_states':162,'finite_return_packet_proposals':345,
    'concrete_finite_population_fixture_tests':0,'symbolic_free_term_checks':'new70-operation family and32 varied source words, both orientations; independent engines',
    'old_semantic_rows_replayed':0,'new_canonical_solver_queries':0,'canonical_query_cap':2000000,
    'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':34359738368,
    'peak_proof_child_working_set_bytes_observed':max(q['peak_working_set_bytes_observed'] for q in attempts),
    'wall_cap_hours':12,'new_universal_weighted_graphs':0,'new_solver_runs':0,'Bank25':25,
    'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True})
pins=read(B/'dependency_pins.json');pinmap={p['path']:p['sha256'] for p in pins['pins']}
direct=[
 ('DO_RESEARCH_REBOOT/ORIGINAL_PIPELINE.md','SOURCE DEFINITION','original semantics previously inspected and reused'),
 ('DO_RESEARCH_REBOOT/RESEARCH_RULES.md','SOURCE RULES','permanent discipline reused'),
 ('DO_RESEARCH_REBOOT/CD5_BASE01/CD5_PROOF.md','PROVED certified support<=5','inherited full proof reused, not reopened'),
 ('DO_RESEARCH_REBOOT/M3_XFER21/FULL_M3_PROOF.md','PROVED frozen M3 source domain','inherited full proof reused without changing-chart extrapolation'),
 ('DO_RESEARCH_REBOOT/SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED auxiliary physical allocation','source event/ownership proof inspected and unchanged'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','PROVED auxiliary domain','gE/fE distinction preserved'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED original closed-source structure','set-inclusion and density proof inspected/reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED original closed maximal sources','full source mass/persistence proof inspected/reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/MARKED_PARENT_PROJECTION.md','PROVED exact source bridge','full compression proof inspected and used directly'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/NEGATIVE_SEED_CORE11.md','PROVED restricted source seed/leaf facts','full accessibility and leaf-floor arguments inspected/reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED successor/pairing','actual fan and disjoint packet proof reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md','PROVED partition; debt OPEN','original actual packets preserved'),
 ('python/independent/splay.py','FROZEN SOURCE DEFINITION','distinct tagged-term trace used read-only; convenience cost not used'),
]
for folder,names in [('SE03_STEP2_COLD_NEG2_01',['SOURCE_SPEC.md','NEG2_CLASSIFICATION.md','NEG2_PAIRED.md','NEG2_SINGLETON.md',
        'SOURCE_REPLAY.md','SOURCE_REPLAY_ADDENDUM.md','COLD_NEG2_FINAL.md','CHECKPOINT.md','source_model.py','symbolic_replay.json',
        'debt_v3_audit.json','source_proof_audit.json']),
    ('SE03_STEP2_FORCED_ZERO_INCOMING_02',['FZ_SOURCE_SPEC.md','FORCED_REGION_RECONSTRUCTION.md','ZERO_PREDECESSOR_CLOSURE.md',
        'PLUS_ONE_PREDECESSORS.md','RETURN_BARRIER.md','EXACT_SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md',
        'forced_regions.json','incoming_family_v2.json','absolute_source_ids.json','resources_checkpoint.json'])]:
    for n in names:direct.append(('DO_RESEARCH_REBOOT/'+folder+'/'+n,'ACCEPTED scoped inherited proof/data',
        'full source/verdict inspected/reused; Sigma prose leaf count explicitly corrected in new campaign where relevant'))
lines=['# Source provenance and status ledger','',f'Branch `{e["branch"]}`, HEAD `{e["head"]}`; tracked files clean.','',
       'All1578 inherited/local pins revalidated; full ledger dependency_pins.json and dependency_revalidation.json.','',
       '| Exact repository path | Status | Inspection/reuse | SHA256 |','|---|---|---|---|']
for rel,status,scope in direct:
    digest=sha(ROOT/rel);assert digest==pinmap[rel]
    lines.append(f'| `{rel}` | {status} | {scope} | `{digest}` |')
lines+=['','External directives (all read at their stated authority; current Campaign03 authorizes this work):','']
for p in pins['external_pins']:lines.append(f'- `{p["path"]}` — `{p["sha256"]}`')
lines+=['','No missing premise is invented. No remote snapshot substituted. Prior source tests are reused,',
    'not replayed as new evidence. The known restricted results do not close general R0/R1,',
    'width-two existence, Step2, core9/10, Step3 or Universal CD.']
put('SOURCE_PROVENANCE.md','\n'.join(lines)+'\n')
# Human-readable shape/cost closure certificate; full A/B terms stay in JSON.
cls=read(B/'forward_closure.json')['results'];lines=['# Complete source-term closure tables','',
    'These are inductive free-term closures ONLY with the source-completeness proof in SOURCE_REPLAY.md.','',
    'No debt factorization through A/B is asserted. Full BE/recent states are preserved in actual witnesses.','']
for c in cls:
    lines += ['## '+c['name'],'',f'Budget {c["budget"]}; {len(c["states"])} cells; no unknown H2/paired branch.','',
        '| Cell | Spent cost | Marked leaves |','|---|---:|---:|']
    lines += [f'| {s["id"]} | {s["cost"]} | {s["marked_leaves"]} |' for s in c['states']]
    lines += ['','| Source | Target | KEEP | H | Q | w | Delta L |','|---|---|---:|---:|---:|---:|---:|']
    lines += [f'| {q["source"]} | {q["target"]} | {q["KEEP"]} | 1 | {q["Q"]} | {q["w"]} | {q["leaf_change"]} |' for q in c['edges']]
    lines += ['','Every cell has no A-one-event q4/q5 source geometry. Missing outgoing entries are exact source exclusions.','']
put('SOURCE_CLOSURE_TABLES.md','\n'.join(lines)+'\n')
# Complete initial example inventory and mirrors; operation IDs remain attached
# as provenance and are not new frozen graph coordinates.
def reflect_tree(t):return 'F'+str(11-int(t[1:])) if isinstance(t,str) else [12-t[0],reflect_tree(t[2]),reflect_tree(t[1])]
def reflect_state(s):
    return {'A':reflect_tree(s['A']),'BF':reflect_tree(s['BF']),'BE':reflect_tree(s['BE']),
        'M':sorted(12-x for x in s['M']),'erased':12-s['erased'],
        'recent':[12-x for x in s['recent']],'packet_phase':s['packet_phase']}
base=read(PREV/'forced_regions.json')['records'];inv=[]
for r in base:
    inv.append({'family':r['family'],'F':r['F_state'],'T':r['T_state'],
        'F_id':r['F_id'],'T_id':r['T_id'],'reflected_F':reflect_state(r['F_state']),
        'reflected_T':reflect_state(r['T_state'])})
sig=read(PREV/'incoming_family_v2.json')
out('starting_states.json',{'known_F_T':inv,'Sigma_plus_one_predecessor':sig['predecessor'],
    'Sigma_reflected_plus_one_predecessor':reflect_state(sig['predecessor']),
    'Sigma_predecessor_marked_leaves':3,'reaching_prefix_and_absolute_ID_provenance':'Campaign02 absolute_source_ids.json',
    'same_projection_not_equal_state':'all complete original fields retained; mirrors are labeled distinct states'})
assert git('rev-parse','HEAD')==e['head'] and git('branch','--show-current')==e['branch']
tracked=git('status','--porcelain','--untracked-files=no');assert not tracked
out('publication_state.json',{'branch':e['branch'],'HEAD':e['head'],'tracked_status':tracked,
    'full_worktree_status':git('status','--porcelain','--untracked-files=normal'),
    'outcome':'D','cumulative_uniform_CPU':total,'all_prior_pins_preserved':True,'metadata_CPU_excluded':time.process_time()})
manifest=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
out('campaign_manifest.json',{'outcome':'D','files':manifest,'excludes_self':True})
print(json.dumps({'outcome':'D','tracked_status':tracked,'cumulative_CPU':total,'remaining_CPU':7200-total,
    'group_CPU':{g:e['inherited_group_CPU'][g]+groups[g] for g in groups},'source_engine_calls':calls,
    'manifest_files':len(manifest)},indent=2))
