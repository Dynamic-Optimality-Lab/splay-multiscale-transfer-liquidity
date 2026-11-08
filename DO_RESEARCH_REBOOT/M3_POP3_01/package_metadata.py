import json
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_POP3_01')
def main():
    run=json.loads((BASE/'run_result.json').read_text());assert run['status']=='ALL7_LEADING_THREE_UNIT_FINITE_CERTIFICATES_PASS'
    for sig in run['completed_signatures']:
        folder=BASE/('s'+''.join(map(str,sig)));out=folder/'metadata.json';assert not out.exists()
        c=json.loads((folder/'relation.json').read_text());a=json.loads((folder/'audit.json').read_text());assert a['status']=='INDEPENDENT_POPULATION_PREFIX_AND_RESIDUAL_PASS'
        with out.open('x',encoding='utf-8') as f:json.dump({'sigma':sig,'classes':c['classes'],'shadows':c['shadows'],'potential_sha256':a['potential_sha256']},f,separators=(',',':'))
    print(json.dumps({'metadata_files':len(run['completed_signatures'])}),flush=True)
if __name__=='__main__':main()
