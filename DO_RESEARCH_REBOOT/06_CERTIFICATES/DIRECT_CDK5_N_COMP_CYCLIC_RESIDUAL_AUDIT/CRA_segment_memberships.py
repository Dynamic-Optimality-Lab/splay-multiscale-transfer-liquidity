# CRA segment banked memberships: exact frozen predicates, own-domain semantics.
# RT2 (supp<=3), CDK4 (supp==4), CDK5L (5 keys + core<=8 throughout),
# NP/S1/S2/VR/MR strict (5 genuine + core9 throughout), AJ-AK-AL-AM-AN exact.
import sys, importlib.util
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import core_of, MSET
from CRA_strict_msink_membership import intervals, strict_K, strict_P, E_slots, relay_len

def _load(modname, relpath):
    spec = importlib.util.spec_from_file_location(
        modname, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/' + relpath)
    mo = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mo
    spec.loader.exec_module(mo)
    return mo
AO = _load('cra_AO', '26AO/26AO_two_order_recognizer.py')
AP = _load('cra_AP', '26AP/26AP_maximal_run_recognizer.py')
AQ = _load('cra_AQ', '26AQ/26AQ_mixed_cyclic_dp_recognizer.py')
AR = _load('cra_AR', '26AR/26AR_mixed_exact_cover_recognizer.py')
ASm = _load('cra_AS', '26AS/26AS_mixed_cyclic_recognizer.py')

def keep_support(legs):
    return sorted({l["x"] for l in legs if l["m"] == "K"})

def genuine_keys(legs):
    return sorted({l["x"] for l in legs if l["m"] == "K" and l["chg"]})

def cores_ok(pairs, need9):
    for ps in pairs:
        c = core_of(ps[1])
        if c is None:
            return False
        if need9 and len(c) != 9:
            return False
        if not need9 and len(c) > 8:
            return False
    return True

def m_RT2(legs, pairs):
    return len(keep_support(legs)) <= 3

def m_CDK4(legs, pairs):
    return len(keep_support(legs)) == 4

def m_CDK5L(legs, pairs):
    # five KEEP keys (any) + marked core <=8 at every segment state
    if len(keep_support(legs)) != 5:
        return False
    return cores_ok(pairs, False)

def _others_strict(iv, legs, skip):
    for j in range(len(iv)):
        if j in skip or iv[j]["w"] <= 0:
            continue
        if strict_K(iv[j], legs) or strict_P(iv[j], legs):
            continue
        return False
    return True

def m_NP(legs, pairs):
    if len(genuine_keys(legs)) != 5 or not cores_ok(pairs, True):
        return False
    return _others_strict(intervals(legs), legs, set())

def m_S1(legs, pairs):
    if len(genuine_keys(legs)) != 5 or not cores_ok(pairs, True):
        return False
    iv = intervals(legs)
    s = len(iv)
    if s < 5:
        return False
    E = E_slots(iv)
    if len(E) != 1:
        return False
    js = (E[0] + 1) % s
    if not (iv[js]["c"] == 1 and iv[js]["q"] <= 3 and iv[js]["H"] >= 2):
        return False
    return _others_strict(iv, legs, {E[0], js})

def m_S2(legs, pairs):
    if len(genuine_keys(legs)) != 5 or not cores_ok(pairs, True):
        return False
    iv = intervals(legs)
    s = len(iv)
    if s < 5:
        return False
    E = E_slots(iv)
    if len(E) != 1:
        return False
    j1, j2 = (E[0] + 1) % s, (E[0] + 2) % s
    if not (iv[j1]["c"] == 1 and iv[j1]["H"] == 1 and iv[j1]["q"] <= 2):
        return False
    if not (iv[j2]["c"] == 1 and iv[j2]["H"] >= 2 and iv[j2]["q"] <= 3):
        return False
    return _others_strict(iv, legs, {E[0], j1, j2})

def m_VR(legs, pairs):
    if len(genuine_keys(legs)) != 5 or not cores_ok(pairs, True):
        return False
    iv = intervals(legs)
    s = len(iv)
    if s < 5:
        return False
    E = E_slots(iv)
    if len(E) != 1:
        return False
    t = relay_len(iv, E[0])
    if not (2 <= t <= s - 2):
        return False
    p = (E[0] + t + 1) % s
    if not (iv[p]["c"] == 1 and iv[p]["H"] >= 2 and iv[p]["q"] <= 3):
        return False
    return _others_strict(iv, legs, {(E[0] + k) % s for k in range(t + 2)})

def m_MR(legs, pairs):
    if len(genuine_keys(legs)) != 5 or not cores_ok(pairs, True):
        return False
    iv = intervals(legs)
    s = len(iv)
    E = E_slots(iv)
    if len(E) < 2:
        return False
    used = set()
    for e in E:
        t = relay_len(iv, e)
        if not (2 <= t <= s - 2):
            return False
        p = (e + t + 1) % s
        if not (iv[p]["c"] == 1 and iv[p]["H"] >= 2 and iv[p]["q"] <= 3):
            return False
        pkt = {(e + k) % s for k in range(t + 2)}
        if pkt & used:
            return False
        used |= pkt
    return _others_strict(iv, legs, used)

# ---- merged A-root blocks (cyclic framing inside the given leg list) ----
def merged_blocks(legs):
    n = len(legs)
    f = next((i for i, lg in enumerate(legs) if lg["a"] >= 1), None)
    if f is None:
        return "A0"
    order = [(f + k) % n for k in range(n)]
    out, cur, gi0 = [], None, None
    for gi in order:
        lg = legs[gi]
        if lg["a"] >= 1:
            if cur is not None:
                out.append(cur)
            cur = {"key": lg["x"], "keys": [lg["x"]], "a": lg["a"],
                   "q": lg["q"], "genuine": bool(lg["chg"]), "dB": lg["dB"],
                   "rb": lg["rb"],
                   "keeps": sorted({lg["x"]} if lg["m"] == "K" else set()),
                   "dA": lg["dA"], "push": sorted(set(lg.get("push") or [])),
                   "l0": gi, "l1": gi + 1, "nleg": 1}
            gi0 = gi
        else:
            if cur is None or lg["x"] != cur["key"]:
                return None
            cur["a"] += lg["a"]; cur["q"] += lg["q"]
            cur["genuine"] = cur["genuine"] or bool(lg["chg"])
            if lg["m"] == "K":
                cur["keeps"] = sorted(set(cur["keeps"]) | {lg["x"]})
            cur["push"] = sorted(set(cur["push"]) | set(lg.get("push") or []))
            cur["l1"] = gi + 1; cur["nleg"] += 1
    if cur is not None:
        out.append(cur)
    for b in out:
        b["delta"] = b["q"] - 2 * b["a"]
    return out

def perleg_blocks(legs):
    return [{"key": lg["x"], "keys": [lg["x"]], "a": lg["a"], "q": lg["q"],
             "delta": lg["delta"], "genuine": bool(lg["chg"]), "dB": lg["dB"],
             "rb": lg["rb"], "keeps": [lg["x"]] if lg["m"] == "K" else []}
            for lg in legs]

def positives(mb):
    return [i for i, b in enumerate(mb) if b["delta"] > 0]

def snap_h(bdep, mb, i, r):
    return bdep[mb[i % len(mb)]["l1"] - 1].get(r)

def m_AJ(mb):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]; nb = mb[(i + 1) % m]
        if nb["key"] != b["rb"]:
            return False
        if not (0 < b["delta"] <= 2 * nb["a"] - 1):
            return False
    return True

