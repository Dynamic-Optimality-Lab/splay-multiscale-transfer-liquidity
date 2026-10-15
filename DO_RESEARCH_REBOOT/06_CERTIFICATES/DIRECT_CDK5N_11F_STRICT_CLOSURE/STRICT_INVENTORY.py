# STRICT_INVENTORY.py — A7 repair: z>0 ==> strict interval compatibility (not just gap labels).
# Gap i spans V-ranks (fullrank(i-1)..fullrank(i)) [with -1/136 sentinels]; port (s,b) spans [plo,phi).
# Overlap (positive width): plo < ghi AND glo < phi. Encoding-auxiliary only (no new coordinates).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_STRUCTURAL_WITNESS import NSLOT


def gap_bounds(d, inv, i):
    if i == 0:
        glo = d.const_int(-1, 9, signed=True)
    else:
        glo = inv.fullrank(i - 1)
    if i == 9:
        ghi = d.const_int(136, 8)
    else:
        ghi = inv.fullrank(i)
    return glo, ghi


def compat_pred(d, inv):
    C = []
    for i in range(10):
        glo, ghi = gap_bounds(d, inv, i)
        for s in range(NSLOT):
            for b in range(2):
                plo, phi = inv.port_bounds(s, b)
                # NECESSARY rank-overlap (LE both sides): value-overlap implies rank overlap
                # (order-faithful). Integer-room sufficiency is reconstruction-checked (see doc).
                overlap = d.AND(d.LE(plo, ghi), d.LE(glo, phi))
                C.append(d.OR(d.EQ(inv.z[i][s][b], d.const_int(0, 9)), overlap))
    return d.AND(*C)
