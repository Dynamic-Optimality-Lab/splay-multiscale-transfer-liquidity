# KEEP35 — source order of every external KEEP retirement, PROVED

Target: constrain an operation that supplies a retirement pool shared with
a later demand. Conditions: C34 maximal source, actual last genuine g
birth, an operation t before the consumer's terminal KEEP, and g still an
old marked B ancestor of consumer target x. Inheritance: C15 only the
accessed marked key grows descendants; ordinary BST order; AR1/OR34.
Dual: a permitted foreign KEEP retirement with the opposite strict order.
Bridge: narrows source-realizable overlap; it does not imply capacity.

No intervening KEEP target lies strictly between g and x after that last
g birth. Such a target y would become the full B root and separate g
from x into opposite sides. Since g is not genuinely accessed afterward,
its marked descendants cannot grow to include x again. This contradicts
its old-ancestor status at the consumer.

Now suppose t is a KEEP of y and A loses g's ancestry of x there. If the
pivot g rotates right, ordinary source geometry gives y<g and x<g.
Immediately after the KEEP, full B is rooted at y, and g must still be
an ancestor of x there: its descendants can only shrink until the consumer.
Both g and x must be on y's right, so

    y < x < g.

For a left retirement the reflected conclusion is g<x<y. Equality y=x
would already remove g's B ancestry of x, so is impossible for a foreign
operation in this birth interval. The consumer's own terminal operation
is explicitly excluded. Nongenuine KEEPs are included, since B still has
root y. A-only DELETEs need not obey this order. QED.

Consequently, among genuine KEEP producers and consumers, right-only
retirement dependencies strictly increase target key; left-only ones
strictly decrease it. A directed cycle made of those edges must mix
directions. This does not rule out cycles using DELETEs, nongenuine
operations whose natural host has another target, or mixed directions.
It is not a new private-capacity or free-donor theorem.
