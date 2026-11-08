# Uniform off-path leaf lifting of a certified primitive

Let T be an ordered BST and x its accessed key. If z is a leaf different
from x, it is outside the search path. Replace the ENTIRE leaf term
z(L,R) by one ordered free gap variable, preserving its identity as payload.
The root-to-x search path, every actual event, and all path operand keys
are unchanged. Each of the six ordinary source formulas is a tree term
in its off-path subtrees; simultaneous substitution of this payload
therefore commutes with every rotation. Reinsert the SAME payload in the
destination's corresponding ordered gap. This recovers the exact full
destination, with the same StepEv count. It changes no actual access,
key, event, mark or physical BST. It is a proof substitution only.

If T has n>=10 known nodes and the primitive has H<=2, some leaf differs
from x. Otherwise x is the sole leaf, T is Hamiltonian of depth n-1,
and H=ceil((n-1)/2)>=5, a contradiction. In particular EVERY positive
H1/H2 action on10 anchors is an order-renamed/gap-substituted instance of
one ALREADY CERTIFIED nine-anchor primitive. Root identities are literal.
This is a uniform structural source proof, not a population passing test.

The payload may carry marked keys or a key accessed later. It must only
be off THIS access path. It is fully restored before the next primitive;
the full ten-key state is retained. This primitive-lifting theorem does
not assert that one fixed globally untouched gap contains all private
accesses, or that the nine-anchor FUNDING potential lifts unchanged.

Resource convention: old native nine-anchor source rows and their checked
free-gap identities are reused. New gap substitutions are recorded as
source-schema instantiations, not fresh calls of an ordinary splay engine.
They are charged as symbolic work. The independent checker must validate
the substitution proof and derive the complete low relation using another
leaf choice. It may not claim new semantic replays or external verification.
The main theorem/funding coefficients require a separate complete check.
