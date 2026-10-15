# STRICT_SOURCE_REPAIRS.py — A1/A2/A8 repair conjuncts + A3 normalizer.
# All predicates over PC build_low handles (no PC modification). Encoding-auxiliary only.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_STRUCTURAL_WITNESS import NSLOT, W_REF
from PC_ROTATION_INTERPRETER import mux_ref
from PC_B_CONTROLLER import NB, NCORE


def a_key_of(d, wit, slot):
    """(isS, sidx-or-0, rank-or-0) of an A slot."""
    return (mux_ref(d, wit.isS, slot), mux_ref(d, wit.sidx, slot), mux_ref(d, wit.rank, slot))


def b_key_of(d, bt, ev):
    """(isCore, id-or-gap) of a B target."""
    t = bt.bT[ev]
    isc = d.LT(t, d.const_int(NCORE, 5))
    return (isc, t)


def same_keep_target(d, wit, inv, bt, ev, active):
    """A1: active KEEP ==> same key both sides. S: exact sidx==core-id. Fringe: same gap
    (gap fungibility for canonical blocks proved in STRICT_KEEP_IDENTITY_THEOREM.md)."""
    isK = d.AND(active, wit.evK[ev])
    tgt = wit.evT[ev]
    aS, aI, aR = a_key_of(d, wit, tgt)
    bC, bT = b_key_of(d, bt, ev)
    C = []
    # S Teeth: A-S <=> B-core, and sidx equal
    C.append(d.OR(d.NOT(isK), d.EQ(aS, bC)))
    C.append(d.OR(d.NOT(d.AND(isK, aS)), d.EQ(aI, bT)))
    # fringe: gaps equal (A gap via inventory gapof, B gap = id-9)
    ag = inv._gapof(aR)
    bg = d.SUB(bT, d.const_int(NCORE, 5), 5)
    C.append(d.OR(d.NOT(d.AND(isK, d.NOT(aS))), d.EQ(ag, bg)))
    return d.AND(*C)


def root_terminated(d, wit, bt, st, bs, ev, active):
    """A2: path[dd]==current root + no repeated nodes, A and B (B only for KEEP). Gated by active."""
    C = []
    dd = wit.evd[ev]
    path = wit.evpath[ev]
    # A root termination: longest meaningful entry equals current root
    plast = path[0]
    for i in range(1, 5):
        plast = d.ITE(d.EQ(dd, d.const_int(i, 3)), path[i], plast)
    C.append(d.EQ(plast, st.root))
    # A no-repeat over the dd+1 entries
    for k in range(5):
        for l in range(k + 1, 5):
            both = d.AND(d.LT(d.const_int(k, 3), d.ADD(dd, d.const_int(1, 3), 3)),
                         d.LT(d.const_int(l, 3), d.ADD(dd, d.const_int(1, 3), 3)))
            C.append(d.OR(d.NOT(both), d.NOT(d.EQ(path[k], path[l]))))
    # B root termination (KEEP only) + no-repeat
    isK = d.AND(active, wit.evK[ev])
    blast = bt.bpath[ev][0]
    for i in range(1, 19):
        blast = d.ITE(d.EQ(bt.bd[ev], d.const_int(i, 5)), bt.bpath[ev][i], blast)
    C.append(d.OR(d.NOT(isK), d.EQ(blast, bs.root)))
    for k in range(19):
        for l in range(k + 1, 19):
            both = d.AND(d.LT(d.const_int(k, 5), d.ADD(bt.bd[ev], d.const_int(1, 5), 5)),
                         d.LT(d.const_int(l, 5), d.ADD(bt.bd[ev], d.const_int(1, 5), 5)))
            C.append(d.OR(d.NOT(d.AND(isK, both)), d.NOT(d.EQ(bt.bpath[ev][k], bt.bpath[ev][l]))))
    return d.OR(d.NOT(active), d.AND(*C))


def no_intermediate_genuine(d, wit, s, bs_list, last, ev, active):
    """A8: non-terminal active KEEP ==> NOT (marked-target AND event-changes-B). Gated by active."""
    islast = d.EQ(last, d.const_int(ev, 3))
    tt = wit.evT[ev]
    tisS = mux_ref(d, wit.isS, tt)
    tsi = mux_ref(d, wit.sidx, tt)
    from PC_LOW_COMPILER import mubit
    marked = d.const_bool(False)
    for k in range(9):
        marked = d.OR(marked, d.AND(d.EQ(tsi, d.const_int(k, 4)), mubit(d, s.mu, k)))
    diff = d.const_bool(False)
    a, b = bs_list[ev], bs_list[ev + 1]
    for x1, x2 in ((a.kl, b.kl), (a.rl, b.rl), (a.kr, b.kr), (a.rr, b.rr)):
        for x, y in zip(x1, x2):
            diff = d.OR(diff, d.NOT(d.EQ(x, y)))
    diff = d.OR(diff, d.NOT(d.EQ(a.root, b.root)))
    genuine_mid = d.AND(active, wit.evK[ev], tisS, marked, diff)
    return d.OR(islast, d.NOT(genuine_mid))


def normalize_word(word, A0, B0):
    """A3 corrected normal form (executable greedy): repeatedly drop full-no-op events
    (A and B serials unchanged by the event). Returns normalized word.
    Preservation (endpoints, H, genuine-q sequence, B trajectory) verified by replay in tests.
    Bound: survivors are <=2 non-root accesses (H<=2) + root events with state effect; the
    grammar theorem (STRICT_ZERO_COST_NORMAL_FORM.md) proves <=5 events and lists the exact
    reduction (DELETE-before-first-KEEP dropped iff full no-op; first B-changing KEEP kept;
    later full no-ops dropped)."""
    import copy
    sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
    from PC_CONCRETIZE import serial
    sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
    from CRA_pointer_tuple_replay import replay
    cur = list(word)
    changed = True
    while changed:
        changed = False
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            try:
                R1 = replay(cur, A0=copy.deepcopy(A0), B0=copy.deepcopy(B0))
                R2 = replay(trial, A0=copy.deepcopy(A0), B0=copy.deepcopy(B0))
            except Exception:
                continue
            if R1['pairs'][-1] == R2['pairs'][-1] and R1['agree'] and R2['agree']:
                # preserve: endpoints, total H, terminal (mode, q, genuineness)
                H1 = sum(l['a'] for l in R1['legs'])
                H2 = sum(l['a'] for l in R2['legs'])
                t1, t2 = R1['legs'][-1], R2['legs'][-1]
                term1 = (t1['m'], t1.get('dB'), t1['chg'])
                term2 = (t2['m'], t2.get('dB'), t2['chg'])
                g1 = [(l['x'], l['dB']) for l in R1['legs'] if l['m'] == 'K' and l['chg']]
                g2 = [(l['x'], l['dB']) for l in R2['legs'] if l['m'] == 'K' and l['chg']]
                if H1 == H2 and term1 == term2 and g1 == g2:
                    cur = trial
                    changed = True
                    break
    return cur
