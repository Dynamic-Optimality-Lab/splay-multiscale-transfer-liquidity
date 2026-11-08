# Reuse of deterministic completed controls

The prototype completed22 support cases (through pair2,7),66 original
predicate checks,22 full O/M closure checks and22 negative controls before
its recorded stop. Those successful cases must not be recomputed merely
because later fixture code removes a duplicate pure assertion. The second
prototype repeated a subset without adding a case; its CPU is retained.

Record the observed completed-case list and pin the original program.
Its deterministic input recipe, source compilers, table files and fixture
code are immutable. Removing a pure assert does not change a returned
environment; no random/global source inputs occur. Reuse those completed
checks, without claiming their lost in-memory rows were saved. The final
audit stores fresh raw interfaces/environments for the REMAINING23 cases,
and explicit reproduction recipes/provenance for the22 reused cases.

Further preparation-only optimization: construct fixture A alpha directly
from the proper prefix and mathematical splay, instead of executing all
inactive branches of the old eager Exact A interpreter. Keep PORT/EMPTY
kinds distinct, no A ghosts are introduced in these fixtures. This follows
from the already audited typed side-pair rotation and shadow definitions;
the unchanged production root still validates every new total environment.
All other fixture assertions/fields remain unchanged. No production source,
transition graph, evaluator, backend, case, coordinate or cap changes.

All prototype CPU, the outer-helper phase and remaining audit CPU share
the ORIGINAL300-second cap. Add a conservative one-second stop margin
per interrupted process. Stop before reaching that sum. Reuse is an exact
deterministic-work identity, not case thinning or UNKNOWN-as-PASS.
