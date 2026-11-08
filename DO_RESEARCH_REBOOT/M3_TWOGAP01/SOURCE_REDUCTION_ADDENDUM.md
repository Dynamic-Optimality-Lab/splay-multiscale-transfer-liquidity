# Normal-form scope check for the two-unit signature

The old dependency ledger groups several single-gap lemmas together. Only
the following charge and path facts are reused here; fixed-gap allocation
determinacy and the old three-anonymous-node pruning are NOT reused.

Every original active target is a present real node. By root termination
and no repetition its A path is the real current parent chain (AER01's
erasure/path induction). Therefore A depth0 is a literal root identity,
including all carried G pairs; a positive event has cost ceil(d/2)>=1.
Every KEEP ends with its A root corresponding to its B target. If the B
splay changes the root, the segment since the last synchronized boundary
must contain a positive A event: a sequence of root identities cannot
change that common target. This injects successive changing B KEEPs,
including the genuine terminal KEEP, into positive A-charge segments.

For H1, only the genuine terminal B change is possible. There is exactly
one positive A event, of depth1/2. If the terminal KEEP is zero-charge,
that event's target is the terminal target: after it every A event is a
root identity. It is a core target because the terminal is genuine.
Deleting zero-charge events and, if necessary, replacing the charged
DELETE followed by root KEEP with that single core access preserves
every final A child pair, including all G pairs. B's only changing event
is that core splay, so actual terminal q and the full endpoint interface
are unchanged. No anonymous-population assumption enters this argument.

For H2 with an internal preterminal fringe, the source charge bound allows
only one earlier changing B KEEP. It is the fringe KEEP that made that
gap internal. The root-gap opposite-side argument in H2R01 excludes an
interior gap: its opposite core side remains nonempty through the terminal
core splay, contradicting the final childless-gap endpoint. Gap9 is absent
under the PRESENT fixed sigma, in either chi8 region. Thus the helper is
gap0. The helper and genuine terminal changes require two positive A
segments, exhausting H2; each segment has one depth1/2 event. Within a
segment a zero-charge KEEP has the same actual A target as its preceding
charged event. There is at most one present anonymous gap0 node here,
so its label is unambiguously f0. Removing root identities yields exactly
(f0,x), with original endpoints/H and the actual B terminal q preserved.
This proof retains the original slot0 object even when its current depth
changes. It does not replace all H2 macros by H1.

When all preterminal gaps remain childless (Gamma0), earlier unmarked
core KEEPs may change B. Do not remove them or use macro-entry credit.
The inherited H2R01 terminal-debt theorem, explicitly stated there for
arbitrary signatures, is sufficient: q3/4 implies psi(core_t)>=q-2.
For q<=2 use the potential range. No A profile is needed in this case.

Source anchors: STRICT_LOW_COMPILER.build_slow's budget, active target,
root_terminated, same_keep_target and no_intermediate_genuine constraints;
PC_ROTATION_INTERPRETER.splay_event/macro_H; WSIGN02D universal charge-
change injection; H2R01 sections D/E (terminal floor and opposite-side
root-gap argument); H1F01's direct charge-segment normalization; AER01
real-path/side-pair induction. The extension above spells out why those
facts remain applicable here despite the old grouped ledger's one-gap
scope. The only new representation step is the all-branch prefix union.
