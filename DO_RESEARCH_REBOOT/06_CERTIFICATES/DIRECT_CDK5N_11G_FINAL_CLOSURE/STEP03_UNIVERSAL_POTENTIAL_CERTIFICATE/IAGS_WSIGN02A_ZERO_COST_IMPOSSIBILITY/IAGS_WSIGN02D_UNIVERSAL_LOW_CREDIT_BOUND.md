# IAGS-WS-02D — Universal Low-Edge Credit Bound: B-Change Injection, Gap-Ancestor Budget, and Elimination of H=2 Negative Edges

Mission: `IAGS-WS-02D-...-UNIVERSAL-LOW-CREDIT-BOUND`, entry HEAD `05e8aa9`
(verified present on `coarse-double-branch`; this report made no other changes).
Method: mathematical proof from frozen source text only. No coding, no solvers,
no source or graph changes. Inherits WS-02A (PROVED), WS-02B (OUTCOME A),
WS-02C (OUTCOME B) as certified, without reproving them.
Verdict: **OUTCOME A — UNIVERSAL LOW CREDIT BOUND PROVED** (see §H).

## A. Exact frozen theorem and inherited certificates

Prove over the complete frozen genuine low-edge relation `E_L`
(`build_slow`, `DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py`):

> `∀e ∈ E_L, q(e) ≤ 4`, hence `H = 2 ⇒ w_L = 4 − q ≥ 0`.

Inherited (used as lemmas, not reproved): WS-02A — every `E_L` edge has
`H ≥ 1` (terminal `tisS ∧ marked ∧ chg` is unconditional, so every edge is
terminal-genuine), `H = Σ_active a`, `a = event_a` table, active `dd ≤ 4`,
`bd ≤ 18`, B-vacuity for root-target KEEPs, `q = ⌊bd_last/2⌋` from conjoined
`2q ≤ bd_last < 2q + 2` (DAG INT exact); WS-02B — `Sync(0)`, KEEP
resynchronization (`K_i = 1 ⇒ Sync(i+1)`), zero-cost preservation
(`Sync ∧ a = 0 ⇒ Sync`), GenDiv classification (divergence needs a charged
DELETE), latest-GenDiv attribution with no intervening KEEP, and its
injectivity for zero-cost B-changing KEEPs; WS-02C — H = 1 fusion to a
single-event KEEP and the endpoint `q`-identity (used only for the final
classification in §F). Frozen constraints R1-T/R2/R3/R4 preserved; nothing
narrowed: all 126 masks, fringe, signatures, KEEP/DELETE, zero-cost and
nongenuine intermediate KEEPs, E3/E4, exact rotations, exact `q`,
Pre/Post/MinPre, both graph sorts, contracted-high edges, abstract cycles.

## B. Lemma A — B-changing KEEP injection (PROVED)

Active events `0..n−1` (`1 ≤ n ≤ 5`). `B = {i : K_i = 1 ∧ B_{i+1} ≠ B_i}`
(full B-controller inequality). Inactive events never belong to `B`:
inactive ⇒ `eff_del = TRUE` ⇒ `b_splay_event` returns `bs0` exactly
(`ITE(is_delete, …)` over all of `kl/rl/kr/rr/root`, `lo/hi` carried), and
A-side gates are off — both sides identity. Let `P = {j active : a_j > 0}`
(`a_j ≥ 1` there: active `dd ≤ 4` bound plus the `event_a` table gives
`a_j = 0 ⟺ dd = 0`). Define `f(i) = i` if `a_i > 0`, else `f(i) = j_i`,
the WS-02B latest divergence-generating charged DELETE before `i`.
`j_i` is active: `GenDiv` needs a genuine `Sync → Div` boundary change,
while inactive events are both-side identities preserving sync status; and
`j_i` is charged by WS-02B Lemma D. Injectivity: charged–charged pairs collide
only if equal (identity map); zero-cost pairs are distinct by WS-02B
Corollary A (if `i1 < i2` shared `j`, KEEP `i1` would sit strictly between
`j` and `i2`, against the no-intervening-KEEP clause); mixed pairs cannot
collide since KEEP positions and DELETE positions are disjoint (`evK`
boolean). Hence `|B| ≤ |P| ≤ H ≤ 2` (each `j ∈ P` contributes `a_j ≥ 1` to
`H = Σ_active a ≤ 2`). The terminal genuine KEEP always belongs to `B`
(`chg` forces terminal `diff`). Therefore at most **one intermediate
B-changing KEEP** per macro. WS-02B's attribution is universal over KEEP
kind (its proof uses only Sync/Div/resynchronization, never S-ness), so
fringe KEEPs are covered, charged or not.