def m_AK(mb, bdep, geometry=True):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]
        x, r = b["key"], b["rb"]
        b1 = mb[(i + 1) % m]; y = b1["key"]
        if not (b1["genuine"] and y != x and y != r):
            return False
        if geometry and not ((r - x) * (y - x) < 0):
            return False
        b2 = mb[(i + 2) % m]
        if b2["key"] != r or mb[(i + 1) % m]["delta"] > 0:
            return False
        h = snap_h(bdep, mb, i, r)
        if h is None or not (1 <= h <= 2):
            return False
        c = (h + 2) // 2
        if not (b["delta"] <= (2 * b1["a"] - b1["q"]) + (2 * b2["a"] - c)):
            return False
    return True

def m_ALS(mb):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]
        if b["delta"] not in (1, 2):
            return False
        x, r = b["key"], b["rb"]
        b1 = mb[(i + 1) % m]
        if not (b1["genuine"] and b1["key"] != x and b1["key"] != r):
            return False
        if b1["q"] != 2 * b1["a"]:
            return False
        b2 = mb[(i + 2) % m]
        if b2["key"] != r or b2["a"] < 2:
            return False
    return True

def m_AMG(mb, bdep):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]; r = b["rb"]
        b1, b2 = mb[(i + 1) % m], mb[(i + 2) % m]
        if not (b1["genuine"] and b1["key"] != r):
            return False
        if not (b2["genuine"] and b2["key"] != r):
            return False
        if b1["delta"] > 0 or b2["delta"] > 0:
            return False
        b3 = mb[(i + 3) % m]
        if b3["key"] != r:
            return False
        h = snap_h(bdep, mb, i, r)
        if h is None or not (1 <= h <= 2):
            return False
        c = (h + 4) // 2
        if not (2 * b3["a"] >= c):
            return False
        if not (b["delta"] <= (2 * b1["a"] - b1["q"]) +
                (2 * b2["a"] - b2["q"]) + (2 * b3["a"] - c)):
            return False
    return True

