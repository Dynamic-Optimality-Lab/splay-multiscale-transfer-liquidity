"""Pin the sealed upstream engines, source universe and original witnesses."""
import sys
import json
import hashlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;P=HERE.parent/'GSO_COMPOSITION_AUDIT_20261121_V001'


def main():
    rows=json.loads((P/'PINNED_SOURCE_INPUTS.json').read_text(encoding='utf-8'));pins={r['path']:r['sha256'] for r in rows}
    requested=[P/'FINAL_MANIFEST.json',HERE.parent/'RESEARCH_RULES.md']+[HERE.parent/'GSO_ENGINE_20261121_V001'/f for f in ('kernel.py','teacher.py','learner.py','symbolic.py','registry.py','gso.py','CertificateKernel.lean')]
    requested.extend(P/r['path'] for r in json.loads((P/'FINAL_MANIFEST.json').read_text(encoding='utf-8'))['files'])
    for p in requested:pins[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    out=[{'path':p,'sha256':h} for p,h in sorted(pins.items())];dest=HERE/'PINNED_SOURCE_INPUTS.json';assert not dest.exists();dest.write_text(json.dumps(out,indent=2),encoding='utf-8');print({'pinned_old_inputs':len(out)})


if __name__=='__main__':main()
