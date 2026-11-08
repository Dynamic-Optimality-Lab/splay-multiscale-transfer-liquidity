"""Expand the actual-source falsifier to every positive A target and true H."""
from pathlib import Path
p=Path(__file__).with_name('search_full_source15_beam.py');s=p.read_text()
s=s.replace("exec(compile(s,str(Path(__file__).resolve()),'exec'))",'')
env={'__file__':str(p),'__name__':'source_builder_only'};exec(compile(s,str(p),'exec'),env);s=env['s']
a="                for x in R.near(ta):\n                    out,h,_=lift.action(ta,15,x);assert h==1"
b="                for x in range(1,16):\n                    if x==ar:continue\n                    out,h,_=lift.action(ta,15,x);assert 1<=h<=7"
assert s.count(a)==1;s=s.replace(a,b)
s=s.replace("actions.append(('DELETE',x,out,1))","actions.append(('DELETE',x,out,h))")
s=s.replace("actions.append(('KEEP',x,out,1))","actions.append(('KEEP',x,out,h))")
s=s.replace("F/'search_full_source15_beam_v2.py')}}", "F/'search_full_source15_beam_v2.py',F/'search_full_source15_beam_fullA.py')}}")
s=s.replace("'source_leaf_substitutions_this_batch':lift.substitutions,'JR35':'OPEN'", "'source_leaf_substitutions_this_batch':lift.substitutions,'A_targets':'all15, original H','B_domain':'original source-valid SS maximal eight-mark steps','JR35':'OPEN'")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
