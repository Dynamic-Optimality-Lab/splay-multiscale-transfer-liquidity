"""Read-only verification of all original pins and every prior sealed run."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=Path('\\\\?\\'+str(HERE.parent.parent))


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def main():
    reboot=ROOT/'DO_RESEARCH_REBOOT'
    audit=reboot/'DO_ROUTE_AUDIT_20261120'
    originals=[x for x in map(json.loads,(audit/'corpus_inventory.jsonl').read_text(encoding='utf-8').splitlines()) if x.get('sha256')]
    groups=[('original_corpus',ROOT,originals),('route_audit',audit,json.loads((audit/'AUDIT_MANIFEST.json').read_text())['files'])]
    for label,dirname in [('H3q','H3Q_ANALYSIS_20261120_V001'),('internal_lifecycle','INTERNAL_LIFECYCLE_20261121_V001'),('interleaved_multiscale','INTERLEAVED_MULTISCALE_20261121_V001')]:
        base=reboot/dirname
        groups.append((label,base,json.loads((base/'FINAL_MANIFEST.json').read_text())['files']))
    counts={};failures=[]
    for name,base,items in groups:
        for item in items:
            path=base/item['path']
            if not path.exists() or digest(path)!=item['sha256']:
                failures.append({'group':name,'path':item['path']})
        counts[name]=len(items)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(HERE.parent.parent),text=True).strip()
    status=subprocess.check_output(['git','status','--porcelain=v1','-uno'],cwd=str(HERE.parent.parent),text=True)
    assert not failures and not status and head=='6d532b2c795c0778f57d8023b23b5fedfc48b010'
    input_names=[
      'RG01_PRIMITIVE_ACCOUNTING.md','IAGS12_D2_RESIDUAL_REGENERATION_COST.md',
      'RESEARCH_RULES.md',
      'ROUTE04_RELAXED_UNIVERSAL_CD_20261108/RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md',
      'PARALLEL_ROUTE02_STEP04_LINEAR_INCIDENCE_20261108/STEP04_LINEAR_INCIDENCE_SOURCE_GEOMETRY.md',
      'ROUTE02_ROUTE04_UNIVERSAL_SOURCE_WORK_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_PROOF_OR_REFUTATION.md',
      'ROUTE02_ROUTE04_REGENERATION_CONTINUATION_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md',
      'ROUTE02_ROUTE04_TF2_AUDIT_AMPLIFICATION_20261109/TF2_INDEPENDENT_AUDIT_AND_PARAMETRIC_AMPLIFICATION.md']
    pins=[{'path':'DO_RESEARCH_REBOOT/'+s,'sha256':digest(reboot/s)} for s in input_names]
    out={'passed':True,'utc':datetime.now(timezone.utc).isoformat(),'counts':counts,'total_prior_hashes':sum(counts.values()),
         'failures':failures,'tracked_changes':status,'HEAD':head,
         'scope':'Integrity only; no assertion that every historical mathematical claim has been independently re-proved.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'PINNED_INPUTS.json').write_text(json.dumps(pins,indent=2))
        (HERE/'PRESERVATION_VERIFICATION.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out))


if __name__=='__main__':
    main()
