"""Versioned context/lifecycle backend for the combined GSO engine.

Previous engine stages and exclusions remain available, read-only. This driver
does not claim to be a complete unbounded-tree theorem synthesizer.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent


def status():
    records={}
    for folder in ('run_001','core5_001'):
        path=HERE/folder/'CONTEXT_CERTIFICATE.json'
        if path.exists():
            z=json.loads(path.read_text(encoding='utf-8'));records[folder]={'C':z['C'],'scope':'Only the declared bounded-core domain, after its separately recorded symbolic compression proof.'}
    return {'engine':'GSO context/lifecycle backend1','previous_engine':'GSO_ENGINE_20261121_V001 (read-only)','root_status':'OPEN','first_missing':'A source-uniform shape-sensitive accounting law at arbitrarily large irreducible paired cores, including neutral B consumers and recreated/interleaved ancestry.','core_size_only_family':'REFUTED for every F_N and every finite whole-operation C by complete H_3,q equal-value witnesses; explicit all-q proof required and saved separately.','context_certificates':records,'new_unrestricted_original_residual_classes_paid':0,'whole_A_core_issuance_bound':'<= real A rotations <=2A; mathematical proof is not inferred from finite tests','forbidden_inference':'A finite table or a restricted-domain symbolic lift cannot set the unrestricted root to PROVED.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=('status','verify','preserve','core3','core5','sources','constructed'));a=p.parse_args()
    if a.command=='status':print(json.dumps(status(),indent=2));return
    script={'verify':'verify.py','preserve':'preserve.py','core3':'context.py','core5':'path_compiler.py','sources':'source_audit.py','constructed':'constructed_sources.py'}[a.command]
    if a.command not in ('verify','preserve'):assert not (HERE/'FINAL_MANIFEST.json').exists(),'sealed checkpoint: use a fresh versioned sibling'
    subprocess.run([sys.executable,'-B',str(HERE/script)],cwd=str(HERE.parent.parent),check=True)


if __name__=='__main__':main()
