# S2P adversarial audit — 18 Gate-0 attacks re-affirmed + 8 certification attacks

Gate-0 18 (seam DELETEs in K3-H=13 IV ✓; no a=0 accesses (18 blocks) ✓;
C_K=8 exact ✓; only K3/K5 debts, both paid (K3-Type-P, K5-triple) ✓;
successor q=2 needs nothing (w=0) ✓; second q≤3 covered incl. q=3 case ✓;
second never double-charged (partition-enforced) ✓; K/P overlap once ✓;
seam exception impossible (seam interval is K3's, H=13) ✓; CTL-B two-exception
excluded ✓; no other debts ✓; core 9 all 19 states ✓; serials per access ✓;
CTL-A never used for novelty ✓; K5-AM-G-local-pass handled (global fails) ✓;
forbidden SHA rejected ✓; no banked ACCEPT ✓; no five-key-full/universal claim ✓).

Certification-specific (all PASS = defect ruled out): (a) positive A-costs not
assumed — a=0 allowed, none occur; baseline uses interval sums ✓; (b) DELETEs
in exactly one interval under rotation (each follows one preceding KEEP) ✓;
(c) K/P-eligible second successor never separately charged (partition) ✓;
(d) arbitrary KEEP gaps — intervals grow, H only larger, reserves monotone ✓;
(e) no finite-to-arbitrary-n inference — proof is per-interval arithmetic ✓;
(f) core-nine is hypothesis H1, verified on controls, never fitted ✓; (g) walks
without positive excess still must satisfy H1–H5 to belong (no vacuous pass) ✓;
(h) result stated as restricted S2 only ✓.

No unresolved attack. Promotion may proceed.
