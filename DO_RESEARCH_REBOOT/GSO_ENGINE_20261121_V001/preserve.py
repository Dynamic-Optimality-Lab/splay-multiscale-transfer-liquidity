"""Byte-integrity audit of all4583 previous pinned/sealed artifacts."""
import hashlib
import json
import subprocess
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;ROOT=Path('\\\\?\\'+str(HERE.parent.parent))


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def main():
    rb=ROOT/'DO_RESEARCH_REBOOT';route=rb/'DO_ROUTE_AUDIT_20261120'
    original=[x for x in map(json.loads,(route/'corpus_inventory.jsonl').read_text(encoding='utf-8').splitlines()) if x.get('sha256')]
    groups=[('original_corpus',ROOT,original),('route_audit',route,json.loads((route/'AUDIT_MANIFEST.json').read_text())['files'])]
    for name in ['H3Q_ANALYSIS_20261120_V001','INTERNAL_LIFECYCLE_20261121_V001','INTERLEAVED_MULTISCALE_20261121_V001','COVER_FLOW_AUDIT_20261121_V001','INTERNAL_PIVOT_DONOR_20261121_V001','GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001']:
        base=rb/name;groups.append((name,base,json.loads((base/'FINAL_MANIFEST.json').read_text())['files']))
    errors=[];counts={}
    for name,base,files in groups:
        for z in files:
            p=base/z['path']
            if not p.exists() or digest(p)!=z['sha256']:errors.append({'group':name,'path':z['path']})
        counts[name]=len(files)
    assert sum(counts.values())==4583 and not errors
    pins=json.loads((HERE/'PINNED_SOURCE_INPUTS.json').read_text(encoding='utf-8'))
    assert all(digest(ROOT/z['path'])==z['sha256'] for z in pins)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(HERE.parent.parent),text=True).strip()
    changes=subprocess.check_output(['git','status','--porcelain=v1','-uno'],cwd=str(HERE.parent.parent),text=True)
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and not changes
    out={'passed':True,'utc':datetime.now(timezone.utc).isoformat(),'counts':counts,'prior_hashes':sum(counts.values()),'current_pinned_inputs':len(pins),'HEAD':head,'tracked_changes':changes,'errors':errors,'scope':'Byte integrity; not recertification of all historical mathematical claims.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
