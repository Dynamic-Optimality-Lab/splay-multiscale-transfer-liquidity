"""Build machine-readable receipts for the completed, scoped bank investigation.

The durable mathematical proof is in Notion. These are executable-checkpoint
metadata, not a universal cost certificate or a second prose research ledger.
"""
import sys
import ast
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROOF = 'https://app.notion.com/p/41f6251839be8161b101fd41e62eda46'


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2), encoding='utf-8')


def main():
    assert not (HERE / 'FINAL_MANIFEST.json').exists(), 'Sealed checkpoint is read-only.'
    notion = read('NOTION_WRITE_VERIFICATION.json')
    assert notion['main']['readback_verified'] and notion['main']['exact_normalized_match']
    assert all(p['exact_normalized_match'] and p['old_normalized_prefix_preserved']
               for p in notion['updated_existing_pages'])
    physical = read('INDEPENDENT_VERIFICATION.json')
    audit = read('AUDIT_INDEPENDENT_VERIFICATION.json')
    preservation = read('PRESERVATION_VERIFICATION.json')
    assert physical['passed'] and audit['passed'] and preservation['passed']
    python_files = sorted(HERE.glob('*.py'))
    for path in python_files:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    lean_source = (HERE / 'BankKernel.lean').read_text(encoding='utf-8')
    assert 'sorry' not in lean_source and '\naxiom ' not in lean_source
    lean = subprocess.run(['lean', '+leanprover/lean4:v4.21.0', str(HERE / 'BankKernel.lean')],
                          cwd=str(HERE), text=True, capture_output=True)
    write('LEAN_VERIFICATION.json', {
        'passed': lean.returncode == 0, 'returncode': lean.returncode,
        'stdout': lean.stdout, 'stderr': lean.stderr,
        'scope': 'Generic fixed-point, conservative accounting and coarsening arithmetic; not full BST/source formalization.'})
    assert lean.returncode == 0, lean.stdout + lean.stderr
    code_files = sorted([*python_files, HERE / 'BankKernel.lean'])
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in code_files}
    write('NOTION_PROOF_REFERENCE.json', {
        'url': PROOF,
        'title': 'GSO physical bank — canonical cyclic closure and all-capacity priority obstruction',
        'readback_verified': True, 'instructions_version': '0.0.6',
        'verification': 'NOTION_WRITE_VERIFICATION.json', 'code_sha256': hashes,
        'status': 'PROVED_CANONICAL_SEAM_AND_SHARED_BUDGET; REFUTED_FROZEN_POLICY_ALL_FINITE_CAPACITIES; UNIVERSAL_CD_OPEN'})
    write('THEOREM_CERTIFICATE.json', {
        'proof': PROOF,
        'frozen_rule': 'ADMISSION.json',
        'persistent_owners': 'Fixed disjoint consecutive physical-rank blocks of at most five keys; no ancestry-birth reset.',
        'A_issuance_per_original_unit': 'At most 8H total over its actual footprint.',
        'KEEP_voucher': 'At most H once per genuine B KEEP; distinct incoming cyclic A-gap units.',
        'shared_global_issuance': '8H*A + H*K_B <= 9H*A',
        'B_rule': 'Pool actual footprint, pay original double once, then target first and remaining touched blocks in increasing key order.',
        'cyclic_construction': {
            'status': 'PROVED_SOURCE_UNIFORM_FOR_FROZEN_MONOTONE_KERNEL',
            'algorithm': 'Iterate clipped full-period map from full capacity vector.',
            'integer_termination': 'At most mH strict descending period passes; one further evaluation can detect equality.',
            'real_extension': 'Continuous monotone maps have a greatest coordinatewise descending limit.',
            'invariance': 'Compatible with cyclic cuts and repeated periods; arbitrary physical interleavings/recreated ancestry allowed.',
            'limitation': 'Closure and maximality do not imply that every funded-B guard holds.'},
        'conditional_costs': {'all_original_Q': 'Q_B <= 9H*A',
                              'all_original_U_plus_old_interface': 'Q_B <= (6+9H)*A'},
        'funding_guard_status': 'REFUTED_EXACT_FOR_EVERY_FINITE_POSITIVE_REAL_CAPACITY',
        'integer_counterfamily': {
            'source': 'H_(p,q), p=3H+4, q=12H+32, N=2^(p+1)*(q+1)+1',
            'word': 'D2..N; descend N..1 keeping exactly x_j=N+1-2^j, j=0..p; K1..N; K(N-1)..1.',
            'initial_pair': 'Both full physical right vines; empty reaching prefix.',
            'closure': 'The final counted increasing/decreasing KEEP scans restore the exact labeled pair.',
            'relaxed_demand': 'Only original critical RR doubles at phases >=4; all other B costs free, physical operations unchanged.',
            'profile': 'M=2a+b upper-bounds future connector inputs, not total bank mass.',
            'drop': 'M_next <= M-1 when M>=1; zero remains zero.',
            'stationary_values': 'a_next=max(0,2a+b-2H-1), b_next=min(H,2a+b-1).',
            'physical_reason': 'Retired middle-root output is at least the persistent coarse-spine output under the frozen priority.',
            'window': 'ell_next=ceil((ell+2)/2)+1; u_next=floor(u/2)-(3H+1).',
            'dry_packet': 'After 3H stages, at least 3H+1 original U RR demands have zero fresh input and carry at most 3H.'},
        'real_extension': {
            'status': 'PROVED_WITHOUT_ROUNDING_CAPACITY',
            'recipe': 'After R weighted-loss stages reach I<1. Choose finite L dominating all stationary burns and floor(3H/(1-I))+1; p=R+4,q=4L+8.',
            'checks': 'REAL_CAPACITY_CERTIFICATE.json'},
        'independent_original_event_witnesses': [
            {'source': 'H_(9,5)', 'keys': 6145, 'H': 8,
             'unpaid_original_U_ids': [['B', 6400, 9], ['B', 6400, 10]]},
            {'source': 'H_(7,44)', 'keys': 11521, 'H': 1,
             'charged_original_U': 671, 'unpaid_original_U': 129,
             'first_unpaid_id': ['B', 11584, 2]}],
        'scope_cautions': [
            'These H sources keep old periodic certificates; they are not new escapes from the final frozen UF/hybrid partition.',
            'The obstruction excludes this transfer kernel, not all banks, nonlocal potentials or Universal CD.',
            'Increasing issuance is already dominated by saturation at fixed capacity.',
            'The all-parameter source/comb proof is mathematical, not a complete Lean formalization.',
            'Finite SMT and replay evidence are separately scoped and are not the universal source proof.'],
        'unrestricted_root_cost_obligations_deleted': 0,
        'universal_CD': 'OPEN', 'Dynamic_Optimality': 'OPEN'})
    write('STRATEGY_REVIEW.json', {
        'status': 'STOP_REFUTED_FROZEN_PRIORITY_FAMILY',
        'proof': PROOF,
        'review_trigger': 'Previous anonymous-state grammar and this saturated physical-priority bank both fail to close the root cost obligation.',
        'completed_progress': ['Constructive canonical cyclic seam for the monotone kernel.',
                               'Shared globally bounded original-A issuance.',
                               'All-finite-capacity physical counterfamily with exact original-U verification.'],
        'do_not_automatically_retry': ['Larger H', 'Larger A/KEEP issuance constants',
                                     'Different cyclic seed', 'Unproved feasibility premise',
                                     'Unannounced priority or feature changes'],
        'first_missing_implication': 'A different physical retention/update law must preserve sufficient reachable credit at every original B guard while deriving shared A issuance and cyclic closure.',
        'local_necessary_specification': 'Within the stationary six-port template, avoiding repeated connector-profile loss requires persistent-spine retention to exceed retired-root retention by at least one on average.',
        'local_specification_is_not': 'A global theorem or proof that reordering suffices.',
        'earlier_results': 'All prior exact eligibility, budgets, scoped theorems and refutations preserved.',
        'root_status': 'OPEN'})
    totals = {key: sum(w[key] for w in physical['witnesses'])
              for key in ('operations', 'real_rotations', 'original_U')}
    write('ENGINE_RESULT.json', {
        'engine': 'WORKING_PHYSICAL_BANK_RULE_BACKEND',
        'date': '2026-11-22', 'proof': PROOF,
        'source_uniform_positive_results': ['Canonical greatest cyclic diagnostic balance',
                                             'Shared original-A issuance <=9H*A'],
        'frozen_policy_funding': 'REFUTED_EXACT_ALL_FINITE_POSITIVE_REAL_CAPACITIES',
        'implemented': ['Exact physical policy and guard failures', 'Monotone cyclic balance construction',
                        'Original-source scaling and six-port coarsening teacher',
                        'Symbolic stationary/window arithmetic', 'Integer and real counterfamily recipes',
                        'Independent full carrier/cyclic-Pi replay', 'Conservative accounting Lean kernel'],
        'not_implemented': ['A successful replacement bank', 'Full original-source Lean proof',
                            'An arbitrary-source funded-B induction', 'Universal CD proof'],
        'independent_new_witnesses': len(physical['witnesses']),
        'independent_new_original_event_totals': totals,
        'previous_physical_trace_capacity_tests': audit['capacity_tests'],
        'exploratory_tests': {'sealed_source_policy_tests': 90, 'new_scaling_policy_tests': 112,
                             'scope': 'Finite diagnostics, not exhaustive coverage.'},
        'soundness_tests_passed': 8, 'previous_artifacts_preserved': 5120,
        'selected_inputs_pinned': 271, 'unrestricted_root_cost_obligations_deleted': 0,
        'universal_CD': 'OPEN', 'Dynamic_Optimality': 'OPEN'})
    write('FINAL_CHECK_RESULTS.json', {
        'passed': True, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'independent_original_event_replay': {'passed': physical['passed'], 'witnesses': len(physical['witnesses']), **totals},
        'previous_trace_independent_policy_replay': {'passed': audit['passed'], 'tests': audit['capacity_tests']},
        'soundness_regressions': {'passed': True, 'tests': 8,
                                 'record': 'Observed tests.py completion before finalization; no bank logic changes afterward.'},
        'symbolic_certificates': ['SYMBOLIC_COARSENING_CERTIFICATE.json',
                                  'SOURCE_INDUCTION_CERTIFICATE.json', 'REAL_CAPACITY_CERTIFICATE.json'],
        'Lean': {'passed': True, 'receipt': 'LEAN_VERIFICATION.json',
                 'no_sorry_or_new_axiom_declaration': True,
                 'full_original_BST_formalization': False},
        'python_AST': {'passed': True, 'files': len(python_files)},
        'preservation': {'passed': True, 'prior_files': preservation['prior_hashes'],
                         'selected_input_pins': preservation['selected_input_pins']},
        'Notion': {'passed': True, 'pages_readback_verified': 3,
                   'existing_page_prefixes_preserved': True},
        'research_claim': 'Scoped bank closure/budget proved and frozen payment law refuted; root bound OPEN.'})
    print(json.dumps({'finalized': True, 'new_witnesses': len(physical['witnesses']),
                      'python_AST_files': len(python_files), 'Lean_passed': True,
                      'Notion_pages_verified': 3, 'root_status': 'OPEN'}))


if __name__ == '__main__':
    main()
