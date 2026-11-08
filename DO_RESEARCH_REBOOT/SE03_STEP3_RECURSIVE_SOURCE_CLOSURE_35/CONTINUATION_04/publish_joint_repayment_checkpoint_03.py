"""Publish the new proof/status pins without advancing the source search."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(p,d):
    with p.open('x',encoding='utf8') as f:json.dump(d,f,indent=2)
def main():
    entry=B/'entry_authorized1920_audit720_q3050000.json';e=json.loads(entry.read_text())
    total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);q=e['inherited_conservative_queries'];runs=[]
    for p in sorted(B.glob('run_*_result.json')):
        r=json.loads(p.read_text());c=json.loads((B/('controller_'+r['phase']+'_exit.json')).read_text())
        v=r['child_CPU']+c['whole_process_CPU_seconds'];total+=v;groups[r['group']]+=v;q+=r.get('source_queries',0)
        runs.append({'phase':r['phase'],'group':r['group'],'CPU':v,'queries':r.get('source_queries',0),'status':r['status']})
    pending=json.loads((F/'global_probe11_H3_DAG_13.json').read_text());assert pending['status']=='CHECKPOINT'
    assert e['group_caps']=={'symbolic':1920,'independent':720}
    resources={'global_CPU_before_this_publication':total,'group_CPU_before_this_publication':groups,'global_cap':7200,
      'group_caps':e['group_caps'],'queries':q,'query_cap':3050000,'query_remaining':3050000-q,'usage_reset':False,
      'Bank25':25,'query_batch_cap':50000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
      'memory_GiB':32,'wall_hours':12,'global_reserve':5,'controller_reserve':1,
      'publication_charge_reference':'add run_proof262_result.json and controller_proof262_exit.json before next execution',
      'all_runs_including_failures':runs}
    out(F/'resources_checkpoint_03.json',resources)
    pins=[F/x for x in (
      'dependency_manifest_02.json','symbolic_authorization_1920.json',
      'SEVEN_KEY_MAXIMAL_CORE_FULL_PROOF.md','independent_paired_branch_certificate.json',
      'FIXED_DEPTH_SOURCE_INFORMATION_THEOREM.md','FD35_INDEPENDENT_PROOF_REVIEW.md',
      'CORE_SECTOR_LIABILITY_THEOREM.md','NEUTRAL_DOUBLE_SOURCE_DECOMPOSITION.md','independent_core_sector_neutral.json',
      'ZERO_NEUTRAL_FULL_SOURCE_FUNDING.md','ZERO_NEUTRAL_PROOF_REVIEW.md','independent_zero_neutral_funding.json',
      'joint_source_relation.json','PROJECTED_CLUSTER_ACCESS_THEOREM.md','projected_cluster_closed_counter_source.json',
      'independent_projected_cluster_theorem.json','TOP_INTERVAL_AND_MARKED_DEMOTION.md',
      'marked_demotion_relation.json','FRESH_PROXY_LOSS_THEOREM.md','independent_fresh_proxy_loss.json',
      'search_global_probe11_DAG_H3_v3.py','global_probe11_LOW_H3_model.pkl','global_probe11_H3_DAG_13.pkl',
      'independent_probe11_H3_DAG_checkpoint_13.json','independent_probe11_HIGH_envelope_H3_13.json',
      'independent_probe11_H3_actual_signs_13.json')]
    pins+=[entry,B/'run_phase_1920_audit720_q3050000.py',B/'STREAMED_BLOCK_THEOREM.md',B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',
      P/'SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md',P/'SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md',
      P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md']
    out(F/'dependency_manifest_03.json',{'branch':e['branch'],'head':e['head'],'input_sha256':{str(p.relative_to(P)):sha(p) for p in pins},
      'root_JR35':'OPEN','reservation':'DEFERRED','original_pins_or_owners_changed':False,'CD_counterexample':False})
    h3=json.loads((F/'independent_probe11_H3_actual_signs_13.json').read_text())
    t=f"""# C35 continuation 04 — checkpoint 03

JR35 **OPEN** at the required universal original r>=7 scope.
Reservation compatibility **DEFERRED** in the requested order.
No Coarse-Double counterexample and no universal funding proof.
This checkpoint supersedes the execution directions in CHECKPOINT_02,
not its accepted proof receipts or frozen source data.

Branch {e['branch']}; HEAD {e['head']}.
The existing tracked tree and frozen certificates were not changed.
See dependency_manifest_03.json for the new pinned source interfaces.
The seven-key maximal-core proof remains at its independently checked
scope; no claim about every other seven-key core or all larger supports.

## Uniform mathematical advances

- CSL35 maps local unpaid demands injectively to doubly missing
  fixed-core sectors, preserving h0. ND35 separately funds every
  nonneutral B double by actual A rotation bits paired on one period.
  The remaining neutral terminals are actual occurrence labels.
