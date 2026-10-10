# MRP interval partition (PROVED — exact cyclic identities with seam)

Cyclic KEEPs K_0..K_{s−1} (s≥5 by H1: five genuine keys ⇒ s≥5). I_j = accesses
strictly after KEEP j−1 (mod s) through KEEP j. Disjoint cover (each access
follows one preceding KEEP); wraparound interval uses exact closure for endpoint
consistency. c_j/H_j/q_j/w_j=q_j−2c_j/R_j=2(H_j−c_j) per frozen defs. ΣH_j=A
(DELETE StepEvs counted once — each DELETE in one I_j; seam DELETEs included,
none duplicated, no prefix inserted). Σq_j=Q_B (DELETEs q=0). Σc_j=C_K. Hence
Σw_j=Q_B−2C_K, ΣR_j=2(A−C_K). C_X never substituted. (Structure shared with
banked partition lemmas; re-proved here from source + closure because the
multi-packet charging depends on the exact seam accounting — cited scope, not
oracle.)
