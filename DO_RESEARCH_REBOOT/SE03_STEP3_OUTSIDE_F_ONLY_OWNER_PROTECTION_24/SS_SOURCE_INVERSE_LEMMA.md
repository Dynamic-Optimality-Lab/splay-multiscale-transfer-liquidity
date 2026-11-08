# O24-S — a source-word inverse for an all-SS splay

Status: NEW symbolic proof, independent audit pending. No replay executed.

Suppose an ordinary access to marked x has even depth2q and consists
entirely of zig-zig doubles. Write its old marked ancestors ROOT-first
as a1,...,aq, with one intervening unmarked path vertex per pair.
All off-path subtrees are full ordered physical terms.

Define a KEEP target word recursively:

    R()=empty;
    R(a1,...,aq) = [a1] followed by
                   [z,a1] for each successive z in R(a2,...,aq).

THEOREM. After the original access x, this word returns the COMPLETE B
tree exactly to its state before x. Every access in R is itself all-SS,
and its targets are original marked ancestors. Its length is2^q-1.

Proof by q. The q=0 case is an identity. The last double of S_x rotates
the old root a1 through its unmarked child and x. In the result a1 is
the outer grandchild of x. Access a1 performs the inverse SS double,
restoring the original top two vertices; the lower subtree is still
S_x(T2), where T2 was the subtree rooted at a2 on the original path.
By induction R(a2,...,aq) restores T2 when executed inside that subtree.
Each such local access z is simulated globally by KEEP z, KEEP a1:
the former executes its local SS steps then one final SS through the
fixed top pair, and the latter undoes just that final top SS. Every key
of T2 lies in the same original ordered child interval, so these top
steps remain outer SS in either orientation. Thus the top pair and all
its private terms stay fixed while the lower induction runs. At the end
the complete original tree is restored. The recurrence for length is
Lq=1+2L(q-1), L0=0. No passive rotation or invented key access is used.

For a finite word of all-SS marked accesses, undo the last access by its
R word, then the penultimate, and so forth. Each inverse restores the
exact preceding physical state, so the original ancestor lists apply.
This gives a finite original-source return word, including arbitrary
ordered private terms and reflection. It is not an inverse cost identity:
the return word generates additional actual A/B events.

This lemma is used only to construct a source-valid adversarial family
in SOURCE_EXACT_EXTERNAL_OWNER_CONTROL. It does not assert that arbitrary
non-SS splay programs have this inverse or that existing histories must
contain its compensating accesses.
