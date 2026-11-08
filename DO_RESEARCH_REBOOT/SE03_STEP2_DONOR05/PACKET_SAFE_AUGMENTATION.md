# A paired-source safe augmentation, and its exact limitation

This is a new source version of the inherited safe augmentation, with
the q5/q1 packet checked explicitly. It does not presume the old one-
macro theorem applies to a segment containing two genuine B changes.

For a synchronized full-source boundary s=(A,B,M), let q(x) be the
actual full B double count of a nonroot marked x. For a=1 or2 define
E_a(s) by all of the following:

* Every marked target with q(x)=5 has initial A depth>4.
* Every marked target with q(x)<=4 and A depth<=2 has q(x)<=2-a.
* Every marked target with q(x)<=4 and A depth<=4 has q(x)<=4-a.

All marked targets are tested, even ones whose B path would not preserve
the closed maximal core; this is a safe overapproximation. These source
predicates depend only on the actual current trees and marks. They
introduce no graph field, private inventory or selected outgoing word.
Let L(s) be the largest a in{1,2} satisfying E_a, or0 if neither does.

For EVERY full segment of the paired partition leaving E_a,

    w=2min(H,4)-Q >= a.                              (1)

For a singleton of H1 orH2, the completed target-cover lemma gives
initial A depth(x)<=2H, and the two displayed bounds give (1). Singleton
H>=3 has q<=4 and price>=2. If a q5/q1 pair had Hsum<=3, its first
natural macro would have Hfirst<=2, since the successor requires at
least one A event. Target cover would put its first q5 target within
initial A depth4, contradicting the first E_a condition. A pair of
Hsum>=4 has price8-6=2. This proves (1), including arbitrary anonymous
helpers, nongenuine KEEPs, DELETEs and all zero operations.

For ANY function F in[0,2], put Fplus=max(F,L). Every individually
F-valid full-segment inequality remains Fplus-valid. If its source is
not raised, only the target increases. If raised, its new value L(s)>0
is at most w by (1), and the target is nonnegative. This is the same
universal safe-raising proof as before, with its missing pair case now
separately justified.

For the explicit negative seed psi11 in NEGATIVE_SEED_CORE11.md, the
candidate D0=max(psi11,L) therefore preserves all proved negative,
H2-helper, paired-zero and range rows. The remaining candidate obligations
are full singleton H1/q1 and H1/q2. ZETA_SOURCE_OBSTRUCTION.md proves
that this D0 does NOT settle those obligations. Safe augmentation must
not be presented as a feasible seed or as full Step2 closure.
