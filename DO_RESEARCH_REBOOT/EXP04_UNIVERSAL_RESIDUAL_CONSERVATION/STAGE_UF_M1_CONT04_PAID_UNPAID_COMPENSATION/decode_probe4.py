"""Export every literal long original event or complete-boundary reference."""
from base4 import *
from probe_long4 import expanded,expanded_boundaries

if __name__=='__main__':
    assert len(sys.argv)==3 and sys.argv[1] in ('--jsonl','--boundaries')
    dest=Path(sys.argv[2]);assert dest.is_absolute()
    p=load(ROOT/'PROBE_SHORT_PHYS.json');rule=load(ROOT/'PROBE_EVENT_EXPANSION.json')
    data=expanded(p,rule) if sys.argv[1]=='--jsonl' else expanded_boundaries(p,rule)
    count=0
    with dest.open('x',encoding='utf-8') as stream:
        for row in data:stream.write(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n');count+=1
    print('EXPORTED',count,'literal original records to',str(dest),flush=True)
