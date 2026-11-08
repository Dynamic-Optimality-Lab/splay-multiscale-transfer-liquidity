# Strict FE coverage of the inherited 19-block family

**PROVED—RESTRICTED DOMAIN, uniformly in fringe size and m.** For every
common finite BST F with keys above7, including empty, and every integer
m>=1, the unchanged PG02 source family W_m(F)=W(F)^m satisfies

    W_m(F) in FE minus PF.                                    (1)

Reflection and order-preserving relabeling give the corresponding lower-
fringe cases. With the universal preservation theorem this proves the
proper closed-certificate inclusion PF proper-subset FE. It is not a
theorem about all one-unit-positive walks or universal Coarse-Double.

## 1. Fixed source and inherited return

No witness is replaced. The exact PG02 source pair is

    A_S=1(.,3(2,7(5(4,6),F))),
    B_S=1(.,2(.,3(.,4(.,5(.,6(.,7(.,F))))))).

Use the EXACT common-KEEP word

    W=K(7,5,3,1,5,6,4,1,2,1,5,1,6,7,1,2,1,3,1).

PG02's original source identities prove reachability from the equal right
spines with common F via

    D3,D5,K7,K(2,6,5,1,7,6,7,1,2,1,3,1),

exact paired return, nowhere-diagonal closure and arbitrary untouched F
substitution. Every W phase is a genuine B change and nontrivial A-root
leader. The only positive phase is0, with a=1,q=3,delta=1. All other phases
are nonpositive. The inherited identities are

    A(W_m)=25m, Q_B(W_m)=22m, Gamma_PF(W_m)=m,
    D_PF,end(c)=D_FI,end(c)=m at every one of the19m cuts.       (2)

The present independent audit replays the exact m=1 ordinary/reflected
source transitions using BOTH original implementations, preserves every
old FI/PF outcome and assignment, and checks the opaque-F return identity.
The all-m assertion (2) is inherited as a mathematical source identity;
it is not extrapolated from this audit. Startup facts and units never enter
a recurrent FE pass.

## 2. Exact FE source correction and actual algorithmic loan

After positive KEEP7,

    T=7(2(1,4(3,6(5,.))),F).

The first intervention KEEP5 has source path7,2,4,6,5 and frames inner RL,
outer LR. Tracked3 has h=3. Its first entry is inner RL in grandparent4's
outer left subtree A, so FE01 gives Delta_entry=+1. It then lies left of
the moving target5, and the outer LR gives -1; there is no terminal zig.

    H(T,5,3)=3+1-1=3,
    c_FE(anchor,KEEP3)=floor(3/2)+1-1=1.                     (3)

PF deliberately keeps its old U=4 and ceiling2. Equation(3) uses only
ORIGINAL source membership and frames, before consulting the KEEP3 own q.
The actual source replay separately verifies q=1 and a=1 at that block.

Choose the valid one-period cut at phase0, KEEP7. FE's execution is:

|Phase|Operation|C|q_B|FE reserve|FE suffix|Debt afterwards|
|---:|---|---:|---:|---:|---:|---:|
|0|KEEP7|2|3|positive own2|0|1|
|1|KEEP5|2|2|2|0|1|
|2|KEEP3|2|1|1|1|0|

At phase1 there is no intervening change, h_T(5)=4 and c_FE=2. At phase2
the retained anchor has k=1 and (3) gives reserve1. The ordinary FE FIFO
rule uses the one offered suffix unit for the oldest residual, which is
exactly the third KEEP7 double. The PHYSICAL assignment, with zero-based
source indices, is

    donor     (copy0,block2,A-event0,bit1),
    recipient (copy0,block0,B-event2).

KEEP7's B-event2 is its third actual double; there is no preceding zig
that would shift this index. KEEP3's A-event0 is its single actual StepEv.
Its bit0 pays own work, and bit1 is outside the frozen reserve. Full
source events, capacities, reservations and assignments are stored in
`FE_witness_certificate.json` and checked independently.

Every remaining phase is nonpositive and cannot create residual debt.
FE therefore ends this one-period pass with zero debt and a complete
22-demand injection into the available50 units. This is FE's OWN accepted
cut, not an inference from PG02's separate direct injection. The two happen
to use the same physical loan because the new source ceiling exposes it
through the ordinary frozen suffix rule.

The fixed m=1 audit checks all cuts: FE accepts exactly cuts0,3,...,18
(17 per orientation) and rejects cuts1,2. FI and PF still reject all19.
Only one successful cut is required. No all-cuts FE acceptance is claimed.

## 3. Uniform all-m proof with retained older anchors

Every copy returns the SAME source pair, so its positive B destination is
the SAME T and its first intervention is the SAME KEEP5. Each copy contains
exactly19 genuine B changes. For any payer phase j>=2, the newest anchor
has k=j-1 and source H(T,5,y_j). An anchor ell>=1 copies older has this
identical source H and k increased by19ell. Thus

    c_FE,older(j)=c_FE,newest(j)+19ell.                        (4)

At phase1, the newest anchor's k=0 gives ceiling2. An older anchor has
k=19ell, H(T,5,5)=0, and

    c_FE,older(1)=19ell-1>=18>=2.                             (5)

Hence older retained facts cannot raise a minimum reservation or lower it
below safety; in fact the newest fact is minimal throughout this family.
Every fact individually protects actual own q by FE02, including paid facts.
At phase2, (3)-(5) force the exact minimum reserve1 even when arbitrarily
many older positive anchors remain in history. Their paid status is irrelevant.

Cut W_m at the first copy's phase0 and use induction on physical copies.
The first copy starts with debt0. Its positive adds one residual, phase1
offers none, phase2 pays that residual, and its remaining nonpositive phases
leave debt0. Equations(4),(5) prove the SAME execution with every older fact
retained at the next copy. Thus every copy starts and ends with zero debt.
After m copies FE accepts its ONE traversal of the actual m-copy walk.

The donor and recipient in copy r carry copy tag r. Each local own-work
assignment and loan is distinct from every other copy's assignments.
There are22m physical demands and at most50m available units, with exactly
one such loan per copy. No physical credit comes from startup, another cut
or a second traversal of this m-copy period. Repeated copies are distinct
occurrences inside ONE period of W_m, not reused periods of W.

This proves W_m in FE for all m>=1 analytically. Equation(2) gives W_m not
in PF. Together they prove (1) and strictness. No m>1 or larger n is tested.

## 4. Arbitrary fringes, reflection and scope

None of the core searches or source-role choices in (3)-(5) descends into F.
The source equations leave it an opaque subtree. Thus size, shape and
internal depth of F affect neither costs nor the new bound and loan.
F may be empty. Reflection interchanges inner RL/A with inner LR/D and
outer LR with RL; its exact shifts remain +1,-1 and the same occurrence/
event/bit identities apply. All claimed orientations are source-valid.

The theorem's arbitrary-fringe claim is this inherited common outer-fringe
substitution. It does not classify arbitrary other witness states or say
all internal-fringe configurations are covered by this word. The UNIVERSAL
entry, depth and soundness results separately cover those source geometries.
No assumption that any general closed history admits these copy spans is
made. The global one-unit and universal CD obligations remain open.
