# GAPINT02 — All populations in gaps 2 and 7

Status: **PROVED—RESTRICTED DOMAIN**. For every original legal five-bit
mu and sigma=n e2 or n e7, 0<=n<=266, every original chi8 leg
satisfies w>=Q(destination)-Q(source), with -2<=Q<=0 and Q(midpoint)=0.
Every fully closed mixed walk in these sectors has nonnegative weight.
No multi-gap or outside-chi8 theorem is asserted.

## Complete source reduction

Apply the fixed-interior-gap proof in ../M3_GAPINT01/RESULT.md with
g=2. Per-gap conservation fixes the gap of each exposed anonymous
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

Reflect mathematical low profiles/core trees by i->8-i for gap7.
This does not reflect the original high sentinel or private LE tests.
Every fixed debt value is checked under reflection, with zero mismatches.
Original high OM toll>=2 and zero MO weight use the same midpoint and
the range [-2,0]. The high h=0 correction is unchanged. Full raw shared
states, including B intervals, must close in every cycle claim.

## Exact construction and audits

The source grammar gives 77570 models, 181888
source cases, and 1317 profile classes. The proof supergraph
has 587493 states and 3957645 materialized relevant edges.
Analytic omissions are 892469 range-safe rows and debt-safe
rows {'0': 250777, '1': 668519}: w1 with psi(dest)>=1, w0 with psi(dest)=2.
Both follow directly from range and the destination floor; cases are
not discarded or stored in a hidden graph.

The exact recurrence starts at -psi and completes with 35816
decreases and 4055618 edge scans. Histogram: {'0': 458728, '-1': 107839, '-2': 20926}.
The independent audit regenerates 225646 source
cases and all 3957645 edges. Minimum residual 0; every residual
is nonnegative; destination floor holds. Potential SHA256:
d09c329356075a100faf8851bb0bbe38e79e6d80bea94114e189b6c1465cb2bb.

Build 8.844 CPU seconds; completion 0.828;
independent audit 9.719; original audit 41.016.
All phase caps are preserved. Certified entry points: build_v2.py and
complete_v3.py, verify_v3.py, potential_v3.py, original_audit_v3.py.

The earlier generated non-v3 entry files are preserved but are not the certified entry points: they prepend the common directory and could resolve its table. The v3 wrappers append that directory, import this campaign's table, and were used for all three audits.

The original audit passes 12 full roots and independent
replays: populations 0,1,2,3,4,266; both gaps; anonymous forks; negative
H1 edges; the unmarked-core H2 macro; and source-legal wrong-side
boundary-touching payloads. A mixed cycle at mu=79, n=3,
gap=2 has weight 8, full original closure and the same high midpoint.
Original DAG sizes: 1400081 low and 53455 high. These controls validate
source alignment; the structural reduction supplies universal coverage.

BEFORE: these two single-gap families remained open. RESULT: complete
source/profile reduction plus independently verified exact certificate.
AFTER: every mask and population in these two original families is
covered. NET ORIGINAL ADVANCEMENT: these signature obligations deleted;
no new assumptions. R1–R4, source q and signed weights, depth2/T266,
exact Int architecture and Bank25=25 preserved. Multi-gap M3, mixed
cycles outside chi8, Stage03 and Dynamic Optimality remain OPEN.
