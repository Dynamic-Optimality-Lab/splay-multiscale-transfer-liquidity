# OUT01 — Outside-chi8 mixed-cycle progress

2026-10-29, Asia/Karachi.

**PROVED—UNIVERSAL high toll:** every original OM high leg whose
destination is outside chi8 has weight at least 2. Consequently EVERY
high leg on ANY mixed closed walk has weight at least 2, for every mask
and signature, including signatures with multiple positive gaps.

**PROVED—RESTRICTED DOMAIN mixed sign:** all legal masks and every
signature with at most one positive component, in any of gaps0..9,
population0..266. Every original closed mixed walk in these sectors has
nonnegative weight, both outside and inside chi8. This covers 2661
distinct signature vectors and 335286 mask/signature sectors. Multiple-
positive-gap compensation remains OPEN. No original negative mixed
cycle is certified.

## 1. Source-exact high toll outside chi8

Use the unchanged STRICT_HIGH_COMPILER relation. A terminal genuine
target x is a marked core; q=floor(d/2), 0<=d<=18; OM weight is 6-q,
MO weight is 0. The high target x and fiber root label v remain distinct
independent marked coordinates. High does NOT require root termination
or a repetition-free path. All statements preserve that freedom.

In a valid source B every ancestor of a core target is core: all gap
slots are childless. Unique incoming claims and exact nonnegative
depths give a true target-to-root path with h<=8. The verified source
path must follow it, then N19. The only additional cheap cases beyond
the inherited M2 proof are d10..13, q5/6, weights1/0. For d<=9, q<=4
and the desired toll2 already holds. M2 already handles d14..18.

For a sentinel-clean source, the suffix after the true root is entirely
N19 with LEFT directions. Since d>=10>h+1, the final primitive is a
target-over-N LEFT rotation with the root flag true. For even d this
is the last pair's rotB; for odd d it is the leftover zig. It writes
root=x, x.right.kind=0 and x.right.ref=N19. These are the FINAL writes,
irrespective of earlier alias effects. Endpoint connectivity and strict
core order force x=8: otherwise a larger core could not reach this root
through either the right sentinel dead end or the smaller left subtree.
Thus every valid clean q5/6 endpoint satisfies chi8. A present gap9
would also be disconnected, so it cannot occur at such an endpoint.
This is the established ESD01 final-write argument, applied at d10..13;
its hypothesis is d>h+1, not negative weight. The true h=0 case is included.

For a dirty source let c be the highest-index core claiming N19 as a
kind0 child. The original parent scan chooses c, and chooses RIGHT if
its right pair claims N19, including a double-sided claim. This is the
actual selected claimant; no single-phantom assumption is made.

The two root paths for x and c contain at most9 distinct cores. Their
detour through N19 reaches the common ancestor by entry at most10.
Every associated static order check is therefore active even at d10.
The inherited DSK01 classification applies without changing its proof:

* A selected RIGHT claim permits only c=x (RIGHT_SELF). For x<c, the
  claimant entry contradicts static order. For x>c, x cannot lie in
  c's right subtree, and the detour first enters their common ancestor
  from the wrong side, including the equality case at ancestor x.
* A selected LEFT claim requires x<c. A proper common ancestor again
  gives a wrong-side entry. The remaining possibility has c in x's
  right subtree, ascending through LEFT links until its final RIGHT
  link into x. Since c.left is a sentinel dead end and every core is
  present, c is x+1 (LEFT_SUCCESSOR).

This argument uses only original endpoint order, parents and static
checks. Lower sentinel claimants, raw padding and any gap populations
remain allowed. Incompatible detours fail by entry10; they cannot be
rescued by a shorter d10..13 suffix.

For RIGHT_SELF write A=(x,...,root). Its path repeats A,N, and directions
repeat the real spine bits,LEFT,RIGHT. All511 direction words with
h0..8 are checked at each of four depths:2044 cases. An active rotA
never reads N as a rotating child: the adjacent directions around N
are different, selecting the target instead. Thus representative
relabeling is a replay identity even if literal slot0 moves. This is
not a symmetry of the high max-claimant scan or BST ordering.

For LEFT_SUCCESSOR write B=(c,...), of length s>=1, with h+s<=8.
The path repeats A,N,B, and directions repeat the spine bits followed
by s+1 LEFTs and a RIGHT. Here rotA can read N and alias literal slot0.
All749 words are checked:502 with slot0 on A,247 with slot0 off A/B.
The ON location is one plus the last RIGHT-bit index, or target when
there is no RIGHT; slot0 cannot be on B because all its keys exceed x.
An OFF case needs h+s<=7. Representative relabeling fixes0 and N.
Four depths give2996 cases. Arbitrary off-spine fields stay symbolic.

