"""Record the completed single-gap certificates and the stopped multi-gap bridge.

Read-only checks precede report creation. Existing research is never overwritten.
Run from the repository root with Python -B.
"""
import hashlib
import sys
from array import array
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / 'DO_RESEARCH_REBOOT'
BASE = RESEARCH / 'M3_GAP01'
FOLDERS = ['M3_GAP01'] + [f'M3_GAPINT0{g}' for g in range(1, 5)]
NEW_FOLDERS = FOLDERS + ['M3_CHIB01', 'M3_CHIB02', 'M3_GAPMULTI01']


def raw(p):
    return Path('\\\\?\\' + str(p.resolve())).read_bytes()


def digest(p):
    return hashlib.sha256(raw(p)).hexdigest()


def read(p):
    return json.loads(raw(p))


def git(*args):
    return subprocess.check_output(['git', *args]).decode().strip()


def write_new(p, text):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        f.write(text)


def verify_debt_floor(folder, c):
    # GAP01's older result schema omits a separate floor Boolean, although
    # its independent verifier checks the floor at every node. Recheck the
    # actual values here for every campaign, without relying on that field.
    labels = array('i'); labels.frombytes(raw(folder / 'potential.bin'))
    bids = array('H'); bids.frombytes(raw(folder / 'ordinary_b.bin'))
    if c['byteorder'] != sys.byteorder:
        labels.byteswap(); bids.byteswap()
    assert len(labels) == len(bids) == c['nodes']
    return all(-2 <= v <= -c['psi'][b] <= 0 for v, b in zip(labels, bids))


