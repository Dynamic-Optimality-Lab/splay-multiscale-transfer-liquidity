# Route 02 — quantitative restriction on reuse, Step 2 of 4

Date: 2026-11-08.
**Outcome B: a restricted source-work theorem is proved symbolically; independent audit pending. Universal CD remains open.**

For a same-access producer-silent chain, let L be its number of designated outputs and let m count those outputs whose original whole B frame becomes A-common during that frame's original B run. Then there are **2m+2 distinct original real A rotations**: one preparation and one positive loss for each of those m frames, plus two producer-flag changes of the innermost output. Consequently

    2m+2 <= 2A(W),  or equivalently  m+1 <= A(W).       (1)

In particular, if all L frames become common, sharing the same blocker addition and return does not permit bounded original A cost as L grows: A(W)>=L+1. The work can occur outside the critical access. It is not asserted to be free of existing payments.

The preparation/loss selectors also have an exact cross-chain multiplicity theorem: one A rotation has at most one preparation role and at most one loss role. A coincidence requires a positive exchange between two **non-nested** frame labels. Nested frame collections have no such coincidences, even across different chains and repeated labelled runs.

The stronger removal-window version in Section 6.2 replaces m by mhat, counting A presence even before the B frame's creation. Section 6.3 also gives a new global raw injection d -> own(bhat(d)) for silent live-run-missing histories with that earlier A presence: its witnesses are distinct nonpositive A rotations, so |D_pre|<=N+T_A. Existing later owners are explicitly guarded.

These are statements about actual source operations. They are not a residual-cardinality restatement of Universal CD.

## 1. Scope fixed before proof

Read STEP02_SCOPE_BEFORE.md in this new folder for the written pre-execution target and smaller obligation. Preserve the original source, A/full-B semantics, support S, private A nodes, SET labels, original Psi, costs, lambda, g1, owners and resource checkpoint. No historical report is rewritten.

One refinement of that record is necessary. Its phrase “compatible (nested/disjoint)” was too broad: disjoint labels can be exchanged by an A rotation. The proved exclusion is for **nested labels, including equal labels**. The target in the record was already a chain of nested whole frames, so it needs no disjoint-label assertion. For example, the formal rotation 1(-,2) -> 2(1,-) loses SET label {2} and creates {1}; this refutes the broader local assertion. It is a rotation identity, not a newly generated source or an asserted CD counterexample. No exclusion of disjoint-frame overlap is used below.

This step proves the quantitative restriction for the stated domain and identifies its exact exception and cross-chain intersections. It does not perform Step 3's joint near-side funding or Step 4's full payment composition.

The original counted object remains one reachable finite exactly labelled A/full-B paired-closed source W. A performs all KEEP/DELETE splays; B performs KEEP only; DELETE never removes a physical key. S is the original ancestor-closed B carrier. Labels are nonempty S-descendant SETS in all physical A nodes, with duplicates counted once. Use only

    Psi=|J_S(B)\J_S(A)|.

Let P,N,T_A count positive, negative and zero real A rotations under the original Psi. Write R_A for the number of original real A rotations and V_A for the original terminal-zig virtual units. The exact cost convention is

    R_A=2A(W)-V_A.                                    (2)

All selected witnesses below are original real rotation bits A(t,j,r). An A double has two such units, while a terminal zig has one real unit and one distinct virtual unit. No new A access, synthetic inverse, period copy, or reachability-prefix unit is introduced.

## 2. Which original frame histories the theorem counts

For a neutral designated demand d, preserve:

* x_d: its original producer;
* I_d: its designated output, with both adjacent S boundaries;
* W_d: the whole grandparent-frame label of the neutral double, containing x_d and all of I_d;
* Gamma_d: the last B creation of W_d before the producer access containing d;
* kappa_d: the preceding B removal of that same label;
* sigma_d^B: the removal ending the W_d B run, later in the producer's B access.

Inherit C02 N8 at its symbolic/audit-pending scope: d -> Gamma_d is globally injective, the producer access is the first B access inside this W_d run, and one current W_d run corresponds to at most one such neutral demand. At the producer's post-A snapshot, W_d is A-absent because it is proper and contains the A root x_d.

Call d **common** in this report if W_d is A-present at some actual snapshot during its B run from Gamma_d to sigma_d^B. This is a source predicate, not a funding assumption.

There are exactly two common cases:

* **D case:** Gamma_d decreases Psi, so W_d is A-present at its B creation.
* **N case:** Gamma_d is neutral, but W_d is later A-acquired before the producer-root snapshot.

The complement H consists of neutral Gamma_d with W_d A-absent throughout that B run. No frame preparation/loss pair is attributed to H. This H is a set of whole-frame histories, not all producer-silent outputs and not a new owner map.

The original output I_d can remain A-absent for the entire period in either common case. Commonness here concerns W_d, which includes the producer; it does not concern I_d.

## 3. Actual event selectors and their signs

For every common d choose the following physical occurrences by the original cyclic chronology.

### 3.1 Preparation a(d)

In the D case, take the **last A SET creation of W_d between kappa_d and Gamma_d**. Its existence and global injectivity are the inherited C05 U1 theorem applied to the actual decreasing B creation Gamma_d. W_d is B-absent at a(d), so

    sign(a(d)) is zero or positive.                   (3)

