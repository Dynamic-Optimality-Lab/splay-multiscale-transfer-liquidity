"""Byte integrity of all4877 earlier pinned/sealed research artifacts."""
import hashlib
import json
import subprocess
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=Path('\\\\?\\'+str(HERE.parent.parent))


def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for data in iter(lambda:f.read(1048576),b''):h.update(data)
    return h.hexdigest()


def main():
    rb=ROOT/'DO_RESEARCH_REBOOT';route=rb/'DO_ROUTE_AUDIT_20261120'
    original=[x for x in map(json.loads,(route/'corpus_inventory.jsonl').read_text(encoding='utf-8').splitlines()) if x.get('sha256')]
    groups=[('original_corpus',ROOT,original),('route_audit',route,json.loads((route/'AUDIT_MANIFEST.json').read_text())['files'])]
    names=['H3Q_ANALYSIS_20261120_V001','INTERNAL_LIFECYCLE_20261121_V001','INTERLEAVED_MULTISCALE_20261121_V001','COVER_FLOW_AUDIT_20261121_V001','INTERNAL_PIVOT_DONOR_20261121_V001','GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001','GSO_ENGINE_20261121_V001']
    for name in names:
        base=rb/name;groups.append((name,base,json.loads((base/'FINAL_MANIFEST.json').read_text())['files']))
    counts={};errors=[]
    for name,base,files in groups:
        counts[name]=len(files)
        for item in files:
            path=base/item['path']
            if not path.exists() or digest(path)!=item['sha256']:errors.append({'group':name,'path':item['path']})
    assert sum(counts.values())==4877 and not errors
    pins=json.loads((HERE/'PINNED_SOURCE_INPUTS.json').read_text(encoding='utf-8')) if (HERE/'PINNED_SOURCE_INPUTS.json').exists() else []
    assert all(digest(ROOT/x['path'])==x['sha256'] for x in pins)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(HERE.parent.parent),text=True).strip();changed=subprocess.check_output(['git','status','--porcelain=v1','-uno'],cwd=str(HERE.parent.parent),text=True)
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and not changed
    result={'passed':True,'utc':datetime.now(timezone.utc).isoformat(),'counts':counts,'prior_hashes':sum(counts.values()),'current_input_pins':len(pins),'HEAD':head,'tracked_changes':changed,'errors':errors,'scope':'Byte preservation, not independent reproving of all earlier mathematics.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
