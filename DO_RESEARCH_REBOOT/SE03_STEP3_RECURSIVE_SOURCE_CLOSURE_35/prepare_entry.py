"""Metadata-only C35 entry: pins, branch, cumulative ledger; no source work."""
import hashlib,json,subprocess,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;ROOT=P.parent;C=P/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT).decode('utf-8',errors='replace').strip()
def main():
    old=read(C/'resources_checkpoint.json');entry=read(B/'entry_authorized1440.json');total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=entry['inherited_conservative_queries'];charges=[]
    for rp in sorted(B.glob('run_*_result.json')):
        r=read(rp);cp=B/f"controller_{r['phase']}_exit.json";c=read(cp);a=r['child_CPU']+c['whole_process_CPU_seconds'];total+=a;groups[r['group']]+=a;queries+=r.get('source_queries',0)
        charges.append(dict(phase=r['phase'],group=r['group'],status=r['status'],charge=a,queries=r.get('source_queries',0),run_sha256=sha(rp),controller_sha256=sha(cp)))
    assert (total,groups['symbolic'],groups['independent'],queries)==(old['global_CPU'],old['symbolic_CPU'],old['independent_CPU'],old['source_queries'])
    assert entry['group_caps']==dict(symbolic=1440,independent=600)
    manifest=read(C/'campaign_manifest.json')
    for n,h in manifest['artifacts'].items():assert sha(C/n)==h
    inherited=read(C/'dependency_manifest.json')['dependencies']
    for d in inherited:assert sha(Path(d['path']))==d['sha256']
    directive=Path(r'C:\Users\Saif malik\.codex\attachments\44b76693-28eb-4489-ab9e-cd8107b0edf8\Pasted text.txt')
    with (F/'USER_DIRECTIVE.txt').open('xb') as f:f.write(directive.read_bytes())
    branch,head=git('branch','--show-current'),git('rev-parse','HEAD');assert branch==old['branch'] and head==old['HEAD'] and not git('status','--porcelain','--untracked-files=no')
    out('entry.json',dict(branch=branch,HEAD=head,tracked_clean=True,global_CPU=total,symbolic_CPU=groups['symbolic'],independent_CPU=groups['independent'],source_queries=queries,remaining_queries=3000000-queries,caps=dict(global_CPU=7200,symbolic_CPU=1440,independent_CPU=600,queries=3000000,batch=50000,Bank25=25),controller=str(B/'run_phase_1440.py'),controller_sha256=sha(B/'run_phase_1440.py'),active_authorization=str(B/'resource_amendment_1440.json'),charges=charges,all_failed_charges_retained=True,usage_reset=False))
    out('dependency_manifest.json',dict(inherited=inherited,C34_artifacts=manifest['artifacts'],C34_manifest_sha256=sha(C/'campaign_manifest.json'),directive_sha256=sha(directive),root_scope_clarification='C35 root is ALL C34 macro subsets; C34 handoff one-interior SI34 is child ONE, not full root'))
    print(json.dumps(dict(status='C35_ENTRY_PINNED',global_CPU=total,symbolic_CPU=groups['symbolic'],independent_CPU=groups['independent'],queries=queries,remaining_queries=3000000-queries)),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('entry_metadata_exit.json',dict(metadata_only=True,whole_process_CPU_seconds=time.process_time(),error=error))
