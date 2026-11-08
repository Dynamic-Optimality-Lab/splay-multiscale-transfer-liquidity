# Uniform core deficiency and exact auxiliary funding domains

Status: structural theorems proved from the inherited arbitrary-mark core
growth lemma and exact original outer rotations. They do not prove signed
repayment or a new original CD class. No population, core-shape or mask tests
are used. The campaign continues on the resulting residual obligations.

## 1. A nonnegative integer deficiency budget for every cyclic cut

Let a nonempty original B-closed period have r>=2 genuine KEEP keys M and
fixed labeled core S of size c. Cut immediately after a genuine KEEP of x.
Initialize V={x}; its current core is the root singleton of size1. Traverse
one complete period, growing V only at each first visit of a new KEEP key.
There are exactly r-1 such additions; at the end V=M and the tree has
returned, so the current V-core has size c.

For a first new target, the original unmarked-access lemma for the current
V gives an increase of at most2 in its core. The target is the new root,
already in the resulting nonempty V-core, so adjoining it to V adds no node.
Write its size increment g_i<=2 and define loss ell_i=2-g_i>=0. This definition
also allows a negative g_i. For a repeated visited target, marked-splay
inclusion gives g_i<=0; define loss ell_i=-g_i>=0. DELETEs freeze B and have
g_i=ell_i=0. Nongenuine root repeats also have0. Thus exact summation yields

    c-1 = 2(r-1) - sum ell_i,
    sum ell_i = 2r-1-c =: delta.                            (1)

The losses are nonnegative integers. Therefore at most delta unit losses
can occur in ANY such growing-visited traversal. If delta=0, every first
new target increases its visited core by exactly2 and every revisit preserves
it. This is valid separately at every cyclic cut; no sum over different
cuts is asserted and the same loss is not spent multiple times.

## 2. Maximal cores forbid odd-depth and outer mixed genuine accesses

Fix ANY genuine KEEP y and cut after its preceding genuine KEEP x, ignoring
intervening B identities. Then y is the first new visited target. At that
point V={x}, x is the B root and y!=x. After splaying y, the core of {x,y}
is exactly the root-to-x path, of size1+d_after(x).

Read the last source event of this ordinary splay. If y's original depth
is odd, the terminal ZIG makes the old root x a child: d_after(x)=1. If
its depth is even, the outermost double uses x as its grandparent. The
source LL/RR identities put x at depth2; LR/RL put it at depth1. These are
all possibilities for a nonroot present target. Thus the first increment
is1 or2, with value2 exactly for EVEN depth and outer LL or RR.

If c=2r-1 then delta=0 in (1), so this increment must be2. Consequently

    maximal closed core => every genuine KEEP has even positive depth
                           and its last double is LL or RR.          (2)

Nongenuine KEEPs remain permitted with depth0. The statement concerns the
OUTERMOST double; inner doubles may be mixed. No upper bound on their count
is implied. In particular (2) does not restore the rejected fixed HIGH price.

More generally, a genuine access with odd depth or outer LR/RL certifies
c<=2r-2. It does not certify a numerical negative CD weight or counterexample.

## 3. A marked leaf supplies a uniformly smaller erased core

At any chosen full boundary every leaf of the marked ancestor core S is
marked: an unmarked leaf would not lie on a path to any mark. For r>=2
choose such a marked leaf z. It is not the root singleton. Removing its
mark makes z absent from C_(M\{z})(B_start), because no remaining mark lies
below that leaf. Therefore this smaller marked core is a SUBSET of S\{z}
and has size at most c-1.

Erase every Kz and use the inherited recurrent alignment from this boundary.
All remaining B accesses are marked in M0=M\{z}; their ancestor core is
nonincreasing as a labeled set. Thus throughout the erased history, including
its preperiod and recurrent block,

    c_E <= c-1,    c_E <= 2(r-1)-1 = 2r-3.                 (3)

The second inequality applies to the closed recurrent block by the inherited
all-support core bound; if its genuine support is smaller it only improves.
The erased core bound does not require full and erased B trees to rejoin.
The cut is reachable by following the original reaching prefix and the
appropriate finite part of the closed walk. All A events are retained here.

## 4. Exact six-key domain consequences

For r=6 and c<=9, leaf selection gives c_E<=8 and erased genuine support<=5.
Consequently the completed RT2/K4/K5-LOW B-only theorems give Q_E<=2C_E on
the correctly aligned auxiliary period. This is a legitimate stronger
funding premise on this SELECTED domain, not a strengthening of scalar CD(5).

The residual six-key cores are c=10 or11. A leaf only supplies c_E<=9 there.
Core11 has delta0 and hence every genuine full KEEP satisfies (2). Core10
has delta1 in each growing-visited traversal. Auxiliary five-key/core9
histories remain a necessary funding case unless a further proved selection
theorem avoids them; no such theorem is asserted. Even for c<=9, Q_E<=2C_E
does not itself reserve enough capacity for general nonrejoining D+J.

For arbitrary r the statements (1)-(3) are uniform. Their consequences are
geometric restrictions, not a uniform repayment or complete CD reduction.
No theorem here says that a source-complete favorable erased key exists for
the signed bound. The universal induction gate remains OPEN.
