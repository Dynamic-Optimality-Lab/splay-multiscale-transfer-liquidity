# DH-01 Frozen Deep Edge Inventory

Low (OO): w = 2H - q, H = sum active event ceil(d_A/2) (DELETE included),
q from terminal B-depth; weights -4..4 observed (-2..4 certified low in
corpus; -4 imported UNSAT scope; -3 UNKNOWN retained). High (contracted):
E^H_w(s,t) iff exists m: E^OM_w(s,m) AND E^MO_0(m,t), same m; w = 6 - q;
all weights -4..6 in scope (anomalous -3 UNKNOWN included; -4 UNSAT scope
imported). Negative deep-involved stored edges: 8 (all 10: dmax 8->5/4;
E4-style collapses). No stored deep self-loops; single-rotation analysis
implies no self-loop can carry w<0 only if terminal B-change is
established per edge (stated, not universally proved — see micro-lemma
doc). Parallel edges preserved with provenance throughout.
