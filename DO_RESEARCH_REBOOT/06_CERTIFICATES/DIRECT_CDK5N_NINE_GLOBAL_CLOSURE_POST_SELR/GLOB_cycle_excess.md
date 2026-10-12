# GLOB cycle-excess identity + E3/E4 classification (§5)

Partition closed walk into cyclic KEEP intervals I_j (prev KEEP exclusive
through current KEEP inclusive; each access exactly once; seam by closure).
c_j=1[x_j≠x_{j-1}]; H_j=Σa; q_j=terminal KEEP B-cost; w_j=q_j−2c_j;
R_j=2(H_j−c_j); C_K=Σc. Then ΣH=A, Σq=Q, Σc=C_K (verified on SELR-OUT:
53/36/16; code: CRA intervals + totals). Hence Σw=Q−2C_K, ΣR=2(A−C_K).
Intervalwise w_j−R_j=q_j−2H_j=:δ_j, so Q_B−2A=Σδ_j (exact accounting).
Root-change baseline: H_j≥c_j (c=0 trivial; c=1/H=0 freezes A-root,
contradicting different-key KEEP; same proof as banked L-docs).
Core-nine ⇒ q≤4; c=0 ⇒ q=0 (B rooted+frozen at prev key). Thus δ_j>0
needs H_j=1, q_j∈{3,4} (if H=0 then q≤2c=0...; if H≥2 then q−2H≤4−4=0).
Define E3={H=1,q=3} (δ=1), E4={H=1,q=4} (δ=2); all else δ≤0. Target:
|E3|+2|E4| ≤ Σ_{∉E3∪E4}(2H−q) (conclusion, never premise).
