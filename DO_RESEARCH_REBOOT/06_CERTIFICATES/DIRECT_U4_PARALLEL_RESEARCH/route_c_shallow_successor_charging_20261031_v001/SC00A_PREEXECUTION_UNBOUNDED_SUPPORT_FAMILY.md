# Preexecution unbounded support consequence of the fixed witness

This addendum is recorded before any producer or source-audit execution. It adds no finite sample, search, formula, or charging mechanism to SC00.

The same local prefix admits an analytic family with unbounded KEEP support, rather than only arbitrary unrequested fringes. For every n>=7, start at the diagonal R_n, use prefix D7,D6, and freeze

    K7 K2 K3 ... Kn
    K1 K2 ... Kn
    K(n-1) ... K1 D7 D6.

The initial two KEEPs use only keys <=7, so the right fringe R_[8,n] stays attached to key 7. The fixed seven-key source calculation showing synchronization at K2 therefore lifts unchanged. All remaining KEEPs act on identical trees and are termwise nonpositive. The full ascending and descending passes restore R_n; final D7,D6 restore the cycle's initial A tree while B stays R_n.

The source proof of ascending-pass synchronization is the usual exact invariant: after accessing k the entire prefix 1,...,k is the left spine below root k, while larger keys are in the right subtree; the next successor is the minimum of that right subtree, so its splay retains the old prefix as its left spine. Reflection proves descending synchronization. This is the same connector identity already used in prior certificates, not an open traversal conjecture.

Thus the seven-key local computation and the common-pass identity determine the entire family. Its only positive block is expected to remain the first K7; its next key is 2 rather than former root 1, and the first former-root return occurs beyond three successors. Every key is a KEEP target. This gives a planned strict-coverage family outside the named AJ-AS and <=5-support domains at arbitrarily large support, without fitting or evaluating another size.

The finite audit remains exactly n=7 plus reflection and the n=4 sharp transport control plus reflection. Promotion still requires the source calculations, disjoint-credit proof and novelty exclusions to pass. All other gate conditions and the no-successor stop remain unchanged.
