# What remains open: the missing joint source relation

**Principal verdict: FE02-RIGIDITY OPEN; FE02-CD OPEN.** No actual saturated
return or CD counterexample was found. No source search was run. The
root-return mechanism proves a universal structural bound and donor criterion,
but does not provide the required arbitrary-support closure contradiction.

## 1. Precise residual source domain

Any still-possible counterexample must be a reachable off-diagonal recurrent
KEEP macro walk, with common roots at each boundary, exactly one (1,3)
block, and all other q_j=2a_j. Its actual source depths must satisfy the
signature in FE02_01; its return gaps and departure frames must satisfy

    L_i>=4+eta_i,
    L_j>=2a_j+1+eta_j for j!=i,
    2(A-N)+1+sum eta <= (s-3)N.

Every mixed original block must lift from these boundary maps with its A
events on the real leader and B demands on the real first KEEP. No initial
diagonal equality is assumed at the recurrent boundary. All complete A and
B source trees must return, not just roots, costs or the gap signature.

This mechanism excludes s<=3 and every candidate with a source-forced short
return donor. It does NOT exclude all candidates meeting the displayed
inequalities. The all-size s<=3 class is already inherited from RT2, and
the separate banked four-KEEP theorem is also preserved. We do not claim
new CD coverage from rediscovering an already proved support class. The
formal four-key numeric signature in FE02_02 is only a demonstration that
the new root-gap constraints alone lack source compatibility information;
it is neither an unresolved counterexample to the banked theorem nor an
actual source witness. Larger-support configurations remain the principal
unsettled domain after applicable inherited small-support results.

## 2. Exact FE01-based return-loss reconstruction

The precise information discarded by the +2-per-change bound can itself be
written from original rotations. This is a DIAGNOSTIC IDENTITY, not another
proof campaign, potential, or unproved sufficient premise.

For either source tree C=A or B, a key y returning at block j had previous
occurrence p, gap L and exact departure depth epsilon in {1,2}. At each
intermediate macro block t=p+2,...,j-1 define

    Delta_t^C(y)=H(C_t,x_t,y)-d_(C_t)(y),
    kappa_t^C(y)=2-Delta_t^C(y)>=0,
    K_j^C=sum_(t=p+2)^(j-1) kappa_t^C(y).

All arguments C_t are the actual ORIGINAL pre-access trees. Applying the
universal source identity separately to actual transitions is legitimate
analysis; it does NOT refresh or change FE's first-intervention algorithm.
Telescoping those exact shifts yields

    d_C,j(y)=epsilon+2(L-2)-K_j^C.                           (10)

Put eta=1-floor(epsilon/2), and define beta=ceil(K/2) for epsilon=2 or
beta=floor(K/2) for epsilon=1. Both are nonnegative integers. Exact floor
arithmetic gives

    floor(d_C,j(y)/2)=L-1-eta_j^C-beta_j^C.                  (11)

Thus the earlier source bound drops the entire beta loss, not an unknown
credit pool. Empty intermediate intervals have K=beta=0. Cyclic indexing
only identifies source predecessors and never duplicates units.

## 3. Why source-depth conservation alone does not close the theorem

Let M=(s-1)N, Z_A the number of A final zigs in the macro word, and define
the history quantities

    R_B=sum_j(eta_j^B+beta_j^B),
    R_A=sum_j(eta_j^A+beta_j^A)-Z_A.

Equation(11), A StepEv=double+zig and the exact gap count imply

    Q_B=M-R_B,
    A=M-R_A,
    Q_B-2A=2R_A-R_B-M.                                    (12)

These are established source identities, not state potentials or inequalities
defined by an assumed CD theorem. They expose exactly what is missing:
there is NO PROVED SOURCE RELATION coupling the A and B return losses tightly
enough to preclude 2R_A-R_B=M+1 for a saturated return.

The desired inequality 2R_A-R_B<=M would be algebraically equivalent to the
target on these histories. Merely naming it, assuming its feasibility or
introducing it as a new invariant would be conjecture substitution. We do
not count (12) as advancement or assert that missing inequality.

One can check that summing all fixed-key B depth changes around closure
adds no extra restriction to (12). Each intermediate (t,y) occurs once
except for the current target and its preceding root. Source-column
telescoping yields

    sum_j K_j^B=2N(s-1)-2Q_B-Z_B-sum_j eta_j^B.

Together with the parity formula for beta this is exactly the same identity.
It does not introduce the missing A-path information. An independent audit
checks these identities on the required source word and reflection, while
explicitly leaving the joint inequality OPEN.

## 4. The exact unsupported bridge and stop

The remaining bridge is original-source COMPATIBILITY of A and B path
changes under the SAME root-key word: show that the single positive event
cannot be followed only by saturated transitions while both interior tree
shapes return. Root alignment, each tree's separate +2 law, gap counting
and each tree's separate exact depth conservation do not supply that
coupling. In particular arbitrary marked/unmarked fringe memberships in
the two trees are not forced to coincide by their common root.

No monotone joint quantity or exact path-repayment inequality achieving
this bridge has been constructed here. It would be a second independent
open source theorem beyond the completed return-budget mechanism. The
four-rule stop therefore applies. We preserve the partial source theorem,
the precise missing relation and the complete evidence, without declaring
all-size rigidity, FE acceptance of every such walk, or a counterexample.
No larger fits, core searches, masks or automatic FE03 follow.
