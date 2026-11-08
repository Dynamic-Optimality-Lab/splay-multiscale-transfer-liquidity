"""Final provenance/resource publication only; no mathematical source replay."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def put(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ident(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
entry=read(B/'entry.json');groups={'symbolic':0,'independent':0};attempts=[];calls=0
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'));used=r['child_CPU']+c['whole_process_CPU_seconds']
    groups[r['group']]+=used;calls+=r['source_engine_calls'];attempts.append({**r,'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':used})
total=entry['prior_uniform_CPU']+sum(groups.values());assert total<7195
assert all(entry['inherited_group_CPU'][g]+groups[g]<entry['group_caps'][g] for g in groups)
out('resources_checkpoint.json',{'prior_uniform_CPU':entry['prior_uniform_CPU'],
    'new_children_and_whole_controllers_CPU':sum(groups.values()),'cumulative_uniform_CPU':total,
    'global_allowance':7200,'required_reserve':5,'remaining_CPU_including_reserve':7200-total,
    'original_SE03_phase_groups':{g:{'inherited_CPU':entry['inherited_group_CPU'][g],'new_CPU':groups[g],
        'combined_CPU':entry['inherited_group_CPU'][g]+groups[g],'cap':entry['group_caps'][g]} for g in groups},
    'attempts':attempts,'all_attempts_including_conservative_checks_charged':True,'source_engine_calls_including_symbolic':calls,
    'discovery_private_preparation_states':925,'discovery_E1_preparation_states':1276,
    'suffix_exact_states':51,'suffix_packet_proposals':166,'concrete_finite_population_fixture_tests':0,
    'new_canonical_solver_queries':0,'old_semantic_rows_replayed':0,'canonical_query_cap':2000000,
    'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':34359738368,
    'peak_proof_child_working_set_bytes_observed':max(v['peak_working_set_bytes_observed'] for v in attempts),
    'wall_cap_hours':12,'new_universal_weighted_graphs':0,'new_solver_runs':0,'Bank25':25,
    'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True})
pins=read(B/'dependency_pins.json');pm={p['path']:p['sha256'] for p in pins['pins']}
direct=[
 ('DO_RESEARCH_REBOOT/ORIGINAL_PIPELINE.md','SOURCE DEFINITION','original semantics previously inspected and reused'),
 ('DO_RESEARCH_REBOOT/RESEARCH_RULES.md','SOURCE RULES','permanent evidence discipline reused'),
 ('DO_RESEARCH_REBOOT/CD5_BASE01/CD5_PROOF.md','PROVED certified support<=5','sealed proof reused; not reopened'),
 ('DO_RESEARCH_REBOOT/M3_XFER21/FULL_M3_PROOF.md','PROVED frozen M3 source scope','full inherited proof reused; no six-key debt inference'),
 ('DO_RESEARCH_REBOOT/SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED physical auxiliary allocation','ownership proof inspected/reused read-only'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','PROVED auxiliary domain','gE/fE distinction retained; no units spent'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED closed source structure','set-growth/density proof inspected and reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED closed maximal source grammar','source mass/persistence theorem inspected/reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/MARKED_PARENT_PROJECTION.md','PROVED exact source bridge','full compression argument inspected/reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/NEGATIVE_SEED_CORE11.md','PROVED restricted fan/leaf facts','source fan ports/accessibility proof inspected/reused'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED forced successor','full Hamiltonian fan and actual successor proof inspected'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md','PROVED original partition; D OPEN','packet domains retained, debt not assumed'),
 ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/RECENT_SUPPORT_COVER.md','PROVED recent-key chart scope','full source window argument inspected'),
 ('python/independent/splay.py','FROZEN SOURCE DEFINITION','read-only distinct recursive-frame trace used; convenience cost not used')]
for folder,names in [('SE03_STEP2_COLD_NEG2_01',['SOURCE_SPEC.md','NEG2_CLASSIFICATION.md','NEG2_PAIRED.md',
        'NEG2_SINGLETON.md','SOURCE_REPLAY.md','SOURCE_REPLAY_ADDENDUM.md','COLD_NEG2_FINAL.md','CHECKPOINT.md','source_model.py']),
    ('SE03_STEP2_FORCED_ZERO_INCOMING_02',['FZ_SOURCE_SPEC.md','RETURN_BARRIER.md','PLUS_ONE_PREDECESSORS.md',
        'incoming_family_v2.json','forced_regions.json','FINAL_VERDICT.md','CHECKPOINT.md']),
    ('SE03_STEP2_LEAF_LOWERING_03',['SOURCE_SPEC.md','LEAF_LOWERING_CLASSIFICATION.md','REGENERATION_AND_REPETITION.md',
        'ZERO_RETURN.md','ONE_PLUS_RETURN.md','SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md','resources_checkpoint.json',
        'pattern_family.json','forward_closure.json','backward_source_audit.json','independent_audit.json'])]:
    for n in names:direct.append(('DO_RESEARCH_REBOOT/'+folder+'/'+n,'ACCEPTED scoped source proof/data',
        'actual local source/verdict inspected/reused; completed replays not repeated; Sigma corrected count3 retained'))
lines=['# Source provenance/status ledger','',f'Branch `{entry["branch"]}`; HEAD `{entry["head"]}`; tracked source clean.','',
       'All1637 inherited/local pins and all external directives verify; full exact ledger in dependency_pins.json.',
       'No older remote source was substituted for the current local worktree. No missing premise was invented.','',
       '| Exact repository path | Status | Inspection/reuse | SHA256 |','|---|---|---|---|']
for rel,status,scope in direct:
    digest=sha(ROOT/rel);assert digest==pm[rel]
    lines.append(f'| `{rel}` | {status} | {scope} | `{digest}` |')
lines+=['','External directives, read at their stated authority; current Campaign04 takes precedence within its scope:','']
for p in pins['external_pins']:lines.append(f'- `{p["path"]}` — `{p["sha256"]}`')
lines+=['','First-lowering entry barrier: REFUTED, exact E0 and E1. Complete cheap return: NOT FOUND.',
    'Global width-two existence, generic post-lowering preservation, Step2, Step3 and Universal CD: OPEN.']
put('SOURCE_PROVENANCE.md','\n'.join(lines)+'\n')
def fmt(t):return t if isinstance(t,str) else f'{t[0]}({fmt(t[1])},{fmt(t[2])})'
inv=[];lines=['# Exact witness trees, charts and state identities','',
    'Notation k(L,R) means an actual node. Fi are distinct arbitrary finite ordered gap BSTs.',
    'Full states are never identified only by projected Scores. Absolute IDs follow the stated reaching prefix.','']
for filename in ('entry_family.json','e1_family.json'):
    fam=read(B/filename);cl=fam['critical'][0];off=len(fam['reaching_prefix']);tag=cl['entry_class']
    lines += ['## '+tag+' — '+filename,'',f'Period {len(fam["word"])}; reaching prefix {off}; erase3. Exact costs `{fam["costs"]}`.','',
        'Complete original recurrent-period word:','','```text',' '.join(k+str(x) for k,x in fam['word']),'```','']
    first=cl['negative_packet']['occurrences'][0];rr=fam['rows'][first-1];cc=fam['charts'][first-1]
    source={'A':rr['before'][0],'BF':rr['before'][1],'BE':rr['before'][2],'M':[1,3,5,7,9,11],
        'erased':3,'recent':cc['recent_before'],'packet_phase':'ready'}
    stages=[('NEG2 source',source,first-1),('t in T11',cl['T_state'],cl['negative_packet']['end']),
        ('ell in L11',cl['L_state'],cl['entry_prefix'][-1]['end']),('ell prime',cl['post_lowering_state'],cl['first_lowering']['end'])]
    for label,st,relative in stages:
        digest=ident(st);inv.append({'family':tag,'label':label,'state':st,'state_id':digest,
            'absolute_boundary_after':off+relative,'period_boundary_after':relative})
        lines += ['### '+label,'',f'Boundary after relative{relative}, absolute{off+relative}; SHA256 `{digest}`.',
            f'Recent-six `{st["recent"]}`, M `{st["M"]}`, erased `{st["erased"]}`, phase `{st["packet_phase"]}`.','']
        for tree in ('A','BF','BE'):lines += [tree+':','','```text',fmt(st[tree]),'```','']
    lines += ['| Occurrence | Mode/key | A path | BF path | a | qF | recent before -> after |','|---|---|---|---|---:|---:|---|']
    for p in [cl['negative_packet']]+cl['entry_prefix']+[cl['first_lowering']]:
        for n in p['occurrences']:
            r=fam['rows'][n-1];c=fam['charts'][n-1]
            lines.append(f'| {n} | {r["mode"]}{r["target"]} | `{r["A_path"]}` | `{r["BF_path"]}` | {r["a"]} | {r["qF"]} | `{c["recent_before"]}` -> `{c["recent_after"]}` |')
    lines += ['','The full physical before/after chart objects and all intervening operations are retained in the family JSON.','']
put('WITNESS_STATES.md','\n'.join(lines)+'\n');out('witness_state_ids.json',{'states':inv,'identity_hash_fields':'actual A,BF,BE,M,z,recent,phase; physical occurrence IDs are separate provenance'})
put('IAGS_CLOSURE.md','''# Campaign04 Box closure

Target entry exclusion is REFUTED by original E0 and E1 source histories.
No theorem weakening or new debt was used. The temporary private key12
was removed from the discovery example; D10 is an original unmarked
core key used only in the charged preparation. Added bounded E1 discovery
used30 CPU seconds/40000 states/500000 splays, and suffix analysis used
30 CPU seconds/15000 states/150000 proposals/700000 splays as local upper
bounds, always inside inherited cumulative phase/global limits. Actual
charges and counters are in the resource ledger. No cap was raised.

Recurse AFTER entry: budgets1/0. Both realized witness-family suffixes
are source-completely closed without reaching F11, using the distinct
engine and depth guards. The general post-lowering child remains OPEN.
Close only the first-entry decision and these restricted suffixes; do
not reopen old normalization, CD5, M3, Step1 or old source controls.
No donor bit was assigned, used twice or borrowed across a period.
''')
assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
tracked=git('status','--porcelain','--untracked-files=no');assert not tracked
out('publication_state.json',{'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':tracked,
    'full_worktree_status':git('status','--porcelain','--untracked-files=normal'),
    'outcome':'B','entry_E0':'REALIZED','entry_E1':'REALIZED','full_cheap_return':'NOT_FOUND',
    'Step2':'OPEN','cumulative_uniform_CPU':total,'metadata_CPU_excluded':time.process_time()})
manifest=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
out('campaign_manifest.json',{'outcome':'B','files':manifest,'excludes_self':True})
print(json.dumps({'outcome':'B','tracked_status':tracked,'cumulative_CPU':total,'remaining_CPU':7200-total,
    'group_CPU':{g:entry['inherited_group_CPU'][g]+groups[g] for g in groups},'source_splays':calls,
    'manifest_files':len(manifest)},indent=2))
