"""Save the completed bounded repair audit exclusively in this append-only run."""
from pathlib import Path
import json,hashlib

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def put(name,text):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f:f.write(text.strip()+'\n')
def js(name,value):put(name,json.dumps(value,indent=2))

def main():
    audit=json.loads((OUT/'independent_audit.json').read_text(encoding='utf-8'))
    assert audit['status']=='PASS'
    lemma=ROOT/'DO_RESEARCH_REBOOT/02_PROVED/26AL_generalized_signed_repayment.md'
    js('additional_source_pins.json',{'files':{lemma.relative_to(ROOT).as_posix():hashlib.sha256(lemma.read_bytes()).hexdigest()},
       'timing':'Source lemma read and pinned during this audit; the ten entry inputs are separately pinned in entry_source_pins.json.'})
    js('external_source_record.json',{'url':'https://arxiv.org/html/1907.06310v3#S3',
       'title':'A Foundation for Proving Splay is Dynamically Optimal','authors':['Caleb C. Levy','Robert E. Tarjan'],
       'version':'arXiv:1907.06310v3, 2022-05-09','access_date':'2026-10-31',
       'passage':'Theorem 3.4 and its proof, HTML lines 128-135',
       'use':'For n>=4, any same-key BST can be transformed to any other by present-key ordinary Splay requests. Only reachability is used; no cost constant enters a potential inequality.',
       'distinction':'The paper measures depth in nodes. This audit measures depth in edges. The reachability statement is independent of that convention.'})
    put('AL01_ROOT_PINNED_B_LAW.md',r'''
# Root restriction preserves the uniform B repayment law

The explicit root-pinned envelope preserves access-root alignment and repays every starved B access, on every finite key set. This is one component law. DELETE fails for the same function, as proved in AL02.

## Source definitions and the two required laws

All trees are finite ordered BSTs on the same nonempty set of present keys. Depth counts edges. KEEP x first splays A, then B. DELETE x splays A and leaves B fixed; no BST node is removed. Write S_x for ordinary source bottom-up splay, a=ceil(d_A(x)/2), q=floor(d_B(x)/2) on a KEEP, and q=0 on a DELETE.

A complete repair Psi must obey

    Psi(S_x A,B)-Psi(A,B) <= 2 ceil(d_A(x)/2),                 (DELETE)
    Psi(A,S_x B)-Psi(A,B) <= -floor(d_B(x)/2), root(A)=x.     (B repayment)

The A-then-B order then gives Delta Psi <= 2a-q on every whole KEEP as well as every DELETE. On a closed source walk these differences telescope exactly to zero, giving Q_B<=2A, the original Universal Coarse-Double obligation that a complete candidate would discharge. No endpoint-growth premise is needed for that closed-walk implication. The second line is itself a legal whole KEEP when A is already rooted at x. Both tests below therefore use whole source operations.

Fix r=1/8 and the undirected unit primitive rotation distance rho. Define

    G(A,B) = sum_y r^{d_A(y)} d_B(y),
    U(A,B) = max_T [G(T,B)-rho(A,T)],
    L(A,B) = max_{root(T)=root(A)} [G(T,B)-rho(A,T)].

All maxima are over actual BSTs on the same keys. There are finitely many of them; the restricted set contains A. Thus these are explicit finite, nonnegative, well-defined functions, with no unknown labels or future-history oracle. U>=L>=G. The one-key case gives G=L=U=0. Empty trees have no present-key operations and may be assigned value zero.

## The source displacement bound

The banked source lemma 26AL-L1 states that under one entire B splay at x, every y!=x satisfies d_{S_xB}(y)-d_B(y)<=2. Its source is DO_RESEARCH_REBOOT/02_PROVED/26AL_generalized_signed_repayment.md, with the bottom-up frames in python/independent/splay.py and the pointer rotations in python/liquidity/legacy_embedding.py.

The reason is local and independent of n. For an LL double, write its old tree g(p(x(t1,t2),t3),t4); its new tree is x(t1,p(t2,g(t3,t4))). Relative depth changes for x,p,g are -2,0,+2, and those for the four entire fringe subtrees are -2,-1,+1,+2. For an LR double g(p(t1,x(t2,t3)),t4) becoming x(p(t1,t2),g(t3,t4)), the changes are -2,0,+1 for x,p,g and 0,-1,-1,+1 for the fringes. RR and RL are their reflections. A final zig increases any non-target depth by at most one. Once a key has entered the rebuilt x subtree, later double operations move its location by -2 or -1, and a later final zig by -1 or 0. Thus a non-target can suffer its at-most-two increase only once; later operations cannot accumulate positive displacement. Arbitrary internal fringe shapes merely share the slot displacement.

## Root-conditioned repayment for G

For every binary T,

    W(T)=sum_y r^{d_T(y)} < sum_{j>=0}(2r)^j = 4/3.

If root(T)=x then the weight at x is one, and the remaining mass is less than 1/3. Let d=d_B(x). For d>=1 the displacement bound gives

    G(T,S_xB)-G(T,B) <= -d + 2 sum_{y!=x} r^{d_T(y)}
                        <= -d+2/3
                        <= -floor(d/2)-1/3.

The last inequality follows from d-floor(d/2)=ceil(d/2)>=1. For d=0 the B tree is unchanged. Both orientations and every present key are covered.

## Passing the law through the restricted maximum

Suppose root(A)=x. During the B phase A is frozen. The feasible auxiliary set in L is exactly the same before and after B, and EVERY auxiliary T is rooted at x. The penalty rho(A,T) also stays fixed. The preceding bound therefore holds for every term in that same maximum, with a common right-hand side. Taking maxima proves, for d>=1,

    L(A,S_xB)-L(A,B) <= -floor(d/2)-1/3.

For d=0 the difference is zero. This proof does not need a common maximizer, a latest setup, a bound on overwrite count, or any finite fringe bound. The B consumer is paid irrespective of its earlier setup history. It does not bound L's motion during those setups or during the A phase of a non-starved zero-weight helper.

The unrestricted U has the DELETE law because it is 1-Lipschitz in A: each term is, by the triangle inequality for rho, and its feasible set is fixed. A splay uses exactly d_A(x) primitive rotations, so Delta U<=d_A(x)<=2a. The restricted L loses this argument as soon as the A root changes: the feasible set itself changes. AL02 proves that this loss is unavoidable for this construction.
''')
    put('AL02_DELETE_BAND_OBSTRUCTION.md',r'''
# A single root change refutes normalized root envelopes

Root restriction preserves B repayment but leaves an unbounded DELETE increase. The obstruction is analytic in n and applies to every internal middle-tree shape.

## One source family and one legal DELETE

For any n>=6 let M be any ordered BST on keys 2 through n-1. Put

    A = 1(empty, n(M,empty)),
    B = 2(leaf 1, right vine on 3 through n),
    A_d = S_n A = n(1(empty,M),empty).

DELETE n is one primitive A zig: d_A(n)=1, a=1 and q=0, so its allowed increase is 2. In B, d_B(1)=1, d_B(n)=n-2, and every depth is at most n-2. The M keys retain their A depths in this zig.

For raw G the only changed weights are at keys 1 and n. Therefore the exact increase is

    G(A_d,B)-G(A,B) = (1-r)(n-3) = 7(n-3)/8.

This already exceeds two at n=6. Any additive repair Psi=G+R satisfying this DELETE must therefore have

    R(A_d,B)-R(A,B) <= 2-7(n-3)/8.                       (1)

Thus a correction with a uniformly bounded oscillation in A cannot repair G. A B-only additive gauge cancels on DELETE. Inequality (1) is a necessary condition, not a construction of R.

## The root-pinned envelope

Every source candidate T in L has root 1. Its root contribution to G is one; all other weights sum to less than 1/3. Nonnegative metric penalties cannot increase a score. Hence

    L(A,B) <= 1+(n-2)/3.

At the destination, T=A_d is allowed, and its penalty is zero. Its root contribution alone is n-2. Consequently

    L(A_d,B) >= n-2,
    Delta_DELETE L >= ell(n) := (2/3)(n-2)-1 = (2n-7)/3.  (2)

For every n>=7, ell(n)>2. This proves an unbounded family of actual DELETE violations, without evaluating L on larger finite graphs. The saved six-key metric certificate gives the additional exact boundary violation Delta L=21/8>2 at n=6; it is stronger than the loose analytic lower bound ell(6)=5/3.

## The normalized envelope class excluded by the same bounds

Let C(A,T,B)>=0 be any finite penalty with C(A,A,B)=0. Replace rho by C in either

    F_max(A,B)=max_{root(T)=root(A)} [G(T,B)-C(A,T,B)],
    F_min(A,B)=min_{root(T)=root(A)} [G(T,B)+C(A,T,B)].

For F_max, the source upper bound uses C>=0, and the destination lower bound uses the self-term. For F_min, every destination term has at least its root contribution, while the source self-term is an upper bound. Both functions consequently obey the same two endpoint bounds used in (2), and both fail DELETE for n>=7. No property of a metric, B independence, or fixed coefficient is required for this corollary. Extended penalties may also be allowed if the expressions are well-defined and the zero self-term remains available.

More generally, the same source family rejects any F lying in the band

    d_B(root(A)) <= F(A,B) <= d_B(root(A))+(max_y d_B(y))/3,

even after adding a B-only gauge. Adding a joint correction whose oscillation over A at fixed B is bounded by an absolute K only weakens (2) to ell(n)-K, which still exceeds two for sufficiently large n.

This does not rule out all root-aligned potentials. A correction whose changes grow with n, a state-dependent combination, or a function outside this root-depth band need not satisfy these endpoint estimates. None is constructed here.

## Admissibility from a diagonal and closure

Theorem 3.4 of [Levy and Tarjan](https://arxiv.org/html/1907.06310v3#S3) guarantees a present-key splay sequence between any two same-key BSTs with n>=4. Starting at any diagonal (T0,T0), a common KEEP sequence first reaches (B,B); a DELETE sequence then changes A from B to the displayed A while B stays fixed. The tested DELETE is therefore reachable from the prescribed diagonal. A DELETE sequence from A_d back to B and a common KEEP sequence from B to T0 close the walk exactly.

Only this reachability theorem is used, not its cost constant or a node-depth convention. The counterexample refutes a potential inequality on a genuine source edge. It does not assert that the entire closed walk violates Coarse-Double. The fixed n=6 word in AL04 establishes its own reachability and closure directly through both source engines.
''')
    put('AL03_SIZE_DEPENDENT_BLEND_NO_GO.md',r'''
# Every size dependent convex blend fails the two required laws

For each n choose any theta_n in [0,1], held fixed over all states and operations of that size. Define the registered family

    P_theta(A,B) = (1-theta_n)L(A,B)+theta_n U(A,B).

No sequence of such coefficients satisfies both the DELETE and B-repayment inequalities on all sizes. In fact, for each n>=13 no coefficient works even on the following two operations from the SAME source state. This is an analytic obstruction; no coefficient or larger finite system was fitted.

## The second operation from the source family

Use the A,B of AL02, and KEEP 1. A is already rooted at 1, so a=0. B has 1 at depth one, giving q=0 and z=1. The B zig gives the right vine on 1 through n, denoted B_k. This whole KEEP has budget 2a-q=0.

Key 1 rises one B level and every other key descends one B level. For every auxiliary tree T, the exact difference is

    G(T,B_k)-G(T,B) = W(T)-2r^{d_T(1)},
    W(T)=sum_y r^{d_T(y)}.

If T is rooted at 1, then 1<=W(T)<4/3, so every such term changes by an amount between -1 and -2/3. The penalty and feasible set in L stay fixed. Maxima preserve both common bounds, proving

    -1 <= Delta_KEEP L <= -2/3.                            (3)

## The unrestricted envelope moves the other way

Every auxiliary T rooted at 1 has source score at most 1+(n-2)/3. But T=A_d is one primitive rotation from A and has G(T,B)>=n-2, so

    U(A,B) >= n-3 > 1+(n-2)/3, for n>=6.

Therefore EVERY source maximizer T* in U has root different from 1. Its weight at 1 is at most r, while W(T*)>=1. Keeping that same maximizer at the destination gives

    Delta_KEEP U >= 1-2r = 3/4.                            (4)

This reuses a source maximizer; it does not require it to maximize after the operation. It is the same all-size U failure proved in the preceding audit, included here to make the tradeoff explicit.

From (3)-(4),

    Delta_KEEP P_theta >= -(1-theta_n)+(3/4)theta_n
                       = -1+(7/4)theta_n.

Nonincrease on this KEEP therefore NECESSARILY implies

    theta_n <= 4/7.                                        (5)

This necessary inequality is not claimed sufficient for any other edge.

## DELETE requires an incompatible coefficient

The DELETE n of AL02 changes A by one primitive rotation. U is 1-Lipschitz in A in BOTH directions, hence Delta_DELETE U>=-1. Combining this with (2),

    Delta_DELETE P_theta >= (1-theta_n)ell(n)-theta_n.

For n>=6 the right side decreases with theta_n. Condition (5) consequently forces

    Delta_DELETE P_theta >= (3/7)ell(n)-4/7
                         = (2n-11)/7.

For every integer n>=13 this is at least 15/7>2, contradicting the DELETE budget. Equivalently, the DELETE necessary bound for n>=7 is

    theta_n >= (ell(n)-2)/(ell(n)+1) = (2n-13)/(2n-4),

which exceeds 4/7 as soon as n>=13. Both inequalities concern the same source A,B at that fixed n and arbitrary M. Allowing theta to depend on n cannot reconcile them.

This theorem makes no assertion for n<=12. The actual n=6 necessary interval is nonempty (AL04), so it cannot substitute for this proof. The integer 13 is a threshold of these conservative analytic estimates, not a computed least failure size.

## Scope of the exclusion

Both endpoints and all size-dependent convex blends are eliminated. The failure uses genuine whole source operations, including a KEEP with a=q=0 and an active B zig. Ignoring q=0 operations would discard a required transition.

Theta depending on A or B is outside this theorem. Such a definition adds a transition term Delta theta times U-L (with the appropriate endpoint); choosing it is a new substantive construction problem. No unproved selector, compatible labeling, all-size finite-fit premise, or surrogate potential-existence assertion is supplied as a repair. A blend that fails these stronger sufficient laws is not a counterexample to Coarse-Double or to unrelated potentials.
''')
    put('AL04_EXACT_CONTROL_AND_REPLAY.md',r'''
# Exact six key control and source replay

The saved certificate verifies a source-level DELETE failure for L and independently checks the finite arithmetic used to distinguish it from the all-size blend obstruction. It reuses the previous 132-tree, 660-directed-arc primitive rotation corpus. No larger tree corpus, pair graph, or fitted potential is involved.

## Exact endpoint evaluations

Set n=6 and M=4(3(2,empty),5). Then

    A = 1(empty,6(M,empty)),
    B = 2(1,3(empty,4(empty,5(empty,6)))).

Trees are represented completely in root_aligned_countercertificate.json. The two operations are DELETE 6 and KEEP 1, each from this same A,B. Exact maxima over all candidate trees are:

| Function | Source | After DELETE 6 | After KEEP 1 |
| --- | --- | --- | --- |
| L | 197/128 | 533/128 | 2801/4096 |
| U | 405/128 | 533/128 | 16625/4096 |

Thus Delta_DELETE L=21/8>2, Delta_DELETE U=1, Delta_KEEP L=-3503/4096 and Delta_KEEP U=3665/4096. DELETE has (a,q,z)=(1,0,0); KEEP has (0,0,1).

The two necessary blend tests at this size give

    5/13 <= theta_6 <= 3503/7168.

This interval is NONEMPTY. It establishes neither a feasible six-key potential nor a six-key refutation of all blends. No coefficient was chosen. The all-size impossibility in AL03 follows instead from its scalar inequalities for n>=13.

## A complete closed source walk containing the failed DELETE

Start from the diagonal (B,B) and execute

    D1 D4 D6 D1 D6 D5 D1 D2.

Every operation is DELETE; B remains fixed. After the first four operations the actual pair is exactly (A,B). The fifth operation is the failed DELETE 6. The last three restore A to B. The full oriented StepEv lists and both complete trees at every endpoint are saved. Both engines agree, and the actual paired endpoint equals the initial diagonal.

The closed totals are A=12 and Q_B=0, so Coarse-Double holds on this walk. Only L's proposed edge inequality is refuted.

## Independent checks

verify_root_aligned_repair.py produces the certificate from the frozen source engines and the prior metric corpus. It adds one metric BFS from A_d on the SAME 132 vertices. independent_verify.py imports neither the producer nor its formulas for the exact endpoint values. It independently recomputes all 396 integer candidate scores using a depth DFS and scale 8^5, restricts the maxima to the correct root at each endpoint, and validates all six displayed values.

The verifier also regenerates the 660 primitive rotation arcs directly from immutable raw tree tuples. For each of the two metric rows, predecessor paths attain every claimed distance, and the inequality |d(u)-d(v)|<=1 on every primitive arc proves the matching lower bound. Together they certify exact rotation distances. All 132 distinct ordered trees are valid, and the Catalan count 132 proves completeness of the fixed six-key corpus.

Full replay uses the pointer engine, independently of the frame-based producer records. All oriented event lists, source costs, source and destination trees, and exact closure agree. independent_audit.json reports PASS. A rational substitution at n=13 checks 15/7>2; it is scalar arithmetic, not an n=13 graph or finite fit.
''')
    put('AL05_STRATEGY_REVIEW.md',r'''
# Strategy review after the two envelope audits

The unrestricted and root-pinned envelopes have complementary component laws, but neither is a complete uniform potential. Their size-dependent convex mixtures also fail. These are two consecutive envelope audits with no positive advancement of Universal Coarse-Double, triggering the strategy review required by RESEARCH_RULES.md.

## Before and after the bounded repair audit

BEFORE: G already paid every root-conditioned B consumer uniformly in n and both arbitrary-fringe zero-weight helper branches of the earlier analytic family. G failed a cheap root-changing DELETE. The unrestricted metric envelope U repaired DELETE but lost the auxiliary root needed for B repayment. A complete A/B potential remained open.

RESULT: Restricting auxiliary roots restores B repayment for L, with a uniform extra margin of 1/3 for every nontrivial B access. The same single-rotation family forces Delta_DELETE L>2 for n>=7, and the exact n=6 control also fails. The necessary bounds for a size-dependent mixture conflict for each n>=13. The endpoint argument also excludes normalized root maxima and minima with arbitrary nonnegative zero-self penalties, plus uniformly bounded corrections to their root-depth band.

AFTER: No complete candidate remains in the registered envelope/blend family. The established raw G laws are retained as partial lemmas; none is transferred to a different function without proof. L's B law does not establish whole overwritten-setup repayment or whole zero-weight helper safety, since their A phases remain exposed. The original all-size potential and Universal Coarse-Double obligations remain OPEN.

GENUINELY DELETED ORIGINAL OBLIGATIONS: none. NET PROOF ADVANCEMENT on Universal Coarse-Double: zero. STRATEGIC ELIMINATION: the explicit root-restriction family, arbitrary size-dependent convex blends, and the normalized root-band subclass are ruled out by analytic source inequalities.

NEW ASSUMPTIONS FOR THE ORIGINAL THEOREM: none. No incompatible capacities, new global selector, unproved certificate existence, or finite feasibility premise is appended to the conditional pipeline.

## What the obstruction requires of a future repair

For Psi=G+R, the displayed DELETE forces Delta R<=2-7(n-3)/8, an unbounded negative correction under one rotation. A B-only gauge or a bounded fringe term cannot provide it. At the same source, the zero-demand B zig still requires nonincrease. These two requirements expose the specific missing mechanism: a joint structural cancellation for root changes that also controls its B motion.

Access-root alignment is a useful sufficient mechanism for the raw G estimate. The present obstruction does not make it an independently necessary property of every valid potential. Imposing it through a normalized auxiliary envelope can add a fatal source-dependent feasible-set jump.

A state-dependent envelope selector would add an uncontrolled Delta theta*(U-L) term; declaring a selector with the desired inequalities would merely restate the open potential problem. Another finite fitted histogram would provide no uniform cancellation. Neither is an admissible automatic continuation.

## Four-rule decision

The pre-execution gate registered one explicit construction family, two concrete necessary source tests, and the original obligation that a SUCCESSFUL complete potential would remove. That principal target was refuted; the negative result cannot be relabeled as successful upward advancement. The bounded repair audit is complete and stops here.

No third envelope, parameter, selector, or larger finite-fit campaign is launched. A future proof campaign needs a fresh written four-rule gate anchored in an explicit new cancellation identity or another independently established construction. It must discharge both source laws for the SAME function and state exactly which original obligation is removed. This review records a mathematical gate decision; it asks for no new workspace authorization.

Stage 11G, its solvers, graph, contracts, certificate files, and status are not edited or promoted. All new work remains in this separate append-only directory.
''')
    put('AL06_FINAL_REPORT.md',r'''
# Route C root alignment repair audit

The explicit root-pinned repair of G preserves access-root alignment and proves the uniform B-repayment bound, but it fails DELETE. No complete uniform A/B potential was found in this repair family.

With r=1/8 and primitive rotation distance rho, the tested functions were

    G(A,B)=sum_y r^{d_A(y)} d_B(y),
    U(A,B)=max_T [G(T,B)-rho(A,T)],
    L(A,B)=max_{root(T)=root(A)} [G(T,B)-rho(A,T)].

For root(A)=x and d_B(x)>=1, every auxiliary term in L decreases by at least floor(d_B(x)/2)+1/3 under the B splay. This gives L the required root-conditioned B law on every size and arbitrary fringe configuration. See [the proof](AL01_ROOT_PINNED_B_LAW.md).

For A=1(empty,n(M,empty)) and B=2(1,right-vine3..n), DELETE n costs a=1 but forces

    Delta L >= (2n-7)/3 > 2, for every n>=7.

The exact n=6 control already gives Delta L=21/8. The same argument excludes normalized root envelopes with arbitrary nonnegative zero-self penalties. See [the DELETE obstruction](AL02_DELETE_BAND_OBSTRUCTION.md).

Blending with U cannot repair both laws, even if the coefficient is chosen separately for every n. KEEP 1 from the SAME source forces theta_n<=4/7, while DELETE n then gives

    Delta[(1-theta_n)L+theta_n U] >= (2n-11)/7 > 2, n>=13.

This is an analytic all-size contradiction, not a fit or extrapolation. It excludes this entire size-dependent convex family. See [the blend proof](AL03_SIZE_DEPENDENT_BLEND_NO_GO.md). Source reachability for these arbitrary-size pairs follows from [Levy and Tarjan, Theorem 3.4](https://arxiv.org/html/1907.06310v3#S3), as explained in the DELETE proof.

[Independent verification](independent_audit.json) passed on the existing six-key metric corpus and the complete eight-DELETE closed replay. The finite blend tests have a nonempty necessary interval; no finite infeasibility or sufficiency is claimed. The closed word has Q_B=0 and does not refute Coarse-Double. See [the exact control](AL04_EXACT_CONTROL_AND_REPLAY.md).

The [four-rule gate](AL00_FOUR_RULE_GATE.md) preceded this bounded audit. The [required strategy review](AL05_STRATEGY_REVIEW.md) records two consecutive envelope failures and stops automatic variants. Strategic elimination is established; no original Coarse-Double obligation is discharged. The uniform potential, Coarse-Double, and downstream Dynamic Optimality proof remain open or conditional as before.

All outputs are append-only here. No larger finite fits, new pair graphs, installs, commits, or Stage 11G edits were made. Preservation details are in final_integrity.json; reproducibility is in [AL07](AL07_REPRODUCIBILITY.md).
''')
    put('AL07_REPRODUCIBILITY.md',r'''
# Reproducing the bounded root alignment audit

The scripts use the Python standard library and the existing frozen source engines. No dependency installation is required. From the repository root, the original producer invocation was

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_alignment_20261031_v001/verify_root_aligned_repair.py
```

The independent verifier invocation was

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_alignment_20261031_v001/independent_verify.py
```

Both scripts use exclusive creation for their outputs. Do not rerun them in this populated directory. To reproduce, copy the scripts into a fresh versioned sibling directory under DIRECT_U4_PARALLEL_RESEARCH and invoke the producer, then the independent verifier there. Keep the prior route_c_potential_20261031_v001 input directory in place. The producer also checks the tracked tree is clean; neither script changes it.

The proof files AL01 through AL03 are analytic. Their universality is proved by the binary mass bound, the source displacement bound and two fixed symbolic source operations, not by extending the six-key computation. In particular, n>=13 is derived algebraically. No n>=7 corpus is generated.

root_aligned_countercertificate.json records all changed metric data, exact values, source edges and complete closed replay. The inherited 132-tree/660-arc metric corpus is referenced by filename and pinned hash in entry_source_pins.json. independent_verify.py independently validates the inherited arcs, both distance rows, all 396 candidate scores, all six maxima and all oriented source replay events. independent_audit.json is its saved PASS result.

entry_source_pins.json records ten original input hashes and the actual HEAD and branch. additional_source_pins.json pins the displacement proof used during this audit. external_source_record.json identifies the primary reachability theorem. final_integrity.json compares the pinned inputs and Git state at delivery. delivery_manifest.json hashes the delivered files, excluding itself. Existing source, reports, failures, Stage 11G assets, and proof statuses remain read-only.
''')
    js('proof_status_ledger.json',{'date':'2026-10-31','principal_target':'Repair G through a root-pinned metric envelope or its size-dependent convex blend with U, satisfying both source laws',
      'claims':[
        {'claim':'L is explicit and finite, and obeys the root-conditioned B-repayment inequality at every size','status':'PROVED—UNIVERSAL','scope':'finite present-key ordered BSTs; root(A)=access key; r=1/8','proof':'AL01_ROOT_PINNED_B_LAW.md'},
        {'claim':'L obeys DELETE','status':'REFUTED—EXACT','scope':'n6 exact source zig; analytic violations for every n>=7, arbitrary M','proof':'AL02_DELETE_BAND_OBSTRUCTION.md'},
        {'claim':'Normalized root envelopes with nonnegative zero-self penalties obey DELETE','status':'REFUTED—EXACT','scope':'root max of G-C or root min of G+C; n>=7','proof':'AL02_DELETE_BAND_OBSTRUCTION.md'},
        {'claim':'A size-dependent convex blend (1-theta_n)L+theta_n U obeys both laws','status':'REFUTED—EXACT','scope':'every n>=13, any theta_n in [0,1], independent of state','proof':'AL03_SIZE_DEPENDENT_BLEND_NO_GO.md'},
        {'claim':'Six-key metric values, maxima and complete closed DELETE replay','status':'FINITE-EXACT','scope':'132 single trees, 660 directed primitive arcs, 2 metric rows, 396 candidate scores, 8 source operations','proof':'independent_audit.json'},
        {'claim':'Six-key necessary blend interval is nonempty','status':'FINITE-EXACT','scope':'[5/13,3503/7168]; no sufficiency or coefficient-fit claim','proof':'AL04_EXACT_CONTROL_AND_REPLAY.md'},
        {'claim':'Uniform A/B potential satisfying both laws','status':'OPEN','scope':'no successful candidate; state-dependent and unrelated constructions not excluded'},
        {'claim':'Universal Coarse-Double','status':'OPEN','scope':'no proof and no counterexample produced'},
        {'claim':'Downstream Dynamic Optimality assembly','status':'CONDITIONAL','scope':'inherited load-bearing obligations unchanged'}],
      'genuinely_deleted_original_obligations':[],'net_original_proof_advancement':0,
      'strategic_elimination':'registered root-envelope/blend mechanism; distinct from positive CD advancement',
      'new_assumptions_for_original_theorem':[],'strategy_review_required':True,'strategy_review_completed':'AL05_STRATEGY_REVIEW.md',
      'next_automatic_campaign':None,'larger_finite_fits':0,'new_pair_graphs':0,'Stage11G_modified':False})
    print(json.dumps({'reports_written':7,'ledger_written':True,'independent_audit':'PASS','new_campaign_launched':False}))

if __name__=='__main__':main()
