# Exact sparse source regeneration, without retaining zero-state edges

This is a representation/algorithm theorem, not a source sign theorem.
No new CPU or query cap is implied. The pending implementation must be
independently checked before it is used as a certificate producer.

## One private branch is recoverable from its full contraction set

Fix any finite ordered anchor set V and one private key p in a known gap.
Ignore rigid mark-free payloads, which cannot affect any known-key search
path. Let Pi(A) be ALL ordered contractions of p. If p is unary, Pi is a
singleton and the prescribed value is the old anchor debt. If p branches,
Pi determines the entire known-key A tree uniquely.

Proof. Outside p's subtree every contraction has exactly the same context.
At p its left and right old trees L,R are both nonempty. Their root keys
are different; the full merge set contains a tree rooted at root(L) and
one rooted at root(R). The first varying root slot of Pi is therefore
exactly p's former slot. This identifies its whole common outer context.
For any merge in this slot, delete all keys above p by one-sided pruning:
at such an upper node keep its left child. The result is L. Symmetrically
pruning the keys below p gives R. These assertions follow immediately
by induction on the defining two possible root choices of ordered merge.
Thus p(L,R), and hence A, is recovered. Arbitrary mark-free payloads are
not claimed recoverable and are not a state variable of this source law.

Consequently mutable profiles (B,Pi) can be represented by (A,B) for the
branched private node; known-key duplicates are aliases, not new values.
This does not make the state space small: it explains why full Pi carries
essentially the whole nonunary A geometry in the saved construction.

## Implicit zero and exact outgoing regeneration

For each branched (A,B) let J start at0 and keep only positive lower labels
and their causal derivations. Unary endpoints retain their old prescribed
coefficient. Generate every declared original LOW source edge eventually.
For an edge of price w update its mutable target to max(J(t),J(s)-w), or
check that bound against its prescribed fixed target value. Whenever a
mutable label rises, regenerate ALL its source-valid outgoing edges.

This has the same least lower-label closure as storing every zero state
and every edge: an omitted mutable value is EXACTLY0, not unknown. A new
edge is checked at the current label. Every later rise of its source
checks it again by regeneration. If the source never rises, its check is
already final. Fixed-source edges are checked during complete generation;
fixed values never rise. These cases exhaust all inequalities. Fixed-to-
fixed rows retain the accepted uniform unary-endpoint source theorem.

Regeneration must use the SAME complete original action grammar and the
accepted source kernel, not a guessed projected graph. In the present
grammar it is direct H1/H2 anchor access, or H1 DELETE followed by H1
terminal anchor access, retaining the original start root and genuine
terminal constraints. The private node is never a B target. The actual B
transition/cost is its already checked native source matrix row. No HIGH
law or arbitrary-private-population lifting is established by this LOW
representation theorem.

An old processed source prefix remains processed when its positive labels,
source cursor, original A enumeration, completed action cache and causal
records are retained. A conversion may conservatively queue all positive
mutable states, including previously processed ones, but that is avoidable:
if a source row was fully generated and all pending propagation finished,
its current outgoing inequalities were already checked. Queue only the
positive source rows not yet fully generated; any FUTURE rise queues the
whole source row. This reuses completed checks without losing future ones.

Every counterderivation retains actual source edge data and parent snapshot
IDs. Losing a stored adjacency list loses no mathematical premise because
its complete source generator is retained. A passing prefix remains only
a passing prefix. A terminal closure certificate still needs complete
generation and a separate verifier. No source theorem, original event,
frozen owner, resource cap or previously accepted receipt is altered.
