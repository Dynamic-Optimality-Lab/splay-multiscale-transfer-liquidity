"""Exact four-depth extension of inherited dirty normal forms; no solver."""
import sys,json,time
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M2_DSK01')
from diagnostic import replay
from left_diagnostic import replay_left
from certify_dirty import cases
BASE=Path('DO_RESEARCH_REBOOT/M3_OUT01')

def main():
    out=BASE/'diagnostic.json';assert not out.exists();start=time.process_time()
    rows=[];bad=[]
    # Each inherited geometry repeats five times, once for d14..18.
    for meta,source,period,word in cases():
        if meta['d']!=14:continue
        for depth in range(10,14):
            assert time.process_time()-start<120,'UNKNOWN diagnostic CPU cap'
            if meta['family']=='RIGHT_SELF':
                _,_,_,_,dest,claims,cycle=replay(meta['h'],meta['bits'],depth)
            else:
                _,_,_,_,_,dest,claims,_=replay_left(meta['h'],meta['s'],meta['bits'],meta['zero_mode'],depth)
                cycle=None
            row={**meta,'d':depth,'final_root':dest['root'],'root_claims':claims}
            rows.append(row)
            if not claims:bad.append({**row,'normal_form':dest,'forced_cycle':cycle})
    result={'status':'PASS_NORMAL_FORM_ROOT_CLAIMS' if not bad else 'ROOT_CLAIM_TEMPLATE_FAILURE',
            'cases':len(rows),'root_claim_cases':len(rows)-len(bad),'failures':bad,
            'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','failures')},indent=2))
    if bad:print(json.dumps(bad[:2],indent=2))

if __name__=='__main__':main()
