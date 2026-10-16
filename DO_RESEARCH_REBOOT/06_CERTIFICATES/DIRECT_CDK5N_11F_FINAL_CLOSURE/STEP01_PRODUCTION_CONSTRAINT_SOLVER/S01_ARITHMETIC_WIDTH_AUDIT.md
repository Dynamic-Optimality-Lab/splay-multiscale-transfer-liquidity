# S01_ARITHMETIC_WIDTH_AUDIT.md — machine audit in S01_ARITHMETIC_WIDTH_AUDIT.json

- Low-relation symbol table: 9544 vars (2796 Bool, 6748 Int). Exactly ONE signed
  variable: `SL_w`, 5-bit, domain [-16,15] (carries low weights -4..4 and high
  selector values). All other ints unsigned, widths {2,3,4,5,7,8,9}.
- Witness interface: `SL_H` 2-bit [0,3] (values 1-2 used); `SLbt_q` 4-bit [0,15]
  (values 0-9 used); `SL_w` as above.
- Encoding consequence: Int-exactness makes wraparound IMPOSSIBLE BY CONSTRUCTION
  (no bitvectors anywhere); width metadata survives only as finite-domain bounds,
  which additionally reject out-of-domain pins as UNSAT (`domain-violation`).
- Adversarial proof: `(v+1)==0` with `v=2^32-1` is UNSAT (would be SAT under
  32-bit wraparound); signed `-4<0` SAT / `-3<=-4` UNSAT; `6-9==-3` SAT;
  150/150 exhaustive 1-2-bit agreements incl. boundary values 0..3.
- Intermediate widths (ADD/SUB width tags up to 33) are carried as metadata only;
  Z3 computes exact sums/differences. No silent signed/unsigned reinterpretation:
  Int comparisons are sign-correct for negative constants by construction.