This is a literal label creation, not lambda(Gamma_d) by definition.

In the N case, take the **last A acquisition of W_d in that live B run before the consuming producer-root snapshot**. It exists by the definition of the N case. W_d is B-present and A-missing just before the acquisition, so this is an actual negative rotation:

    sign(a(d))=-1.                                   (4)

This is the inherited whole-frame acquisition selector in N9. No fresh payment from it is installed here.

### 3.2 Loss b(d)

Take the **last A SET loss of W_d between Gamma_d and the producer-root snapshot**. Such a loss exists because W_d is A-present somewhere in that interval and absent at the endpoint. In the N case it follows a(d); in the D case a(d) is before Gamma_d and hence also before b(d).

B still has its original W_d label throughout these A operations. Losing that common label has the original positive sign:

    sign(b(d))=+1.                                   (5)

The inherited real-rotation/common-label sign law is used, with the full B carrier and SET convention. The operation is not inferred from a B rotation: it is selected from a necessary A SET change.

### 3.3 Individual global multiplicities

The map d -> a(d) is injective on ALL common neutral demands, without a nesting assumption:

* D-case preparations are globally injective by U1.
* N-case acquisitions create one label in one current B run; N8 permits one demand for that run.
* A D-case event has sign zero/positive; an N-case event has negative sign. They cannot coincide.

The map d -> b(d) is also globally injective. One positive A rotation loses one common B label in one current B run; N8 permits one demand for that run. Repeated equal labels in other runs do not identify the run.

Thus each physical A rotation has at most ONE a-role and at most ONE b-role. These assertions already include both orientations, private A operands, different producer accesses and cyclic seams.

The unresolved question is cross-type overlap a(e)=b(d). The next lemma controls it geometrically.

## 4. New SET-label lemma: nested frames cannot exchange

Consider a literal physical A left rotation

    u(L,v(T,R))  -->  v(u(L,T),R).

Let lambda_S(U) mean the S-descendant set of a physical subtree U, and let {u}_S be {u} if u belongs to S, empty otherwise. Put

    C=lambda_S(T) union {v}_S union lambda_S(R),
    D=lambda_S(L) union {u}_S union lambda_S(T),
    F=C union D.

C is the old promoted-child label. D is the new demoted-pivot label. F is the whole frame label, present before and after. These identities retain all private nodes.

If a nonempty SET label is lost in this rotation, it can only be C. If one is SET-created, it can only be D. Duplicates elsewhere may suppress a loss or a creation; they cannot add another candidate.

Suppose a SET loss C and a SET creation D both occur.

* If C is contained in D, then F=D. But F was already a label before the rotation, so D cannot be SET-created.
* If D is contained in C, then F=C. But F remains a label after the rotation, so C cannot be SET-lost.

Therefore simultaneous SET loss and creation require

    C not contained in D,  D not contained in C.       (6)

The right-rotation proof is the literal reflection.

**Consequence.** If W_d and W_e are nested, including equality, then

    b(d) != a(e).                                    (7)

No assumption about the B snapshot at a(e) is needed for this exclusion. It is an A SET-label theorem, not a potential or a claim that compatible B labels are simultaneously present.

### 4.1 New quantitative frame restriction

Let C be ANY collection of common neutral demands whose W_d labels are pairwise nested. They may be in different chains, producer accesses or equal-label runs. Sections 3 and 4 show that

    {a(d): d in C} disjoint-union {b(d): d in C}

has exactly 2|C| original real rotations. Hence

    2|C| <= R_A <= 2A(W).                             (8)

The original A cost is at least |C|, globally for this declared collection. No A event is repeated within the union. The nesting hypothesis is a condition on actual historical labels, not an assumed scalar inequality.

For a same-access chain, the hypothesis is automatic: successive B doubles have strictly growing whole grandparent frames. At each step the actual target moves upward through S ancestors, so these proper S-frame labels are strictly nested. No test over arbitrary BSTs is needed to obtain this fact.

This is the first new restriction on reuse: one common frame cannot share its preparation with another nested frame's loss. Counting only distinct preparations and only distinct losses separately would miss this cross-type exclusion.

## 5. New protection lemma for the shared producer-flag changes

Fix an output I=[l,a] with original producer x=pred_S(l), using the right-output orientation. Define the producer flag P_I as “x lies below LCA_A(I).” This predicate remains meaningful after the B run retires.

Consider an actual A rotation that changes P_I. The elementary canonical-ancestor geometry gives:

* For a P_I addition, the rotation is LEFT,

      u(L,v(T,R)) -> v(u(L,T),R),
      x <= u < l <= v <= a.

  The old promoted-child label excludes x. The new demoted-pivot label excludes an S key of I at or above v. If v is private, use ceil_S(v), which is in I.

* For a P_I erasure, the rotation is RIGHT,

      u(v(L,T),R) -> v(L,u(T,R)),
      x <= v < l <= u <= a.

  The old promoted-child label excludes an S key of I at or above u. The new demoted-pivot label excludes x. If u is private, use ceil_S(u), which is in I.

