"""Render independently verified source budgets and all rejection certificates."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
audit=json.loads((HERE/'independent_audit.json').read_text(encoding='utf-8'))
assert audit['status']=='PASS'
for name,h in audit['output_hashes'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h
budgets=json.loads((HERE/'fresh_run_budget_certificate.json').read_text())['cases']
certs=json.loads((HERE/'FI_rejection_certificates.json').read_text())['certificates']
lines=['# Fixed-source budgets and exact rejected-cut certificates','',
    'These are14 previously source-verified controls and their636 previously checked cuts. Every control is FI-accepted at some cut. The44 rows below describe individual rejected cuts; none is asserted to be an all-cut counterexample. Source names and full trees are in fixed_corpus_sources.json.','',
    '## Source-local budget controls','',
    '|Control|E|C_D|L_fresh|Gamma|Constructed positive cut|',
    '|---:|---:|---:|---:|---:|---:|']
for b in budgets:lines.append(f"|{b['case']}|{b['E']}|{b['C_D']}|{b['L_fresh']}|{b['Gamma']}|{b['constructed_positive_cut']}|")
lines+=['','Controls0..11 are the twelve old ordinary/reflected FI witnesses. Controls12/13 are H5 and its reflection. All budgets are strictly negative. Controls6/7 have run gaps2 and-12, so an individually starved run is paid through later physical pools; private repayment of every run is not assumed.','',
    '## All44 rejected-cut certificates','',
    '|Control|Cut|Busy source blocks|Final debt|Source delta sum|Reserved loss|Paid facts retained at start|',
    '|---:|---:|---|---:|---:|---:|---:|']
for c in certs:
    ids=','.join(map(str,c['busy_blocks']))
    lines.append(f"|{c['case']}|{c['cut']}|{ids}|{c['terminal_debt']}|{c['source_delta_sum']}|{c['reserved_loss_sum']}|{len(c['paid_source_history_before_busy'])}|")
lines+=['','All indices are zero-based physical block indices. The44 canonical suffixes have lengths1(26 cases),2(16 cases),or3(2 cases). All44 controls have zero reserved loss on the final busy suffix;32 retain earlier paid source facts. The universal certificate split permits nonzero reserved loss, but this fixed corpus does not supply that failure type. No extra source word or size was added to seek it.','']
with (HERE/'RC02_CONTROL_AND_CERTIFICATE_TABLES.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines))
print('Rendered14 budget rows and44 exact source certificates exclusively.')
