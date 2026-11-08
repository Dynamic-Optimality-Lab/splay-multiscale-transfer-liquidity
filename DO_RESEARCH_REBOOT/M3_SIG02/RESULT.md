# M3-SIG02 — Exact obstruction to the literal completion extension

Status: **REFUTED—EXACT for literal port-inventory determinacy.**
Roadmap step #3 (all-mask/all-signature chi8 closure): **OPEN**.
M3, Stage03 and Dynamic Optimality: **OPEN**.

## Before / result / after

BEFORE: ACL01 proves every original low/high edge inequality in the
fixed sector mu=341, sigma=(1,0,...,0), chi8. The proposed successor
would extend its literal port-completion mechanism to other signatures.

RESULT: its first mandatory sublemma fails already at sigma=(2,0,...,0)
with the SAME mu=341. Two complete original low witnesses have identical
full shared source states and identical full shared destination states,
but different literal port contents and different physical source alpha
after filling those contents. Both original roots are TRUE and were
independently replayed. The frozen state has no coordinate which
distinguishes the witnesses.

AFTER: stop this mechanism as prescribed by RESEARCH_RULES. Do not
run or claim the all-mask/all-signature theorem after its prerequisite
has failed. This pair eliminates the proposed uniqueness proof; it does
not supply a negative mixed cycle or refute M3. No new fit, potential,
state coordinate, source constraint or universal status is introduced.

## Exact witness pair

Notation N(k,L,R), with E empty. Let T be the same balanced tree on
keys3..8. The two physical A trees are

    A_lower = N(0, N(-2, E, N(-1,E,E)), N(2,N(1,E,E),T))
    A_upper = N(0, N(-1, N(-2,E,E), E), N(2,N(1,E,E),T)).

In each original prefix, expose the anonymous left child of root0 and
make BOTH its children opaque ports, including the empty child. All
other prefix choices agree. Source alpha, in root,L,R,LL,LR,RL,RR order,
is identical:

    [(0,1,0), (0,0,0), (0,1,2), (1,0,0), (1,0,0), (0,1,1), (0,1,6)].

The source mask is341 and signature is(2,0,...,0). The identical B has
root0, gap0 proxy at0.left, and core path0.right=8, 8.left=6, 6.left=4,
4.left=2; core2 has children1,3, core4.right=5, core6.right=7. Its
core8.right is the original (kind0,ref19) chi8 sentinel. The full
source and destination B arrays, including lo/hi, are saved and compared
in obstruction.json/audit.json. A gap proxy's presence depends on
sigma0>0, not on whether that population is one or two.

Both witnesses execute the original terminal KEEP2. A depth=1, H=1;
actual terminal B depth=4, q=2, and w_L=2H-q=0. They give identical
complete shared destination states as well. Their source and destination
are different, so this pair is NOT a closed walk.

For A_lower, the left anonymous node is the lower of the two gap keys:
its LL port is empty and LR port contains the other key. The port
population bills are (0,1). For A_upper, they are (1,0). There are no
hidden S labels in either of these two ports. All full S-cover and gap
conservation constraints hold. Empty opaque ports are source-legal.

Literal filling produces different source physical shadows precisely
at positions LL and LR:

    A_lower: LL=EMPTY, LR=real anonymous;
    A_upper: LL=real anonymous, LR=EMPTY.

Let pi(w) be the shared source state of a private witness and F(w) the
physical alpha obtained by filling its actual inventory. The exact
pair satisfies pi(w_lower)=pi(w_upper) but F(w_lower)!=F(w_upper).
Hence there is NO function rho of that shared state with F=rho o pi
for ALL witnesses in this signature. This is the precise refuted lemma.
Even using the entire shared source AND destination and event label
cannot distinguish this pair; their full edge records agree there.

## What this does and does not establish

In ACL01, with one fringe key, a visible anonymous slot has an absolute
logical identity. With two fringe keys it can be either key while both
coarse children remain opaque. Canonical derived beta orders the visible
anonymous slots; it does not reveal their order among hidden gap keys.
Adding the private population bill as an observable would change the
frozen state and is not allowed.

A different compatible canonical allocation could still exist. A
potential might take the same value on multiple physical completions.
An allocation-invariance theorem might therefore avoid this obstruction.
NONE of those statements has been proved or refuted by this pair. The
all-mask/all-signature step remains OPEN and requires a different
argument. No experiment on mask extension alone was substituted for it.

## Certification and four-rule exit

obstruction.json saves both complete private environments. Both unchanged
original low roots are TRUE. Raising a populated port's bill from1 to2
violates total signature conservation and makes the original root FALSE
in each control. Source DAG:1400081 nodes. Certification CPU:12.312s.

audit.json independently rebuilds and evaluates the unchanged compiler,
checks all bit-width bounds, compares ALL mu/sigma/alpha/B fields,
replays the physical A accesses, and locates exactly the two different
physical source positions [3,4]. Independent replay CPU:7.344s. No
solver, backend/cap change, new fitting, or production edit occurred.

R1 PASS: exact two-witness mandatory identity, parent domain retained.
R2 PASS as a bounded proof/refutation attack: explicit original valid
witnesses decide the stated lemma.
R3 PASS: one mechanism, one exact obstruction; stopped on refutation.
R4 EXIT: no advancement claimed for the original general M3 theorem.
The proposed literal-determinacy route is strategically eliminated;
NET ORIGINAL PROOF ADVANCEMENT for step #3 is ZERO. ACL01's completed
fixed-sector theorem remains valid. No new assumptions.

Frozen R1-R4, original high h=0 correction, state tuple/depth2/T266,
same high midpoint, source q and weights, and Bank25=25 are preserved.
All other sectors remain in scope of the parent theorem. Stage04 is
still unauthorized. Further mechanisms need a fresh four-rule gate.
