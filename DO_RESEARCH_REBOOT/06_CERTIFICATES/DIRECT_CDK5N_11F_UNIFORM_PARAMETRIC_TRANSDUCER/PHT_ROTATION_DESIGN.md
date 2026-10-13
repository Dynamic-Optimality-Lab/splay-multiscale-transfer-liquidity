# PHT rotation transducer design note (STEP 05 record).
#
# Representation choice: heap-indexed slots (1..127) with (occ, key, holetag).
# A primitive rotation is compiled as a FIXED slot-reassignment pattern per
# (case, depth) with middle-subtree rigid relocation handled by subtree-size
# counters: each slot carries sz = number of occupied nodes in its subtree.
# Rotation at (p,c) with middle M (|M| = m from counters): new occupancy of
# affected slots is determined arithmetically (no enumeration of M's shape:
# M moves as one rigid block; its new root slot + size counter update; its
# interior slots are remapped by a fixed offset permutation derived from
# (case, m)). Since m is a symbolic counter, the remapping is expressed as
# arithmetic on slot indices guarded by size comparisons -- all within the
# frozen bounded-integer fragment. Opaque holes (fringe blocks) are exactly
# the M blocks: never inspected, only relocated with counters.
# This avoids per-placement instantiation: ONE transducer circuit handles all
# rotations via symbolic slot/counter variables. Node budget: slots*fields +
# case logic (5 event kinds x fixed patterns) + counter arithmetic (12-bit).
# Measured below in PHT_ROTATION_CIRCUIT.py.
