# Signed ancestor-incidence object and gap identity (P1)

## Definition

M = five genuine KEEP keys of the walk. For pair state P, marked x ∈ M,
ambient z ≠ x: Ω_P(x,z) = 1[z ∈ Anc_{B_P}(x)] − 1[z ∈ Anc_{A_P}(x)] ∈
{−1,0,1} (proper ancestors). Second argument ranges over the ENTIRE ambient
key universe (probe: ambient = all tree keys, e.g. 9 keys → 5×8=40 coords;
Control A: 15 nonzero before, 8 after, 19 changed).

## Identity (P1)

g_P(x) = Σ_{z≠x} Ω_P(x,z). Proof: d_{B}(x) = |Anc_B(x)| (edge-count = number
of proper ancestors; root depth 0 ✓); likewise d_A. Subtract: d_B−d_A =
Σ_z(1[z∈Anc_B]−1[z∈Anc_A]) = Σ_z Ω. Finite sums, no convergence issues;
holds for every ambient size, marked or not. ∎ (Verified computationally:
gap vectors from Ω-sums match replay dB−dA on all 5 frozen walks, all
boundaries — see MIG_replay certs + probe log.)

## Limitation (frozen)

Nonzero-coordinate count is NOT credit: one rotation alters many coords
(Control A E3: 19 changed in one access); one paid access alters many;
deficits reuse relationships; B-KEEP rotations create disparity at a=0
(Control B: 14 coords changed, a=0). Coordinate counting without a
source-cost capacity bound is forbidden (see double-spend audit).
