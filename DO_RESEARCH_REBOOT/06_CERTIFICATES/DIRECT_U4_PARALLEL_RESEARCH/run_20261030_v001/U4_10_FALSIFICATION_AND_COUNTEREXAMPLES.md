# Falsification, witnesses and reproduction

## Seven-key witness and all-size family

See U4_05 and u4_counterexample_certificate.json. Define V_n=right vine1..n and
W_n=D(n-1),Dn,Kn,D(n-1),K(n-1),...,D1,K1. For every n>=2 it is exactly closed from
(V_n,V_n). After D(n-1), n is its right child; Dn costs1. B is still V_n, so Kn has
q=floor((n-1)/2) and a=0. Every KEEP is immediately preceded by DELETE of the same key.
Every possible creator therefore has zero credits. Kn's complete neighborhood is the
two Dn credits. For n>=7 the whole Kn bundle has Hall defect floor((n-1)/2)-2;
any three of its demands already give a minimal deficiency1.

Closure proof, not finite extrapolation: after the initial D(n-1), A's remaining non-noop
key sequence is n,n-1,...,1; B's is that same descending sequence. A descending sweep
sends any n-key BST to V_n. Inductively after k+1,...,n, the processed right subtree is
a right vine; accessing k (maximum remaining left subtree) preserves it as the right
subtree of the new root k. At a final attachment the access path is L followed by Rs,
so the final zig/zigzag attaches the old root as right child. This proves the invariant.

n<=6 sharpness for the original matching (paper proof): q<=2 for every access. Nonstarved
demands fit their local2a>=2; starved demands fit the positive DELETE-setup2a>=2. Distinct
active starved accesses have distinct DELETE setups, which are disjoint from nonstarved
local pools. Thus U4-M holds at total key counts<=6 and first fails at n7. This is about
total keys; the second witness already fails with only five KEEP keys.

Finite controls: n2..64 in both mirror orientations,126 cases, exact paired closure and
depth/event/state equality between the pointer and independent frame engines. They support
the all-n proof; they do not replace it. The seven-key graph stabilizes under2/3/4 context
laps with credits indexed once. W7 repeated twice closes with A22,Q12; no credit duplication.

## Physical five-KEEP/nine-core witness

Initial trees are identical to the exact T0 literal in the inherited nine-node replay.
Complete nested trees, all32 transitions and exact neighborhoods are in the new JSON.
Its word is:

    D3 D2 D3 K3 D7 D6 D7 K7 D1 D6 D1 K1 D9 D6 D9 K9 D5 D2 D5 K5 D7 D6 D7 K7 D1 D6 D1 K1 D9 D6 D9 K9

Original B word: K3,K7,K1,K9,K5,K7,K1,K9. B depths6,4,4,4,6,4,4,4;
genuine support{1,3,5,7,9}, nine-core at EVERY boundary. A34,Q18,Z0,B18,
R18,S68. Two disjoint minimal Hall triples each have3 demands and2 neighbors;
original maximum matching16/18 agrees with the exact disjoint-block formula.
Original symbolic chi8 states or a symbolic lift are not asserted by this physical replay.

## Reproduction

Run from the pinned repo root using Python -B. First certificate creators refuse overwrites:
use a fresh versioned sibling run, copying ONLY the new verification scripts there. Their
parent-depth ROOT calculation is unchanged at that level. Existing source/certificates remain inputs.

    python -B <fresh-run>/verify_u4_counterexample.py
    python -B <fresh-run>/verify_saved_and_route_c.py
    python -B <fresh-run>/verify_five_key_counterexample.py
    python -B <fresh-run>/replay_inherited.py chr
    python -B <fresh-run>/replay_inherited.py frc
    python -B <fresh-run>/replay_inherited.py m2

The first checker uses source pointer + independent frame replay and original matching.
The saved-certificate checker imports neither pointer genealogy nor original matching:
it replays the tuple engine, derives complete neighborhoods from all-creators-zero,
exhausts all64 Hall subsets and independently computes the maximum matching.
All computations are exact integers. No search timeout is promoted. No genuine CD counterexample
was found or claimed. Later multi-billion-row population certificates were not rerun here.
