# One explicit uniform A/B potential candidate

Fix r=1/8. For same-key finite BSTs define

    G(A,B)=sum_y 8^{-d_A(y)} d_B(y),
    Psi(A,B)=max_T [G(T,B)-rho(A,T)],

where T ranges over all BSTs on the SAME ordered key set and rho is the undirected unit-cost primitive rotation distance. No coefficient, potential label or distribution is fitted. Primitive rotations connect the finite BST set, for example by transformation through a right vine, so the maximum is finite and attained. This is one constructive function for every n; computational efficiency is not a proof premise.

This formula is an explicit static optimization, not maximum future Pair Access excess. Its data are only the current A,B and a separately specified primitive metric. No cycle-sign/feasibility assumption is embedded in the definition. It uses full A geometry, not just its root or a fixed shadow.

G itself lies in the historically refuted additive joint-depth family and is NOT proposed as a complete potential. Its useful partial bounds are proved separately in SP02. Psi is the nonlinear repair being audited: it is not rho(A,B), and it is not an arbitrary assignment of unknown potential values.

The max-envelope construction was not found in the inspected repository sources. This is a scoped repository observation, not a literature novelty claim. Old failures and constraints were read before this test: PIVOT_CONSTRAINT_GUIDED_DUAL.md, REWEIGHTING_BRIDGE_AUDIT.md, wp6_rotdist.py and the existing Route C analytic reports.

Raw G is not the final answer. The principal question is whether its root-conditioned B repayment survives the repair that guarantees the A/DELETE law. SP03 gives both the successful A law and an analytic NO for that transfer.
