# EXP-03 theorem and refutation ledger

Status terminology: PROVED below means a same-agent mathematical derivation from the explicitly inherited sequential-access and three-slot interfaces. It does not mean formal verification or an independent theorem audit. FINITE EXACT means a saved, paired-closed original source checked by the inherited oracle and immutable tuple transition engine. No numerical coefficient for C_seq is invented.

## T1. Distinct original parent interface — PROVED, independently checked finitely

For the fixed EXP-02 residual, retain the original source, operation and StepEv identity of the consuming B double. Partition those occurrences into omitted unsynchronized O, retained without a common grandparent G, and outside the selected cover X. These three sets are disjoint: cover membership and retained/omitted status are fixed per operation, and grandparent matching is fixed per original parent. Several gaps with one parent are demands of that same occurrence, not additional parents.

The inherited original three-slot lemma gives

`R_unhandled <= 3 (|P_O| + |P_G| + |P_X|)`.

This statement supplies no A budget. In the inherited 171 sources it is 14 gaps, 11 distinct parents: O has 10 gaps/7 parents and G has 4 gaps/4 parents. The two repeated sources are separate original sources; occurrences from them are never merged.

## T2. Complete equality excludes a neutral consumer — PROVED

At KEEP x, original A finishes at root x before B starts. Every real B rotation loses a proper S-subtree label containing x and creates the demoted pivot's label, which excludes x. The pivot and promoted key lie on a genuine B access path, hence in S. The proper lost label cannot be present in A: its only S-subtree containing its root x is the full carrier S.

The newly created demoted label persists through the rest of this splay. In a same-side double, the first demoted g remains below the subsequently demoted p; in an opposite-side double the first demoted p remains attached to x while the second rotation demotes g. Later doubles move x above higher ancestors without changing these completed off-path components. A terminal zig has the same property.

If complete A=B after this KEEP, every such output label is present in the fixed post-A tree. Each B bit therefore has SET sign -1, by the original set-difference definition. Thus a fully neutral original parent, in particular an unhandled R6 parent, cannot finish at a complete equality boundary. This argument covers private physical nodes and all source populations; it uses carrier labels only for genuine B path vertices.

## T3. Actual discrepancy episodes have a globally disjoint A budget — PROVED

Test complete A/B equality at original operation boundaries. If the source's initial pair is equal, traverse from its designated cut; otherwise, if some post-operation pair is equal, traverse one lap starting just after the earliest such equality. Each maximal unequal component begins with the first unequal post-operation pair after equality and includes its first subsequent equality-closing operation. If the complete cyclic period never reaches equality, use its entire designated lap as one persistent component. No component is assumed to be a paired-closed source on its own, and common trees at different endpoints need not agree.

Every original operation belongs to at most one episode. Assign its genuine A StepEv to that episode, including all DELETEs and closing work. The sets are disjoint, so `sum_E A(E) <= A(W)`. T2 places every unpaid consumer in one of these components. Persistent components handle arbitrary legal nondiagonal starting pairs and the cyclic seam. These results do **not** prove `|P(E)| <= c A(E)`; that would still be an unpaid substantive assertion.

## T4. Equality-restarted common-grandparent comparison — PROVED quantitative partial result

Use the one original EXP-01 orientation, unchanged: increasing iff `2 rank_S(root B_initial) < |S|`, with zero-based rank; empty S is increasing. Fix this orientation once for the whole source. Within each T3 episode, form chronological constant-target KEEP blocks. Start at its first block, without wrapping across the episode's end. At an eligible anchor `min S` (or `max S` in decreasing orientation), greedily retain the next required S rank, including all its repeated occurrences, and omit intervening KEEP blocks. Take the maximal attained prefix. Accept it only when its complete initial B path union J has those targets as its extreme-anchored consecutive ranks and `ell >= ceil(|J|/2)+1`. Advance past the whole accepted span, or advance one block after rejection. Source operations and R6 demands do not participate in selection. Actual B initializes each accepted shadow; only retained original targets are executed in that separate comparison.

The initial path union J is ancestor-closed. Splaying retained targets in J changes only its internal search skeleton and component attachment edges; it does not change the internal structure of attached outside components. Consecutive J ranks from its extreme can be mathematically completed to a full sorted scan of J. The inherited sequential-access interface and nonnegative costs give `Q_shadow <= C_seq |J|`, including any internal terminal zig convention as in EXP-02. No completion operation becomes original work.

For each successive pair of distinct retained blocks, take the original interval from the previous block's last post-A time through the next block's first post-A time, inclusive only at the right. Its A roots differ, so it contains at least one original A StepEv. Choose its first bit0. These intervals are disjoint within a window; different selected spans and different episodes have disjoint interiors, including when the source seam is crossed. None borrows the incoming gap of another episode. Thus all chosen `(source,t,j)` A occurrences are distinct. Since `|J| <= 2(ell-1)`,

