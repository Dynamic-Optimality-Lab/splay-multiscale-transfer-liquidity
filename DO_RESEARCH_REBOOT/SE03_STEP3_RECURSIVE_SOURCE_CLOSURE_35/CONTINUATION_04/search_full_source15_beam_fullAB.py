"""All original A targets and all odd genuine B targets, including mixed cores."""
from pathlib import Path
p=Path(__file__).with_name('search_full_source15_beam_fullA.py');s=p.read_text()
s=s.replace("exec(compile(s,str(Path(__file__).resolve()),'exec'))",'')
env={'__file__':str(p),'__name__':'source_builder_only'};exec(compile(s,str(p),'exec'),env);s=env['s']
start=s.index('    def allowed(t,x):');end=s.index('    def balanced(lo,hi):',start)
s=s[:start]+"    def allowed(t,x):\n        return x%2==1\n"+s[end:]
s=s.replace('assert h==q','assert h in (q,q+1)')
s=s.replace("'B_domain':'original source-valid SS maximal eight-mark steps'", "'B_domain':'all original ordinary odd KEEP accesses; mixed and smaller cores retained'")
s=s.replace("F/'search_full_source15_beam_fullA.py')}}", "F/'search_full_source15_beam_fullA.py',F/'search_full_source15_beam_fullAB.py')}}")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
