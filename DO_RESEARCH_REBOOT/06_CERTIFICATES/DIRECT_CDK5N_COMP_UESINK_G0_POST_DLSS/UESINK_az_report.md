# UESINK AZ report

- Entry `6bf8781` (branch/remote/hashes/status); 22-bank record intact.
- Post-DLSS census reconstructed: 378 direct (MSINK 160, DLSS 125, MR 122,
  VR 73, AMG 9, AMS 6, NP 8, S1 12) + 6 cyclic + 0 residual = 384.
- IN (a7c6504c, 56/36/16): strict member (E=[12], t=2, sink p=0 H=18,
  others strict-K/P), 22/22 negative, primitive ⇒ outside C22*.
- Control (6b242e23): strict-DLSS member (sink p=8) ⇒ not OUT (supporting).
- Distance-zero: 1 member + 4 banked, 0 OUT, 0 indeterminate → mutant search.
- OUT frozen at in-L1 idx8 rm19 (593b3f3a, 32 acc, 56/36/16; H2-fail |E|=0;
  22/22 negative; primitive). First qualifying in global order (idx0,1,5,6,7
  non-closed; idx2,3 member; idx4 MSINK-banked). No L2 anywhere.
- L1–L7 + C9 relay-independence + ambient core-nine proof; K-erratum filed
  (strict predicates only; Q−2A recomputed).
- 73 adversarial attacks PASS + fault injections detected; R1–R4 PASS.
- OUTCOME A (Gate-0 only). No promotion, no mutation, no successor.
