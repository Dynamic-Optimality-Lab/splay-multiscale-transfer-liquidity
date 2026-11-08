# All direct LOW exceptions for one active maximum

Inherit the exact domain and pi of PRIVATE_MAX_ONE_EVENT_PROJECTION.
Let A=g(L,R) be the old ten-anchor shape. The new maximum z occurs on
the right spine, inserted above an old nonempty right subtree. Off-path
cases commute. If the marked target is the root, the access is identity.

## Canonical wrapper and its exact mismatch

For Lift(A)=g(L,z(R,E)) and x>g of old depth d, bottom-up doubles inside
R agree until only the top frame remains.

For odd d=2m+1, the old last right zig is the new last RL double:

    S_x(Lift(A)) = Lift(S_x(A)),  H_new=H_old.

This equation retains E and every hanging subtree. If x<g, z is off-path
and projection commutes. For even d=2m, H_new=H_old+1. In the old RL top
frame projection also commutes. In the old RR top frame

    old source:    g(A,p(B,x(C,D)))
    native target: x(p(g(A,B),C),D) = N
    projected new: x(g(A,p(B,C)),D) = P.

The actual new target has z(D,E) as its right subtree. P is converted
to N by one left rotation inside P.left. This is a genuine shape mismatch,
so simply claiming suppression always commutes would be wrong.

For the old range-three debt, let m0=2 min(H_old,3)-Q+D(N,Bt)-Ds.
Using c_new=min(H_new,4), the actual margin in this mismatch is

    m_new = m0 + 2 - (D(N,Bt)-D(P,Bt))

when H_old<=3. With integer debts in[0,3], failure requires exactly
D(N,Bt)=3, D(P,Bt)=0 and m0=0. Since Q<=4, the only tuples
(H_old,Q,Ds,D(N),D(P)) are

    (1,2,3,3,0), (1,3,2,3,0), (1,4,1,3,0), (2,4,3,3,0).

The immutable coefficient property that none occurs is checked independently
in private_max_pullback_independent_audit.json. It covers all13624 raw
RR-even inverse source rows, both orientations via the accepted reflection
code, and all66 potentially critical couplings. This proves the canonical
wrapper pointwise law, not an invariant assertion that every later source
must still be a canonical wrapper.

## Every actual H2 marked access, all maximum positions

If the path contains z and has length three or four, suppressing z leaves
old depth two or three. Its position is on the initial right-going prefix.

Length three: z has depth one or two. In both cases the only mismatch is
the same old RR depth-two frame above, with old H1 and new H2. The other
case is an RL commuting frame. The critical-quartet property handles both.

Length four: old depth three. If z is at depth one, odd-depth canonical
commutation applies. If at depth two, the old prefix is RRR or RRL.
The full arbitrary-term formulas are:

RRR source: g(A,p(B,u(C,x(D,E))));
actual lifted source: g(A,p(B,z(u(C,x(D,E)),F)));
projected actual target: x(p(g(A,B),u(C,D)),E).

RRL source: g(A,p(B,u(x(C,D),E)));
actual lifted source: g(A,p(B,z(u(x(C,D),E),F)));
projected actual target: x(p(g(A,B),C),u(D,E)).

If z is at depth three, the old prefix must be RRR, and the projected
target is exactly the same RRR projected target just displayed. These
statements follow by performing the bottom double and then the top double
on the displayed source terms. There are no further positions or prefixes.

For these depth-four cases actual H=old H=2, so price4-Q>=0. Every zero
source debt is automatically safe. On every positive source coefficient
the independent forward-prefix audit checks4-Q+D(P,Bt)-Ds>=0: all7280
old A motifs and2811 possibly constraining source/B couplings. Unlisted
coefficients are exactly zero, not untested states. This is a complete
finite coefficient lemma used inside a uniform source-term proof; its
scope is the specified ten-anchor coefficient function, not all support.

Combined with the one-event/helper proof, this exhausts every actual LOW
packet in the eleven-anchor domain. HIGH does not require further path
classification: the accepted native-ten endpoint envelopes cover arbitrary
old projected A source and target shapes at their synchronized roots.
