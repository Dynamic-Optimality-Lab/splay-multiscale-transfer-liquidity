"""Original-source search, adding explicit shallow-A/deep-B seed frames."""
from pathlib import Path
p=Path(__file__).with_name('search_full_source13_beam_v2.py');s=p.read_text()
# Obtain the previous exact generated program without executing it.
s=s.replace("exec(compile(s,str(Path(__file__).resolve()),'exec'))", "")
env={'__file__':str(p),'__name__':'source_builder_only'};exec(compile(s,str(p),'exec'),env)
s=env['s'];s=s.replace('if BATCH in (1,2):','if BATCH in (1,2,3):')
a='            for a in [b]+special:'
b='''            def balanced(lo,hi):
                if lo>hi:return None
                k=(lo+hi)//2;return (k,balanced(lo,k-1),balanced(k+1,hi))
            for x in range(1,14):
                if x==g:continue
                if x<g:t=(g,(x,balanced(1,x-1),balanced(x+1,g-1)),balanced(g+1,13))
                else:t=(g,balanced(1,g-1),(x,balanced(g+1,x-1),balanced(x+1,13)))
                special.append(R.rank_tree(t,1,13))
            for a in [b]+special:'''
assert s.count(a)==1;s=s.replace(a,b)
s=s.replace("records.setdefault((a,b),(0,None,None,None,None,None));frontier.append((a,b))", "records[(a,b)]=max(records.get((a,b),(-10**9,)),(0,None,None,None,None,None),key=lambda z:z[0]);frontier.append((a,b))")
s=s.replace("F/'search_full_source13_beam_v2.py')}}", "F/'search_full_source13_beam_v2.py',F/'search_full_source13_beam_v3.py')}}")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
