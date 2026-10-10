# S1P novelty regression (§18) — exclusion retained at current HEAD

Witness re-verified against current banked definitions (no superseding theorem;
hashes match erratum run: 4f4b40e0/9abefb16/9dc40634/8bab76f3/1b737aae).

- Cardinality/core/baselines: 5 keys; core 9; n=9; positive dB=6; A=33. EXCLUDED.
- AJ: successors K7≠9 (both positives). AK/AL: K3→D5≠9; K5→K1≠9. EXCLUDED.
- 26AM-G: K3 packet (K3,K7,D5,K1): G2 FAIL (D5 DELETE not genuine) + G4 FAIL
  (K1≠9). K5 packet (K5,K7,K1,K9): G1–G7 all PASS (G5 4≥3 with measured a=2 —
  local compatibility affirmed, never denied). Global: K3 uncovered ⇒ walk ∉
  C_26AM-G. 26AM-S fails (nonzero intermediates). EXCLUDED globally.
- 26AN/AO: positives at blocks 2,8; zero Type-I/II matches at all 17 cuts.
- 26AP: runs [2],[8] len-1, successors K7≠9. 26AQ: run total 2<3. 26AR: no run≥3.
- 26AS: anchors r=s=9. Executable 26AO/26AP/26AQ/26AR/26AS: all REJECT.

**W_INC ∈ S ∖ C_banked. Rule 4 retained.** No replacement witness.
