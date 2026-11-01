"""Save the completed one-mechanism audit in this append-only directory."""
from pathlib import Path
import json,hashlib

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def put(name,s):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f:f.write(s.strip()+'\n')
def js(name,v):put(name,json.dumps(v,indent=2))
def main():
    assert json.loads((OUT/'independent_audit.json').read_text(encoding='utf-8'))['status']=='PASS'
    assert json.loads((OUT/'sharp_bound_audit.json').read_text(encoding='utf-8'))['status']=='PASS'
    helper=OUT.parent/'route_c_analytic_20261030_v001/RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md'
    js('additional_source_pins.json',{'files':{helper.relative_to(ROOT).as_posix():hashlib.sha256(helper.read_bytes()).hexdigest()},
      'timing':'The existing arbitrary-fringe source family was read during this audit. Only its exact d_A=1,d_B=4 costs are used for a direct consequence of the universal partial bound.'})
    put('CC01_SOURCE_ROTATION_IDENTITY.md',r'''
# Subtree key set identities for source rotations

A primitive rotation replaces exactly one nonempty subtree key set. This identity gives a DELETE bound and a root-conditioned B decrease for an explicit structural function, with no bound on key count or fringe size.

## Definitions and multiplicity

Let C(T) contain the exact sets of keys in all nonempty node-rooted subtrees of a finite ordered BST T. Include the full key set. A singleton occurs only for a leaf node; do not add a singleton for every key. Internal shape and the label of the subtree root are not part of the set's identity.

For n-node T, |C(T)|=n. Subtrees at different nodes are disjoint or strictly nested. Strict containment follows because the ancestor's key is absent from its descendant's subtree. Thus there are no duplicate sets within C(T). For same-key A,B define

    F(A,B)=n-|C(A) intersection C(B)|
          =(1/2)|C(A) symmetric-difference C(B)|.

The full key set is always shared, so 0<=F<=n-1 when n>=1. At n=1, F=0. Set F=0 for empty trees, which have no present-key accesses. C(T) is a family of node-key sets, not a family of external-leaf clusters or exact subtree shapes.

## The exact primitive identity

Consider a left rotation

    p(L,x(M,R))  ->  x(p(L,M),R).

The key set of the whole local subtree is retained, now rooted at x instead of p. All outside subtree sets and the internal sets of L,M,R remain unchanged. The only replaced sets are

    J={x} union keys(M) union keys(R),
    K={p} union keys(L) union keys(M).

J contains x and excludes p, while K contains p and excludes x, so they are distinct. They cannot equal any retained set of the same tree. Consequently, with B fixed,

    F(A_after,B)-F(A_before,B)
      = indicator(J in C(B))-indicator(K in C(B)).          (1)

In particular, the absolute change is at most one. Right rotations give the same formula after exchanging left and right. Empty fringe slots cause no exception.

## The actual source ordering of a B splay

Let x be the accessed key. At every primitive rotation in an ordinary bottom-up source splay, the removed proper subtree set J contains x and the added set K excludes x. For a final zig the promoted child is x. In an LL or RR double, the first promoted child is the parent of x, whose old subtree contains x; the second promoted child is x itself. For an LR or RL double both rotations promote x. In each case the demoted-node subtree created by the rotation excludes x.

This covers the exact same-side order in python/liquidity/legacy_embedding.py and the LL/RR/LR/RL frame reconstructions in python/independent/splay.py. In particular, it does not treat a same-side double as two consecutive rotations both promoting x. Earlier rebuilt x subtrees and arbitrary fringes are carried as actual subtrees, so the argument continues at all later operation sites.

Assume now root(A)=x while B splays x and A is frozen. Every proper A subtree excludes x. A removed proper B set J containing x therefore belongs to no C(A). Formula (1), applied with the moving side B, becomes

    Delta_primitive F = -indicator(K in C(A)) <= 0.         (2)

No common set is ever lost. This is an exact structural cancellation, not a bound on a fitted depth histogram.

## At least one new shared set for a nontrivial B access

Suppose d_B(x)>0 and let y be B's old root. Choose the side of x containing y:

    I={k:k<x}, if y<x; otherwise I={k:k>x}.

I is nonempty and proper. It is the entire corresponding child-subtree key set of A because root(A)=x. It becomes the same child-subtree key set in S_x B. It was NOT in C(B): I contains the old B root y but is a proper set, and a proper node-rooted subtree cannot contain the global root.

Thus at least this one set is newly shared. Since none are lost,

    F(A,S_x B)-F(A,B) <= -1, root(A)=x, d_B(x)>0.         (3)

For d_B(x)=0, B is unchanged. More precisely, the whole difference equals minus the number of newly shared B subtree key sets. Nothing here implies one new shared set per B double; that stronger claim is false (CC03).
''')
    put('CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md',r'''
# An explicit unbounded correction and its proved partial laws

The subtree-set correction cancels the old root-changing DELETE obstruction and obeys DELETE on every source edge. It also preserves a strict B decrease and the earlier arbitrary-fringe zero-weight helpers. Its decrease does not always repay the full q, so it is not a complete Route C potential.

## Explicit definition

Retain r=1/8 and edge depths. For actual same-key BSTs put

    G(A,B)=sum_y r^{d_A(y)}d_B(y),
    F(A,B)=n-|C(A) intersection C(B)|,
    R(A,B)=F(A,B)-G(A,B),
    Psi(A,B)=G(A,B)+R(A,B)=F(A,B).

Every term is determined by the current physical pair. There is no unknown function to construct and no compatibility assumption hidden in the definition. Merely writing R=F-G supplies no proof; the content is the source rotation identity for this specified F and the laws below. This correction uses labeled subtree-set agreement, beyond a global joint-depth histogram.

## Universal DELETE bound

An A splay at x uses exactly d_A(x) primitive rotations: each double consumes two levels and a final zig consumes one. Formula (1) of CC01 bounds the increase of F by one per rotation with B fixed. Therefore

    Delta_DELETE Psi <= d_A(x) <= 2 ceil(d_A(x)/2)=2a.     (4)

This holds for all finite valid pairs, both orientations, every present x and arbitrary fringes. When d_A=0, the A tree is unchanged. DELETE omits a request from B; no BST node is removed.

## Exact cancellation on the old unbounded-drift family

For n>=3 and ANY BST M on keys 2 through n-1, take

    A=1(empty,n(M,empty)),
    B=2(leaf 1,right vine on 3 through n),
    A_d=S_n A=n(1(empty,M),empty).

The one root zig changes only the A weights at 1 and n; every M key keeps its A depth. Since d_B(1)=1 and d_B(n)=n-2,

    Delta_DELETE G=(1-r)(n-3)=7(n-3)/8.

Both before and after, the only subtree key set shared with B is the full set. B's proper sets are {1} and suffixes containing n but excluding 2. A's proper M sets contain neither 1 nor n; the remaining proper set is [2,n] before or [1,n-1] after. Neither occurs in C(B). Hence

    F(A,B)=F(A_d,B)=n-1,
    Delta_DELETE R=-7(n-3)/8,
    Delta_DELETE Psi=0.                                   (5)

This is the demanded unbounded negative correction under one rotation, not a bounded reserve or B-only gauge. The oscillation of R on these endpoints tends to infinity with n, proving R is unbounded on the all-size domain.

KEEP 1 from the SAME source has a=q=0 and one B zig. B becomes the right vine on 1 through n. Its new proper set [2,n] agrees with A's child subtree; no other proper agreement occurs. Thus Delta Psi=-1. The correction passes BOTH operations that defeated the previous root-envelope repairs.

## B repayment that is actually proved

When root(A)=x, CC01 gives

    Delta_B Psi <= -1, if d_B(x)>0;
    Delta_B Psi = 0,   if d_B(x)=0.                       (6)

This is uniform in n and fringe shape and uses no setup identity, latest arrival or history restriction. It pays the required -q for q<=1. It does NOT establish the required -q at larger demand.

For a whole KEEP, compose the A and B phases in the actual source order. After A splays x, it is rooted at x, so (6) applies to B. Consequently

    Delta_KEEP Psi <= d_A(x)-indicator(d_B(x)>0).         (7)

Let epsilon_A=d_A(x) mod 2, so 2a=d_A+epsilon_A. Bound (7) implies the required Delta Psi<=2a-q for every KEEP with d_B=0, and for every other KEEP satisfying

    q <= 1+epsilon_A.                                    (8)

This includes all q<=1 edges and all q=2 edges with odd A depth. Closed source walks entirely in this stated class satisfy Q_B<=2A by exact telescoping. This is a restricted-domain result, not a mandatory property of all source walks or a completed universal reduction.

## Arbitrary-fringe zero-weight helpers

Both branches of the existing [arbitrary-fringe helper family](../route_c_analytic_20261030_v001/RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md) have d_A=1 and d_B=4, hence a=1,q=2 and budget zero. Formula (7) gives Delta Psi<=1-1=0 for ALL of them, independently of fringe cardinality, internal paired shapes or reflection. No new helper corpus was needed.

The correction therefore survives that specific all-size helper obstruction and the old cheap-DELETE/zero-demand-KEEP pair. Whole overwritten-setup histories with unrestricted q remain outside (8); CC03 supplies an actual starved q=2 failure. Success on the earlier necessary tests is not sufficient for the universal theorem.
''')
    put('CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md',r'''
# Full B repayment and every scalar rescaling fail

The corrected potential F lowers by only one or two on an opposite-vine starved KEEP, even though q grows with n. This refutes full B repayment for every n>=6. A diagonal DELETE then excludes every scalar rescaling c_n F, even if its coefficient is chosen separately for each size.

## Opposite vines

Let R_n be the right vine 1,2,...,n, rooted at 1. Let L_n be the left vine n,n-1,...,1, rooted at n. Their subtree sets are respectively all suffix intervals [k,n] and all prefix intervals [1,k]. For n>=2 their only shared set is the full set, so

    F(L_n,R_n)=n-1.

Take A=L_n, B=R_n and KEEP n. A is already rooted at n: a=0. B has depth n-1, hence q=floor((n-1)/2) and z=(n-1) mod 2. Denote V_n=S_n R_n.

The source RR recurrence is explicit. When two outer right-vine ancestors k,k+1 are consumed, the rebuilt target remains n and its old left subtree J is replaced by

    (k+1)(leaf k,J).

For odd n the final left subtree of V_n has a right spine 2,4,...,n-1, with the preceding odd singleton attached at each left child. For even n there is one final zig at 1: the final left subtree has root 1, then right spine 3,5,...,n-1, with singleton 2,4,...,n-2 at their left children. V_n has root n and empty right subtree in both cases.

For n>=3, the proper prefix sets shared by L_n and V_n are exactly:

| Parity | Newly shared proper prefix sets | Count m_n |
| --- | --- | --- |
| n even | [1,n-1] | 1 |
| n odd | [1,n-1] and {1} | 2 |

Every other right-spine subtree has minimum at least 2, and every other singleton has key at least 2, so none can be a prefix [1,k]. The two sets in the odd row are distinct for n>=3. Thus the exact source change is

    Delta_KEEP F=-m_n.

For even n>=6, q=(n-2)/2>=2>m_n=1. For odd n>=7, q=(n-1)/2>=3>m_n=2. Hence Delta F>-q for EVERY n>=6. This is an all-size algebraic proof, not extrapolation from the fixed six- and seven-key controls. The mirrored counterexample follows by reversing key order and interchanging children.

## Scalar rescaling cannot fix the deficit

Let c_n be ANY real number fixed over all states and operations of size n, and consider Psi_c=c_n F, or equivalently R_c=c_n F-G. The preceding KEEP necessarily requires

    c_n >= q/m_n.                                       (9)

Now use the diagonal source (R_n,R_n) and DELETE n. The destination is (V_n,R_n). All proper V_n subtree sets exclude n; all proper R_n sets contain n. They share only the full set, so

    Delta_DELETE F=n-1,
    2a=2 ceil((n-1)/2).

The DELETE bound therefore necessarily requires

    c_n <= 2 ceil((n-1)/2)/(n-1).                       (10)

For odd n>=7, (10) gives c_n<=1 while (9) gives c_n>1. For even n>=6, (10) gives c_n<=n/(n-1)<=6/5 while (9) gives c_n>=(n-2)/2>=2. These constraints are disjoint at every n>=6. They use the same size and a single coefficient, so size dependence does not help. They are necessary inequalities, with no coefficient fitted.

This refutes unit F and its complete registered scalar family. It does not refute arbitrary corrections, variable subtree-set weights, state-dependent functions, or unrelated nonlinear mechanisms. No such alternative is asserted or launched.

## Source reachability and exact closure

The starved pair (L_n,R_n) is reached from the diagonal (R_n,R_n) by DELETE 2, DELETE 3,...,DELETE n. Each is a single right-child zig in A. Thus all counterexamples are physical reachable source states without a separate reachability theorem.

For every n>=6 an explicit closed source word from the right-vine diagonal is

    D2 D3 ... Dn ; Kn ; K1 K2 ... Kn ; K(n-1) K(n-2) ... K1.

The first block reaches (L_n,R_n), then Kn is the failed edge. An ascending pass 1 through n transforms ANY present-key BST into L_n: after the pass has accessed k, the accessed prefix is the left spine k,k-1,...,1; promoting the next successor retains that spine below its new root. A descending pass analogously yields R_n. Therefore the last two blocks restore the diagonal exactly. This connector argument asserts endpoints only, not a sign or cost bound.

CC04 independently replays the n=6 word. Its totals obey Coarse-Double. Refuting the candidate's edge inequality does not refute the original closed-walk theorem.
''')
    put('CC04_EXACT_SOURCE_CONTROL.md',r'''
# Fixed source controls and the closed replay

The exact audit used nine pre-registered controls at n=6 or n=7, plus one complete seventeen-operation source replay. It built no source graph, generated no tree corpus and fitted no coefficient.

## Exact failures and successful old tests

| Source operation | Source F | Destination F | a | q | Delta F | Required upper bound |
| --- | --- | --- | --- | --- | --- | --- |
| DELETE 6 from (R6,R6) | 0 | 5 | 3 | 0 | 5 | 6 |
| KEEP 6 from (L6,R6) | 5 | 4 | 0 | 2 | -1 | -2 |
| DELETE 7 from (R7,R7) | 0 | 6 | 3 | 0 | 6 | 6 |
| KEEP 7 from (L7,R7) | 6 | 4 | 0 | 3 | -2 | -3 |

At n=6 the scale would need c_6<=6/5 from DELETE and c_6>=2 from KEEP. At n=7 it would need c_7<=1 and c_7>=3/2. These controls check the symbolic parity formulas; they do not replace the all-size proof in CC03.

The previous n=6 source with arbitrary middle tree instantiated by the balanced tree on 2 through 5 gives

    Delta_DELETE G=21/8, Delta_DELETE R=-21/8, Delta_DELETE Psi=0.

KEEP 1 from that same pair gives Delta Psi=-1 and budget zero. Mirrored controls agree, including the opposite-vine repayment failure. The countercertificate saves all complete trees, subtree key sets, rational values, grouped oriented events and primitive rotation states.

## A closed word starting at the right-vine diagonal

Start from (R6,R6) and execute

    D2 D3 D4 D5 D6 K6 K1 K2 K3 K4 K5 K6 K5 K4 K3 K2 K1.

The sixth operation, K6, is exactly the starved counterexample. The actual final pair equals (R6,R6). The totals are A=19, Q_B=4 and Z_B=12, so this is not a Coarse-Double counterexample.

The original producer replays a cyclic rotation of this word starting at (L6,L6). right_vine_closed_rotation.json identifies the precise row permutation into the fully recorded replay; verify_sharp_bound.py verifies the complete rotated shared-state chain and endpoint. No new connector search is used.

## Independent verification

audit_clade_correction.py compares the frozen pointer and frame source engines on every full state and oriented event. It instruments primitive rotations only in its local Python process, restores the functions after each trace, and writes no source file. Its seventy-five primitive rotation records verify the one-set identity in the fixed controls and replay.

independent_verify.py imports neither the producer nor its set-counting routine. It computes subtree key sets through exact rank intervals and recomputes G and R by an independent depth DFS with rational arithmetic. It verifies every primitive transition as an actual immutable-tree rotation, every changed interval, all grouped events and source costs, all twenty-six recorded source edges and exact paired closure. independent_audit.json reports PASS.

verify_sharp_bound.py checks the sharper at-least-one B drop, the distinguished newly shared root-side set, and the bound Delta_KEEP F<=d_A-indicator(d_B>0) on the SAME saved source edges. Its report sharp_bound_audit.json is PASS. Arbitrary-fringe helper safety is an analytic consequence of that universal bound, not a larger helper fit or an extra finite experiment.
''')
    put('CC05_STRATEGY_AND_PROOF_STATUS.md',r'''
# Strategy and proof status after the subtree set audit

An explicit unbounded correction now cancels the old root-changing DELETE drift, obeys DELETE universally and preserves the arbitrary-fringe zero-weight helpers. It still fails the full B double repayment requirement. The registered construction and every scalar rescaling are refuted; Universal Coarse-Double remains open.

## Before and after

BEFORE: G repaid root-conditioned B consumers but had unbounded positive DELETE drift. The unrestricted rotation envelope repaired DELETE and lost B repayment; root restriction recovered B repayment and lost DELETE. Their size-dependent convex mixtures were excluded, and a mandatory strategy review stopped further envelope variants.

RESULT: This new audit used a different source identity: one primitive rotation replaces one subtree key set. For the explicit F=n-|C(A) intersection C(B)| and R=F-G, DELETE motion is bounded by d_A. A nontrivial B splay at A's root creates at least one new common set and loses none. The resulting whole-access bound is

    Delta_KEEP F <= d_A-indicator(d_B>0).

It proves the desired source inequality when q<=1+(d_A mod 2) on nontrivial B accesses, and in particular for the all-size arbitrary-fringe helpers with d_A=1,q=2. The old root-changing DELETE and its zero-demand KEEP are both repaired, with exact cancellation Delta R=-7(n-3)/8 on the DELETE family.

AFTER: Opposite vines have q growing with n but gain only one or two common sets. They refute full repayment for every n>=6. A diagonal DELETE forbids raising the global scale enough to pay that deficit, even with a separate scale for each n. No complete A/B potential has been constructed.

GENUINELY DELETED ORIGINAL LOAD-BEARING OBLIGATIONS: none. The original universal potential/Coarse-Double premise is unchanged. NET ADVANCEMENT OF THE FULL ORIGINAL PROOF: zero. POSITIVE PARTIAL CONTENT: the specified unbounded correction, universal DELETE law, strict root-conditioned one-unit B law, exact cancellation on the old family and the stated restricted-domain source inequality. The latter is not claimed to be a previously unresolved or literature-new subclass; the old proof ledger is not rewritten.

NEW ASSUMPTIONS FOR THE ORIGINAL THEOREM: none. No cluster-weight existence problem, selector, compatibility premise, or finite-feasibility assertion is appended to the conditional pipeline. Formula (8) in CC02 is only an explicit sufficient restriction; it is not asserted necessary or automatic in original walks.

## Why the mechanism falls short

A root-aligned splay always creates the entire child-side key set containing B's old root, which accounts for one compulsory common set. Intermediate double steps can create many other sets without matching any A subtree. Opposite vines make that failure exact. A new shared root alone cannot pay an unbounded double count.

Writing R=F-G is not an abstract existence reduction: F is specified and independently computable, and the proofs concern that actual function. Conversely, calling some new weighted common-set count the needed reserve would not construct it. Any future candidate must prove a sufficient per-demand gain while controlling its actual A motion for the SAME function.

## Gate decision and stop

CC00 froze the formula, the one-set identity, source controls, scalar test and original success obligation before execution. The audit completed its principal proof/refutation target. It did not achieve the registered complete-potential success condition and does not relabel partial laws as Universal Coarse-Double.

The earlier two-envelope strategy review stays intact. This audit used an independently explicit rotation cancellation instead of another envelope. It now stops on the new counterexample as RESEARCH_RULES requires. No weighted-set, selector, hybrid, rescaled parameter search, or larger finite-fit campaign is launched. A future campaign needs its own concrete construction and written four-rule gate; no new workspace permission is needed for authorized append-only work.

Stage 11G's graph, solvers, certificates, contracts and proof status are not edited or promoted. Source and prior report hashes are checked separately in final_integrity.json, and the tracked tree, branch and HEAD are preserved.
''')
    put('CC06_FINAL_REPORT.md',r'''
# An unbounded correction to G and its remaining repayment failure

The subtree-set construction gives an explicit unbounded R that cancels the old root-changing DELETE drift, proves DELETE universally, and preserves the arbitrary-fringe zero-weight helpers. It does not preserve full B repayment; a six-key source witness refutes that remaining requirement.

Let C(T) be the exact key sets of T's nonempty node-rooted subtrees, including its full key set. Define

    F(A,B)=n-|C(A) intersection C(B)|,
    R(A,B)=F(A,B)-G(A,B),
    Psi(A,B)=G(A,B)+R(A,B)=F(A,B).

One primitive rotation replaces only one subtree key set. This proves Delta_DELETE Psi<=d_A<=2a. When A is rooted at the accessed key x, a B splay loses no common set and, if nontrivial, creates at least one. Thus Delta_B Psi<=-1. See [the source identity](CC01_SOURCE_ROTATION_IDENTITY.md).

On the old family A=1(empty,n(M,empty)), B=2(1,right-vine3..n), the one-rotation DELETE n has

    Delta G=7(n-3)/8, Delta R=-7(n-3)/8, Delta Psi=0,

for every middle tree M. KEEP 1 from the same pair also passes, with Delta Psi=-1. The correction is unbounded in n and cancels the drift exactly. It is not another root envelope.

The general whole-KEEP bound is

    Delta Psi<=d_A-indicator(d_B>0).

Consequently, the required inequality holds on all q<=1 edges and on q=2 edges with odd A depth, including every earlier arbitrary-fringe helper with d_A=1,q=2. See [the correction and partial laws](CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md).

Full B repayment nevertheless fails. With A the six-key left vine, B the right vine, and KEEP 6, a=0 and q=2 but Psi falls only from 5 to 4; it must fall by at least 2. Analytically, opposite vines refute the formula for every n>=6. A diagonal DELETE also excludes every scalar rescaling c_n F, even with a different coefficient at each size. See [the all-size obstruction](CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md).

[Independent verification](independent_audit.json) passed on nine fixed controls and a complete seventeen-operation closed source replay. The replay has A=19,Q_B=4; it does not refute Coarse-Double. There were zero fits, new source graphs or larger finite corpora. [Exact control details](CC04_EXACT_SOURCE_CONTROL.md) and [reproducibility](CC07_REPRODUCIBILITY.md) are saved here.

The [four-rule gate](CC00_FOUR_RULE_GATE.md) preceded the audit; the [strategy and status record](CC05_STRATEGY_AND_PROOF_STATUS.md) stops this refuted construction. No complete potential or universal Coarse-Double proof was obtained. Stage 11G and all inherited sources remain read-only; delivery checks are in final_integrity.json.
''')
    put('CC07_REPRODUCIBILITY.md',r'''
# Reproducing the fixed subtree set audit

No packages are installed. The producer and independent verifiers use Python's standard library and the existing frozen source engines. Run from the repository root with Python -X utf8 -B. The original execution order was

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_clade_correction_20261031_v001/audit_clade_correction.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_clade_correction_20261031_v001/independent_verify.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_clade_correction_20261031_v001/verify_sharp_bound.py
```

The scripts create output files exclusively. Do not rerun in this populated directory. To reproduce, copy the scripts into a fresh versioned sibling under DIRECT_U4_PARALLEL_RESEARCH and use its path in the invocations. Keep the old route_c_alignment_20261031_v001 and route_c_analytic_20261030_v001 input directories in place. The producer checks the tracked tree is clean and records source hashes before evaluation.

Only nine fixed source controls at n=6 or 7 are evaluated, together with a seventeen-access n=6 word. No complete tree corpus or pair graph is generated. The n>=6 failure and scalar exclusion come from the exact parity formulas in CC03, not increasing finite fits. The arbitrary-fringe helper result follows directly from the all-size sharp bound, not an enlarged helper sample.

clade_correction_countercertificate.json contains full source trees, exact key sets, grouped oriented events, primitive rotation snapshots, rational G and R values and the complete original closed replay. independent_verify.py checks those data with independent rank-interval and depth arithmetic. right_vine_closed_rotation.json indexes a cyclic permutation of the same verified replay starting and ending at the right-vine diagonal. sharp_bound_audit.json verifies its composition and the sharper bounds on the same source edges.

entry_source_pins.json records eleven inherited inputs, HEAD and branch. additional_source_pins.json pins the helper-family source read during the audit. final_integrity.json compares all twelve hashes and the tracked Git state at delivery. delivery_manifest.json hashes the new artifacts and excludes itself. Existing proofs, source engines, research failures, graph data, Stage 11G assets and proof statuses remain read-only.
''')
    js('proof_status_ledger.json',{'date':'2026-10-31','candidate':'R=F-G, F=n-|C(A) intersection C(B)|',
      'claims':[
        {'claim':'Primitive rotation replaces exactly one subtree key set','status':'PROVED—UNIVERSAL','proof':'CC01_SOURCE_ROTATION_IDENTITY.md'},
        {'claim':'R has unbounded negative drift cancelling the old root-changing DELETE family','status':'PROVED—UNIVERSAL','scope':'n>=3 and arbitrary middle M; Delta R=-7(n-3)/8','proof':'CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md'},
        {'claim':'Corrected Psi=F satisfies DELETE','status':'PROVED—UNIVERSAL','scope':'finite same-key present-key BST source; Delta F<=d_A<=2a','proof':'CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md'},
        {'claim':'Root-conditioned B access loses at least one unit of F when nontrivial','status':'PROVED—UNIVERSAL','scope':'d_B>0, root(A)=access key; not the full q bound','proof':'CC01_SOURCE_ROTATION_IDENTITY.md'},
        {'claim':'Whole source inequality and closed-walk Coarse-Double on the stated subclass','status':'PROVED—RESTRICTED DOMAIN','scope':'every nontrivial KEEP has q<=1+(d_A mod 2); d_B=0 and all DELETE allowed; includes arbitrary-fringe d_A=1,q=2 helpers','proof':'CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md'},
        {'claim':'Corrected Psi=F satisfies full B repayment','status':'REFUTED—EXACT','scope':'opposite-vine source family at every n>=6; fixed n6 witness a=0,q=2,Delta F=-1','proof':'CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md'},
        {'claim':'Some size-dependent scalar c_n F satisfies both full laws','status':'REFUTED—EXACT','scope':'no real coefficient for any n>=6; two explicit necessary source tests','proof':'CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md'},
        {'claim':'Fixed controls, rational arithmetic, source events and closed replay','status':'FINITE-EXACT','scope':'9 controls at n6,7; 17 closed operations; 26 edges,75 primitive identities','proof':'independent_audit.json'},
        {'claim':'Uniform complete A/B potential','status':'OPEN','scope':'no construction satisfying both full laws'},
        {'claim':'Universal Coarse-Double','status':'OPEN','scope':'no universal proof or counterexample'},
        {'claim':'Downstream Dynamic Optimality assembly','status':'CONDITIONAL','scope':'inherited obligations unchanged'}],
      'original_load_bearing_obligations_discharged':[],'net_advancement_of_full_original_proof':0,
      'positive_partial_content':['explicit unbounded correction','universal DELETE bound','strict one-unit root-conditioned B drop','exact old-drift cancellation','specified restricted-domain whole-edge bound and arbitrary-fringe helper safety'],
      'new_assumptions_for_original_theorem':[],'candidate_and_scalar_family_refuted':True,
      'strategy_record':'CC05_STRATEGY_AND_PROOF_STATUS.md','next_automatic_campaign':None,
      'finite_fits':0,'new_pair_graphs':0,'Stage11G_writes_performed':False})
    print(json.dumps({'reports_written':7,'ledger_written':True,'independent_audits':'PASS','new_campaign_launched':False}))

if __name__=='__main__':main()
