"""Append-only publication: actual resource sums, source hashes and witness terms."""
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
    'attempts':attempts,'all_inconclusive_search_and_controller_CPU_charged':True,'source_engine_calls_including_symbolic':calls,
    'fixed_word_finite_search_states':40000,'fixed_word_search_status':'PREDECLARED_LIMIT, inconclusive',
    'abstract_parent_map_controls':1296,'new_archived_boundary_predicate_checks':370,
    'old_semantic_rows_replayed':0,'new_canonical_solver_queries':0,'concrete_population_fixture_tests':0,
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':34359738368,'peak_proof_child_working_set_bytes_observed':max(q['peak_working_set_bytes_observed'] for q in attempts),
    'wall_cap_hours':12,'new_universal_weighted_graphs':0,'new_solver_runs':0,'Bank25':25,
    'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True})
pins=read(B/'dependency_pins.json');pm={p['path']:p['sha256'] for p in pins['pins']}
# Preserve the previous direct ledger, with its original scoped statuses,
# and append the exact Campaign04 leaves directly used in this campaign.
oldledger=(B.parent/'SE03_STEP2_FIRST_LOWERING_04/SOURCE_PROVENANCE.md').read_text(encoding='utf-8')
rows=[s for s in oldledger.splitlines() if s.startswith('| `')]
for row in rows:
    path=row.split('`')[1];digest=row.split('`')[-2];assert sha(ROOT/path)==digest==pm[path]
lines=['# Campaign05 direct source provenance and status','',f'Branch `{e["branch"]}`; HEAD `{e["head"]}`; tracked source clean.','',
    'All1706 inherited/local pins and external directives revalidate. Full ledger: dependency_pins.json.',
    'The inherited direct ledger below retains its scoped status/inspection attributes; source files are unchanged.','',
    '| Exact repository path | Status | Inspection/reuse | SHA256 |','|---|---|---|---|']+rows
new=[('SOURCE_SPEC.md','SOURCE DEFINITION'),('NEG2_EXIT_GEOMETRY.md','PROVED BF source normal forms'),
     ('FIRST_LOWERING_ENTRY.md','PROVED local conditions; entries realized'),('NEUTRAL_ZERO_PREFIX.md','PROVED E0 source prefix bound'),
     ('PLUS_ONE_INTERVENTION.md','PROVED E1 source realization'),('ENTRY_BARRIER.md','REFUTED universal entry exclusion'),
     ('POST_LOWERING_RESIDUAL.md','PROVED restricted witness suffixes; general OPEN'),('SOURCE_REPLAY.md','verified source methods/data'),
     ('FINAL_VERDICT.md','Outcome B entry realized; return OPEN'),('CHECKPOINT.md','scoped current inherited checkpoint'),
     ('entry_family.json','verified E0 source data'),('e1_family.json','verified E1 source data'),('independent_audit.json','verified separate-engine receipt')]
for n,status in new:
    rel='DO_RESEARCH_REBOOT/SE03_STEP2_FIRST_LOWERING_04/'+n;digest=sha(ROOT/rel);assert digest==pm[rel]
    lines.append(f'| `{rel}` | {status} | actual local artifact fully inspected/reused; completed replay not repeated | `{digest}` |')
lines+=['','External directives, actual original authorities; current Campaign05 governs the new work:','']
for p in pins['external_pins']:lines.append(f'- `{p["path"]}` — `{p["sha256"]}`')
lines+=['','No older remote snapshot substituted and no missing premise invented. Old E0/E1 and prior certificates remain',
    'sealed. New final-tail/shield proofs have restricted stated scopes. General suffix closure remains OPEN.']
put('SOURCE_PROVENANCE.md','\n'.join(lines)+'\n')
fam=read(B/'partial_family.json');cl=fam['critical'][0];offset=len(fam['reaching_prefix'])
def fmt(t):return t if isinstance(t,str) else f'{t[0]}({fmt(t[1])},{fmt(t[2])})'
text=['# Exact new post-loss witness and frontier','',
    'Fi are arbitrary independent finite ordered gap BSTs; k(L,R) retains actual nodes.','',
    f'Period96; actual reaching prefix96; erase3. Costs `{fam["costs"]}`.','',
    'Original recurrent word:','','```text',' '.join(k+str(x) for k,x in fam['word']),'```',''];states=[]
for label,key,n in [('T11','T_state',40),('first-loss source','entry_state',42),
                    ('P1 after3->2','post_first_loss',43),('RELAXED Fork41 frontier','frontier_state',44)]:
    st=cl[key];digest=ident(st);states.append({'label':label,'state':st,'state_id':digest,'period_after':n,'absolute_after':offset+n})
    text+=['## '+label,'',f'Boundary after relative{n}, absolute{offset+n}; SHA256 `{digest}`.',
        f'M `{st["M"]}`, erased `{st["erased"]}`, recent `{st["recent"]}`, phase `{st["packet_phase"]}`.','']
    for k in ('A','BF','BE'):text += [k+':','','```text',fmt(st[k]),'```','']
text+=['## Critical physical accesses','',
    '| Occurrence | Request | A path | BF path | a | qF | Cold |','|---|---|---|---|---:|---:|---|']
for n in range(40,46):
    r=fam['rows'][n-1];c=fam['charts'][n-1]
    text.append(f'| {n} | {r["mode"]}{r["target"]} | `{r["A_path"]}` | `{r["BF_path"]}` | {r["a"]} | {r["qF"]} | {c["cold"]} |')
text+=['','The relaxed frontier is NOT F11 or certified B0. The true cold key11 has A-depth8 and requires H>=4.']
put('WITNESS_STATES.md','\n'.join(text)+'\n');out('witness_state_ids.json',{'states':states,'full_state_identity':True})
put('IAGS_CLOSURE.md','''# Campaign05 Box closure

Outcome D: universal parent suffix target OPEN. Close only the symbolic
normal-form/frontier/last-tail/placement/shield restrictions and the new
96-operation source family and its two-cell zero-suffix exclusion.
The bounded fixed complete-return preparation search stopped at40000
states, within30CPU/500000-splay bounds. Its failure is inconclusive,
not the proof of the separate turnaround theorem. All CPU is charged.
No failed normalization or first-entry search was restarted. The new
3->2 P1 start only certifies the post-lowering source class needed here.
The relaxed cold-B frontier does not assert F11/B0 membership. Next
recurse into E1 terminal A exposure with full regenerated provenance.
All R1-R4, Bank25, allocations, frozen source and caps remain unchanged.
''')
assert git('branch','--show-current')==e['branch'] and git('rev-parse','HEAD')==e['head']
tracked=git('status','--porcelain','--untracked-files=no');assert not tracked
out('publication_state.json',{'branch':e['branch'],'HEAD':e['head'],'tracked_status':tracked,
    'full_worktree_status':git('status','--porcelain','--untracked-files=normal'),
    'outcome':'D','general_E1_zero':'OPEN','general_E0_zero':'OPEN','general_E0_plus_one':'OPEN',
    'complete_cheap_return':False,'Step2':'OPEN','cumulative_uniform_CPU':total,'metadata_CPU_excluded':time.process_time()})
manifest=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
out('campaign_manifest.json',{'outcome':'D','files':manifest,'excludes_self':True})
print(json.dumps({'outcome':'D','tracked_status':tracked,'cumulative_CPU':total,'remaining_CPU':7200-total,
    'group_CPU':{g:e['inherited_group_CPU'][g]+groups[g] for g in groups},'source_splays':calls,
    'manifest_files':len(manifest)},indent=2))
