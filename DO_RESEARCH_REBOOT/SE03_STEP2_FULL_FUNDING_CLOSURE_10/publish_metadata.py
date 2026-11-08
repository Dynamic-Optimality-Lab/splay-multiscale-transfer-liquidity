"""Campaign10 metadata: exact scopes, status gates, provenance and receipt."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:
        if isinstance(v,str):f.write(v)
        else:json.dump(v,f,indent=2)
def before():
    pins=read('dependency_pins.json');by={v['path']:v for v in pins['pins']}
    src=[
        ('ORIGINAL_PIPELINE.md','SOURCE DEFINITION; original operations/costs, no depth+1 substitute'),
        ('RESEARCH_RULES.md','SOURCE RULES; no circular existence burdens or finite promotion'),
        ('CD5_BASE01/CD5_PROOF.md','PROVED complete scalar support<=5; source proof inspected; explicit Step1 owner scope kept distinct'),
        ('M3_XFER21/FULL_M3_PROOF.md','PROVED frozen local five-mark/nine-Score signed theorem, source formula/scope inspected'),
        ('SE03_STEP1_FUND01/SOURCE_BRIDGE.md','PROVED auxiliary five-key/core9 scope; inspected, not universalized to all lower cores'),
        ('SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED first-three selector/cyclic bank and physical reserve, inspected'),
        ('SE03_STEP1_FUND01/SIGNED_CANCELLATION.md','PROVED ordinal C/P/N and fixed common-owner interface, inspected'),
        ('SE03_STEP1_FUND01/SOURCE_IDS_AND_CYCLIC_CUT.md','PROVED actual aligned interval and legal maximum-debt cut, inspected'),
        ('SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED set-growth/density/alternation, proof reused at true source scope'),
        ('SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED actual successor and disjoint max-depth packets, inspected'),
        ('SE03_STEP2_REPAY01/IMPROVED_FULL_DEBT_TARGET.md','PROVED conditional exchange, global debt OPEN; inspected'),
        ('SE03_STEP2_REPAY01/PACKET_PERIOD_TRANSPORT.md','PROVED both-endpoint actual-time period bijection, inspected'),
        ('SE03_STEP2_REPAY01/SOURCE_OBSTRUCTION_AND_TWO_BLOCK_REPAIR.md','PROVED original Gamma family/two physical tail units, inspected'),
        ('SE03_STEP2_REPAY01/CYCLIC_DONOR_ID_AUDIT.md','PROVED Gamma legal-cut condition, newly independently checked'),
        ('SE03_STEP2_REPAY01/source_term_derivation.json','EXACT source Gamma26; source trees/word/costs independently replayed'),
        ('SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md','PROVED source width>=r-3 on unpaired macros, inspected'),
        ('SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md','PROVED actual partition and modified Gamma_r width>=r-4; sufficiency OPEN'),
        ('SE03_STEP2_REPAY02/RECENT_SUPPORT_COVER.md','PROVED actual windows/complement/core10-11 hit charts, inspected'),
        ('SE03_STEP2_REPAY02/NINE_SCORE_SOURCE_BRIDGE.md','PROVED LOCAL bridge including unmarked Score leaves; virtual comparison hypotheses inspected'),
        ('SE03_STEP2_REPAY02/COLD_EXCHANGE_IDENTITY.md','PROVED identities, signs OPEN; original minus1 retained'),
        ('SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','PROVED refined gE only; fixed fE distinction preserved'),
        ('SE03_STEP2_TERMINAL_PAIR_06/saturation3.json','ACCEPTED06; reuse completed audit, invalid saturation.json excluded'),
        ('SE03_STEP2_FINAL_PLUS_ONE_07/independent_audit2.json','ACCEPTED07; initial raw-count check superseded, completed audit reused'),
        ('SE03_STEP2_PLUS_ONE_ZERO_TAIL_08/FULL_PROOF.md','PROVED08 at original scope, completed checks reused'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/FULL_PROOF.md','PROVED CORE11-RETURN exact R01 domain; inspected, not reopened'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/PHYSICAL_FUNDING_INTERFACE.md','OPEN full Step2; exact load-bearing source bridge inspected'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/CHECKPOINT.md','Authoritative current source/resource handoff, inspected'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/CASE_LEDGER.md','PROVED coverage at core11 R01 scope; no other signed paths inferred'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/INDEPENDENT_AUDIT.md','Accepted distinct implementation audit, reused without repeat'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/source_control_replay.json','Accepted18 controls/1234 period rows, retained; only new-load-bearing controls replayed10'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/seal_audit.json','Accepted09 seal, all14 gates at exact scope'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/campaign_manifest.json','Accepted09 manifest, all files rehashed'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/resources_checkpoint.json','Authoritative3399.796875 CPU ledger, no reset')]
    rows=['# Direct inspected/reused local provenance','',
        'The current local worktree is authoritative. Every inherited2114 local pin',
        'and external directive verifies at entry/final audit. There is no remote',
        'snapshot substitution. dependency_pins.json stores the full transitive set.','',
        '| Repository path | Status / permitted use / inspection | SHA256 |','|---|---|---|']
    for rel,status in src:
        path='DO_RESEARCH_REBOOT/'+rel;assert path in by,path
        rows.append('|'+path+'|'+status+'|'+by[path]['sha256']+'|')
    for path in ('DO_RESEARCH_REBOOT/SE03_STEP2_COLD_NEG2_01/source_model.py','python/independent/splay.py'):
        rows.append('|'+path+'|IMMUTABLE original trace implementation; no modification|'+by[path]['sha256']+'|')
    rows+=['','No critical missing input was invented. Missing mathematical donor-supply',
        'theorems remain OPEN rather than becoming dependency assumptions. The old',
        'changing-chart Hamiltonian debt stays REFUTED; no current graph edge, mu,',
        'sigma, private scope, shared midpoint or raw original state is altered.','',
        'All new local comparisons invoke the existing universal LOCAL M3 relation',
        'at its proven scope. They neither apply a closed-walk IH to an open source',
        'nor identify the comparison with the actual erased execution.','']
    out('SOURCE_PROVENANCE.md','\n'.join(rows))
    part=read('source_partition_certificate.json');families=read('deficient_source_schemas.json')['families']
    rows=['# Complete source/owner case ledger with unresolved classes','',
        '| Full core | Necessary marked masks | Recent5 core range | Physical residual slots | Status |','|---|---:|---|---|---|']
    for v in part['rows']:
        d='; '.join('H'+str(x['H'])+'/Q'+str(x['Q'])+':'+str(x['slots']) for x in v['negative_physical_classes']) or 'none'
        rows.append('|'+str(v['core'])+'|'+str(len(v['necessary_masks']))+'|'+str(v['recent5_core_interval'])+'|'+d+'|'+('PROVED full-core6' if v['core']==6 else 'OPEN arbitrary-history funding')+'|')
    rows+=['','Mask lists are NECESSARY SOURCE coverage, never realization claims. Whole',
        'full and auxiliary labeled cores are constant on their respective actual',
        'closed periods. Shapes, charts and BE/full interference may vary.','',
        '| Packet/operation/owner case | Exact treatment |','|---|---|',
        '|H0 and root identities|No genuine H0 macro; actual repeats retained with BE actions|',
        '|Singleton H1/Q0,1,2 and H>=2/Q<=4|Own actual bits cover raw full demands; locks handled by partial exchange|',
        '|Singleton H1/Q3 or Q4|One/two actual excess slots, global residual repair OPEN|',
        '|Pair H2/Q6|Both actual H1 macros, two excess slots|',
        '|Pair H>=3/Q6|Raw-balanced own bits; all source midpoints/occurrences retained|',
        '|Fixed-chart hits|Existing local signed M3 comparison, not individually free physical credit|',
        '|Small-core cold marks|New fixed-Score relabeling difference, sign OPEN|',
        '|Core10 cold v not ancestor|Direct new cover and mark-switch difference, sign OPEN|',
        '|Core10 cold v ancestor, Q>=2|Internal first-double virtual source; actual minus1 preserved|',
        '|Core10 root-changing Q1 peel|Separate raw-balanced physical case; no unsynchronized M3 source fabricated|',
        '|Core11 cold two twigs/one chain|Inherited direct/peeled identity; actual charts and minus1 retained|',
        '|C common owners|All fixed fE values retained exactly|',
        '|N auxiliary-only|Claims retired in alternative full allocation, actual unit IDs released once|',
        '|Successful unmatched root|Distinct free terminal of finite exchange path|',
        '|Blocked unmatched root|Explicit distinct common-owner anchor in R; not funded|',
        '|Global source supply|Pstar->Wstar distinct physical repair NOT PROVED|',
        '|Private helpers / reflection|Universal source proofs and exact separate controls; no population cap|',
        '|Cuts / copies|Bijection of both donor and demand IDs, no extra physical pool|','',
        'The six new specified source words have complete receipts; this does not',
        'upgrade any OPEN arbitrary-history row. Duplicate/outside-period donors',
        'are rejected; the adjacent-packet global repair has two exact failures.','']
    out('CASE_LEDGER.md','\n'.join(rows))
    gates={
        'J1':('RESTRICTED_BASE_VERIFIED','Step1 core9 physical allocator and scalar CD5 scopes preserved; lower-core physical base not silently supplied'),
        'J2':('PASS_COVERAGE','all full cores6..11 and auxiliary5..9, fixed-core transitions and residual classes accounted'),
        'J3':('OPEN','core6 proved; arbitrary core7..10 residual supply unproved'),
        'J4':('PASS_EXACT_INHERITANCE','accepted09 CORE11_RETURN retained at its R01 scope'),
        'J5':('PARTIAL','exact chart identities/geometry derived; repayment of corrections unproved'),
        'J6':('PASS_LEDGER','every physical demand in common/successful/unpaid Pstar ledger'),
        'J7':('OPEN','all used units actual, but source-derived supply for every unpaid root absent'),
        'J8':('PARTIAL','fixed common owners preserved in proved partial map; no complete global extension'),
        'J9':('OPEN','partial maps injective; arbitrary full-demand injection not established'),
        'J10':('PARTIAL','period transport proved for existing receipts; full map not constructed'),
        'J11':('OPEN_TARGET','partial theorems universal, complete arbitrary-history source funding absent'),
        'J12':('PASS_IMPLICATION_ONLY','a complete physical injection would imply QF<=2A; its premise not claimed'),
        'J13':('PARTIAL','distinct-engine component/receipt checks only, no arbitrary-history full map to audit'),
        'J14':('OPEN','frozen full six-key theorem has not been proved')}
    out('completion_gates.json',{'status':'NOT_ALL_CLOSED_NO_OUTCOME_A','gates':{k:{'status':s,'reason':r} for k,(s,r) in gates.items()},
        'Gate_U':'U_OPEN_REPLACEMENT_INVARIANT; U_E_ADJACENT_PACKET_CANDIDATE_ONLY',
        'terminal_outcome':'UNRESOLVED_PROOF_LIMIT','CPU_exhausted':False})
    out('research_status_ledger.json',{'CD6_FUNDING':'OPEN','full_core6_CD_and_physical_map':'PROVED_UNIVERSAL_SUBCLASS',
        'residual_slot_owner_normalform':'PROVED_UNIFORM_COMPONENT',
        'small_core_local_comparison_graft':'PROVED_LOCAL_COMPARISON_ONLY',
        'deficiency_one_peel_geometry':'PROVED_UNIFORM_SOURCE_LEMMA',
        'chart_correction_signs':'OPEN','source_donor_supply_Pstar_to_Wstar':'OPEN',
        'adjacent_packet_repair':'REFUTED_EXACT_ONLY_THIS_RULE',
        'new_source_families':'EXACT_ARBITRARY_GAP_IDENTITIES_WITH_RESTRICTED_FULL_RECEIPTS',
        'old06_09':'PROVED_SCOPES_UNCHANGED','old_changing_chart_debt':'REFUTED_UNCHANGED',
        'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'formal_assistant':False,'external_peer_review':False})
    out('residual_slot_spec.json',{'status':'UNIFORM_COMPONENT_PROVED_NOT_SOURCE_SUPPLY',
        'h0':'first min(Qe,2He) actual full demand IDs mapped to first own physical bits in each disjoint actual packet',
        'R':'final (Qe-2He)+ demand slots, disjoint over source packets',
        'locked':'actual pulled-back fixed fE common map, unchanged',
        'unpaid_roots':'(P intersect R) disjoint_union blocked_roots',
        'anchor':'identity on P intersect R; blocked actual common owner on blocked roots',
        'available':'U minus image(proved partial allocation)',
        'missing':'source-derived DISTINCT available actual bits for every unpaid root',
        'scope':'any finite support/length/private trees; actual permitted period/block eligibility only'})
    out('artifact_status_ledger.json',{'accepted_bridge_version':'audit_bridges2.py / bridge_audit2.json',
        'failed_draft':'audit_bridges.py; c9 zero-padding symbolic-hole/empty bug; preserved and CPU charged',
        'failed_draft_test_counter':'exit reports planned8; actual log reaches7th control after6 completed, no passing certificate produced',
        'Step2_FULL_PROOF.md':'ABSENT_BY_DESIGN_TARGET_UNPROVED',
        'all_old_proof_artifacts':'unchanged pinned',
        'historical_controls':'09 full accepted receipt reused; Gamma26 and new-load-bearing failed-rule controls replayed10'})
    print(json.dumps({'status':'METADATA_READY_PARTIAL_ONLY','metadata_CPU_excluded':time.process_time()}))
def after():
    e=read('entry.json');total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);phases=[]
    for p in sorted(B.glob('run_*_result.json')):
        v=json.loads(p.read_text());c=read('controller_'+v['phase']+'_exit.json')
        charge=v['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[v['group']]+=charge
        phases.append({'phase':v['phase'],'status':v['status'],'group':v['group'],'child_CPU':v['child_CPU'],
            'whole_controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,'source_calls':v['source_engine_calls'],
            'declared_finite_checks':v['new_finite_tests'],'old_rows_replayed':v['old_semantic_rows_replayed']})
    assert total<7195 and all(groups[g]<e['group_caps'][g] for g in groups)
    assert read('seal_audit.json')['terminal_outcome']=='UNRESOLVED_PROOF_LIMIT'
    out('resources_checkpoint.json',{'status':'PASS_CAPS_PRESERVED_PROOF_LIMIT_NOT_RESOURCE_LIMIT',
        'prior_CPU':e['prior_uniform_CPU'],'cumulative_CPU':total,'ceiling':7200,'reserve':5,
        'remaining_CPU':7200-total,'available_before_reserve':7195-total,
        'cumulative_group_CPU':groups,'group_caps':e['group_caps'],
        'remaining_group_CPU':{g:e['group_caps'][g]-groups[g] for g in groups},'phases':phases,
        'source_engine_calls':sum(v['source_calls'] for v in phases),'failed_CPU_included':True,
        '2M_query_live_cap':2000000,'DAG_cap':4000000,'edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
        'metadata_exclusion':'same inherited entry/provenance/publication convention; every proof/replay/seal child and whole controller charged',
        'stopping_reason':'no proved arbitrary-history residual donor supply; local repair refuted; no circular Hall/cardinality substitution',
        'CPU_exhausted':False,'no_budget_reset':True,'metadata_CPU_this_invocation_excluded':time.process_time()})
    def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('rev-parse','HEAD')==e['head'] and git('branch','--show-current')==e['branch']
    assert not git('status','--porcelain','--untracked-files=no')
    out('publication_receipt.json',{'status':'PASS_PARTIAL_PUBLICATION_NO_STEP2_PROMOTION',
        'branch':e['branch'],'HEAD':e['head'],'tracked_status':'','only_new_campaign_written':True,
        'terminal_outcome':'UNRESOLVED_PROOF_LIMIT','Gate_U':'U_OPEN','Step2':'OPEN',
        'CPU':total,'remaining_CPU':7200-total})
    files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.rglob('*')) if p.is_file()]
    out('campaign_manifest.json',{'status':'SEALED_PARTIAL_RESEARCH_NO_STEP2_PROMOTION','branch':e['branch'],'HEAD':e['head'],
        'files':files,'terminal_outcome':'UNRESOLVED_PROOF_LIMIT','Gate_U':'U_OPEN','self_hash':'manifest excludes itself; verify external receipt',
        'Step2':'OPEN','CD6_full_scope':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
    assert all(sha(ROOT/v['path'])==v['sha256'] for v in files)
    print(json.dumps({'status':'ALL_MANIFEST_BYTES_VERIFIED_PARTIAL_ONLY','files':len(files),
        'manifest_sha256':sha(B/'campaign_manifest.json'),'CPU':total,'remaining_CPU':7200-total,'groups':groups}))
if __name__=='__main__':{'before':before,'after':after}[sys.argv[1]]()
