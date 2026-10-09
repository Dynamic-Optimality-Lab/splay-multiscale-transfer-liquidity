"""Read-only repository digest audit; all outputs confined to this workspace."""
import os, sys, json, hashlib, subprocess, datetime
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
sys.dont_write_bytecode = True
def git(*args):
    p = subprocess.run(['git', '--no-optional-locks', *args], cwd=ROOT, capture_output=True, text=True)
    if p.returncode: raise RuntimeError(p.stderr)
    return p.stdout
def manifest():
    files, directories = {}, []
    for base, dirs, names in os.walk(ROOT):
        if Path(base) == ROOT: dirs[:] = [d for d in dirs if d != HERE.name]
        directories.extend(str((Path(base)/d).relative_to(ROOT)).replace('\\','/') for d in dirs)
        for name in names:
            path = Path(base)/name
            rel = str(path.relative_to(ROOT)).replace('\\','/')
            if path.is_symlink():
                files[rel] = {'symlink': os.readlink(path)}
                continue
            h = hashlib.sha256()
            with path.open('rb') as f:
                for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
            st = path.stat()
            files[rel] = {'sha256':h.hexdigest(), 'size':st.st_size, 'mtime_ns':st.st_mtime_ns}
    return {'files':files, 'directories': sorted(directories)}
def state():
    return {'branch':git('branch','--show-current').strip(), 'head':git('rev-parse','HEAD').strip(),
            'status_porcelain':git('status','--porcelain=v1','--untracked-files=all'),
            'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
out = HERE/'11_REPRODUCIBILITY'
out.mkdir(exist_ok=True)
mode = sys.argv[1]
baseline = out/'baseline.json'
if mode == 'begin':
    if baseline.exists(): raise RuntimeError('Refusing to overwrite an existing baseline')
    data = {'git':state(), **manifest()}
    baseline.write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps({'files':len(data['files']), 'bytes':sum(v.get('size',0) for v in data['files'].values()), 'git':data['git']},indent=2))
elif mode == 'end':
    old = json.loads(baseline.read_text(encoding='utf-8'))
    new = manifest()
    added = sorted(new['files'].keys()-old['files'].keys())
    deleted = sorted(old['files'].keys()-new['files'].keys())
    changed = sorted(k for k in new['files'].keys() & old['files'].keys() if new['files'][k] != old['files'][k])
    final_git = state()
    filtered_status = '\n'.join(s for s in final_git['status_porcelain'].splitlines() if s[3:].strip('"').replace('\\','/').split('/')[0] != HERE.name)
    original_status = '\n'.join(s for s in old['git']['status_porcelain'].splitlines() if s[3:].strip('"').replace('\\','/').split('/')[0] != HERE.name)
    report = {'added_outside':added,'deleted_outside':deleted,'changed_outside':changed,
              'added_directories_outside':sorted(set(new['directories'])-set(old['directories'])),
              'deleted_directories_outside':sorted(set(old['directories'])-set(new['directories'])),
              'git':final_git,'outside_git_status_unchanged':filtered_status==original_status,
              'branch_head_unchanged':all(final_git[k]==old['git'][k] for k in ('branch','head')),
              'checked_files':len(new['files'])}
    report['pass'] = not any((added,deleted,changed,report['added_directories_outside'],report['deleted_directories_outside'])) and report['outside_git_status_unchanged'] and report['branch_head_unchanged']
    (out/'final_safety_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='git'},indent=2))
else: raise RuntimeError('Expected begin or end')
