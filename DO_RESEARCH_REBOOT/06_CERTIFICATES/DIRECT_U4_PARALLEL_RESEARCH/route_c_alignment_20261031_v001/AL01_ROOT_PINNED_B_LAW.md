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
