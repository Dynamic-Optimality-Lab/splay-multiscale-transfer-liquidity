# Separate derivation/review of FD35 and SP35

Status: proof review complete at the stated formula-class scope. The
distinct mutable source controls are independent_fixed_depth_controls.json
and independent_rank_return_controls.json. This work is by the SAME
research agent, with distinct source implementation; not external peer
review or formal proof-assistant verification. The controls do not stand
in for the following universal proof.

The following proof is shorter than the producer's weighted-cover walk.
It avoids assigning costs to anchor-cover edges altogether.

1. Form the finite graph of REACHABLE B-only states under EVERY root-return
choice y!=g, retaining actual BE and both recent-key charts. Choose a
sink SCC C. Each of its outgoing pair edges stays in C.

2. EVERY edge of C has a separately containing closed B walk of genuine
support K: take that edge, return to its start by strong connectivity,
and add closed excursions which exercise every remaining target y!=g.
Each pair has consecutive genuine y,g. Return to the original actual
state, not only to its BF root. All states used are reachable from a
common diagonal by the original graph definition. No A cost bound on
the excursions is used.

3. For the producer's common shallow prefix P_d and finite backbone loop
cost M_d, choose m>=2^(4M_d+2). At EVERY state of C there is an eligible
key x in E of BF depth>=4M_d+2, so its pair has Q>=2M_d+1. Choose that
edge and its source A_x. The true original local packet has H=M_d,
returns ALL of A_x, and has the common shallow prefix P_d at both ends.

4. Apply the prescribed-state source embedding to the closed all-K B
walk from step2. Preparation is BEFORE the preceding genuine g. The
test packet's DELETE Gamma is retained BEFORE its terminal g. The rest
of the closed source and its actual A reset can have any positive cost.
Those costs are outside the separately asserted local inequality. Thus
the chosen edge is a legitimate input to the candidate potential law,
with exactly the actual BE/chart coordinates specified by C.

5. If J existed, put G(z)=J(P_d,z). For every deepest-E edge selected in
step3, its source-valid inequality forces

             G(z_next)-G(z)>=Q-2M_d>=1.

But selection is a self-map of the finite nonempty C, hence eventually
has a directed cycle. Summing those strict increases gives0>=length>0.
Contradiction. No costs on the all-key cover excursions enter this sum.
No A representative is concatenated with a different one.

This proves FD35 independently of the extra anchor-cost and repeated
negative-cycle steps in the producer proof. Those steps are consistent,
but are not needed for the conclusion. For SP35 replace the common-prefix
condition by exact A return, which cancels the arbitrary A-only function;
the same finite-cycle contradiction then excludes F(A)+G(z).

## Critical premise audit

- A word with only deepest-E targets need not have all K as its own
genuine support. Step2 solves this by separate all-K containing histories,
not by pretending that its selected cycle visits every mark.
- A root-return B orbit need not close from an arbitrary starting state.
The proof explicitly takes a reachable sink SCC before using closure.
- A generic erased recurrence need not select a prescribed BE phase.
SP35 section4 fixes this: start at the actual preceding-g state, prepare
A there, then use the ALREADY CLOSED actual BF/BE/chart walk.
- Preparation after the prior genuine g would increase the tested H.
The explicit source word places it before that cut and retains its cost.
- The fixed backbone has d+3>=4 keys for d>=1. Its Gamma word exists by
the inspected ordinary-bottom-up transformation theorem. Ordered payload
substitution retains every physical/genuine key and the exact cost M_d.
- Anchors are marked and are genuinely accessed in the containing source.
Thus the hidden chain persists even in the A branch quotient. The result
is not an artifact of inserting anonymous unary ancestors.
- Counterexamples to this potential architecture are NOT counterexamples
to original source funding: actual between-representative preparations
have positive work. No source credit, donor assignment or Bank25 bound
has been fabricated from the contradictory profile walk.

FD35 is therefore a source-uniform architecture obstruction. It leaves
JR35 and the RT35-JOINT physical donor theorem open. Original CD6, all
frozen source certificates and every original owner map remain intact.
