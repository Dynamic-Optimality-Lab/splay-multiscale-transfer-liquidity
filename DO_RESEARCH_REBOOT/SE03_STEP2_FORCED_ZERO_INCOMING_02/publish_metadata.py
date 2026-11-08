"""Provenance/resource publication only; no mathematical engine execution."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def put(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
entry=json.loads((B/'entry.json').read_text());attempts=[];sums={'symbolic':0,'independent':0}
calls=0
for p in sorted(B.glob('run_*_result.json')):
    r=json.loads(p.read_text());c=json.loads((B/('controller_'+r['phase']+'_exit.json')).read_text())
    used=r['child_CPU']+c['whole_process_CPU_seconds'];sums[r['group']]+=used;calls+=r['source_engine_calls']
    attempts.append({**r,'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':used})
total=entry['prior_uniform_CPU']+sum(sums.values())
assert total<7195 and all(entry['inherited_group_CPU'][g]+sums[g]<entry['group_caps'][g] for g in sums)
out('resources_checkpoint.json',{'prior_uniform_CPU':entry['prior_uniform_CPU'],
    'new_children_plus_whole_controllers_CPU':sum(sums.values()),'cumulative_uniform_CPU':total,
    'global_allowance':7200,'required_reserve':5,'remaining_CPU_including_reserve':7200-total,
    'original_SE03_phase_groups':{g:{'inherited_CPU':entry['inherited_group_CPU'][g],'new_CPU':sums[g],
        'combined_CPU':entry['inherited_group_CPU'][g]+sums[g],'cap':entry['group_caps'][g]} for g in sums},
    'attempts':attempts,'failed_drafts_included':True,'source_engine_calls_including_failed_and_symbolic':calls,
    'bounded_search_exact_states':12,'bounded_search_packet_proposals':20,
    'concrete_finite_BST_fixture_tests':0,'symbolic_source_family_replays':'new75-operation family and mirror, two engines; failed draft charged',
    'new_canonical_solver_queries':0,'old_semantic_rows_replayed':0,'canonical_query_cap':2000000,
    'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,'new_frozen_graphs_or_solver_runs':0,
    'memory_cap_bytes':34359738368,'wall_cap_hours':12,
    'peak_proof_child_working_set_bytes_observed':max(r['peak_working_set_bytes_observed'] for r in attempts),
    'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True,'Bank25':25})
direct=[
 ('DO_RESEARCH_REBOOT/ORIGINAL_PIPELINE.md','source definition','previously inspected/reused exact semantics'),
 ('DO_RESEARCH_REBOOT/RESEARCH_RULES.md','permanent proof discipline','previously inspected/reused'),
 ('DO_RESEARCH_REBOOT/CD5_BASE01/CD5_PROOF.md','PROVED at <=5 support','sealed proof reused, not replayed'),
 ('DO_RESEARCH_REBOOT/M3_XFER21/FULL_M3_PROOF.md','PROVED at frozen M3 source scope','complete inherited proof inspected/reused; not extended to6'),
 ('DO_RESEARCH_REBOOT/SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED auxiliary allocation','source allocation inspected/reused unchanged'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','PROVED restricted auxiliary source domain','full proof inspected; gE not equated with fE'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/NINE_SCORE_SOURCE_BRIDGE.md','PROVED fixed nine-Score bridge','full source proof inspected; no changing-chart extension'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/HAMILTONIAN_DEBT_NORMALIZATION.md','PROVED fixed-chart; REFUTED global extension','definition inspected; no rescue attempted'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED actual closed sources','set inclusion/density proof inspected'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED actual closed maximal sources','full persistence/mass/source grammar inspected'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/MARKED_PARENT_PROJECTION.md','PROVED exact source projection','full compression proof inspected; parent notation retains full state'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/NEGATIVE_SEED_CORE11.md','PROVED restricted negative-source lemmas','full fan accessibility and leaf-floor proofs inspected'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/B_ONLY_SOURCE_OBSTRUCTION.md','PROVED B-only obstruction','full source argument inspected; not mistaken for negative source cycle'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED source successor','full fan and disjoint-packet proof inspected'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md','PROVED partition; potential OPEN','complete partition source proof inspected'),
 ('python/independent/splay.py','frozen source definition','independent trace used read-only; pair convenience costs not used'),
]
for n in ['SOURCE_SPEC.md','NEG2_CLASSIFICATION.md','NEG2_PAIRED.md','NEG2_SINGLETON.md','SOURCE_REPLAY.md',
          'SOURCE_REPLAY_ADDENDUM.md','COLD_NEG2_FINAL.md','CHECKPOINT.md','symbolic_replay.json',
          'debt_v3_audit.json','source_proof_audit.json','resources_checkpoint.json','source_model.py']:
    direct.append(('DO_RESEARCH_REBOOT/SE03_STEP2_COLD_NEG2_01/'+n,
        'ACCEPTED Campaign01 result/data/definition','full relevant content inspected; completed control replays reused'))
pins={p['path']:p['sha256'] for p in json.loads((B/'dependency_pins.json').read_text())['pins']}
lines=['# Direct source provenance\n',f'Branch `{git("branch","--show-current")}`; HEAD `{git("rev-parse","HEAD")}`.\n',
       'All1522 pins revalidated in dependency_revalidation.json; no mismatches.\n',
       '| Exact repository path | Status | Inspection/reuse | SHA256 |','|---|---|---|---|']
for rel,status,inspection in direct:
    digest=sha(ROOT/rel)
    assert rel in pins and digest==pins[rel]
    lines.append(f'| `{rel}` | {status} | {inspection} | `{digest}` |')
lines+=['','External IAGS and immutable R1-R4 were read at their original attachment;',
        'the current Campaign02 request takes precedence over historical hard-stop/no-test',
        'instructions, within its explicit Gate F scope. External directive hashes are',
        'recorded in entry verification/USER_REQUEST.json. No source theorem was supplied',
        'by a remote snapshot or invented missing artifact.','',
        'The all-cold-chart potential, the universal incoming barrier and Step2 remain OPEN.']
put('SOURCE_PROVENANCE.md','\n'.join(lines)+'\n')
tracked=git('status','--porcelain','--untracked-files=no')
assert tracked==entry['tracked_status']==''
assert git('rev-parse','HEAD')==entry['head'] and git('branch','--show-current')==entry['branch']
out('publication_state.json',{'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':tracked,
    'full_worktree_status':git('status','--porcelain','--untracked-files=normal'),
    'outcome':'D','historical_pins_revalidated':1522,'scope':'partial universal source lemmas; incoming barrier OPEN',
    'cumulative_uniform_CPU':total,'metadata_CPU_excluded':time.process_time()})
manifest=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
out('campaign_manifest.json',{'outcome':'D','files':manifest,'excludes_self':True})
print(json.dumps({'outcome':'D','tracked_status':tracked,'cumulative_uniform_CPU':total,
    'remaining_CPU':7200-total,'phase_groups':{g:entry['inherited_group_CPU'][g]+sums[g] for g in sums},
    'new_source_engine_calls':calls,'manifest_files':len(manifest)},indent=2))
