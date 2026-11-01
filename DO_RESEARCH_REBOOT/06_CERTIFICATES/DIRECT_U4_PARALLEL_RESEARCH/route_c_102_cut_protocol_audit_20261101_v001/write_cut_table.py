"""Render the already independently verified102-cut classification."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NI = HERE.parent / 'route_c_nowhere_immediate_residual_20261101_v001'
audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
assert audit['status'] == 'PASS'
assert audit['cut_ledgers_sha256'] == hashlib.sha256((HERE / 'cut_ledgers.json').read_bytes()).hexdigest()
trials = json.loads((HERE / 'cut_ledgers.json').read_text(encoding='utf-8'))['trials']['normal']
rows = json.loads((NI / 'full_source_replays.json').read_text(encoding='utf-8'))['cycle']
lines = ['# All102 physical cuts: verified UD/FI results', '',
    'FINITE-EXACT. Cut k starts at zero-based recurrent source occurrence k. Each pass visits all102 physical blocks once, with empty initial history, no startup units and no second lap. Reflected results are identical at the same physical indices.', '',
    '|Cut|First request|UD final debt|UD result|FI final debt|FI result|',
    '|---:|---|---:|---|---:|---|']
for cut in range(102):
    a, b, row = trials['UD'][cut], trials['FI'][cut], rows[cut]
    request = ('K' if row['mode'] == 'KEEP' else 'D')+str(row['key'])
    lines.append(f"|{cut}|{request}|{a['final_debt']}|{'ACCEPT' if a['accepted'] else 'REJECT'}|{b['final_debt']}|{'ACCEPT' if b['accepted'] else 'REJECT'}|")
lines += ['', 'UD accepts0 cuts and rejects102. FI accepts92 cuts and rejects10. Each rejected FI pass has exactly one unpaid demand. Every accepted FI pass supplies98 distinct-unit assignments. Full histories, reservations, residual cursors, transfers and assignments are in cut_ledgers.json; alternatives are separate ledgers and never pooled.', '']
with (HERE / 'CA02_ALL_CUTS.md').open('x', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('CA02_ALL_CUTS.md:102 verified rows written exclusively.')
