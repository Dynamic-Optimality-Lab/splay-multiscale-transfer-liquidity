"""UTF-8 finalization; retain the first finalizer's mojibake main report as v002.

The v002 resume refused to overwrite that different historical output. This
version writes the correctly decoded main report as v003, then verifies all
old bytes and publishes the final verdict. Run with python -X utf8 -B.
"""
import sys
import finalize_audit as F
if not sys.flags.utf8_mode:raise RuntimeError('Use python -X utf8 -B')
original_write=F.write
def versioned_write(name,data):
    if name=='U4_05_E0_MINIMAL_DEFICIENCY_v002.md' and (F.OUT/name).exists():
        if (F.OUT/name).read_text(encoding='utf-8')!=data:
            raise AssertionError('Existing E0 formatting revision differs')
        return
    if name=='U4_AZ_RESEARCH_REPORT_v002.md':name='U4_AZ_RESEARCH_REPORT_v003.md'
    if name=='delivery_manifest.json':
        data={**data,'main_report':'U4_AZ_RESEARCH_REPORT_v003.md',
              'formatting_history':'v002 retained; v003 uses correct explicit UTF-8 decoding'}
    return original_write(name,data)
F.write=versioned_write
if __name__=='__main__':F.main()
