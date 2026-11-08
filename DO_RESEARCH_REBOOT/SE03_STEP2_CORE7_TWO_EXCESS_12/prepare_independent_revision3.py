"""Keep source-passing draft; normalize integer generic IDs as well as tuples."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/'audit_independent2.py').read_text()
s=s.replace("d=tuple(v['root']);assert d not in a","d=freeze(v['root']);assert d not in a")
s=s.replace('dd,uu=tuple(dd),tuple(uu);assert dd==d','dd,uu=freeze(dd),freeze(uu);assert dd==d')
s=s.replace("u=tuple(v['terminal_unit']);assert u==uu","u=freeze(v['terminal_unit']);assert u==uu")
s=s.replace("'audit_independent2_exit.json'","'audit_independent3_exit.json'")
compile(s,'audit_independent3.py','exec')
with (B/'audit_independent3.py').open('x',encoding='utf-8') as f:f.write(s)
