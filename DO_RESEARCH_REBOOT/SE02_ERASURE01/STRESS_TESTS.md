# Analytic source-family stress tests; no finite instances executed

## 1. Inherited positive-marginal RR/LL family

For T_R=y(A,p(B,z(C,D))), the full period Kz,Ky has one direct and one positive
indirect B-double marginal. The proposed protected rule admits it when A also
starts with the allowed reversible y-to-z path: the first A event has two units
and the block is a paired identity. It assigns bit0 to Kz and bit1 to Ky.
The erased period's B work is0, and contraction removes the whole paired
identity. Thus no sign assumption on interference is smuggled into the rule.
Reflection gives the LL/RR family with identical physical accounting.

## 2. Arbitrarily many root repetitions and DELETEs

Permit arbitrary nonempty mode words on the z-run and on the y-run, each
containing at least one KEEP. The first access to each key is A's only real
event in that run, even if it is DELETE; the first KEEP is B's only genuine
event in that run, even if A is already rooted there. All remaining operations
are identities for the relevant tree. This proves the same D=1,J=1,A=2
per block for unbounded run lengths. The donor ID is the first SOURCE A event,
not an invented event at the later starved KEEP. Different blocks/copies keep
different IDs; no unit from the reaching prefix or another lap is reused.

## 3. Negative interference exists

Take D=w(E,F) in the inherited RR source family, with w>z. After full Kz, w
is at depth1, whereas after erasure it is still at depth3. A retained Kw then
contributes-1 to the indirect sum. This source-local identity is not a closed
counterexample, and is not a protected two-run block. It rejects a proposed
global J>=0 law just as the return-y family rejects J<=0. The general signed
decomposition retains both possibilities.

## 4. Missing producer: a false credit rule is rejected

Start a local B RR/LL pulse with A already at z (for example the reachable
pair (T_L,T_R) obtained by a preceding Dz from the diagonal T_R). The local
Kz has a=0: there is no first-z A event to donate. Its return Ky changes A's
tree from T_L to T_R rather than restoring its input A. Counting the earlier
Dz unit from outside the selected block would be an unauthorized boundary
borrow. This local pulse FAILS our guard. No claim is made that it cannot be
paid by a different valid mechanism on a larger closed source interval.

## 5. Zigzag A paths are not reversible two-run identities

The unqualified assertion that every grandchild splay followed by the old-root
return restores A is false. With y<z<p,

    y(empty,p(z,empty)) --S_z--> z(y,p)
                        --S_y--> y(empty,z(empty,p)).

The last full tree differs from the first. Source LR/RL doubles and the return
ZIG prove this symbolically. The protected rule excludes this A geometry;
it does not quietly weaken full closure to equal roots.

## 6. Interleaved third keys

If an unrelated key occurs between arrival at z and return to y, full and
erased splay words on later retained accesses may differ. The primitive
depth-update/parity equations still hold, but the paired-identity contraction
and the D=J=1 calculation are no longer justified. Such intervals fail the
contiguous two-run guard; no convenient key-selection assumption admits them.

## 7. Transients and multiple periods

For arbitrary input walks use the aligned I=[uN,(u+L)N) construction and subtract
the transient marginal exactly. Protected block-boundary cuts have u=0,L=1.
An input cut in the active B phase has first erased charge Q0+1, then recurrent
charge Q0, giving u=1,L=1. Its first-period marginal is2m-1 rather than2m;
the aligned recurrent marginal is2m. No transient unit pays an aligned demand.
The compensation interval is selected at a block boundary, preserving
reachability while keeping each donor and its consumers inside that period.
Repeating L physical copies multiplies D,J,capacities and distinct IDs by L.
No single-period demand is compared with an unnormalized multi-period charge.

All seven stress categories are algebraic/term proofs over arbitrary source
hangers, modes and repetitions. No concrete tree, larger core graph, finite
population search, old certificate row or source witness was run.
