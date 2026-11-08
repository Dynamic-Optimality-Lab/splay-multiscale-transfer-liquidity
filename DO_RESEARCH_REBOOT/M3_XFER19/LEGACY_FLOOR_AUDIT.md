# Independent guard/provenance audit of the reused lower floors

This audits LOWER bounds, not a claim that the translated function is the
complete saved debt. A false lower bound would invalidate the new proof,
so missing guards and missing old augmentations are treated differently:
an omitted augmentation weakens a lower bound safely; an omitted theorem
hypothesis would be unsound. The following blocks were compared to the
actual named theorem definitions, with all old files independently pinned.

* XFER01 Q: exactly one real nonroot child Score x, all other observed
  positions nonreal; the capacity min(2,4-floor(d(x)/2)) supplies threshold1
  at d<=7 and threshold2 at d<=5. Root/nonreal unused fields stay free.
* XFER02 R: first two marks a<b, the literal PORT branch and V={other};
  both depth thresholds use that same capacity. PORT is10, EMPTY12, and
  they are never merged. Actual opposite predicates use the last pair.
* XFER03 S/T/L: S is ONLY one credit, with b4/5, root b, LL=a,d(a)<=3;
  T and L are two-credit with the original V and PORT guards. No S cap2.
* XFER04 J and05 Z: J5/J6 retain the exact upper constructors and V subset
  {4..8}; J retains the unmarked Score separator a<k<4; Z permits any kind0
  parent at L with LL=4. K/C are only one-credit without a V filter.
* XFER06 N: the same J5/J6, L=4, anonymous LL, V subset upper group; cap2.
* XFER07 G7/Cx/Kx: G7 is J7 with upper-V and either exact separator branch;
  Cx/Kx require mark7 and are only one-credit, with their stated depths.
* XFER08 GB/RB/CB/TB: GB retains d(a)<=5 and upper-V, RB retains d(a)<=5
  and either L4/LLa or real-L/LL4, including B6p. CB requires d(a)<=3;
  TB requires H8,d(a)<=7,upper-V. Only GB has two credits.
* XFER09 I: x<r at L, nonreal LL/R, V={x}, same capacity thresholds;
  the actual opposite supplies x>r. This includes both nonreal kinds.
* XFER10 root-unmarked clauses are absent at the marked P sources/targets
  used by this proof. Omitting them is a lower bound, not a domain deletion.
* XFER11 J and XFER12 G45/K: first two marks a<b4/5 and marked c>b.
  J retains span<=3 and exact core right b/right c. G45 retains immediate
  left b, d(a)=4/5, Lb/LLa and nonreal LR/R. K retains both stated core
  alternatives; q in(a,b) is automatically unmarked. All are cap2.
* XFER12 Bdry/Rsh/Q8/P8/C5/C8/J8: exactly the retained core/mark/depth
  and A guards in its section1. Bdry alone drops old upper-V, as proved
  by its no-new-fresh-source theorem. P8 keeps the exact five-bit mask.
* XFER13: exact mask{0,2,4,5,8}; T/G cap2 retain their exact constructors,
  A guards and G's nonreal LR/R. EB/ER/H/CA/CB/R are one-credit only,
  with the original free-parent and no-V boundary qualifications.

`only_v` excludes the current root and uses a SET of marked observed
Score labels. `v_exact` adds every required occurrence. `minpair` includes
both marks and excludes all smaller marks except a. Five-bit cardinality
is enforced separately. Actual opposite calls reverse ordered roles,
positions and mask bits only; every psi lookup uses its ACTUAL core.

Observation encoding is Score0..8, anonymous9, PORT10, EMPTY12; raw G
is privately resolved through literal source owner/current children.
Root.kind, anonymous unused index and nonreal unused fields never enter
these predicates. `real<=9` is exactly observed kind0 on valid observations.

`complete_floor` caps ONLY the old upward debt at1 on the precise XFER16
H_min/H_max predicates, then includes the later XFER18 proven floors.
The level2 old disjunction is therefore intersected with !H. The psi
shortcut is sound: psi2 has height<=5, while H has height>=7. Level1
floors survive the ceiling. XFER17 zeroes outside P; all new signed
checks require marked synchronized sources/targets, so their floors
are in its retained domain. No global unmarked-source psi floor is used.

The lazy cheap tier is an even smaller proven bound: psi or the original
capacity c, with !H at level2. Every genuine LOW target and marked source
has that bound in D0. SAT at the cheap tier is rechecked against the full
proved floor before suggesting a clause. No SAT branch certifies a row.

The additional19 floors are exactly the separately audited Bad boundary,
R_T reset return, paired upper family, lower return family and accepted
seven-anchor union. Their range, signed preservation and fresh-source
H1 results supply the exact-source-debt induction used in the final bridge.
This audit borrows NO sector certificate with a different potential and
NO unproved sign conclusion from the old FAILED_SIGNED_EXTENSION report.
