# MSINK OUT exclusion worksheet (b8b02be76c04 — first clean OUT in campaign order)

Word (34 accesses, A=55, Q=36, Ck=16, W=4):
`D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9`
Derivation: mr33 seed plus inserted D3 at gap 2 (L1 insertion order g=2,k=3;
census idx173). Not an old control (n=34; sha distinct).

Machine facts (pointer audit `MSINK_worksheet_b8b02be76c04.json`): closed exact
both trees; engines agree all 34; genuine keys {1,3,5,7,9}; core 9 at all 35
boundaries; splits=[] (aperiodic); 16 intervals; E=[4,12] (x=5 twice).

MSINK-fail (structural, deterministic): relays t=(2,2) — both long, no short
relay (needs one t in {0,1}). Fails the mixed-relay gate; R1 MSINK/MR-side
separator. (Payers iv7/iv15 valid; sink candidates exist; irrelevant — gate
order fails at H3-mixed first.)

Exclusions (exact predicates, battery PASS):
- RT2/CDK4 (5 keys), CDK5L (core 9). Structural.
- NP (False): E-slots iv4/iv12 (x=5,dA=2,H=1) fail K and P.
- S1/S2/VR (False): |E|=2, need exactly one.
- MR (False): packets {4..7},{12..15} valid and disjoint, payers ok, but
  other-positive iv0 (x=3,q=3,w=1,dA=0) fails K (dA<3) and MR-strict-P
  (KEEP a=0 breaks "a>=1 both"). Precise H6 fail.
- AJ (False): all 3 positive merged blocks succ=7 != rb=9.
- AK/AL-G (False): plus-2 keys (5/1/1) != 9. AL-S (False): S4 fails.
- AM-G/S (False): K3-positive (mb 2) plus-3 = 1 != 9.
- AN (False): zero valid P-packets; all 3 positives uncovered.
- AO/AP/AQ/AR/AS: executable REJECT (pointer push + snaps for AS).
- Additive: splits=[] => no closed-segment decomposition.

Hence W_OUT in R5 ∖ S_raw outside banked union + additive closure. Rule 4 OUT. ∎
