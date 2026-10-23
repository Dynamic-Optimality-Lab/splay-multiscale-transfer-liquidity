# DH-01 Deep Guard Definition (frozen; verified against implementation)

D(s) = b_depth_max(s) = max core-slot B-depth (9 S-indices; parent-walk;
total on valid states; observed range 0..8, max 8 not proved-but-unused).
g(s) = 1 iff D(s) >= 7 (fixed, no tuning). L = {g=0}, D-region V_D =
{g=1}. Edge classes E_00/E_01/E_11/E_10 partition ALL frozen edges (low
and high; contracted-high midpoint is M-sort, not an ordinary vertex, so
it carries no guard; the GUARDED endpoints do). All 126 masks and valid
signatures retained in every class. Stored corpus: 00:52+, 10:35+, 11:22+,
01:8 certified (no 0->1 in the 96-corpus; 8 certified via targeted hunt)
— 01 class nonempty, H2-relevant.
