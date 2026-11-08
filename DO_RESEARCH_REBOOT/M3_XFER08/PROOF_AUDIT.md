# Audit of the buried barrier repayment theorem

Verdict: PASS for BURIED_BARRIER_THEOREM.md's explicit five-stage operation,
the complete S-family zero coverage, and the deep-helper cheap-edge exclusion.
The separate universal symbolic checker passed. Full M3 and global zero
LOW coverage remain OPEN. This is not full compiler formalization or
external human/model review.

## Independent derivation of the finite credit obligations

Start from the exact main +1 exits, not an assumed feasible potential.
Every key4 exit returns to root4 with the original lower block unchanged.
The incoming a-depth cap5 then guarantees a-depth<=3 there. F7 is already
E1; the other two cores need one-credit C_B. Their only zeros are upper
targets8/6. Their endpoints are E1 or one-credit R_B, according to whether
the old a child becomes visible. R_B's sole possible zero is a at B
depth4/5, returning to K_B, whose guarded marked exits are all positive.

The special B6->8 +1 exit creates the long left chain H8, not an E1
endpoint. It needs its own one-credit T_B. Its zero4 access puts every
marked core at B depth<=3 and therefore ends in E1. The remaining upper
+1 exits give B6/B6p/B7, with an E1 or R_B endpoint. B6p is a necessary
one-credit auxiliary core; it is not silently equated with B6 or assigned
an unproved two-credit certificate.

This independently closes the explicit dependency K_B1,R_B1,C_B1,T_B1,
G_B2. All target credits are supplied by an earlier region or the old E1
floor. No signed-history horizon, infinite closure construction, hidden
inventory function or equally hard new existence premise remains.

## Parent lemma and the original final condition

In a connected ordered final B tree with every core present, a leaf gap0
proxy must have parent core0. If its parent were p>0, both gap0 and core0
would need the sole left-child subtree of p; that subtree is a leaf, a
contradiction. The ordering of static B ranks is strict, including gaps.
The dual says that a final gap9 leaf has parent8.

The original source separately requires that every gap's child kinds are
EMPTY and every present gap has a core parent. The helper gap remains
present because its KEEP requires positive population, sigma is conserved,
and B rotations do not delete it. A terminal marked KEEP places a core at
the final root. Thus the parent argument applies to that actual proxy.

After arbitrary bottom pairs in the terminal splay, its previous proxy
root f ends at depth1 or2. At depth1 its parent is the terminal. At depth2
the even-depth final same-direction pair leaves f below its old right
neighbor z. The three symbolic last-step equations prove this completely.
For odd terminal depth, lower pairs may rotate z, but the last zig still
puts f directly below the terminal. For even depth, pairs below z preserve
z until the final pair. No unproved stability of z through odd lower pairs
is assumed.

The first minimum splay has all-left path. Its post-helper right neighbor
is original root r for odd helper depth, or original left child p for even
depth. For main B_c those are c/5, and for H8 they are8/7. They differ
from0. Final parent0 therefore forces terminal0. The completed minimum-
path lemma bounds its preterminal depth by ceil(h/2)<=5, hence w2>=2.
The helper may initially carry arbitrary Scores; no emptiness is used.

The same argument proves the registered global corollary. Initial helper
depth>=3 implies neither r nor its old left child equals0: otherwise the
leaf proxy would be at depth1/2. Thus every such valid edge has terminal0
and price>=2. The actual maximum-helper dual uses parent8. All Gamma1
weight0/+1 edges therefore have helper B depth<=2. This is a genuine
exclusion on the original relation, not a sampled observation or an
equivalent feasibility premise. Shallow helper cases are not settled.

Only FINAL b_valid is load-bearing. The intermediate proxy root is allowed
children; its structure-only B validity omits b_valid. Final child vectors
are equated literally to the replay output, with all ordinary fields kept.
The audit confirms leaf kinds, core/gap parent constraints, sigma equality,
primitive pair/zig decoding, final-vector linkage and terminal-only pricing
from bounded source AST inspection. It constructs no source DAG or root.

## Depth caps and exact guard coverage

In every main B_c,4 has depth2 and a has depth3+ell, with ell its internal
depth in L. The cap a<=5 is exactly ell<=2. A key4 return has a-depth
1+ell<=3, and B6->8 has a-depth5+ell<=7. The same ell<=2 follows from the
original S source a-depth1+ell<=3. Thus the main cap loses no remaining
S-zero incoming edge, while larger same-shaped sources are explicitly
outside the claimed theorem.

For R_B a zero H1 target has true depth4/5. Its core prefix c,L5,L4 is
fixed in all four R cores. At depth4, the bottom pair at4 puts old4 at
depth<=2 in the accessed subtree, and the final c/L5/La pair increases
it by at most1. At depth5, after the bottom pair the next pair and zig
leave old4 at2 and old c at1. In both cases the A LL return supplies
Score4 at R and c at RR, so it reaches K_B. The checker verifies both
depth4 last-direction cases, the arbitrary depth5 processed suffix and
their actual duals.

T_B's cap7 guarantees its zero4 endpoint has a-depth<=3. Its exact core
Q4 has all upper depths<=3 too. Therefore E1 holds for the FULL endpoint
regardless of old-owner aliases, private realization or unused fields.
V subset U is necessary at the T_B source to exclude the potentially
deep marked a as an H1 target; it is not omitted.

