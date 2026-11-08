"""Keep source-search coverage across actual A/B root classes.

This changes only the bounded falsification heuristic, never source costs
or the mathematical theorem. Pruned states give no positive proof.
"""
from pathlib import Path
p=Path(__file__).with_name('search_full_source15_beam_fullAB_reserve8.py');s=p.read_text()
s=s.replace("exec(compile(s,str(Path(__file__).resolve()),'exec'))",'')
env={'__file__':str(p),'__name__':'source_builder_only'};exec(compile(s,str(p),'exec'),env);s=env['s']
a='    def prune_to(keys):'
b='''    def pick(values):
        import bisect
        ordered=sorted(values,key=lambda k:(values[k],k),reverse=True)
        classes={(bisect.bisect_right(R.OFF[15],a),bisect.bisect_right(R.OFF[15],b)) for a,b in ordered}
        quota=max(1,3000//max(1,len(classes)));counts={};chosen=[];skip=[]
        for key in ordered:
            a,b=key;c=(bisect.bisect_right(R.OFF[15],a),bisect.bisect_right(R.OFF[15],b))
            if counts.get(c,0)<quota and len(chosen)<3000:chosen.append(key);counts[c]=counts.get(c,0)+1
            else:skip.append(key)
        return chosen+skip[:max(0,3000-len(chosen))]
    def prune_to(keys):'''
assert s.count(a)==1;s=s.replace(a,b)
a='sorted(newfront,key=lambda k:(newfront[k],k),reverse=True)[:3000]'
assert s.count(a)==4;s=s.replace(a,'pick(newfront)')
s=s.replace("F/'search_full_source15_beam_fullAB_reserve8.py')}}", "F/'search_full_source15_beam_fullAB_reserve8.py',F/'search_full_source15_beam_diverse.py')}}")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
