"""Exclusive verifier repair: include the already validated lap-zero B endpoint."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=(HERE/'independent_verify.py').read_text(encoding='utf-8')
needle='shared_B={};maps=[]'
assert source.count(needle)==1
source=source.replace(needle,'shared_B={0:b0};maps=[]',1)
with (HERE/'independent_verify_v002.py').open('x',encoding='utf-8') as f:f.write(source)
