# IAGS-11G-S03-M2-R8R01 — Immediate Key-8 Repeat Exclusion

## A. Pre-execution record

Recorded before computational replay, 2026-10-28 (Asia/Karachi).
The user authorized execution of the drafted campaign and clarified that this
agent is to perform experiments and verification. The earlier proof-only ban
was an assistant-added restriction. Execution here permits bounded in-memory
exact replay of the existing controller, without a solver or source changes.
Only this new report may be written. No auxiliary files, bytecode caches,
commits, pushes, or automatic successor are permitted.

Repository: Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity.
Local branch and remote branch: coarse-double-branch.
Local HEAD and remote branch HEAD: fea2a25b05e97f726b6e1891cebb12c4cfca821a.
Tracked tree unchanged. Six pre-existing untracked MSINK/DLSS side files plus
x.json (seven files total) are preserved; baseline SHA256 hashes were recorded
in tool output.
No applicable AGENTS.md was found in the repository or inspected ancestors.

### Four-rule preflight

1. Strictly smaller: one outgoing high-edge family from root-8 extremal-phantom
   states, rather than arbitrary closed B-walks.
2. Concrete mechanism: source validity fixes parent(8)=19; the maximal claimant
   fixes parent(19)=8 and its right side. Active witness prefixes are therefore
   periodic. Audit exact aliased primitive writes for all declared d=0..18.
3. Bounded scope: one exclusion theorem, one alias-composition mechanism, one
   finite controller audit, and its direct signed-successor consequence.
4. Upward advancement: success excludes every negative target-8 edge from this
   source region, and, with ESD01's smaller-target barrier, forces every valid
   high successor there to have weight at least +2. It does not settle M2.

### Frozen theorem and architecture

Parent: for every sector and every closed high B-walk, sum(6-q_H)>=0.
Child: R8(b) := (b.root=8 and b.kr[8]=0 and b.rr[8]=19) implies that
there is no valid genuine frozen high edge with B target x=8, at any weight.
The destination is unrestricted. This is not merely self-loop exclusion.

R1-R4: full G_star=G_AF, original masks/signatures/states/weights/witness scope,
shared midpoint, exact interval closure, Z3 5.1.0 / z3-solver 5.1.0.0 architecture,
exact Int, A-shadow depth 2, T=266, Bank25=25. No graph restriction is imposed.
M1/M2/M3 and Step 03 remain OPEN; Step 04 is UNAUTHORIZED.

### IAGS Box

T: the child exclusion above.
C: orbit determination; exact alias-sensitive primitive composition; all 19
declared depths covered; rejection by genuine diff or endpoint validity;
original-graph projection; signed-successor consequence.
I: frozen compilers; M2 B-only equivalence; ESD01 barrier and persistence;
the audited clean-source h=0 negative edge.
U: can any repeated-8 witness produce a valid genuinely changed endpoint?
beta: local edge exclusion + inherited barrier/persistence -> positive successor
restriction -> one deleted local M2 obligation, not universal cycle closure.

## B. Result and claim status

**OUTCOME A — THE AUTHORIZED LOCAL THEOREM IS PROVED. M2 REMAINS OPEN.**

The principal theorem is universal over its exact antecedent:

> For every frozen sector, every fully valid B-state b with
> root(b)=8 and chi8(b), every destination b', every weight and every original
> high witness, a genuine high edge targeting 8 from b does not exist.

Here chi8(b) means kr[8]=0 and rr[8]=19. Other structural fields, interval
annotations, signatures, masks, additional sentinel claimants and inactive
witness entries are not narrowed. If 8 is unmarked, marked-target legality
already excludes the edge; the proof below covers all masks containing 8.

This is stronger than exclusion of a self-loop: every destination is excluded.
The proof is source algebra, supported by an exact 19-case symbolic normal-form
audit using the unchanged production controller. No solver is used.

New signed consequence: every valid high edge from such a state targets x<8,
has weight at least +2 and preserves chi8. The +2 bound is attained by a fully
validated example in Section H. It is insufficient for universal compensation.

## C. Authoritative source references and inheritance

Paths in this report are relative to the repository root pinned in Section A.
Line numbers refer to the unchanged entry HEAD.

