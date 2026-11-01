"""Read-only inventory of pre-existing repository bytes; writes only beside this file."""
from pathlib import Path
import hashlib, json, subprocess, datetime

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    target = OUT / 'entry_baseline.json'
    if target.exists():
        raise RuntimeError('append-only baseline already exists')
    paths = git('ls-files', '--cached', '--others', '--exclude-standard', '-z').decode('utf-8').split('\0')
    files = {}
    for name in sorted(set(filter(None, paths))):
        path = ROOT / name
        if path.is_relative_to(OUT) or not path.is_file():
            continue
        files[name] = {'bytes': path.stat().st_size, 'sha256': digest(path)}
    data = {
        'client_date': '2026-10-30', 'timezone': 'Asia/Karachi',
        'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'root': str(ROOT), 'branch': git('branch','--show-current').decode().strip(),
        'head': git('rev-parse','HEAD').decode().strip(),
        'status': git('status','--porcelain=v1','--untracked-files=all').decode(),
        'worktrees': git('worktree','list','--porcelain').decode(),
        'remote': git('remote','-v').decode(),
        'remote_tip': git('ls-remote','origin','refs/heads/coarse-double-branch').decode().strip(),
        'files': files,
        'coverage': 'All tracked and nonignored untracked regular files outside this new run. Ignored caches/build outputs excluded; Python runs use -B.'
    }
    target.write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps({'files_hashed':len(files),'bytes_hashed':sum(x['bytes'] for x in files.values()),'head':data['head'],'output':str(target)}))

if __name__ == '__main__':
    main()