The unchanged production b_splay_event DAG is partially evaluated on
ALL5040 cases. Each final property is literally CONST BOOL TRUE:

    out.root == target
    AND some real slot has a kind0 child reference to target.

That incoming claim contradicts the mandatory zero incoming claim
count at the final root. Structural b_equal copies the contradiction
to the original fiber endpoint, regardless of fresh interval choices.
This is a final-endpoint contradiction, after every alias write and
possible repair has run. No intermediate tree validity is invented.

The certificate has14600 production DAG nodes;5040/5040 cases pass,
2044 RIGHT_SELF and2996 LEFT_SUCCESSOR, in83.5 CPU seconds. The earlier
symbolic diagnostic independently found all5040 root claims in41.562s.
Each certificate row includes deterministic pin SHA256 and parameters.
Only original integer constant folding is used; no SMT solver runs.

Therefore dirty q5/6 edges are impossible; clean q5/6 edges enter chi8.
Together with inherited M2, every high OM leg ending outside chi8 has
q<=4 and weight>=2. Every high edge from chi8 also has weight>=2 and
stays there. Low conservation and high absorption of chi8 imply a
mixed closed walk stays wholly in one region. Its high legs ALL pay2.

## 2. Universal all-signature compensation consequence

For ANY original mixed closed walk, let N_H count OM legs, let
D_L=sum max(0,-w_L), and P_L=sum max(0,w_L). Then

    weight(C) >= 2*N_H + P_L - D_L.

Thus D_L<=2*N_H+P_L excludes a negative mixed cycle, for all signatures
inside OR outside chi8. In particular N_H>=number of negative low edges
suffices because every low deficit is at most2. This deletes original
outside-cycle cases without assuming a multi-gap low potential. The
remaining multi-gap case requires D_L>2*N_H+P_L and is still OPEN.

## 3. Transfer of the existing low tables

The low source reductions in GAP01 and GAPINT01..04 never use the
chi8 maximum pair to determine the A image, core B splay, H, or actual
terminal q. Their chi8 input in the signed theorem was the high toll.
Active low paths use distinct real operands and ordinary ordered
rotations; all raw phantom pairs and interval padding travel as side
data. Extracting the complete core tree discards this opaque padding.

For sigma=0 or n e_g, g0..8, use exactly the previous J values in[-2,0].
The population-opaque shared S completion, S-empty erasure, at-most3
protected-node classification, full finite row coverage and destination
floor J<=-psi remain valid without chi8. H1 and cheap Gamma1 use the
verified rows; H2 Gamma0 uses its ACTUAL preterminal debt floor and
retains changing unmarked core KEEP events. There is no new fit.

The complete original-root transfer audit removes the chi8 decoration
in each of the62 prior controls, in BOTH endpoints and all flat input
fields, then evaluates the ENTIRE unchanged original low/high root.
All62 pass and independently replay. Every table value agrees exactly
with its old value. This includes every gap0..8, population266, opaque
S ports, whole macros, allocation ambiguity and five mixed cycles that
close on all raw fields and the actual shared high midpoint. CPU180.062s.
These are alignment controls; universal coverage is the source argument.

Gap9 was impossible at chi8 low endpoints and therefore needs the
separately registered GAP9_TRANSFER_GATE. Every exposed anonymous key
now follows S8. Run GAP01's structural proof directly on the right
spine, with L/R reversed. Hidden S sets are determined from this known
gap and ancestor order. Anonymous populations stay opaque; weak private
LE tests are NOT reflected or asserted physically sufficient. S-empty
dangling artifacts erase before they are interpreted as real labels.
All protected-node cases mirror: H1 needs at most2 and cheap Gamma1
at most3. The S-empty first-fringe case forces terminal entry root or
S8 and has weight>=2 by the reflected kernel. Gamma0 debt is unchanged.

Mathematical order reversal i->8-i commutes with these real LOW splays,
preserves H/depth/q, and leaves psi invariant. It reflects proof core
trees and A profiles only. Raw high sentinels, max scans, literal slot0
fallbacks and private inventory witnesses are never reflected. Fresh
original gap9 witnesses are built with their OWN ranks and predicates.

