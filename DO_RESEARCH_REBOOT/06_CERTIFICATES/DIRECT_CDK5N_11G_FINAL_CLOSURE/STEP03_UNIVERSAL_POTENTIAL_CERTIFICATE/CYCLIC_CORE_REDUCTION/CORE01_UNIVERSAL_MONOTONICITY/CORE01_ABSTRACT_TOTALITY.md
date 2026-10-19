# CORE-01 Abstract Totality + Reference Identity (Gate A4/A5, E1)

rho(s) = |C_mu(b_s)|: total on every 147-field state (finite BFS walk;
no solver needed). Range on valid states: observed {5..9} on 110+ sampled
endpoints; theoretical range 0..19 (5 marked nodes + ancestors; root-span
[0,18] bounds depth). Reference semantics: slot index i IS S-index i for
core slots (compiler construction: BState arrays indexed over NB with
NCORE core; mu bit i; crank; verified consistent across ssertify envs,
T-A tests, and feature code). Ancestor relation from b_parent_of muxes
over all 19 slots. No physical-identity claim beyond indices is needed:
inclusion C(t) subset C(s) is an index-set statement, stable across the
edge by construction.
