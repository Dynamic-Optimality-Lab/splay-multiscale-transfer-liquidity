from pathlib import Path
p=Path('DO_RESEARCH_REBOOT/M3_MSK01/complete_v2.py');q=Path('DO_RESEARCH_REBOOT/M3_CHIB01/complete.py');assert not q.exists()
s=p.read_text().replace('from build_v2 import','from build import').replace("initial=array('i',[-c['psi'][b] for b in a['ordinary_b']])","initial=array('i',[0]*N)")
with q.open('x',encoding='utf-8') as f:f.write(s)
print({'prepared':True})