## C. Lemma B — One B-splay produces at most one internal gap (PROVED)

Define `Γ(B)` = gap slots `9..18` with a kind-0 (node) child, read off the
exact `kl/rl/kr/rr` fields. Pre-state hypothesis: all gaps kind-childless
(`Γ = ∅`; follows from full `b_valid`, which forces `kl = kr = 2` on gaps —
`PC_B_CONTROLLER.py:49-53` — and entry `bs[0] = s.b` carries `b_valid` via
`state_valid7`). Consider one valid active-KEEP B-splay. Every primitive
writes child fields only at its `{x, p, gp}` slots (`b_single_rot` updates
exactly indices `p`, `x`, `gp`, gated by `NOT(p_was_root)` for `gp`;
`NULLB` gp matches no index so writes nothing; `b_blend` keeps all other
fields verbatim), and `{x, p, gp} ⊆ path ∪ {NULLB}` for every prim
(rotA/rotB/zig address only `path[t..t+3]` entries). Non-target gaps can
never be path entries at index `≥ 1`: such an entry claims the next-down
node with a kind-0 child, contradicting pre-state childlessness. Hence only
the target slot may gain kind-0 children; all other gaps keep entry
childlessness. Case I (core target): the whole path is core (gaps cannot
parent anything), so no gap field changes and `Γ(after) = ∅` — off-path gap
subtrees are untouched, and a root-target (`bd = 0` forced by root
termination + no-repeat) fires nothing. Case II (fringe target `g`):
`g` begins a leaf; with `bd = 0` nothing fires; with `bd ≥ 1` only `g`
(always `x = path[0]`) may acquire children while every other gap stays
childless, so `Γ(after) ⊆ {g}` and `|Γ| ≤ 1`, for every depth ≤ 18 and both
zigzig/zagzig wirings (direction only selects wirings, never the write
set). Fully-valid pre-states additionally have core roots (9 core slots with
exactly-one-parent counts plus strict depth decrease forbid an all-core
closed parent map under a gap root), consistent with the above. No step uses
textbook splay theorems — only the frozen write indices and gate equations.

## D. Lemma C — Preterminal gap budget (PROVED)

By Lemma A there is at most one intermediate B-changing KEEP. B-evolution
is exactly event replay (validity predicates constrain, never mutate —
§G.7): DELETEs are full identities, non-changing KEEPs are replay identities
(`bd ≥ 1` always fires a prim and every prim changes refs under acyclic
one-parent/depth validity, so unchanged ⟹ nothing fired). Hence
`B_preterminal` (state before the terminal KEEP) is either the unchanged
entry B-tree or the result of exactly one intermediate B-splay applied
directly to the entry tree (all prior events are B-identities, so the single
changing splay sees pristine entry state with `Γ = ∅`). Lemma B gives
`|Γ(B_preterminal)| ≤ 1` in the second case, `= 0` in the first. No
intermediate `b_valid` is assumed at any point — the conclusion flows from
history plus rotations.

## E. Lemma D — Terminal B-depth and `q` bound (PROVED)

The terminal event is an active KEEP, so `verify_bpath`, KEEP-gated
root-termination (`blast = path[min(bd,18)] = bs.root`), no-repeat over all
both-active pairs, and `bd ≤ 18` all apply. Root first appears on the path
at exactly `bd`: `path[bd] = root` by termination, and any earlier
appearance contradicts no-repeat. NULLB never occurs on the active path:
it would force the previous node to be an unclaimed non-root slot, i.e. an
absent gap — but absent gaps are permanently kind-childless (never path
nodes in the entry-validated intermediate splay: childless ⇒ never parents;
fringe targets require nonempty `sig`; S-targets are core — hence untouched
since entry, retaining entry kind-2 children), contradicting the kind-0
child the parent link requires. Childless gaps are likewise excluded from
path indices `≥ 1` (the parent link is a kind-0 claim). Therefore every
path node lies in core ∪ Γ(`B_preterminal`): `path[0]` is the marked core
target, proper ancestors are claimants (core or internal gap), and the root
is core (entry) or a changing-splay target (core, or fringe gap with the
kind-0 children its `bd ≥ 1` splay necessarily created — a `bd = 0` fringe
splay is a B-identity and cannot be the changing one). The `bd + 1` nodes
are pairwise distinct in a set of at most `9 + 1 = 10`: `d_B^term ≤ 9`,
so `q = ⌊d_B^term/2⌋ ≤ 4`, for every satisfying witness — fused or not, no
enumeration. (Note: `bd = 9` needs the single internal gap on-path;
`q = 4` covers `bd ∈ {8, 9}`.)

