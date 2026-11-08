"""Content publication metadata only; never a proof seal or source check."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*a):
    return subprocess.check_output(['git', *a], cwd=ROOT, text=True).strip()

assert not git('status', '--porcelain', '--untracked-files=no')
assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
entry = read(B / 'entry.json')
assert sha(B / 'EXTREME_FRAME_FROZEN_OBLIGATION.md') == entry['frozen_obligation_sha256']
assert not (B / 'FULL_PROOF.md').exists()

required = '''SOURCE_SPEC.md EXTREME_FRAME_FROZEN_OBLIGATION.md
C20_DEPENDENCY_RECONSTRUCTION.md EXTREME_ORDER_NORMAL_FORM.md
RG_EXACT_RETURN_THEOREM.md H1Q6_EFFECTIVE_OWNER_LEDGER.md
EXTREME_NONLOCAL_SUPPLY.md EXTREME_OWNER_EXCHANGE.md REPEATED_SHARED_EXTREME.md
COLLECTIVE_SECOND_DONOR.md FOUR_ORDER_INTERFACE.md SIGNED_COMPARISON_ACCOUNTING.md
ABSOLUTE_PERIOD_VALIDITY.md ARBITRARY_SOURCE_LIFTING.md ADVERSARIAL_AUDIT.md
INDEPENDENT_AUDIT_STATUS.md GATE_U_DISCHARGE.md FINAL_VERDICT.md CHECKPOINT.md
resources_checkpoint.json'''.split()
for name in required:
    assert (B / name).is_file() and (B / name).stat().st_size > 0, name

# Content/syntax metadata checks only; mathematical certificates are NOT run.
for p in B.glob('*.json'):
    read(p)
for x in read(B / 'dependency_pins.json')['pins']:
    assert sha(ROOT / x['path']) == x['sha256'], x['path']

r = read(B / 'resources_checkpoint.json')
prior = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == prior['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == prior['cumulative_group_CPU']
assert r['new_controllers'] == r['new_independent_runs'] == r['campaign_source_engine_calls'] == 0

provenance = {
    'status': 'CONTENT_METADATA_NOT_PROOF_CERTIFICATION',
    'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
    'tracked_status': '', 'all_campaign_writes_in_21': True,
    'inherited_local_pins_preserved': entry['pins_verified'],
    'frozen_obligation_unchanged': True,
    'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
    'new_source_or_verifier_or_audit_processes': 0,
    'entry_metadata_CPU_excluded': entry['metadata_CPU_excluded'],
    'publication_metadata_CPU_excluded': time.process_time(),
    'primary_outcome': 'UNRESOLVED', 'Gate_U21': 'U_OPEN',
    'new_comparison_proof': 'MATHEMATICAL_DERIVATION_COMPLETE_INDEPENDENT_AUDIT_PENDING',
    'FULL_PROOF_created': False}
with (B / 'publication_provenance.json').open('x', encoding='utf-8') as f:
    json.dump(provenance, f, indent=2)

files = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
          'bytes': p.stat().st_size} for p in sorted(B.iterdir()) if p.is_file()
         and p.name != 'campaign_manifest.json']
with (B / 'campaign_manifest.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'CONTENT_CHECKPOINT_NOT_PROOF_SEAL',
               'primary': 'UNRESOLVED', 'Gate_U21': 'U_OPEN', 'files': files}, f, indent=2)
print(json.dumps({'status': 'PUBLISHED_C21_PRIMARY_OPEN', 'files': len(files),
                  'comparison_derivation': 'FOUR_ORDERS_AUDIT_PENDING',
                  'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
                  'new_source_or_audit_processes': 0}))