For completeness, the bounds are forced by a change of the ancestor relation: the producer must move into or out of the relevant LCA subtree, so one operand is in the adjacent gap [x,l), and the other is in the closed physical span of I. An operand outside that span would leave the same interval ancestor as before. This is the canonical boundary argument used in the inherited flag geometry; it does not require I to be a current B label.

In both directions neither changed proper-label candidate contains x together with ALL of I. Therefore:

> A producer-flag transition for I preserves the A SET presence of every label K containing {x} union I.                         (9)

The left-output proof is order reflection, using the adjacent upper gap and floor_S for a private operand inside I. Private unary duplicates do not invalidate the proof: a membership change still requires one of the two changed-label candidates.

In particular, the transition cannot be a SET creation or SET loss of any such K. This protection applies to the live-run first doubling and to the later post-retirement erasure, whatever that erasure's sign.

## 6. The main theorem for a producer-silent burst

Take a same-access chain or chain segment of L>=1 designated outputs with:

* one original producer x and one side;
* nested outputs I_0 contained in I_1 contained in ...;
* unacquired, producer-silent output runs, exactly as in the completed attachment trace.

Let I_0 be the innermost output, and let m of the L whole-frame histories be common as defined in Section 2.

The attachment trace gives two actual A rotations for I_0:

    theta_0 = its first producer-flag addition after birth;
    rho_0   = its first producer-flag erasure after retirement.

At birth the flags are (P,O)=(0,1). At its first-hit A snapshot they are (1,1), so theta_0 exists. A is unchanged throughout that B phase. Before or during the next actual A access to x, the producer flag must become false, so rho_0 exists. Opposite rotation directions make these two physical events distinct.

Silence locates theta_0 while I_0 is attached to its opposite boundary; it does not make theta_0 a new zero unit. rho_0 is selected after retirement, so no current-output sign theorem is applied to it.

Every W_d in the burst contains x and its own I_d, hence contains {x} union I_0. By (9), theta_0 and rho_0 preserve every W_d. They are therefore different from every a(d) and b(d) selected for the m common frames.

Those m frames are nested, so (7) also separates all a/b cross-types. Consequently the physical set

    E = {a(d),b(d): d common in this burst}
        disjoint-union {theta_0,rho_0}

has exactly

    |E|=2m+2.                                        (10)

This proves (1) by actual event inclusion, not a residual-count identity.

If v(E) of these real rotations are terminal zigs, their distinct virtual units can also be included. The exact accounting consequence is

    2m+2+v(E) <= 2A(W).                               (11)

No virtual unit is assigned to a double. Two selected real rotations in one double consume its two distinct original units, not two A StepEv costs.

### 6.1 Reuse restriction stated in terms of exceptions

Let h=L-m count the frames that remain A-absent throughout their original B runs. Then

    A(W) >= L-h+1.                                   (12)

Thus a silent burst of length L in a source with A cost a requires at least

    h >= max(0,L-a+1)                                 (13)

such always-missing frame histories. This is a genuine structural alternative:

* growing common-frame reuse forces additional counted A work; or
* that work cannot be charged to an asserted common history, and the source must contain the stated number of actual neutral-creator, never-acquired frame runs.

The hypothesis is not that these h histories are funded. Their further neutral genealogy is the remaining case.

The theorem imposes no A operation inside a B switch and counts no first-hit phase once per output. Preparation and loss may be far apart or across the period seam. It accepts one theta and one rho shared by arbitrarily many chain nodes.


### 6.2 Stronger cost bound from the preceding B-removal window

The same mechanism counts A preparation/loss even when it occurs BEFORE Gamma_d and the frame is never common in the later B run. The written scope of this extension is STEP02_EXTENSION_SCOPE_BEFORE.md.

Let t_d^A be the producer's post-A snapshot. Define the actual cyclic interval

    Pi_d = (kappa_d, t_d^A].

At kappa_d, B removes W_d in an access whose target belongs to W_d. A is rooted at that target, so the proper W_d is A-absent. It is also A-absent at t_d^A, where A has root x_d in W_d.

Call d exposed in this larger window if W_d is A-present anywhere in Pi_d. Every common d from Section 2 is exposed, but an exposed frame may have become A-present and disappeared before its B creation Gamma_d.

For every exposed d select

    ahat(d) = the last A SET creation of W_d in Pi_d;
    bhat(d) = its subsequent A SET loss.

The latter is the first loss after that last creation and hence the last loss in Pi_d. Both exist because A presence starts and ends absent on this interval.

These two selectors are individually globally injective:

* One A rotation SET-creates at most one label, and SET-loses at most one.
* For a fixed W label, different neutral frame demands use different B runs by N8. Their Pi intervals are disjoint: a producer's A snapshot is before the B removal ending its run; the next such interval starts at that removal or a later removal.
* Thus the same physical A creation/loss for a fixed label cannot serve two demands in different Pi intervals. Cyclic lifts do not create another copy.

The nested-label and protection lemmas apply unchanged. For a burst let mhat be the number of exposed frames. Then

    2mhat+2 <= R_A <= 2A(W),  A(W)>=mhat+1.           (13a)

