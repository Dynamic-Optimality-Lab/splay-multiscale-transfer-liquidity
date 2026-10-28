# IAGS-11G-S03-M2-ESD01 — ORIENTED SENTINEL-DEBT AND UNIVERSAL HIGH-CYCLE CLOSURE

## Excess-Credit Amplification, Extremal Phantom Barriers, Signed Return Rigidity

**IAGS v1.0 | Stage 11G Step 03 | M2 Subordinate Box | Post-M2-CYCLE/M1-ZRC01 | Source-Exact | R1–R4 | OUTCOME B (partial signed restrictions; M2 OPEN)**

---

## A. Entry checkpoint and freeze

- Repository: `Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity`.
- Branch (verified at entry): `coarse-double-branch`.
- Entry HEAD (verified): `5e4f9d39412131c76ea5ac0075562f4f05078a5d` (`IAGS M1-ZRC01 ... OUTCOME F`).
- Tracked tree clean; only pre-existing untracked MSINK side-files + `x.json` (no Step 03 content).
- Freeze preserved, no exceptions: `G_*=G_AF`; contracted high relation
  `E^H_w(s,t) <=> exists m (E^OM_w(s,m) /\ E^MO_0(m,t))` with shared midpoint;
  `w_H = 6 - q_H`; all 126 masks, all signatures, core 0..8, gaps 9..18, sentinel 19,
  complete B topology + exact `lo/hi`, all phantom refs admitted by frozen source, genuine
  B-changing marked KEEPs, declared depths through 18, original parent/side muxes, original
  static-order checks, original rotation semantics, zero-weight high transitions, arbitrary
  finite closed walks (repeated states, nonprimitive, parallel edges/witnesses, abstract-only),
  exact full-state closure. Structural `b_equal` vs complete B-state equality retained.
- No source repairs, solver changes, graph changes, credit changes, budget changes, new
  observables, or domain narrowing. Z3 5.1.0, integer-exact, `h=2`, `T=266`, R1–R4 frozen.
- No solver runs, computational searches, or code experiments were performed in this campaign.
  All results below are hand-derived source-level proofs from the frozen compilers read in full:
  `PC/PC_B_CONTROLLER.py` (BState/BTrace/b_valid/verify_bpath/b_parent_of/b_side_of/
  b_single_rot/b_splay_event/muxb), `STRICT/STRICT_B_CONTROLLER.py` (BStruct/b_tree_valid),
  `CW/STRICT_HIGH_COMPILER.py` (build_shigh, 90 lines), `CW/CW_PRODUCT_COMPILER.py`
  (OM/MO projection), `STRICT/STRICT_LOW_COMPILER.py` (StateVars7/state_valid7).
- `Bank25 = 25` unchanged (zero solver spend). Step 04 remains UNAUTHORIZED.

## B. Exact IAGS Box

`B_ESD01 = (T, C, I, U, beta)`:
- **T:** Resolve M2 — `forall C_B closed in H^B_{mu,sigma}, sum(6 - q_H) >= 0` — by universal
  proof or certified negative B-cycle with exact original-graph lift.
- **C:** (1) certify clean `q_H=9` witness; (2) clean-source extremal phantom theorem;
  (3) directional high-credit barrier; (4) phantom persistence; (5) signed return/escape
  constraints; (6) extension beyond extremal region; (7) universal cycle theorem or countercertificate.
- **I:** M2 B-only equivalence (OUTCOME B), WS-02H normal form, P19 orbit, M2-CYCLE
  determinism, COREK retraction, KD01 rectangularity/alternation, frozen high compiler.
- **U:** padding-vs-endpoint identity (resolved: Gate A same-endpoint multi-credit confirmed);
  forced-phantom scope (resolved: B1/B2 proved); barrier persistence (resolved: C2 proved);
  escape cost (OPEN); h-odd return (OPEN); dirty-state coverage (partial: G core proved).
