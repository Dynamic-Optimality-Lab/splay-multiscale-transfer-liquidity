from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
p=BASE/'source_audit_v2.py';assert not p.exists();s=(BASE/'source_audit.py').read_text()
assert s.count("out=BASE/'source_audit.json'")==1 and s.count('helper=OUT if h==9 or (g+h)%2 else IN')==1
s=s.replace("out=BASE/'source_audit.json'","out=BASE/'source_audit_v2.json'")
s=s.replace('def main():','from proposal_factory import proposals\nFIN,FOUT=proposals(IN),proposals(OUT)\ndef main():',1)
s=s.replace('helper=OUT if h==9 or (g+h)%2 else IN','helper=FOUT if h==9 or (g+h)%2 else FIN')
s=s.replace("'full_M3_proved':False}","'full_M3_proved':False,'proposal_fixture_AST_edits':FIN.proposal_edits+FOUT.proposal_edits}")
with p.open('x',encoding='utf-8') as f:f.write(s)
print('Created source_audit_v2.py; original predicate checks unchanged.',flush=True)