This is at least as strong as (1), since mhat>=m. With hhat=L-mhat,

    hhat >= max(0,L-A(W)+1).                         (13b)

The narrower surviving exception is a frame A-absent throughout Pi_d, not merely absent after Gamma_d.

The extended events can have different signs:

* ahat before Gamma_d has sign 0/+; ahat after Gamma_d has sign -.
* bhat before Gamma_d has sign 0/-; bhat after Gamma_d has sign +.

Before Gamma_d B lacks W_d; after it B retains W_d until the producer's B phase. One-label changes give these signs directly.

For all exposed demands, each extended physical event has at most one ahat-role and one bhat-role. Simultaneous roles still require non-nested labels. The “positive event only” assertion of Section 7 belongs to the original a/b selectors and is NOT extended to ahat/bhat: a non-nested extended exchange can have negative or zero sign too.

Use one certificate at a time. The original a/b set and the extended ahat/bhat set may differ. Their costs and raw pools are never added as though they were independent events.

For a globally nested collection of exposed demands, all ahat/bhat events are distinct across every chain. For an arbitrary collection of n exposed demands, put chat=|{ahat(d)} intersection {bhat(d)}|. Its physical frame-work union has exactly 2n-chat events, with multiplicity at most two and no intersection for nested frames. Adding deduplicated anchors uses their actual additional IDs, as in (16).

### 6.3 New raw injection for a previously exposed, currently missing frame

There is a useful quantitative payment consequence of the extension, not just an A-cost count.

Let D_pre consist of actual demands d in F whose designated outputs are unacquired and producer-silent, and for which:

    W_d is A-absent throughout its B run Gamma_d to sigma_d^B,
    but W_d is A-present somewhere in Pi_d.

For this class all A presence in Pi_d lies before Gamma_d. Consequently bhat(d) is before Gamma_d, while W_d is B-absent. Its actual sign is zero or negative.

The rule

    d -> own(bhat(d)),  d in D_pre,                   (13c)

is globally injective into NONPOSITIVE original A units. Its proof is the global loss-selector proof above, with no nesting, same-producer or disjoint-chain hypothesis. In particular,

    |D_pre| <= N+T_A.                                (13d)

These units are unused by g1 because g1 uses positive heads only. Thus (13c) gives a separate, explicit analytical raw extension of g1 paying this entire source-defined class. No historical owner map is changed.

For a larger fixed coherent H retain only

    D_pre,free = {d in D_pre outside dom(H):
                 own(bhat(d)) not in im(H)
                 and not genuinely reserved}.

On this guarded subset the same pairs extend H, with multiplicity one. Excluding the rest does not prove that their old owners have replacements.

There is a geometric restriction on one important occupied case. If a negative bhat(d) is also N9's own acquisition for another whole-frame demand e, that event loses W_d and creates W_e. Equation (6) forces W_d,W_e to be non-nested. Such an owner cannot be silently treated as another use of the same nested frame history. Zero losses can instead be occupied by a zero-own rule such as L6; no quietness or vacancy is assumed.

This is the additional original obligation deleted by the larger window: silent, live-run-missing histories with an actual earlier A presence have a globally non-overcounting real A unit. After accounting for fixed-owner intersections, only frames absent on the full Pi interval remain outside this exposure mechanism.


## 7. Exact reuse across different chains

The event selectors in Section 3 are defined for all common neutral demands, not just one burst. Let D be any such collection and n=|D|. Write

    A_D={a(d):d in D},  B_D={b(d):d in D},
    c=|A_D intersection B_D|.

Individual injectivity gives |A_D|=|B_D|=n. The actual union therefore has

    |A_D union B_D|=2n-c.                             (14)

What makes (14) useful is the new source restriction on every one of its c overlaps:

* b(d)=a(e) uses one original positive A rotation;
* e is a D-case demand with positive preparation, not an N-case acquisition or a zero preparation;
* W_d and W_e are not nested, by (6);
* at that snapshot B holds W_d but not W_e: one common label is lost and the other, future B frame is prepared;
* a physical event supports one such ordered pair (d,e), with no further multiplicity.

The directed relation d -> e defined by b(d)=a(e) has indegree and outdegree at most one. It has no self-loop and no edge between nested frame labels. It is not declared acyclic: cyclic source chronology alone would not justify that.

If n_+ preparations are positive, n_0 are zero and n_- are negative, then

    c <= n_+,
    2n-c <= R_A,
    n+n_0+n_- <= R_A.                                (15)

The last inequality drops the at most n_+ actual cross-type coincidences. It is not a free-owner bound.

This proves an explicit global reuse limit for the frame events: **multiplicity at most two, one preparation plus one loss**, with exact source geometry for every double use. Within any pairwise nested subcollection multiplicity is one.

This statement includes other chains sharing A events. It does not assume their windows disjoint or multiply the A budget by the number of chains.

### 7.1 The anchor events must also be counted by physical ID

For any chosen collection of silent bursts, form F as the SET of their selected theta_0 and rho_0 physical IDs. A repeated anchor is entered once. Put

    f_out=|F \ (A_D union B_D)|.

Then the union of all identified real work has exactly

    2n-c+f_out

