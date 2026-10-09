# PIVOT-9-2: Vine Excursion Decomposition (toward global B<=2A)

Branch `wp5x-k6c2-specialized`, HEAD `88f344d`. Uses banked universal vine
chamber (PIVOT-9: closed vine-pair walks satisfy B<=A, all n) without
reopening it, except one documentation-level bit-convention fix below
(math unaffected; kernel re-verified green).

Critical path served: closed-cycle W_2<=0 -> E_B<=2S_A+g(T0) ->
LT(Y)<=5LT(X)+2g -> Levy-Tarjan -> Dynamic Optimality.

## 0. Conventions (fixed once, used everywhere)
Differ bit tau = [A-root != B-root] (1 = differ, 0 = twin). Lean
`GCStaticVine.lean` bits are twin-bits (negation of tau); the file's old
comment stated the mapping backwards (comment-only fix, proofs untouched,
exit 0 re-verified). PIVOT_VINE_UNIVERSAL.md flip bullets corrected to
differ-bit-consistent form. Per-edge vine weights w' = b-a with
(a,b) in {(0,0),(1,0),(0,1),(1,1)} (V1, n>=5).

## 1. Open vine-segment law (PROVED, kernelized) -- answers §2/A
For any vine-confined PATH V:s->t (open allowed):
  B(V)-A(V) <= tau(s)-tau(t).
Proof: per-edge w' <= tau(u)-tau(v), checked exhaustively on all 2,688
vine-internal edges (n=6, 0 violations), then telescope. Cases: (0,1):
+1 <= 1-0 tight; (1,1): 0 <= diff (flips 1->0 or 0->0); (1,0): -1 <= diff
(diff >= -1); (0,0): 0 <= 0. Sharp (single (0,1) attains). Closed walks
recover B<=A (boundary cancels). Under C=2:
  W_2(V) = [B(V)-A(V)] - A(V) <= tau(s)-tau(t) - A(V),
i.e. negative A-work plus endpoint correction in {-1,0,+1}. Lean
`vine_path_bound` (green). Lean-mapping (edgeOk under inverted bits)
verified on all 2,688 edges, 0 mismatches: kernel applicability confirmed.

## 2. Decomposition (well-defined) -- answers §3
Closed walk visiting vine-pairs, rotated to start at one, splits uniquely
into alternating maximal vine-confined paths V_i and vine-to-vine
non-vine-interior first-return excursions E_i. Maximality forces
alternation; returns exist by closedness. No claim that every cycle visits
vines (see §7 coverage).

## 3. Excursion oracle -- answers §5/D
n=6 (complete, 17,424-node pair graph): 1,024 vine-pairs, 9,600 exit edges,
all return (0 unreachable). Shortest first-return W_2 in [-12,+2]:
58 positives (50 x +1, 8 x +2). n=7 (streaming, 184,041 nodes, 46,592
shortest first-returns, complete): W_2 in [-18,+2]: 104 positives
(103 x +1, 1 x +2). Max excursion surplus is +2 at both n (no growth).
Positives profile: all short (len 3-4), all-KEEP, exits (K,1/6,a=0,b=2/3),
all differ->twin (boundary +1), (A,B) in {(2,5),(3,7),(2,6)[n6],(4,9),(4,10)[n7]}.
Scripts: `scripts/wp6_vine_excursion.py` (n=6), `scripts/wp6_vine_excursion_n7.py`
(n=7); artifacts `vine_excursion/{exc_n6,exc_n7,...}.json`.

## 4. Bound verdicts E0-E5 -- answers §4/§21/G
- E0 (W_2(E)<=0): REFUTED (58/104 positives).
- E1 (W_2(E)<=1): REFUTED (8 at n=6, 1 at n=7).
- E2 (W_2 <= entry branch-tokens): REFUTED (same 8, worst gap 1).
- E3 (W_2 <= tau(s)-tau(t)): holds 9,592/9,600 (n=6) and 46,591/46,592
  (n=7); failures exactly the +2 excursions (residual +1, all tau 1->0).