| Source | Load-bearing definition |
|---|---|
| DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py | b_valid:39; muxb:66; b_single_rot:73; BTrace:99; b_parent_of:110; b_side_of:121; verify_bpath:130; b_splay_event:164 |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py | BStruct:13 and b_tree_valid:22; especially root claimant count zero |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py | b_equal:23; build_shigh:31, endpoint validity, witnessed replay, structural diff and credit |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py | StateVars7:22 and state_valid7:44, used only for high ordinary-state legality |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_PRODUCT_COMPILER.py | Product:38, edge:74, _sm_w:90; OM/MO construction |
| DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS/S03_EDGE_PROJECTIONS.py | build_projections:36, private existential witnesses and complete interfaces |

All table paths are under DO_RESEARCH_REBOOT/06_CERTIFICATES/.

Reports in this report's directory:

- IAGS_11G_S03_M2_HIGH_ONLY_B_PROJECTION.md, Sections C-H: exact B-only
  relation, interval distinction, uniform fixed-shadow lifting.
- IAGS_11G_S03_M2_CYCLE_SIGN_OR_COUNTERCERTIFICATE.md, Sections D-F:
  deterministic active witnesses, genuine diff, minimum-weight envelope.
- IAGS_11G_S03_M2_ESD01_ORIENTED_SENTINEL_DEBT.md, Sections F-H:
  clean negative -> root 8 with chi8, smaller-target barrier and persistence.
  Section I's h=0 proof gap is treated explicitly below.