The complete GAP01 corpus reflection passes48450 models and151717
A-word identities, plus43758 B-kernel identities and all4862 debt
values, in9.625 CPU seconds. No new potential table or graph is fitted.
The fresh gap9 original audit passes14 full roots and independent
replays, including populations0,1,2,3,4,266, whole H2 macros, actual
source-legal dangling refs127/255 and a fully closed mixed cycle at
mu484,population3,weight8. CPU39.734s. The initial audit script stopped
on a fixture assertion that required an empty branch to have kind2;
it was a zero-inventory kind1 port. Version2 corrects that assertion,
keeps both kinds, and runs every ORIGINAL predicate. The prototype is
preserved and is not a failed mathematical source identity.

Define J on ordinary states by the static signature dispatch:
g0/9 use GAP01, g1/8 GAPINT01, g2/7 GAPINT02, g3/6 GAPINT03, g4/5
GAPINT04; zero support uses GAP01. For reflected gaps reflect only the
mathematical core tree/A profile. Assign0 to non-low-realizable boundary
shapes, as in the earlier proofs. Every actual low boundary has the
proved valid image. Every low satisfies w>=J(t)-J(s). J(midpoint)=0.
Within the outside induced graph, high OM toll2 and MO weight0 give the
same inequality. Therefore any walk wholly outside chi8 satisfies

    sum w >= J(end)-J(start) >= -2,

and every full closed mixed walk in these single-gap sectors is
nonnegative. All126 masks and every population through266 are included.

## 4. Explicit global glue, without a new existence premise

There is also a single global certificate on these single-gap sectors.
For either original sort use chi8 of its own B fields, and define

    W(ordinary s) = J(s) - 5*indicator(chi8(s.b)),
    W(midpoint m) =       - 5*indicator(chi8(m.b)).

The coefficient5 follows directly from the J range and minimum high
weight-3. It is a sufficient explicit constant, not an optimized fit.

Low preserves chi8, so Delta W=Delta J and its inequality holds.
For a high OM leg within one region, Delta W=-J(s)<=2<=w.
For a high leg entering chi8, Delta W=-5-J(s)<=-3<=w.
A high leg leaving chi8 is impossible. For every MO leg chi8 is
preserved by the original shared B equality, and Delta W=J(t)<=0=w.
This works with independent private OM/MO witnesses on the SAME actual
midpoint. No identification of private histories is imposed.

Thus every original edge on the stated signature domain satisfies
w>=Delta W, with W in[-7,0]. Every finite global walk has sum w>=-7,
and every fully closed walk has sum w>=0. The original h=0,d18,-3
high anomaly is retained as an entering edge. global_potential.py
implements this exact formula; it adds no graph coordinate/observable.

## 5. Original high controls, boundaries and evidence limits

The fresh high-control audit has100 entire original root evaluations
and independent replays. All72 q5/6 dirty candidates have a valid source
and source path but fail the final root-claim condition;28 valid high
controls are accepted. These include multiple claimants, a nonleaf
literal slot0, opaque population266, and clean h0 at declared depths
10,11,12,13,18. The h0,d18,-3 anomaly remains valid and creates chi8.
The high DAG has53455 nodes; audit CPU71.406s. No rejected candidate
is called an original edge or cycle. Complete environments are saved.

All successful original-control programs stay under their registered
300 CPU cap; the gap9 fixture failure and its corrected version are
preserved. Diagnostic/finite phases stay under120 CPU and the production
certificate under300. No state/edge/DAG cap is raised. Only one old
potential table is resident at once. No new full graph is materialized.

BEFORE: outside mixed cycles could have high toll0/1; all single-gap
outside cases and the outer gap9 family were open.
RESULT: universal outside high toll2, complete all-signature signed
subclass, and all-single-gap low transfer with explicit global glue.
AFTER: all single-gap mixed-cycle sectors are closed in both regions;
multi-positive-gap cycles with D_L>2*N_H+P_L remain OPEN in both regions.
NET ORIGINAL ADVANCEMENT: the specified outside mixed-cycle obligations
are deleted; no new assumptions or equivalent existence burden.

The full M3/Stage03/Dynamic Optimality target remains OPEN. There is no
certified original negative mixed cycle. R1–R4, source q, exact signed
weights, O/M sorts and shared midpoint, depth2/T266, frozen Int/Z3
architecture, h0 correction and Bank25=25 remain unchanged. No Stage04,
source/Git edit, installation, commit, push or new graph coordinate.
All414 pre-existing research files are checked against entry SHA256.