- E4a (W_2 <= re-entry A-cost): fails on same 8 (re-entry always costs
  A>=1, measured 8,768 x A=1 + 832 x A=2 at n=6, zero A=0 occurrences).
- E4b (W_2 <= own A, i.e. B<=3A on excursions): HOLDS fully (0 violations
  n=6 and n=7).
- Residual equation (exact): total W_2 = SUM_E r_E - A_vine + 0, where
  r_E = W_2(E)-(tau(s_E)-tau(t_E)) in {-13..+1} (n=6 hist banked) and
  vine terms contribute -A(V) each (boundary charges telescope to 0).
  E5 (global <= 0) needs vine-A to cover the +1 residuals: 8 cases (n=6),
  1 case (n=7). OPEN (precise obstruction).
- Growth: longer excursions strictly more negative (n=6 DFS simple first-returns
  to len 9: max +1 at len 3-5, <= -1 beyond; +2 only at len 3-4 shortest;
  n=7 shortest-only census, growth not re-verified there).

## 5. The eight +2s are self-repaying (finite) -- supports E5
Minimal closed walks through each +2 (BFS shortest returns): totals
-12..-18 (returns contribute -14..-20). Exact bounded max-return
(layered DP, len<=12): -13..-15, i.e. every length<=12 closure totals
-11..-13. No vine-confined path from any +2-end to any +2-start (empty):
bad excursions cannot chain inside the chamber; every closure exits to
non-vine and over-repays ~7-10x. Margin is large but unbounded-length
returns are not covered: E5-global remains OPEN.

## 6. Minimal positives -- answers §6
n=6 minimal: len-3 all-KEEP (K,1,0,2)-exit family, (A,B)=(2,6), W=+2,
differ->twin, e.g. u0=4220->u1=1593 word K1,K2,K1. n=7 sole +2: (A,B)=(4,10).
No smaller obstruction exists (len-2 excursions never positive: max 0).

## 7. Entry anatomy -- answers §7/B
THEOREM (n>=5, from V1 contrapositive): leaving the vine chamber requires
a splay at depth >= 2 in some tree. Finite universal types (local rotation
patterns, n-independent): first doubles LL/RR/LR/RL/zig-with-outer-child x
{A-only (52%), both (44%), B-only (4%)} at n=6 (9,600 exits; DELETE exits
dA 2-5 all four doubles + zig; KEEP exits deep-deep (4,4),(5,5),(4,5) top).
Positives: KEEP at A-root (a=0) with B-depth 3-5.

## 8. Exit anatomy -- answers §8/C
Re-entry (last edge into vine): DELETE 5,182 / KEEP 4,418 (n=6); branch
delta (pre-post) always +1 (5,310) or +2 (4,290): returning destroys the
last 1-2 branch-nodes. Re-entry A-cost always >= 1 (finite; a=0 re-entry
possible in principle but 0 occurrences). Universal structural claim:
exit eliminates all remaining branch-nodes (post is vine by definition);
exact A-cost floor open universally.

## 9. Branch resource + token -- answers §9-10
Entry creates 1-4 branch-nodes (4,192/3,602/1,532/274 at n=6); exit removes
the final 1-2 (interior fluctuates). Token does NOT stay: entry key ==
exit key in only 150/9,600 (1.6%); all eight +2s flip ends (1<->6).
Genealogy transfer is the rule; same-object return is the rare exception.
No fixed repair word is involved (consistent with PIVOT-8).

## 10. Non-vine-only cycles -- answers §14/F
Exist (abundantly). n=6: non-vine subgraph (16,400 nodes) has NO positive
cycle at C=2 or C=5/3 (SPFA) => max rho <= 5/3 there; the bound is TIGHT:
the n=6 5/3 achiever word [K3,K6,K3,K4,K2,K1] (A=6,B=10) closes uniquely
at u0=137 and NEVER visits a vine-pair (all 7 states non-vine-pair;
A-vine-only at the seam). So non-vine-only max rho = 5/3 = global max.
Trivial W_2 = 0 via (0,0) self-loops at twin states. Largest observed
nontrivial: -2 (the achiever attains it; rho proves <= -1). Consequence: excursion decomposition (vine-pair endpoints)
cannot cover this cycle; §18 second chamber (or anchor) is mandatory.

