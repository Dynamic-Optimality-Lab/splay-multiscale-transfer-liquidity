"""Campaign12 status/provenance/resource publication; no source execution."""
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
    ind=read('independent_audit.json');owner=read('ownership_audit.json');src=read('physical_receipts2.json');old=read('historical_controls.json')
    for ph in ('geometry','construction2','independent3','ownership','controls'):assert read('run_'+ph+'_result.json')['status']=='PASS'
    rows=['# Complete source/ownership case ledger','',
        '| Case | Exact treatment | Status |','|---|---|---|',
        '|Five unmarked roles/all source shapes|fixed labeled core,429 skeletons, arbitrary eight ordered private gaps|COVERED|',
        '|Same macro for both slots|Q<=3,H>=1 implies one slot at most|IMPOSSIBLE|',
        '|Distinct critical macros|each actual H1Q3, r=(t,3)|COVERED|',
        '|Adjacent critical macros/shared predecessor|Q predecessor<=1 and cyclic predecessor injective|IMPOSSIBLE|',
        '|Same/different marked targets or charts|no equality assumption in the source/owner proof|COVERED WHEN SOURCE-VALID|',
        '|Zero/one raw Splus|two distinct predecessor inventories each contribute >=1|IMPOSSIBLE|',
        '|Two or more raw spare bits|specified seeds complete h independently of owners|COVERED|',
        '|Pstar0|return a unchanged|COVERED|',
        '|Pstar1 in a TWO-slot source|use complete two-slot h, not whole-period11 theorem|COVERED|',
        '|Pstar2|two disjoint fixed-a paths and distinct free endpoints|COVERED|',
        '|Both roots own anchors / blocked-common anchors / mixed|literal alpha formula, licensed original C exchange|COVERED|',
        '|Zero/one/two initially locked seeds|follow owners, never steal locks; new terminals free|COVERED|',
        '|All previous paid full mappings|old successful h0/l paths IDENTICAL under h extension|FIXED EXACTLY|',
        '|Eligibility coupling|one jointly licensed complete h/l receipt, no assumed static Hall|COVERED|',
        '|Nongenuine KEEPs/DELETEs/A0 operations|all retained in literal original macros/erased replay|COVERED|',
        '|Positive anonymous helper/private access|actual A events in H,U; no A pruning|COVERED|',
        '|All erased runs/BF-BE disagreement/chart correction|every full D paid once, signed C/P/N retained|COVERED|',
        '|Both orientations/indefinite finite length|separate LL/RR induction, finite injective-path proof|COVERED|',
        '|Legal seam/aligned period|disjoint two blocks, both-ID period transport; fE cut fixed|COVERED|',
        '|More than two slots/other cores|outside frozen source target|NOT PROMOTED|','',
        'The classification is necessary source coverage, not realization of every abstract edge.',
        'All valid source classes are covered by the symbolic construction even where a',
        'particular finite source fixture does not realize an asymmetric owner branch.','']
    out('CASE_LEDGER.md','\n'.join(rows))
    out('INDEPENDENT_AUDIT.md',f'''# Independent source and joint ownership audit

The distinct immutable python/independent/splay.py engine recomputes429
ordered seven-Score skeletons and3003 target accesses BEFORE comparing
the producer relation. It verifies all five mark masks,1320 necessary
contexts,5784 genuine edges,132 Q3 sectors and198 predecessor incidences,
all reflected edges, and incoming-Hamiltonian counts q0:128,q1:48.
No producer rotation code or primary source replay is imported.

It independently replays{len(src['families'])} actual full/erased source
reports: four closed two-slot words and their reflections, each with all
SIX erasures. Base sources have46 occurrences; early-DELETE/repeated-KEEP
variants102; private-gap variants46; actual private-helper excursions48.
All original A/BF/BE states, event cases/ordinals, six genuine marks,
fixed core, reaching erased recurrence, charts, physical R and chosen
seed IDs are recomputed. Total5816 source events are compared. The
independent causal h stream holds at most4 units and transports both
endpoints through2904 cuts. Symbolic gap/source proof supplies unbounded
private/source-length coverage; these concrete extensions are audits.

The432 auxiliary-demand-indexed owner fixtures are arbitrary logical
injections on actual source IDs, NOT numerical sealed fE realizations.
Their symmetric repeated-word erased sectors yield288 two-root cases
and144 empty cases. A source-ID one-hole paid fixture is separately
checked, without calling it the exact partial10 map of that word.
Source eligibility for every ACTUAL supplied fE is a universal parametric
common-path-stability proof, not numerical substitution of these maps.

A different BACKWARDS checker reconstructs partial/common exchange and
free endpoints from inverse h edges. It checks{ind['generic_owner_cases']}
generic paid-map cases (zero14976, one31104, two16128), including tight
and spare unit inventories. Separately{owner['cases']} exact-common-set
completion cases cover zero136080, one188352, two41544 residuals;
1440 cases have two blocked nonanchor roots,113616 have both seeds
already owned. All old successful paths/values remain identical and
simultaneous extension equals the LICENSED original complete h/l exchange.
Sequential addition gives the same second endpoint. The three-hole384
MAP checks are algebraic Gate U12 controls only, not a source campaign.

Required historical replay is unchanged:1856 source-period rows, including
Sigma45/46/reflections, original Gamma26 actual cuts/donors, all prior
18 original/reflected source controls,06 terminal-pair controls,08 neutral
tail,09 all62 sectors/aliases/reflected4858 frames and10 families/erasures.
All outputs are redirected into12; no old artifact is rewritten.

Authoritative checkers: audit_construction2.py, audit_independent3.py,
audit_ownership.py, audit_controls.py and final audit_seal.py. The initial
construction draft incorrectly required asymmetric branches from a
symmetric repeated-word fixture; the source/funding checks had passed,
but its branch assertion failed. Independent draft1 had a syntax error;
draft2 passed source replay then mishandled integer generic IDs. These
drafts are preserved, superseded and fully charged, never PASS evidence.

This is SAME-agent distinct-implementation auditing plus explicit
mathematical proof, not external peer review or formal proof-assistant
certification. No finite control implies universality or unrestricted CD6.
''')
    out('ADVERSARIAL_AUDIT.md',f'''# Adversarial source/owner audit

The physical seed witness is NOT presumed free. Exact common-lock
completion controls include{owner['seed_bits_already_owned']['2']} cases
with both seed bits owned and{owner['blocked_anchor_counts']['2']} with
two blocked roots anchored at common excess slots. Disjoint terminating
owner paths yield distinct free terminals while all old values stay fixed.

Naively selecting the same first free bit independently for both demands
duplicates its physical ID; ownership_audit.json retains an actual-source-ID
illustration with logical owners. It rejects that heuristic only and is
NOT claimed as a numerical sealed-fE source counterexample. The accepted
construction chooses distinct predecessor seeds and a joint common receipt.

Duplicate donor, outside-period donor and three-residual public-allocator
input are explicitly rejected. All actual cut transports preserve both
endpoints. Gamma26 still uses(10,3,0/1) for(9,1),(13,5) in one permitted
copy; forbidden cut12 is not used. Sigma45/46 still refutes its old
two-bit adjacent-predecessor rule; this core7 construction needs just one
bit at each distinct predecessor and does not generalize that failed rule.

Private BST tests instantiate all eight ordered gaps with three private
keys each, sparse Score labels, reflection and an A-only private-helper
excursion followed by its inverse root zig. Its two actual A events are
retained, BF/BE freeze and all full pairs close. Early DELETE events
and zero-cost root repeats also retain original IDs/charts/erased replay.

Zero/one Splus is structurally impossible, not merely absent from tests.
Any perceived single-donor bottleneck is contradicted by the two licensed
disjoint endpoint paths, not a raw-spare count. Every actual full B
double—including a chart correction's physical double—is in D exactly
once; debt differences are not new events or credit. No old normalized
changing-chart M3 potential is resurrected.

Failed drafts: run_construction_result.json, run_independent_result.json,
run_independent2_result.json remain FAILED_OR_UNKNOWN, not promoted.
Their precise test-coverage/syntax/integer-representation errors and later
accepted versions are in artifact_status_ledger.json; all CPU and source
calls are charged. No failed source lifting/ownership premise or exact
main-theorem/CD(6) counterexample was produced.
''')
    gates={
        'L1':'fixed source core/pruning/macro coverage, all5 masks and arbitrary gaps',
        'L2':'literal10 alpha:Pstar->R, own and blocked-common anchor cases',
        'L3':'empty Pstar returns a unchanged',
        'L4':'one residual handled by actual complete TWO-slot h',
        'L5':'simultaneous fixed-a disjoint owner paths',
        'L6':'distinct predecessors -> distinct seed IDs -> distinct endpoints',
        'L7':'all original common fE values fixed by exact licensed exchange',
        'L8':'all old successful partial paths and endpoints identical',
        'L9':'actual specified(t,j,b) in source predecessor list',
        'L10':'complete original common-set h/l receipt licenses all new pairs jointly',
        'L11':'Splus>=2 by two actual distinct predecessor contributions',
        'L12':'construction covers/excludes E1-E6 and adversarial A-J',
        'L13':'disjoint two-block stream and both-ID transport to fixed I',
        'L14':'free-tree LL/RR induction, actual helpers and finite-path termination',
        'L15':'distinct immutable source engine plus backwards owner verifier and historical controls',
        'L16':'literal final map a union fstar, complete injective and all prior values fixed'}
    out('completion_gates.json',{'status':'L1_L16_AND_A_L_PASS','gates':{k:{'status':'PASS','evidence':v} for k,v in gates.items()},
        'A_to_L':{k:'PASS_DECLARED_SOURCE_AND_OWNERSHIP_INTERFACE' for k in 'ABCDEFGHIJKL'},'Gate_U12':'U-B',
        'trust':'mathematical proof with same-agent independent implementation audit, not formal or external certification'})
    out('artifact_status_ledger.json',{
        'physical_receipts2.json':'AUTHORITATIVE actual A/BF/BE/source/owner fixtures',
        'independent_audit.json':'AUTHORITATIVE output of audit_independent3.py',
        'ownership_audit.json':'AUTHORITATIVE simultaneous licensed-common completion check',
        'geometry_certificate.json':'AUTHORITATIVE regenerated complete necessary grammar, exact11 equality',
        'historical_controls.json':'AUTHORITATIVE required fresh controls, all old statuses unchanged',
        'audit_construction.py':'SUPERSEDED failed symmetric-fixture branch assertion after all source/funding checks;8064 calls charged',
        'audit_construction2.py':'AUTHORITATIVE revision; no asymmetric branch realization inferred',
        'audit_independent.py':'SUPERSEDED syntax error before source calls; entire child/controller charged',
        'audit_independent2.py':'SUPERSEDED integer generic-ID TypeError after all source checks;9667 calls charged',
        'audit_independent3.py':'AUTHORITATIVE correction plus all generic checks PASS',
        'all_fixture_fE':'LOGICAL test placements, not actual numerical sealed-fE claims',
        'old11_artifacts':'UNCHANGED, all original manifests/pins verified'})
    receipts=[]
    for f in src['families']:
        for v in f['fixtures']:
            receipts.append({'variant':f['variant'],'reflected':f['reflected'],'erased':f['erased'],'fixture':v['label'],
                'physical_R':f['R'],'source_seeds':f['seed_receipts'],'residual_roots':v['uncovered'],
                'certified_neighborhood_subrelation':v['additions'],'joint_paths':v['extension_paths'],
                'ownership':'all prior paid and common values fixed',
                'eligibility_receipt':'original complete h/l on same C, old successful paths identical',
                'fixture_status':'logical owner placement on actual closed source IDs, not numerical sealed fE'})
    out('joint_donor_certificate.json',{'status':'JOINT_CERTIFIED_SOURCE_ELIGIBILITY_SUBRELATION',
        'not_claimed':'exhaustive static eligibility graph or numerical fE realizations','receipts':receipts,
        'universal_licensing':'FULL_PROOF.md sections3-5, independent of finite placements'})
    out('two_slot_certificate.json',{'status':'C7_TWO_SLOT_FUNDING_PROVED','terminal_outcome':'A',
        'domain':'original admissible six-genuine-KEEP full-core7 actual aligned I with exactly TWO physical R slots',
        'source_supply':'distinct critical macros -> distinct noncritical Q<=1 actual predecessors -> specified distinct own-unused bits',
        'independent_full_map':'h extends h0 only at both actual R slots, working<=4, legal period transport',
        'simultaneous_ownership':'disjoint terminating paths against fixed a; original common h/l exchange keeps every old path/value',
        'residual_cardinalities':[0,1,2],'zero_one_raw_surplus':'IMPOSSIBLE_BY_SOURCE',
        'eligible_edge_policy':'original actual counting/block-cyclic receipt, no new strict native timing/key-match policy',
        'full_proof_sha256':sha(B/'FULL_PROOF.md'),'independent_audit_sha256':sha(B/'independent_audit.json'),
        'ownership_audit_sha256':sha(B/'ownership_audit.json'),'source_receipts_sha256':sha(B/'physical_receipts2.json'),
        'allocator_sha256':sha(B/'two_slot_allocator.py'),'Gate_U12':'U-B',
        'unrestricted_core7':'OPEN_NOT_EXECUTED','CD6':'OPEN','Step2':'OPEN','Step3':'OPEN','Dynamic_Optimality':'OPEN'})
    out('research_status_ledger.json',{'C7_TWO_SLOT_FUNDING':'PROVED_UNIVERSAL_AT_DECLARED_SOURCE_INTERFACE',
        'C7_ONE_SLOT_FUNDING':'PROVED_UNCHANGED','two_slot_zero_one_Splus':'IMPOSSIBLE_UNIVERSAL_SOURCE',
        'simultaneous_finite_owner_exchange':'PROVED_PARAMETERIZED_SUFFICIENT_THEOREM','Gate_U12':'U-B',
        'arbitrary_support_source_supply':'OPEN','unrestricted_core7':'OPEN_NOT_EXECUTED',
        'other_cores':'OPEN_NOT_EXECUTED','Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'old_changing_chart_normalization':'REFUTED_UNCHANGED','old06_09':'PROVED_EXACT_SCOPES_UNCHANGED',
        'old10_full_funding':'UNRESOLVED_UNCHANGED','Campaign13':'NEXT_NOT_EXECUTED',
        'external_review':False,'formal_proof_assistant':False})
    print(json.dumps({'status':'PROOF_CERTIFICATE_METADATA_READY','L_gates':len(gates),'joint_source_fixture_receipts':len(receipts)}))