Inherited signs are used only at their proved scope:
chi8(b) and x<8 imply d<=h+1<=9, q<=4, w>=2, and chi8(b').
No high root termination, no-repeat, canonical-depth substitution, or low-edge
fusion is imported.

Source SHA256 values:

| File | SHA256 |
|---|---|
| PC_B_CONTROLLER.py | 3137135eaa9c0c92ae3fd7d57b9f06b90d7fff8524d7063c27cb3b62082c99db |
| PC_TYPED_DAG.py | ec17b28e0ba688fd8aeae08409fab7ea789bc458a00716afaf87117a4095ce6e |
| STRICT_B_CONTROLLER.py | 325a367b92b5d01655403588a56866ae5998390b851b4a00ca146e2f25e4dd60 |
| STRICT_HIGH_COMPILER.py | b5136fa0efa0c3fa9bec472b19a89a58c9bb0697ecbd919c034c362e4ce91b64 |

## D. Forced orbit and static-order audit

Write r=8 and N=19. Assume b is fully valid, b.root=r and chi8(b).

1. In b_tree_valid the root's total number of kind-0 real-slot claims is
   exactly zero. Exact Int sums of nonnegative indicators imply no slot
   claims r. Thus b_parent_of(b,r)=N.
2. Slot r claims N on its right. Every slot above r is a gap and has both
   child kinds equal to 2 by b_valid. The last-match parent mux therefore
   returns r for N, irrespective of lower-index claimants:
   b_parent_of(b,N)=r.
3. b_side_of(b,r,N)=LEFT, because N matches no real parent index.
   b_side_of(b,N,r)=RIGHT, because r.right is precisely (0,N).

The original path conjuncts therefore force, for every active entry,

  p_k = r for even k; N for odd k.
  dir_k = LEFT for even k; RIGHT for odd k.

The path is read against the fixed source, not recomputed after rotations.
At odd k the core ancestor is r: target rank 17 < ancestor rank 17 is FALSE,
so the required side is RIGHT, which matches. At even k the ancestor is N
and the core-ancestor static gate is inactive. Hence static order itself
does NOT exclude any of the 19 declared lengths.

Only p_0..p_d and dir_0..dir_(d-1) are forced. Inactive entries stay arbitrary.
Every operand selected by an active primitive comes from this active prefix
or is an explicit sentinel fallback. Inactive primitives are blended off.

## E. Alias-sensitive primitive proof

For any current state let L denote slot r's current left kind/ref pair.
The original source order matters: parent writes happen first, target writes
second, grandparent writes last.

### E1. One active pair

Every pair starts at even t. Its two directions are LEFT,RIGHT, so same=FALSE.
The exact b_splay_event operands reduce to:

- rotA: x=r, p=N, gp=r, side_x=LEFT, side_p=RIGHT, p_was_root=FALSE.
- rotB: x=r, p=r, gp=N, side_x=RIGHT, p_was_root=(t+2=d).
  The chosen grandparent is N whether its optional active entry exists or
  the sentinel fallback is selected.

For rotA, parent N matches no write index. The target first writes
r.right=(0,N). The final grandparent adoption aliases gp=x=r and overwrites
that same right field with (0,r). Its left field is unchanged.

For rotB, parent and target alias: p=x=r. Since side_x=RIGHT,
the parent write assigns r.right the PRE-rotB left pair L; the target write
assigns r.left=(0,r). These writes affect different sides. Grandparent N
matches no slot. Any root update assigns r.

Therefore every active pair implements the exact map

  (left(r),right(r)) -> ((0,r), old left(r)),

leaves every other slot field unchanged, and keeps root=r.

This calculation allows all original operand aliasing. No distinct-node
rotation theorem is used. All active rotation children here are r, so their
reads use slot r; sentinel-as-child slot-0 reads occur only in blended-off
computations and cannot affect the result.

### E2. Pair iteration

After one pair, left(r)=(0,r) permanently.
After two or more pairs, both sides equal (0,r).
Every subsequent pair preserves these values.

The proof does not reject a trace at its first transient self-reference.
It explicitly checks that no later active operation removes the final left
self-reference.

### E3. Odd final zig

For odd d, p_d=N and dir_(d-1)=LEFT. The final zig has x=r, p=N and
p_was_root=TRUE. It writes right(r)=(0,N), keeps left(r), and sets root=r.

Thus at d=1 it merely rewrites the pre-existing phantom and is an identity.
For odd d>=3 it preserves the left self-reference created by the earlier pair.

### E4. d=0

No primitive is active. The complete B-state is unchanged.

## F. Exhaustive disposition and endpoint contradiction

Let L0 be the original left kind/ref pair of slot 8.
All unlisted B fields, including all lo/hi fields carried by replay, are
unchanged. Root is 8 in every case. q/w columns are the arithmetic values a
candidate would have, not claims that these edges exist.

| d | q=floor(d/2) | w=6-q | Final left(8) | Final right(8) | Decisive rejection |
|---:|---:|---:|---|---|---|
| 0 | 0 | 6 | L0 | (0,19) | structural diff FALSE |
| 1 | 0 | 6 | L0 | (0,19) | structural diff FALSE |
| 2 | 1 | 5 | (0,8) | L0 | root claims itself |
| 3 | 1 | 5 | (0,8) | (0,19) | root claims itself |
| 4 | 2 | 4 | (0,8) | (0,8) | root claims itself |
| 5 | 2 | 4 | (0,8) | (0,19) | root claims itself |
| 6 | 3 | 3 | (0,8) | (0,8) | root claims itself |
| 7 | 3 | 3 | (0,8) | (0,19) | root claims itself |
| 8 | 4 | 2 | (0,8) | (0,8) | root claims itself |
| 9 | 4 | 2 | (0,8) | (0,19) | root claims itself |
| 10 | 5 | 1 | (0,8) | (0,8) | root claims itself |
| 11 | 5 | 1 | (0,8) | (0,19) | root claims itself |
| 12 | 6 | 0 | (0,8) | (0,8) | root claims itself |
| 13 | 6 | 0 | (0,8) | (0,19) | root claims itself |
| 14 | 7 | -1 | (0,8) | (0,8) | root claims itself |
| 15 | 7 | -1 | (0,8) | (0,19) | root claims itself |
| 16 | 8 | -2 | (0,8) | (0,8) | root claims itself |
| 17 | 8 | -2 | (0,8) | (0,19) | root claims itself |
| 18 | 9 | -3 | (0,8) | (0,8) | root claims itself |

For d=0,1 every structural field and root equals the source. The high
compiler's unconditional genuine diff is FALSE.

For d>=2 the final root is 8 and its left pair is (0,8). Structural b_equal
forces the same root and left pair on g.b, whose b_tree_valid requires root
claim count zero. Its self-claim contributes at least one, contradiction.

Independently, b_valid on that self-left link would require
hi[8]=crank(8)-1=16, while its root interval requires hi[8]=18. Thus fresh
endpoint annotations cannot rescue the witness. This argument does not
mistake structural b_equal for equality of replay-carried lo/hi.

All original declared lengths are covered; every candidate is rejected by
a mandatory original conjunct. This proves T_R8R01.

The projected OM relation retains this actual source B-state and its witness,
so cannot create a missing target-8 transition. Contracting with a shared
MO midpoint cannot restore it. The exclusion therefore holds in the original
contracted high graph as well as the B-only relation. No alpha narrowing or
hidden-history concatenation is used.

## G. Signed consequences and the h=0 correction

### G1. Forced positive successor

For any valid high edge with source R8, the target is marked core and lies
in 0..8. The theorem excludes 8, so x<8. ESD01 C1/C2 give:

  w>=2 and chi8(destination)=1.

Existence of an outgoing edge is not assumed; this is a restriction on every
one that exists. Section H gives a valid nonvacuous example.

### G2. Repetition inside the extremal phantom region

If a high edge targets 8 and its destination satisfies chi8, that destination
has root 8 by the final-root theorem and hence satisfies R8. Any following
high edge must target a smaller key and contribute at least +2.

Thus two consecutive target-8 edges are impossible on a path all of whose
vertices satisfy chi8. This does NOT exclude target-8 repetitions separated
by smaller-target edges. Nor does it say every dirty target-8 edge preserves
chi8; that question is outside this Box.

Every clean-source negative edge lands at R8, so its immediate high successor
is positive with the stated bound, including when the clean source has h=0.

### G3. Explicit h=0 boundary and two-cycle repair

The clean root-8 descending chain supports d=18, q=9, w=-3 targeting 8.
Its final root is still 8 but it adds the right phantom. Genuine change
therefore does not imply root change.

The next edge cannot target 8 by T_R8R01. In a two-edge closed high B-walk
containing this h=0 outgoing edge, the direct return would have to target
the initial root 8, because every genuine high edge ends at its target.
This is impossible. Consequently the h=0 clean-negative two-cycle boundary
is now excluded by the new local theorem, not by an r<8 barrier.

For positive even h, ESD01's audited old-root depth <=2 and r<8 direct-return
bound still apply. Combining that existing proof with the separate h=0
argument repairs the even-h two-cycle summary at exactly the clean-negative
scope. The older report is not rewritten. No odd-h extension is asserted.

## H. Exact computational checks and sharp control

The user's execution instruction permits these bounded experiments. They
were run in memory with Python 3.13 using -B and stdin, importing unchanged
repository modules. No files or bytecode caches were created by the checks.
They use no SMT solver, fitting, random search, or alternative graph.

### H1. Symbolic replay audit: 19/19

For every d=0..18, the original b_splay_event was built in the original
PC_TYPED_DAG. Only root=8, right(8)=(0,19), target/depth, and active
periodic witness entries were pinned. Every other B field and every inactive
trace entry remained symbolic.

A conjunction comparing all 115 replayed B fields with Section F's normal
form was reduced by the production DAG constant-folding method. Every
residual conjunct was TRUE or EQ of the identical symbolic node to itself.
All 19 cases passed.

This checks algebra under the orbit pins, not a random state sample.
Section D supplies the universal source-validity -> orbit implication;
Sections E-F supply the independently readable proof and endpoint rejection.
The check alone is not presented as a solver UNSAT result.

### H2. Full high-relation controls: 252/252 expected results

The entire unmodified build_shigh root was evaluated under complete legal
assignments for two clean-source geometries, each across all 126 masks:

| True h | Source root | Declared d | q | w | Masks containing 8: accepted | Masks excluding 8: rejected |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 8 | 18 | 9 | -3 | 70 | 56 |
| 1 | 7 | 18 | 9 | -3 | 70 | 56 |

Both destinations are the root-8 left chain with right(8)=(0,19).
All signatures are zero. Core/gap intervals and all BStruct auxiliaries are
assigned, rather than inferred from topology-only equality. Both ordinary
shadows use root label 8 with legal remaining fields; the shared fiber label
is 8. All auxiliary variables receive legal finite-domain values.
Measured CPU for the 252 full-root evaluations: 13.344 seconds.
The full high DAG had 53,455 nodes.

The h=0 example is nonvacuous and confirms that R8 is a reachable graph
destination even though the theorem excludes a repeated target 8 from it.
These finite controls do not prove the universal theorem over other geometries.

The complete positive assignment also supplies shared-midpoint existence:
its source, destination and fiber satisfy the unprojected high conjunction,
so the same fiber satisfies both projected OM/MO legs. No independent
midpoints are substituted.

### H3. The +2 successor bound is sharp

Use mask {0,1,2,7,8} (mu=391), all signatures zero and fixed ordinary
A-shadow root label 8.

- First edge: clean root-8 descending chain -> same chain with phantom
  right(8)=(0,19), target 8, h=0, d=18, q=9, w=-3.
- Second edge: from that exact full destination, target 0 with declared
  path (0,1,2,3,4,5,6,7,8), all LEFT, d=8, q=4, w=+2.

The second endpoint's nonempty core links are:

  0.right=7
  7.left=5, 7.right=8
  5.left=3, 5.right=6
  3.left=1, 3.right=4
  1.right=2
  8.right=sentinel 19 (kind 0)

Other core children are empty (kind 2, raw ref 19); every gap is absent,
childless, with lo=hi=its rank. Root is 0.

Core endpoint annotations and structural auxiliaries:

| i | lo | hi | bpar | bdep |
|---:|---:|---:|---:|---:|
| 0 | 0 | 18 | 19 | 0 |
| 1 | 2 | 6 | 3 | 4 |
| 2 | 4 | 6 | 1 | 5 |
| 3 | 2 | 10 | 5 | 3 |
| 4 | 8 | 10 | 3 | 4 |
| 5 | 2 | 14 | 7 | 2 |
| 6 | 12 | 14 | 5 | 3 |
| 7 | 2 | 18 | 0 | 1 |
| 8 | 16 | 18 | 7 | 2 |

The entire build_shigh conjunction evaluates TRUE for the second edge with
these fresh endpoint annotations. chi8 persists. The intermediate B-state,
mask/signature and all ordinary alpha fields match the first edge's
destination exactly.

Therefore a valid two-edge prefix has total weight -1. It is NOT closed:
its source B-root is 8 and its final B-root is 0. This neither refutes M2
nor supports a negative-cycle claim. It proves that immediate +2 repayment
cannot be silently strengthened to +3.

## I. Adversarial audit

| Concern | Disposition |
|---|---|
| h=0 genuine root-preserving negative edge | Preserved and fully evaluated |
| d=0 and d=1 | Identity; rejected only by original diff |
| Both declared parities | All 19 lengths covered |
| Target/parent/grandparent aliases | Explicitly composed in source assignment order |
| Additional sentinel claimants | Max index 8 dominates; gaps cannot claim |
| Arbitrary slot-0 values | Do not affect active reads in this orbit; remained symbolic |
| Inactive witness fields | Unpinned in H1; blended-off operations proved irrelevant |
| Phantom refs with non-node kinds | Left arbitrary outside the required right phantom |
| Multiple sentinel refs on a slot | Right-claim side selected exactly as source; no uniqueness assumed |
| Transient invalidity | Not used as rejection; final left self-reference proved persistent |
| Endpoint intervals | Independently contradict self-left; no stale-interval equality imposed |
| Genuine change vs root change | Distinguished throughout |
| All masks/signatures | Universal proof; unmarked 8 vacuous, no sector deleted |
| Shared OM/MO midpoint | Original projection used; no witness-history concatenation |
| Dirty-only cycles | Not settled; separated 8-accesses remain possible questions |
| Low-only or mixed cycles | No imported high conclusion or claimed closure |

## J. Parent reconstruction, BEFORE / RESULT / AFTER

BEFORE:
M2 open; repeated-8 behavior from root-8 extremal phantom states unclassified.
The h=0 correction left ESD01's r<8 return argument inapplicable to that boundary.

RESULT:
1. Entire target-8 outgoing relation from R8 is empty.
2. Every valid high successor from R8 is a smaller-target edge with w>=2 and
   persistent chi8.
3. Immediate target-8 repetition in chi8 paths is excluded.
4. h=0 clean-negative direct two-edge returns are excluded, repairing that
   boundary by a distinct argument.
5. A complete +2 successor control proves the local signed bound is sharp.

AFTER:
One genuine local negative-edge family and its immediate-repeat obligation
are deleted. No new existence premise is introduced. No representation-only
result is promoted to sign progress. OUTCOME A applies only to this Box.

M2 still requires signed closed-walk accounting for separated target-8
repetitions, general dirty states and changing claimants, and any needed
escape/return paths. A -3 edge plus its forced +2 successor can still have
negative prefix weight; closure and further repayment remain uncontrolled.
M1 and M3 remain open independently. Restricted Coarse-Double and Dynamic
Optimality remain open. No successor Box is executed.

## K. Reproduction

The following are the exact in-memory Python programs used. Run each from the
pinned repository root with Python -B on stdin. They perform no writes and
invoke no solver. Source code is embedded here so no auxiliary script artifact
is needed. H1 is a symbolic normal-form check; H2/H3 are complete-assignment
controls and must not be confused with universal search.

### K1. Nineteen symbolic normal forms

```python
import sys, json, hashlib
from pathlib import Path
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG
from PC_B_CONTROLLER import BState, BTrace, b_splay_event

def tautology(d, root):
    for n in d.topo([root]):
        k,t,a,e=d.nodes[n]
        if k=='and':
            continue
    def rec(n):
        k,t,a,e=d.nodes[n]
        if k=='const' and t=='bool': return bool(e)
        if k=='and': return rec(a[0]) and rec(a[1])
        if k=='eq': return a[0]==a[1]
        return False
    return rec(root)

rows=[]
for depth in range(19):
    d=DAG()
    b=BState(d,'S')
    bt=BTrace(d,'T')
    out=b_splay_event(d,b,bt,0,d.const_bool(False))
    pins={'S_broot':8,'S_bkr8':0,'S_brr8':19,'T_bT0':8,'T_bd0':depth}
    for k in range(depth+1): pins[f'T_bp0_{k}']=8 if k%2==0 else 19
    for k in range(depth): pins[f'T_bdir0_{k}']=bool(k%2)
    expected={f:list(getattr(b,f)) for f in ('kl','rl','kr','rr','lo','hi')}
    if depth>=2:
        expected['kl'][8]=d.const_int(0,2)
        expected['rl'][8]=d.const_int(8,5)
        if depth%2:
            expected['kr'][8]=d.const_int(0,2)
            expected['rr'][8]=d.const_int(19,5)
        elif depth==2:
            expected['kr'][8]=b.kl[8]
            expected['rr'][8]=b.rl[8]
        else:
            expected['kr'][8]=d.const_int(0,2)
            expected['rr'][8]=d.const_int(8,5)
    checks=[d.EQ(out.root,b.root)]
    for f in expected:
        checks += [d.EQ(x,y) for x,y in zip(getattr(out,f),expected[f])]
    claim=d.AND(*checks)
    reduced=d.simplify(claim,pins)
    ok=tautology(d,reduced)
    assert ok, ('normal_form_failure',depth)
    rows.append({'d':depth,'q':depth//2,'w':6-depth//2,
        'normal_form':'IDENTITY' if depth<2 else
        ('LEFT_SELF_RIGHT_OLD_LEFT' if depth==2 else
         ('LEFT_SELF_RIGHT_SENTINEL' if depth%2 else 'BOTH_SELF')),
        'rejection':'GENUINE_DIFF_FALSE' if depth<2 else 'ROOT_HAS_SELF_CLAIM',
        'all_115_fields_verified':ok,
        'raw_DAG_nodes':len(d.nodes)})
print(json.dumps({'audit':'frozen b_splay_event; original DAG constant-folding; 115-field symbolic normal forms; active pins only',
                  'cases':rows,'pass_count':len(rows)},indent=2))
for p in [
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']:
    print('SHA256',hashlib.sha256(Path(p).read_bytes()).hexdigest(),p)
```

### K2. Full high-relation boundary controls

```python
import sys,json,itertools,time
sys.path[:0]=[
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']
from PC_TYPED_DAG import DAG,BOOL
from STRICT_HIGH_COMPILER import build_shigh
from PC_B_CONTROLLER import crank
d=DAG()
H=build_shigh(d,'R8H')
def name(n): return d.nodes[n][3][1]
def put(env,n,v): env[name(n)]=v
def tree(root,phantom):
    kl=[2]*19; kr=[2]*19; rl=[19]*19; rr=[19]*19
    for i in range(1,root+1): kl[i]=0;rl[i]=i-1
    if root==7: kr[7]=0;rr[7]=8
    if phantom: kr[8]=0;rr[8]=19
    lo=[crank(i) for i in range(19)]; hi=list(lo)
    par=[19]*19; dep=[0]*19
    def walk(i,l,h,p,z):
        lo[i]=l;hi[i]=h;par[i]=p;dep[i]=z
        if kl[i]==0 and rl[i]<19: walk(rl[i],l,crank(i)-1,i,z+1)
        if kr[i]==0 and rr[i]<19: walk(rr[i],crank(i)+1,h,i,z+1)
    walk(root,0,18,19,0)
    return dict(root=root,kl=kl,rl=rl,kr=kr,rr=rr,lo=lo,hi=hi),par,dep
def fill_b(env,b,model):
    vals,_,_=model
    put(env,b.root,vals['root'])
    for f in ('kl','rl','kr','rr','lo','hi'):
        for node,val in zip(getattr(b,f),vals[f]):put(env,node,val)
def fill_aux(env,prefix,model):
    for i,(p,z) in enumerate(zip(model[1],model[2])):
        env[f'{prefix}_bpar{i}']=p;env[f'{prefix}_bdep{i}']=z
results=[]
start=time.process_time()
for h in (0,1):
    env={nm:(False if d.nodes[n][1]==BOOL else 0) for nm,n in d.vars.items()}
    source=tree(8 if h==0 else 7,False)
    dest=tree(8,True)
    for state in (H['s'],H['t']):
        for x in state.ak:put(env,x,2)
        put(env,state.aS[0],True);put(env,state.aI[0],8)
    fill_b(env,H['s'].b,source)
    fill_b(env,H['t'].b,dest)
    fill_b(env,H['g'].b,dest)
    for suffix,model in [('sbs',source),('sbt',dest),('sbg',dest)]:
        fill_aux(env,'R8H'+suffix,model)
    put(env,H['g'].v,8)
    env['R8Hbt_bT0']=8;env['R8Hbt_bd0']=18
    path=[8]+([7] if h==1 else [])+[19]*(18-h)
    for k,v in enumerate(path):env[f'R8Hbt_bp0_{k}']=v
    for k in range(18):env[f'R8Hbt_bdir0_{k}']=(h==1 and k==0)
    put(env,H['q'],9);put(env,H['w1'],-3)
    accepted=rejected=0
    for bits in itertools.combinations(range(9),5):
        mu=sum(1<<i for i in bits)
        for obj in (H['s'],H['t'],H['g']):put(env,obj.mu,mu)
        answer=d.ev_ground(H['root'],env)
        assert answer==(8 in bits),(h,bits,answer)
        accepted+=bool(answer);rejected+=not answer
    results.append({'true_depth_h':h,'declared_depth':18,'q':9,'weight':-3,
                    'complete_high_assignments_checked':126,
                    'accepted_masks_containing_8':accepted,
                    'rejected_masks_excluding_8':rejected,
                    'source_root':source[0]['root'],'destination_root':8,
                    'source_clean':True,'destination_chi8':True})
print(json.dumps({'audit':'actual unmodified build_shigh root under complete assignments; no solver',
                  'results':results,'DAG_nodes':len(d.nodes),'cpu_seconds':round(time.process_time()-start,3)},indent=2))
```

### K3. Sharp positive successor

```python
import sys,json,itertools,time
sys.path[:0]=[
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']
from PC_TYPED_DAG import DAG,BOOL
from STRICT_HIGH_COMPILER import build_shigh
from PC_B_CONTROLLER import crank
d=DAG()
H=build_shigh(d,'R8H')
def name(n): return d.nodes[n][3][1]
def put(env,n,v): env[name(n)]=v
def tree(root,phantom):
    kl=[2]*19; kr=[2]*19; rl=[19]*19; rr=[19]*19
    for i in range(1,root+1): kl[i]=0;rl[i]=i-1
    if root==7: kr[7]=0;rr[7]=8
    if phantom: kr[8]=0;rr[8]=19
    lo=[crank(i) for i in range(19)]; hi=list(lo)
    par=[19]*19; dep=[0]*19
    def walk(i,l,h,p,z):
        lo[i]=l;hi[i]=h;par[i]=p;dep[i]=z
        if kl[i]==0 and rl[i]<19: walk(rl[i],l,crank(i)-1,i,z+1)
        if kr[i]==0 and rr[i]<19: walk(rr[i],crank(i)+1,h,i,z+1)
    walk(root,0,18,19,0)
    return dict(root=root,kl=kl,rl=rl,kr=kr,rr=rr,lo=lo,hi=hi),par,dep
def fill_b(env,b,model):
    vals,_,_=model
    put(env,b.root,vals['root'])
    for f in ('kl','rl','kr','rr','lo','hi'):
        for node,val in zip(getattr(b,f),vals[f]):put(env,node,val)
def fill_aux(env,prefix,model):
    for i,(p,z) in enumerate(zip(model[1],model[2])):
        env[f'{prefix}_bpar{i}']=p;env[f'{prefix}_bdep{i}']=z

from PC_B_CONTROLLER import BTrace,b_splay_event
env={nm:(False if d.nodes[n][1]==BOOL else 0) for nm,n in d.vars.items()}
source=tree(8,True)
for state in (H['s'],H['t']):
    for v in state.ak:put(env,v,2)
    put(env,state.aS[0],True);put(env,state.aI[0],8)
for obj in (H['s'],H['t'],H['g']):put(env,obj.mu,391)
put(env,H['g'].v,8)
fill_b(env,H['s'].b,source)
fill_aux(env,'R8Hsbs',source)
env['R8Hbt_bT0']=0;env['R8Hbt_bd0']=8
for k in range(19):env[f'R8Hbt_bp0_{k}']=k if k<=8 else 19
for k in range(18):env[f'R8Hbt_bdir0_{k}']=False
put(env,H['q'],4);put(env,H['w1'],2)
bt=BTrace(d,'R8Hbt')
out=b_splay_event(d,H['s'].b,bt,0,d.const_bool(False))
vals={f:[d.ev_ground(n,env) for n in getattr(out,f)] for f in ('kl','rl','kr','rr')}
vals['root']=d.ev_ground(out.root,env)
lo=[crank(i) for i in range(19)];hi=list(lo);par=[19]*19;dep=[0]*19;seen=set()
def walk(i,l,h,p,z):
    assert i not in seen,('cycle',i)
    seen.add(i);lo[i]=l;hi[i]=h;par[i]=p;dep[i]=z
    for side in ('l','r'):
        k=vals['k'+side][i];ref=vals['r'+side][i]
        if k==0 and ref<19:
            walk(ref,l if side=='l' else crank(i)+1,crank(i)-1 if side=='l' else h,i,z+1)
walk(vals['root'],0,18,19,0)
assert seen==set(range(9)),seen
vals.update(lo=lo,hi=hi)
dest=(vals,par,dep)
fill_b(env,H['t'].b,dest);fill_b(env,H['g'].b,dest)
fill_aux(env,'R8Hsbt',dest);fill_aux(env,'R8Hsbg',dest)
ok=d.ev_ground(H['root'],env)
assert ok
assert vals['root']==0 and vals['kr'][8]==0 and vals['rr'][8]==19
print(json.dumps({'audit':'full frozen high relation: sharp +2 successor from the h=0 negative-edge destination',
    'valid':ok,'mask':391,'target':0,'d':8,'q':4,'w':2,
    'source_root':8,'source_chi8':True,'destination_root':vals['root'],
    'destination_chi8':True,'alpha_source_and_destination_root_label':8,
    'two_edge_prefix_weight':-1,'closed':False,'destination_B':vals,
    'destination_bpar':par,'destination_bdep':dep},indent=2))
```

## L. Integrity and final status

Final integrity verification passed after assembly: branch and HEAD unchanged;
zero tracked-file differences from HEAD; all seven baseline untracked files
retain their original SHA256 hashes; the sole new untracked file is this report.
All three embedded Python programs parse successfully. No inherited report or
production source is modified. Python's report-read check used the Windows
extended-length absolute path because this repository path exceeds MAX_PATH.

IAGS-11G-S03-M2-R8R01 — TERMINAL VERDICT

PRINCIPAL LOCAL THEOREM: PROVED
SIGNED SUCCESSOR CONSEQUENCE: PROVED, LOWER BOUND +2 ATTAINED
h=0 CORRECTION: EXPLICITLY PRESERVED; DIRECT TWO-CYCLE BOUNDARY EXCLUDED
OUTCOME: A FOR THIS LOCAL BOX
M1: OPEN
M2: OPEN
M3: OPEN
STEP 03: OPEN
STEP 04: UNAUTHORIZED
BANK25: 25
NEGATIVE HIGH CYCLE: NONE CERTIFIED
NO SOLVER RUN
NO COMPUTATIONAL SEARCH CAMPAIGN
BOUNDED EXACT CONTROLLER CHECKS EXECUTED AND EMBEDDED ABOVE
NO SOURCE OR GRAPH MODIFICATIONS
NO COMMIT OR PUSH
NO AUTOMATIC SUCCESSOR

HARD STOP

