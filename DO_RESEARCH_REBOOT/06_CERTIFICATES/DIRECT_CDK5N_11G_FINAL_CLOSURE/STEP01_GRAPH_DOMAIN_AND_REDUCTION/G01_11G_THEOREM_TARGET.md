# G01_11G_THEOREM_TARGET.md — NonNegCycles(G_star) and its implication (Phase A)

Required graph theorem for Step 04:

\[

\boxed{\operatorname{NonNegCycles}(G_\star):\quad
\forall P\text{ closed in }G_\star,\; w(P)\ge0.}

\]

Mandatory implication (proved here, premise reserved for Steps 02-03):

\[

\boxed{\operatorname{NonNegCycles}(G_\star)
\Longrightarrow
\forall W\in\mathcal W_5^9,\; Q_B(W)\le2A(W).}

\]

Proof. Let W in W_5^9. By the certified Stage 11F simulation there is a closed
P in G_AF (hence in G_star, by the coverage theorem) with
w(P) <= 2A(W) - Q_B(W). NonNegCycles(G_star) gives 0 <= w(P). Chaining,
0 <= 2A(W) - Q_B(W), i.e. Q_B(W) <= 2A(W). The implication uses only the
existence of ONE such P per W plus the universal lower bound — no uniformity
beyond Step-04's verification. (This does not claim the terminal inequality
until NonNegCycles is proved; that proof belongs to Steps 02-04.)
