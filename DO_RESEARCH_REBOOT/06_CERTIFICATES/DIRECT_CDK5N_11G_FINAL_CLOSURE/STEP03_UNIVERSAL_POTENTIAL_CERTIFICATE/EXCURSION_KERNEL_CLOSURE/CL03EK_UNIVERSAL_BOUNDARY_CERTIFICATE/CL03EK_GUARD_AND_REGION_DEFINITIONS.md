# CL-03EK Guard and Region Definitions (verified against frozen schema)

g(s) = 1[D(s)>=7] with D = maximum B-depth over 9 core slots (parent-walk
depths; total on valid states; range 0..8 observed). Guard depends only on
frozen b fields (no H/witness/edge data). L = {g=0}, D-region = {g=1}.
Edge classes E_00/E_01/E_11/E_10 partition all frozen edges (low OO and
contracted-high with shared midpoint; verified present in the edge
inventory). No vertex excluded; no liftability assumed; all 126 masks and
valid saturated signatures retained in every class. Threshold 7 is FROZEN
(no tuning under any outcome).
