"""Format-only audit copy; preserve all completed proof/evidence files."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parent=BASE/'final_manifest.json'
    assert parent.exists()
    old=(BASE/'PROOF_AUDIT.md').read_text(encoding='utf-8')
    assert old.count('legs,+J-source legs')==1
    corrected=old.replace('legs,+J-source legs','legs,\nJ-source legs')
    with (BASE/'PROOF_AUDIT_v2.md').open('x',encoding='utf-8') as stream:stream.write(corrected)
    obj={'status':'FORMAT_ONLY_PUBLICATION_NO_NEW_MATHEMATICAL_CHECKS','parent_manifest':parent.as_posix(),'parent_manifest_sha256':sha(parent),'old_files_preserved':True,'correction':'remove one accidental plus and restore a line break in audit prose','mathematical_claims_and_resources_unchanged':True,'M3_status':'OPEN','new_finite_tests':0,'new_source_queries':0,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in (BASE/'PROOF_AUDIT_v2.md',BASE/'publication_v2.py')]}
    with (BASE/'final_manifest_v2.json').open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
    print(json.dumps({'status':obj['status'],'M3':'OPEN'}),flush=True)
if __name__=='__main__':main()
