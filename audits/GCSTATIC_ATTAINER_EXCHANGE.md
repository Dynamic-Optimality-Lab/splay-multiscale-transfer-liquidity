# C189 — ATTAINER EXCHANGE DECISION AUDIT

Branch `wp5x-k6c2-specialized`, HEAD `88f344d` + uncommitted C184–C189
tree (authoritative; history untouched, main untouched).

Target: MAX-EXCHANGE-3 — post R3 attainer sigma* -> SOME pre word tau
with Net_s(tau) >= rho + Net_{s'}(sigma*), closing both Lipschitz
transitions, then Phi>=R3>=0 induction to GC-STATIC.

## 1. Single-prepend (Phase 2)

- Ceil assembly kernel green (`single_prepend_assembly`,
  `single_prepend_consume`): (dx+1)/2 <= (dz+1)/2 + (dxp+1)/2 from
  dx <= dxp + dz, pure omega.
- Depth-drop premise [MECHANICS-ROT] open (rotation rows + telescoping +
  ecount_eq, BD1 kit). Finite 0/2640+ (single saving <= 0 tight).
- B-side bounded-prepend REFUTED (+3/+4 at n=16/24): B-splays can set up
  downstream B-savings exceeding own cost. Kills DELETE [z]+sub route.

## 2. Exchange scanner (Phases 3-5)

`scripts/wp6_exchange.py` (Net words exact replay; post-attainer via R3
structure; families Fm1(STOP)/F0(same)/F1/F2/F3/F4 over K={z,x,y,w};
F5 global = Lipschitz invariant check). Artifacts
`attainer_exchange/{hard_transitions,selector_scan}.json`.

- Hard set: vine52 (F0 fails +33 but STOP wins, lip holds); plus1 (+1
  KEEP killer: NO menu wins, global fails — genuine violation, correctly
  isolated); bk1_z1/r42del (F0 tight, attainer [1,1,2] with repetition);
  bk1_z2 (F1 [z] tight).
- Broad scan n=16 (424 transitions, walks + arbitrary): 0 lipfail;
  F2+ NEVER needed (Fm1 ~404, F0 10 len-1, F1 10 len-0).
- Joint hunt: TRUE-EXCHANGE (tgt>0, same fails, menu saves) only 2
  cases, both len-0 with F1 singleton. No len>=1 F1-save observed.

## 3. Selector rule (Phases 6-8)

COMPLETE structural menu (all observed winners fit; F3/F4 empty):
- tgt <= 0 -> STOP (Net([])=0; sound trivially).
- len(sigma*) = 0, tgt > 0 -> [z] (KEEP exact: Net=r_z=rho; DELETE
  vacuous since tgt=-3a_z<=0). Sound by r_z >= -3a_z.
- KEEP len<=2 -> [z]+sigma* (EXACT replay equality; sound, needs
  |tau|<=3 + Net-split + R3-max = O5 word-model).
- KEEP len 3 + s'-tie (proper subseq sub with Net_{s'}(sub)=post) ->
  [z]+sub (same replay soundness).
- Else same-chain sigma* (drop-correlation: 1-term closed mod
  single-prepend; 2-term finite; 3-term open) or genuine violation.
- DELETE has NO [z]+sub rule (B-prepend false). DELETE menu is
  {STOP, [z], same-chain}.

Tie data: walk KEEP-len3 all tied (thin: 3 instances); plus1 and t=5
(+1 family) have NO ties — exact violation diagnosis. Len>=2/tgt>0
pattern REFUTED at n=24 arbitrary (12 hits); 10/12 same-chain tight,
1 F2-[z]+sigma exact, 1 genuine violation.

## 4. Kernelized (all exit 0, no sorry/admit/axioms)

`R3_nonneg`, `exch_stop_consume`, `keep_exchange_short`,
`keep_exchange_tie` (conditional arithmetic; replay-split + R3-max =
O5 word-model obligations). Prior: z-exactness, max-lifting,
same-B diff, split, 1-term, cleanliness-\/a-free.

## 5. Verdict

NO TERMINAL. The exchange architecture is COMPLETE and SOUND everywhere
except: (i) same-chain drop-correlation len>=1/tgt>0 (1-term closed mod
single-prepend-proof; 2-term finite-clean min 0; 3-term open with -11
drops + slack undescribed); (ii) O5 word-model (Net-split, R3-max over
words, floor-collapse) specified not built; (iii) [MECHANICS-ROT]
drop-bound proof; (iv) a_z=0 cleanliness/macro proof; (v) reachable
a_z>=1 mechanism. GC-STATIC OPEN/NO_WITNESS. Falsification (KR2,
Lipschitz-reachable, Phi-SA to n=64) all clean. Zero kills (one genuine
arbitrary-pair Lipschitz violation family, not GC).
