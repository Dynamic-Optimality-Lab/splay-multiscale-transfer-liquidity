# PC35 — projected cluster multiplicities and the final-event decrease

Status: uniform source derivation, with an explicit limitation below.
This is not a proof of the remaining neutral liabilities.

## IAGS Box

Target: identify additional actual potential decrease slots and a source
obstruction to funding all doubles using only these slots and own bits.
Conditions: original paired-closed source, original M and fixed BF
carrier S. Freeze any fixed accounting projection M ⊆ C ⊆ S.
Inheritance: C14 actual source and period rules, fixed core, ordinary
rotation formulas, ND35 level matching, JR35-N0 block construction.
Ambiguity: not all neutral demands have a licensed nonlocal donor.
Bridge: count multiplicities after projecting; separate final-step
decreases from general deep-access decreases.

## 1. Fine-step inequalities

At an actual subtree label it by its descendant set intersected with C.
Count these labels with multiplicities, including the empty label.
Let m_B count labels of exactly the fixed S vertices in BF. Let m_A
count labels of ALL actual A vertices. Define

    Phi_C(A,BF) = sum_L max(m_B(L)-m_A(L),0).

The range is 0..|S|. There is no bound on private A populations.
Equivalently m_A(L) may be capped at |S| for computing Phi_C.
The mathematical rotation proof uses the actual multiplicities.

An A single rotation replaces the old promoted child's label by the
new pivot's label in its multiset. The frame's whole label is carried
to the promoted vertex; off-frame subtree labels do not change.
Removing one count can increase Phi_C by at most1, and adding one
can decrease it by at most1. Thus DeltaPhi_C is in{-1,0,1}, even with
duplicate or empty labels. Attach every +1 to the original rotation bit.

For B, both operands are S vertices and the same replacement description
applies to its S-vertex multiset. Let g be the full B root just before
this genuine KEEP x. Every replaced old label contains x but omits g.
Indeed, until the final event involving the original root, g is still
the root. In the first rotation of a final same-side double, the
promoted parent has g outside its old subtree. In the second rotation,
g is on the opposite side of that parent from x. Thus the promoted x
subtree still omits g. The opposite-side double and terminal zig have
g as root up to the last rotation and give the same exclusion.
Both g and x are in M, hence in C. The removed label is therefore
proper in C and contains x. A already has root x, so this label has
ZERO A multiplicity. Removing it drops Phi_C by1; adding the new
label increases it by at most1. Every B rotation has DeltaPhi_C=-1/0.

## 2. A decrease in the actual final B StepEv

Let V be the C-label of the root-child subtree on g's side of x
AFTER the B access. It is exactly the C keys on that side of x.
It contains g and omits x. The corresponding actual A root-child
subtree has label V as well, because A and B have the same physical
key set and A has already splayed x. This is why the A multiset
counts ALL physical vertices: the child can be outside S.

At the start of the final B event g is still the root. No B S-vertex
label then equals V: every proper subtree excludes g and the root
label contains x. By the end of this event V occurs at its newly
created root child, an S vertex. At the first rotation creating V,
the new multiplicity1 does not exceed m_A(V). Its addition does not
increase Phi_C; the removed old label decreases it by1.

Consequently every genuine B access has at least one decrease in
its final event. If that event is a terminal zig, that zig decreases
Phi_C by1. A final double is nonneutral. Reflection is literal under
key reversal and exchange of left/right child slots.

## 3. Access-level reassignment and restricted full funding

Let delta_t be the total decrease of Phi_C during one genuine B access.
Use the ND35 cyclic level construction on the actual period, with Phi_C
in place of Psi. It gives distinct real A +1 bits for all decrease
slots, including those at A -1 rotations (analytical releases).
At each B access use the first min(q_t,delta_t) of its decrease slots
for that many distinct original double demands of THIS access.
It need not be the same double that generated a slot. This lets a
terminal B zig or a second decrease in one double fund a neutral
double in that access. The residual is max(q_t-delta_t,0) actual claims.
Alternate with literal h0 as in ND35. This does not make any released
or non-h0 bit automatically eligible under a frozen fE policy.

For an actual natural macro e, P_e,N_e are A +/- rotation counts.
Its genuine B access has Q_e and delta_e. Then

    2H_e-Q_e-DeltaPhi_C = (2H_e-P_e)+N_e+delta_e-Q_e.     (PC)

