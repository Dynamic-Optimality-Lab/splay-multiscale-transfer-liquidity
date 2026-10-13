# WQ_HIGH_COST_FIBERS.md + WQ_MIDPOINT_EQUIVALENCE.md (condensed proofs)

Fibers (STEP 03/HF-1): g=(μ,σ,b',v); S_g = incidences with B-successor b';
D_g = compatible A-destinations (root v, same mask/signature); E_high =
∪_g{(s,t,6−q(s,v))} complete bipartite per fiber (conservative
overapproximation; abstract feasibility ≠ original realizability).
Weights source-side-only (6−q(s,v) depends on s via B-depth, never t).
Midpoint (HF-2): m_g per nonempty fiber; s→m_g (6−q) + m_g→t (0);
five-point equivalence proved algebraically (expansion/contraction preserve
edges/weights/cycles; fiber separation by private mids; empty fibers
emit nothing). Grouped constraints Ψ(g)≤Φ(s)+6−q, Φ(t)≤Ψ(g) eliminate to
max_D Φ ≤ min_S (Φ+6−q) (exact equivalence, complete-bipartite premise).
Tests: group algebra 400/400; cycle preservation 400/400 (faithful model;
two test-model bugs fixed and documented — sparse-fiber and shared-mid
variants correctly excluded as out-of-construction). Status: PROVED.
