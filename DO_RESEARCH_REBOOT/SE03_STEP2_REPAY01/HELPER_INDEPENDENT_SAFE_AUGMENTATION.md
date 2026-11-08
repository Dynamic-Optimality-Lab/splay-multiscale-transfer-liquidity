# Safe debt augmentation through all low-cost anonymous helpers

This proves a new conditional preservation operation on ACTUAL full-source
boundary states. It neither defines the missing baseline debt nor proves
Step2. It does not alter the frozen M3 state space or apply its theorem
to larger cores. The old E1 theorem is reused as motivation, not as an
unsupported extension premise.

## Universal target-cover lemma

In one primitive BST rotation, the depths of its parent and child change
by+1 and-1; the outer subtrees change by+1 or-1; the middle subtree stays
at the same depth. All other nodes retain their depths. These assertions
hold for every node inside every arbitrary hanging subtree, since its
internal depth is unchanged. Thus a FIXED present key changes depth by at
most1 per primitive rotation.

An actual A macro with H StepEvs executes at most2H primitive rotations.
If its final root is x, then

    depth_A_initial(x)<=2H.                              (1)

All DELETE helpers, repeated targets and nongenuine KEEPs are included
in H. Newly exposed anonymous nodes need not be named or inventoried.
Equation(1) concerns the actual terminal marked key, not helper identities.
No bound on the size, shape or population below any source cut is used.

## Source predicates for a width-K, threshold-T candidate

Fix the genuine KEEP label set M, a B-core double bound Qmax, K>=0 and
T>=1 with2T-Qmax>=K. On the actual synchronized full-source boundary
s=(A,B,M), define E_a(s), for0<=a<=K, by the following explicit predicate:

    For every integer h with1<=h<T and every x in M other than root(B),
    if depth_A(x)<=2h then floor(depth_B(x)/2)<=2h-a.       (2)

E_a only reads M, B depths, and the A tree through depth2(T-1). It is
independent of private inventory, helper choices and the outgoing request
word. The family is nested: E_b implies E_a when b>=a. Negative right-hand
sides in (2) simply forbid such a visible nonroot marked key.

For ANY actual full macro out of E_a, its clipped weight

    w_T=2min(H,T)-q

is at least a. For H<T, (1) puts its terminal x into (2), giving
q<=2H-a. For H>=T, q<=Qmax gives w_T>=2T-Qmax>=K>=a.
B is frozen until its terminal genuine KEEP, so its source q is exactly
the depth used in (2). No unmentioned B transitions occur inside this
natural full-source macro.

Define L(s) as the largest a in[0,K] satisfying (2), or0 if no positive
a satisfies it. The endpoint0 is a DEFAULT even when E_0 itself fails.
Thus a negative outgoing weight is possible only when L(s)=0; no false
claim of nonnegative weight at every zero-level source is made.

## Preservation theorem

Let D be ANY actual-state function in[0,K]. Set

    Dplus(s)=max(D(s),L(s)).

For EVERY actual full macro on which w_T+D(t)-D(s)>=0, the inequality
w_T+Dplus(t)-Dplus(s)>=0 remains true.

If its source is not raised, Dplus(s)=D(s) and raising its destination
only increases the residual. If its source is raised, Dplus(s)=L(s)>0;
the source predicate gives w_T>=L(s), and Dplus(t)>=0 gives

    w_T+Dplus(t)-Dplus(s)
      =(w_T-L(s))+Dplus(t)>=0.

Both endpoints may be raised. The result applies individually to valid
edges even if D is not globally feasible. It covers all original helpers
and all H, without any inventory bound, new controller graph, proxy
execution, or finite population argument.

## Six-key specialization and exact limitation

Take Qmax=5,K=3,T=4. Condition(2) reads:

| Candidate level | A depth<=2 | A depth<=4 | A depth<=6 |
|---|---|---|---|
|1|q_B<=1|q_B<=3|q_B<=5|
|2|q_B<=0|q_B<=2|q_B<=4|
|3|no nonroot mark|q_B<=1|q_B<=3|

Each column applies to all nonroot marked keys visible within that depth,
including those exposed by any legal subsequent helpers. The overlapping
columns are intentional. Conditions for the smaller depths are stronger.
This preserves all existing H1/H2/H3 inequalities, including positive
weight2 release obligations introduced by the wider range.

Starting from D=0 alone is NOT a proof: negative edges may remain invalid
unless their destinations receive enough debt. The theorem preserves
already valid edges; it does not prove that every negative edge becomes
valid, nor that repeated transfers close after one augmentation. The
missing source-defined baseline and complete signed preservation remain
the exact Step2 gap. Applying the operation iteratively cannot substitute
for proving a feasible baseline or an exhaustive source closure theorem.