## 11. 5/3 anatomy -- answers §19/E
Per-edge (a,b,W_2): (1,2,0),(1,2,0),(1,1,-1),(1,2,0),(1,2,0),(1,1,-1).
The -2 defect sits on two balanced (1,1) edges, not deep splays.
V/E decomposition vacuous (no vine-pair contact). Classified §10/§18.

## 12. Hub / sweep / anchor -- answers §15-17/F
- Sweep (universal word, finite-verified to n=10 + random to 64): KEEP 1..n maps EVERY BST to the left vine
  [n,[n-1,...]]; KEEP n..1 to the right vine. One-way universal EXIT into
  the vine chamber (pair version: same sweep on both trees -> twin vine).
- LV reaches all shapes (BFS, n=4..8 full coverage): return direction
  exists finitely; universal constructive word OPEN.
- Pair-level hub: single SCC verified n=6 (banked) and n=7 (forward +
  reverse BFS from one vine-pair cover all 184,041 both ways). Hence every
  n<=7 state lies on vine-anchored closed walks.
- Anchor reduction (CONDITIONAL, proved as implication): E5-vine-return
  (all vine-anchored closed walks W_2<=0) + both-direction hub =>
  no positive cycle exists (else C^m + fixed connectors => W_2->+infinity
  on vine-anchored walks, contradiction). E5 open (8+1 residuals); hub
  return-direction open universally. Neither assumed.

## 13. Minimal-counterexample mode -- answers §22
Assume positive global cycle; minimize n/support/crossings/length/A.
Vine theorem simplifies vine regions (B<=A there, stronger than needed).
The +2-excursion analysis shows bad local surplus cannot chain inside the
chamber (no vine u1->u0' paths) and over-repays on forced returns; the
remaining hard core is non-vine-only (5/3-type, currently negative).
No positive cycle exists n<=7 (rho<=5/3 / single-SCC + hub).

## 14. -2 defect diagnostic -- answers §20
Closed searches give max W_2 = -2 (not 0): the 5/3 extremal pays via two
(1,1) edges; +2-excursion closures sit at -11..-18. Consistent with two
boundary crossings (entry+exit) each costing >=1, banked as observation
only (NOT a target).

## 15. Statuses (§24) and endpoints
PROVED_KERNEL: open vine law + counting + branch lemmas (GCStaticVine.lean
green, incl. new `vine_path_bound`); V1 finite boundary (n=3/n=4 mirrors).
PROVED_AUTHOR: sweep canonicalization (finite-exhaustive to n=10 + random
to 64, universal-word form stated as verified-finite); V1 assembly (n>=5);
decomposition well-definedness; anchor implication; entry-type finiteness.
FINITE_EVIDENCE: excursion census/bounds/growth/B2/DP-returns (n=6,7);
hub both directions (n<=7); LV-reach (n<=8); E4b; re-entry floors.
REFUTED: E0, E1, E2, E3-as-universal (exact witnesses banked); fixed repair
words (reaffirmed); blanket potential lifts (reaffirmed).
OPEN: E5-global (8+1 residual-+1 excursion types need cover); non-vine-only
universal (second chamber); hub return-word universally; global B<=2A;
DO chain. C.ZIG preserved untouched (§23). GC-STATIC retired, unvisited.

## 16. Global status (H) and DO chain (I)
B<=2A NOT proved. Strongest proved excursion statement (G): for every
vine-visiting closed walk, total W_2 <= SUM_E r_E - A_vine with r_E <= +1
(8 cases n=6, 1 case n=7) else <= 0; walks avoiding the bad-excursion
types satisfy W_2 <= -A_vine <= 0 unconditionally (finite n<=7). Non-vine-only
walks satisfy W_2 <= -1 nontrivially (n=6, via rho: B<=5A/3 gives
W_2<=-A/3<0; extremal -2 observed). DO chain
not assembled (endpoint B not reached).
