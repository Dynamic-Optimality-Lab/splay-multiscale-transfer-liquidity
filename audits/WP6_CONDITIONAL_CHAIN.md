# Conditional composition map: GC-STATIC → … → MSTL-14P (C40)

Exactly one open premise (GC-STATIC). Everything else verified or banked.
Status per step; §21 semantic audit + §22 ten-point temporal audit mapped.

## C0. GC-STATIC (OPEN premise — the only one)

For every finite present-legal prefix: cap-3 causal assignment of B(t) to A(t)
exists (past-only E1+E2+E3+E4+E7 edges, sited cap 3). Finite: killer 0/112,
26k+ hunts shortfall 0, 41k+ raw-GC gap 0. Unproved (old-abundance theorem open).

## C1. OFFLINE-CAUSAL-ACCOUNTING-VALIDITY (conditional proof, author)

Assume a valid cap-3 matching M_t for prefix t. Then: (1) each B-event one
matched incidence (demand 1 per B-node in flow construction); (2) each A-event
≤ 3 (S→a cap exactly 3); (3) |B(t)| ≤ 3|A_sited(t)| (counting over M_t);
(4) |A_sited(t)| = S_A(t) under U=0/P_all (lemma_sited_identity: every A-event
sited, S_A = E_A; DELETE A-StepEvs included as aev vertices); (5) E_B(t) ≤ 3S_A(t).
No double-count (vertices distinct aev/bev ids); no genealogy-created capacity
(labels only select edges); prefix endpoint = KEEP-prefixes (B(t) complete per
access; mid-access cuts use the same vertex sets restricted — definitions align
since StepEv sets are per-access atomic in builders).
Status: PROVED_AUTHOR conditional on C0 (pure counting; no splay content).

## C2. GC (conditional)

E_B(t) ≤ 3S_A(t) every present prefix, by C0+C1. E_B = all B StepEvs
(splay_trace per KEEP; DELETE contributes none — Pair Access def);
S_A = all sited A StepEvs (U=0). Status: OPEN (inherits C0).

## C3. D6: D(t) ≤ 6S_A(t) (conditional; §21 audit)

D2 (banked): need = max(y−2a,0) ≤ y−1 ≤ 2e_B per KEEP (b_event_count_lemma +
service_bound kernel AR-05); sums to D ≤ 2E_B (cumulative_lemma + L1 banked).
D6 = D2 + GC: arithmetic AR-13 kernel (N ≤ 2X, X ≤ 3SA ⟹ N ≤ 6SA).
Semantic audit: prefix t (KEEP-prefixes, matches D2/GC builders); present-key
(LegalPairInstance + closure audit); fixed universe ([n] legality.py);
D = cumulative need (required(y,a) = max(y−2a,0), C=2: legacy_embedding.py:213);
B StepEv count (splay_trace); S_A count (U=0 identity); DELETE inclusion
(DELETE A-StepEvs are aev vertices; DELETE needs are 0 (y=0) so D unaffected);
KEEP filtering (B only at KEEPs); U=0/P_all (banked). Status: OPEN (needs C2).

## C4. Service → MSTL-14P (conditional; §22 ten-point audit vs code)

Machinery (all banked): k=6 injection (t7inject: 6 LATENT per sited A-StepEv,
legacy_embedding.py:164-172; exactly 6 per A-event per lemma_sited_identity);
rho=2 bandwidth (LIQ0-04: activations ≤ rho(ev); T5 first-eligible order);
conservation (LIQ0-05 kernel); support (LIQ0-06); books-split (LIQ0-09:
repayment = ACTIVE_pre_discharge ≥ need; paid = min(liquidity, need),
discharge(): legacy_embedding.py:200-210); D2 need; D6 stock.
Order per KEEP (replay_B: legacy_embedding.py:235-246): B-splay trace →
T5 per B-StepEv (activation BEFORE spend: ract loop precedes discharge) →
need = required(y,a) → discharge spends min(ACTIVE, need) → paid.
Audit: (1) stock exists before discharge (D6 prefix counts + LATENT injected
at A-events which precede (A-part before B-part intra-access; past accesses
before)); (2) activation precedes spend (code order); (3) LATENT/ACTIVE
transfer preserves conservation (LIQ0-05; discharge only relabels ACTIVE→SPENT,
count-preserving); (4) no double-spend (each credit spent once: ledger order
scan, SPENT never reselected LIQ0-07); (5) cumulative stock + instantaneous rho
both enforced (D6 counts + LIQ0-04 per-event caps); (6) SUPPORT-COLLAPSE MAPPING:
no repo object bears that exact name (grep-verified in math/ + present
artifacts); the composition uses LIQ0-06 (support multiset invariant under T5)
+ banked cumulative reduction (cumulative_lemma.json + tstar_conditional) in its
place — recorded as terminology mapping, not a gap; (7) need generated exactly
(required(y,a), D2-checked); (8) DELETE accounted (A-only replay, y=0, no B
demand; DELETE A-StepEvs inject LATENT normally); (9) every prefix covered
(KEEP-prefix induction; C2 per prefix); (10) no absent-key claims (present
domain throughout; broad MSTL-14 untouched).
Conclusion (conditional): ACTIVE_pre_discharge ≥ need every present KEEP =
MSTL-14P. Status: OPEN (needs C3; ledger/code legs verified now).

## C5. Downstream (unchanged per §23)

MSTL-14P OPEN (needs C4). 15P/17P/18P OPEN (14P-gated consumers, untouched).
MSTL-17P/19 statuses preserved (17P UNPROVED/NO_WITNESS; 19 BLOCKED_BY_SOURCE).
No expansion into those searches (not part of current chain).
Kernel: AR-01..21 reverified exit 0 (this turn); StageBArith = arithmetic only
(§24.2: refuted online Stage B NOT represented as proved); semantic gaps
honestly labeled (§24.4 list stands + Hall/minimal-violator + accounting-validity
conditional proof above).
