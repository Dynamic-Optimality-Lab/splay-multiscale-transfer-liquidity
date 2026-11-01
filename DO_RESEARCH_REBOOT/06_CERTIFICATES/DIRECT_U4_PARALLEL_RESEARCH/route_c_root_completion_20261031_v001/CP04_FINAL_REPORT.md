# Root completion retains equal root reserve and pays B but fails DELETE

An explicit joint correction now retains unbounded reserve on equal-root pairs and satisfies the full universal B bound exactly. It fails universal DELETE on an analytic odd-size family, so no correction satisfying both bounds was obtained. Step 3 remains open.

The fixed construction is

    Phi(A,B)=F(A,S_root(A) B)+floor(d_B(root(A))/2),
    R(A,B)=Phi(A,B)-P(A,B).

This evaluates one source B splay at the current A root; it is not an envelope, B-only gauge, future-history oracle or fitted potential. The completion is a potential evaluation and does not execute B during DELETE.

For A rooted at x, both sides of an actual B splay use the same completed tree S_x B. Its completion double count changes q->0. Therefore Delta_B Phi=-q for every finite pair and every fringe shape, with both orientations covered. On equal-root pairs R=F-P=mu_r, so the prior JA family retains R=n-3. The old six-key equal-root DELETE is now paid with Phi=4->4, and the starved helper has Phi=5->3 with q=2.

The new failure uses a LEFT-vine middle:

    A=1(empty,n(L_[2,n-1],empty)), B=R_n, DELETE n.

For every odd n>=7, the actual operation is one A zig with budget2. The source and destination completed-pair F values are both n-2, while the completion double count changes 0->(n-1)/2. Thus

    Delta_DELETE Phi=(n-1)/2>2.

At seven keys Phi rises5->8. The same equality of terminal F values excludes every arbitrary size-dependent scalar replacement f_n(F_terminal)+Q. It does not exclude richer joint terminal functions or general corrections.

The written four-rule gate was applied before execution. Independent verification checks twelve matching/cover equalities, twenty-seven full source rows and eighty-one potential-completion evaluations, including a closed paired replay with A=27,Q_B=0,Z_B=12. That walk is not a Coarse-Double counterexample. The only new connector search is a fixed seven-key single-tree reachability check for the analytic witness; it fits no potential values. No finite potential fit or source-pair graph was run. All193 inherited/source pins and all125 Stage 11G final-closure files are checked at delivery.

No original CD obligation was discharged. Full B repayment alone cannot be combined with another potential's DELETE theorem. The failed mechanism stops under the gate, with no replacement existence premise.

Details: [four-rule gate](CP00_FOUR_RULE_GATE.md), [explicit correction and universal B proof](CP01_EXPLICIT_CORRECTION_AND_UNIVERSAL_B_LAW.md), [all-odd DELETE and terminal-statistic obstruction](CP02_ALL_ODD_DELETE_AND_TERMINAL_CLASS_OBSTRUCTION.md), [strategy review](CP03_STRATEGY_REVIEW.md), [source certificate](root_completion_certificate.json), [independent audit](independent_audit.json), [status ledger](proof_status_ledger.json) and [preservation checks](final_integrity.json).
