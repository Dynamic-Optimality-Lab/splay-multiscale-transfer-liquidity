"""Fresh reproduction of the completed V002 audit, preserving partial runs.

V002 correctly resumed an already-written W certificate. This wrapper also
allows exclusive first creation in a fresh reproduction, with no scientific
or source-provenance change. Do not run over sealed output files.
"""
from pathlib import Path

HERE=Path(__file__).resolve().parent
original=HERE/'build_paired_certificates_v002.py'
source=original.read_text(encoding='utf-8')
old="if name=='walk_deep_certificate.json':"
new="if name=='walk_deep_certificate.json' and (HERE/name).exists():"
assert source.count(old)==1
namespace={'__file__':str(original),'__name__':'__main__'}
exec(compile(source.replace(old,new),str(original),'exec'),namespace)
