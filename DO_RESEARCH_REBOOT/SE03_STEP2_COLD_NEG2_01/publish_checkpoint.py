"""Publish exact refutation, all attempted charges, and inspected source pins."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;started=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def prose(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def main():
    e=read(B/'entry.json');pins=read(B/'dependency_pins.json')
    for p in pins['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    for p in pins['external_pins']:assert sha(Path(p['path']))==p['sha256']
    assert len(pins['pins'])==e['pins_verified']==1455
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==e['head']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
    proof=read(B/'source_proof_audit.json');classification=read(B/'classification_audit.json')
    assert proof['status']=='PASS_INDEPENDENT_UNIVERSAL_SOURCE_COUNTERCERTIFICATES'
    assert classification['terminal_outcome']=='B_NORMALIZATION_REFUTED'
    data=read(B/'symbolic_replay.json')
    # Exact Hamiltonian SOURCE topology, not only a root/height guess.
    r9=None
    for k in range(8,-1,-1):r9=[k,None,r9]
    for f in data['families']:
        assert f['old_chart']['tree']==r9
        assert [f['old_chart']['Scores'].index(x) for x in f['old_chart']['marks']]==[0,2,4,6,8]
        if f['name']!='Gamma_pair':assert f['old_A_shadow_known_real_Scores']['R']=={'kind':0,'isS':True,'index':2,'key':3}
    extra={g:0 for g in e['inherited_group_CPU']};attempts=[];finite=calls=0
    for p in sorted(B.glob('run_*_result.json')):
        r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];extra[r['group']]+=charge
        finite+=r['new_finite_tests'];calls+=r['source_engine_calls']
        attempts.append({'phase':r['phase'],'group':r['group'],'status':r['status'],
            'child_CPU':r['child_CPU'],'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,
            'allocated_child_cap':r['allocated_child_cap'],'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed'],
            'new_finite_tests':r['new_finite_tests'],'source_replay_calls':r['source_engine_calls']})
        assert r['termination'] is None and r['old_semantic_rows_replayed']==0
    statuses={p['phase']:p['status'] for p in attempts}
    assert set(statuses)=={'replay','debt','debt_v2','debt_v3','independent','source_proof','masks','classification'}
    assert {p for p,s in statuses.items() if s!='PASS'}=={'debt','debt_v2'}
    assert finite==101 and calls==11256
    total=e['prior_uniform_CPU']+sum(extra.values())
    groups={g:{'inherited_CPU':e['inherited_group_CPU'][g],'new_CPU':v,
        'combined_CPU':e['inherited_group_CPU'][g]+v,'cap':e['group_caps'][g]} for g,v in extra.items()}
    assert total<7195 and all(v['combined_CPU']<v['cap'] for v in groups.values())
    out('resources_checkpoint.json',{'prior_uniform_CPU':e['prior_uniform_CPU'],
        'new_CPU_all_children_and_whole_controllers':sum(extra.values()),'cumulative_uniform_CPU':total,
        'global_allowance':7200,'required_reserve':5,'remaining_CPU_including_reserve':7200-total,
        'original_SE03_phase_groups':groups,'attempts':attempts,'failed_drafts_included':True,
        'new_finite_tests':finite,'source_replay_calls_including_symbolic':calls,
        'source_tests_authorized_by':'current user Gate E','old_semantic_rows_replayed':0,
        'new_canonical_solver_queries':0,'canonical_query_cap':2000000,'live_record_cap':2000000,
        'DAG_cap':4000000,'stored_edge_cap':5000000,'new_weighted_graphs':0,'new_solver_runs':0,
        'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'old_signature_ledger_unchanged':7195.203125,
        'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True})
    dependencies=[
        ('ORIGINAL_PIPELINE.md','SOURCE DEFINITION','full definitions inspected; historical OPEN status not used to overwrite sealed later CD5'),
        ('RESEARCH_RULES.md','SOURCE DEFINITION','full permanent rules inspected'),
        ('CD5_BASE01/CD5_PROOF.md','PROVED—UNIVERSAL at support<=5','full proof inspected, leaf theorems reused'),
        ('M3_XFER21/FULL_M3_PROOF.md','PROVED—UNIVERSAL frozen M3','formula refreshed; complete proof previously inspected and reused'),
        ('M3_XFER16/debt_definition.json','PROVED—RESTRICTED ceiling and SOURCE DEFINITION','literal sole downward ceiling inspected; no global Lambda floor assumed'),
        ('M3_XFER17/debt_definition.json','PROVED marked-root normalization','proper-marked predicate/formula inspected'),
        ('M3_XFER18/debt_definition.json','PROVED current debt augmentation','explicit max formula inspected'),
        ('M3_XFER19/STEP4_CERTIFICATE.json','PROVED Step4 certificate','formula and accepted clause guards inspected; completed checks not replayed'),
        ('M3_XFER21/audit_extremal.json','PROVED accepted completion clauses via final seal','accepted4359-clause data reused; source generator inspected, not executed'),
        ('M3_LDR01/negative_run_census.json','FINITE-EXACT frozen topology/psi facts','read-only facts reused; no regeneration'),
        ('M3_H1F01/cheap_census.json','FINITE-EXACT frozen depth/destination facts','read-only facts reused; no regeneration'),
        ('SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','PROVED—UNIVERSAL auxiliary domain','full physical allocation proof inspected'),
        ('SE03_STEP1_FUND01/SOURCE_IDS_AND_CYCLIC_CUT.md','PROVED period transport','full proof inspected'),
        ('SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED—UNIVERSAL actual closed B sources','set-growth, label counting and prefix proof inspected'),
        ('SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED maximum-depth successor','full fan and disjoint-packet proof inspected'),
        ('SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md','PROVED source family/necessary range','full source W_r,H_r and Gamma proof inspected'),
        ('SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md','PROVED partition; proposed D OPEN','exact partition and modified Gamma witness inspected'),
        ('SE03_STEP2_REPAY02/CHECKPOINT.md','OPEN Step2; prior candidate REFUTED','full current local checkpoint inspected'),
        ('SE03_STEP2_REPAY02/NINE_SCORE_SOURCE_BRIDGE.md','PROVED—UNIVERSAL fixed actual nine Scores','full source embedding proof inspected'),
        ('SE03_STEP2_REPAY02/COLD_EXCHANGE_IDENTITY.md','PROVED identity; sign comparison OPEN','full signed source interface inspected, -1 retained'),
        ('SE03_STEP2_REPAY02/RECENT_SUPPORT_COVER.md','PROVED actual recent-key cover','full source proof inspected'),
        ('SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','PROVED—UNIVERSAL auxiliary reservation domain','full proof inspected; gE not identified with fE'),
        ('SE03_STEP2_REPAY02/HAMILTONIAN_DEBT_NORMALIZATION.md','PROVED fixed-chart preservation; changing-chart candidate now REFUTED','full exact Hhidden/proof inspected'),
        ('SE03_STEP2_REPAY02/RAY_NORMALIZATION_AND_OBSTRUCTION.md','PROVED fixed-chart ray ceiling and actual Omega obstruction','full source/debt proof inspected; old/new normalization distinguished'),
        ('SE03_STEP2_REPAY02/PERSISTENT_OMEGA_EXTENSION.md','PROVED—RESTRICTED actual arbitrary-fringe family','full closure/recurrence/old receipt proof inspected'),
        ('SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED actual closed maximal sources','full source mass/persistence proof inspected; not a frozen graph filter'),
        ('SE03_STEP2_DONOR06/CHECKPOINT.md','OPEN Step2, Step3 and Universal CD','latest local status inspected, not replaced by remote history')]
    index={p['path']:p['sha256'] for p in pins['pins']}
    ledger=[]
    for name,status,inspection in dependencies:
        p=B.parent/name;rel=p.relative_to(ROOT).as_posix();h=sha(p)
        assert index[rel]==h,rel
        ledger.append({'path':rel,'sha256':h,'status':status,'inspection':inspection})
    for rel in ['python/independent/splay.py','python/independent/pair.py']:
        assert index[rel]==sha(ROOT/rel)
        ledger.append({'path':rel,'sha256':index[rel],'status':'SOURCE DEFINITION',
            'inspection':'full source inspected; trace used, depth+1 pair cost functions NOT used'})
    out('dependency_status.json',{'dependencies':ledger,'external_IAGS_spec':pins['external_pins'],
        'missing_critical_prerequisites':[],'changed_chart_universal_inequality':'REFUTED, never inherited as a premise'})
    table='\n'.join('| `'+q['path']+'` | '+q['status']+' | '+q['inspection']+' | `'+q['sha256']+'` |' for q in ledger)
    prose('SOURCE_SPEC.md',f'''# Frozen original source and normalized COLD-NEG2 specification

Repository Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity.
Local branch coarse-double-branch, HEAD {e['head']}.
Tracked tree clean at entry and publication; substantial PRE-EXISTING
untracked research is preserved. Complete entry dirty-tree listing is
in entry.json. No fetch/pull/checkout/reset/stash/commit or overwrite.
Latest local DONOR06 and earlier source proofs are used, not an older
remote snapshot. All1455 inherited/local pins and the external IAGS
specification hash verify. New files exist only in this campaign folder.

Original model: any finite ordered present-key set, any common initial
BST diagonal, actual ordinary parent-first bottom-up splays. KEEP acts
in A and full B; DELETE acts only in A, never deletes a key. Erasing z
changes Kz to Dz and preserves the ENTIRE actual A trajectory. Costs are
a=ceil(dA/2), q=floor(dB/2) on KEEP, q0 on DELETE. A DOUBLE and terminal
ZIG each count one A StepEv; only DOUBLE contributes B q. The read-only
engine's depth+1 convenience pair costs are NOT used.

Domain: original reachable finite exactly labeled paired-closed histories
with six genuine KEEP keys. Full B core S is fixed,6<=|S|<=11. Natural
FULL macros end at genuine full KEEPs and retain all intervening actual
operations. Pair every core11 q5 with its actual forced q1 successor;
all others are singletons. w=2min(H,4)-Q, with H actual A StepEvs.
NEG2_CLASSIFICATION.md proves the exact two negative-two classes.

The actual cyclic most-recent-five distinct KEEP set determines chart
marks before/after each packet. At core11 its actual ancestor core is
exactly nine physical Scores; no choice of representative is allowed.
At core10 the established padding is S minus the omitted recent key.
Core9 is not silently excluded from the cost classification; a global
padding convention there remains outside the present counterproof.

Candidate EXACTLY as requested: D is the sealed original fixed-nine-Score
debt in[0,2]. On a Hamiltonian nine-Score B skeleton, Hhidden means NO
marked SECOND/THIRD path Score is visible at an authorized NONROOT alpha
point with kind0,isS=true,index that role. Set Dhat0 when Hhidden,
min(D,1) at other Hamiltonian states, and D elsewhere. The literal R
observation of marked role2 in both counterexamples makes Hhidden false.
No new safe maximum is combined with this formula. The fixed-chart
incoming-Hamiltonian q<=1 lemma is not applied to a changing-chart miss.

Target: for EVERY source-valid COLD packet w-2, Dhat_old0 and Dhat_new2,
equivalently residual0. This is now REFUTED—EXACT by actual closed source
members of both classes. No critical source prerequisite was unavailable.
Normalized fixed-chart preservation remains proved at its own scope.

The density audit needs nonempty V, present target x and the rooted
ancestor core. If x is already in C_V, all operands are in that core and
outside hangers are V-free. If x is outside, the first frame touching
the last core ancestor introduces at most x and its next outside child p;
deeper processed pieces are V-free. This is SET inclusion, not a cardinal
surrogate. First visits into a source subtree count labeled introductions
over a FULL period; no fixed-subtree dynamic assumption is used. This
establishes the sorted odd mask at core11 and necessary16 P-bit masks
at core10, not the dynamic realization of every such mask.

R1-R4 preserve original semantics, full closure, signed costs, actual IDs,
ownership, frozen graph/raw states/observables/solver/private scopes,
shared midpoint, matching-terminal, corrected h0 and Bank25=25. The
CURRENT Gate E explicitly authorizes bounded actual source replays;
it supersedes the older no-replay restriction only for these checks.
All cumulative resource caps remain. No universal graph/solver is built.

IAGS uses the inspected original specification section24: Freeze,
Inherit, Alter, Recurse, Create/New Lemma, Reconstruct, Close/Reopen.
IAGS_BOXES.md records the exact child implications and strategic status.
Research-quality rules in RESEARCH_RULES.md are distinct from the source
R1-R4 contract. Success here is candidate elimination, not positive CD
coverage. Existing source receipts and unused reservations are unchanged.

## Inspected dependency ledger

| Exact repository path | Status | Inspection/reuse attribute | SHA256 |
|---|---|---|---|
{table}

External original IAGS specification: `{pins['external_pins'][0]['path']}`,
SHA256 `{pins['external_pins'][0]['sha256']}`. Only its declared sections
are used. Source precedence and prior corrected status distinctions remain.

## Acyclic dependency graph

```mermaid
graph TD
  Density[Closed-source density] --> Pair[Maximum-depth q5/q1 pairing]
  Pair --> Class[Exact price-2 classification]
  M3[Sealed fixed-chart M3] --> Floor[Scoped debt floors and range]
  M3 --> Bridge[Actual nine-Score local bridge]
  Norm[Literal Hamiltonian-Hhidden formula] --> Old[Source normalized debt1]
  Floor --> Old
  Source[Original closed Omega and Sigma source identities] --> Cold[Actual cold price-2 packets]
  Class --> Cold
  Bridge --> Target[Target <=2; Sigma exactly2]
  Old --> Refute[COLD-NEG2 candidate refuted]
  Target --> Refute
  Cold --> Refute
```

There is no dependency on CD6, Universal CD, desired donor cardinality,
unproved chart comparison or the full Step2 conclusion.
''')
    out('RESULT.json',{'outcome':'B_NORMALIZATION_REFUTED','statement':'COLD-NEG2 CANDIDATE REFUTED. This is not a counterexample to Coarse-Double.',
        'NEG2_P':'REFUTED_EXACT_ORIGINAL_CLOSED_SOURCE','NEG2_S':'REFUTED_EXACT_ORIGINAL_CLOSED_SOURCE',
        'Gamma_control':[0,2,0],'Omega_plus':{'source_Dhat':1,'target_interval':[1,2],'residual_interval':[-2,-1],'A':48,'QF':32,'slack':64},
        'Sigma_singleton':{'source_Dhat':1,'target_Dhat':2,'residual':-1,'A':95,'QF':42,'slack':148},
        'arbitrary_fringe_source_proofs':True,'counterexamples_to_generic_width2_architecture':False,
        'new_full_allocator':False,'old_allocations_changed':False,'Bank25':25,
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'independence':'same-agent independent source representations and frozen engine; not external review or complete compiler formalization'})
    prose('CHECKPOINT.md',f'''# OUTCOME B — normalized COLD-NEG2 candidate refuted

COLD-NEG2 CANDIDATE REFUTED. This is not a counterexample to Coarse-Double.

Current branch coarse-double-branch; HEAD {e['head']}.
Tracked tree clean; pre-existing untracked research preserved. All1455
dependency pins and external IAGS hash verify. Full source/provenance,
statuses, inspection attributes and hashes are in SOURCE_SPEC.md.

Both declared negative-two classes have original reachable fully paired-
closed arbitrary-fringe counterfamilies. Omega_plus's actual q5/q1 packet
has H2,Q6 and normalized source1,target in[1,2], residual[-2,-1]. New Sigma's
single cold K7 at occurrence47 has H1,Q4 and exact debt1->2, residual-1.
Modified Gamma_pair remains0->2 with residual0. No candidate was patched.

NEG2_CLASSIFICATION.md proves the exhaustive source COST partition,
including nongenuine KEEPs, zero operations, seam pairing, core9/10/11
and auxiliary/full disagreement. NEG2_PAIRED.md and NEG2_SINGLETON.md give
the complete proofs and words. SOURCE_REPLAY.md plus its later ADDENDUM
give deterministic tests, full event/chart records, independent universal
free-term checks, all16 necessary-mask controls and the two rejected
audit drafts. COLD_NEG2_FINAL.md gives all Gate A-G outcomes and scope.

There are101 authorized finite source checks,11256 source replay calls
including symbolic identities, no new solver queries/weighted graph and
no old symbolic semantic-row replays. Six promoted phases PASS; two
earlier debt-audit drafts FAILED and are retained/charged, never used as
evidence. The independent audit is same-agent separate derivation using
the frozen source engine, not external peer review/full formalization.

Original slacks: Omega_plus64, Sigma148, Gamma42, all positive. Witness
packet-path minima are-2, not below-2. Therefore only THIS normalization
is refuted; an arbitrary width-two full-source potential is not refuted.
No new physical allocation or donor ownership theorem is claimed.

R1-R4, original source/raw graph/h0/private scopes/shared midpoint,
matching-terminal, all allocations and Bank25=25 remain. The current
Gate E authorization permits these replays without another permission
flow. CPU {total:.6f}/7200, remaining {7200-total:.6f} including reserve5.
Original cumulative groups symbolic {groups['symbolic']['combined_CPU']:.6f}/120,
independent {groups['independent']['combined_CPU']:.6f}/300. All proof
children, FAILED drafts and whole controllers are charged. Other caps
remain2M queries/live records,4M DAG,5M edges,32GiB,12h/phase. No reset,
raise or exhaustion is claimed.

Step2, CD6, Step3, Universal CD and Dynamic Optimality remain OPEN.
Next bounded target: actual H1 zero/+1 incoming compatibility of the
forced-zero NEG2-source region, BEFORE proposing any source-lowering
repair. Its exact statement and limitations are in COLD_NEG2_FINAL.md.
No successor campaign has been run.
''')
    out('final_integrity.json',{'status':'PASS_EXACT_REFUTATION_AND_LIMITED_SCOPE','head':e['head'],'branch':e['branch'],
        'tracked_tree_clean':True,'inherited_pins_verified':1455,'external_IAGS_hash_verified':True,
        'R1_R4_preserved':True,'Bank25':25,'old_allocations_changed':False,
        'promoted_phases_pass':6,'failed_drafts_retained':2,'outcome':'B_NORMALIZATION_REFUTED',
        'source_replay_count':calls,'finite_tests':finite,'metadata_CPU_excluded':time.process_time()-started})
    files=sorted(p for p in B.iterdir() if p.is_file())
    out('checkpoint_manifest.json',{'kind':'exact original-source refutation of a specified normalized debt candidate',
        'files':[{'file':p.name,'sha256':sha(p)} for p in files],'outcome':'B_NORMALIZATION_REFUTED',
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print(json.dumps({'status':'OUTCOME_B_NORMALIZATION_REFUTED','pins_verified':1455,'files_pinned':len(files),
        'CPU':total,'finite_tests':finite,'source_replays':calls,'Step2':'OPEN'}))
if __name__=='__main__':main()
