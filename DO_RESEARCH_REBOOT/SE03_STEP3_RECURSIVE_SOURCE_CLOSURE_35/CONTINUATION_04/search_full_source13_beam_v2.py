"""Continue the exact bounded falsification search with ancestry-safe pruning.

Discarding dominated exploratory states sacrifices coverage, not source
validity of retained edges/cycles. No passing claim is a universal proof.
"""
from pathlib import Path
p=Path(__file__).with_name('search_full_source13_beam.py');s=p.read_text()
a="    if BATCH==1:\n        with (F/'ranked13_LOW_search_01.pkl').open('rb') as f:z=pickle.load(f)"
b="    if BATCH in (1,2):\n        with (F/'ranked13_LOW_search_01.pkl').open('rb') as f:z=pickle.load(f)"
assert s.count(a)==1;s=s.replace(a,b)
a="            for a in [b]+special:"
b="            low=int(D[lo:hi].min());special += [lo+i for i in range(hi-lo) if int(D[lo+i])==low][:3]\n            special += [lo+((g*104729+j*7919)%(hi-lo)) for j in range(4)]\n            for a in [b]+special:"
assert s.count(a)==1;s=s.replace(a,b)
a="    def check_cycle(key):"
b="""    def prune_to(keys):
        keep=set(keys);todo=list(keep)
        while todo:
            u=todo.pop();p=records[u][1]
            if p is not None and p not in keep:keep.add(p);todo.append(p)
        return {k:records[k] for k in keep}
    def check_cycle(key):"""
assert s.count(a)==1;s=s.replace(a,b)
a="        while frontier and time.process_time()-START<CAP-4:\n            newfront={};i=0"
b="        while frontier and time.process_time()-START<CAP-4:\n            if len(records)>60000:records=prune_to(frontier)\n            newfront={};i=0"
assert s.count(a)==1;s=s.replace(a,b)
a="                if len(records)>=150000 or live>=1900000:status='RECORD_GUARD_CHECKPOINT';break"
b="""                if len(records)>=150000:
                    records=prune_to(frontier[i:]+list(newfront))
                    if len(records)>=140000:status='RECORD_GUARD_CHECKPOINT';break
                if live>=1900000:status='RECORD_GUARD_CHECKPOINT';break"""
assert s.count(a)==1;s=s.replace(a,b)
s=s.replace("if value>6 and processed%127==0:","if value>3 and processed%127==0:")
s=s.replace("F/'search_full_source13_beam.py')}}", "F/'search_full_source13_beam.py',F/'search_full_source13_beam_v2.py')}}")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
