# An explicit unbounded correction fixes DELETE but loses B repayment

An explicit unbounded correction R to P cancels the root-changing DELETE drift and proves the full universal DELETE bound. It does not satisfy full B repayment: a zero-double B zig raises the corrected potential by one. Step 3 remains open.

The construction is

    J(A,B)=max_T[P(T,B)-rho(A,T)], R=J-P,

where rho is unit primitive rotation distance and T ranges over present same-key trees. It is a defined finite current-state maximum, with no fitted labels or future-access premise. Triangle inequality proves universally

    |Delta_A J|<=rho(A,A') and Delta_DELETE J<=d_A<=2a.

Moreover P<=J<=F. On the root-drift family for every n>=4, the correction changes n-4->0, reducing the old n-3 DELETE drift to +1. Thus R is genuinely unbounded and the registered DELETE failure is repaired.

The same source with KEEP1 has a=0,q=0,z=1. Exact global maxima over ALL auxiliary trees give

    J_source=n-3, J_destination=n-2,
    Delta J=1>0=2a-q.

At six keys, DELETE6 is repaired by P=1->4, R=2->0 and J=3->4 within budget 2. KEEP1 instead has P=1->1, R=2->3 and J=3->4 against budget 0. The correction revives the auxiliary-root alignment problem.

The same two operations prove more: for max_T[P(T,B)-lambda_n rho(A,T)], DELETE at n=6 forces lambda_6<=2, while the B zig forces lambda_6>=4. No nonnegative scalar penalty works, even when chosen separately for each size. This exact class obstruction excludes neither other penalties nor arbitrary unbounded corrections.

The four-rule gate was written before execution. Analytic extremal bounds settle the envelope without a fit, auxiliary-tree enumeration or graph search. Independent verification checks eight hand matching/cover certificates, one-zig distance witnesses, both orientations and 22 full source rows including an 18-access closed paired replay. The walk has A=18,Q_B=0,Z_B=12 and is not a Coarse-Double counterexample.

No original CD obligation was discharged. The failed mechanism stops under the gate; no successor existence premise is introduced. All 164 inherited/source pins and all 125 Stage 11G final-closure files are checked again at delivery.

Details: [four-rule gate](PE00_FOUR_RULE_GATE.md), [explicit correction and universal DELETE proof](PE01_EXPLICIT_CORRECTION_AND_DELETE.md), [exact extrema and coefficient obstruction](PE02_EXACT_EXTREMA_AND_B_OBSTRUCTION.md), [reachable closed replay](PE03_SOURCE_REPLAY_AND_VERIFICATION.md), [strategy review](PE04_STRATEGY_REVIEW.md), [source certificate](p_envelope_certificate.json), [independent audit](independent_audit.json), [status ledger](proof_status_ledger.json) and [preservation checks](final_integrity.json).
