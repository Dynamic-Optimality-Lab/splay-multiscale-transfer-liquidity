# Exact finite refutation of the joint LRF template

STATUS: REFUTED — EXACT for the saved reduced SH567 system with the listed homogeneous LRF equalities. This does not refute unrestricted J4, ROW-DIAMETER, COARSE-DOUBLE, or Dynamic Optimality.

The stored reduced inequality matrix has shape 26,823×163 and integer entries/RHS (although serialized as float64). It is the n=5,6,7 shared J4 system after the source's finite UG, rho=c and NONE reductions. Let its constraints be A x≥r. Let Gx=0 be the extra LRF equalities from j4_lrflist.json (with the gauge row if present).

The 15 nonnegative inequality multipliers and three equality multipliers saved by the floating discovery routine reconstruct to exact rational numbers. Independently checking all 163 columns gives y^T A+w^T G=0 and y^T r=9/34>0. Therefore every purported solution would satisfy 0=(y^T A+w^T G)x≥9/34, a contradiction.

Every multiplier, row index, original SELF/DIAM shape/node metadata, reduced RHS and equality coordinate is recorded in 06_CERTIFICATES/LRF_EXACT_RECHECK.json. Original generator row order is n-size block, then shape index, then n SELF rows and n(n−1) ordered DIAM rows. The certificate binds the saved reduced matrix by SHA-256 in 11_REPRODUCIBILITY/evidence_metadata.json. It does not certify that the reduced extra constraints are universally mandatory.

Sources: scripts/wp6_lrffarkas.py; scripts/wp6_rednorm.py; artifacts/v04/wp6_present/0909c74a/dual_mine/j4_rednorm_mat.npz, j4_lrffarkas.json, j4_lrflist.json. Recheck: python -B DO_RESEARCH_REBOOT/11_REPRODUCIBILITY/inspect_evidence.py. No source solver or writer was run.
