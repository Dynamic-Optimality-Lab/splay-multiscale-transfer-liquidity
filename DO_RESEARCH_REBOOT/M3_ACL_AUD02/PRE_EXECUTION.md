# ACL-AUD02 — Adversarial source-completeness audit and repair gate

User requests correction of gaps before further M3 work. This audit is
required before treating ACL01 as a premise. All prior research/source/Git
read-only. New writes only this folder. Python -B, existing exact Int DAG,
same R1-R4 and caps: 4m DAG, 2m diagnostic states, 5m edges, 1m queries,
120 CPU finite phase / 300 CPU original audit. No solver or installs.

Source issue: Witness.child_bound_prop checks kind-0 child refs only for
c in0..126, but cleft/cright have width8. wellformed restricts kinds, not
kind-0 refs. Thus a present node may carry kind0/ref255 without that pair
attaching a present child. A.mux_ref reads invalid indices as slot0.
ACL01's ordinary prefix grammar assumes every kind0 child names a real
present slot. That implication requires verification and may be false.

Principal task: prove ACL01's source completeness or certify an original
low edge missing from its grammar/potential, then repair if a credible
bounded construction exists. First audit is strictly bounded mutation
of saved TRUE original controls: replace a physically empty child by
kind0/ref127 or255, rederive BOTH shared shadows with original interpreter,
and evaluate the unchanged full low root and claimed Q inequality.
Save all accepted environments and any negative residual. No mutant
source constraint or hidden observable is added. A negative residual
refutes the claimed Q, not M3 or all other potentials.

R1: finite typed-reference boundary audit, rather than global M3.
R2: exact source default-index semantics and existing TRUE environments;
no new existence premise. Invalid pairs cannot be path operands on the
chosen valid event paths, but can affect their observed shadows.
R3: one source-completeness obligation, one exact source attack; if the
mechanism fails, stop and correct status before any further pivot.
R4: success repairs a mandatory source bridge; failure withdraws the
unsupported ACL01 universal-sector promotion. Finite physical/singleton
certificates remain at their established scope. No negative cycle claim.

Next mechanisms need a fresh gate AFTER this audit result. In particular
do not proceed to all-mask fitting using an unestablished lifting premise.
