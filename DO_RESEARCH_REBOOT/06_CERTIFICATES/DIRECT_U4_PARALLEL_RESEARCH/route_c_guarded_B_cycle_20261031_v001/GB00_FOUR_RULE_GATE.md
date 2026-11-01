# Gate: derive a recurrent B cycle with at least five surplus units

2026-10-31, Asia/Karachi. The user narrows this turn to the source-exact B-cycle threshold for two one-StepEv resets. Matching-terminal work remains FROZEN. Old source/research/status/Git files and Stage 11G are read-only. All new outputs are exclusive to this fresh run. No larger finite key size, fitted coefficient, adaptive word change, A-policy hunt or automatic successor is authorized here.

## One exact source mechanism

Take a maximum guard r and B=r(U,V), where every U key is <r and every V key is >r. Query present x in U, then return to r. Let d be x's depth in U and u the root of U. Bottom-up source frames give

    q_x=ceil(d/2),
    q_return=1 iff d is odd and x<u; otherwise 0.

If d is even, or d is odd and x>u, the returned tree is r(S_x U,V). If d is odd and x<u, consume the inner local doubles but omit the final local left zig: the returned tree is r(U^-_x,V). Equivalently, if the full local splay is x(A,u(B,C)), then U^-_x=u(x(A,B),C). At d=0 the round trip is the identity and both double counts are zero. These cases must be proved with the actual parent-first LL/RR formulas, not inferred from a fit.

The guard return never contributes max(q-2,0). The query contributes

    max(ceil(d/2)-2,0),

so odd depth five already supplies one surplus unit. The invariant guard root and explicit parity recurrence form a determined source construction. Its purpose is to create real primitive B headroom, not to infer any A repayment theorem.

## Fixed input and fixed word

Use thirteen keys, as already audited. Start from the valid diagonal tree T0=13(R_[1,12],empty). No larger tree is evaluated. The fixed local query list is the prior four-bit-reversal order with the maximum guard removed:

    L=(1,9,5,3,11,7,2,10,6,4,12,8).

The only generator is the 24-request guarded word

    W=(K1,K13,K9,K13,K5,K13,K3,K13,K11,K13,K7,K13,
       K2,K13,K10,K13,K6,K13,K4,K13,K12,K13,K8,K13).

Iterate its B source map at whole-W boundaries, stopping at the FIRST repeated exact B tree or after 64 laps. Record every global query and guard return, and check the local parity identity at every pair. If no repeat occurs within the cap, record OPEN and stop without enlarging the cap or changing L/T0.

## Primitive-cycle extraction fixed in advance

Once a whole-boundary source cycle is found, decompose that closed source path by chronological loop erasure. Keep a stack of distinct B states and their source edges; whenever an edge returns to a stack state, emit the resulting simple cycle and pop that loop. Every emitted cycle is an actual source word with no repeated internal tree state. Every original edge is assigned once; their q and G_B sums are conserved across the decomposition.

Select the FIRST emitted simple cycle with G_B=sum max(q_B-2,0)>=5. The original source prefix to its stack starting occurrence supplies reachability. Replay that extracted word separately and verify exact closure. This canonical extraction is a source cancellation/normalization, not an optimizer or adaptive skeleton search. It prevents merely repeating or concatenating a previously low-budget loop to pass the threshold.

If no emitted simple cycle reaches five, the specific construction fails this gate's success criterion. Record it honestly and stop. A nonprimitive whole-word total of five is insufficient. Do not replace the word, seed, guard, threshold, decomposition or cycle order after the outcome. Reflection x->14-x is the only second orientation.

## Four rules before execution

1. **Strictly smaller — PASS.** One maximum-guard source recurrence, one fixed 13-key seed and 24-request word, one bounded orbit and canonical simple-cycle decomposition. All trees/words, larger n, A reset placement, potentials and global allocation are outside scope.
2. **Concrete reason — PASS.** The source parity/guard identities give exact returned shapes and costs, including an extra double at odd local depths. The fixed local query list drives that determined recurrence; exact tree repetition constructs closure. Loop cancellation preserves actual source inputs and produces primitive finite candidates. No floating plausibility or global feasibility witness is assumed; the construction may fail.
3. **One bounded campaign — PASS.** Prove the guard identity and audit this one construction, its exact cycle extraction, reachability, source events and reflection. No second independent open theorem, fit, source-graph optimizer, A search or automatic next generator is needed.
4. **Exact original obligation — PASS subject to the fixed threshold.** Success supplies one reachable simple recurrent B cycle with G_B>=5, removing the previously blocking B-only necessary budget for two resets of total four units PER THIS CHOSEN CYCLE. This proves only B headroom. It does not assert those A resets exist, yield E>C_D, preserve non-synchronization, or make FI strict over UD. Those remain separate original Step 3 obligations. The source example must not obtain success by period multiplication.

## Certification and stop

Pin all old artifacts and the complete 125-file Stage 11G inventory before execution. Preserve branch/HEAD/tracked state. Verify present keys, raw BSTs, all depths, source event cases/intervals/orientations, exact local-law checkpoints, first boundary repetition, decomposition edge multiplicity, every emitted cycle's simplicity, selected primitive closure and diagonal reachability prefix. Use the independent pointer source and reflect both states and events.

No B-surplus quantity is a new A credit pool. Two one-StepEv resets would supply four distinguishable actual units only when later constructed; no reset or FI/UD credit map is executed in this turn. Record BEFORE/RESULT/AFTER and the exact B-budget obligation removed or still open. Keep universal Step 3/CD OPEN. Preserve all old matching-terminal and Stage 11G statuses, and stop after this predeclared construction.
