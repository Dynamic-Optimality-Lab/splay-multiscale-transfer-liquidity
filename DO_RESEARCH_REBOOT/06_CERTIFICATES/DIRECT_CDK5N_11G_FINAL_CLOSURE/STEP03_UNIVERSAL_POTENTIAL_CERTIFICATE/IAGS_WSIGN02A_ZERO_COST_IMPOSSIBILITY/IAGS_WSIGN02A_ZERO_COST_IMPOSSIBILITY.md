# IAGS-WS-02A — Zero-Cost Impossibility: genuine low edges have H >= 1

Mission: `IAGS-WS-02A-...-ZERO-COST-IMPOSSIBILITY`, entry HEAD `e6f3f87`.
Verdict: **PROVED** (universal theorem, code-text verified, 30/30 machine re-check).

## 1. Statement

Let E_L be the slow/low edge relation (`build_slow` root in
`DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py`,
`H == Hv`, `Hv <= 2`). A witness edge is *genuine* iff the terminal
conjunction `tisS /\ marked /\ chg` holds (terminal B-target is S,
marked, terminal event changes B). Then:

> No genuine edge of E_L has H = 0. Equivalently, every genuine low
> edge satisfies H >= 1.

## 2. Load-bearing conjunct inventory (all verified in source text)

All items below are conjoined in the `build_slow` root (per-event items
gated by `active = (e < nev)`). Machine re-check: `CONJUNCT_AUDIT.py`
(30/30 PASS) asserts each quoted line is present in the frozen files.

- (C1) `nev >= 1`: `C.append(d.LT(d.const_int(0, 3), wit.nev))`.
- (C2) Terminal KEEP: with `last = nev-1`,
  `C.append(mux_ref(d, wit.evK, last))` forces `evK[last] = TRUE`.
- (C3) `H == Hv <= 2`: `d.EQ(macro_H(d, wit), Hv)`,
  `C.append(d.LE(Hv, d.const_int(2, 2)))`;
  `macro_H = SUM_e ITE(active, event_a(e), 0)`
  (`PC_ROTATION_INTERPRETER.macro_H`);
  `event_a` table (`event_a`): `dd=0->0, 1->1, 2->1, 3->2, 4->2`.
- (C4) A-depth bound + path anchor (`verify_path_dyn`, active-gated):
  `C.append(d.LE(dd, d.const_int(4, 3)))`,
  `C.append(d.EQ(wit.evpath[ev][0], tgt))`.
- (C5) A rotation gates (`splay_event`, AND-gated with `ev_active`):
  `pair_on = LT(t+2, dd+1)` for `t in {0,2}`;
  `zig_on = EQ(dd, t+1)`; rotations apply by ITE-blend
  (same construction as the verified `b_blend` below).
- (C6) Root termination + no-repeat (`root_terminated`,
  `STRICT_SOURCE_REPAIRS.py:42`, called per active event):
  A: `plast == st.root` where `plast = path[min(dd,4)]`;
  B (KEEP-gated): `blast == bs.root` where `blast = bpath[min(bd,18)]`;
  no-repeat (`NOT(EQ(p[k],p[l]))`) over both-active index pairs.
- (C7) B path anchor + depth cap (`verify_bpath`, active-gated):
  `C.append(d.EQ(bt.bpath[ev][0], bt.bT[ev]))`,
  `C.append(d.LE(bt.bd[ev], d.const_int(18, 5)))`.
- (C8) Key agreement (`same_keep_target`, active-gated):
  `KEEP ==> aS == bC`;
  `(KEEP /\ aS) ==> aI == bT`;
  with `b_key_of = ((bT < NCORE), bT)` and
  `a_key_of = (wit.isS[slot], wit.sidx[slot], wit.rank[slot])`.
- (C9) Entry sync: `C.append(s.aS[0])` (A-root is S);
  `brootS == 1` (B-root is core);
  `s.aI[0] == muxb([i if i < NCORE else 0], bs[0].root)`
  (B-root slot; muxb is identity on core slots).
- (C10) Shadow pinning (`shadow_match7`, both endpoints):
  `wit.isS[st.root] == s.aS[0]`, and if S,
  `wit.sidx[st.root] == s.aI[0]`.
- (C11) State threading: `sts` via `splay_event`;
  `bs` via `b_splay_event(d, bs[e], bt, e, eff_del)` with
  `eff_del = NOT(active) OR NOT(KEEP)`;
  `b_splay_event`: `pair_on = NOT(del) AND (t+2 <= bd)`,
  `zig_on = NOT(del) AND (bd == t+1)` (t even, 0..16);
  `b_blend` is ITE-select per field (verified body: gate FALSE keeps
  old state exactly, all of kl/rl/kr/rr/root);
  `end = ITE(is_delete, bs0-fields, st-fields)` —
  DELETE and inactive events are FULL B-state identity.
- (C12) Terminal genuine block: `tisS`, `marked` appended;
  `C.append(chg)` (`STRICT_LOW_COMPILER.py:197`);
  `chg = OR_e (islast(e) AND diff(bs[e], bs[e+1]))`
  with `diff` over kl/rl/kr/rr/root.

## 3. Lemma A — H = 0 freezes the A-side and pins every target