physical rotations. If v is the number of terminal rotations in this union, inclusion of their original virtual units gives the valid global cost restriction

    2n-c+f_out+v <= 2A(W).                            (16)

Within its own burst each anchor is separate from every frame event, by (9). It may be a preparation or loss for another burst. Such an intersection contributes zero to f_out, not another A unit.

A single anchor can also be described by several bursts. Nothing here supplies a two-unit bonus PER burst in a sum over all bursts. The two-unit bonus in (10) is valid for the stated one burst; for larger collections use the actual union or the following stronger source condition:

> If all selected frame labels are nested and every selected anchor is a producer-flag transition for an output I whose producer x and whole I are contained in every selected frame label, then all those distinct anchors are outside A_D union B_D. The total is 2n+|F| real rotations.

This condition is checked on source intervals and selected flag transitions, not inferred from source solvency.

The adjacent-gap geometry additionally fixes the producer roles of an anchor. A left rotation can add producer flags only for the one lower boundary floor_S(old pivot), and erase producer flags only for the one upper boundary ceil_S(promoted node). Right rotations reflect. Thus many histories sharing one such role have the same producer and side. Their number is not bounded by that observation; no constant per-history charge is inferred.

## 8. Quantitative accounting and existing payments

The new bound counts original units, not new labels in a substitute source. Its sign inventory is:

| Source witness | Real sign | Physical multiplicity | What is available without a new owner theorem |
|---|---|---|---|
| D-case a(d) | 0 or + | One preparation per event globally | A zero own bit is in R1 under g1; it may already have a later owner. A positive bit may be selected. |
| N-case a(d) | - | One acquisition per event globally | This is already N9's negative-own class at its declared scope. |
| b(d) | + | One loss per event globally | Counted work; its lambda destination and existing owner must be retained. |
| a(e)=b(d) | + | Exactly one a-role plus one b-role | One unit, occurring only for non-nested frames. |
| theta_0 | 0 or + | Shared by histories; once as a physical ID | No assumption that it is quiet or free. |
| rho_0 after retirement | Actual source sign | Shared by histories; once as a physical ID | No live-I zero-sign inference. |
| Terminal witness's virtual unit | Virtual | One per distinct terminal StepEv | Separate from its real bit; no double receives one. |

Negative own bits and their positive lambda heads remain different units. No extra positive head is added simply because a negative event appears in this table. A label-preparation selector a(d) is not universally equal to lambda(Gamma_d).

For the exact g_pre base, its existing components use no virtual units. Consequently the v original virtual units in (16) are outside that base's image. This identifies that limited category; an arbitrary later map or protected reservation still needs its own physical-ID check.

A raw payment corollary has only the following guarded form. In a nested collection, select at most one actual unused unit per unpaid demand from its a/b witnesses or their terminal virtual bits. Distinct witness events and their virtual bits do not collide within that collection. If each selected unit avoids the image and reservations of the fixed base H, the assignments extend H. The theorem supplies event separation, not the unproved premise that every demand has such an unused unit.

In particular, two distinct counted A rotations per frame do not imply two unoccupied units per neutral demand. Both can already be positive heads paying other B obligations. Step 4 must resolve that issue.

## 9. The descending-scan family passes the decisive test

Use the inherited family n=2m_0+1>=9 and L=m_0-1. To avoid confusing m_0 with the common-frame count m in the theorem, keep both names explicit.

At the critical KEEP n there are L silent neutral outputs

    I_j=[n-2j,n-1],  j=1,...,L,

with one producer n. Their original whole frames are

    W_j=[n-2j,n].

These labels are nested and contain n together with the innermost I_1. All chain links occur in the same B phase. No A rotation occurs between them.

Every Gamma_j is the final B rotation at the cyclic scan access to b_j=n-2j-1. That rotation creates W_j commonly, so every one of these frames is in the D case:

    m=L,  h=0.

The actual preparation a_j is the second A LR rotation at that KEEP b_j. Each prepares W_j. The original A-only reset must later lose each W_j before reaching A_source. Its last such loss b_j^A is positive while B retains the frame. The new nesting lemma separates all L preparations from all L losses; the protection lemma separates the innermost output's first doubling and post-retirement erasure from all 2L frame events.

Thus this family has the source-derived bound

    2L+2 <= R_A <= 2A(W),  hence A(W)>=L+1.           (17)

It detects actual preparation and reset work despite a single shared first-hit A phase and arbitrarily small A cost at the critical access. It does not replace the stronger restricted scan-pool and reset results already proved in the earlier Step 02.

The general family specifies an original A-only realization/reset word by the inherited theorem; its precise event IDs depend on that original word. No new reset is generated here. The saved eleven-key source fixes the concrete occurrences below.

### 9.1 Exact original IDs for n=11

The counted original period remains [35,57], one actual copy. The four-frame preparation/loss pairs are:

| Demand | W_d | Gamma_d | a(d), positive preparation | b(d), positive loss |
|---|---|---|---|---|
| (35,1) | [9,11] | B(38,1,0) | A(38,1,1) | A(52,1,0) |
| (35,2) | [7,11] | B(40,1,0) | A(40,1,1) | A(50,1,0) |
| (35,3) | [5,11] | B(42,1,0) | A(42,1,1) | A(48,1,0) |
| (35,4) | [3,11] | B(44,1,0) | A(44,1,1) | A(46,1,0) |

