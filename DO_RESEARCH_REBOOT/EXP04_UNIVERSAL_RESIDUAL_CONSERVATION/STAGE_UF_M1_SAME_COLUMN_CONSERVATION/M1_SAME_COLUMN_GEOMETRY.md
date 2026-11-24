# Exact same-column geometry

Use M0's original all-double vertex IDs, original fixed S and priority R>P>C. No comparison or paid-subset forest is substituted.

## One C edge

Let u->v be a C edge, with g=g(u)=g(v), and x_u,x_v the physical targets. Its interval runs from post-full-B(u) through post-A/pre-B(v). These are consecutive uses of g as old grandparent in the **all-double** column. There is no actual A demotion of g and no B promotion of g in the interval. There may be DELETEs, B accesses, losses at g as an old parent, rotations below or above it, and arbitrary internal edge recreation elsewhere.

The complete old-grandparent B output J_g(u) persists through the remainder of its producer splay. With no later promotion of g, rooted descendant sets at g can only shrink. Consequently the full physical frames, as well as their S restrictions, satisfy

\[
F(v)\subseteq J_g(u)\subsetneq F(u),\quad x_v\in J_g(u),\quad x_u\notin J_g(u).
\]

This is inherited completed-output descent, including both SS and OS predecessor shapes. J_g is the original chosen grandparent output; it is not the old-parent output of a P predecessor and not an older cohort endpoint.

## Full A rigidity, including chronology

There is no A access to a strict descendant of g in this interval: splaying that target would physically demote g. There is also no A access to g. Such an access would leave A rooted at g, and the first subsequent different request, at latest the request for x_v!=g, would demote g before v. A non-target A promotion of g in a same-side double is followed by its demotion in the second bit; it cannot evade the no-demotion condition.

Thus every intervening A target avoids the complete A subtree at g. This includes all DELETE helpers and the current A access. Outside-target rigidity preserves its full key set and internal labelled edges throughout; only the external attachment can move. In particular the component at post-A(u) equals the one at pre-B(v). It contains neither x_u nor x_v, since at each of those boundaries A is rooted at that different target.

At the original pre-A boundary of v, g cannot be on the target path: it would be a strict ancestor, hence demoted in the current A phase. Therefore the physical off-path distance ell(v) used in the scoped theorem is defined and positive.

## Continuous ancestry versus continuous edges

The particular relation B:g ancestor of x_v is present immediately after u and survives until pre-B(v), since B descendants of g only shrink. An intervening B access to x_v is impossible: it would put x_v above g and destroy this relation with no permitted later promotion of g to restore it. Other target relations can be lost, and other edges can be destroyed and recreated. No assertion that J_g(u) stays internally rigid throughout this interval is made; an intervening inside target can shrink it while retaining x_v. An identical edge tuple at two times is not a continuous edge run or a new A resource.

Private components remain full physical subtrees. Their movement does not create an A demotion, turn a B promotion into A work, or change original Pi/SET membership. M0's original whole-frame/selected-output labels and each residual's full original beta remain unchanged.

## Evidence bindings

Each HISTORICAL_AUDIT or NEW_AUDIT retains the actual C predecessor, complete rigid A component, original frame/output references, old g, target sequence, primitive intervals and ancestry lifetimes. The corresponding complete PHYS record supplies every full A/B boundary and double pre/post state. Independent edge replay checks the full labelled states and absence of A operands/B promotions of g in each C interval. These finite checks audit the argument; the physical proof is source-uniform.
