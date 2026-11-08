# PEEL35 — a stronger source route, ACTIVE

Target: every nonempty actual coalition S has m with p_m(S)>=Q_m.
Hypotheses: ROOT35 maximal source domain; p is REM35's exact capacity.
Inheritance: LPR, ATOM35, source snapshots. Dual: an actual source and
nonempty S with p_m<Q_m for every m. Such a witness refutes PEEL35 even
when delta(S)<=0; it does not necessarily refute ROOT35.

The upward bridge is noncircular: remove m, use the smaller |S| instance,
then REM35. Empty coalition has delta0; singleton LPR is also available.
Each induction step strictly decreases the natural number |S| on the
SAME original source. No access/bit/owner is removed from W in this step.

## CORE35 — exact finite recursion theorem, PROVED

Repeatedly remove any m with p_m>=Q_m. The process terminates because
|S| decreases. If it empties the FULL macro set of a fixed W, restrict
that deletion order to any coalition: its remaining neighborhoods form a
subset of the original remaining neighborhoods, so each private capacity
can only increase. The restricted order certifies PEEL35 for EVERY
coalition of that fixed W. Choose Q_m private bits at each deletion;
these selected images are disjoint, since earlier selected bits were
outside every later neighborhood. This gives a raw comparison.

If the process stops nonempty, its terminal core refutes PEEL35 for W.
The terminal core is independent of removal order: any set with every
private capacity<Q cannot lose its first vertex during any deletion
process, since extra surrounding neighborhoods only lower private
capacity. Thus every terminal core contains every other terminal core.
An unpeeled core may have delta<=0; its existence is not a negative cut.
QED.

## Reconstruction and exact remainder

proof170 tested small candidate coalitions solely to falsify PEEL35;
proof171 instead produced complete fixed-W deletion certificates for
all five accepted controls. The latter covers all subsets of EACH fixed
graph, not merely tested subset sizes. It does not quantify over other W.
No negative source witness was found. The compressed-A source is a new
adversarial input, independently checked, with the same limitation.

Uniform PEEL35 remains unproved. Weakening it to 'if delta(S)>0 there
exists a smaller negative subcoalition' does NOT produce a simpler
source lemma: with LPR and finite descent that assertion is equivalent
to ROOT35 (ROOT35 makes it vacuous; the assertion excludes every minimal
negative set). It may not be used as an assumed child proof.

Necessary further debt: derive a source reason why a nonempty private
core is impossible, OR replace peeling by a source-proved collective
exchange/compensation law. Existing certificates do not close this child.
