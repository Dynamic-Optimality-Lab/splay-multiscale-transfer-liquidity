import json
from pathlib import Path
BASE=Path(__file__).resolve().parent

def main():
    run=json.loads((BASE/'run_result.json').read_text());count=0
    for sig in run['completed_signatures']:
        folder=BASE/('s'+''.join(map(str,sig)));out=folder/'metadata.json'
        if out.exists():continue
        c=json.loads((folder/'relation.json').read_text());a=json.loads((folder/'audit.json').read_text());assert a['status']=='INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS'
        with out.open('x') as f:json.dump({'sigma':sig,'classes':c['classes'],'shadows':c['shadows'],'potential_sha256':a['potential_sha256']},f,separators=(',',':'))
        count+=1
    print(json.dumps({'new_metadata_files':count,'completed_canonical_tables':len(run['completed_signatures'])}),flush=True)
if __name__=='__main__':main()
