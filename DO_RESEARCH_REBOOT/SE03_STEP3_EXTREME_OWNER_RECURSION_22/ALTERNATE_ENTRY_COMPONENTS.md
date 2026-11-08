# R22-E — exact compression of multiple physical escape entries

Status: derived finite-map theorem; independent audit pending. This lemma
does not itself assert a source escape is available.

Fix finite actual demand/unit sets D,U, injective frozen a:D0->U and
injective partial source comparison h:D1->U on ONE original licensed I.
Take distinct actual units V outside im(h), supplied by a separate source
rule. For each u in V, begin at u. If it has no a owner it is a free
endpoint. Otherwise continue to d=a^{-1}(u). If h(d) is undefined stop
at that actual demand; otherwise continue at h(d).

## No cycles, no mergers, one-to-one endpoint compression

Every paid demand has exactly one incoming a unit; each unit has at most
one incoming h edge. The entry units have NO incoming h edge. If an entry
path cycled or two distinct entries merged, reversing these unique incoming
predecessors would either give the cycle a second entrance or identify the
two distinct entries. Both are impossible. Finiteness therefore forces
a free unit or undefined comparison demand, and these endpoints are
distinct for different entries.

Thus there is a specified injection

    terminal_h,a : V -> (U\im(a)) disjoint-union (D\dom(h)).

It is constructed by actual paths, not a cardinality assumption. If B
is any proved set containing all possible blocked terminal demands, at
least |V|-|B| entries reach distinct effectively free units. This count
is a consequence of the constructed paths, not a replacement for them.

## New obstruction certificate for alternate-tail attempts

Let R be ALL unpaid original roots of a, and trace their original h paths
before inserting escape edges. Their paths are disjoint by the same
unique-predecessor proof. A V-entry path cannot meet any nonroot vertex
of these paths: that vertex's incoming a unit is already an h value,
whereas backwards uniqueness would require the V-entry to be that h value.
It cannot meet an unpaid root because that root has no a incoming edge.

Therefore if FOUR comparison-unused tail entries at a critical H>=3 Q1
supplier all fail, they give FOUR DISTINCT undefined frontiers in rootless
components of the original h/a system. No fixed-endpoint walk or simple
cycle can explain that failure. This is a smaller falsifiable obstruction
than 'some unknown owner walk may fail'. It still needs a source theorem
excluding or funding those rootless components; they are not impossible
just from injectivity, and arbitrary a may have many of them.

When a prescribed creator map spends some entries first, apply this lemma
only to the ACTUALLY remaining fresh units; do not reuse the four raw bits.
For other immutable comparisons their images must likewise be removed.
All entries and endpoints are actual source IDs, not new credits.