The two selected anchor events of I_1=[9,10] are:

    theta_0=A(36,1,1), positive,
    rho_0=A(55,1,1), positive.

There are ten distinct real A IDs in this table and pair of anchors: 2m+2=10. Each of these ten is a bit of a double, so this selected set has v(E)=0. The source's terminal virtual units are not silently added to this ten-unit certificate.

The cyclic order is preserved: the frame creators at printed 38,40,42,44 precede the cyclic K11 at 35. No prefix copy or extra period copy supplies a unit.

In this concrete source all four Gamma_j are unselected terminal releases under g1. Their positive lambda heads are a(d), already selected by N9 for the four critical demands. The common theta_0 already pays the nonneutral double (36,2) under g1. The common rho_0 is the unselected B(57,1,0) release head. Its raw category does not guarantee availability under every later comparison.

The new theorem therefore detects ten distinct original work units, while preserving the fact that several have existing jobs. It does not install ten new payments.

### 9.2 The fifth silent neutral demand is an actual exception

The saved control's other neutral double v=(36,1) has

    producer 10,  output [5,9],  whole frame W_v=[5,10],
    Gamma_v=B(35,3,1), neutral.

W_v stays A-absent throughout that B run. Thus v is in H, not in the common-frame collection. Its frame has no a(v)/b(v) pair of the form proved above. The saved A shapes never contain W_v=[5,10] during its full Pi_v interval either, so this fifth demand also illustrates the narrower unexposed exception.

Its mandatory first A-root entry is A(36,1,1), shared with the four critical theta events and already g1-owned. This illustrates why arbitrary root-entry witnesses cannot be substituted for the separated frame events.

The demand v is already g1-paid by the terminal B release at (36,3,0). It is not an unpaid counterexample to the theorem or to CD.

### 9.3 Complete original costs and no extracted closure

The original counted cost remains A=27, Q_B=11, giving scalar slack 43. The critical access has A=1, Q_B=5. The other scan accesses have A=9, Q_B=6. The actual twelve-access A-only reset has A=17, Q_B=0; the final K1 has zero A/double cost.

The reset word is unchanged:

    D1,D4,D1,D6,D1,D8,D1,D10,D9,D1,D11,D1.

All four b(d) are in that original reset. The initial reachability preparation and preperiod are retained as provenance and contribute no new A(W) units.

The new law passes the requested test because it counts this preparation/restoration history. It would fail if it demanded a separate A event inside each neutral B switch; no such assertion is made.


## 10. Signed alternative using the original decrease events

The distinct-work theorem also identifies how the positive work can enter the old scalar account; it does not create another potential. Equations (18)–(19) use the original common-frame a/b selectors, for which b is positive. For the extended Pi-window pair use its actual signs from Section 6.2 instead.

For a nested common-frame collection with selected distinct anchor set, let E be the actual real-work set established above. Let p_E, n_E and t_E be its positive, negative and zero counts. These sum to |E|. All b(d) are positive; N-case a(d) are negative; D-case a(d) have their actual zero/positive signs.

For a burst, write m_+,m_0,m_- for the counts of its positive/zero/negative preparations, so m=m_++m_0+m_-. Since the witnesses are disjoint,

    p_E >= m+m_+
           +1_{theta_0 positive}+1_{rho_0 positive},
    n_E >= m_-+1_{rho_0 negative},
    t_E >= m_0+1_{theta_0 zero}+1_{rho_0 zero}.         (18)

These are counts of source bits, not copies of work per label.

Every positive A unit in E has exactly one inverse decrease under the inherited cyclic crossing lambda. Distinct units in E give distinct original decrease slots. Therefore the p_E units require p_E actual slots among

    A-negative rotations,
    first/second B-double decreases,
    terminal B-zig decreases.

In particular the old closed-source balance gives the source-derived consequence

    p_E <= N+B_1+2B_2+Z_1.                           (19)

The content beyond that balance is the independently proved lower bound (18) on distinct p_E units. No sign conclusion is extracted from the balance alone.

Each such actual slot has multiplicity one in this association; a B2 double has two distinct decrease slots and cannot provide a third. An A-negative has one own negative unit and a different positive lambda head. A terminal B zig has one release slot.

Classify the inverse slot of each selected positive unit literally under the preserved g1:

* an A-negative slot gives its original raw positive release head;
* an unselected B release gives its original raw positive head;
* a selected first-decrease or same-access release head remains occupied by its actual g1 owner.

Thus positive preparation/restoration cannot disappear from the original account. It either corresponds to a recorded raw category or has an actual competing payment owner. What is not proved is that enough of these heads are unoccupied under a larger fixed comparison. A selected first decrease is not relabelled as surplus.

For any fixed coherent later H, the selected work units inside im(H) have distinct H owners because H is injective. Cross-descriptions in (14) are still a single unit and hence have a single owner. This identifies the actual competing events and their multiplicities, while leaving Step 4's required joint owner treatment open.

## 11. Remaining exception and what has genuinely been reduced