def after():
    e=read('entry.json');total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);phases=[]
    failed={'construction','independent','independent2'}
    for p in sorted(B.glob('run_*_result.json')):
        r=json.loads(p.read_text());c=read('controller_'+r['phase']+'_exit.json');ph=r['phase']
        if ph in failed:assert r['status']=='FAILED_OR_UNKNOWN'
        else:assert r['status']=='PASS' and not c['error']
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge
        semantic={'construction2':'physical_receipts2.json','independent3':'independent_audit.json','ownership':'ownership_audit.json'}.get(ph)
        tests=read(semantic).get('new_finite_tests',0) if semantic else r['new_finite_tests']
        phases.append({'phase':ph,'status':r['status'],'accepted':ph not in failed,'group':r['group'],
            'child_CPU':r['child_CPU'],'whole_controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,
            'source_calls':r['source_engine_calls'],'finite_control_count_from_semantic_receipt':tests,
            'historical_period_rows':r['old_semantic_rows_replayed']})
    assert total<7195 and all(groups[g]<e['group_caps'][g] for g in groups)
    assert read('seal_audit.json')['terminal_outcome']=='A'
    out('resources_checkpoint.json',{'status':'ALL_EXISTING_CAPS_PRESERVED_ALL_RUNS_CHARGED',
        'prior_CPU':e['prior_uniform_CPU'],'cumulative_CPU':total,'ceiling':7200,'required_reserve':5,
        'remaining_CPU':7200-total,'available_before_reserve':7195-total,'cumulative_group_CPU':groups,
        'group_caps':e['group_caps'],'remaining_group_CPU':{g:e['group_caps'][g]-groups[g] for g in groups},
        'phases':phases,'campaign_source_engine_calls':sum(v['source_calls'] for v in phases),
        'query_live_cap':2000000,'DAG_cap':4000000,'edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
        'no_reset':True,'failed_drafts':'all child/controller CPU and all completed source calls retained',
        'metadata_convention':'unchanged inherited entry/provenance/prose/publication exclusion; all proof/replay/ownership/seal child and whole controller CPU charged',
        'this_publication_metadata_CPU_excluded':time.process_time()})
    out('publication_receipt.json',{'status':'PASS_C7_TWO_SLOT_OUTCOME_A','branch':e['branch'],'HEAD':e['head'],
        'tracked_status':'','old_worktree':'all research preserved; writes only new12',
        'terminal_outcome':'A','theorem':'C7_TWO_SLOT_FUNDING','Gate_U12':'U-B',
        'scope':'exactly TWO physical slots only','Step2':'OPEN','CD6':'OPEN','Campaign13':'NEXT_NOT_EXECUTED',
        'CPU':total,'remaining_CPU':7200-total})
    files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.rglob('*')) if p.is_file()]
    out('campaign_manifest.json',{'status':'SEALED_C7_TWO_SLOT_OUTCOME_A','branch':e['branch'],'HEAD':e['head'],
        'files':files,'self_hash':'excluded from own file list; console verification provides manifest SHA256',
        'theorem':'C7_TWO_SLOT_FUNDING','Gate_U12':'U-B','Step2':'OPEN','CD6':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
    assert all(sha(ROOT/v['path'])==v['sha256'] for v in files)
    print(json.dumps({'status':'ALL_MANIFEST_BYTES_VERIFIED_OUTCOME_A','files':len(files),
        'manifest_sha256':sha(B/'campaign_manifest.json'),'cumulative_CPU':total,'remaining_CPU':7200-total,'groups':groups}))
if __name__=='__main__':{'before':before,'after':after}[sys.argv[1]]()
