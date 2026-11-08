"""Publish cumulative metadata and exact research status; no semantic run."""
import collections,hashlib,json,subprocess,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];ROOT=P.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def main():
    e=json.loads((B/'entry_authorized1680_audit720_q3050000.json').read_text());tot=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);q=e['inherited_conservative_queries'];runs=[]
    for p in sorted(B.glob('run_*_result.json')):
        r=json.loads(p.read_text());cp=B/('controller_'+r['phase']+'_exit.json');assert cp.exists();c=json.loads(cp.read_text());charge=r['child_CPU']+c['whole_process_CPU_seconds']
        tot+=charge;groups[r['group']]+=charge;q+=r.get('source_queries',0);runs.append({'phase':r['phase'],'group':r['group'],'charge':charge,'status':r['status'],'queries':r.get('source_queries',0)})
    assert tot<7200 and groups['symbolic']<1680 and groups['independent']<720 and q<=3050000
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    status=git('status','--porcelain=v1');lines=status.splitlines();tracked=[s for s in lines if not s.startswith('??')]
    provenance={'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'tracked_changes':tracked,
      'untracked_status_entries':len(lines)-len(tracked),'all_existing_untracked_artifacts_preserved':True,
      'note':'status counts collapsed untracked directories as git reports them; no destructive operation or frozen certificate edit'}
    assert provenance['head']==e['head'] and provenance['branch']==e['branch'] and not tracked
    source_paths=[P/'SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md',P/'SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md',
      P/'SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md',P/'SE03_STEP2_UNARY_A_LIFT_14/FULL_PROOF.md',
      P/'SE03_STEP2_UNARY_A_LIFT_14/branch_core11_mask0.json',P/'SE03_STEP2_UNARY_A_LIFT_14/branch_grammar2.json',
      P/'SE03_STEP2_UNARY_A_LIFT_14/branch_all_independent_audit.json',
      B/'native10_source_actions.json',B/'native10_source_independent_audit.json',B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',
      B/'audit_core39.py',B/'audit_verify79.py',F.parent/'CONTINUATION_02/GLOBAL_FULL_H_AND_FROZEN_EXCHANGE.md']
    manifest={'provenance':provenance,'inherited_sources':{str(p):{'sha256':sha(p),'exists':True,'proof_inspected_or_accepted_receipt_reused':True} for p in source_paths},
      'campaign_files':{p.name:sha(p) for p in sorted(F.iterdir()) if p.is_file() and p.name not in ('dependency_manifest.json','resources_checkpoint.json')},
      'new_full_source_scope':'seven genuine KEEP keys, fixed full B marked core13, arbitrary A/private/helper populations',
      'root_JR35':'OPEN','reservation_compatibility':'DEFERRED','unconditional_Gate_U':'OPEN','Universal_CD':'OPEN'}
    put(F/'dependency_manifest.json',manifest)
    resource={'provenance':provenance,'controller':str(B/'run_phase_1680_audit720_q3050000.py'),
      'entry_sha256':sha(B/'entry_authorized1680_audit720_q3050000.json'),
      'cumulative_global_CPU_before_publication':tot,'cumulative_group_CPU_before_publication':groups,
      'global_cap':7200,'group_caps':e['group_caps'],'source_queries':q,'query_cap':3050000,'query_remaining':3050000-q,
      'global_reserve':5,'controller_reserve':1,'new_named_phase_CPU_cap':20,'query_batch_cap':50000,
      'Bank25':25,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_GiB':32,'wall_hours':12,
      'usage_reset':False,'failed_runs_retained_and_charged':True,
      'publication_charge':'add run_proof227_result.json child plus controller_proof227_exit.json; this receipt is a before-publication snapshot',
      'all_run_receipts':runs}
    put(F/'resources_checkpoint.json',resource)
    checkpoint=f'''# C35 / continuation04 — current checkpoint

Root Joint Repayment remains **OPEN**. Reservation compatibility remains
**DEFERRED**, in the requested order. No C35/UCF35, universal CD, or Dynamic
Optimality completion is claimed. No original-source counterexample with
Q_B>2A has been found. This checkpoint does not claim resource exhaustion.

Branch `{provenance['branch']}`, HEAD `{provenance['head']}`. Tracked worktree
unchanged; historical and new untracked research artifacts are preserved.
Exact dependency hashes are in dependency_manifest.json.

## Completed new source certificate

JR35-MAX7 covers EVERY original paired-closed source with seven genuine
KEEP keys and full B marked core13, arbitrary A anonymous/unary/private
populations, arbitrary helpers and word lengths. Complete B grammar3876;
A branch grammar5947; complete H1/H2 relations12400/64654. Independent H2
coverage intervals[0,1100),[1100,5100),[5100,5947) are all complete. Every
q6 macro has its actual q1 successor; all126 sectors and full endpoints
are retained. The signed certificate has D in[0,4], min(H,4) packet budget,
working bank<=12, literal h0, and empty closing carry. Distinct checker
passed53,357,044 LOW and13,246 HIGH inequalities. Read
SEVEN_KEY_MAXIMAL_CORE_FULL_PROOF.md and independent_paired_branch_certificate.json.
This is not full I7 while the original external reservation chi is open.

## New universal smaller statements and exact failures

- CCR35: cluster-collateral repayment on disjoint blocks under its explicit
  source delta>=Q+L hypothesis, with L<=23 for the stated Bank25 schedule.
  New actual closed dirty source has22 demands,16 h0 owners,6 loans, bank5;
  both recovery terminal KEEPs have a=0, with their positive helper costs
  retained. Independent full A/B/BE/chart/owner replay passes.
- Maximal-completion shortcut refuted by the cyclic word1,13,3,11,5,9,7:
  all144 possible root7 maximal starts leave the legal grammar in one copy.
  A real nonmaximal closed source with that word has A13,Q8, not a CD failure.
- LP35: ANY function of full B and all leaf-indexed inherited D6 values
  fails even with literal q6/q1 packets:21-edge price-2 source-profile cycle.
  Independent replay47 calls. No concatenated negative actual source path.
- JC35: exact rational source-inequality certificate refutes the specified
 14-feature linear joint cluster class, weighted price-1417/2118; independent
  checker18 new calls and reuse of accepted actions. No root counterexample.
- SP35/FD35: uniform written proofs exclude separable source-pair potentials
  and EVERY fixed A-prefix depth for sufficiently large support. FD35 also
  applies to the A branch quotient: the anchors are genuine marked keys.
  A separate shorter proof/review and distinct source controls are retained.
  No finite passing replay is substituted for the universal proof.
- RT35: one balanced two-interval rank update per ACTUAL rotation bit,
  valid at arbitrary depth/population. Full B target paths are heavy after
  A's target access. These tokens are not additional free credits.

## Smallest active source obligation

RT35_JOINT_FROZEN_OBLIGATION.md: derive a joint source interval/owner charging
rule whose augmentations always reach distinct usable ORIGINAL bits while
preserving natural h0, actual period and Bank25. Prove the endpoint and
global noncollision from source rotations; do not substitute Hall's global
cardinality statement. Locked h0/fE bits are not assumed free. Full h's
additional original reservation compatibility is still the later task.

The unrestricted complement still includes arbitrary seven-key cores9–12
and arbitrary supports>=8 outside the exact already covered subdomains.
Do not simply enumerate larger fixed populations or reuse a bounded-depth
formula: neither supplies the required uniform bridge.

## Resources

Authorized cumulative caps: symbolic1680, independent720, global7200 CPU
seconds; queries3,050,000; batches50,000; every other cap and Bank25 fixed.
Before this publication: global{tot}, symbolic{groups['symbolic']},
independent{groups['independent']}; queries{q}, remaining{3050000-q}.
Add the exact publication receipt charge before any next semantic phase.
All failed and superseded run charges remain included. Resources remain;
no resource-limit explanation for mathematical nonclosure is asserted.
'''
    with (F/'CHECKPOINT.md').open('x',encoding='utf8') as f:f.write(checkpoint)
    print(json.dumps({'status':'PUBLISHED_CHECKPOINT_NOT_ROOT_CLOSURE','provenance':provenance,'CPU_before_publication':tot,
      'groups':groups,'queries':q,'remaining_queries':3050000-q,'campaign_files_hashed':len(manifest['campaign_files'])}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof227_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