The restriction is unconditional on its stated source domain, but it is not a theorem that every frame is common or exposed. The live-run class H below is split by Section 6.3: its previously exposed D_pre members have the new nonpositive-loss witness, while frames absent on the entire Pi interval remain unexposed.

For an H-history:

* Gamma_d is neutral.
* W_d is never A-acquired in the actual B run.
* The consuming producer-root snapshot is also A-absent.
* The source may have no A preparation/loss pair for that W_d run.
* A compulsory first A-root entry need not supply an unused or distinct unit; the saved fifth neutral demand demonstrates sharing of that kind.

One must not set a(d) equal to a nonexistent frame preparation, nor charge rho(d) once per H-history. The inequalities (12)–(13) quantify how many such histories are necessary if a long burst has insufficient A cost for many common frames.

The inherited N8 genealogy supplies a further exact structural description, not a new payment. An H-history's neutral Gamma lies either in another neutral double or in the neutral half of a B1 double. In the former case the child's frame is a strict subset of its creator double's whole frame. One neutral double has at most two such children; at most one new frame is created by each of its two physical rotations. Root histories of this always-missing type can start only at the neutral half of B1. These are the inherited forest restrictions. No global bound on their descendants or unused capacity is inferred here.

After a complete N9 selection, an unpaid N-case frame-acquisition history is already excluded at that map's declared scope. A remaining unpaid common-frame case can still have a decreasing Gamma whose head was selected by g1 or another fixed owner. The new pair-separation theorem still counts its a/b work, but does not erase those owners.

For chains whose nodes are produced in DIFFERENT accesses, the W_d sets are not known to be nested. Nested outputs alone do not imply nested historical whole frames: their other endpoints can differ between accesses. Apply (14)–(16) with the actual frame relations; do not apply the burst bonus automatically.

The smallest surviving mathematical obstruction is therefore explicit:

> Bound or eliminate unpaid frames A-absent on the full Pi interval, and resolve real outside owners occupying the new nonpositive loss witnesses or the separated frame work. Non-nested exchanges and shared anchors between bursts must retain their original event multiplicities. A small number of shared blocker events alone is not an insolvency witness.

This remains a source-history problem. Reasserting the desired residual-capacity inequality would not solve it.

## 12. Near-side endpoints: interface for Step 3

The new work theorem does not assume the output retires at its opposite boundary. It applies to a producer-retired silent output when its frame belongs to the declared nested collection. The Pi-window extension and the global nonpositive-loss rule also retain the original retirement type; they do not exclude producer-retired members.

For a persistent-blocker near-side output, the attachment trace still has theta off the producer frontier, a final reverse attachment with P already true, and rho after retirement. Protection (9) remains valid. If its whole frame becomes common, it has the original a/b pair. If it is exposed only before Gamma, it has the extended pair and the nonpositive loss of (13c), subject to the fixed-owner guard. If it is absent on the full Pi interval, no frame-event pair is supplied.

These observations do not yet fund all endpoints.

An attached near-side endpoint can be included in the SAME nested work collection only when its actual whole frame and provenance satisfy those hypotheses. It does not receive another two-unit anchor bonus merely because it is called an endpoint. If it is born in a different access, nesting must be proved from the source or its cross-type intersections must be retained.

For an unattached P_free input, no predecessor chain or common-frame preparation is invented. Its real frame history, producer flag changes and existing owners are the inputs needed next.

No epsilon_C or P_free cardinality is turned into a paid source block here. This is the exact interface to the user's Step 3, not a substitute for it.

## 13. Verdict and advancement record

**PROVED—RESTRICTED DOMAIN, symbolic / independent-audit pending:**

1. A rotation cannot simultaneously SET-lose and SET-create nested labels, even with arbitrary private A nodes and SET duplicates.
2. Every common neutral whole-frame history has the actual preparation/loss pair defined in Section 3. Each selector is globally injective.
3. Every producer-flag transition for I preserves all labels containing its producer together with I.
4. A same-access producer-silent chain with m common frames has 2m+2 distinct original real A rotations, with exact virtual-unit refinement (11).
5. Across arbitrary chains, an original a/b frame event has at most one preparation and one loss role. A coincidence is a positive event involving non-nested labels, with exact role count (14) and global cost restriction (16).
6. The larger Pi-window version gives 2mhat+2 distinct rotations for a burst and leaves only frames absent on the full interval unexposed.
7. Previously exposed but live-run-missing silent frames admit the globally injective nonpositive-loss rule (13c), paying D_pre relative to g1; larger fixed maps retain the explicit vacancy/reservation guard.

These are physical source consequences. Their statements do not assume Universal CD, an unused-unit matching, a new potential, a locally closed access, or a constant endpoint allowance.

**BEFORE:** the attachment trace allowed an unbounded number of outputs to share theta and rho without a quantitative separation of their frame work.

**RESULT:** common nested frames force two actual A rotations each, disjoint from the two selected blocker changes. No cross-type reuse is possible in that nested collection. The original common-frame selectors have cross-chain multiplicity at most two with an identified positive exchange. The extended selectors have the same multiplicity bound, while their exchanges can also be zero or negative.

