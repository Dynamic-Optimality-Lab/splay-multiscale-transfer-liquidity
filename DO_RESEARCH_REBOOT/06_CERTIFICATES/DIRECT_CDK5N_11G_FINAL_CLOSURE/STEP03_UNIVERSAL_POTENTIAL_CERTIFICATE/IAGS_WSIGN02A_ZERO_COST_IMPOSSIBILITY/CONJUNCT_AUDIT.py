# IAGS-WS-02A machine re-check (duplicate name; first inode not executable by FS).
import sys
BASE = "DO_RESEARCH_REBOOT/06_CERTIFICATES"
F11F = BASE + "/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER"
F11S = BASE + "/DIRECT_CDK5N_11F_STRICT_CLOSURE"
CHECKS = [
    (F11F + "/PC_ROTATION_INTERPRETER.py", "H = d.ADD(H, d.ITE(active, event_a(d, wit, e), d.const_int(0, 3)), 3)"),
    (F11F + "/PC_ROTATION_INTERPRETER.py", "a = d.ITE(d.EQ(dd, d.const_int(1, 3)), d.const_int(1, 3), a)"),
    (F11F + "/PC_ROTATION_INTERPRETER.py", "C.append(d.EQ(wit.evpath[ev][0], tgt))"),
    (F11F + "/PC_ROTATION_INTERPRETER.py", "C.append(d.LE(dd, d.const_int(4, 3)))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "d.EQ(macro_H(d, wit), Hv)"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(d.LE(Hv, d.const_int(2, 2)))"),
    (F11F + "/PC_ROTATION_INTERPRETER.py", "pair_on = d.LT(d.const_int(t + 2, 3), d.ADD(dd, d.const_int(1, 3), 3))"),
    (F11F + "/PC_ROTATION_INTERPRETER.py", "zig_on = d.EQ(dd, d.const_int(t + 1, 3))"),
    (F11F + "/PC_B_CONTROLLER.py", "C.append(d.EQ(bt.bpath[ev][0], bt.bT[ev]))"),
    (F11F + "/PC_B_CONTROLLER.py", "C.append(d.LE(bt.bd[ev], d.const_int(18, 5)))"),
    (F11S + "/STRICT_SOURCE_REPAIRS.py", "C.append(d.EQ(plast, st.root))"),
    (F11S + "/STRICT_SOURCE_REPAIRS.py", "C.append(d.OR(d.NOT(isK), d.EQ(blast, bs.root)))"),
    (F11S + "/STRICT_SOURCE_REPAIRS.py", "C.append(d.OR(d.NOT(isK), d.EQ(aS, bC)))"),
    (F11S + "/STRICT_SOURCE_REPAIRS.py", "C.append(d.OR(d.NOT(d.AND(isK, aS)), d.EQ(aI, bT)))"),
    (F11S + "/STRICT_SOURCE_REPAIRS.py", "isc = d.LT(t, d.const_int(NCORE, 5))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(s.aS[0])"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(d.EQ(brootS, d.const_int(1, 1)))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(d.EQ(s.aI[0], muxb(d, [d.const_int(i if i < NCORE else 0, 4) for i in range(NB)], bs[0].root)))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(d.EQ(mux_ref(d, wit.isS, sh['root']), s.aS[p]))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(d.OR(d.NOT(s.aS[p]), d.EQ(mux_ref(d, wit.sidx, sh['root']), s.aI[p])))"),
    (F11F + "/PC_B_CONTROLLER.py", "pair_on = d.AND(d.NOT(is_delete), d.LT(d.const_int(t + 2, 5), d.ADD(dd, d.const_int(1, 5), 5)))"),
    (F11F + "/PC_B_CONTROLLER.py", "zig_on = d.AND(d.NOT(is_delete), d.EQ(dd, d.const_int(t + 1, 5)))"),
    (F11F + "/PC_B_CONTROLLER.py", "root=d.ITE(is_delete, bs0.root, st.root))"),
    (F11F + "/PC_B_CONTROLLER.py", "return old_st._clone(kl=[b(n, o) for n, o in zip(new_st.kl, old_st.kl)]"),
    (F11S + "/STRICT_LOW_COMPILER.py", "bs.append(b_splay_event(d, bs[e], bt, e, eff_del))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(d.LT(d.const_int(0, 3), wit.nev))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(mux_ref(d, wit.evK, last))"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(tisS)"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(marked)"),
    (F11S + "/STRICT_LOW_COMPILER.py", "C.append(chg)"),
]
fails = 0
for path, needle in CHECKS:
    try:
        src = open(path, "r", encoding="utf-8").read()
    except OSError as ex:
        print("MISSING-FILE %s (%s)" % (path, ex)); fails += 1; continue
    if needle in src:
        print("PASS %s :: %.64s" % (path.split("/")[-1], needle))
    else:
        print("FAIL %s :: %.64s" % (path.split("/")[-1], needle)); fails += 1
print("checks=%d fails=%d" % (len(CHECKS), fails))
sys.exit(1 if fails else 0)
