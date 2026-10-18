# G02_NEGATIVE_CYCLE_LEMMA.md — simple-cycle + k=1 theorems (Phase D/Gate G)

Lemma (simple cycles suffice): a negative closed walk exists iff a negative
SIMPLE directed cycle exists. Proof: decompose any closed walk into simple
cycles (repeated-vertex splitting); total weight is the sum of parts; a negative
total forces a negative part. Contrapositive gives the reverse. Hence Step-02
search may restrict to simple cycles without losing existence (BFS visited-set
uses this: revisiting a state continues from the first visit's frontier).

k=1 theorem (no solver needed): a genuine single-KEEP closed walk is impossible
(genuine KEEP changes B by source definition, so B_T != B_0). Nongenuine single
KEEPs have dB=0 (root target, identity), hence q=0 and w = 2H-0 = 2H >= 0
(a>=0 per event, H>=0). No negative 1-edge closed walk exists. Both used as
preregistered search bounds (k=1 proved UNSAT; k=2 exhaustive 342 words).
