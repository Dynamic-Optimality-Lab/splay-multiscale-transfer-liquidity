"""Explicit cap amendment metadata; no cumulative usage is reset."""
from pathlib import Path
p=Path(__file__).with_name('record_symbolic_authorization_1920.py')
s=p.read_text()
s=s.replace('1920','2160').replace('1680','1920')
s=s.replace('1,920','2,160')
s=s.replace('call_f06bec57ae354b5e9e177b797d532a31','call_b0249c3580ec4c1fb3b7e89426b452e9')
s=s.replace('1675.59375','1915.46875')
exec(compile(s,str(Path(__file__).resolve()),'exec'))