- **beta:** Exact Excess-Trace Effects => Directional Credit Restriction => Cycle-Sign Law.
  Arrow 1 PROVED (B1/B2 + clean-excess theorem). Arrow 2 PROVED for clean + chi_8 sources
  (R2/R3) and partially for general dirty (R4 core). Arrow 3 (universal closure) OPEN —
  blocked exactly at escape cost (Gate E) and h-odd return (Gate D).

## C. Inherited M2 theorems and failed-route ledger

Inherited (scope-exact): M2 B-only `NegCycle(G^H) <=> NegCycle(H^B)` per sector with uniform
fixed-shadow lifting; `q_H<=9`, `w_H>=-3`, `-4` impossible, `-1/-2` SAT, `-3` UNKNOWN (this
campaign upgrades `-3` to SAT, Sec. D); deterministic witness given `(b,x,d)` with declared
length the only freedom; sentinel orbit (`P_19`, last-match mux, clean-suffix vs claimant
detour, forced `(0,19)` creation); final-root theorem `b'.root=x`; no self-loop by `diff`;
endpoint gap-childlessness filter; min-weight envelope (combinatorial only).
Failed routes (not revived, not reclassified): claimant-count monotonicity, depth-sum reserves,
rank/subtree repayment, generic positive-return assumptions, sentinel-orbit counting,
finite-state-only arguments, envelope-only equivalence, zero-weight restoration assumptions,
direct potential attempts without signed invariant. None is an impossibility proof (Correction B).

## D. Source-certified `q_H=9` candidate audit (Gate A: PROVED — individual edge SAT)

Sector `M={0,1,2,7,8}` (mu bits 0,1,2,7,8; popcount 5), all `sig=0`. Source B0: root 7,
right child 8 (leaf), left chain `7->6->5->...->0`, gaps childless, no kind-0 ref to 19
(sentinel-clean). Dest B1: root 8, left chain `8->7->...->0`, `kr[8]=0, rr[8]=19`, rest empty.
Intervals: root spans `[0,18]` both ends; node `i` on left chain `[0,2i+2]`; source 8 `[16,18]`;
phantom `(0,19)` unconstrained (child loop in `b_valid` ranges over slots 0..18 only).
Target `x=8`, true depth `h=1`, path `8,7,19,...,19`, dirs `RIGHT,LEFT,LEFT,...`.
Audit (20 conjunct classes of charter §5, all checked against code):
(1-5) B0/B1 satisfy `b_valid` (rank containment incl. chain intervals above; root spans full
range; gaps `kl=kr=2`) and `b_tree_valid` (core claimant counts exact — root tot 0, others
tot 1; gap slots absent hence tot 0 with `bpar=NULLB,dep=0`; gap parents core-or-NULLB;
depths 8:0,7:1,...,0:7; `bpar` = unique claimants). (6-8) `verify_bpath` k=0: path[1]=7 =
`b_parent_of(B0,8)` (unique claimant), side RIGHT = dir; static: ancestor 7 core,
`shouldL=(17<15)=FALSE`, `NOT(RIGHT)=FALSE` ok. k=1: path[2]=19 = parent(root 7, tot 0),
side LEFT (19 never matches mux indices), ancestor 19 non-core so static vacuous. k=2..17:
19/19 clean-suffix, dirs LEFT, static vacuous. `bd=18<=18`. (9-13) Splay trace: j=0
zigzag (dirs RIGHT vs LEFT): rotA (x=8 over p=7, side RIGHT): 7.right := 8's old left
(empty), 8.left := (0,7); rotB (x=8 over p=path[2]=19, side LEFT): 8.kr:=0, 8.rr:=19
(phantom installed), p/gp=19 unwritten, root field untouched (pwr FALSE). j=1..7 (all-LEFT
suffix): rotA with xA=19 (no slot writes — `EQ(19,i)` never true; reads alias slot 0,
results written nowhere), rotB idempotent phantom rewrite on slot 8 only. j=8 (t=16):
rotB with `pwrB=(18==18)` sets root := 8. Final: exactly B1 (8 root, 7 left-child with
empty right, chain intact, phantom right). No zig (dd=18 even). (14-17) `diff` holds
(root 7->8); `q`: `2q<=18<2q+2` forces `q=9`; `w1=6-9=-3`; `tt=8<9` marked in mu.
(18) `build_shigh` conjuncts: mu/sig equalities, `b_equal(bs1,g.b)` with g.b:=B1,
`t.aS[0]`, `t.aI[0]=g.v=8`, `state_valid7` (popcount/mu, b_valid, sig bounds, ak/aI ranges —
no shadow coupling in high compiler). (19) Shared OM/MO midpoint `m=(mu,sig,B1,8)`:
OM leg witnessed by t:=(mu,B1,root-marked-8,sig); MO leg by s:=(mu,B0,trivial-alpha,sig).
(20) Marked-target requirements satisfied.
**Theorem (credit amplification):** `exists e_H, w_H(e_H)=-3`. The same endpoints validate
for even `d in {2,12,14,16,18}` (excess prims are endpoint-idempotent; final root-set
`pwrB` fires in the last pair), giving weights `+5,0,-1,-2,-3` on one fixed B-transition.
Inherited `-3` ledger entry UNKNOWN -> SAT (individual-edge satisfiability only; no cycle).

