# MSINK banked-union membership battery (exact per-theorem predicates).
# Member True => word is banked-covered (reject as residual witness).
# Member False => outside that class (exclusion evidence).
# Operates on screening replay products: legs, merged blocks, intervals, bdep.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import MSINK_bounded_search as B

def keep_dA(iv_j, legs):
    return legs[iv_j["gi"]]["dA"]

def isP(iv_j, legs, strict=False):
    x = iv_j["x"]
    if iv_j["H"] < 2:
        return False
    for k in iv_j["segi"]:
        lg = legs[k]
        if lg["m"] == "D" and lg["x"] != x:
            if not strict or (lg["a"] >= 1 and legs[iv_j["gi"]]["a"] >= 1):
                return True
    return False

def isK(iv_j, legs):
    return keep_dA(iv_j, legs) >= 3

def others_KP(iv, legs, skip, strictP=False):
    for j in range(len(iv)):
        if j in skip:
            continue
        if iv[j]["w"] <= 0:
            continue
        if isK(iv[j], legs) or isP(iv[j], legs, strictP):
            continue
        return False
    return True

def E_slots(iv):
    return [j for j in range(len(iv))
            if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]

def relay(iv, e):
    s = len(iv)
    k = 1
    while k < s:
        j = (e + k) % s
        if iv[j]["c"] == 1 and iv[j]["H"] == 1 and iv[j]["q"] <= 2:
            k += 1
        else:
            break
    return k - 1

def payer_ok(iv, p):
    return iv[p]["c"] == 1 and iv[p]["H"] >= 2 and iv[p]["q"] <= 3

def member_NP(iv, legs):
    return others_KP(iv, legs, set())

def member_S1(iv, legs):
    s = len(iv)
    if s < 5:
        return False
    E = E_slots(iv)
    if len(E) != 1:
        return False
    e = E[0]
    js = (e + 1) % s
    if not (iv[js]["c"] == 1 and iv[js]["q"] <= 3 and iv[js]["H"] >= 2):
        return False
    return others_KP(iv, legs, {e, js})

def member_S2(iv, legs):
    s = len(iv)
    if s < 5:
        return False
    E = E_slots(iv)
    if len(E) != 1:
        return False
    e = E[0]
    j1, j2 = (e + 1) % s, (e + 2) % s
    if not (iv[j1]["c"] == 1 and iv[j1]["H"] == 1 and iv[j1]["q"] <= 2):
        return False
    if not (iv[j2]["c"] == 1 and iv[j2]["H"] >= 2 and iv[j2]["q"] <= 3):
        return False
    return others_KP(iv, legs, {e, j1, j2})

def member_VR(iv, legs):
    s = len(iv)
    if s < 5:
        return False
    E = E_slots(iv)
    if len(E) != 1:
        return False
    e = E[0]
    t = relay(iv, e)
    if not (2 <= t <= s - 2):
        return False
    p = (e + t + 1) % s
    if not payer_ok(iv, p):
        return False
    used = {(e + k) % s for k in range(t + 2)}
    return others_KP(iv, legs, used)

def member_MR(iv, legs):
    s = len(iv)
    E = E_slots(iv)
    if len(E) < 2:
        return False
    used = set()
    for e in E:
        t = relay(iv, e)
        if not (2 <= t <= s - 2):
            return False
        p = (e + t + 1) % s
        if not payer_ok(iv, p):
            return False
        pkt = {(e + k) % s for k in range(t + 2)}
        if pkt & used:
            return False
        used |= pkt
    return others_KP(iv, legs, used, strictP=True)

# ---- merged-block mechanisms (AJ/AK/AL/AM need snapshot h) ----
def snap_h(bdep, mb, i, r):
    blk = mb[i % len(mb)]
    return bdep[blk["l1"] - 1].get(r)

def positives(mb):
    return [i for i, b in enumerate(mb) if b["delta"] > 0]

def member_AJ(mb):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]
        nb = mb[(i + 1) % m]
        if nb["key"] != b["rb"]:
            return False
        if not (0 < b["delta"] <= 2 * nb["a"] - 1):
            return False
    return True

