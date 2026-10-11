# CRA strict frozen MSINK membership (fresh H1-H6, existential sink, strict K/P).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')

def intervals(legs):
    n = len(legs)
    ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
    out = []
    for t, i in enumerate(ki):
        prev = ki[t - 1]
        if prev < i:
            segi = list(range(prev + 1, i + 1))
        else:
            segi = list(range(prev + 1, n)) + list(range(0, i + 1))
        H = sum(legs[k]["a"] for k in segi)
        x = legs[i]["x"]; xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        out.append({"x": x, "H": H, "c": c, "q": legs[i]["q"],
                    "w": legs[i]["q"] - 2 * c, "R": 2 * (H - c), "gi": i,
                    "segi": segi})
    return out

def strict_K(ivj, legs):
    return legs[ivj["gi"]]["dA"] >= 3

def strict_P(ivj, legs):
    # immediately preceding ORIGINAL ACCESS occurrence (gi-1, seam-aware)
    n = len(legs)
    gi = ivj["gi"]
    prev = legs[(gi - 1) % n]
    cur = legs[gi]
    if cur["m"] != "K":
        return False
    return (prev["m"] == "D" and prev["x"] != cur["x"]
            and prev["a"] >= 1 and cur["a"] >= 1)

def E_slots(iv):
    return [j for j in range(len(iv))
            if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]

def relay_len(iv, e):
    s = len(iv)
    k = 1
    while k < s:
        j = (e + k) % s
        if iv[j]["c"] == 1 and iv[j]["H"] == 1 and iv[j]["q"] <= 2:
            k += 1
        else:
            break
    return k - 1

def strict_msink(legs):
    """Returns dict: member bool, E, relays, sinks (all jointly eligible),
    per-positive dispositions. Pure frozen predicates."""
    iv = intervals(legs)
    s = len(iv)
    E = E_slots(iv)
    res = {"s": s, "E": E, "member": False, "sinks": [], "t": {},
           "pos": [], "stage": None}
    if len(E) != 2:
        res["stage"] = "E-count-%d" % len(E)
        return res
    tl = []
    for e in E:
        tl.append(relay_len(iv, e))
    res["t"] = dict(zip(E, tl))
    if not ((tl[0] in (0, 1)) ^ (tl[1] in (0, 1))):
        res["stage"] = "mixed-relay-%s" % (tl,)
        return res
    for p in range(s):
        if p in E or not (iv[p]["c"] == 1 and iv[p]["H"] >= 3):
            continue
        jp = iv[p]
        if jp["q"] > 4 or not (jp["w"] <= jp["R"] - 2):
            continue
        ok = True
        for j in range(s):
            if j in E or j == p or iv[j]["w"] <= 0:
                continue
            if strict_K(iv[j], legs) or strict_P(iv[j], legs):
                continue
            ok = False
            break
        if ok:
            res["sinks"].append(p)
    if not res["sinks"]:
        res["stage"] = "no-joint-sink"
        return res
    res["member"] = True
    res["stage"] = "member"
    for j in range(s):
        if iv[j]["w"] > 0:
            d = {"j": j, "x": iv[j]["x"], "H": iv[j]["H"], "c": iv[j]["c"],
                 "q": iv[j]["q"], "w": iv[j]["w"], "R": iv[j]["R"],
                 "dA": legs[iv[j]["gi"]]["dA"],
                 "K": strict_K(iv[j], legs), "P": strict_P(iv[j], legs),
                 "role": ("E" if j in E else ("sink" if j == res["sinks"][0] else "other"))}
            res["pos"].append(d)
    return res
