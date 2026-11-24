import hashlib
import json
import sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent


def files():
    return [{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='FINAL_MANIFEST.json']


def main():
    target=HERE/'FINAL_MANIFEST.json'
    if '--verify' in sys.argv:
        saved=json.loads(target.read_text(encoding='utf-8'));assert saved['files']==files()
        print(json.dumps({'passed':True,'files':len(saved['files']),'bytes':sum(x['bytes'] for x in saved['files'])}));return
    assert not target.exists()
    for name in ['PRESERVATION_VERIFICATION.json','run_001/INDEPENDENT_VERIFICATION.json','cold_run_002/INDEPENDENT_VERIFICATION.json','run_001/LEAN_KERNEL_CHECK.json','cold_run_002/LEAN_KERNEL_CHECK.json']:
        assert json.loads((HERE/name).read_text(encoding='utf-8'))['passed']
    ref=json.loads((HERE/'NOTION_ENGINE_REFERENCE.json').read_text(encoding='utf-8'));assert ref['readback_verified'] and all(x['verified'] and x['old_preserved'] for x in ref['workspace_updates'])
    for run in ['run_001','cold_run_002']:
        result=json.loads((HERE/run/'ENGINE_RESULT.json').read_text(encoding='utf-8'))
        assert result['source_uniform_root']=='OPEN' and result['principal_grammar_status']=='REFUTED—EXACT'
    output={'date':'2026-11-21','created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Working bounded GSO version1; exact all-finite-C obstruction to the declared full-X frontier3 whole-operation potential grammars. Original universal cost bound remains OPEN.','notion':ref,'files':files()}
    target.write_text(json.dumps(output,indent=2),encoding='utf-8');print(json.dumps({'created':True,'files':len(output['files']),'bytes':sum(x['bytes'] for x in output['files'])}))


if __name__=='__main__':main()
