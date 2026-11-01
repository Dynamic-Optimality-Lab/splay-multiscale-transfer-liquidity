# Exact Hall obstruction outside the claimed E0 normal form

Start A=B=the right vine 1->2->3->4->5->6->7. Execute

    D6 D7 K7 D6 K6 D5 K5 D4 K4 D3 K3 D2 K2 D1 K1.

|0-based access|operation|dA|a|dB|q|z|
|---|---|---|---|---|---|---|
|0|D6|5|3|-|0|0|
|1|D7|1|1|-|0|0|
|2|K7|0|0|6|3|0|
|3|D6|1|1|-|0|0|
|4|K6|0|0|3|1|1|
|5|D5|3|2|-|0|0|
|6|K5|0|0|2|1|0|
|7|D4|2|1|-|0|0|
|8|K4|0|0|1|0|1|
|9|D3|1|1|-|0|0|
|10|K3|0|0|2|1|0|
|11|D2|2|1|-|0|0|
|12|K2|0|0|1|0|1|
|13|D1|1|1|-|0|0|
|14|K1|0|0|1|0|1|

Both complete trees return EXACTLY to the initial right vine; the initial state is diagonal,
so no reachability prefix is needed. Every KEEP has a=0. A=11,Q=6,Z=4,B=10,R=6,S=22.
In particular Q-2A=-16: scalar Coarse-Double holds.

Let X be the three K7 doubles at access2, sequences0,1,2. Their triples are respectively
(7,6,5),(7,4,3),(7,2,1), all RR. Cyclic creator indices from the original replay are6,10,14
modulo15, all in the previous period, all zero-cost KEEPs. Latest positive A arrival of7
is D7 at access1, with exactly one StepEv. Therefore the COMPLETE neighborhood is
{(1,0,0),(1,0,1)}. |X|=3>2=|Gamma(X)|. Every proper subset satisfies Hall.
Original matching is5/6; an independent exhaustive matching and all64 Hall subsets agree.

There is NO nonstarved KEEP competitor anywhere. The earlier inference 'shared setup
credits force a nonstarved co-namer' confuses demands with accesses. All three demands
from K7 already share both credits. This is an actual source-realizable minimal deficiency
outside E0's required s<t<u<t' with a positive-A-cost competing KEEP.

E0's equation (q_t-2a_s)+(q_t'-2a_t')=1 is valid only for the stated two-access/full-demand/
zero-fat graph with no further eligible positive pools. Fat pools must be distinct before
subtracting their capacities; partial demand subsets need their actual cardinalities.
E0-overfull is a sufficient Hall obstruction under those assumptions, not a universal normal form.
[the historical correction](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/audits/PIVOT_18R_CLOSE.md:15>) already withdrew necessity.
Our witness supplies an exact physical falsification of the earlier stronger bridge.

L3 erratum: q>=2a+1 is equivalent to dB>=4a+2, not4a+1. The historical n<=8 examples
dB=6/7 for a=1 are consistent with the corrected threshold.

[u4_counterexample_certificate.json](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/u4_counterexample_certificate.json>) includes every state, event, creator, credit,
adjacency and closure. [independent_witness_and_route_c.json](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/independent_witness_and_route_c.json>) records the independent check.

Formatting revision v002; mathematical content unchanged, v001 preserved.
