# Required guard on OR35's reduced syntax

OR35 proves completeness FROM actual runs. Turning the representation into
a transition syntax also requires this explicit guard; ordinary unannotated
unary contraction is not used.

Retain the identity and empty/nonempty status of every contracted ordered
unary context. A legal reduced H1 event must use only marked root/target
and, for a double, a parent in the fixed entry P0 if that parent is
anonymous. Its ACTIVE root-to-target path cannot cross a nonempty inactive
context. Side hangers may contain such contexts and move only whole.

Why essential: symbolically let the path be marked y, a nonempty anonymous
unary context C of length ell>=1, anonymous p, marked x. Actual depth is
ell+2>=3 and actual cost is at least2. Contracting C without a barrier would
falsely make x a depth2 H1 target. This is an algebraic source-family
counterargument, not a new concrete source-engine replay or a CD witness.

With the guard, root-to-target operands in the full tree are precisely
the named reduced operands; each ordinary zig/double formula reattaches
the same full ordered contexts without entering them. Induction lifts the
ENTIRE guarded reduced run on any fixed original context assignment,
preserving all operations, exact StepEv counts and unit labels. Conversely
OR35 shows every original H1 run satisfies these guards. This is the
source-exact transition correspondence at a supplied incoming state.

For complete-history reachability or closure retain the original context
assignments and full source evidence. An abstract cycle with unequal
context endpoints, or an initial pair not realized from the original
source, is not promoted to a countercertificate. Finite skeleton syntax
does not prove any new sign or erase this source-realization requirement.
