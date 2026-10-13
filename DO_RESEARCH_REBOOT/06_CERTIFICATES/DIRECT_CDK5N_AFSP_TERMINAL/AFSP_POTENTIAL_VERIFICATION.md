# AFSP_INDEPENDENT_PRODUCT_CHECK.md + AFSP_POTENTIAL_VERIFICATION.md (condensed)

Separation (§20/§24): replay / canonicalization / extraction / allocation /
reconstruction / pumping / macro-gen / product / potential-discovery /
potential-checking implemented as distinct modules with no shared
traversal code beyond engine primitives (splay.py, CRA replay).
Gate-A low product: independently regenerated macros for 600 sampled
states (fresh code path, O(1) reverse index) + dst-existence + domain
filters + inequality vs saved potential: 9,348/9,348 PASS (miss=0).
High-cost max-constraints via one-pass group maxima: 650/650 PASS.
BF stability re-confirmed on load (5 iters). int64 arithmetic (no float,
no overflow: |values| ≤ N·4 ≪ 2^63). Prior 1,081+673 checks superseded
(not relied upon). Sampled—not—exhaustive noted: full-edge re-verification
would re-enumerate 29M edges (same code path as generator for enumeration
+ independent inequality evaluation; performed on 9,998 sampled edges —
sufficient for implementation-agreement evidence, not a second full proof).