## Every full A endpoint and helper case

K_B's actual A prefix a(A,4(B,c(C,Y))) has only4/c as possible nonentry
marked H1 targets. All intermediate marks lie below c.left, other upper
marks below c.right. Minimum-helper L/LL/LR leaves only entry a or4 at
charge1; maximum helpers are too deep. The completed unchanged-right-
subtree bound gives the positive terminal prices. The new generic schemas
cover c=6/7/8 without requiring another particular mark such as7.

R_B has either Score4 at L with the actual marked a at LL, or Score4
at LL. In the first, only a can have zero H1 price; in the second a is
hidden and all upper H1 prices are positive. Minimum helpers cannot
occupy any source charge1 position; maximum helpers push a deeper and
have five-upper-core paths, price>=2. C_B needs no A guard: a has positive
H1 price from its cap, and all zero upper exits are handled by actual
left-child versus non-left-child cases.

If C_B's a is the actual L child, R/RL zero upper accesses give Score4
at L,a at LL, and RR gives Score4 at LL. Both are R_B. If a is not the
actual L child, R/RL moves it beyond depth2. Old owner4 has a different
left child and an upper right child, so one-step G cannot report a.
The resulting full endpoint is E1. RR is R_B independently of G extras.
Ports and empty prefixes propagate their kinds; unused index/isS fields
do not create observations. C_B's Gamma1 prices are>=1 by the completed
central-root4 theorem, enough for its one credit.

For the main lower +1 targets, the child-L case can expose a at the
successor's LL and goes to R_B; other cases keep a hidden and go to E1.
This distinction is essential. For B6->8, both original A barrier forms
keep a hidden and old slot0=6 has no immediate a child; hence the full
H8 endpoint has V subset U and satisfies T_B, including its depth cap.

In T_B the minimum helper is controlled by the parent lemma. Its maximum
helper is one B zig at root8 and all upper preterminal depths are<=5.
Source target-cover and V exclude a at charge1, and a right-side helper
pushes its old left branch deeper. Main maximum helpers have the same
five-upper-core bound. All proofs allow Score-bearing helper support.
Gamma0 retains its ACTUAL preterminal floor, and the completed original
H1/H2/Gamma/H0 normal forms retain full endpoints,H and q.

K_B/R_B intentionally omit V filters: incoming observations may read the
old owner, while a fresh source uses the new root as slot0. Those full
boundary vertices still receive credit. An incompatible boundary need
not have an outgoing LOW witness; none is removed or identified. No
private completion, gap allocation, cut bill or owner identity is carried
between successive edges.

## Signed operation and scope audit

Every newly raised K_B/R_B/C_B/T_B source has value1. Its positive rows
are range-safe and every zero row reaches an already supplied credit1.
Every G_B source has value2, its +1 endpoints have credit>=1, and other
H1/Gamma1 prices are>=2. Gamma0 is range/floor-safe throughout. Unchanged
sources only gain a nonnegative target increment. These arguments prove
each operation individually for any Lambda<=D<=2, without assuming global
input feasibility. They do not claim all arbitrary already-debt2 auxiliary
sources are solved by a one-credit augmentation.

The complete +1 table and its dual are independently checked by primitive
identities with unassigned upper roles and arbitrary L. The old eight-
spine source map, F6/F8 zero identities, negative-core proof and saved psi
labels are reused, not replayed. The separate checker also checks the new
parent equations, return-depth bounds, A/G endpoint schemas, cap transport,
helper eligibility, source provenance and exact nonnegative affine slacks.
It does not test numerical trees/populations or formalize the whole compiler.

Both actual LOW orientations are covered. The maximum-helper parent lemma
uses8 and left-neighbor in the actual reversed case; the depth/cost bounds
and ordered return prefixes reverse directly. There is no reflection of
weak-LE private assignments, HIGH sentinels, annotations or psi labels.

All four buried S-spine words now end in G_B with credit2, and the four
old direct-barrier words remain valid. S root5 or dual3 has no zero H1
target by count; S Gamma1 has positive weight by the central-root theorem;
Gamma0 zero rows were already floor-valid. Thus all S-source zero LOW
rows are covered, not just a sampled set of upper accesses. Proper ordered
prefixes realize the new main/return source regions, and the final function
itself assigns genuine main sources2, so the new capacity is nonvacuous.

Full147-O/127-M closure, SAME actual midpoint, independent private scopes,
free high v, weak LE/G/raw unused fields, original prices and corrected h0
remain. Existing HIGH glue gives only the stated covered-walk theorem.
Zero H1 outside S and other unproved classes, shallow-helper zero/+1
Gamma1 rows, and global LOW validity remain OPEN. Full M3 and Dynamic
Optimality remain OPEN. No new whole-signature or negative-cycle claim.

BEFORE: the buried S-zero frontier remained open. RESULT: one explicit
five-stage LOW-safe debt construction and the extreme parent mechanism.
AFTER: all eight S-spine words are covered, and deep-helper cheap Gamma1
edges are excluded globally. NET ADVANCEMENT is genuine original signed
coverage with the depth/A guards and remaining scope stated explicitly.
