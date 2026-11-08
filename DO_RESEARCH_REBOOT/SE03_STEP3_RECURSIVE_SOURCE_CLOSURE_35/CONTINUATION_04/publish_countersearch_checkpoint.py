"""Cumulative resource/status metadata only; no producer continuation."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    e=json.loads((B/'entry_authorized1680_audit720_q3050000.json').read_text());total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);queries=e['inherited_conservative_queries'];runs=[]
    for p in B.glob('run_*_result.json'):
        r=json.loads(p.read_text());c=json.loads((B/('controller_'+r['phase']+'_exit.json')).read_text());v=r['child_CPU']+c['whole_process_CPU_seconds'];total+=v;groups[r['group']]+=v;queries+=r.get('source_queries',0)
        runs.append({'phase':r['phase'],'group':r['group'],'CPU':v,'queries':r.get('source_queries',0),'status':r['status']})
    pending=json.loads((F/'global_probe11_DAG_06.json').read_text());assert pending['status']=='CHECKPOINT'
    resources={'global_CPU_before_this_publication':total,'group_CPU_before_this_publication':groups,'global_cap':7200,'group_caps':e['group_caps'],
      'queries':queries,'query_cap':3050000,'query_remaining':3050000-queries,'usage_reset':False,'Bank25':25,'query_batch_cap':50000,
      'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_GiB':32,'wall_hours':12,'global_reserve':5,'controller_reserve':1,
      'publication_charge_reference':'add run_proof240_result.json and controller_proof240_exit.json before next execution','all_runs_including_failures':runs}
    with (F/'resources_checkpoint_02.json').open('x',encoding='utf8') as f:json.dump(resources,f,indent=2)
    checked=json.loads((F/'independent_probe11_DAG_checkpoint_05.json').read_text())
    manifest={'parent_manifest_sha256':sha(F/'dependency_manifest.json'),'branch':e['branch'],'head':e['head'],
      'countersearch_inputs':{p:sha(F/p) for p in ('probe11_source_actions.pkl','independent_probe11_source_actions.json','global_probe11_LOW_model.pkl',
        'independent_global_probe11_LOW_model.json','global_probe11_DAG_entry.pkl','independent_probe11_DAG_conversion.json','global_probe11_DAG_06.pkl',
        'independent_probe11_DAG_checkpoint_05.json','DECISION_DAG_REPRESENTATION.md','EXACT_LOW_IMAGE_MEMOIZATION.md','ACTUAL_CLOSED_SOURCE_FALSIFICATION_BOX.md')},
      'root_JR35':'OPEN','reservation':'DEFERRED','new_root_counterexample':False}
    with (F/'dependency_manifest_02.json').open('x',encoding='utf8') as f:json.dump(manifest,f,indent=2)
    text=f'''# C35 / continuation04 — actual-source search checkpoint02

JR35 is **OPEN** at the original all-r>=7 scope. Reservation compatibility
is **DEFERRED**. This is neither universal funding nor a Coarse-Double
counterexample. The completed maximal-seven/core13 source theorem and all
earlier frozen proofs remain as recorded in CHECKPOINT.md.

## New actual-source falsification route

The complete eleven-key ordinary action table has58786 actual trees and
646646 actions. Reused645622 non-Hamiltonian actions via proved off-path
leaf substitution. All1024 genuinely new Hamiltonian actions were checked
with the functional producer AND distinct mutable auditor;2048 queries
charged. The complete source table is independently accepted. This is a
primitive source result, not a funding proof.

Six deterministic full-B recurrent KEEP-word models with arbitrary A-only
helpers yielded no negative actual source cycle. Two longer phase models
were explicitly skipped at that stage's live-state cap. No passing-word
result is called universal.

The current broader search ranges over ALL full B trees and every literal
H1/H2 natural A macro. Its independent source-node-first regeneration
accepts184756 H1 and587860 H2 rows,772616 total. Every row carries literal
full A states and zero/one helper DELETE; there are no abstract HIGH edges.
Any reported negative cycle would retain literal A/B closure and would
still require complete independent original-source witness replay.

## Smaller complete representation, correction, and audit

The old scalar memoization omitted re-enqueuing cached changed targets.
It remained an INCOMPLETE checkpoint, never an accepted certificate. Its
valid lower bounds were preserved and ALL58786 B columns were rescheduled.
All old scripts, receipts and charges remain. The corrected engines always
schedule changed targets, including cached numerical merges.

The immutable coefficient functions now share exact subfunctions in an
ordered interval decision DAG. The initial1,420,697 coefficient records
became28511 nodes. An independent decoder checked8,106,596 profile-domain
values and every zero padding coefficient. This is lossless function
sharing, not an identification of distinct A/B source states.

The separate checkpoint05 audit confirms full representation validity,
padding and monotonicity from that audited entry, across58786 literal B
states and18463 distinct root functions. It does NOT claim signed closure.
The latest checkpoint06 is newer and remains producer-only/incomplete;
no audit receipt for05 is extended silently to06.

## Exact resume

Use `search_global_probe11_DAG_v2.py`, BATCH7, reading
`global_probe11_DAG_06.pkl`. Latest processed B columns cumulatively:
{pending['processed']}; pending:{pending['pending_B_columns']}; maxD:{pending['max_D']};
live DAG nodes:{pending['DAG_nodes']}. No genuine negative cycle has appeared.
Queues are not empty; no positive native11 certificate is claimed. Parent
tracing starts above8 only as an optimization;8 is NOT a proposed bound.

If the producer reaches quiescence, independently check ALL literal LOW
inequalities and the HIGH endpoint envelope (or actual H3 obligations if
needed). Passing at eleven physical anchors is not unrestricted JR35.
Do not begin reservation compatibility or promote C35/Gate U.

The main uniform mathematical obligation is still RT35-JOINT: prove a
joint source interval/owner charging rule with distinct usable original
bits, h0, one actual period and Bank25. FD35 proves no fixed A-prefix depth
plus full B can suffice for the universal small-packet potential route.

## Resources — no reset or cap increase

Before this metadata publication: global{total}/7200, symbolic
{groups['symbolic']}/1680, independent{groups['independent']}/720 CPU seconds;
queries{queries}/3050000, remaining{3050000-queries}. Add the exact proof240
publication/controller charge. Controller reserves and every other cap
remain fixed. A renewed symbolic allowance has NOT been authorized.
Do not load/advance the next producer batch if the safe load/save reserve
does not fit. Independent checking and written mathematical derivation
remain separate activities, not disguised producer continuation.
'''
    with (F/'CHECKPOINT_02.md').open('x',encoding='utf8') as f:f.write(text)
    print(json.dumps({'status':'ACTUAL_SOURCE_CHECKPOINT_PRESERVED','global_before_publication':total,'groups':groups,'queries':queries,
      'pending_B_columns':pending['pending_B_columns'],'DAG_nodes':pending['DAG_nodes'],'JR35':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof240_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
