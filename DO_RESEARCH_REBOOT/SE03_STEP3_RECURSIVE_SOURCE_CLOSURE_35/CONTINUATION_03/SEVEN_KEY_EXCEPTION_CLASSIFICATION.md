# SE35 — exhaustive residual classes for DL35 at r=7, core13

Use k=2 and the exact actual source T. Let b count old ancestors with
degree>=3, q the full double count, d the target's old degree, and
kappa=min(q,(2-d)_+). DL3 gives q+2b+d<=6 and b<=q.

First b<=2: b>=3 would require q+2b+d>=9. Also kappa<=2. Thus H>=2
implies 2H>=b+kappa and NO degree-layer hole. For H=1:

* kappa=0 implies b+kappa<=2.
* kappa=1 and d=0 means q=1, so b<=1.
* kappa=1 and d=1 cannot have b>=2, because q>=2 would give q+2b+d>=7.
* Therefore a hole requires kappa=2, hence d=0 and q>=2.

For d=0,q>=2, the positive cases b+2>2 together with q+2b<=6 give
EXACTLY the following necessary, exhaustive classes of source instances:

| Class | H | q | b | Target degree d | DL margin | Comparison holes |
|---|---:|---:|---:|---:|---:|---:|
| E2a | 1 | 2 | 1 | 0 | -1 | 1 |
| E2b | 1 | 2 | 2 | 0 | -2 | 2 |
| E3 | 1 | 3 | 1 | 0 | -1 | 1 |
| E4 | 1 | 4 | 1 | 0 | -1 | 1 |

All q5/q6 macros are nonexceptional for THIS identity, including H1.
No assertion says every abstract tuple is realizable in a closed source.
Every ACTUAL source instance either has a nonnegative DL margin or is in
exactly one of these four rows. Root-repeat and zero-A operations inside
natural macros are retained and do not create an additional genuine macro.

## Exact marked-tree normal forms at saturation

E2b: both path ancestors have degree3, the target is a leaf. Their degree
sum is6, so every other vertex is a leaf. There are exactly two path
ancestors and four off-path leaves, two at each ancestor. This is the
two-degree-three-ancestor form; all key orders and actual physical A/B
embeddings must still obey the original source grammar.

E2a: the two path degrees, in either actual path order, are
(3,1),(3,2),(4,1),(4,2), or(5,1). Nodes not counted by these degrees lie
in the off-path terms; the degree bound limits their total population.

E3: the path degree multiset is(3,1,1), (3,2,1), or(4,1,1).
E4: it is exactly(3,1,1,1), with no unused marked vertex; the high-degree
ancestor has two off-path leaves. Permutations are actual path-order
subcases, not an assumption of dynamic realizability.

This is a finite DEGREE classification backed by an exhaustive integer
bound at fixed support7. It does not enumerate BSTs or use bounded private
populations to stand for arbitrary ones.

## Completed source theorem on the complement

If an original core13 period contains NONE of E2a,E2b,E3,E4, then use

    D=L_2 in[0,4],    c=min(H,3).

For H>=2, 2c>=4>=b+kappa. For H=1 the nonexception condition gives the
same inequality. DL1 proves EVERY original packet inequality. Selected
first2c bits contain all natural h0 owners, since q<=6 and h0 uses the
first min(q,2H) bits. The inherited Type B induction therefore constructs
complete h containing h0. Working <=4+6=10<25, and the actual maximum-D
cut closes empty. Both endpoints transport to I; the fixed auxiliary cut
is unchanged. This is a uniform SOURCE-RESTRICTED credit theorem, allowing
arbitrary A ancestors, private populations, charts and source length.

## Remaining compensation is explicit

Let S be the sum of nonnegative DL margins on nonexceptional macros.
Let E be #E2a+2#E2b+#E3+#E4. The exact closed-period identity is

    2sum min(H,3)-Q = S-E.

This equality is bookkeeping, NOT a proof S>=E. It is not relabeled a
signed repayment theorem. A source-forced physical assignment financing
these losses, including shared occurrences and owners, is still needed
for periods containing exceptions. q2/H1 itself is own-solvent; its
negative DL margin is a degree-potential release, not a CD violation.
