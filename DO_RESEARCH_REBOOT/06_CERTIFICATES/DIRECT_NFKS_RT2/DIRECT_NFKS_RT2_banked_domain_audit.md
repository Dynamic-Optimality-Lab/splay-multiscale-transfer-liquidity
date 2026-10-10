# Banked-domain audit: ≤3-KEEP-key class is NEW (Rule 4 verified)

**Question.** Does any banked AJ–AS theorem already discharge "all closed walks
with ≤3 distinct KEEP keys" universally?

**Method.** Searched CLAIM_LEDGER.md + 02_PROVED AJ–AR/AS docs for KEEP-support /
key-alphabet bounds; inspected each gate's domain quantifiers; ran the five
executable recognizers' specifications against the class definition.

**Findings.**
- 26AJ/26AK/26AL-G/S: require per-positive immediate / one-intervening former-root
  returns with capacities. A ≤3-key walk with a positive and no return (e.g. three
  positives cycling without ever revisiting a former root within the window) is
  outside all three. No key-count clause exists.
- 26AM-G/S: require two-intervening returns with nonpositive intermediates. Same
  gap (consecutive positives violate G3). No alphabet bound.
- 26AN/26AO: four-block two-positive packets (26AO: two orders). A three-positive
  walk is outside (parity); a return-less walk is outside. No alphabet bound.
- 26AP: maximal unit runs + immediate a≥p returns. Walks with shallow/partial
  returns are outside. No alphabet bound.
- 26AQ: requires a shallow bridge between runs. Single-run or bridgeless walks
  outside. No alphabet bound.
- 26AR: split-sink p≥3 runs with AR-P8-gated partial sinks. Walks with immediate
  deep returns or no runs outside. No alphabet bound.
- 26AS: two-group dual-push Hall components. Walks without dual-push events
  outside (26AS hunt: 944/1000 sampled walks uncovered). No alphabet bound.
- Baselines (zero-A, n≤6, depth≤5): orthogonal restrictions, none implies a
  3-key-alphabet theorem at arbitrary n.

**Conclusion.** No banked result quantifies over KEEP-support size. The
"≤3 distinct KEEP keys ⇒ Q_B≤2A" universal is NOT previously discharged.
RT2-A therefore eliminates a genuine original restricted obligation. Rule 4: PASS.
(Nonvacuity walk D1,K1,K3,K4,K3 is AJ-covered individually — immaterial, since
Rule 4 here is class-level, not witness-level, per charter §9.)
