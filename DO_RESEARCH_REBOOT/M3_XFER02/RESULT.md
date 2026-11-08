# Cut-separated marked pair: new LOW-safe repayment theorem

A larger class beyond opaque two-core Q is proved and independently
symbolically audited. It allows newly exposed anonymous/unmarked nodes
and includes Score-bearing H2/Gamma1 helpers. No finite tests were run.

The two smallest marked keys a<b are separated from all other marked
keys by an observed PORT at b.right. Root b may have a at L or LR;
root a may have b at R. Include the order-dual for the largest marked
pair and a.left PORT. These guards use only the frozen shared state.

Set h_R=min(2,w_x+2) on this region R,0 elsewhere. For EVERY public
psi<=D<=2, max(D,h_R) preserves each previously valid ORIGINAL LOW
inequality, including Score-bearing helpers. It assumes no globally
feasible D. This is stronger than an H1-only augmentation.

The explicit D_R=max(D_Q,h_R) satisfies ALL LOW edges with source in
Q union R. Outside E1, unique-target B depths4/5 give debt2 and safe
zero-weight exits/incoming0/+1 transfers; depths6/7 give debt1 and
safe incoming+1 transfers (zero incoming requires source<=1).
The proof permits fresh anonymous exposure while the separating port
remains observed. A new symbolic B lemma bounds the entry core's
depth by3 after an extreme helper and a different core access, giving
the required destination debt2. Actual H2,H/q/weights are unchanged.

The existing HIGH glue gives finite walks>=-7 and fully closed walks>=0
when every LOW source lies in Q union R. This is a RESTRICTED DOMAIN
theorem for arbitrary compatible signatures. It does not prove all
remaining transfers or M3. Cases with the cut below the visible shadow,
additional marked targets, and other non-Q/non-R sources remain OPEN.
No new whole-signature certificate or original negative cycle is claimed.

See CUT_PAIR_THEOREM.md and PROOF_AUDIT.md. The independent audit checks
six H1, eight allowed helper and four excluded helper schemas (including
duals), arbitrary-depth B parity/order branches and signed residuals.
Analytic nonvacuity includes a Score-bearing helper family with weights
0/+1 outside E1/Q; no new finite source/root test or label lookup is used.
Source semantic dependencies are reused; this is not a full compiler
formalization. All previous completed checks are preserved, not replayed.

R1-R4/current caps, weak LE/G/unused fields, full147-O/127-M closure,
independent witnesses/SAME midpoint/free high v and corrected h0 remain.
All13565 pinned prior files and Git HEAD/tracked tree are unchanged.
New charged CPU=0.359375; cumulative=756.859375/7200s; remaining=6443.140625
including reserve5. New finite tests/source queries/root evaluations=0.
Full M3 and Dynamic Optimality remain OPEN.