def m_AMS(mb):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]
        if b["delta"] != 1:
            return False
        x, r = b["key"], b["rb"]
        b1, b2 = mb[(i + 1) % m], mb[(i + 2) % m]
        if not (b1["genuine"] and b1["key"] != x and b1["key"] != r):
            return False
        if not (b2["genuine"] and b2["key"] != x and b2["key"] != r):
            return False
        if b1["q"] != 2 * b1["a"] or b2["q"] != 2 * b2["a"]:
            return False
        b3 = mb[(i + 3) % m]
        if b3["key"] != r or b3["a"] < 2:
            return False
    return True

def valid_AN_packet(mb, j):
    m = len(mb)
    if m < 4:
        return None
    b0 = mb[j % m]
    if not (b0["delta"] == 1 and b0["genuine"]):
        return None
    x, r = b0["key"], b0["rb"]
    b1 = mb[(j + 1) % m]; y = b1["key"]
    if not (b1["genuine"] and y != x and y != r):
        return None
    if not (b1["dB"] is not None and 1 <= b1["dB"] <= 3 and b1["a"] >= 1):
        return None
    b2 = mb[(j + 2) % m]; z = b2["key"]
    if not (b2["genuine"] and z != y and z != r) or b2["delta"] != 1:
        return None
    b3 = mb[(j + 3) % m]
    if b3["key"] != r or r not in b3["keeps"] or b3["a"] < 2:
        return None
    return True

def m_AN(mb):
    m = len(mb)
    pos = positives(mb)
    if not pos:
        return True
    valid = [j for j in range(m) if valid_AN_packet(mb, j) is not None]
    if not valid:
        return False
    memo = {}
    def search(ai, used, covered):
        key = (ai, used, covered)
        if key in memo:
            return memo[key]
        if covered == frozenset(pos):
            memo[key] = True
            return True
        if ai == len(valid):
            memo[key] = False
            return False
        if search(ai + 1, used, covered):
            memo[key] = True
            return True
        j = valid[ai]
        slots = frozenset((j + k) % m for k in range(4))
        res = False
        if not (slots & used) and mb[(j + 1) % m]["delta"] <= 0 \
                and mb[(j + 3) % m]["delta"] <= 0:
            new = frozenset(o for k in (0, 2) for o in [(j + k) % m]
                            if mb[o]["delta"] > 0)
            res = search(ai + 1, used | slots, covered | new)
        memo[key] = res
        return res
    return search(0, frozenset(), frozenset())

def recognizers(lb, mb, snaps):
    r = {}
    r["AO"] = AO.recognize(lb) is not None
    r["AP"] = bool(AP.recognize(mb).get("accepted", False))
    r["AQ"] = bool(AQ.recognize(mb).get("accepted", False))
    r["AR"] = bool(AR.recognize(mb).get("accepted", False))
    rAS = ASm.recognize(mb, snaps)
    r["AS"] = bool(rAS.get("accepted", False))
    return r

def full_banked(legs, pairs, snaps):
    """All 17 + RT2/CDK4/CDK5L. bdep/snaps keyed by leg index (slice frame)."""
    n = len(legs)
    bdep = [snaps.get(t, {}) for t in range(n)]
    lb = perleg_blocks(legs)
    mb = merged_blocks(legs)
    out = {}
    if not isinstance(mb, list):
        return None
    out.update(recognizers(lb, mb, snaps))
    out["AJ"] = m_AJ(mb)
    out["AK"] = m_AK(mb, bdep)
    out["ALG"] = m_AK(mb, bdep, geometry=False)
    out["ALS"] = m_ALS(mb)
    out["AMG"] = m_AMG(mb, bdep)
    out["AMS"] = m_AMS(mb)
    out["AN"] = m_AN(mb)
    out["NP"] = m_NP(legs, pairs)
    out["S1"] = m_S1(legs, pairs)
    out["S2"] = m_S2(legs, pairs)
    out["VR"] = m_VR(legs, pairs)
    out["MR"] = m_MR(legs, pairs)
    out["RT2"] = m_RT2(legs, pairs)
    out["CDK4"] = m_CDK4(legs, pairs)
    out["CDK5L"] = m_CDK5L(legs, pairs)
    return out