Assume a satisfying witness with `H = 0`.
By (C3), `Hv = 0`, so `macro_H = 0`; every summand is `>= 0`, hence
every active event has `event_a = 0`; by the table in (C3) and the
`dd <= 4` bound in (C4), every active event has `dd_A = 0`.
By (C5), for `dd = 0`: `pair_on` needs `t+2 <= 0` (false for
`t in {0,2}`), `zig_on` needs `0 == t+1` (false) — all A gates are
off, so `splay_event` returns its input: the A-state is frozen,
`sts[e] == st0` for all `e`, A-root slot `R* = st0.root` constant.
For each active event, (C4) gives `evT == evpath[0]` and (C6) with
`dd = 0` gives `evpath[0] == plast == sts[e].root = R*`.
Hence **every active A-target is exactly the slot `R*`**.

## 4. Fact S — key pinning at entry

Let `x0 := s.aI[0]`. By (C9), the B-root is a core slot and
`x0 == bs[0].root` exactly (slot, not just S-index; `< NCORE = 9`).
By (C10) at the `st0` endpoint with `st0.root = R*`:
`wit.isS[R*] == s.aS[0] == TRUE` (by (C9)) and
`wit.sidx[R*] == x0`.
So every active event's A-target `R*` has `(aS, aI) = (1, x0)`.

## 5. Lemma B — B-root-slot induction (vacuity sub-lemma)

Claim: `bs[e].root == x0` for all `0 <= e <= nev`.
Base: (C9) gives `bs[0].root == x0`.
Step, event `e` active: DELETE gives `bs[e+1] == bs[e]` by the
`ITE(is_delete, ...)` identity in (C11). KEEP: by (C8) with
`(aS, aI) = (1, x0)`, the B-target satisfies `bC = 1` and
`bT == x0` — i.e. the target IS the core slot `x0`, which by the
induction hypothesis is the current B-root.
Vacuity: suppose the witness has `bd >= 1`. By (C7),
`bpath[0] == bT == x0 == bs[e].root`, and `bd <= 18`, so the ITE
in (C6) resolves `blast = bpath[bd]`; (C6) requires
`blast == bs[e].root = x0 = bpath[0]`. But the no-repeat pair
`(0, bd)` is both-active (`0 < bd+1` and `bd < bd+1` always) and
requires `bpath[0] != bpath[bd]` — contradiction. Hence `bd = 0`
in every satisfying witness. Then all B gates in (C11) are off
(`t+2 <= 0` false; `bd == t+1` false), every `b_blend` keeps the
old state, and `bs[e+1] == bs[e]` — root preserved.
Inactive events give identity via `eff_del = TRUE`. QED.

## 6. Lemma C — terminal contradiction

`nev >= 1` (C1), so `L = last` is a valid active index with
`evK[L] = TRUE` (C2): the terminal event is an active KEEP.
Its B-target is slot `x0 == bs[L].root` (Lemma B + (C8)), so by
the vacuity sub-lemma `bd[L] = 0` and `bs[L+1] == bs[L]` exactly.
Hence `diff(bs[L], bs[L+1])` is FALSE on every field, and for
`e != L`, `islast(e)` is FALSE — so `chg` is FALSE, contradicting
the conjoined `chg` in (C12) (together with `tisS`, `marked`).
No satisfying witness exists: **H = 0 is UNSAT for genuine edges**.

## 7. Verdict and boundary

**Verdict: PROVED.** `E_L` contains no genuine zero-cost edge;
`genuine ==> H >= 1` universally (no sampling, no solver call —
pure consequence of the conjoined relation).

Boundary (explicit non-claims):
- This does NOT resolve the OM `w = -3` UNKNOWN (B-depth sign at
  `H >= 1`: `q <= bd_last <= 2q+1` with `bd_last > 0` is untouched).
- No Step04, Bank25, or potential-certificate consequence is claimed;
  Step03 remains OPEN pending the `H >= 1` sign certificate (`w >= 0`).

Residuals (minor, construction-cited, none load-bearing against the
verdict): (R1) `shadow7` body not read — `sh['root'] = st.root`
used by construction of the state-derived shadow (root clause of
`shadow_match7` explicit). (R2) A-side rotation application is
ITE-blend by the same construction as the verified `b_blend`
(gate equations verified; all-off implies identity). (R3) DAG `EQ`
width-coercion 4-bit `aI` vs 5-bit `bT` (corpus SAT confirms the
intended integer-equality semantics; forces `bT == x0 < 9`).

## 8. Ledger and evidence

- Machine re-check `CONJUNCT_AUDIT.py`: 30/30 PASS (read-only
  substring audit of the frozen files; CPU < 5 s; no solver).
- Interactive code-text audit session (this turn): all of (C1)-(C12)
  read verbatim from source, including `root_terminated`
  (`STRICT_SOURCE_REPAIRS.py:42`), `b_blend` body, `b_splay_event`
  tail (`ITE(is_delete, ...)` identity), `splay_event` gates,
  `event_a` table, `b_key_of`/`a_key_of`, `shadow_match7` root
  clause, `C.append(chg)` (`STRICT_LOW_COMPILER.py:197`).
- No solver CPU spent; no PC/SOURCE modification (additive docs only).
- Note: a first audit-script inode in this directory failed
  filesystem materialization (visible to listing, unreadable to the
  interpreter); removed via `git clean`. `CONJUNCT_AUDIT.py` is the
  runnable copy (30/30 re-verified after cleanup).
