# Separate audit of the interval-child augmentation

This audit derives the endpoint credit before inspecting the proposed cap.
It uses universal terms and order/type arguments, then a separate bounded
checker of the new identities, affine slacks and source AST provenance.
No original source root, transition, bank entry or population is evaluated.
This is not external human/model review or full compiler formalization.
The machine portion's execution status is recorded in symbolic_audit.json
and run_result.json; publication requires both to pass.

## Endpoint-first derivation

Take an arbitrary original H1 edge from an I_L source, with actual child
x<r. Present marked x cannot be an invalid reference, since mux_ref's
fallback is immutable source slot0, with label r, not x. Completed H1
normalization therefore gives the actual zig r(x(A,M),C)->x(A,r(M,C)).
A and C are the opaque exterior cuts. The arbitrary M stays at depth2;
even if it has a real unmarked/anonymous root and marked descendants,
none of those descendants is promoted into the observed shadow.

The target exterior cuts are L=A and RR=C, so they have nonzero kind.
The old root r is the real right child. Its Score/mark type is immutable.
The only other possibly real observed position is M at RL. Source V={x}
forbids any marked label there except r or x, with r excluded at the old
root. At the target x is the new root and excluded from V. G at M reports
the SAME old slot0 label r, possibly duplicating the actual right child.
Set-valued V therefore is {r} if r is marked, and empty if r is unmarked.
No source/type interpretation of unused opaque fields is made.

In the marked branch the target is I_R. The completed old-root core-B
last-step theorem puts r at depth1/2; its reverse weight is>=1, whence the
target cap is2. In the unmarked branch the existing empty-V floor itself
is2. Thus F(target)=2 regardless of whether that target can be completed
as a fresh LOW source. No edge is pruned at a boundary.

Starting instead with an I_R edge gives x(r(A,M),C), M at LR, exterior
cuts LL=A and R=C and the left real child r. The same two mark branches
give I_L or empty V. This independently uses the actual right zig; it
does not reflect psi, weak-LE private witnesses, annotations or HIGH data.

The separate checker certifies both universal term identities, exterior
positions and preservation of an arbitrary middle root at depth2, including
an arbitrary marked descendant at depth3. These are substitutions in term
identities, not finite numerical tree tests or compiler execution.

## Signed preservation without a typed cap assumption

For any existing public Lambda<=D<=2, F=max(D,h_I) never lowers a target.
If a source is unchanged, the residual is its old residual plus a
nonnegative target increment. If it is raised, it belongs to I. Its H1
target has value2 by the endpoint derivation. Write the weight as w=s>=0
or w=-delta with 0<delta<=2. In the first case the raised source is2 and
the residual is s. In the second its value is2-delta and the residual is
-delta+2-(2-delta)=0. These exact polynomial identities are checked with
indeterminates. Consequently EVERY previously valid H1 row is preserved.

Every nonnegative I-source H1 row is directly valid, even if its old row
was unknown: h_I=2 forces both endpoints to2. Zero rows have residual0.
For a negative I-source row an arbitrary input D can exceed h_I; the
operation makes no unconditional claim there. With actual D_buried, the
already valid negative row gives D_buried(s)<=w+D_buried(t)<=w+2=h_I(s).
Only THEN may one infer F(s)=h_I(s), and its residual is0. This is a bound
on an actual edge, not a universal source cap imposed on typed boundaries.

Incoming nonnegative LOW rows to I2 have target2 and source<=2, and hence
are valid. The argument does not give arbitrary incoming rows to all I.
An unrestricted input D is not asserted globally LOW-feasible.

## H2 and hidden helpers

The completed original normal forms split H2 into Gamma0 and Gamma1.
Gamma0's actual-preterminal psi floor proves its LOW inequality for ANY
public psi<=F<=2. The proof remains valid if a DELETE or a core-prefix
operation exposes a marked descendant below M. No terminal-only-x claim
is used and no sum of helper/terminal B charges replaces original q.

For Gamma1 the first changing anonymous helper must be at source depth1/2
and in extreme gap0 or9. In I the only possible anonymous position there
is M: root and the marked child are Scores and every exterior path meets
a nonreal cut. A G reference reports a Score root, not an anonymous node.
If M is an actual anonymous root, child interval propagation makes its
rank strictly between PRESENT Score endpoints x,r. Fullrank agrees with
each present endpoint (Score uniqueness/exact cover), so inv._gapof counts
at least one Score below M and excludes at least one above it. Hence its
gap is in1..8. This contradicts Gamma1's extreme-gap condition, on either
orientation, regardless of whether mu marks r. No hidden-rank weak-LE
inequality is strengthened. Score-bearing versus Score-empty M support
does not matter. This closes all I-source H2 rows and proves preservation
of every formerly valid H2 row, using the unchanged-source argument elsewhere.

## Coverage, strictness and dependencies

The nine ordered-role construction in the theorem has an interior marked
pair x,r and a REAL middle node u above another marked node m. It has a
legal original A child access and a formal B path of length4, hence w=0.
It is outside Q, extremal-pair R, S and the later central-second-mark
guards. Compatible arbitrary private counts may occupy opaque cuts.
The argument is uniform over every admissible signature for which the
source has a witness; it does not require every signature to realize it.

Strict change of the CURRENT debt uses the already published Transfer01
helper_reset_2 B fact; no new psi query or core replay occurs. With marks
0,2,4,6,8, A middle1 real and marked2 at depth3, all old saturation guards
are false (Q's cuts fail; neither extremal pair is0/8; central4 is neither
the second nor second-largest mark). Its V={0}, so the completed psi0,
weight0,target-psi0 fact gives Lambda=D_buried=0, whereas h_I=2. This is
an analytic reuse of a completed fact, separate from the universal proof.
It does not claim any old row failed or a new signature was certified.

The proof dependency order is acyclic: original repaired semantics and
normal forms -> psi/negative-core and c/U/Lambda -> Q/R/S and successive
safe max operations -> completed D_buried negative H1 validity -> this
new max operation. Endpoint old-root depth and H2 normal-form/floor facts
are reused, not replayed. Existing HIGH/h0 glue applies at the same range
and totalizations. No premise is a global M3 feasibility assertion.

Full147-O/127-M states, SAME actual midpoint, independent private scopes,
free high v, weak LE, G, all unused raw fields, original H/q/prices and
h0(actual0,declared18,q9,w=-3) remain literal. No shared state quotient is
introduced. The guarded signed walk bound is-7, closed-walk bound0, using
the inherited HIGH bridge only when every LOW row has stated coverage.

Audit outcome: the mathematical derivation closes this restricted class
and the safe augmentation, with no additional open lemma introduced.
Global zero-weight LOW, other outside-S H1 source classes, remaining
shallow Gamma1 cheap transfers, full M3 and Dynamic Optimality remain OPEN.
No certified negative cycle or new whole-signature certificate is claimed.

R1-R4: one smaller public region, one explicit repayment mechanism, one
bounded symbolic audit and a real strict public-capacity increase. All
completed rows stay valid. Per-phase and cumulative caps are checked by
the controller/publication ledger. New finite tests=0.
