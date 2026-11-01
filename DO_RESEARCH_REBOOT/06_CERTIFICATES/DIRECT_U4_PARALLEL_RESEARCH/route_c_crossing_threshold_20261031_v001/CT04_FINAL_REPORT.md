# Structural crossing potential fails universal B repayment

A concrete potential outside the previously excluded monotone-combination bracket satisfies universal DELETE but fails B repayment on four keys. Step 3 remains open. The four-rule gate was applied before the bounded source audit; no larger finite fit was run, and Stage 11G is preserved.

The tested function counts proper A-subtree intervals whose boundary chords cross at least two proper B-subtree chords:

    H2(A,B)=sum_{I in C0(A)} indicator(b_B(I)>=2).

One primitive A rotation changes just one summand. Hence, for arbitrary sizes, shapes and fringes,

    Delta_DELETE H2 <= d_A <= 2a.

This is an analytic universal A-law proof. The full construction uses current tree incidence data and is outside the old Ehat<=T<=F bracket: at the counterexample source H2=1, Ehat=2 and F=3.

The full B law fails at

    A=4(2(1,3),empty), B=R4, KEEP 4.

A is already rooted at 4, so a=0. B has one double and one final zig: q=1,z=1. The crossing degrees on A intervals {1},[1,3],{3} change

    (1,3,1) -> (2,0,1).

The counted conflict shifts from [1,3] to {1}; H2 remains 1. Thus Delta H2=0, whereas the source bound requires at most -1. This rejects the whole source law, not an additional micro-step condition.

The frozen three- and six-key controls also exclude every fixed positive-integer crossing threshold Hk. This class exclusion does not cover size-dependent thresholds, weighted profiles or arbitrary structural potentials. No successor candidate was launched after the failure.

The independently checked closed word

    D4 D2 D4 K4 K1 K2 K3 K4 K3 K2 K1

starts and ends at the actual diagonal pair (R4,R4), reaches the counteredge, and has A=12,Q_B=2,Z_B=8. It satisfies Coarse-Double; it is a counterexample to the proposed potential only. The audit checks 17 full source rows, reflected controls and 525 chord comparisons with multiplicity. No pair-state graph, fitting, installation, Git mutation or Stage 11G computation occurred.

No original CD obligation was discharged. The diagnostic result is precise: an independently counted structural conflict can be removed at one A boundary and recreated at another during an otherwise successful B access. The missing step is an explicit construction that controls such transfer while retaining both universal source bounds. That construction has not been supplied or assumed.

Details: [written gate](CT00_FOUR_RULE_GATE.md), [definition and universal DELETE proof](CT01_STRUCTURAL_DEFINITION_AND_DELETE.md), [exact B obstruction and threshold corollary](CT02_EXACT_REPAYMENT_OBSTRUCTION.md), [strategy review](CT03_STRATEGY_REVIEW.md), [source certificate](crossing_certificate.json), [independent audit](independent_audit.json), [proof-status ledger](proof_status_ledger.json) and [final preservation checks](final_integrity.json).