def main():
    baseline = read(BASE / 'entry_baseline.json')
    assert len(baseline) == 264
    for row in baseline:
        assert digest(ROOT / row['path']) == row['sha256'], row['path']
    assert not git('status', '--porcelain', '--untracked-files=no')
    assert git('branch', '--show-current') == 'coarse-double-branch'
    assert git('rev-parse', 'HEAD') == 'fea2a25b05e97f726b6e1891cebb12c4cfca821a'

    rows = []
    for name in FOLDERS:
        folder = RESEARCH / name
        c = read(folder / 'catalog.json')
        p = read(folder / 'completion.json')
        a = read(folder / 'edge_audit.json')
        o = read(folder / 'original_audit.json')
        assert a['status'] == 'FINITE_EXACT_VERIFIED', (name, a['status'])
        assert o['status'] == 'PASS'
        assert c['nodes'] == p['nodes'] == a['states']
        assert c['edges'] == p['edges'] == a['edges_independently_regenerated']
        assert c['nodes'] < 2000000 and c['edges'] <= 5000000
        assert p['range'] == a['range'] == [-2, 0]
        assert a['minimum_residual'] == 0 and verify_debt_floor(folder, c)
        assert digest(folder / 'potential.bin') == a['potential_sha256']
        assert len(raw(folder / 'potential.bin')) == 4 * c['nodes']
        assert all(v < 120 for v in [c['cpu_seconds'], a['cpu_seconds']])
        assert p['cpu_seconds'] < 300 and o['cpu_seconds'] < 300
        assert o['DAG_nodes'] == [1400081, 53455]
        cycle = o['closed_mixed_cycle']
        assert cycle['full_state_closure'] and cycle['same_midpoint']
        assert cycle['weight'] == 8
        row = {
            'campaign': name,
            'gaps': [0] if name == 'M3_GAP01' else o['gaps'],
            'models': a.get('models', a.get('seed_models')),
            'states': c['nodes'], 'edges': c['edges'],
            'source_cases_independent': a['source_case_queries'],
            'build_cpu': c['cpu_seconds'], 'completion_cpu': p['cpu_seconds'],
            'independent_audit_cpu': a['cpu_seconds'],
            'original_audit_cpu': o['cpu_seconds'],
            'original_roots': o.get('original_roots', o.get('complete_original_roots')),
            'potential_sha256': a['potential_sha256'],
            'histogram': p['histogram'],
        }
        rows.append(row)
        if name in ['M3_GAPINT02', 'M3_GAPINT03', 'M3_GAPINT04']:
            g = c['gap']
            entries = ('complete_v3.py, verify_v3.py, potential_v3.py, original_audit_v3.py'
                       if g == 2 else 'complete.py, verify.py, potential.py, original_audit.py')
            extra = ("The earlier generated non-v3 entry files are preserved but are not the "
                     "certified entry points: they prepend the common directory and could "
                     "resolve its table. The v3 wrappers append that directory, import "
                     "this campaign's table, and were used for all three audits.\n\n"
                     if g == 2 else '')
            text = f'''# GAPINT0{g} — All populations in gaps {g} and {9-g}

Status: **PROVED—RESTRICTED DOMAIN**. For every original legal five-bit
mu and sigma=n e{g} or n e{9-g}, 0<=n<=266, every original chi8 leg
satisfies w>=Q(destination)-Q(source), with -2<=Q<=0 and Q(midpoint)=0.
Every fully closed mixed walk in these sectors has nonnegative weight.
No multi-gap or outside-chi8 theorem is asserted.

## Complete source reduction

Apply the fixed-interior-gap proof in ../M3_GAPINT01/RESULT.md with
g={g}. Per-gap conservation fixes the gap of each exposed anonymous
node; ancestor order determines each port's hidden S set. Anonymous
port populations remain opaque and their literal locations are not
inferred from weak LE compatibility. Collapse S-empty subtrees, including
AER01 dangling artifacts, to PORT; balance S-containing hidden blocks.
This is a shared-state potential image, not a new graph coordinate.

The complete depth1/2 H1 orientation classification retains at most
three core-bearing anonymous nodes across the active path and both
endpoint shadows. The ordered-tree grammar enumerates all nine S keys
and 0..3 such nodes, including forks. Replace whole unobserved side
blocks, preserving their S sets; no unseen fork's lower branch is lost.
The proof is independent of the remaining opaque population, so it
covers every n, not merely the audited numerical controls.

Because gap0 is absent, all H2 have Gamma_pre=0. Use the actual terminal
B-core debt floor psi(destination)>=q-2 when q=3/4. With Q(source)>=-2
and Q(destination)<=-psi, Delta Q<=4-q. Range covers q<=2. Changing
unmarked core KEEP events and whole DELETE/KEEP macros remain allowed.

Reflect mathematical low profiles/core trees by i->8-i for gap{9-g}.
This does not reflect the original high sentinel or private LE tests.
Every fixed debt value is checked under reflection, with zero mismatches.
Original high OM toll>=2 and zero MO weight use the same midpoint and
the range [-2,0]. The high h=0 correction is unchanged. Full raw shared
states, including B intervals, must close in every cycle claim.

## Exact construction and audits

The source grammar gives {c['models']} models, {c['source_case_queries']}
source cases, and {len(c['shadows'])} profile classes. The proof supergraph
has {c['nodes']} states and {c['edges']} materialized relevant edges.
Analytic omissions are {c['range_safe']} range-safe rows and debt-safe
rows {c['debt_safe']}: w1 with psi(dest)>=1, w0 with psi(dest)=2.
Both follow directly from range and the destination floor; cases are
not discarded or stored in a hidden graph.

The exact recurrence starts at -psi and completes with {p['updates']}
decreases and {p['edge_scans']} edge scans. Histogram: {p['histogram']}.
The independent audit regenerates {a['source_case_queries']} source
cases and all {c['edges']} edges. Minimum residual 0; every residual
is nonnegative; destination floor holds. Potential SHA256:
{a['potential_sha256']}.

Build {c['cpu_seconds']} CPU seconds; completion {p['cpu_seconds']};
independent audit {a['cpu_seconds']}; original audit {o['cpu_seconds']}.
All phase caps are preserved. Certified entry points: build_v2.py and
{entries}.

{extra}The original audit passes {o['original_roots']} full roots and independent
replays: populations 0,1,2,3,4,266; both gaps; anonymous forks; negative
H1 edges; the unmarked-core H2 macro; and source-legal wrong-side
boundary-touching payloads. A mixed cycle at mu={cycle['mu']}, n=3,
gap={g} has weight 8, full original closure and the same high midpoint.
Original DAG sizes: 1400081 low and 53455 high. These controls validate
source alignment; the structural reduction supplies universal coverage.

BEFORE: these two single-gap families remained open. RESULT: complete
source/profile reduction plus independently verified exact certificate.
AFTER: every mask and population in these two original families is
covered. NET ORIGINAL ADVANCEMENT: these signature obligations deleted;
no new assumptions. R1–R4, source q and signed weights, depth2/T266,
exact Int architecture and Bank25=25 preserved. Multi-gap M3, mixed
cycles outside chi8, Stage03 and Dynamic Optimality remain OPEN.
'''
            write_new(folder / 'RESULT.md', text)

    obstruction = read(RESEARCH / 'M3_GAPMULTI01/obstruction.json')
    assert obstruction['status'] == 'REFUTED_EXACT_SHARED_PORT_CORE_SPLIT_DETERMINACY'
    assert obstruction['same_full_source_state'] and obstruction['same_full_destination_state']
    assert obstruction['hidden_core_bills'] == [[[], [0, 1]], [[0], [1]]]
    assert obstruction['complete_original_roots'] == obstruction['independent_replays'] == 2
    assert not obstruction['counterexample_to_M3']
    assert not obstruction['negative_original_cycle_certified']
    write_new(RESEARCH / 'M3_GAPMULTI01/RESULT.md', '''# GAPMULTI01 — Exact failure of literal shared hidden-core splitting

Status: **REFUTED—EXACT** for the proposed deterministic literal port
completion bridge. M3 on multiple positive gaps remains **OPEN**.

At mu=341, sigma=(1,1,0,...,0), two full original LOW witnesses have
identical complete source states and identical complete destination
states. Both execute terminal KEEP6 with H=1, actual q=2 and weight 0.
Both original roots are TRUE and independently replayed. Original low
DAG: 1400081 nodes; audit CPU 12.016 seconds.

At the shared source, root S2 has a visible anonymous left child f,
whose two children are opaque ports. The same right core subtree and
the same B state are used in both witnesses. In witness0, f is in gap0;
its left port contains no S key, its right port contains S0 and S1.
The gap1 unit is hidden there. In witness1, f is in gap1; its left port
contains S0 and the hidden gap0 unit, and its right port contains S1.
All original mu, sigma, alpha, B child refs/kinds and lo/hi agree.

Thus the hidden S bills are respectively ([],[0,1]) and ([0],[1]).
The fixed-gap0 and fixed-gap1 literal completion images differ, although
the full shared state cannot distinguish the witnesses. This disproves
the first required identity for directly extending the fixed-gap
completion mechanism. It does not disprove an allocation-invariant or
branch-robust potential, and two copies of the same weight0 edge do not
give a negative cycle.

BEFORE: a multi-gap extension needed deterministic hidden-S port sets.
RESULT: exact original equal-state witness pair refutes that premise.
AFTER: stop this completion route as required by PRE_EXECUTION.md.
NET ORIGINAL THEOREM ADVANCEMENT: 0 from this obstruction; strategic
elimination only. The separately proved single-gap families survive.
No additional coordinate, private observable or graph modification is
authorized or introduced. No original negative mixed cycle is certified.
R1–R4 and the high h=0 correction are preserved. A fresh multi-gap
mechanism needs its own four-rule gate; an unknown completion existence
premise cannot be treated as a proof.
''')

    table = '\n'.join(
        f"| {','.join(map(str, r['gaps']))} | {r['states']:,} | {r['edges']:,} | {r['original_roots']} |"
        for r in rows)
    total_edges = sum(r['edges'] for r in rows)
    total_roots = sum(r['original_roots'] for r in rows)
    write_new(BASE / 'CURRENT_STATUS.md', f'''# M3 — Current proved scope after the remaining single-gap campaigns

**PROVED—RESTRICTED DOMAIN:** every legal mask mu, inside chi8, with
sigma=0 or sigma=n e_g for 0<=g<=8 and 1<=n<=266. This is 2395 distinct
signature vectors and 301770 mask/signature sectors. Multiple positive
gap components remain OPEN. This supersedes the narrower scope in
../M3_ACL_AUD02/CURRENT_STATUS.md without changing that historical file.

## Original signed theorem

There is an explicitly tabulated shared-state Q in [-2,0], with the
original midpoint assigned 0, such that every original leg in these
sectors obeys

    w(u,v) >= Q(v)-Q(u).

Consequently every finite original walk has sum w>=Q(end)-Q(start)>=-2,
and every fully closed original mixed walk has sum w>=0. Closure includes
all raw mu/sigma/alpha/B fields and the shared high midpoint.

The dispatch is static: use GAP01 for zero support or gap0; GAPINT01 for
gaps1/8; GAPINT02 for gaps2/7; GAPINT03 for gaps3/6; GAPINT04 for gaps4/5.
Mu and sigma are preserved on every leg, so there is no cross-sector
compatibility assumption. Each component supplies all masks and all
allowed populations. Gap9 cannot be present at a valid chi8 low boundary:
its maximum-rank gap leaf must be attached at core8.right, which chi8
fixes to the N19 sentinel. Pure high walks are already covered by M2.

The proof retains opaque anonymous populations, completes only hidden
S structure using the fixed gap, erases source-legal dangling artifacts,
and gives a complete at-most-three-node profile reduction. All H1 rows
are classified; H2 Gamma0 uses the ACTUAL terminal debt floor. GAP01 also
covers cheap Gamma1 fringe macros. High legs use the original chi8 toll
and preserve the h=0 correction. See each campaign's RESULT.md for the
source proof and exact provenance.

| Positive gap | Finite states | Independently verified edges | Original roots |
|---|---:|---:|---:|
{table}

Across separate bounded phases: {total_edges:,} relevant edges and
{total_roots} complete original roots independently replayed. Each
graph stays below the frozen live state/edge caps. Large population266
is kept in original source ports, rather than inferred from a finite
small-tree enumeration. Universal scope comes from the structural
reduction; source roots are alignment controls. All tables have exact
integer residuals >=0 and destination debt floors.

## Exact frontier and stopped mechanisms

Multi-gap support is unresolved. GAPMULTI01 gives two original witnesses
at sigma=(1,1,0,...,0) with identical source AND destination but different
hidden S splits across anonymous ports. This refutes the literal
fixed-gap completion extension. It does not refute M3 or every shared
potential. The registered route stops at this obstruction; it is not
replaced by an assumed allocation-invariance theorem.

CHIB01 refutes a range-two B-only path bound. CHIB02 gives a negative
cycle in the relaxed B-only graph (weight -2, mu341); its registered
full-alpha lift fails, and its first three A accesses have a source-order
obstruction. It is not an original negative mixed cycle. The required
two-pivot strategy review stops the B-only route.

Still OPEN: multiple positive gaps inside chi8; mixed cycles outside
chi8; full M3/Stage03 and Dynamic Optimality. No certified original
negative mixed cycle was found. The successful single-gap theorems
delete original obligations; the failed mechanisms provide strategic
elimination only. R1–R4, frozen architecture/source, source q and signed
weights, depth2/T266 and Bank25=25 remain unchanged. Stage04 is not run.

Integrity and hashes are recorded in final_manifest.json. All 264
pre-existing untracked research files are checked against the entry
baseline; tracked source and Git branch/HEAD are checked unchanged.
''')

    # Repeat preservation checks after reports, then inventory every fresh artifact.
    for row in baseline:
        assert digest(ROOT / row['path']) == row['sha256'], row['path']
    assert not git('status', '--porcelain', '--untracked-files=no')
    baseline_names = {r['path'] for r in baseline}
    fresh_prefixes = tuple('DO_RESEARCH_REBOOT/' + n + '/' for n in NEW_FOLDERS)
    untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0')
    unexpected = [p for p in untracked if p and p not in baseline_names and not p.startswith(fresh_prefixes)]
    assert not unexpected, unexpected
    files = []
    for name in NEW_FOLDERS:
        for p in sorted((RESEARCH / name).rglob('*')):
            if p.is_file():
                files.append({'path': p.relative_to(ROOT).as_posix(), 'bytes': len(raw(p)), 'sha256': digest(p)})
    dependencies = []
    for d in ['DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
              'DIRECT_CDK5N_11F_STRICT_CLOSURE',
              'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']:
        for p in sorted((RESEARCH / '06_CERTIFICATES' / d).glob('*.py')):
            dependencies.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': digest(p)})
    for name in ['M3_LDR01/negative_run_census.json', 'M3_H1F01/cheap_census.json',
                 'M3_H2R01/fringe_kernel_certificate.json', 'M3_H2R01/terminal_potential.py']:
        p = RESEARCH / name
        dependencies.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': digest(p)})
    manifest = {
        'status': 'PASS_RESTRICTED_SINGLE_GAP_CERTIFICATES',
        'date_local': '2026-10-29 Asia/Karachi',
        'branch': git('branch', '--show-current'), 'HEAD': git('rev-parse', 'HEAD'),
        'tracked_source_unchanged': True, 'old_research_files_unchanged': len(baseline),
        'all_new_files_in_registered_research_folders': True,
        'source_dependencies': dependencies, 'campaigns': rows,
        'proved_signature_vectors': 2395, 'proved_mask_signature_sectors': 301770,
        'separate_phase_edges_total': total_edges, 'complete_original_roots': total_roots,
        'multi_gap_status': 'OPEN', 'outside_chi8_status': 'OPEN',
        'original_negative_cycle_certified': False,
        'multi_gap_literal_split_bridge': obstruction['status'],
        'resource_stop_preserved': 'GAPINT01 v1 stopped at 5m edges; v2 analytic row discharge under same caps',
        'architecture_and_R1_R4_preserved': True, 'high_h0_correction_preserved': True,
        'Bank25': 25, 'Stage04_run': False,
        'files_excluding_this_manifest': files,
    }
    write_new(BASE / 'final_manifest.json', json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in manifest.items() if k not in ['files_excluding_this_manifest', 'source_dependencies', 'campaigns']}, indent=2))


if __name__ == '__main__':
    main()
