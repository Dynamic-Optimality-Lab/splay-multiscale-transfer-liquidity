# ZULRP historical reconstruction (REC-1; evidence-indexed)

Campaign: DIRECT-CDK5N-COMP-ZULR-PROOF, stage 8B, branch coarse-double-branch,
base checkpoint 87f1c02576d3281e1e0cc4abb214518faca3494c (parent 405861c).
Active theorem CDK5NZULR-A (Gate-0 approved, proof-stage promotion unverified).

## 1. Original objective and source model

- Sleator-Tarjan Dynamic Optimality: exists c with LT(X,T0) <= c.OPT(X,T0)
  for all finite key sets, initial trees T0, access sequences X
  (DO_RESEARCH_REBOOT/START_HERE.md; 01_MAIN_PIPELINE/stage_00).
- A/B pair-access model: A splays every access; B splays only KEEP, freezes
  on DELETE; same T0; keys never physically removed; edge depths (root 0);
  a=ceil(dA/2), KEEP q=floor(dB/2), DELETE q=0 (ORIGINAL_PIPELINE.md,
  ZULRP_original_source_semantics.md, replay engines
  CRA_pointer_tuple_replay / CRA_strict_msink_membership).
- Conditional pipeline (all arrows per 01_MAIN_PIPELINE/stage_01-10):
  PAIR ACCESS (PROVED encoding) -> COARSE-DOUBLE Q_B<=2A (OPEN universal) +
  C.ZIG Z_B<=A (proved-math) -> B<=3A (COND arith) -> PIVOT-2 excision
  E_B<=3S_A+g (COND) -> LT<=7LT+2g (COND) -> Levy-Tarjan v3 Thm 4.3
  (established external) -> DYNAMIC OPTIMALITY (OPEN).
- J4/global-potential route (sufficient, not necessary; currently OPEN:
  shared assignment, J-SELF, ROW-DIAMETER) is historical context only; the
  active route is direct Coarse-Double local charging (STRATEGY_REVIEW.md,
  subagent foundation report 2026-10-12).

## 2. Older history (context, not active task)

GC-STATIC, MSTL liquidity, WP-0..WP-6, k=6 specialization, PIVOT-26 family,
J4/row-diameter/J-SELF/shared assignment, root/fringe coefficients, rank-48
finite coupling, LRF/Farkas obstruction, sibling erasure (REBOOT-01, the only
new theorem of the Oct-9 snapshot), abandoned direct mechanisms, early
Coarse-Double cycle attacks: see RECONSTRUCTION_REPORT.md, WORKLOG.md,
STRATEGY_REVIEW.md, 07_STRATEGIES/STOP_RECORD.md. Handbook snapshot
(wp5x-k6c2-specialized @88f344d, 9-Oct-2026) is superseded for the
coarse-double-branch campaign; post-snapshot CLAIM_LEDGER C10-C18/U-B/CWC/
RT2/CDK entries are branch additions under four-rule audit.

## 3. Direct Coarse-Double chronology (git-verified)

RT2 (23392fc) -> CDK4 (9ec277c) -> CDK5L (b888049) -> nine-core novelty audit
(28094e8 G0-C refuted by 26AM-G; 61e5bdc GAP) -> NP (3ac0f8c) -> S1
(6740b19 G0 fail; 0835c6b erratum; a6ba09f PROOF) -> S2 (7299c76; b837b78) ->
VR (6f95703; 783b1c7) -> MR (9396c19; 754202b replay erratum; df416ec) ->
MSINK (87a26a8 G0; e07d683 OUTCOME-B cyclic failure; 3332362 census repair;
28733e0 RC-G0; 6213764 PROOF) -> DLSS (450f60e G0; 864bacc arithmetic erratum;
c914703 re-verify; 6bf8781 PROOF) -> UESINK (f902c36 G0; 405861c PROOF) ->
ZULR Gate-0 (87f1c02 HEAD; theorem SHA
e39e8447c08b3cd5adc8dad1d505cad7f0008ae222ecc1a27bad34aa97c0a447).
Mechanisms 26AJ-26AS are additional banked packet/split domains (C10-C18).

## 4. Bank23 (pre-ZULR; ZULR excluded from own baseline)

Foundations 3 (RT2, CDK4, CDK5L) + five-key nine-core 8
(NP,S1,S2,VR,MR,MSINK,DLSS,UESINK) + packets 12
(26AJ,26AK,26AL-G,26AL-S,26AM-G,26AM-S,26AN,26AO,26AP,26AQ,26AR,26AS) = 23.
Per-theorem domains/status/certs: see ZULRP_banked_inventory.md and
theorem-chronology report (both engines agree; corpus 378 direct + 6 cyclic,
0 residual over 384 archived words).

## 5. Frozen ZULR identity (§5-6)

H1 five keys + core-nine closed walk; H2 E empty; H3 U={p} unique; H4 H_p>=2;
H5 rest strict-K/P; H6 Q<=2A conclusion-only. Witness T0
[9,[6,[1,null,[2,null,[5,[4,[3,null,null],null],null]]],[8,[7,null,null],null]],null].
IN SHA 593b3f3a... (n=32,A=56,Q=36,C_K=16,p=0,H=18,q=3,w=1,R=34; 32/32
primitive). OUT SHA 8cd970c7... = IN minus DELETE(8) at original index 7
(in-L1 idx4 rm7; n=31,A=53,Q=36,C_K=16,E={4}; 31/31 primitive; outside C23*).
Neither witness is a Coarse-Double counterexample.

## 6. What the interrupted session left (see ZULRP_recovery_state.md)

80-attack proof adversarial passed; provenance/negative-cert/corpus/oracle
checks recorded PASS; rewritten ZULRP_adversarial.py has 80 attacks, 10 short
of the 90 required (§8.2 A15/B20/C20/D18/E12/F5). Recovery continues from the
attack-ID audit with a versioned 90-obligation script preserving the 80.
