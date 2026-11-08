"""Campaign09 provenance/publication metadata, not a new proof experiment."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:
        if isinstance(v,str):f.write(v)
        else:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def before():
    ind=read('independent_audit.json');adv=read('adversarial_audit.json');pins=read('dependency_pins.json')
    by={v['path']:v['sha256'] for v in pins['pins']}
    paths=[
        ('ORIGINAL_PIPELINE.md','SOURCE DEFINITION; actual costs/Pair Access inspected'),
        ('RESEARCH_RULES.md','SOURCE RULES; IAGS and status discipline inspected'),
        ('CD5_BASE01/CD5_PROOF.md','SEALED original CD5 scope; prior proof inspection reused, not reopened'),
        ('M3_XFER21/FULL_M3_PROOF.md','SEALED M3; prior proof inspection reused; not extended to chart switches'),
        ('SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED auxiliary allocation; source funding/cut inspected'),
        ('SE03_STEP1_FUND01/SIGNED_CANCELLATION.md','PROVED signed cancellation; physical identities inspected'),
        ('SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','PROVED refined reservation; gE/fE distinction inspected'),
        ('SE03_STEP2_REPAY02/COLD_EXCHANGE_IDENTITY.md','PROVED identity only; -1 correction inspected'),
        ('SE03_STEP2_REPAY01/PACKET_PERIOD_TRANSPORT.md','PROVED conditional allocation transport; both IDs retained'),
        ('SE03_STEP2_REPAY01/IMPROVED_FULL_DEBT_TARGET.md','Conditional exchange proof inspected; full allocator still OPEN'),
        ('SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md','PROVED partition; proposed global range-two debt OPEN'),
        ('SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED source set-growth/density/alternation; proof inspected'),
        ('SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED source all-SS/no-zig; proof inspected'),
        ('SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED actual q5/q1 successor, full source proof inspected'),
        ('SE03_STEP2_COLD_NEG2_01/NEG2_CLASSIFICATION.md','PROVED exhaustive source price classification; inspected'),
        ('SE03_STEP2_FORCED_ZERO_INCOMING_02/RETURN_BARRIER.md','PROVED marked-parent compression/leaf rule; inherited proof reused'),
        ('SE03_STEP2_POST_LOWERING_05/POST_LOWERING_NORMAL_FORM.md','PROVED source recency/interfaces; inherited proof reused'),
        ('SE03_STEP2_POST_LOWERING_05/FORCED_ZERO_BACKWARD_FRONTIER.md','PROVED J2/K2/final-zero source rule; inspected and independently recomputed'),
        ('SE03_STEP2_TERMINAL_PAIR_06/FULL_PROOF.md','PROVED TP-DEPTH3; inspected and independently recomputed'),
        ('SE03_STEP2_TERMINAL_PAIR_06/saturation3.json','ACCEPTED06 version; independently recomputed, invalid saturation excluded'),
        ('SE03_STEP2_FINAL_PLUS_ONE_07/FULL_PROOF.md','PROVED FINAL-PLUS1; independently recomputed'),
        ('SE03_STEP2_FINAL_PLUS_ONE_07/independent_audit2.json','ACCEPTED07 semantic checker; recomputed, initial raw-count check superseded'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/FULL_PROOF.md','PROVED P1Z-RETURN; inspected and independently recomputed'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/final_zero_inverse.json','ACCEPTED08 complete new source grammar; recomputed'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/terminal_seeds.json','ACCEPTED08 terminal language; recomputed'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/zero_closure.json','ACCEPTED08 closed necessary language; recomputed'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/independent_audit.json','ACCEPTED08 distinct-engine audit; recomputed'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/seal_audit.json','ACCEPTED08 local seal; source inspected, hash verified'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/campaign_manifest.json','ACCEPTED08 local provenance manifest; every file pinned'),
        ('SE03_STEP2_COLD_NEG2_01/source_model.py','IMMUTABLE primary engine; ordinary traces only')]
    rows=['# Exact local source provenance','',
        'All2036 inherited/local pins and the external original IAGS/current directives',
        'verified at entry; final seal revalidates every byte. No remote snapshot was',
        'substituted for the current local worktree. Complete transitive paths/hashes',
        'are in dependency_pins.json. Every direct proof below was inspected in this',
        'campaign or inherited with a recorded prior proof inspection as stated.','',
        '| Exact repository path | Status and verification attribute | SHA256 |','|---|---|---|']
    for rel,status in paths:
        path='DO_RESEARCH_REBOOT/'+rel;assert path in by,path
        rows.append('|'+path+'|'+status+'|'+by[path]+'|')
    path='python/independent/splay.py';assert path in by
    rows.append('|'+path+'|IMMUTABLE distinct checker engine; original trace inspected|'+by[path]+'|')
    rows+=['','External pinned sources:','']
    for v in pins['external_pins']:rows.append('- '+v['path']+' — SHA256 '+v['sha256'])
    rows+=['','No missing/conditional prerequisite is used inside CORE11-RETURN.',
        'The old changing-chart Hamiltonian normalization stays REFUTED. The invalid',
        '06 saturation.json and superseded07 initial raw-count check remain preserved',
        'but never serve as premises. No proposed global debt or cardinality inequality',
        'is used circularly. All full physical funding and support descent claims stay OPEN.','']
    out('SOURCE_PROVENANCE.md','\n'.join(rows))
    rows=['# Complete Campaign09 source case ledger','',
        'CORE11_CLASS_LEDGER.md is the disjoint return-word ledger. Every row below',
        'has universal ordered private BST slots, not a population bound.','',
        '| Source operation/packet | Coverage |','|---|---|',
        '|Cold NEG2-S H1/Q4|Actual shallow A event, cold BF leaf, target shape(4,4)|',
        '|Cold NEG2-P H2/Q6|Both H1 macros,32 BF initial contexts,62 actual successor sectors, target(4,1)|',
        '|Zero H1/Q2|Every six-schema A inverse, actual BF path/recent inversion;2688 new incidences|',
        '|Zero H2/Q4|Output>=4 leaves, cannot enter new paired L1/L2 language; q4 scopes verified separately|',
        '|Zero paired H3/Q6|Both splits(1,2)/(2,1), all actual successors; output(4,1), cannot enter new language|',
        '|+1 H1/Q1|Full event-at-KEEP/DELETE normal form, aliases retained;62 new combined sectors|',
        '|+1 H2/Q3 one positive operation|Actual two events at target depth3/4; excluded from relevant terminal interface by BF degree|',
        '|+1 H2/Q3 two operations|DELETE helper then terminal target, each one event; arbitrary helper excluded by SAME BF argument|',
        '|H0/Q0 identity cuts|Projected identity only; BE action/absolute occurrence preserved in original fiber|',
        '|Nongenuine/root KEEPs|All actual A work remains in natural macro; BE not equated with BF chart|',
        '|Arbitrary private labels|Literal Score cells, ordered injective role matching, arbitrary free interval BSTs|',
        '|Source phase/cyclic seam|Whole actual packets, shared q5/q1 midpoint; actual closed history retained|','',
        '| New paired successor alias | Compositions |','|---|---:|']
    for k,v in adv['aliases'].items():rows.append('|'+k+'|'+str(v)+'|')
    rows+=['','| Root-word order/equality profile g,y,x,v | BF compositions |','|---|---:|']
    for r in adv['rank_profiles']:rows.append('|'+','.join(map(str,r['root_word']))+'|'+str(r['BF_cases'])+'|')
    rows+=['','Every profile and its reflection is retained. The A word may have three',
        'distinct labels (successor equals an earlier root); requiring four would',
        'omit48 actual necessary compositions. These aliases were covered BEFORE',
        'closure construction and independently recomputed.','',
        '| Position in g->y->x->v | Actual A event kind | Symbolic incidences |','|---|---|---:|']
    for r in adv['three_event_A_kinds']:rows.append('|'+str(r['position'])+'|'+r['kind']+'|'+str(r['incidences'])+'|')
    rows+=['','Both zig directions are considered in the source calculus; all private',
        'order cases are quantified. An absent kind in this table is a derived empty',
        'composed sector, never an omitted inverse schema. Exact lower-level A/BF',
        'rotation words, reflection and counts are in adversarial_audit.json.','',
        '| Marked leaves | Marked-root degree | New closed frames |','|---|---|---:|']
    for r in ind['state_shapes']:rows.append(f"|{r['leaves']}|{r['marked_root_degree']}|{r['frames']}|")
    rows+=['','The4858 new frames and2688 inverse incidences cover arbitrary finite',
        'zero prefixes; no q4 certificate is substituted for the paired source.',
        'Both genuine cold NEG2 target classes have L4 and are excluded.','']
    out('CASE_LEDGER.md','\n'.join(rows))
    ctrl=read('source_control_replay.json')
    rows=['# Source controls and replay limitations','',
        'No new finite-population experiment was used for the proof. The required',
        'accepted historical controls were replayed unchanged, with both engines,',
        'including their full reflected histories. These are regressions, not the',
        'universal source-coverage argument. source_control_replay.json is the',
        'new09 receipt; exact source words/initial trees/gap terms/period rows remain',
        'in the pinned original artifacts listed below.','',
        '| Family | Reflected | Period operations | A | QF | QE | 2A-QF | Closed A/BF/BE/recent/chart |','|---|---|---:|---:|---:|---:|---:|---|']
    for r in ctrl['families']:
        rows.append('|'+r['name']+'|'+str(r['reflected'])+'|'+str(r['original_period_operations'])+'|'+str(r['A'])+'|'+str(r['QF'])+'|'+str(r['QE'])+'|'+str(r['original_CD_slack'])+'|'+str(r['A_BF_BE_recent_and_chart_closure'])+'|')
    rows+=['','Exact immutable control sources:','',
        '- SE03_STEP2_COLD_NEG2_01/symbolic_replay.json: Omega+, Sigma, modified Gamma, exact operations/trees/rows.',
        '- SE03_STEP2_FORCED_ZERO_INCOMING_02/incoming_family_v2.json: corrected Sigma predecessor with THREE leaves.',
        '- SE03_STEP2_LEAF_LOWERING_03/pattern_family.json: zero4->3->2->3 regeneration.',
        '- SE03_STEP2_FIRST_LOWERING_04/entry_family.json: E0 68-operation history.',
        '- SE03_STEP2_FIRST_LOWERING_04/e1_family.json: E1 90-operation history.',
        '- SE03_STEP2_POST_LOWERING_05/partial_family.json:96-operation B-geometry history.',
        '- SE03_STEP2_FINAL_PLUS_ONE_07/delete_event_control.json:76-operation DELETE-event variant, A93/QF42/QE32.',
        '',
        'All paths above are under DO_RESEARCH_REBOOT/. dependency_pins.json records',
        'their exact hashes. audit_controls.py retains each original operation kind,',
        'packet occurrence set, physical costs and BE action, checking dual-engine',
        'state equality at every boundary and exact final period closure. Its new',
        'receipt has18 cases and1234 period rows; all original CD slacks are positive.',
        'New H1 normal-form predicates verify event-at-KEEP and event-at-DELETE where',
        'present. Missing H2 occurrences in these controls are NOT evidence of a',
        'universal exclusion; that is proved directly by marked BF degree.','',
        'New09 symbolic paired controls: all32 BF paths,62 actual successors, both',
        'future A events, both mirrored orientations, two successor chart misses,',
        'all62 incoming+1 compositions and aliases, all4858 reflected closure records.',
        'These terms retain arbitrary free BST slots and are covered by universal',
        'source lifting, not an exhaustion of concrete private populations. There',
        'is no new alleged closed witness, source counterexample or negative cycle.',
        'No donor is transported or allocated in a regression or in this theorem.','']
    out('SOURCE_REPLAY.md','\n'.join(rows))
    out('budget_product_certificate.json',{'status':'COMPLETE_NECESSARY_PRODUCT_AND_SEPARATION',
        'budget1':{'artifact':'paired_destination_seeds.json','sha256':sha(B/'paired_destination_seeds.json'),
            'frames':4464,'marked_leaves':1,'zero_predecessors':'none genuine','positive_consumption':'H1Q1 only'},
        'budget0':{'seed_artifact':'terminal_seeds.json','seed_sha256':sha(B/'terminal_seeds.json'),
            'closure_artifact':'zero_closure.json','closure_sha256':sha(B/'zero_closure.json'),
            'frames':4858,'zero_inverse_incidences':2688,'marked_leaves':2},
        'target_shapes':[[4,4],[4,1]],'target_intersection':False,
        'coverage':'one-way necessary source projection and arbitrary-slot lifting; no realization claim',
        'independent_audit_sha256':sha(B/'independent_audit.json')})
    out('research_status_ledger.json',{'CORE11_RETURN':'PROVED_UNIVERSAL_DECLARED_CORE11_SOURCE_SCOPE',
        'q4_return_assembly':'PROVED','paired_return':'PROVED',
        'accepted06_07_08':'PROVED_SCOPES_UNCHANGED_RECOMPUTED',
        'CD5_M3_Step1':'SEALED_ORIGINAL_SCOPES_UNCHANGED',
        'old_changing_chart_normalized_debt':'REFUTED_UNCHANGED',
        'global_width_two_debt':'OPEN','physical_full_allocation':'OPEN',
        'core9_core10_compatibility':'OPEN','CD6':'OPEN','Step2':'OPEN','Step3':'OPEN',
        'Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'new_finite_tests':0,'formal_assistant':False,'external_peer_review':False})
    print(json.dumps({'status':'PUBLICATION_METADATA_READY','CPU_excluded_by_inherited_metadata_convention':time.process_time()}))
def after():
    e=read('entry.json');total=e['prior_uniform_CPU'];group=dict(e['inherited_group_CPU']);phases=[]
    for p in sorted(B.glob('run_*_result.json')):
        v=json.loads(p.read_text());c=read('controller_'+v['phase']+'_exit.json')
        assert v['status']=='PASS' and not c['error']
        charge=v['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;group[v['group']]+=charge
        phases.append({'phase':v['phase'],'group':v['group'],'whole_child_CPU':v['child_CPU'],
            'whole_controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,
            'source_engine_calls':v['source_engine_calls'],'peak_working_set':v['peak_working_set_bytes_observed']})
    assert total<7195 and all(group[g]<e['group_caps'][g] for g in group)
    assert read('seal_audit.json')['terminal_outcome']=='A'
    resources={'status':'PASS_ALL_INHERITED_CAPS_PRESERVED','prior_CPU':e['prior_uniform_CPU'],
        'cumulative_CPU':total,'ceiling':7200,'required_reserve':5,'remaining_CPU':7200-total,
        'available_before_reserve':7195-total,'cumulative_group_CPU':group,'group_caps':e['group_caps'],
        'remaining_group_CPU':{g:e['group_caps'][g]-group[g] for g in group},'phases':phases,
        'source_engine_calls_this_campaign':sum(v['source_engine_calls'] for v in phases),
        'query_cap':2000000,'live_cap':2000000,'DAG_cap':4000000,'edge_cap':5000000,
        'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'no_reset':True,'new_finite_tests':0,
        'metadata_convention':'entry/provenance/publication excluded as inherited; all proof/replay/seal child and controller CPU charged',
        'metadata_publisher_CPU_this_invocation_excluded':time.process_time()}
    out('resources_checkpoint.json',resources)
    def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('branch','--show-current')==e['branch'] and git('rev-parse','HEAD')==e['head']
    assert not git('status','--porcelain','--untracked-files=no')
    out('publication_receipt.json',{'status':'PASS','branch':e['branch'],'HEAD':e['head'],'tracked_status':'',
        'untracked_research':'old inventory/hash pins preserved; only09 created/edited',
        'terminal_outcome':'A','cumulative_CPU':total,'remaining_CPU':7200-total})
    files=[]
    for p in sorted(B.rglob('*')):
        if p.is_file():files.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
    out('campaign_manifest.json',{'status':'SEALED_CORE11_RETURN_OUTCOME_A','branch':e['branch'],'HEAD':e['head'],
        'files':files,'self_hash':'external verification receipt; manifest excludes its own bytes',
        'resources':resources,'theorem':'CORE11-RETURN','scope':'core11 R01 only; Step2/CD6/UniversalCD/DO OPEN'})
    m=read('campaign_manifest.json')
    assert all(sha(ROOT/v['path'])==v['sha256'] for v in m['files'])
    print(json.dumps({'status':'MANIFEST_ALL_BYTES_VERIFIED','files':len(files),'manifest_sha256':sha(B/'campaign_manifest.json'),
        'cumulative_CPU':total,'remaining_CPU':7200-total,'groups':group}))
if __name__=='__main__':{'before':before,'after':after}[sys.argv[1]]()
