"""Fresh-entry reproduction helper with corrected final progress count.

The retained research entry was captured successfully inline. The unexecuted
saved V001 helper used the wrong key only in its final print. This wrapper
fixes that print, preserving the old helper and every scientific artifact.
"""
from pathlib import Path

original=Path(__file__).resolve().parent/'capture_entry.py'
source=original.read_text(encoding='utf-8')
old="len(pins['files'])"
assert source.count(old)==1
namespace={'__file__':str(original),'__name__':'__main__'}
exec(compile(source.replace(old,'len(pins)'),str(original),'exec'),namespace)
