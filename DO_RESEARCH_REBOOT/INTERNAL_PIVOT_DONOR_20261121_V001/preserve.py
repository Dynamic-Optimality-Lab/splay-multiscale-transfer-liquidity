"""Verify all prior pinned originals and all five previous sealed outputs."""
import hashlib
import json
import subprocess
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=Path('\\\\?\\'+str(HERE.parent.parent))


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def main():
    rb=ROOT/'DO_RESEARCH_REBOOT';audit=rb/'DO_ROUTE_AUDIT_20261120'
    original=[x for x in map(json.loads,(audit/'corpus_inventory.jsonl').read_text(encoding='utf-8').splitlines()) if x.get('sha256')]
    groups=[('original_corpus',ROOT,original),('route_audit',audit,json.loads((audit/'AUDIT_MANIFEST.json').read_text())['files'])]
    for name in ['H3Q_ANALYSIS_20261120_V001','INTERNAL_LIFECYCLE_20261121_V001','INTERLEAVED_MULTISCALE_20261121_V001','COVER_FLOW_AUDIT_20261121_V001']:
        base=rb/name;groups.append((name,base,json.loads((base/'FINAL_MANIFEST.json').read_text())['files']))
    counts={};errors=[]
    for name,base,items in groups:
        for item in items:
            p=base/item['path']
            if not p.exists() or sha(p)!=item['sha256']:errors.append({'group':name,'path':item['path']})
        counts[name]=len(items)
    pins=json.loads((HERE/'PINNED_SOURCE_INPUTS.json').read_text())
    assert all(sha(ROOT/x['path'])==x['sha256'] for x in pins)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(HERE.parent.parent),text=True).strip()
    changes=subprocess.check_output(['git','status','--porcelain=v1','-uno'],cwd=str(HERE.parent.parent),text=True)
    assert not errors and not changes and head=='6d532b2c795c0778f57d8023b23b5fedfc48b010'
    result={'passed':True,'utc':datetime.now(timezone.utc).isoformat(),'counts':counts,'prior_hashes':sum(counts.values()),
            'current_source_input_hashes':len(pins),'errors':errors,'tracked_changes':changes,'HEAD':head,
            'scope':'Integrity only; not a re-certification of all historical mathematical claims.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
