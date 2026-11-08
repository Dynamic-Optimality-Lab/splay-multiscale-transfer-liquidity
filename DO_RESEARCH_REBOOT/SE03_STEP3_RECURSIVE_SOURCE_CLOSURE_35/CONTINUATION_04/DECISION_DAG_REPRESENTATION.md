# Exact coefficient decision DAG and scheduling correction

For each fixed A-root class, order its actual full A trees by the pinned
source enumeration. Pad its numerical debt vector with zeros to a power
of two. A terminal v represents the constant value v over the current
index interval. A binary node stores two child IDs for its two halves.
Collapse only two equal CONSTANT children. Intern equal child pairs.
An actual B tree retains its own root pointer and root-class domain.

Induction on interval length proves exact evaluation: terminal evaluation
is constant; an internal node chooses the actual index's half and invokes
the corresponding exact child. Building only the branches of updated
indices preserves every other coefficient. Sharing equal subfunctions
does not identify A/B states or source edges. This is partial-function
sharing, rather than merely bit-packing a larger independent table.

Keep only reachable DAG nodes; node IDs are never reused. A cached merge
result may be used only while its root is still live. The interval-image
cache still uses actual root classes and literal full-source rows. Count
live DAG nodes, cache cells, source states and stored relation edges
against the unchanged caps. No budget is raised or reset.

The conversion exports an exact old-profile-to-DAG-root map and checks
every coefficient before search resumes. A separate decoder independently
checks it. Derived caches are not source evidence or new physical credit.

## v2 scheduling correction

search_global_probe11_LOW_v2.py reused an exact merged profile on a cache
hit but omitted enqueuing the changed target B column. Thus propagation
could be incomplete. Its reported status was CHECKPOINT, not a completed
certificate. The numerical values remain genuine monotone path lower
bounds: the cached merge uses literal original-source inequalities.

The corrected DAG engine schedules every changed target, including cached
merges, and begins with ALL B columns pending. This repairs the scheduling
omission without erasing either old checkpoint, receipt or CPU charge.
No positive theorem is inferred from the incomplete old scan. Its negative
cycle test, if it had produced a witness, would still have required literal
source closure and independent replay; it produced none.
