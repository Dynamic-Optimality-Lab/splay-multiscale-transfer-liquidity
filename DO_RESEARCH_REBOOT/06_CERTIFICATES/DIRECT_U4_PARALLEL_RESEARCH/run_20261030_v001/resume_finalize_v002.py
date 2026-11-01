"""Resume final verification with explicit UTF-8; preserve completed formatting versions.

Invoke: python -X utf8 -B <this script>. The first finalizer reached the
report-link scan after hashing, then encountered Windows cp1252 decoding.
No integrity verdict was published from that interrupted run.
"""
import sys,json
import finalize_audit as F

if not sys.flags.utf8_mode:
    raise RuntimeError('Use python -X utf8 -B for explicit UTF-8 on Windows')

original_write=F.write
def resume_write(name,data):
    if name in ('U4_05_E0_MINIMAL_DEFICIENCY_v002.md','U4_AZ_RESEARCH_REPORT_v002.md') and (F.OUT/name).exists():
        if (F.OUT/name).read_text(encoding='utf-8')!=data:
            raise AssertionError('Existing formatting version differs; will not overwrite')
        return
    return original_write(name,data)

F.write=resume_write
if __name__=='__main__':F.main()