- JR35-N0 gives a full h0-preserving static block comparison with
  working bank <=2 for every source in its no-neutral class, arbitrary
  support and private populations. Group at minimum joint potential
  on original genuine boundaries, apply the proved signed macro law,
  then the inherited static block constructor. It does not assert a
  stronger online bank or extra fE locks. See its separate review.
- PC35 projects subtree labels onto any mark-retaining C and counts
  multiplicity. Its final B event has a decrease, and access-level
  slots permit an actual terminal zig/extra decrease to fund another
  double of that access. The AF projection gives an independently
  checked alternative full 36-demand comparison preserving 32 h0
  values, working bank 2. No earlier comparison is replaced.
- The exact closed eleven-key counterexample to PC35 has actual
  interval [35,57], A=27, QF=11, QE=12. Its designated H1/Q5
  macro has signed margin -3 and four neutral doubles. The
  double-specific donor graph has a four-claim/two-bit cut; the
  access-level rule has only one additional slot. A/B/BE/charts
  were independently replayed. It is not a CD or JR35 counterexample.
- TI35 pays some different source doubles via the shallowest A key
  of a B interval. Its branchy fully marked family defeats both
  TI35 and PC35 scalar summaries simultaneously, with a symbolic
  source-embedding proof and distinct packet-geometry control.
- MD35 proves monotone B shrinkage for an actual marked grandparent
  between its genuine KEEPs, and identifies every actual A loss
  candidate. AF/CCR refute loss-only completion, but both are
  fundable under the union with their own macro units. These exact
  controls do not prove universal expansion.
- FP35 works for all B cores: each B double has a distinct recent
  source proxy within its macro, derived by orienting a degree-two
  graph of actual first core entries. Every proxy yields an actual
  A ancestor-loss bit. The bits for repeated occurrences of any
  fixed target are disjoint. Different targets can still collide.
  The source audit checks the tags and gives AF's six-demand /
  one-loss-bit cut for the bare FP relation. Adding own bits
  resolves that control, and does not settle arbitrary sources.

The distinct audits are operated by this research agent; they are
not external peer review or formal proof-assistant verification.
All original source operations, h0 values, Bank25 and frozen fE
interfaces are unchanged.

## Exact remaining proof target

MIXED-TARGET LOSS ESCAPE: from original rotations and marked-core
geometry, find distinct eligible physical endpoints for the claims
that share a loss rotation across DIFFERENT targets. Use alternative
actual operand tags, actual eligible own units and source-licensed
nonlocal exchange. The relation is specified without assuming a
matching. A complete theorem must cover arbitrary connected
collections and supply the original static block/cut/Bank25 trace.
An exact cut would refute that particular relation, not universal
JR35 unless it excludes every permitted source allocation.

Start with the first saturated collision component: every competing
claim has its actual pivot and y tenure, source tag birth, own macro
and exact previously occupied bits. Prove a source-forced exit using
the distinct birth operands, marked demotion shrinkage where it applies,
or an independently licensed new supplier. Do not replace this by
the total capacity inequality. No reservation work before root JR35.

## Actual-source search resume

Resume the checkpointed actual native11 graph using
search_global_probe11_DAG_H3_v3.py, BATCH14, reading
global_probe11_H3_DAG_13.pkl. The accepted source model retains all
literal H1/H2 and the already added H3 subset. {pending['processed']}
column processes, {pending['pending_B_columns']} pending, maxD
{pending['max_D']}, DAG nodes {pending['DAG_nodes']}; no negative
original cycle found. The checked numerical representation and queue
are not signed closure.

Independent exact endpoint checking covers H>=4 for this candidate
with min margin 1 and c=4. The 14 failed H3 envelopes were separately
resolved by reverse source cost reachability, revealing
{len(h3['actual_H3_failure_controls'])} recorded actual violating controls
for the current candidate. They are individual original transitions,
not a negative source cycle. Future augmentation must incorporate
all required H3 constraints, not only these recorded controls.
Independently verify all LOW/H3 and the new HIGH envelope after any
quiescent candidate. Passing native11 would still be bounded.

## Cumulative caps

Before this metadata publication: global {total}/7200, symbolic
{groups['symbolic']}/1920, audit {groups['independent']}/720 CPU seconds;
queries {q}/3050000, remaining {3050000-q}. Add the exact proof262
and controller charge. No allowance was reset. All failures and
superseded executions are charged in resources_checkpoint_03.json.

The remaining symbolic allowance does not safely load, advance
and save another producer phase under the existing guard/reserve.
The requested 2160 cap is not in force unless the user authorizes it.
Do not start a renewed producer or move it to the audit account.
"""
    with (F/'CHECKPOINT_03.md').open('x',encoding='utf8') as f:f.write(t)
    print(json.dumps({'status':'NEW_JR35_DERIVATIONS_AND_SOURCE_RESUME_PINNED','global_before_publication':total,
      'groups_before_publication':groups,'queries':q,'pending_B_columns':pending['pending_B_columns'],
      'JR35':'OPEN','reservation':'DEFERRED'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof262_exit.json').open('x',encoding='utf8') as f:
            json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