`sum_windows |J| <= 2 sum_windows (ell-1) <= 2 A(W)`.

Define R_restart as the literal subset of **old unhandled gaps** whose original parent has a shadow double at that same retained operation with the same labelled old grandparent in this restarted system. A different frame or different StepEv ordinal is allowed; a different grandparent is not. Within a splay each old grandparent is used at most once, because its completed demoted component remains off x's remaining upward path. Consequently distinct original parents inject into distinct shadow doubles, and the original three-slot lemma bounds each image by three gaps. Therefore

`R_restart <= 3 sum Q_shadow <= 6 C_seq A(W)`.

Let `R_* = R_unhandled \ R_restart`, without changing any old ownership or source predicate. Then

**`Q_B <= (35 + 36 C_seq) A + R_*`.**

This is source-uniform payment of a newly defined subset. It is NOT a theorem that all Type G, O, or X events belong to it. The inherited four G gaps belong to it by exact replay; the ten inherited O gaps do not.

## T5. Exact grandparent-set distortion identity — PROVED and checked

Uniqueness of old grandparents within each actual or shadow splay identifies the number of doubles with the cardinality of its grandparent set. Hence at each retained operation, `q_actual-q_shadow = |G_actual\G_shadow| - |G_shadow\G_actual|`. Summing gives `delta = sum(L-M)`. There is no matching to a different labelled grandparent and no A credit from this signed equality. EXP03_GRANDPARENT_SET_AUDIT.json records the actual sets for the checked windows.

## R1. Outside-window consumers are impossible — REFUTED, FINITE EXACT

Xprobe_p4_L3_hitNone_boundary1 is a complete 65-key common-diagonal source, A=261, Q_B=110. Its gap `(197,(137,3),(145,1))`, original parent `(197,2)`, g=48, target63, is in the unchanged R6_other and outside both paid EXP-02 classes. The canonical comparison covers the initial ascending scan, not this later short decreasing wave. The full closing decreasing scan and final KEEP2 restore both physical trees to the saved common initial state. Larger/reflected controls are saved. A zero X count in EXP-02 was not a universal exclusion.

## R2. The last A ancestry-loss selector is injective — REFUTED, FINITE EXACT

In mixed_p5_Gcopies2, A=1793 and Q_B=712, original G parents `(785,2)` and `(793,2)` both have g=34 and targets11 and19, respectively. Both select the same real rotation `A(740,1,0)` as their most recent cyclic A loss of `(g,target)` ancestry. Each consumes a distinct old genuine residual gap. The complete two-period version repeats the collision at parents `(1301,2)` and `(1309,2)`, selecting `A(1256,1,0)`. These are physical occurrences, not a repeated vertex-label counting error.

The first collision suffices to reject unit injectivity. It does not disprove a larger absolute load bound; no such bound is established here. The signed SET identity cannot turn this rotation into two credits without an additional theorem. Full words, relation changes and original parent certificates are saved.

## R3. Unit-weight ancestry disagreement changes by O(1) per A StepEv — REFUTED parametrically

On the complete common right vine `[n]`, the first original DELETE2 rotates1 below2. A loses `(1,x)` for every x=2..n and creates `(2,1)`. B has not moved. The symmetric difference of ordered physical ancestor relations jumps from0 to n, for exactly one A StepEv. This is the first operation of the exactly paired-closed omitted-hit family for all n=2^(p+2)+1, p>=3. Thus a population-independent Lipschitz bound on this unweighted mass is false. A normalized or weighted alternative would require its own original residual/payment argument and is not supplied.

## R4. Sparse-key relabelling preserves full paired closure — REJECTED CONSTRUCTION

The first separated-private attempt restores A's even spine with odd leaves but changes B's complete physical tree. Its legal prefix does not repair its measured-period closure. It is explicitly excluded from all admissible-source totals and counterexamples. Closed-private variants include actual physical preparation and a full closing scan, and warmed variants retain their actual reaching prefix and detected exact paired cycle. See EXP03_REJECTED_CONSTRUCTIONS.json.

## Open debt, without relabelling the target

R_* remains the exact old unhandled complement of T4. Maximal actual mismatch episodes cover its consumers and have disjoint A budgets, but a local bound on their remaining parent counts has not been proved. Raw comparison divergences have a separate namespace and may overlap; disjointness in tested examples is not an all-source overlap theorem. Merging their spans can remove budget duplication, but it does not prove a demand bound for the merged component.

There is no proved absolute C3 for the entire R_unhandled, no unrestricted Universal Relaxed Coarse-Double conclusion, and no refutation of that universal target. The valid verdict is a quantitative partial pass plus targeted refutations of R1–R3.
