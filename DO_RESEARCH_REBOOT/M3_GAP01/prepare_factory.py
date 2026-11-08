"""Reuse environment construction; A fringe identity and B gap proxy differ."""
from pathlib import Path
p=Path('DO_RESEARCH_REBOOT/M3_ACL01/original_controls.py');q=Path('DO_RESEARCH_REBOOT/M3_GAP01/original_factory.py');assert not q.exists()
s=p.read_text().split('\ndef main():')[0]
old='bp,bd=V.path(bc,x);bw.append';assert old in s
s=s.replace(old,'bx=-1 if x<0 else x;bp,bd=V.path(bc,bx);bw.append')
old="if mode=='K':bc=S.trace(bc,x)[0]";assert old in s
s=s.replace(old,"if mode=='K':bc=S.trace(bc,bx)[0]")
with q.open('x',encoding='utf-8') as f:f.write(s)
print({'factory_created':str(q)})