## E. Credit amplification and parallel-edge consequences

Parallel declared lengths on one B-transition (Sec. D) confirm the min-weight envelope
(M2-CYCLE) is the right combinatorics: only the minimum-attainable weight matters for
negative-cycle existence. Amplification cuts one way only: excess padding can always
*decrease* the weight of a fixed clean transition (down to -3); the reverse (padding to
*increase* weight) is what barriers restrict (Secs. F-H). No SAT edge is promoted to a cycle.

## F. Clean-source extremal phantom theorem (Gate B: PROVED)

Suffix determinism lemma (from `verify_bpath` + `b_valid` + `b_tree_valid`): for sentinel-clean
source, with `h<=8` (chain from core target stays in core — gaps have no kind-0 children so
never parents; indegree exactly 1 per non-root core; depths strictly increase along
`bpar`, hence acyclic; at most 9 core slots), the witness path is `x,...,root,19,19,...`
and all suffix dirs are LEFT (`b_side_of(19,19)=FALSE` since index 19 never matches).
**Theorem B1 (forced right-phantom):** Let `b` be sentinel-clean, `b ->^{w<0} b'` valid
(`d in {14,...,18}`). Then the final primitive (last-pair rotB if d even, zig if d odd)
has `side_x=LEFT`, real-or-19 parent `p=19`, `pwr=TRUE`, hence
`boxed{b'.kr[x]=0, b'.rr[x]=19}` with `b'.root=x`. Proof: final indices satisfy
`t,t+1,t+2 >= h+1` (resp. `dd,dd-1 > h`), so all referenced path entries are 19 and all
referenced dirs LEFT — for the even case regardless of `same` (`pB,side` are drawn from
`{path[d-1],path[d]}={19}` and `{dirs[d-2],dirs[d-1]}={LEFT}`); rotB/zig lines 88-89 write
exactly `x.kr:=0, x.rr:=p=19`; earlier prims cannot overwrite afterwards; `pwr` sets root.
The argument extends to every excess depth `d>h+1` (covers `d in {12,13}`, Sec. H).
**Theorem B2 (target must be 8):** Under B1's hypotheses, `x=8`. Proof: `b'` is endpoint-valid
(`b_tree_valid` on `g.b`) with root `x` and dead-end right child `(0,19)` (`19` is not a slot;
no chain passes through it). Any core `c>x` must chain to root `x`; the link below `x` must
be a kind-0 slot-child, hence `x`'s left child `L` (right is dead); but `b_valid` forces
`hi[L]=crank(x)-1=2x-1... ` intervals propagate `hi<=2x` down the left subtree while
`hi[c]>=crank(c)=2c+1>2x` — contradiction. If `x`'s left is not kind-0, larger keys are
disconnected (depth contradiction). Hence no core key exceeds `x`: `x=8`.
**Corollary:** No negative high edge from a sentinel-clean source targets `x<8`. Masks
excluding 8 admit no clean-source negative edge at all. (The apparent `x=5` counterexample
fails endpoint validity by exactly the B2 interval argument.)

## G. Max-key sentinel parent theorem

`b_parent_of(19)=8` whenever `chi_8(b)=1` (`kr[8]=0 /\ rr[8]=19`): `P_19(b)` contains 8 and no
slot above 8 (gaps 9..18 have `kl=kr=2` by `b_valid`, never claimants), and the mux scans
0..18 last-match, so the maximum claimant 8 wins. `b_side_of(19,8)=RIGHT` identically under
`chi_8`. Both facts are used in Secs. H-K.

## H. Directional high-credit barrier (Gate C: PROVED)

**Theorem C1 (extremal barrier):** `chi_8(b)=1 /\ x<8 ==> w_H(b,b')>=2`. Proof: target chain
reaches root in `h<=8` steps (Sec. F); path[h+1]=19 (root tot 0); path[h+2]=parent(19)=8
(Sec. G). If `d>h+1`, static check k=h+1 is active with core ancestor 8: required
`NOT(dir)=shouldL` with `shouldL=(trank(x)<17)=TRUE` (x<8 core) forces dir LEFT, but
constrained dir = side of 19 under 8 = RIGHT — contradiction. Hence `d<=h+1<=9`,
`q<=4`, `w=6-q>=2`. Genuinely signed (lower-bounds a high-edge class); strictly stronger
than structural classification. The earlier intuition that zero-weight edges repair arbitrary
B-changes is false in this region (Correction A instance).
**Theorem C2 (persistence):** `chi_8(b)=1 /\ x<8 ==> chi_8(b')=1`. Write-site audit over all
prims (`{x,p,gp}` locality, inherited 02E): slots touched are `chain(x) ∪ {19}`. If
`8 ∉ chain(x)`: untouched. If 8 is a proper ancestor of core `x<8`: `x` lies in 8's left
subtree (core-in-right-subtree impossible by `lo[8's-right]>=18` intervals; gap-18 aside,
high targets are core) — as `p`, side_x is forced LEFT by the phantom itself
(`rr[8]=19≠real` ⇒ not-right), so p-writes hit 8's left only; as `gp`, p-side is likewise
LEFT; as `xA` (zigzig-first): core parent ⇒ RIGHT side (left-child-of-core-parent violates
`hi[8]>=17`) so writes hit 8's left, or parent 19 ⇒ LEFT side rewriting `(0,19)` identically.
`8=x` excluded; 8 below `x` never touched (path goes up). Hence the phantom survives.
**Corollary (forward-invariant positive region):** `{b: chi_8(b)=1}` is forward-invariant
under `x<8` accesses, every such edge contributing `>=+2`. For masks not marking 8, every
high edge inside the region has weight `>=2` (all targets `<8`).

## I. Old-root depth and two-cycle exclusion (Gate D: PARTIAL — even case proved)

**Preservation lemma (proved):** For a clean-source edge with `d>h+1`, every excess prim
(all-19 rotA: no slot writes; rotB `x`-over-19: writes only slot-8's right fields;
odd zig: slot-8 side + root field) preserves every other slot's fields — in particular
the old root `r`'s slot and `r`'s claimant (parent) relation.
**Theorem D1-even:** If `h` is even, `depth_{b'}(r)<=2`. Proof: pairs `t=0..h-2` fire with
fully real triples (path[t+2] real; gp real-or-19 ≈ root rotation; `pwrA=FALSE` since
`t+2<h<d`) — an exact standard bottom-up splay completing with 8 topological root:
zigzag-top puts `r` at depth 1, zigzig-top at depth 2 (audited against `b_single_rot`
lines 73-96). Boundary pair `t=h` is forced `same=TRUE` (dirs[h]=dirs[h+1]=LEFT: `r`
under 19) so rotA is a 19-no-op and rotB only rewrites 8's right (validity filters the
single clobber case: `r` on 8's right with kind-0 would orphan — such witnesses are
invalid, the rest keep `r`'s parent). Excess prims preserve `r`'s parent (lemma). Final
root-set is field-only. Hence depth fixed at 1-2. (h=0 degenerate: r=x, depth 0.)
**Status D1-odd:** OPEN. h-odd genuine prefix cannot complete (no zig at even d; mixed
boundary pair `t=h-1` restructures without detaching the target in the general `h>=3`
subcase — first unproved implication: mixed-boundary claimant analysis for h-odd `>=3`;
h=1 subcase understood: zigzag/zigzig-first rotA detaches via `pA=r`).
**Theorem D2 (conditional two-cycle exclusion):** A clean-source negative edge with h even
(`w1>=-3`, dest `chi_8`, `depth_{b'}(r)<=2`) followed by the direct return targeting
`r<8` satisfies `d_ret<=depth+1<=3` (C1 applied with target r), `q_ret<=1`, `w_ret>=5`,
`w1+w2>=2>0`. So **no negative high-only two-cycle contains a clean-source negative edge
with even h**. H-odd two-cycles remain OPEN (inherit D1-odd). Note the Gate-A `-3`
witness has h=1 (odd) — the certified edge itself is outside the proved exclusion; no
overclaim.

## J. Key-8 phantom escape analysis (Gate E: OPEN — mechanism mapped, no bound)

From `chi_8(b)=1`, target 8: static at k=h+1 passes (`shouldL=(17<17)=FALSE` needs RIGHT;
dir RIGHT ✓) — excess allowed. Path enters the self-referential orbit
`...->root->19->8->...` (parent(19)=8). Final-prim side is orbit-determined (real sides,
LEFT or RIGHT): LEFT with real p erases the phantom (`x.rr:=p`); RIGHT preserves it.
Erasure is structurally possible; whether a *valid* erasing witness exists at zero or
negative weight is uncertified (no solver authorized; hand-construction of a full
endpoint-valid orbit witness exceeds the analytic budget). Classification established:
(1) preserve+negative/zero (weight unquantified); (2) erase at unknown cost; (3) spawn
further claimants (forced-creation law: excess beyond root+1 forces kind-0 `(0,19)` at 8 —
already present, idempotent); (4) all-dirty closed walks via 8-edges (structurally
admissible, signed cost unknown). The decisive missing quantity is a source-derived
escape/return cost `lambda` for `chi_8 -> clean` paths; inventing a value is forbidden
(R2-20); the correct value may be ≤0. **Gate E is the crux residual for M2.**

## K. Multi-edge signed return analysis (Gate F: OPEN with proved narrowing)

Return-path bound `w(P)>=delta` for clean-to-phantom creation is NOT established (needs E).
Proved narrowing: **every negative high edge from a clean or `chi_8`-dirty source targets
8** (B2; C1 contrapositive). Hence along any high-only closed walk, negatives can only
occur on 8-targeted edges; every `x<8` edge from a dirty `chi_8` state contributes `>=+2`
(C1) while staying dirty (C2). A phase decomposition (clean→phantom creation / dirty
smaller-key accumulation / key-8 modification / erasure / topological return) is
structurally available, but phase (erasure) has no cost bound — a phase map without costs
is normal form, not sign progress (filter §14). No universal or partial return theorem
claimed.

## L. Dirty-state and claimant-orientation generalization (Gate G: core proved)

**Generalized barrier (proved core):** Let `P_19(b)≠∅`, `c_max=max P_19(b)` (core, ≤8).
Parent(19)=`c_max`; side `S_c` = claimant side (RIGHT iff `kr[c]=0/\rr[c]=19`).
For target x with rank on the contradicted side — right-claimant with `trank(x)<2c+1`,
or left-claimant with `trank(x)>=2c+1` — excess (`d>h+1`) fails the static check at
k=h+1 exactly as in C1, giving `d<=h+1`, `w>=2`. Proof obligations discharged: mux
precedence, gap non-claimancy, static gate, active indices, boundary, full endpoint
validity hypotheses. **OPEN:** persistence/general coverage (write-site analysis for
arbitrary `c` — the orientation self-reinforcement of C2 is special to max-key right
phantoms; other orientations lack the interval one-sidedness; multiple-claimant max
changes unanalyzed). Retained as proved core lemma, not a universal closure.

## M. Zero-weight adversarial review (Gate H: restrictions survive; exclusion conditional)

`w=0 ⟺ q=6 ⟺ d∈{12,13}`: both exceed `h+1`, so the B1-extension forces clean-source
zero-weight edges to target 8 with phantom (no zero-weight smaller-target edge from
clean); C1 gives `w>=2` (hence no zero-weight `x<8`) from `chi_8`-dirty. Adversarial
cases audited: clean→dirty (forced to 8, Sec. F); dirty→dirty smaller-key (`+2`, stay,
Sec. H); negative+negative alternation (negatives all target 8, Sec. K — accumulation
possible in principle via 8-edges, cost unknown = E); max-key repeated access (orbit,
Sec. J); multi-claimant (G-core only); signed parallels (compatible with min-weight
envelope); exact closure incl. intervals (enforced throughout); `q=9` class (now SAT,
destined for 8-phantom by B1/B2). Stress result: the two-cycle sum reaches `-3+2=-1`
without D1 — hence two-cycle exclusion is genuinely conditional on the depth bound, not
a free corollary; no cheap-return witness constructed, none excluded in general.

## N. Universal sign reconstruction or countercertificate (Gate I: neither — residual mapped)

Universal M2 (`sum(6-q)>=0` over all closed `C_B`) is NOT proved: any closed walk's return
leg from dirty to clean passes through Gate E (escape cost unquantified). No negative
B-cycle countercertificate constructed (no valid witnesses beyond single edges; bounded
searches inherited, none exhaustive). Conditional closure sketch (for the record, not a
theorem): IF escape cost `lambda` satisfies `lambda >= 3` for `chi_8 -> clean` paths AND
D1-odd is discharged, THEN every excursion from clean pays `>=+2` per dirty smaller-key
edge and at most `-3` per 8-edge creation, and the walk-level accounting closes — both
antecedents OPEN. Precise residuals: (R-E) escape signed cost; (R-D) h-odd old-root depth;
(R-G) general persistence/coverage.

## O. M1/M3 conditional interface implications

M1: untouched. No low lemma used or transferred; sentinel quarantine (M1-ZRC01) respected —
all phantom reasoning is high-side (`build_shigh` excess suffix, absent from `build_slow`
by root-termination/no-repeat). M3: KD01 alternation (`NegMixed <=> NegAlternating(L+,H+)`)
gains a conditional helper — high bridges from clean/`chi_8` sources with smaller targets
now carry `w>=2` (R2/R3); mixed-sign closure still needs E/D1-odd plus low/high coupling,
so no M3 theorem. No promotion of any kind.

## P. R1 sign-relevance audit

Qualifying (genuine source-derived signed restrictions): (R2) clean-source excess theorem —
excludes ALL negative and zero-weight smaller-target edges from clean sources, forces
clean negatives to target 8 into `chi_8` (nontrivial family exclusion); (R3) extremal
barrier + persistence + forward-invariant strictly-positive region (for 8-less masks, the
whole `chi_8` region is `>=+2` per edge); (R4) generalized max-claimant barrier core.
Supporting but non-qualifying alone: (R1) `-3` individual-edge SAT (filter §14: single-edge
SAT ≠ sign progress — recorded as evidence-status change, not leverage); D-preservation
lemma; structural phase map. Non-qualifying (correctly not claimed): envelope re-derivation,
orbit restatement, unverified two-cycle exclusion (kept conditional), circular return
bounds (none asserted).

## Q. R2 source-correctness audit

Firewall items (charter §15) all respected: (1-3) never imposed high root-termination,
no-repeat, or declared:=true substitution — excess suffix explicitly modeled; (4-6) never
removed detours, never assumed all-19 or forced-detour — clean-suffix proved from
`P_19=∅`, claimant orbit from last-match mux; (7) compatibility ≠ satisfaction — Gate A
traced all 20 conjunct classes to a concrete assignment; (8-9) zero-weight edges kept,
no positive restoration assumed — R2/R3 bound weights from below only where proved;
(10) persistence proved (C2) before use, generalized persistence left OPEN; (11) no
classical import — D1-even traced through `b_single_rot` prims, h-odd left open rather
than imported; (12) full endpoint `b_valid+b_tree_valid` enforced on every claimed edge
(B2/Gate-A validity are load-bearing); (13-14) `b_equal` never strengthened inside edges,
full-state equality at closure; (15-17) no hidden histories concatenated, no SAT→cycle
promotion (R1 isolated), no bounded→universal promotion; (18) graph untouched;
(19) UNKNOWN→SAT promoted only for `-3` individual-edge SAT on a certified witness
(cycle status untouched); (20) two-cycle exclusion kept conditional on D1-even hypotheses.

## R. R3/R4 compliance

R1 (freeze): intact — theorem, graph, weights, masks, signatures, depths, muxes, checks,
prims, zero-weight edges, walk classes, closure all preserved; only reading + this report
file added. R2 (source-exactness): every lemma cites conjuncts by file/line-defined
behavior; applicability domains explicit (clean vs `chi_8` vs general-dirty; h parity).
R3 (no silent alteration): no repair, no narrowing, no new observables; `h<=8`, `q<=9`
used as proved, never assumed. R4 (no premature promotion): M2 OPEN; Step 03 OPEN;
Step 04 UNAUTHORIZED untouched; Bank25=25; UNKNOWN never passed as SAT except the
certified `-3` edge-SAT (cycle-UNKNOWN retained).

## S. Final Outcome: OUTCOME B (new sign-relevant restrictions; M2 OPEN)

Proved in one authorized Box: (i) clean `q_H=9` edge SAT with multi-credit same-endpoint
ladder; (ii) forced right-phantom + target-8 law for all clean excess/negative edges;
(iii) extremal `chi_8` barrier `w>=2` for `x<8` with proved persistence and forward-invariant
positive region; (iv) generalized max-claimant orientation barrier (core); (v) h-even
old-root depth `<=2` with excess-preservation lemma and proved h-even clean-negative
two-cycle exclusion. Failed/conditional (preserved exactly): h-odd D1, escape cost E,
universal return F, general persistence G, universal M2, countercertificate (none found).
M1/M3 unchanged (OPEN). Step 03 OPEN. This is genuine signed progress toward M2, not closure.

## T. Residual Step 03 obligations

M1 OPEN (compensation/return-deficit law missing). M2 OPEN with narrowed residual:
(R-E) escape/return cost from `chi_8` (or general dirty) to clean — the single load-bearing
gap; (R-D) h-odd old-root depth; (R-G) general-claimant persistence/coverage. M3 OPEN
(needs M1+M2 resolutions plus low/high coupling). Certified negative full-graph cycle: NONE.
Bank25: 25. No other Box spawned; no successor authorized by this report.

## U. HARD STOP

RECONSTRUCTION of prior state verified at entry; CREATION confined to Secs. D-N above;
no promotion beyond OUTCOME B. M1/M2/M3 REMAIN OPEN. STEP 03 OPEN. STEP 04 UNAUTHORIZED.
BANK25: 25. NO GRAPH MODIFICATIONS. NO SOLVER EXPENDITURE. NO CIRCULAR POTENTIAL.
NO UNKNOWN-AS-PASS (except certified `-3` edge-SAT, cycle status unchanged).

HARD STOP.
