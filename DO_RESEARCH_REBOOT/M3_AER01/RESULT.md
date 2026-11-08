# AER01 — Corrected full-source one-gap theorem

Status: **PROVED—RESTRICTED DOMAIN**, every original low/high leg in
mu341, sigma=(1,0,...,0), chi8. This corrected construction supersedes
ACL01's full-source potential, whose two failed inequalities are recorded
in ACL-AUD02. The old ACL01 files are preserved as superseded research.

## Source correction

An original present A slot may have kind0 child reference r>=127.
The actual child-bound constraints check real c in0..126 only; the
8-bit child field allows127..255. Such a pair references NO present
node and is NOT an active inventory port. The original alpha reader
nevertheless treats its kind as real and defaults its lookups to slot0.
The earlier proof wrongly identified all kind0 observations with real
nodes. Full original roots show the distinction is necessary.

Define E on the actual A pointer structure: replace any kind0/r>=127
child pair by an empty pair. Keep every real node and active port.
After E the present nodes and remaining real child links form the
proper ordered prefix used by the old completion proof. The source
parent/depth/link/bound constraints ensure this: every real child points
to a present node with the stated parent/side and increasing depth;
every present nonroot has that real parent; real ranks are distinct.
No real child can be slot0, which would contradict the fixed root
parent/bounds. The only unaccounted kind0 pairs were the out-of-range
ones, now erased. All S claims and population bills remain unchanged.

## Active paths and commuting erasure

Every active target is a present real slot. Starting there, the original
parent lookup follows the unique real present-node chain to the current
root: an out-of-range child reference cannot equal a real slot index.
Absent AState slots have only kind2 children. An attempted extra step
beyond the current root could enter NULL_REF127 and possibly follow a
spurious dangling claimant. But reaching the required final current
root again would repeat that root, forbidden by the original no-repeat
constraint. Therefore every verified active operand is a real present
node; there is no invalid reference on an active path. This argument
holds initially and after each valid rotation by induction.

The original single_rot rewrites only real path operands and carries
each side (kind,ref) pair as a unit. For real x,p,gp, erasing a side
pair before or after the rewrite gives the same real tree and ports.
The term identities p(x(A,B),C)<->x(A,p(B,C)) are unchanged when an
erased side block is empty. This proves

    E(rot(st)) = rot(E(st))

for every active primitive, both orientations and root cases, including
arbitrarily many simultaneous invalid pairs. Induct over active
primitives and all macro events. Every access depth, H, terminal marked
key, actual terminal B depth and q remain identical. B is unchanged by
this A-side erasure. The prior free-field A rewrite identity applies
to all side pairs; additional checks cover all129 invalid refs, all
three side blocks, both orientations and root flags (3096 cases).

## Shared-state recognition without access to private references

Complete E(st) using the fixed logical universe U=(-1,0,...,8), with
the unique gap0 key and the port-interval construction in ACL01 C1-C2.
Its inventory proof now applies to an actual proper prefix. No erased
branch has a node or active port to hold a key. Exact S-cover and the
unique gap0 population imply that branch's U interval is EMPTY. This
also remains true at the destination because erasure commutes with
the full macro, yielding a complete physical U tree with that empty
branch. At observed depth1/2, the interval is determined by observed
real ancestors alone; no private bounds or inventory become coordinates.

Define rho*(alpha) recursively. At any observed nonroot position whose
logical U interval is empty, return EMPTY and IGNORE its raw alpha entry
and, at depth1, both reported grandchildren. Otherwise use the old proper
prefix rule: real logical key, canonical filling of a port, or rejection
of an inconsistent pattern. Root ak remains normalized as before. For
every actual original low source/destination this produces exactly the
physical alpha of completed E(st). Misleading lookups through an invalid
reference only occur below an erased EMPTY interval, so they are all
ignored. No assumption about their copied slot0 label is needed.

The construction handles any number of invalid pairs, combined with
arbitrary multi-S/empty ports, all irrelevant alpha fields and B padding.
It preserves every constrained real key and all active paths. Physical
canonical depth-six cuts still stay below the observed depth-two region
after at most2H<=4 rotations, as in ACL01. Hence the exact H1/normalized
Gamma1-H2 physical edges and Gamma0 debt proof remain available.

## Corrected potential and signed theorem

For marked synchronized roots with proper corrected image and B core,
set Q*(s)=J_H1F01(core B, rho*(alpha)). For unmarked/unsynchronized roots
or non-low-realizable patterns use zero. Put Q*(midpoint)=0. Its range
is[-2,0]. Every original genuine low destination is marked/synchronized
and now ALWAYS receives its valid physical table value <=-psi(core B).

The complete low cases are the same established source reductions:
H1 with marked source pulls back to a verified physical edge; an
unmarked source has Q*=0 and uses Q*(t)<=0 for q<=2 or the debt floor
Q*(t)<=2-q for q3/4. H2 with Gamma0 uses range for q<=2 and the
destination floor plus source>=-2 for q3/4. Gamma1 pulls back to the
two-access physical edge (-1,x). Gamma>1 and genuine H0 are impossible
by the established charge/change injection. This is not a new source
constraint. Thus Q*(t)-Q*(s)<=w_L=2H-q for EVERY original low edge.

All original chi8 high legs use w_H>=2 and midpoint correction0, so
w_H+Q*(source)>=0 and -Q*(destination)>=0 independently of whether
their alpha is realizable by a low witness. The original high h=0
correction and all high witness freedoms remain intact.

Therefore for ANY walk within this fixed original sector,

    sum w >= Q*(end)-Q*(start) >= -2.

For a closed walk the first right side is zero. Closure and high
midpoints are the full frozen shared states, including B lo/hi and
all raw alpha fields. No endpoints are identified by their images.
Every closed mixed walk in this corrected sector is nonnegative.

## Executed evidence and exit

repair_certificate.json: all8534 proper patterns retain their image;
293760 local empty-interval junk patterns checked;302294 total finite
queries. All481562 previously registered values unchanged. All70 TRUE
original mutant edges satisfy the new inequality, minimum residual0;
both old failed inequalities repaired. No new fit. CPU21.906s.

primitive_erasure.json:3096 original primitive cases,129 invalid refs,
509 fields each; both orientations/root flags/three side blocks.
CPU12.656s. Arbitrary simultaneous pairs follow from the compositional
source proof, not an unexecuted Cartesian enumeration.

original_replay.json: independent complete original roots TRUE for the
two old failure refs127/255 plus128. Old residual-1; corrected residual1.
Original DAG1400081 nodes, CPU13.812s. All caps respected.

BEFORE: old full-source promotion withdrawn by ACL-AUD02. RESULT:
explicit corrected source-complete construction. AFTER: full-sector
theorem restored with Q*, no source/backend/state change. R1-R4 PASS:
one necessary boundary repair, direct erasure proof, bounded exact audit,
and the mandatory original bridge actually closed. No new assumptions.
NET ADVANCEMENT relative to the PREVIOUS ANSWER: correction of its gap;
relative to the audited valid proof bank: full fixed sector restored.
SIG02's allocation obstruction remains independently valid. All other
masks/signatures, outside-chi8 M3, Stage03 and Dynamic Optimality OPEN.
