"""Metadata-only publication; does not change historical C35 records."""
import hashlib,json,subprocess,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;ROOT=P.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT).decode('utf-8',errors='replace').strip()
def main():
    entry=read(F/'entry.json');base=read(B/'entry_authorized1440.json');old=set(entry['prior_phases']);total=base['prior_uniform_CPU'];groups=dict(base['inherited_group_CPU']);queries=base['inherited_conservative_queries'];new=[]
    for rp in sorted(B.glob('run_*_result.json')):
        r=read(rp);cp=B/f"controller_{r['phase']}_exit.json";c=read(cp);a=r['child_CPU']+c['whole_process_CPU_seconds'];total+=a;groups[r['group']]+=a;queries+=r.get('source_queries',0)
        if r['phase'] not in old:new.append(dict(phase=r['phase'],group=r['group'],status=r['status'],child_CPU=r['child_CPU'],controller_CPU=c['whole_process_CPU_seconds'],total_charge=a,source_queries=r.get('source_queries',0),run_sha256=sha(rp),controller_exit_sha256=sha(cp)))
    assert queries==2999999 and queries-entry['source_queries']==28
    assert total<7200 and groups['symbolic']<1440 and groups['independent']<600 and all(n['status']=='PASS' for n in new)
    assert sha(B/'run_phase_1440.py')==entry['controller_sha256']
    assert git('rev-parse','HEAD')==entry['HEAD'] and not git('status','--porcelain','--untracked-files=no')
    for n,h in read(C/'campaign_manifest.json')['artifacts'].items():assert sha(C/n)==h
    for audit in ('independent_critical_source_audit.json','independent_symbolic_source_audit.json','independent_resolution_certificate_audit.json'):
        for n,h in read(F/audit)['input_sha256'].items():assert sha(F/n)==h
    resource=dict(status='C35_E_SI34_SOURCE_LAW_REFUTED',branch=entry['branch'],HEAD=entry['HEAD'],tracked_clean=True,global_CPU=total,global_cap=7200,symbolic_CPU=groups['symbolic'],symbolic_cap=1440,independent_CPU=groups['independent'],independent_cap=600,source_queries=queries,source_query_cap=3000000,remaining_queries=1,new_source_queries=28,source_query_batch_cap=50000,Bank25=25,remaining_global_CPU=7200-total,remaining_symbolic_CPU_including_reserve=1440-groups['symbolic'],remaining_independent_CPU_including_reserve=600-groups['independent'],global_reserve=5,controller_reserve=1,live_state_limit=2000000,DAG_limit=4000000,stored_edge_limit=5000000,memory_limit_bytes=32*1024**3,wall_limit_hours=12,controller=str(B/'run_phase_1440.py'),controller_sha256=sha(B/'run_phase_1440.py'),active_authorization=str(B/'resource_amendment_1440.json'),phase_caps_unchanged=base['phase_caps'],default_new_phase_cap=20,new_charges=new,usage_reset=False,old_failed_charges_retained=True,cap_increase=False,cap_request_pending=False,ROOT35='REFUTED',SI34='REFUTED',terminal_outcome='E-SI34',higher_original_Gate_U='OPEN',architecture_refuted=False,Coarse_Double_counterexample=False,full_numerical_source_replayed=False,metadata_CPU='excluded under inherited metadata-only convention; publication_metadata_exit.json separately records it')
    out('resources_checkpoint.json',resource)
    with (F/'RESOURCE_LEDGER.md').open('x',encoding='utf-8') as f:f.write(f'''# Unchanged cumulative allowance after SI34 refutation

| Resource | Used | Cap | Remaining including reserve |
|---|---:|---:|---:|
| Global CPU | {total} | 7200 | {7200-total} |
| Symbolic CPU | {groups['symbolic']} | 1440 | {1440-groups['symbolic']} |
| Independent CPU | {groups['independent']} | 600 | {600-groups['independent']} |
| Source queries | {queries} | 3000000 | 1 |

The continuation used28 fresh source queries:11 A+3 B in core44 and
the same14 accesses in the independent mutable implementation verify87.
Symbolic source construction/closure audits do not claim numerical
Gamma or whole-period replay. No unaccepted old source was retried.
All continuation phases pass; all historical failures remain charged.

Bank25,50k batches,2m live states,4m DAG,5m edges,32GiB memory,12h wall,
global/controller5/1 reserves and all phase caps remain unchanged.
Every semantic/audit run used the accepted controller. No allowance was
reset or increased. Metadata entry/publication follows the inherited
exclusion and records its CPU separately.

The root is resolved by a mathematical source counterexample, not by a
resource-limit stopping condition. Universal original funding, owner
and Bank25 conclusions remain OPEN; no new cap request is pending.
''')
    latest=dict(status='E-SI34',ROOT35='REFUTED',checkpoint=str(F/'CHECKPOINT.md'),proof=str(F/'SI34_SOURCE_REFUTATION.md'),certificate=str(F/'SI34_source_countercertificate.json'),certificate_sha256=sha(F/'SI34_source_countercertificate.json'),resources=str(F/'resources_checkpoint.json'),resources_sha256=sha(F/'resources_checkpoint.json'),prior_publication_preserved=True,higher_Gate_U='OPEN')
    with (C/'LATEST_RESOLUTION.json').open('x',encoding='utf-8') as f:json.dump(latest,f,indent=2)
    with (C/'LATEST_CHECKPOINT.md').open('x',encoding='utf-8') as f:f.write('''# Latest C35 resolution — SI34 REFUTED

The earlier BLOCKED publication is preserved as history. The source law
is now resolved negatively by CONTINUATION_01/SI34_SOURCE_REFUTATION.md.
The exact source countercertificate, independent audits and current
resources are in CONTINUATION_01/. See its CHECKPOINT.md.

Three interior H1/Q3 macros have9 demands and8 exact C34 pool bits.
The original source is reachable and paired-closed by the symbolic
construction, and is itself CD-safe. Gamma blocks are not numerically
expanded; this verification limit is explicit. The entire original
funding/owner/Bank25 mechanism and unconditional Gate U remain OPEN.
''')
    manifest=dict(branch=entry['branch'],HEAD=entry['HEAD'],outcome='E-SI34',artifacts={p.name:sha(p) for p in sorted(F.iterdir()) if p.is_file() and p.name not in ('campaign_manifest.json','publication_metadata_exit.json')},parent_latest_pointers={n:sha(C/n) for n in ('LATEST_RESOLUTION.json','LATEST_CHECKPOINT.md')},new_controller_receipts=new,prior_C35_publication_unchanged=True,full_numerical_source_replay=False,mathematical_source_counterexample=True)
    out('campaign_manifest.json',manifest)
    print(json.dumps({k:resource[k] for k in ('status','global_CPU','symbolic_CPU','independent_CPU','source_queries','remaining_queries')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('publication_metadata_exit.json',dict(metadata_only=True,whole_process_CPU_seconds=time.process_time(),error=error))
