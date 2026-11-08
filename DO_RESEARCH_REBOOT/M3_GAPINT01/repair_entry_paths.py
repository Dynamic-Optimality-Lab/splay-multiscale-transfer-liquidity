from pathlib import Path
dst=Path('DO_RESEARCH_REBOOT/M3_GAPINT02')
for old,new in (('complete.py','complete_v3.py'),('verify.py','verify_v3.py'),('potential.py','potential_v3.py'),('original_audit.py','original_audit_v3.py')):
    s=(dst/old).read_text().replace("sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_GAPINT01')","sys.path.append('DO_RESEARCH_REBOOT/M3_GAPINT01')")
    if old=='original_audit.py':s=s.replace('from potential import','from potential_v3 import')
    q=dst/new;assert not q.exists();q.write_text(s)
p=Path('DO_RESEARCH_REBOOT/M3_GAPINT01/prepare_next.py');q=p.with_name('prepare_next_v2.py');assert not q.exists();q.write_text(p.read_text().replace("sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_GAPINT01')","sys.path.append('DO_RESEARCH_REBOOT/M3_GAPINT01')"))
print({'versioned_entry_paths_corrected':True})
