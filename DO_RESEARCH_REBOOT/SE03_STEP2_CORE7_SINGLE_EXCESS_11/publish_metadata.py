"""Campaign11 provenance, logical scope and cumulative publication metadata."""
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
        ('ORIGINAL_PIPELINE.md','SOURCE DEFINITION; actual original event costs/present-key model retained'),
        ('RESEARCH_RULES.md','SOURCE RULES; true-scope proof/evidence discipline'),
        ('CD5_BASE01/CD5_PROOF.md','PROVED base/support normalization/core constancy, scope inspected; not applied to a six-key word'),
        ('SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED counting-bit/source-period fE interface; no native eligibility expansion'),
        ('SE03_STEP1_FUND01/SOURCE_IDS_AND_CYCLIC_CUT.md','PROVED actual aligned interval and maximum-debt cut, inspected'),
        ('SE03_STEP1_FUND01/SIGNED_CANCELLATION.md','PROVED ordinal C/P/N, retirement and locked-owner pool; inspected'),
        ('SE03_STEP2_REPAY01/IMPROVED_FULL_DEBT_TARGET.md','PROVED source-ID fixed-owner exchange component; unproved debt NOT assumed'),
        ('SE03_STEP2_REPAY01/PACKET_PERIOD_TRANSPORT.md','PROVED simultaneous donor/demand period transport; inspected'),
        ('SE03_STEP2_REPAY01/CYCLIC_DONOR_ID_AUDIT.md','PROVED original Gamma cut; independently recomputed again'),
        ('SE03_STEP2_REPAY02/HAMILTONIAN_DEBT_NORMALIZATION.md','ONLY incoming-Hamiltonian structural proof inherited/generalized; old changing-chart normalization REFUTED unchanged'),
        ('SE03_STEP2_CORE11_RETURN_ASSEMBLY_09/FULL_PROOF.md','PROVED core11 R01 scope unchanged; mandatory controls replayed'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/FINAL_VERDICT.md','UNRESOLVED full Step2, inspected; not mistaken for complete funding'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/CHECKPOINT.md','Authoritative ONE-slot core7 target and zero-source necessary condition, inspected'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/RESIDUAL_SLOT_THEOREM.md','PROVED actual-ID anchor/partial map; complete proof inspected and reused'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/PHYSICAL_DONOR_LEDGER.md','PROVED inventory/interface, source supply formerly OPEN; inspected'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/FROZEN_FE_AUDIT.md','PROVED component scope; fE/gE/base distinctions preserved'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/DEFICIENT_CORE_CLOSURE.md','PROVED core6/restricted word receipts; core7 one-slot open10, inspected'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/CHART_BOUNDARY_CORRECTIONS.md','PROVED comparison identities; correction signs not imported as positive'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/SIX_KEY_SOURCE_PARTITION.md','PROVED necessary source coverage, exact c7 costs/masks inspected'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/PERIOD_CUT_VALIDITY.md','PROVED actual-period transport component, inspected'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/UNIFORM_R_INTERFACE.md','U-OPEN, preserved; no arbitrary-support campaign executed'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/INDEPENDENT_AUDIT.md','Accepted partial source/audit scope, inspected; controls newly replayed11'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/ADVERSARIAL_AUDIT.md','Accepted local-rule refutations, freshly replayed unchanged'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py','IMMUTABLE accepted actual-ID partial algorithm reused with supplied actual fE'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/deficient_source_schemas.json','EXACT source words/free-gap/erasure receipts; actual states independently recomputed'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/resources_checkpoint.json','Authoritative3404.1875 CPU, no reset'),
        ('SE03_STEP2_FULL_FUNDING_CLOSURE_10/campaign_manifest.json','Accepted PARTIAL publication manifest; every byte verified')]
    rows=['# Exact source provenance and accepted scopes','',
        'The authoritative LOCAL worktree was inspected. All2204 inherited/local',
        'pins and external directives verify at entry and final seal. No remote',
        'snapshot was substituted. Full transitive hashes are in dependency_pins.json.','',
        '| Repository path | Status / inspection / use | SHA256 |','|---|---|---|']
    for rel,status in src:
        path='DO_RESEARCH_REBOOT/'+rel;assert path in by,path
        rows.append('|'+path+'|'+status+'|'+by[path]['sha256']+'|')
    for path in ('DO_RESEARCH_REBOOT/SE03_STEP2_COLD_NEG2_01/source_model.py','python/independent/splay.py'):
        rows.append('|'+path+'|IMMUTABLE source engine; ordinary trace only, no depth+1 proxy|'+by[path]['sha256']+'|')
    rows+=['','External pinned source directives include the original IAGS/R1-R4',
        'reconstruction and current Campaign11. Their exact paths/hashes appear',
        'in dependency_pins.json. No inherited theorem or graph is rewritten.','',
        'All critical prerequisites are available and verified at their true scopes.',
        'No missing donor/Hall/global CD6 premise is assumed. Only the structural',
        'incoming-Hamiltonian induction is reused from the refuted normalization',
        'route, with a fresh number-independent proof and separate seven-Score check.',
        'Old06 saturation3 and07 independent_audit2 remain the accepted versions;',
        'invalid/superseded artifacts remain preserved but are not premises.','']
    out('SOURCE_PROVENANCE.md','\n'.join(rows))
    geo=read('geometry_certificate.json');ind=read('independent_audit.json');owner=read('ownership_audit.json')
    rows=['# Complete one-slot source/ownership case ledger','',
        '| Case | Source/physical treatment | Status |','|---|---|---|',
        '|Six marks in seven-node full core|One unmarked role2..6, all ordered skeletons and arbitrary private gaps|COVERED|',
        '|Sole physical excess slot|Unique actual H1/Q3 macro, r=(t*,3), no q5 pair|COVERED|',
        '|Preceding genuine macro|Hamiltonian-destination fork lemma forces Q<=1; H>=1|PROVED source positive supply|',
        '|Positive Splus|Pick actual first h0-unused bit; build source-certified complete h|PROVED|',
        '|Zero Splus candidate|Would require all other H1/Q2, contradict actual predecessor Q<=1|IMPOSSIBLE BY SOURCE|',
        '|Empty Pstar|Existing a already complete; return unchanged|COVERED|',
        '|p=r unmatched excess|h/a free-terminal walk; no raw bit assumed free|COVERED|',
        '|p!=r, common excess owner|p anchored at already-paid r; all-paid walk preserves it|COVERED|',
        '|Seed v already owned|Continue through its exact a owner, never steal it|COVERED|',
        '|Wstar bit eligibility|Independent stream + actual-period transport + accepted fixed-owner endpoint receipt|PROVED for selected u|',
        '|Actual fE image|ALL certified supplied maps covered parametrically; no fixture substituted|PRESERVED|',
        '|N retired E-only owners|Existing cancellation authority only; no new release|PRESERVED|',
        '|Root repeats / nongenuine KEEP|All A work, BE transitions and physical IDs retained in macro|COVERED|',
        '|DELETE-positive event at terminal key|Actual original A event/bit ID retained, even if KEEP has A0|COVERED|',
        '|Anonymous helpers outside zero candidate|Arbitrary actual source work in H; no population cap|COVERED|',
        '|All actual chart/erasure changes|Pay every full D; literal C/P/N signed ledger, no debt credit|COVERED|',
        '|Private BSTs and sparse labels|Order-preserving core normalization; free-gap commuting induction|COVERED|',
        '|Both orientations|Separate LL/RR fork proofs and full relation reflection|COVERED|',
        '|Actual period / seam|Both endpoint IDs transported; old fE/a cut/values fixed|COVERED|',
        '|Multiple residuals / other cores|Rejected by this algorithm scope; separate future campaign|OUTSIDE CURRENT THEOREM|','',
        '| Unmarked role | Complete necessary contexts | Genuine edges | Q3 sectors |','|---|---:|---:|---:|']
    for v in geo['classes']:rows.append(f"|{v['unmarked']}|{v['core_contexts']}|{v['admitted_genuine_edges']}|{v['Q3_sectors']}|")
    rows+=['','Totals1320 contexts,5784 genuine edges,132 critical sectors and198',
        'preceding incidences. All are parameterized source languages; no realization',
        'of arbitrary table paths is presumed. Arbitrary finite source lengths use',
        'the structural argument and terminating ownership path, not a depth bound.','',
        'Owner tests:696 actual auxiliary-demand-indexed injection fixtures give',
        '464 p=r and232 empty cases; a separate COMMON-excess blocked-other fixture',
        'covers p!=r. Test placements are logical, not numerical sealed fE maps.',
        'Independent abstract one-hole cases31104 include2304 tight inventories.',
        'The universal proof is injectivity/actual-source geometry, not these tests.','']
    out('CASE_LEDGER.md','\n'.join(rows))
    evidence={
        'K1':'complete7-Score source/gap coverage and all5 unmarked positions',
        'K2':'literal10 anchor, exact empty/p=r/blocked p!=r cases',
        'K3':'U,common/used images and Wstar exact; no phantom/duplicate units',
        'K4':'constructive actual positive-macro spare -> full h -> owner terminal',
        'K5':'zero candidate universally contradicted by Hamiltonian predecessor',
        'K6':'all-paid ownership route permits nonlocal terminal and legal cyclic receipt',
        'K7':'actual(t,j,b) free terminal explicitly computed',
        'K8':'every supplied actual common fE value retained; ALL paid values fixed',
        'K9':'h/a path and final injection proof, no duplicate bit',
        'K10':'one actual interval, full-cut stream and both-endpoint transport',
        'K11':'all original full D demands paid; exact auxiliary C/P/N and signed J retained',
        'K12':'free-tree induction, arbitrary H/private source work, unbounded finite owner path',
        'K13':'separate immutable splay/backwards ownership checks and mandatory controls',
        'K14':'explicit C7-ONE-SLOT reconstruction, no broader funding claim'}
    out('completion_gates.json',{'status':'ALL_RELEVANT_K1_K14_PASS','gates':{k:{'status':'PASS','evidence':v} for k,v in evidence.items()},
        'Gate_A_to_J':{k:'PASS_AT_DECLARED_CERTIFIED_COUNTING_SOURCE_INTERFACE' for k in 'ABCDEFGHIJ'},
        'U11':'PROVED_REUSABLE_ONE_SLOT_COMPONENT','general_Gate_U':'U_OPEN',
        'trust':'mathematical source proof and same-agent independent implementation audit, not formal certification'})
    draft=read('physical_receipts.json');actual_calls=sum(len(v['rows'])+2*sum(r['mode']=='K' for r in v['rows']) for v in draft['families'])
    assert actual_calls==102
    out('construction_accounting_correction.json',{'status':'EXACT_STATIC_TRACE_ACCOUNTING_FOR_SUPERSEDED_DRAFT',
        'phase':'construction','controller_reported_source_calls':0,'actual_source_calls':actual_calls,
        'reason':'p.replay has one A trace per operation and full/duplicate-E traces per KEEP when erased=None; explicit call counter absent in initial draft',
        'draft_internal_estimate':draft['source_engine_calls'],'accepted_source_receipt':'physical_receipts2.json, actual erased recurrence, counted96 calls',
        'CPU':'original child/controller already fully charged; no semantic check repeated to repair this ledger'})
    out('artifact_status_ledger.json',{'geometry_certificate.json':'AUTHORITATIVE complete necessary source grammar',
        'physical_receipts2.json':'AUTHORITATIVE actual full/erased source and physical fixtures',
        'physical_receipts.json':'SUPERSEDED un-erased-placeholder/accounting draft, retained and query count corrected',
        'independent_audit.json':'AUTHORITATIVE distinct-engine/backwards checker',
        'ownership_audit.json':'AUTHORITATIVE696 logical owner fixture checks, not numerical fE realization',
        'blocked_common_case.json':'AUTHORITATIVE p!=r COMMON-anchor logical case',
        'source_stream_audit.json':'AUTHORITATIVE independent original-time stream and period transport',
        'historical_controls.json':'AUTHORITATIVE mandatory fresh control replay, old artifacts unchanged'})
    out('single_slot_certificate.json',{'status':'C7_ONE_SLOT_SOURCE_FUNDING_PROVED',
        'source':'original reachable finite exactly paired-closed six-mark full-core7 actual aligned periods with |R|1',
        'supply':'unique H1Q3 -> Hamiltonian source -> previous Q<=1,H>=1 -> Splus>=1',
        'zero_surplus':'IMPOSSIBLE_BY_SOURCE','independent_full_h':'h0 plus actual first positive-packet own-unselected v for r',
        'physical_stream':'one carried v, working<=4, actual source time before both-endpoint transport',
        'available_donor':'free terminal of complete h against ALL existing a owners',
        'preserves':'EVERY prior a assignment and actual common frozen fE value',
        'eligibility':'inherited physical counting/block-cyclic same-period source receipt, no new native policy',
        'empty_residual':'return a unchanged','two_root_locations':['p=r','p!=r blocked at COMMON r'],
        'geometry_sha256':sha(B/'geometry_certificate.json'),'independent_audit_sha256':sha(B/'independent_audit.json'),
        'actual_receipts_sha256':sha(B/'physical_receipts2.json'),'allocator_sha256':sha(B/'single_slot_allocator.py'),
        'scope':'ONE excess slot ONLY; full Step2 and CD6 open'})
    out('research_status_ledger.json',{'C7_ONE_SLOT_FUNDING':'PROVED_UNIVERSAL_DECLARED_SOURCE_SCOPE',
        'zero_surplus_core7_one_slot':'IMPOSSIBLE_UNIVERSAL_SOURCE',
        'all_paid_one_hole_endpoint':'PROVED','U11_single_slot_principle':'PROVED',
        'old10_full_Step2':'UNRESOLVED_UNCHANGED','old06_09':'PROVED_SCOPES_UNCHANGED',
        'old_changing_chart_Hamiltonian_debt':'REFUTED_UNCHANGED',
        'core7_multi_slot':'OPEN_NOT_EXECUTED','other_cores':'OPEN_NOT_EXECUTED','Step2':'OPEN','CD6_full_scope':'OPEN',
        'Step3':'OPEN','general_Gate_U':'U_OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'external_peer_review':False,'formal_assistant':False})
    print(json.dumps({'status':'C11_METADATA_READY','metadata_CPU_excluded':time.process_time()}))
def after():
    e=read('entry.json');total=e['prior_uniform_CPU'];group=dict(e['inherited_group_CPU']);phases=[]
    correction=read('construction_accounting_correction.json')
    for p in sorted(B.glob('run_*_result.json')):
        v=json.loads(p.read_text());c=read('controller_'+v['phase']+'_exit.json')
        assert v['status']=='PASS' and not c['error']
        charge=v['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;group[v['group']]+=charge
        actual=correction['actual_source_calls'] if v['phase']=='construction' else v['source_engine_calls']
        phases.append({'phase':v['phase'],'group':v['group'],'child_CPU':v['child_CPU'],
            'whole_controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,
            'reported_source_calls':v['source_engine_calls'],'actual_source_calls':actual,
            'new_finite_controls':v['new_finite_tests'],'old_period_rows':v['old_semantic_rows_replayed']})
    assert total<7195 and all(group[g]<e['group_caps'][g] for g in group)
    assert read('seal_audit2.json')['terminal_outcome']=='A'
    out('resources_checkpoint.json',{'status':'PASS_ALL_EXISTING_CAPS_PRESERVED','prior_CPU':e['prior_uniform_CPU'],
        'cumulative_CPU':total,'ceiling':7200,'required_reserve':5,'remaining_CPU':7200-total,
        'available_before_reserve':7195-total,'cumulative_group_CPU':group,'group_caps':e['group_caps'],
        'remaining_group_CPU':{g:e['group_caps'][g]-group[g] for g in group},'phases':phases,
        'actual_source_engine_calls':sum(v['actual_source_calls'] for v in phases),'query_accounting_correction':correction,
        'query_live_cap':2000000,'DAG_cap':4000000,'edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
        'no_reset':True,'metadata_convention':'same inherited entry/provenance/publication exclusion; all proof/replay/seal child and whole controller CPU charged',
        'metadata_CPU_this_publication_excluded':time.process_time()})
    def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('rev-parse','HEAD')==e['head'] and git('branch','--show-current')==e['branch']
    assert not git('status','--porcelain','--untracked-files=no')
    out('final_artifact_status_addendum.json',{'status':'FINAL_ELIGIBILITY_RECONSTRUCTION_VERIFIED',
        'final_seal':'seal_audit2.json','final_dependency_check':'dependency_revalidation2.json',
        'earlier_seal':'seal_audit.json retained, superseded for final publication after sharper eligibility audit',
        'eligibility_audit':'eligibility_exchange_audit.json',
        'eligibility_audit_sha256':sha(B/'eligibility_exchange_audit.json'),
        'reason':'licensed original common-set exchange preserves every old successful partial path; no enlarged auxiliary interpretation',
        'new_eligibility_cases':5256,'universal_proof':'path stability under h0 completion only at r'})
    out('publication_receipt.json',{'status':'PASS_C7_ONE_SLOT_OUTCOME_A','branch':e['branch'],'HEAD':e['head'],'tracked_status':'',
        'old_untracked_research':'preserved, only11 written','terminal_outcome':'A','theorem':'C7_ONE_SLOT_FUNDING',
        'scope':'exactly ONE excess slot; no multi-slot or other-core campaign','Step2':'OPEN',
        'CPU':total,'remaining_CPU':7200-total})
    files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.rglob('*')) if p.is_file()]
    out('campaign_manifest.json',{'status':'SEALED_C7_ONE_SLOT_OUTCOME_A','branch':e['branch'],'HEAD':e['head'],
        'files':files,'self_hash':'manifest excludes its own bytes; external verification receipt',
        'theorem':'C7_ONE_SLOT_FUNDING','Step2':'OPEN','CD6_full_scope':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
    assert all(sha(ROOT/v['path'])==v['sha256'] for v in files)
    print(json.dumps({'status':'ALL_MANIFEST_BYTES_VERIFIED_OUTCOME_A','files':len(files),
        'manifest_sha256':sha(B/'campaign_manifest.json'),'CPU':total,'remaining_CPU':7200-total,'groups':group}))
if __name__=='__main__':{'before':before,'after':after}[sys.argv[1]]()
