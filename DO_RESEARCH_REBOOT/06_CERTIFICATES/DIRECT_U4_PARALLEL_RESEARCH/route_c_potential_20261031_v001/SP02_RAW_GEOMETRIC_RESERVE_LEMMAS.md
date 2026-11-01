# Uniform positive bounds for the raw geometric reserve, and its precise failure

These are source-exact ALL-SIZE partial laws. They do not make G a complete potential.

## 1. Finite binary mass budget

For r=1/8, at depth j a binary A tree has at most2^j nodes. Therefore

    sum_y r^{d_A(y)} < sum_{j>=0}(2r)^j = 4/3,
    sum_{y!=root(A)} r^{d_A(y)} < 1/3.

No key-count or balanced-tree assumption enters this bound.

## 2. Every root-conditioned B splay repays q

Assume A is rooted at the accessed key x. Keep A frozen and splay x in B, whose initial x-depth is d. The banked physical source lemma 26AL-L1 states that every other key's B depth increases by at most2 under one whole splay. Key x, of A-weight1, drops its B depth by d. Thus, for d>=1,

    G(A,S_xB)-G(A,B) <= -d + 2*sum_{y!=x} r^{d_A(y)}
                     <= -d+2/3
                     <= -floor(d/2)-1/3.

For d=0 the B tree is unchanged. Hence every starved KEEP, including a zero-demand B zig, is paid by G, uniformly in n and every fringe configuration.

Source dependency: DO_RESEARCH_REBOOT/02_PROVED/26AL_generalized_signed_repayment.md, 26AL-L1, derived there from the bottom-up frame/source rotation geometry. No Coarse-Double or U4 claim is a premise.

This directly handles the CONSUMER part of every overwritten-setup family: no latest-arrival credit pool is used. It does not say that the preparatory DELETEs obey G's budget.

## 3. Both arbitrary-fringe zero-helper branches are safe for G

Use the source-exact H0(C),HL(C),HR(C) family of route_c_analytic_20261030_v001/RA02. Since G(A,B)=partial_w H(r,1), its exact whole-access changes are

    Delta G_L = -r-5r^2 = -13/64,
    Delta G_R = -r-6r^2+r^3+C(r,1).

The fringe is attached at A depth5, so C(r,1)=r^5 sum_{y in U}r^{d_U(y)} <= r^5/(1-2r)=1/24576. Consequently

    Delta G_R <= -111/512+1/24576 = -5327/24576 < 0.

Both helpers have a=1,q=2 and require nonincrease. These inequalities hold for arbitrary m and arbitrary internal A/B fringe shapes, also after reflection. Exponential A-depth damping defeats the earlier unbounded passive-fringe DEPTH-MOMENT increase here. No fringe-size fit is used.

## 4. G still fails the DELETE law

Let n>=6, let M be ANY BST on2..n-1, and set

    A = 1(empty,n(M,empty)),
    B = 2(1, right-vine on3..n).

DELETE n is one A zig. The middle subtree M keeps its A depths, while weights at1 and n swap1 and r. Since d_B(1)=1 and d_B(n)=n-2,

    Delta G=(1-r)(n-3)=7(n-3)/8.

This exceeds the2a=2 budget at n>=6 (n6 gives21/8). Thus G is NOT a potential satisfying the complete source inequality. Its starved-consumer and specific zero-helper successes cannot be promoted to survival of whole overwritten-setup histories.

The repair Psi addresses exactly this missing A-motion budget. The next document proves that repair's law and exposes its failure on B repayment.