**AFTER:** constant-work reuse is excluded on the exposed-frame burst domain. If A cost is too small, (13b) forces actual frames absent on their full Pi intervals. Previously exposed but live-run-missing frames have the new nonpositive injection relative to g1. Full source coverage and composition with larger fixed maps remain open.

**Genuinely deleted inference burden:** no new noncollision proof is needed to separate preparation/loss/anchor operations WITHIN a declared burst, or preparation/loss operations across a globally nested frame collection. Their physical union is constructed above. The entire D_pre class also has an explicit globally injective raw payment under g1; only actual intersections with larger fixed maps are left for that class.

**New assumptions:** no extra assumption on W; the proved cost domain is explicitly restricted by actual nesting and commonness/exposure. Those properties are not asserted for all residual demands; the separate D_pre injection does not require nesting.

**NET PROOF ADVANCEMENT:** a quantitative source-cost restriction, a bounded cross-type reuse law, and the globally injective raw nonpositive-loss rule (13c). This is not merely another decomposition of residual cardinality. It does not complete unrestricted source coverage or composition with every fixed owner.

Outcome remains **B**. The universal inequality Q_B(W)<=2A(W), the full near-side theorem, global owner composition, Bank25 promotion and Dynamic Optimality remain unproved.

The broader disjoint-label exchange exclusion in the scope note was rejected, as explained in Section 1. The main nested-frame mechanism survives with its exact hypotheses.

## 14. Next steps requested by the user

**3. Handle near-side endpoints jointly.** Cover attached epsilon_C and unattached P_free using their original frame runs and persistent-blocker attachment records. Include qualifying exposed frames in one physical work collection and retain frames absent on the full Pi interval. The new nonpositive map (13c) also applies to near-side members of D_pre, with its actual owner guard. Do not give shared anchors another allowance or assert another producer-child addition.

**4. Establish global composition.** Fix one coherent base comparison. Resolve the actual intersections a(e)=b(d) and ahat(e)=bhat(d), the nonpositive-loss witnesses (13c), shared anchors, D4 preparations and g1/N9/L5/L6/L7 or other-chain owners, including genuine protected reservations. Every occupied physical bit keeps its owner until a valid joint argument replaces or avoids it. Only after source coverage and non-overcounting payments are complete can the counts yield Universal CD.

No work on either of these two full stages is claimed in this report.

## 15. Preservation and verification scope

Only this new isolated folder is written. Existing trace/Step 01/Step 02 reports, C01–C09, saved sources, resource records and Routes 01/03 remain unchanged. No commit, branch change or other Git mutation occurs.

Source control: branch coarse-double-branch, HEAD 8c378d49283b3738b18e7175886772a98025e4e9.

Read-only provenance, relative to DO_RESEARCH_REBOOT:

| Input | SHA256 |
|---|---|
| PARALLEL_ROUTE02_ATTACHMENT_TRACE_20261108/STEP01_ATTACHMENT_TRACE.md | fc07769642f6b08f35f6d6cfdd45290f740772556d7ad754757eb94a3a9949b4 |
| PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP01_20261108/PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP01.md | 2304e5c6f9f030bba07f593fd7d3cb35eac742b4220a848d64bcb44f48dd37d0 |
| PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP02_20261108/PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP02_GLOBAL_COUPLING.md | 98d827fca54d74820f7bfb598fe7198ef2b694e9c553da7f168bc193b2cd99e6 |
| C/STEP3_1B_NECESSITY_CONTINUATION_02.md | 9b784193b5d68bc0fc358ca09204ff4ebacb69ba1db0fabce422cf97ff98a1e3 |
| C/STEP3_1B_NECESSITY_CONTINUATION_03.md | 00a004ec6f55fbe3e4e7bc8c4866782f428edbcbc40f1eb7c4903e46769e2059 |
| C/STEP3_1B_NECESSITY_CONTINUATION_05.md | 57261c7bc9e45579acd42c90862baf985bda6c3a4eb726d6773e03c8d0ad43e4 |
| C/CONTINUATION_04/projected_cluster_closed_counter_source.json | f276a3b5d4f95d0f0328d762f7ea8749b35a00f546393d9d164ab24dcd972f80 |
| C/UNIVERSAL_GLOBAL_FUNDING_11/resources_checkpoint.json | 76c8be7af7b580a06f659c3147b6090968aac7e5cc9e7c77001afb46654dce10 |

C denotes SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35. Pins identify input bytes, not independent proof certificates.

Verification is symbolic self-review: literal A rotation/SET cases, private operands, equal labels and duplicate suppression, actual current versus retired B runs, disjoint Pi windows for equal labels, both orientations, cyclic selection, preparation/loss signs, the new nonpositive-loss injection and its owner guard, physical-event multiplicities, terminal accounting and the already saved scan IDs. No external/formal audit of the new theorem is claimed.

No new source query, executable source replay, experiment, state/solver search, potential or verification phase is run. Only static inspection and manuscript work take place. The authoritative inherited resource checkpoint is preserved: global CPU 6394.71875/7200; symbolic 2452.375/2640; independent 740.96875/750; source queries 3050330/3100000; batch 50000; Bank25 25. No allowance is reset or increased, and no resource-exhaustion claim is made.


