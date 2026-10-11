# MSINK IN exclusion worksheet (19ff110a7c60 — first clean IN in campaign order)

Word (34 accesses, A=61, Q=36, Ck=16, W=4):
`D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9`
Derivation: concat35 seed minus DELETE at position 15 (D1 at S1|VR seam;
L1 removal dpos[7]; census idx7). Not an old control (n=34; sha distinct).

Machine facts (pointer audit `MSINK_worksheet_19ff110a7c60.json`): closed exact
both trees; engines agree all 34 accesses; genuine keys {1,3,5,7,9}; core 9 at
all 35 boundaries; splits=[] (35 distinct pair-states; aperiodic); 16 KEEP
intervals; E=[4,12] (x=5,(c=1,q=3,H=1) twice); relays t=(0,2) mixed;
joint sink p=0 (x=3,H=13,q=3; 1<=24-2); others: 12 nonpos + iv8 K (H=13).

Exclusions (battery `MSINK_battery_selftest.py` PASS; exact predicates):
- RT2/CDK4: 5 keys (need <=4). CDK5L: core 9 (needs <=8). Structural, no run.
- NP (member_NP False): positives iv4 (x=5,dA=1), iv12 (x=5,dA=2) fail K
  (dA<3) and P (H=1, no distinct DELETE). Exact per CDK5NP-A (Type K d_A>=3).
- S1/S2/VR (all False): |E|=2; each needs exactly one exception (S1P/S2P/VRP).
- MR (member_MR False): relay t=0 at e=4 violates H3 (2<=t_e). Short relay is
  the MSINK/MR separator per charter R1.
- AJ (False): all 4 positive merged blocks have successor key 7 != rb 9.
- AK/AL-G (False): all 4 have plus-2 key (5/1) != 9 (H4 fails).
- AL-S (False): same (S4 delayed-r fails).
- AM-G/S (False): K3-positive blocks (mb 2,18) have plus-3 key 1 != 9 (G4/S6).
- AN (False): zero valid P-packets over 34 blocks; all 4 positives uncovered.
- AO/AP/AQ/AR (executable REJECT on per-leg/merged blocks, unmodified banked
  recognizers); AS (executable REJECT with pointer push sets + B-depth snaps).
- Additive: no proper pair-closed split (splits=[]) => no decomposition into
  >=2 closed banked segments (anti-concatenation per MR precedent).

Hence W_INC in S_raw ∩ R5 outside banked union + additive closure. Rule 4 IN. ∎
