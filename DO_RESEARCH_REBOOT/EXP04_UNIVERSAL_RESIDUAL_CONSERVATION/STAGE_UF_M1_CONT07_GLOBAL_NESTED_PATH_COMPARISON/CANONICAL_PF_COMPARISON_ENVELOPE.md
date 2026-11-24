# GC-A: exact canonical workload and decomposition

Use C5's preceding ORIGINAL C_old parent, never merely physical index-noncheap adjacency. Exclude full endpoint B phases in the reset/promotion test. First C_old parents of actual A-demotion epochs are E_old boundaries; other eligible parents have the unique reset-free predecessor. No-reset columns use their cyclic lists, possibly a preceding-lap same-ID copy. C6 proves that each nonempty epochless list has a PM edge. Cut PM edges and epoch boundaries: the remaining PF edges form finite maximal paths b=(w0,...,wr), with common old g, no copied events counted as new work.

F_(i+1) subseteq J_i proper-subset F_i holds on COMPLETE physical sets at their respective timestamps. It composes for the same g, and also strictly nests the completed J_i. Each endpoint B phase itself has no promotion of g: lower doubles are below it, its double demotes it, and higher steps transport its output. Thus the entire lifted block from post-B(w0) through B(wr) is promotion-free. A_g is rigid. Different columns need not be laminar.

Let B0 be actual post-B(w0), T_b its full rooted component at g, P_b the root-to-g path INCLUDING g in B0. For side s, H_b^s is the sequence of ALL original KEEPs in this block whose target lies in the actual pre-access B_g and on side s of g. Left hits strictly increase; right hits strictly decrease. Every target is distinct on a side. C6's one-sided shadow starts from B0 and retains exactly H_b^s. Define

    J_b^s = union_(x in H_b^s) path_B0(root,x),
    I_b^s = union_(x in H_b^s) path_T_b(g,x) minus {g}.

If H is empty both domains are empty and there is no shadow. Otherwise J_b^s=P_b disjoint-union I_b^s. The left and right I sets are disjoint; their intersection with P is empty. Let k_b be the number of nonempty sides. Then EXACTLY

    M_PF = sum_b,s |J_b^s|
         = M_stem + M_hit + M_padding,
    M_stem = sum_b k_b |P_b|,
    M_hit = sum_b,s |H_b^s|,
    M_padding = sum_b,s (|I_b^s|-|H_b^s|).

M_inside:=M_hit+M_padding=sum|I|. These are classifications of INITIAL DOMAIN KEYS, with path/side occurrence IDs. M_hit is also the number of retained accesses because targets on each side are distinct. It is not the physical number of PF vertices, number of C_old edges, number of prehybrid gaps, or literal post-hybrid gap weight. Padding includes initial path nodes that are not retained targets. Do not add M_hit again as scan cost after charging M_PF.

The comparison itself has no required return to its initial state. Sequential access controls its rotations, including initialization, by Q_shadow<=C_seq |J| under the inherited convention. There is no additional real closure operation hidden in M_PF, and no original source work donated by copying an initial state.

For actual rho in S_PF its original parent has an incoming PF edge on one unique path. It is retained in its target's side shadow, and C6's active-side coupling matches the original old grandparent/double. Distinct parents within a shadow have distinct original operation/double destinations; at most3 original gap slots share each. Therefore

    |S_PF|<=3 sum Q_shadow<=3 C_seq M_PF.

This proof preserves literal IDs/fibers and invokes the SAME pinned classical sequential-access interface. It does not reprove that external theorem or fund M_PF. INHERITED_PATH_WORKLOADS supplies the complete canonical graph/workload for the48 known native-accounting controls. Other historical native scopes remain explicit rather than assumed empty.
