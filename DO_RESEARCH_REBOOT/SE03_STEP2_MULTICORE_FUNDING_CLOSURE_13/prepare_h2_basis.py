"""Versioned metadata preparation, preserve all accepted releases unchanged."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/'audit_h2_release.py').read_text()
s=s.replace("'h2_release_audit.json'","'h2_transition_basis.json'")
s=s.replace("'A_H2_boundary_transitions':len(transitions),","'A_H2_boundary_transitions':len(transitions),'transition_basis':sorted(transitions),")
s=s.replace("'audit_h2_release_exit.json'","'audit_h2_basis_exit.json'")
with (B/'audit_h2_basis.py').open('x',encoding='utf-8') as f:f.write(s)
