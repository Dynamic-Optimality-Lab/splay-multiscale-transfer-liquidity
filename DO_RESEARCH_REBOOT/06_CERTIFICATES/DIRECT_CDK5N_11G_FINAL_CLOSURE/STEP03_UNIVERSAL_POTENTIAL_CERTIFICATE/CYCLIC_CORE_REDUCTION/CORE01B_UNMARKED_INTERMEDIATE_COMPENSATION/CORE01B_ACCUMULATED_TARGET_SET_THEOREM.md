# CORE-01B Accumulated Target-Set Theorem (PROVED conditional form)

Let C_0..C_n be marked closures along a low macro (DELETE/inactive =
identity steps). By the eventwise lemma, C_i subset C_{i-1} union R_i
where R_i = rotated children of event i. By induction:
C_n subset C_0 union R, R = union of all rotated children.
MARKED-TARGET COROLLARY: if every rotated child in every B-changing event
is already in C at its rotation time (in particular: every B-changing
event's splay path[0] is marked, since path nodes are its ancestors),
then the union adds nothing new and C_n subset C_0 (strong inclusion).
Single-event genuine KEEPs satisfy this unconditionally (terminal marked;
only its path rotated). Multi-event macros satisfy it IFF all
B-changing intermediate targets are marked — which A8 does NOT enforce.
