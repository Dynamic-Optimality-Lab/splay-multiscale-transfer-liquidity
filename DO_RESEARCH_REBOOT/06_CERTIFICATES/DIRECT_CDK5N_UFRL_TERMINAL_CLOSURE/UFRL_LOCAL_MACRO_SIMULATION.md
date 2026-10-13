# UFRL_LOCAL_MACRO_SIMULATION.md (Steps 8-10: grammar, high-cost, edgewise composition)

## Grammar completeness (Step 8)

H≤2 ⇒ ≤2 nontrivial accesses (a≥1 each). Exhaustive patterns (terminal
KEEP(v), v marked; interior nonzero must be DELETE — a nonzero interior
KEEP would end the interval): [K(v)]; [D(y),K(v)]; [D(y1),D(y2),K(v)] with
a_term=0 (1+1+0=2 is the only 2-nontrivial shape). Verified: 3,060/3,060
corpus low intervals match ([T] 3,027; [D,T] 33; [D,D,T]-with-zero-terminal
vacuous in corpus, covered by construction). Every H≤2 original interval
maps to a macro with identical H (L3) and q (exact B controller).

## High-cost lifting (Step 9)

H≥3: abstract edge with exact B successor, root v, preserved signature,
any compatible A' shadow, weight ŵ=6−q ≤ 2H−q (H≥3 ⟹ 2H≥6; verified
3,084/3,084 corpus high intervals). Overapproximation declared (spurious
cycles possible; §15 classification applies; none found).

## Edgewise composition + Stage 10 (Steps 10-13, §12)

Per interval (not per walk): representative from true boundary ⇒ abstract
edge with exact (H,q)/lower-bound weight. Consecutive edges share the
EXACT symbolic boundary computed from the true intermediate state
(stronger than §12's minimum: dst(src-state) == src(next) by construction,
both derived from the same concrete pair state). No cross-edge
representative compatibility needed (private concretions differ harmlessly;
symbolic states match exactly). U1 rotation (costs/closure/reachability
preserved — prior lemma); U2 fixed core+mask; U3 B projection (controller);
U4 A shadows; U5 low intervals via representative theorem (above); U6 high
intervals via lower bound; U7 composition (exact boundary match); U8 closed
(original full pair equality ⇒ B equal + A-shadows equal + mask/signature
equal ⇒ abstract closed); U9 weights (low exact ⇒ equal; high ⇒ ≤) giving
w(P) ≤ Σ(2H−q) = 2A−Q; U10 conclusion. STAGE 10 UFRL — PROVED (all U1-U10
discharged; L1-L8 fuzz-verified 2,485 cases + analytic proofs; B-compat
30,773 cases; grammar/high-cost corpus-verified). This is correspondence
(Q: does every walk have a light-enough abstract image?), NOT the
inequality (which needs the product certificate: Part II).
