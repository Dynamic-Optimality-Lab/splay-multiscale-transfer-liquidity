# DS35 — descending maxima with intervening minimum return

Status: mathematical derivation complete; symbolic identity audit pending
at initial publication. No numeric access replay is needed for this proof.

Let a=x0<x1<...<xk be the complete keys of an ordered BST with root xk.
Its left subtree is arbitrary. The ordinary bottom-up access word

    a,x(k-1),a,x(k-2), ... ,a,x1,a

returns the right vine a,x1,...,xk. For k=1 the word is just a.

Proof by descending induction. Before a stage the root is xi, all lower
keys are in its left subtree, and its right subtree is the right vine
x(i+1),...,xk. Accessing a can change the lower tree and xi's position,
but cannot touch any edge strictly inside that high right vine: all its
keys exceed both forthcoming targets. Accessing p=x(i-1) then puts p at
the root. The only keys above p are xi,...,xk. Their internal high vine
has not changed, and xi has no possible left key in this set, since p and
xi are consecutive. Thus the new right subtree is exactly xi,...,xk;
all lower keys lie to the left of p. This is the next induction invariant.
At root x1, the final access a leaves the full right vine. QED.

This proof concerns ALL keys of the displayed BST. Applying it to a
marked projection needs a separate commutation argument; it does not
authorize contraction of active unary anonymous ancestors.

## Legal application to the new anchored source family

At T from RESET_CLUSTER_LOWER_BOUND.md every even key below m is a
mark-free leaf. During accesses only to odd keys <=m these leaves are
rigid off-path operands: no such leaf can become a pivot, gain a marked
descendant or split. The whole high term m.right=(n-1,empty,n) is also
off every lower search path. Erasing JUST these rigid operands therefore
commutes frame-by-frame with ordinary splaying on all odd keys <=m.
This is an inactive-hanger argument, not the false active-unary quotient.

After the forward anchored word the maximum odd key m is the A root.
The reverse word of the immutable B witness is exactly DS35 on the odd
keys 1,3,...,m. The final projected A is their right vine. Each even leaf
has only one legal attachment to that vine (left of its next odd key),
and the high term remains attached at m.right. Thus the FULL actual A
tree after forward followed by reverse is exactly T.

This identifies the previously symbolic Av as T, for this whole family.
It does not claim the same return for arbitrary source frames, extra
active ancestors or arbitrary placements of private keys.
