"""Pin the actual upstream engines and full original source dependencies."""
import sys
import json
import hashlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_TRACE_ENGINE_20261122_V001';ROOT=HERE.parent.parent


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    pins={r['path']:r['sha256'] for r in json.loads((PREV/'PINNED_SOURCE_INPUTS.json').read_text(encoding='utf-8'))}
    paths=[PREV/'FINAL_MANIFEST.json',HERE.parent/'RESEARCH_RULES.md']+[PREV/r['path'] for r in json.loads((PREV/'FINAL_MANIFEST.json').read_text(encoding='utf-8'))['files']]
    paths.extend(HERE.parent/p for p in ('INTERNAL_PIVOT_DONOR_20261121_V001/replay.py','INTERNAL_PIVOT_DONOR_20261121_V001/sources.py','COVER_FLOW_AUDIT_20261121_V001/verify.py','GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/model.py'))
    for p in paths:pins[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    dest=HERE/'PINNED_SOURCE_INPUTS.json';assert not dest.exists();dest.write_text(json.dumps([{'path':p,'sha256':h} for p,h in sorted(pins.items())],indent=2),encoding='utf-8');print({'upstream_inputs':len(pins)})


if __name__=='__main__':main()
