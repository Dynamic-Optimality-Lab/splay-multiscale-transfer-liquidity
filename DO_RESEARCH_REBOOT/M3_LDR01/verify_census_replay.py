"""Every negative census row rechecked through frozen B replay functions."""
import sys,json,time,hashlib
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M2_SEP01','DO_RESEARCH_REBOOT/M3_PHI01']
from experiment import D,trace,unpack,structure
from verify_full_mixed import from_serial,bmodel
from PC_B_CONTROLLER import verify_bpath,b_splay_event
OUT=Path('DO_RESEARCH_REBOOT/M3_LDR01/census_replay.json')
def main():
    assert not OUT.exists();start=time.process_time()
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    models=[bmodel(from_serial(n['tree']),True) for n in c['nodes']];rows=[]
    for e in c['edges']:
        assert time.process_time()-start<120,'UNKNOWN: replay audit cap'
        source=models[e['source']];expected=models[e['destination']]
        b,bt,path,dirs=trace(source,e['target'],e['depth'])
        assert verify_bpath(D,b,bt,0).v
        raw=unpack(b_splay_event(D,b,bt,0,D.const_bool(False)))
        assert structure(raw)==structure(expected),e
        assert raw['lo']==source['lo'] and raw['hi']==source['hi']
        rows.append({**e,'production_replay_matches':True,
                     'output_structure_sha256':hashlib.sha256(json.dumps(structure(raw)).encode()).hexdigest()})
    result={'status':'COMPLETE','cases':len(rows),'all_match':True,
            'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
