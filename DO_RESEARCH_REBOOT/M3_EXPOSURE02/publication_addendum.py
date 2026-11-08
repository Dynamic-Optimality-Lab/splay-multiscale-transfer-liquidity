"""Versioned publication addendum; completed evidence and manifests unchanged."""
import json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parent=BASE/'final_manifest.json';assert parent.exists() and not (BASE/'final_manifest_v2.json').exists()
    report={'status':'PUBLICATION_CLARIFICATION_NO_NEW_MATHEMATICAL_TESTS','parent_manifest':parent.as_posix(),'parent_manifest_sha256':sha(parent),'original_manifest_preserved':True,'new_documents':[{'path':(BASE/n).as_posix(),'sha256':sha(BASE/n)} for n in ('ADDENDUM_RANGE_ARGUMENT.md','publication_addendum.py')],'mathematical_status_unchanged':True,'public_debt_constructed':False,'both_gaps_closed':False,'M3_status':'OPEN','new_finite_population_tests':0,'new_source_queries':0,'resource_accounting':'publication/provenance metadata under existing convention'}
    with (BASE/'final_manifest_v2.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='new_documents'},indent=2))
if __name__=='__main__':main()
