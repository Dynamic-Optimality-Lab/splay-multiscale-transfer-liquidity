"""Read-only recheck of pinned old research and all prior seals."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('\\\\?\\'+str(HERE.parent.parent))


def digest(file):
    h = hashlib.sha256()
    with file.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    counts, failures = {}, []
    groups = []
    audit = ROOT/'DO_RESEARCH_REBOOT/DO_ROUTE_AUDIT_20261120'
    groups.append(('original_corpus_hashes',ROOT,[x for x in map(json.loads,(audit/'corpus_inventory.jsonl').read_text(encoding='utf-8').splitlines()) if x.get('sha256')]))
    groups.append(('prior_route_audit_files',audit,json.loads((audit/'AUDIT_MANIFEST.json').read_text())['files']))
    old = ROOT/'DO_RESEARCH_REBOOT/H3Q_ANALYSIS_20261120_V001'
    groups.append(('prior_H3q_sealed_files',old,json.loads((old/'FINAL_MANIFEST.json').read_text())['files']))
    groups.append(('current_pinned_inputs',ROOT,json.loads((HERE/'PINNED_INPUTS.json').read_text())))
    for name, base, items in groups:
        for item in items:
            file = base/item['path']
            if not file.exists() or digest(file) != item['sha256']:
                failures.append({'group':name,'path':item['path']})
        counts[name] = len(items)
    status = subprocess.run(['git','status','--porcelain=v1','-uno'],cwd=str(HERE.parent.parent),capture_output=True,text=True,check=True).stdout
    head = subprocess.run(['git','rev-parse','HEAD'],cwd=str(HERE.parent.parent),capture_output=True,text=True,check=True).stdout.strip()
    assert not failures and not status and head == '6d532b2c795c0778f57d8023b23b5fedfc48b010'
    out = {'passed':True,'checked_utc':datetime.now(timezone.utc).isoformat(),'counts':counts,
           'failures':failures,'tracked_diff_empty':not bool(status),'HEAD':head,
           'scope':'SHA-256 integrity of original pinned corpus and two prior sealed outputs; no re-certification of every old mathematical assertion.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
