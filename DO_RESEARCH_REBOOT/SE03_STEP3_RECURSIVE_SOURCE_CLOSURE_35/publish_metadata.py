"""Metadata-only final cumulative publication; no source or proof engine."""
import hashlib,json,subprocess,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;ROOT=P.parent;C=P/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT).decode('utf-8',errors='replace').strip()
def main():
    old=read(F/'entry.json');e=read(B/'entry_authorized1440.json');oldph={r['phase'] for r in old['charges']};total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);queries=e['inherited_conservative_queries'];new=[]
    for rp in sorted(B.glob('run_*_result.json')):
        r=read(rp);cp=B/f"controller_{r['phase']}_exit.json";c=read(cp);charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge;queries+=r.get('source_queries',0)
        if r['phase'] not in oldph:new.append(dict(phase=r['phase'],group=r['group'],status=r['status'],child_CPU=r['child_CPU'],controller_CPU=c['whole_process_CPU_seconds'],total_charge=charge,source_queries=r.get('source_queries',0),run_sha256=sha(rp),controller_exit_sha256=sha(cp)))
    assert queries==2999971 and 3000000-queries==29
    assert total<7200 and groups['symbolic']<1440 and groups['independent']<600 and all(r['status']=='PASS' for r in new)
    branch,head=git('branch','--show-current'),git('rev-parse','HEAD');assert branch==old['branch'] and head==old['HEAD'] and not git('status','--porcelain','--untracked-files=no')
    dep=read(F/'dependency_manifest.json')
    for d in dep['inherited']:assert sha(Path(d['path']))==d['sha256']
    for n,h in dep['C34_artifacts'].items():assert sha(C/n)==h
    assert sha(B/'run_phase_1440.py')==old['controller_sha256']
    result=dict(status='C35_MATHEMATICAL_BLOCKER_NO_A_OR_E',branch=branch,HEAD=head,tracked_clean=True,global_CPU=total,global_cap=7200,symbolic_CPU=groups['symbolic'],symbolic_cap=1440,independent_CPU=groups['independent'],independent_cap=600,source_queries=queries,source_query_cap=3000000,remaining_queries=3000000-queries,new_source_queries=queries-old['source_queries'],source_query_batch_cap=50000,Bank25=25,remaining_global_CPU=7200-total,remaining_symbolic_CPU_including_reserve=1440-groups['symbolic'],remaining_independent_CPU_including_reserve=600-groups['independent'],global_reserve=5,controller_reserve=1,live_state_limit=2000000,DAG_limit=4000000,stored_edge_limit=5000000,memory_limit_bytes=32*1024**3,wall_limit_hours=12,controller=str(B/'run_phase_1440.py'),controller_sha256=sha(B/'run_phase_1440.py'),active_authorization=str(B/'resource_amendment_1440.json'),phase_caps_unchanged=e['phase_caps'],default_new_phase_cap=20,new_charges=new,usage_reset=False,old_failed_charges_retained=True,cap_increase=False,cap_request_pending=False,resource_exhaustion_claimed=False,mathematical_blocker='COMP35 joint source compensation not proved; no further justified descending source reduction established',ROOT35='UNRESOLVED',U35='UNRESOLVED',terminal_A_L=False,source_countercut_proved=False,source_root_proved=False,metadata_CPU='excluded under inherited metadata-only convention; publication_metadata_exit.json records it')
    out('resources_checkpoint.json',result)
    with (F/'RESOURCE_LEDGER.md').open('x',encoding='utf-8') as f:
        f.write(f'''# Unchanged cumulative research allowance

| Resource | Used | Cap | Remaining including reserve |
|---|---:|---:|---:|
| Global CPU | {total} | 7200 | {7200-total} |
| Symbolic CPU | {groups['symbolic']} | 1440 | {1440-groups['symbolic']} |
| Independent CPU | {groups['independent']} | 600 | {600-groups['independent']} |
| Source queries | {queries} | 3000000 | {3000000-queries} |

New C35 queries32:16 actual A splays in core43,16 in verify84. BF/BE
primitive states were reused from the accepted source, with exact identity
checks; no new B replay was disguised. All other C35 phases use zero
fresh primitive queries. No optional C34 failed construction was retried.
All new phases pass; historical failures stay cumulatively charged.

Bank25,50k batch,2m live states,4m DAG,5m edges,32GiB memory,12h wall and
5/1 global/controller reserves are unchanged. Every semantic/audit phase
uses the original accepted controller (default20-second new phase cap).
Metadata-only entry/publication follow the inherited exclusion and record
their CPU separately. No budget is reset or increased; no parallel
controller or implicit allowance is used.

The terminal blocker is mathematical, not resource exhaustion. More
passing finite controls would not close the remaining source implication.
No cap renewal is requested. The exact charges are in resources_checkpoint.json.
''')
    dependencies=[]
    for p in (B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',B/'uniform_A_realization_independent_audit.json',B/'uniform_A_realization_proof_object.json',B/'primary_1907_06310v3.pdf'):
        if p.is_file():dependencies.append(dict(path=str(p),sha256=sha(p),role='inherited source-reachability dependency, no numerical cost imported'))
    manifest=dict(branch=branch,HEAD=head,tracked_clean=True,directive_sha256=sha(F/'USER_DIRECTIVE.txt'),entry_dependencies_sha256=sha(F/'dependency_manifest.json'),additional_dependencies=dependencies,artifacts={p.name:sha(p) for p in sorted(F.iterdir()) if p.is_file() and p.name not in ('campaign_manifest.json','publication_metadata_exit.json')},new_controller_receipts=new,source_root_proved=False,source_countercut_proved=False,terminal_status='GENUINE_MATHEMATICAL_BLOCKER',full_proof_absent=not(F/'FULL_PROOF.md').exists())
    out('campaign_manifest.json',manifest)
    print(json.dumps({k:result[k] for k in ('status','global_CPU','symbolic_CPU','independent_CPU','source_queries','remaining_queries')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('publication_metadata_exit.json',dict(metadata_only=True,whole_process_CPU_seconds=time.process_time(),error=error))