def member_AK(mb, bdep, geometry=True):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]
        x, r = b["key"], b["rb"]
        b1 = mb[(i + 1) % m]
        y = b1["key"]
        if not (b1["genuine"] and y != x and y != r):
            return False
        if geometry and not ((r - x) * (y - x) < 0):
            return False
        b2 = mb[(i + 2) % m]
        if b2["key"] != r:
            return False
        if not (mb[(i + 1) % m]["delta"] <= 0):
            return False
        h = snap_h(bdep, mb, i, r)
        if h is None or not (1 <= h <= 2):
            return False
        c = (h + 2) // 2
        if not (b["delta"] <= (2 * b1["a"] - b1["q"]) + (2 * b2["a"] - c)):
            return False
    return True

def member_ALG(mb, bdep):
    return member_AK(mb, bdep, geometry=False)

def member_ALS(mb):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]
        if b["delta"] not in (1, 2):
            return False
        x, r = b["key"], b["rb"]
        b1 = mb[(i + 1) % m]
        if not (b1["genuine"] and b1["key"] != x and b1["key"] != r):
            return False
        if not (b1["q"] == 2 * b1["a"]):
            return False
        b2 = mb[(i + 2) % m]
        if b2["key"] != r:
            return False
        if not (b2["a"] >= 2):
            return False
    return True

def member_AMG(mb, bdep):
    m = len(mb)
    for i in positives(mb):
        b = mb[i]
        r = b["rb"]
        b1, b2 = mb[(i + 1) % m], mb[(i + 2) % m]
        if not (b1["genuine"] and b1["key"] != r):
            return False
        if not (b2["genuine"] and b2["key"] != r):
            return False
        if not (b1["delta"] <= 0 and b2["delta"] <= 0):
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

def member_AMS(mb):
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
        if not (b1["q"] == 2 * b1["a"] and b2["q"] == 2 * b2["a"]):
            return False
        b3 = mb[(i + 3) % m]
        if b3["key"] != r:
            return False
        if not (b3["a"] >= 2):
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
    b1 = mb[(j + 1) % m]
    y = b1["key"]
    if not (b1["genuine"] and y != x and y != r):
        return None
    if not (b1["dB"] is not None and 1 <= b1["dB"] <= 3 and b1["a"] >= 1):
        return None
    b2 = mb[(j + 2) % m]
    z = b2["key"]
    if not (b2["genuine"] and z != y and z != r):
        return None
    if b2["delta"] != 1:
        return None
    b3 = mb[(j + 3) % m]
    if b3["key"] != r:
        return None
    if r not in b3["keeps"]:
        return None
    if not (b3["a"] >= 2):
        return None
    return {"r": r}

def member_AN(mb):
    m = len(mb)
    pos = positives(mb)
    if not pos:
        return True
    valid = {}
    for j in range(m):
        pc = valid_AN_packet(mb, j)
        if pc is not None:
            valid[j] = pc
    if not valid:
        return False
    anchors = sorted(valid)
    memo = {}
    # exact disjoint cover of positives at slots 0/2
    def search(ai, used_mask, covered):
        key = (ai, used_mask, covered)
        if key in memo:
            return memo[key]
        if covered == frozenset(pos):
            memo[key] = True
            return True
        if ai == len(anchors):
            memo[key] = False
            return False
        if search(ai + 1, used_mask, covered):
            memo[key] = True
            return True
        j = anchors[ai]
        slots = frozenset((j + k) % m for k in range(4))
        res = False
        if not (slots & used_mask) and mb[(j + 1) % m]["delta"] <= 0 \
                and mb[(j + 3) % m]["delta"] <= 0:
            new = set()
            for k in (0, 2):
                o = (j + k) % m
                if mb[o]["delta"] > 0:
                    new.add(o)
            res = search(ai + 1, used_mask | slots, covered | frozenset(new))
        memo[key] = res
        return res
    return search(0, frozenset(), frozenset())
