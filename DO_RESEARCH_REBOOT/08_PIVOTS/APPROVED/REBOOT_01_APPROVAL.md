# REBOOT-01 approval record — equal-signature sibling erasure

Approval fixed before running the verification script or writing the completed proof.

CURRENT ORIGINAL PROOF NODE: arbitrary-depth SAME-CHILD inside ROW-DIAMETER, upstream of COARSE-DOUBLE.

EXACT THEOREM: Let B be any finite valid BST with root p and children T,S. Let u≠v belong to T, at the same edge-depth d≥1 in B. Let f_u,f_v be the coefficients of the top fringe F_(d−1) in the source fold for those two rows. If f_u=f_v, then for every globally shared real assignment j(tau), rho(c), D_J([p,T,S];u,v)=D_J([p,T,empty];u,v). The mirrored theorem holds with T on the right. No restrictions on S's size, shape, or depth. The root, T, and keys of T remain fixed during erasure. Order-preserving relabeling is allowed. In particular, all such pairs with odd ambient depth d qualify (f_u=f_v=1).

RULE 1 — PASS. Removes the entire independent sibling subtree for a strict, nonempty class of pairs; does not prove arbitrary-T width or construct J.

RULE 2 — PASS. The fold is path-only, so old coefficients, depths, slots, and root tokens are unchanged by sibling insertion. Each sibling key contributes the same tau to both equal-signature rows; the static contribution and 4|S| terms also cancel. Principal mechanism: exact algebraic cancellation.

RULE 3 — PASS. Bounded source audit: wp6_staticR.py, wp6_lambda.py, wp6_j4shared.py. Prove insertion formula, identical-signature cancellation, and mirror. Verify coefficient multisets with integer arithmetic on a bounded corpus. This requires no independent open lemma.

RULE 4 — PASS. Deletes quantification over arbitrary S from the equal-depth/equal-top-coefficient SAME-CHILD cases in the original row obligation, reducing them to S=empty under the same J. Does not delete the empty-sibling base inequality. No located source contains a completed universal theorem covering this class (context scripts are finite probes).

PREVIOUSLY PROVED PREMISES: Source definitions of R_static, R_coeffs, slots, tau4, and H0. R=c+sum lambda follows directly from the identical fold used by R_static/R_coeffs, with disjoint fringe/child blocks. The path and slot partition are elementary tree facts; their proof will be included rather than assumed from finite tests.

NEW HYPOTHESES: Only the stated geometric subclass restriction d_u=d_v, f_u=f_v. No UG, no rho=c, no NONE quotient, no witness-existence premise. The theorem is valid for arbitrary shared j,rho.

SOURCE LOCATIONS: scripts/wp6_staticR.py:21-131; scripts/wp6_lambda.py:49-104; scripts/wp6_j4shared.py:36-100,110-166. Exact source hashes will be retained with the verification output.

PROOF PLAN: Recover full row sum including root token and repeated atoms. Compare B with B0 preserving root/child orientation. Prove all old rows and root tokens fixed. Sum the sibling contribution explicitly. Deduce cancellation for equal signatures and the odd-depth corollary. Mirror by exchanging left/right in the fold maps.

NONVACUITY WITNESS: p=80, T=[40,[20,[10],[30]],[60,[50],[70]]], u=10,v=30, S arbitrary with keys>80. Both nodes have ambient depth 3. Also extend a fixed T by arbitrary one-child ancestors to realize arbitrarily large qualifying depths. Mirror the witness.

EXPECTED OUTPUT: One universal restricted-domain proof; integer coefficient verification; exact domain/mirror checks; advancement report identifying deleted sibling quantifiers and remaining base/global obligations.

FAILURE STANDARD: A valid tree in the stated domain with a nonzero complete difference form, or an omitted old-key/root contribution, or failure of the top-fold equality at odd d. On failure do not introduce a new J system.

APPROVAL: PASS (all four rules). This is internal authorization under the master directive, not a request for additional user permission.
