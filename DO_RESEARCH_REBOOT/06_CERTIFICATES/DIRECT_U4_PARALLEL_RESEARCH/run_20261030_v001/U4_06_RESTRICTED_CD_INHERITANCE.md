# Restricted inheritance and arbitrary marked sets

[DO_RESEARCH_REBOOT/02_PROVED/DIRECT_NFKS_RT2_three_keep_key_coarse_double.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/02_PROVED/DIRECT_NFKS_RT2_three_keep_key_coarse_double.md>): root-return +2,
idempotence and depth<=4 yield Q<=2C_KEEP<=2C_full<=2A for at most three KEEP keys.
[DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CD_K4_four_keep_key_coarse_double.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CD_K4_four_keep_key_coarse_double.md>): arbitrary-M marked-core
reduction and a 68,876-transition one-bit certificate prove the four-key class.
[DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CDK5_LOW_five_key_submaximal_core.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CDK5_LOW_five_key_submaximal_core.md>): five-key core<=8,
28,477 vertices/142,385 retained transitions, an explicit 0/1 potential and the same A charging.
These are scoped proof components; this run read their proofs/certificate definitions, but
did not rerun those complete older matrices or promote their union to a universal theorem.

Arbitrary-M core growth: a marked splay never adds an ancestor-core member; an unmarked
splay increases its size by at most2, because only the first mark-acquiring StepEv can grow
it. Start a cyclic period just after one marked root; adding successive first-visited targets
gives1+2(k-1)=2k-1, exact B closure transfers it to the start, and a rotated seam covers all
boundaries. Pruning mark-free hanging subtrees commutes with marked splay, preserving depths.
With M fixed, marked splays give core-set inclusion; cyclic closure therefore fixes the set.

The old CDK5_LOW_source_reduction_proof paragraph asserting arbitrary label swapping is
superseded by Stage11F's inclusion/constancy proof: an old mark-free hanger is rigid and
cannot acquire a descendant mark from outside; all rotating operands already lie on a
marked path. Its size-only overapproximation still suffices for the earlier finite certificate.

For k=5: core<=9,dB<=8,q<=4, so positive individual overflow has a=0,q1..4 or a=1,q3..4.
This is arithmetic, not payment. For k=6: core<=11 allows the arithmetic type a=2,q=5
with overflow1; no physical closed six-support witness of that type is claimed by this run.
No theorem reduces KEEP-support cardinality. Our second counterexample lies EXACTLY in
the five-genuine-key/nine-core physical domain and leaves every scalar theorem intact.
