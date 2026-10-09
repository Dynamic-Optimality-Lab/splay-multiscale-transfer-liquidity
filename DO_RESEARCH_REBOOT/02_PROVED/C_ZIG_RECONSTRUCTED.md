# C.ZIG — reconstructed universal mathematical proof

STATUS: PROVED — UNIVERSAL on finite closed present-key Pair Access walks. Formal tree/run assembly was not rerun or completed here.

For any finite nonempty fixed key set K, a valid pair state is (A_tree,B_tree). KEEP x splays both trees; DELETE x splays only A_tree and freezes B_tree. DELETE is a mask operation, not deletion of a BST key. Write a_i=ceil(d_A(x_i)/2), b_i=ceil(d_B(x_i)/2) on KEEP, and b_i=0 on DELETE; z_i=d_B(x_i) mod 2 on KEEP and 0 on DELETE. A=sum a_i and Z_B=sum z_i. For every closed pair walk, Z_B≤A.

Proof. Present-key splay at a root is a no-op; a nonroot splay produces at least one StepEv and makes its key the root. If all a_i=0, A_tree is constant and every key is its root r. After the first KEEP r, B_tree is rooted at r forever. Closure forces B_tree to have been rooted at r already if there is any KEEP, or B_tree never changes. Thus Z_B=0.

Otherwise view the walk cyclically and partition it into blocks, each beginning with one access L having a_L≥1, followed by all consecutive A-no-op accesses until the next nontrivial A access. Since L makes its key r the A root, every later access in its block is to r. If L is KEEP, its B splay has at most one zig; all later KEEP r accesses are B-root no-ops. If L is DELETE, it has no B event; only the first later KEEP r can have a zig, and all further KEEP r accesses are B-root no-ops. In either case the block has at most one B zig. Charge that zig, if present, to one StepEv of L. Blocks have different leading accesses, so charges are injective. Hence Z_B≤number of nontrivial A accesses≤sum a_i. Empty walks satisfy the inequality as well.

Dependencies: validity/key preservation and ordinary bottom-up splay mechanics. These are definitional operations, not a finite-corpus premise. No reachability or size bound is needed. The theorem is for closed walks: a prefix starting with a long A-no-op run may use initial B work and is handled later by startup overhead.

Source: audits/PIVOT_RECURRENT_EXCESS.md:136 onward contains this run proof; scripts/wp6_cycle_ratio.py:58-100 defines pair transitions and StepEv counts; python/independent/splay.py and python/liquidity/legacy_embedding.py define present splay. Source formalization tasks V1–V3 remain; this reconstruction does not claim their kernel completion.
