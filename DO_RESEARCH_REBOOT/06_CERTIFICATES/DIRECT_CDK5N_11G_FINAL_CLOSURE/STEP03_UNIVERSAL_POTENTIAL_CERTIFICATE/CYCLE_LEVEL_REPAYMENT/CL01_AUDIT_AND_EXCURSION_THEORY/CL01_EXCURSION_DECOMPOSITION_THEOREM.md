# CL-01 Excursion Decomposition Theorem (PROVED)

Let g be any vertex-defined {0,1} guard (here dmax>=7). Every closed walk
is exactly one of: TYPE L (all g=0), TYPE H (all g=1), TYPE M (mixed).
For TYPE M, fix a cyclic start at a shallow vertex; scanning forward,
cut at each 0->1 (excursion start) and each subsequent first 1->0
(excursion end): yields maximal deep excursions
u0 -01-> v1 -11-> ... -11-> vk -10-> u1 with all vi deep, endpoints
shallow; remaining edges are 00. PROVED: (1) partition exists (start
exists since mixed; cuts well-defined); (2) every edge in exactly one
piece (cuts alternate forced by guard values); (3) nothing omitted
(scan covers all edges); (4) no double count; (5) endpoints match by
construction (consecutive edges share vertices); (6) weights sum
(addition assoc/comm); (7-11) repeated vertices/parallel/zero/high/arbitrary
length all admitted (no simplicity/finiteness beyond the walk itself);
(12) no lift needed (pure endpoint equality). No weight/sign hypothesis.
