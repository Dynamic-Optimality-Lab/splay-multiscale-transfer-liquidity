"""Versioned private environment helper; original compilers are unchanged."""
from pathlib import Path
src=Path('DO_RESEARCH_REBOOT/M3_GAPINT01/interior_original.py')
dst=Path('DO_RESEARCH_REBOOT/M3_OUT01/outside_original.py')
s=src.read_text()
old="go(t,0,18,19,0);assert b['kr'][8]==2;b['kr'][8]=0;b['rr'][8]=19"
assert old in s
s=s.replace(old,'go(t,0,18,19,0)')
with dst.open('x',encoding='utf-8') as f:f.write(s)
print('Prepared canonical outside-chi8 environment helper; no source predicate edited.')
