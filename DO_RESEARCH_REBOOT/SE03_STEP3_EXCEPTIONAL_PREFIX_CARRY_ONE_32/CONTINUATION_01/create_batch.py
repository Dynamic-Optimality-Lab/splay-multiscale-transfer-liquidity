"""Metadata-only creation of one capped source/audit batch wrapper."""
import sys,re,json
from pathlib import Path
B=Path(__file__).resolve().parent
backend,phase,start,stop=sys.argv[1:];start=int(start);stop=int(stop)
assert backend in ('producer','independent') and re.fullmatch(r'(cold|verify)[0-9]+',phase)
assert 0<=start<stop<=5577
with (B/('audit_'+phase+'.py')).open('x',encoding='utf-8') as f:
    f.write('import sys\nfrom cold_frames import run\nrun('+repr(backend)+','+str(start)+','+str(stop)+','+repr(phase)+',float(sys.argv[1]),int(sys.argv[2]))\n')
print(json.dumps({'created':phase,'backend':backend,'range':[start,stop]}))