In particular the signed law holds if delta_e >= Q_e, or when
the actual nonpositive/zig A units and N_e pay the difference by
the displayed source inequality. For example, if H_e=1 is one
actual A zig and Q_e<=2, the final-event theorem gives the sign.
If the law is proved on EVERY macro of a class, group at minimum
Phi_C genuine boundaries as in JR35-N0. The signed local proof yields
an independently licensed grouped budget, c=H and D=0 per group,
literal h0 and working<=2 under the original static block license.
No universal hypothesis delta_e>=Q_e is asserted.

## 4. Uniform source obstruction: the fully marked descending-scan family

Take n=2m+1>=9 physical keys, ALL genuine. Here M=C=S=[n]; there
is no alternate mark-retaining projection. Write R for the ascending
right vine 1->2->...->n. Let T be the descending left vine on 2..n-1.
At the natural source boundary let B=R and

    A = 1(empty, n(T,empty)).

The next original operation is KEEP n. A performs one zig, H=1.
B performs m RR doubles, Q=m. In chronological bottom-up order
their grandparent keys are n-2,n-4,...,1, all odd. For each such g'
the two new proper B labels are {g'} and [g',n-1]. This follows
inductively from the RR frame: the promoted n's left subtree before
this frame contains exactly the previously processed larger keys
up to n-1, which become the new parent's right subtree.

After the A zig the proper A labels are [1,n-1] and [2,k] for
2<=k<=n-1. No {g'} appears, and [g',n-1] appears only for g'=1.
Thus exactly ONE B decrease occurs, in the final double. Each other
B double is neutral. At the source Phi_C=n-2: the only proper
common label is [2,n]. The A zig loses it, increasing Phi_C to n-1;
the B access decreases it to n-2. Therefore the actual signed
price with this potential is 2-m<0. In fact EVERY function of this
single Phi_C value has equal endpoints on this macro.

This packet is original-source realizable in a paired-closed history.
The decreasing scan n,n-1,...,1 ends at R from ANY BST on [n]:
after splaying k the keys >k form the ascending right vine, by
induction. For the next access k-1 the only greater path node is
the current root k; its right vine hangs unchanged, and its new
left child is empty once k-1 is root. Hence the invariant continues.
Use the following literal source word:

    KEEP n, KEEP n-1, ..., KEEP 2,
    DELETE Gamma(A_after_KEEP_2, A_source),
    KEEP 1.

Gamma is an actual A-only ordinary-splay transformation word on
the same keys from the inherited all-BST realization theorem (n>=4).
The last KEEP is genuine in B and has A cost0. B ends at R and A
ends at A_source. Start from the diagonal R and an actual A-only
Gamma preparation. All n KEEPs are genuine. Fix any one erased
genuine key; keep the same A operations, and use the actual eventual
BE/chart recurrence and its preperiod. Repeat the full word the
required finite number of times on that ONE actual aligned interval.
Its chosen KEEP n has the same original source packet. No reset
operations are dropped; they occur in a different natural macro.
The accompanying eleven-key witness fixes every Gamma occurrence
and checks literal A/B/BE/chart closure rather than presuming it.

At this packet m-1>=3 neutral demands have only TWO eligible bits
under the rule 'all own-macro bits plus any Phi_C decrease donor'.
Their exact neighborhood is those two real A zig units, regardless
of how the nonneutral demand's slots are assigned. First-loss
sector choices add no nonlocal edge. This is a genuine Hall cut of
THAT candidate relation, even if h0 ownership is relaxed. An
augmentation whose flips remain inside that relation cannot remove it.
It does not exclude adding a new independently licensed nonlocal
rule for neutral claims, and it is not a Coarse-Double counterexample.

## 5. Precise continuation

The saved AF period is no-neutral for C=M (unlike the full S-label
potential), so this refinement can pay real nonlocal residuals.
The fully marked family rules out extending it to all sources by
projection choice, scalar transformation, or alternative within-level
pairing. The remaining universal proof must supply nonlocal eligible
bits specifically for demands beyond the access's decrease slots
and own units, without reusing physical capacity or changing h0.
The original Bank25 and additional owner/period requirements remain.
JR35 OPEN; reservation compatibility DEFERRED.