## F. Resulting low-edge sign classification (PROVED)

`H ∈ {1,2}` universally (WS-02A over always-genuine-terminal `E_L`).
`H = 2 ⇒ w_L = 4 − q ≥ 0`. Hence `w_L < 0 ⇒ H = 1, q ∈ {3,4}`
(`w = 2 − q < 0` with `q ≤ 4` forces `q ≥ 3`), `w_L ∈ {−1,−2}`,
`d_B^term ∈ {6, 7} ∪ {8, 9}` (correcting the anticipated `{6,7,8}`: `q = 4`
admits `bd = 9` through the single allowed internal gap). Every negative low
edge therefore belongs to the WS-02C fused class: unit-charge single access
of a marked key at entry-A-depth 1–2 with entry-B-depth 6–9. This does not
imply cycle nonnegativity; H = 1 compensation stays open; contracted-high
edges (`w_H = 6 − q`) are untouched.

## G. Independent proof audit and IAGS R1 evaluation

1. WS-02B injection covers fringe KEEPs: its lemmas never assume S-ness;
   fringe agreement flows through the same `same_keep_target` gap branch. ✓
2. Charged-KEEP vs charged-DELETE images cannot collide: disjoint `evK`. ✓
3. Entry gaps are leaves: `b_valid` (`kl = kr = 2`, `i ≥ 9`) via
   `state_valid7` on `s.b = bs[0]`. ✓
4. Core-target paths avoid gap leaves: childless slots cannot parent. ✓
5. One fringe splay creates at most one internal gap: write-set ⊆ path,
   non-target gaps are never path nodes. Audited against every prim form. ✓
6. No other B-mutation exists: replay is DELETE-identity / KEEP-splay-or-
   vacuity-identity / inactive-identity; only KEEPs change B, bounded by A. ✓
7. Structure-only validity never mutates: predicates only; replay constructs. ✓
8. Ten-node bound: degenerate sentinels excluded (NULLB ⇒ absent-gap-with-
   kind-0-child, impossible by entry-untouched permanence; repeats excluded
   by no-repeat; root pinned at `bd`). ✓
9. `q = ⌊d_B/2⌋`: unconditional integer consequence of conjoined
   `2q ≤ d < 2q + 2`. ✓
10. No narrowing: all arguments are consequences of frozen conjuncts; every
    witness class (fringe, zero-cost, nongenuine, DELETE) preserved. ✓
R1: the H = 2 negative class is eliminated universally; the remaining low-
edge sign problem is exactly the fused H = 1 deficit (`δ ∈ {1,2}`) plus
compensation — a genuine, non-tautological restriction of the search space.

## H. Final verdict

**OUTCOME A — UNIVERSAL LOW CREDIT BOUND PROVED.** All four lemmas are
certified from frozen semantics: `∀e ∈ E_L, q(e) ≤ 4`; `H = 2 ⇒ w_L ≥ 0`;
negatives satisfy `H = 1, q ∈ {3,4}, w_L ∈ {−1,−2}` with the fused
shallow-A/deep-B structure (B-depth 6–9).

## I. Next-step authorization status and hard stop

Remaining low-edge work is exactly the fused H = 1 quantitative compensation
(deficit reserve + replenishment), which is NOT authorized by this campaign
and is not executed here. Logically subsequent boxes (H = 1 compensation,
contracted-high-edge accounting, global cycle certificate) are identified
only; none is opened. No Step 04 promotion (Step 03 obligations remain),
Bank25 = 25 unchanged, no source or graph modifications.

**HARD STOP.**
