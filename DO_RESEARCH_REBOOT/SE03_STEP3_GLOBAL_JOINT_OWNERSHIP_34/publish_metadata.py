"""Metadata-only cumulative publication; no new semantic/source computation."""
import hashlib,json,subprocess,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;ROOT=P.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8',errors='replace').strip()
def main():
    e=read(B/'entry_authorized1440.json');old=read(F/'entry.json');oldph={r['phase'] for r in old['historical_charges']};total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);queries=e['inherited_conservative_queries'];new=[]
    for rp in sorted(B.glob('run_*_result.json')):
        r=read(rp);cp=B/f"controller_{r['phase']}_exit.json";c=read(cp);charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge;queries+=r.get('source_queries',0)
        if r['phase'] not in oldph:new.append(dict(phase=r['phase'],group=r['group'],status=r['status'],child_CPU=r['child_CPU'],controller_CPU=c['whole_process_CPU_seconds'],total_charge=charge,source_queries=r.get('source_queries',0),run_sha256=sha(rp),controller_exit_sha256=sha(cp)))
    assert queries==2999939 and total<7200 and groups['symbolic']<1440 and groups['independent']<600
    assert not git('status','--porcelain','--untracked-files=no')
    branch,head=git('branch','--show-current'),git('rev-parse','HEAD');assert branch==old['branch'] and head==old['HEAD']
    for d in read(F/'dependency_manifest.json')['dependencies']:assert sha(Path(d['path']))==d['sha256']
    result=dict(status='C34_STRUCTURAL_PARTIAL_JIO34_OPEN',branch=branch,HEAD=head,tracked_clean=True,global_CPU=total,global_cap=7200,symbolic_CPU=groups['symbolic'],symbolic_cap=1440,independent_CPU=groups['independent'],independent_cap=600,source_queries=queries,source_query_cap=3000000,remaining_queries=3000000-queries,source_query_batch_cap=50000,Bank25=25,remaining_global_CPU=7200-total,remaining_symbolic_CPU_including_reserve=1440-groups['symbolic'],remaining_independent_CPU_including_reserve=600-groups['independent'],global_reserve=5,controller_reserve=1,live_state_limit=2000000,DAG_limit=4000000,stored_edge_limit=5000000,memory_limit_bytes=32*1024**3,wall_limit_hours=12,controller=str(B/'run_phase_1440.py'),controller_sha256=sha(B/'run_phase_1440.py'),active_authorization=str(B/'resource_amendment_1440.json'),phase_caps_unchanged=e['phase_caps'],default_new_phase_cap=20,new_charges=new,all_historical_charges_including_failures_retained=True,usage_reset=False,cap_increase=False,new_cap_request_pending=False,resource_exhaustion_claimed=False,optional_185_query_replay_exceeds_remaining_61=True,metadata_publication_CPU='excluded under inherited metadata convention; publication_metadata_exit.json separately records it',JIO34='OPEN',terminal_outcome='A-L_STRUCTURAL_PARTIAL',unconditional_Gate_U='OPEN')
    out('resources_checkpoint.json',result)
    text=f'''# Cumulative resource ledger — unchanged allowances

| Resource | Cumulative use | Cap | Remaining including reserve |
|---|---:|---:|---:|
| Global CPU seconds | {total} | 7200 | {7200-total} |
| Symbolic CPU seconds | {groups['symbolic']} | 1440 | {1440-groups['symbolic']} |
| Independent CPU seconds | {groups['independent']} | 600 | {600-groups['independent']} |
| Source queries | {queries} | 3000000 | {3000000-queries} |

Authoritative machine ledger: resources_checkpoint.json. Every new child
and controller charge is listed there, including core41/core42/verify82
failures. The original accepted controller and all historical charges
are unchanged. The C34 entry was global{old['global_CPU']},
symbolic{old['symbolic_CPU']}, independent{old['independent_CPU']},
queries{old['source_queries']}. New queries total{queries-old['source_queries']}.

Bank25 remains25; query batch cap50000; global/controller reserves5/1;
live states2m, DAG4m, stored edges5m, memory32GiB, wall12h. New phases use
the unchanged controller default20-second child cap. No cumulative cap
was extended or reset. No parallel controller ran. Metadata-only entry
and publication follow the inherited exclusion and record their own CPU.

CPU is not exhausted. The optional185-query diagnostic cannot be rerun
within the remaining61 queries. It is unaccepted, and more passing finite
examples would not prove the missing universal source law. The final
mathematical status remains structural partial/JIO34 OPEN. No new cap
authorization is pending or requested.
'''
    with (F/'RESOURCE_LEDGER.md').open('x',encoding='utf-8') as f:f.write(text)
    additional=[]
    for c in read(F/'pooled_source_results.json')['cases']:
        for k in ('path','receipt'):
            p=Path(c[k]);additional.append(dict(path=str(p),sha256=sha(p),status='ACCEPTED_SOURCE_OR_PRIMITIVE_RECEIPT_REUSED_BY_HASH'))
    p=P/'SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md';additional.append(dict(path=str(p),sha256=sha(p),status='INSPECTED_MAXIMAL_SOURCE_PROOF'))
    manifest=dict(branch=branch,HEAD=head,tracked_clean=True,entry_manifest_sha256=sha(F/'dependency_manifest.json'),additional_dependencies=additional,artifacts={p.name:sha(p) for p in sorted(F.iterdir()) if p.is_file() and p.name not in ('campaign_manifest.json','publication_metadata_exit.json')},new_controller_receipts=new,proof_status='A-L_STRUCTURAL_PARTIAL; principal_JIO34_OPEN',full_proof_absent=not(F/'FULL_PROOF.md').exists())
    out('campaign_manifest.json',manifest)
    print(json.dumps({k:result[k] for k in ('status','global_CPU','symbolic_CPU','independent_CPU','source_queries','remaining_queries')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('publication_metadata_exit.json',dict(metadata_only=True,whole_process_CPU_seconds=time.process_time(),error=error))
