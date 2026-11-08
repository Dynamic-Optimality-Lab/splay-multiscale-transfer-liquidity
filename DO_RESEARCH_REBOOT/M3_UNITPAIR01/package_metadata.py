import json
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
def main():
    run=json.loads((BASE/'run_result.json').read_text());assert run['status']=='ALL24_NEW_CANONICAL_FINITE_CERTIFICATES_PASS'
    for g,h in run['completed_pairs']:
        folder=BASE/f'p{g}_{h}';out=folder/'metadata.json';assert not out.exists()
        c=json.loads((folder/'relation.json').read_text());a=json.loads((folder/'audit.json').read_text());assert a['status']=='INDEPENDENT_FINITE_EXACT_PASS'
        obj={'g':g,'h':h,'classes':c['classes'],'shadows':c['shadows'],'keys':c['keys'],'potential_sha256':a['potential_sha256'],'status':'FINITE_EXACT_INDEPENDENT_PASS_SOURCE_FAMILY_AUDIT_PENDING'}
        with out.open('x',encoding='utf-8') as f:json.dump(obj,f,separators=(',',':'))
    print(json.dumps({'metadata_files':len(run['completed_pairs'])}),flush=True)
if __name__=='__main__':main()
