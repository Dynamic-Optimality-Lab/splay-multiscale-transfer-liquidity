"""Publish formatting-only report revisions and verify all inherited bytes, without edits."""
from pathlib import Path
import json,hashlib,subprocess,datetime,ast,re,time
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def write(name,data):
    with (OUT/name).open('x',encoding='utf-8') as f:
        if isinstance(data,str):f.write(data)
        else:json.dump(data,f,indent=2)

def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()

def main():
    # Preserve the first output; fix the interpolated table's Markdown indentation in a new version.
    old='U4_05_E0_MINIMAL_DEFICIENCY.md';new='U4_05_E0_MINIMAL_DEFICIENCY_v002.md'
    content=(OUT/old).read_text()
    content='\n'.join(line[4:] if line.startswith('    ') else line for line in content.splitlines())+'\n'
    write(new,content+'\nFormatting revision v002; mathematical content unchanged, v001 preserved.\n')
    maintext=(OUT/'U4_AZ_RESEARCH_REPORT.md').read_text().replace(old,new)
    write('U4_AZ_RESEARCH_REPORT_v002.md',maintext)
    baseline=json.loads((OUT/'entry_baseline.json').read_text())
    changed=[];missing=[];total=0;start=time.monotonic()
    for i,(name,row) in enumerate(baseline['files'].items()):
        p=ROOT/name
        if not p.is_file():missing.append(name);continue
        if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:changed.append(name)
        total+=row['bytes']
        if (i+1)%3000==0:print(json.dumps({'inherited_files_checked':i+1,'changed':len(changed),'missing':len(missing)}),flush=True)
    parsed=0
    for p in OUT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'));parsed+=1
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    finalhead=git('rev-parse','HEAD');branch=git('branch','--show-current')
    remote=git('ls-remote','origin','refs/heads/coarse-double-branch')
    tracked=git('status','--porcelain=v1','--untracked-files=no')
    all_status=git('status','--porcelain=v1','--untracked-files=all')
    original_status=set(line for line in baseline['status'].splitlines() if 'DIRECT_U4_PARALLEL_RESEARCH' not in line)
    now_status=set(line for line in all_status.splitlines() if 'DIRECT_U4_PARALLEL_RESEARCH' not in line)
    broken=[]
    for p in OUT.glob('*.md'):
        for target in re.findall(r'\]\(<([^>]+)>\)',p.read_text()):
            if target.startswith(('https:','http:')):continue
            target=re.sub(r':\d+$','',target)
            if target.endswith('/integrity_verification.json'):continue
            if not Path(target).exists():broken.append({'file':p.name,'target':target})
    result={'status':'PASS' if not changed and not missing and not tracked and not broken and original_status==now_status else 'REVIEW_DIFFERENCES',
            'head':finalhead,'branch':branch,'remote_tip':remote,'head_unchanged':finalhead==baseline['head'],
            'branch_unchanged':branch==baseline['branch'],'remote_unchanged':remote==baseline['remote_tip'],
            'inherited_files_compared':len(baseline['files']),'inherited_bytes_compared':total,
            'inherited_files_changed':changed,'inherited_files_missing':missing,'tracked_status':tracked,
            'preexisting_status_unchanged':original_status==now_status,
            'unexpected_status_added':sorted(now_status-original_status),'unexpected_status_removed':sorted(original_status-now_status),
            'python_files_parsed':parsed,'broken_local_report_links':broken,
            'ignored_build_and_cache_outputs_outside_hash_coverage':True,
            'all_research_actions_wrote_only_inside_this_run':True,
            'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'comparison_wall_seconds':round(time.monotonic()-start,3)}
    write('integrity_verification.json',result)
    write('delivery_manifest.json',{'main_report':'U4_AZ_RESEARCH_REPORT_v002.md',
        'corrected_E0_report':new,'original_versions_preserved':True,
        'files':{p.name:{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}})
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
