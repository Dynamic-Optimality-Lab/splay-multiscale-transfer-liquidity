# Root synchronization and a source range that repays locally

These are intermediate universal source lemmas. Step2 is not completed
by them; the remaining low-cost macros require a signed carry invariant.

## 1. A retained nongenuine full KEEP cannot become genuine after erasure

On an aligned recurrent comparison period, immediately after every retained
KEEP x both B roots are x. Between retained KEEPs, the erased root stays
at the last retained target y; the full root is either y or z, depending
on whether the most recent full KEEP targeted y or erased z. Original
DELETEs freeze both. Root identities do not change this conclusion.

For a retained x!=z, if its full access is nongenuine, the full root is
x and therefore equals y, so the erased root is x too. Thus

    retained E-genuine => full genuine;
    retained full nongenuine => E nongenuine.               (1)

This corrects the overbroad POSSIBILITY statement in inherited
SE02_ERASURE01/ERASURE_ALIGNMENT.md about a nongenuine full retained KEEP
becoming genuine after single-key erasure. That possibility does not occur
on the recurrent aligned single-key-erasure domain. The signed sum and
all earlier source identities remain valid; negative J can occur with
BOTH accesses genuine and different depths. No completed inequality
relied on that extra possibility.

## 2. Exact intermediate alphabet inside an auxiliary macro

Start just after a genuine auxiliary KEEP y and end at the next genuine
auxiliary KEEP x. Then x!=y and x!=z. Every retained intermediate KEEP is
nongenuine for E, so its target is y. Erased intermediates target z.
Consequently the full intermediate B word uses only {y,z}, with arbitrary
DELETE interleaving and repetitions. The full source A root at entry is y.

Let g count genuine FULL intermediate changes. If g>=1 the first one is
z. After an ordinary splay of z from root y, the old root y has depth at
most2 by the original outer-source rotation formulas. Every subsequent
genuine alternation between y,z therefore has depth<=2; this property
persists by induction after each splay. Such an access has q<=1. Repeated
same-target KEEPs have q0. No two-key stabilization or graph computation
is required for this bound.

Let Qmax=floor((c_F-1)/2), which is4 for c_F10 and5 for c_F11. Let F_i
be the total FULL B doubles in the auxiliary macro, including its terminal
x. If g>=1, the first intermediate charge is at most Qmax, the next g-1
charges are at most1, and the terminal x charge is at most Qmax. Thus

    F_i<=2Qmax+g-1.                                      (2)

The g+1 full genuine changes, starting from A-root y and ending with x,
give g+1 disjoint source A change-gaps, each with at least one actual
StepEv. Hence H_i>=g+1. If g=0, F_i<=Qmax and H_i>=1. For Qmax>=2 these
cases jointly imply

    F_i<=H_i+2Qmax-2.                                    (3)

## 3. Range-paid signed repayment from the Step1 release

Let q_i be the auxiliary terminal doubles and d_i its sealed ordinary
M3 debt. Its actual Step1 reserve birth is

    r_i=2H_i-q_i+d_(i+1)-d_i>=0.

The signed full marginal in this macro is m_i=F_i-q_i. Since debts range
from0 to2, (3) gives

    r_i-m_i=2H_i-F_i+d_(i+1)-d_i >= H_i-2Qmax.             (4)

Therefore every auxiliary macro with H_i>=8 when c_F10, or H_i>=10 when
c_F11, satisfies m_i<=r_i from an INDEPENDENT source counting law. If
g=0, the sharper bound F_i<=Qmax pays already when2H_i>=Qmax+2.

Let P_i,N_i be its unmatched full/auxiliary demands. The Step1 units released
in that macro, together with f_E(N_i), are actual disjoint units of size
r_i+N_i>=P_i. They can be injected into its unmatched demands by ordinal
order, at the block's end. Sets released at different macros and retired
auxiliary assignments have distinct IDs, so these local repayments do not
reuse a source unit. This is a block repayment, not a claimed native
causal matching-terminal execution for demands earlier in the block.

The unhandled pointwise cases have H<=7 (full core10) or H<=9 (core11),
with g<=H-1. The source A active-path union has at most2H+1 vertices,
but anonymous values and future exposures remain arbitrary. These bounds
are not finite tests, and do not prove that all unhandled cases repay.
