# Gate: two cheap path resets, with an independent B-budget test

2026-10-31, Asia/Karachi. The user explicitly authorizes continuing beyond single resets. Matching-terminal work remains FROZEN. Old source/research/status/Git files and all Stage 11G artifacts are read-only. All new writes are exclusive to this fresh run. No larger finite key size, fitted coefficient, adaptive skeleton/seed change, optimizer or automatic successor is permitted.

## Why adding resets to the old skeleton cannot suffice

For every closed source walk with nontrivial cyclic A-root blocks, each positive block has a_i>=1 and at most one genuine B-changing KEEP. It follows directly that

    E=sum max(q_i-2a_i,0)
       <= G_B=sum_(KEEP requests) max(q_B-2,0).

The old recurrent B skeleton has double counts 5,3,1,2,1,2,1,2,1,2,1,1,1, so G_B=4 per lap. Two positive-cost KEEP-less reset blocks contribute C_D>=4 per lap. Therefore that B skeleton cannot produce E>C_D with two such resets per lap, regardless of A trajectory. This is an independently mandatory budget obstruction, not a finite fit or a universal bound on other B sequences.

## One fixed new architecture

Keep the 13-key diagonal R13 and setup D13,D12. Replace the old KEEP skeleton with the single fixed four-bit-reversal order restricted to ranks 0..12 and shifted by one:

    V=1,9,5,13,3,11,7,2,10,6,4,12,8.

First compute its B-only source orbit at whole-V boundaries, stopping at first exact repeat or after 64 laps. DELETE does not change B, so this orbit is independent of A reset choices. On the exact recurrent B period of b laps, compute G_B. If G_B<=4b, STOP before all A-policy cases: every cycle with two effective one-StepEv pure resets per lap has C_D=4p and E<=G_B*p/b<=C_D. If B does not close within the cap, record OPEN and stop; do not increase the cap or select another skeleton.

Only if the B budget passes, classify the 78 lexicographic gap pairs 0<=g<h<=12. After the KEEP at each selected gap, look at A's search path to the NEXT KEEP target. If that target has depth at least three, DELETE its depth-two ancestor. This is a genuine source double costing a_D=1, distinct from both current and next target, and its block is KEEP-less. If the target depth is one or two, DELETE the current root as a prescribed zero-cost fallback. This makes the source policy deterministic and present-key total; the recurrent cycle is admissible only if BOTH reset slots are effective pure one-StepEv resets in EVERY lap.

The reset target is selected from A's current path to a fixed next key, never from FI/UD outcomes, future B costs or an optimizer. It brings a proper ancestor of the next target to the A root with exactly two source rotations; B remains unchanged. The two actual unit pools are charged once each. Root fallback cannot be counted as a successful multi-reset case.

Iterate the actual pair/policy map at whole-V boundaries, retaining exact states, until its first repeat or 64 laps. A repeated pair also repeats the deterministic reset choices; extract that actual finite source word and its reachability prefix. Temporary A=B does not stop execution because a later reset can separate the pair. A qualifying recurrent cycle must be nowhere diagonal, have two effective pure resets per lap, satisfy E>C_D, have some FI-accepted physical cut and have NO UD-accepted cut. Perform unchanged FI/UD all-cut comparison only on survivors of these mandatory source filters.

Visit all gap pairs in lexicographic order, stopping immediately at the first strict witness. Certify it and reflection with the independent pointer source. If none succeeds, complete the declared finite classification and reflect all examined source cases. Any cap-limited case remains OPEN and prevents a complete exclusion claim. No gap, reset policy, cap, seed, skeleton or ceiling is replaced after results.

## Four rules before execution

1. **Strictly smaller — PASS.** One fixed 13-key B order, two prescribed depth-two path-reset slots, 78 fixed gap pairs and a deterministic bounded orbit. Arbitrary words, n, reset keys, numbers of resets, potentials and general allocation are removed. The architecture differs from the one-reset class in both B demand and source reset mechanism.
2. **Concrete reason — PASS.** The source block inequality E<=G_B provides a pre-execution necessary budget test independent of A. Each effective reset has the exact depth-two a_D=1 identity, hence minimum four-unit funding per lap. Its path-ancestor placement targets future A costs without completing that future KEEP. Exact repeated source states give reachability and closure; unchanged FI source-frame ceilings give a concrete repayment mechanism if it succeeds. No numerical feasibility premise or guaranteed strictness is assumed.
3. **One bounded campaign — PASS.** One B-budget-gated two-reset architecture, at most 78 policies, one tuple/pointer source audit, one strict certificate or exact scoped obstruction. The B preflight is a filter for this same architecture, not permission to try more skeletons. No second independent open theorem or adaptive successor follows.
4. **Original obligation — PASS subject to exact success.** Success is the requested actual reachable, nowhere-diagonal closed pair with E>C_D, FI acceptance and UD rejection at every cut. Earlier repayment, an ineffective reset, a diagonal cycle, a cap-limited trajectory or a UD-covered cycle does not count. If no witness results, no original CD case is newly settled and strict coverage remains NOT ESTABLISHED.

## Certification and stop

Pin all old artifacts and the entire 125-file Stage 11G inventory before executing new source requests. Preserve branch/HEAD/tracked status. The source uses parent-first LL/RR and the same cyclic A-root-block definitions. UD/FI, positive-fact histories, one reservation per payer, residual cursors and one-period budgets remain unchanged. No old executable recognizer/status writer is imported or executed.

Record the exact B source recurrence and G_B calculation, every tested policy/source input, first repeated pair, actual reset targets/costs, paired closure, all diagonal indicators, E and C_D, every rejection reason, and all-cut source-unit certificates if a candidate survives. No prefix, second-lap or alternative-map credit may pay a cycle. Use distinct actual event identities and both orientations. Record BEFORE/RESULT/AFTER and the strategy review honestly. Stop after this fixed attempt; universal Step 3/CD remains OPEN and matching-terminal/Stage 11G remain FROZEN/unchanged.
