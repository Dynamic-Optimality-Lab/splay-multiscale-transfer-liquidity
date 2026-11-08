"""Metadata-only continuation entry; preserve C35's previous publication."""
import hashlib,json,subprocess,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;ROOT=P.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    old=read(C/'resources_checkpoint.json');base=read(B/'entry_authorized1440.json');total=base['prior_uniform_CPU'];groups=dict(base['inherited_group_CPU']);queries=base['inherited_conservative_queries'];phases=[]
    for rp in B.glob('run_*_result.json'):
        r=read(rp);cp=B/f"controller_{r['phase']}_exit.json";c=read(cp);a=r['child_CPU']+c['whole_process_CPU_seconds'];total+=a;groups[r['group']]+=a;queries+=r.get('source_queries',0);phases.append(r['phase'])
    assert (total,groups['symbolic'],groups['independent'],queries)==(old['global_CPU'],old['symbolic_CPU'],old['independent_CPU'],old['source_queries'])
    for n,h in read(C/'campaign_manifest.json')['artifacts'].items():assert sha(C/n)==h
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();assert head==old['HEAD']
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT).strip()
    out('entry.json',dict(branch='coarse-double-branch',HEAD=head,global_CPU=total,symbolic_CPU=groups['symbolic'],independent_CPU=groups['independent'],source_queries=queries,remaining_queries=3000000-queries,prior_phases=sorted(phases),caps=dict(global_CPU=7200,symbolic_CPU=1440,independent_CPU=600,queries=3000000,Bank25=25),controller_sha256=sha(B/'run_phase_1440.py'),old_publication_sha256=sha(C/'campaign_manifest.json'),usage_reset=False))
    print('CONTINUATION_ENTRY_PRESERVED_29_QUERIES',flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('entry_metadata_exit.json',dict(metadata_only=True,whole_process_CPU_seconds=time.process_time(),error=error))
