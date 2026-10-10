"""26AR ARmix exact-cover recognizer: Direct (banked 26AP) + Bridge (banked
26AQ) + Split-Sink (new), all cyclic cuts x memoized DP. O(m^4) worst case.

Block fields: key,keys,a,q,delta,genuine,dB,rb,keeps,dA (leader pre-A-depth).
Direct/Bridge matchers are IMPORTED from the banked 26AQ module (exact
preservation by construction). Split-Sink implements AR-P1..P10 (no aggregate
premise; u/v thresholds checked separately; a_r,a_s<p required).
"""
import json, importlib.util
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AR')

def _load_banked(name, rel):
    spec = importlib.util.spec_from_file_location(
        name, str(Path('DO_RESEARCH_REBOOT/06_CERTIFICATES') / rel))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
_AQ = _load_banked('aq26_banked', '26AQ/26AQ_mixed_cyclic_dp_recognizer.py')
valid_direct = _AQ.valid_direct
valid_bridge = _AQ.valid_bridge

def valid_split(blocks, idx, j):
    m = len(blocks)
    # candidate run lengths p>=3 (bounded by remaining length)
    k = j
    run = []
    while k < m and blocks[idx[k]]["delta"] == 1:
        run.append(idx[k]); k += 1
    if len(run) < 3:
        return None
    # try every p in [3, len(run)] (run may extend; maximal-run semantics:
    # a longer +1 run would need its own cover; DP explores all p)
    for p in range(3, len(run) + 1):
        r = blocks[run[0]]["rb"]
        s = blocks[run[p - 1]]["rb"]
        if r == s:
            continue
        if not all(blocks[o]["genuine"] for o in run[:p]):
            continue
        # AR-P4: intervening keeps avoid r
        if any(r in blocks[o]["keeps"] for o in run[1:p]):
            continue
        if j + p + 1 >= m:
            continue
        r1, r2 = idx[j + p], idx[j + p + 1]
        b1, b2 = blocks[r1], blocks[r2]
        if b1["delta"] > 0 or b2["delta"] > 0:
            continue
        if not (b1["key"] == r and r in b1["keeps"]):
            continue
        if not (b2["key"] == s and s in b2["keeps"]):
            continue
        u = (p + 2) // 2  # ceil((p+1)/2)
        v = (p + 1) // 2  # floor((p+1)/2)
        if not (b1.get("dA") is not None and b1["dA"] >= 2 * u - 1):
            continue
        if not (b2.get("dA") is not None and b2["dA"] >= 2 * v - 1):
            continue
        if not (b1["a"] < p and b2["a"] < p):  # AR-P8
            continue
        piece = {"type": "AR-split", "run": run[:p], "ret1": r1, "ret2": r2,
                 "r": r, "s": s, "p": p, "u": u, "v": v}
        return (p + 2, piece)
    return None

def recognize(blocks):
    m = len(blocks)
    if m == 0:
        return None
    if all(b["delta"] <= 0 for b in blocks):
        return {"accepted": True, "pieces": [], "singles": list(range(m)),
                "cut": None, "m": m}
    for cut in range(m):
        idx = [(cut + t) % m for t in range(m)]
        memo = {}
        def dp(p):
            if p == m:
                return []
            if p in memo:
                return memo[p]
            o = idx[p]
            res = None
            if blocks[o]["delta"] <= 0:
                t = dp(p + 1)
                if t is not None:
                    res = [("S", o)] + t
            if res is None:
                d = valid_direct(blocks, idx, p)
                if d is not None:
                    L, piece = d
                    t = dp(p + L)
                    if t is not None:
                        res = [("D", piece)] + t
            if res is None:
                d = valid_bridge(blocks, idx, p)
                if d is not None:
                    L, piece = d
                    t = dp(p + L)
                    if t is not None:
                        res = [("B", piece)] + t
            if res is None:
                d = valid_split(blocks, idx, p)
                if d is not None:
                    L, piece = d
                    t = dp(p + L)
                    if t is not None:
                        res = [("T", piece)] + t
            memo[p] = res
            return res
        path = dp(0)
        if path is not None:
            pieces, singles = [], []
            for typ, v in path:
                if typ == "S":
                    singles.append(v)
                else:
                    pieces.append(v)
            return {"accepted": True, "pieces": pieces,
                    "singles": sorted(singles), "cut": cut, "m": m}
    return {"accepted": False, "m": m}

def _chk(cond):
    return bool(cond)

def verify_cert(blocks, cert):
    if not cert.get("accepted"):
        return False
    m = len(blocks)
    seen = set()
    for pc in cert["pieces"]:
        t = pc["type"]
        if t == "AP-direct":
            rng = pc["run"] + [pc["return"]]
            if not _chk(pc["p"] >= 1 and all(blocks[o]["delta"] == 1 for o in pc["run"])):
                return False
            rb = blocks[pc["return"]]
            if not _chk(rb["key"] == pc["r"] and pc["r"] in rb["keeps"] and rb["a"] >= pc["p"]):
                return False
            if not _chk(rb["delta"] <= 0):
                return False
        elif t == "AQ-bridge":
            rng = pc["run1"] + [pc["bridge"]] + pc["run2"] + [pc["return"]]
            if not _chk(pc["p"] == pc["p1"] + pc["p2"] >= 3):
                return False
            if not _chk(all(blocks[o]["delta"] == 1 for o in pc["run1"] + pc["run2"])):
                return False
            if not _chk(blocks[pc["bridge"]]["delta"] <= -1):
                return False
            rb = blocks[pc["return"]]
            if not _chk(rb["key"] == pc["r"] and pc["r"] in rb["keeps"] and rb["a"] >= pc["p"]):
                return False
        elif t == "AR-split":
            p = pc["p"]
            if not _chk(p >= 3 and len(pc["run"]) == p):
                return False
            if not _chk(all(blocks[o]["delta"] == 1 for o in pc["run"])):
                return False
            r1 = blocks[pc["ret1"]]; r2 = blocks[pc["ret2"]]
            if not _chk(r1["key"] == pc["r"] and pc["r"] in r1["keeps"]):
                return False
            if not _chk(r2["key"] == pc["s"] and pc["s"] in r2["keeps"]):
                return False
            if not _chk(pc["r"] != pc["s"] and r1["a"] < p and r2["a"] < p):
                return False
            u = (p + 2) // 2; v = (p + 1) // 2
            if not _chk(r1["dA"] >= 2 * u - 1 and r2["dA"] >= 2 * v - 1):
                return False
            # theorem cross-checks (derived, not admission):
            if not _chk(r1["delta"] <= p - 2 * u and r2["delta"] <= 2 - 2 * v):
                return False
            if not _chk(p + r1["delta"] + r2["delta"] <= 0):
                return False
            rng = pc["run"] + [pc["ret1"], pc["ret2"]]
        else:
            return False
        for o in rng:
            if o in seen:
                return False
            seen.add(o)
    for o in cert["singles"]:
        if o in seen or blocks[o]["delta"] > 0:
            return False
        seen.add(o)
    return seen == set(range(m))

def essentiality(blocks, piece):
    p = piece["p"]
    dr = blocks[piece["ret1"]]["delta"]; ds = blocks[piece["ret2"]]["delta"]
    return {"p+dr>0": p + dr > 0, "p+ds>0": p + ds > 0,
            "joint<=0": p + dr + ds <= 0,
            "essential": (p + dr > 0) and (p + ds > 0) and (p + dr + ds <= 0)}

def synth(key, keys, a, q, genuine, dB, rb, keeps, dA):
    return {"key": key, "keys": keys, "a": a, "q": q, "delta": q - 2 * a,
            "genuine": genuine, "dB": dB, "rb": rb, "keeps": keeps, "dA": dA}

def enrich(wblocks, legs):
    out, li = [], 0
    for b in wblocks:
        b = dict(b)
        b["dA"] = legs[li]["dA"]
        li += b.get("nleg", 1)
        out.append(b)
    return out

if __name__ == "__main__":
    out = {}
    cert = json.load(open(RDIR / '26AR_vine16_closed_witness.json'))
    wb = enrich(cert["blocks"], cert["legs"])
    # T1: witness ACCEPT as Split
    r0 = recognize(wb)
    out["T1_witness"] = r0
    assert r0["accepted"] and verify_cert(wb, r0), r0
    sp = [p for p in r0["pieces"] if p["type"] == "AR-split"]
    assert len(sp) == 1, r0
    t = sp[0]
    assert (t["run"], t["ret1"], t["ret2"], t["r"], t["s"], t["p"]) == (
        [0, 1, 2], 3, 4, 16, 4, 3), t
    ess = essentiality(wb, t)
    out["T1_essentiality"] = ess
    assert ess["essential"], ess
    assert all(b["delta"] <= 0 for i, b in enumerate(wb) if i not in (0, 1, 2, 3, 4))
    # T2/T3: banked 26AP / 26AQ witnesses preserved
    ap = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP/'
                        '26AP_vine16_witness_certificate.json'))
    apb = enrich(ap["blocks"], ap["legs"])
    rp = recognize(apb)
    out["T2_ap_preserved"] = {"accepted": rp["accepted"]}
    assert rp["accepted"] and verify_cert(apb, rp), rp
    assert any(p["type"] == "AP-direct" and p["p"] == 3 for p in rp["pieces"]), rp
    aq = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ/'
                        '26AQ_vine16_witness_certificate.json'))
    aqb = enrich(aq["blocks"], aq["legs"])
    rq = recognize(aqb)
    out["T3_aq_preserved"] = {"accepted": rq["accepted"]}
    assert rq["accepted"] and verify_cert(aqb, rq), rq
    assert any(p["type"] == "AQ-bridge" for p in rq["pieces"]), rq
    # T4/T5: rotations incl. boundary-crossing packet
    n = len(wb)
    for rot in (5, n - 2):
        wr = wb[rot:] + wb[:rot]
        rr = recognize(wr)
        assert rr["accepted"] and verify_cert(wr, rr), (rot, rr)
        assert any(p["type"] == "AR-split" for p in rr["pieces"]), (rot, rr)
    out["T4_rot5"], out["T5_rot_boundary"] = "accept", "accept"
    # T6/T7/T8: wrong r / wrong s / r==s
    bad = [dict(b) for b in wb[:5]]
    bad[3] = dict(bad[3]); bad[3]["key"] = 15; bad[3]["keeps"] = [15]
    assert not recognize(bad + [dict(b, delta=-1) for b in wb[5:]])["accepted"]
    out["T6_wrong_r"] = "reject"
    bad = [dict(b) for b in wb[:5]]
    bad[4] = dict(bad[4]); bad[4]["key"] = 15; bad[4]["keeps"] = [15]
    assert not recognize(bad + [dict(b, delta=-1) for b in wb[5:]])["accepted"]
    out["T7_wrong_s"] = "reject"
    s0 = [synth(1, [1], 1, 3, True, 7, 9, [1], 2),
          synth(2, [2], 1, 3, True, 6, 9, [2], 2),
          synth(3, [3], 1, 3, True, 6, 9, [3], 2),
          synth(9, [9], 2, 2, True, 4, 1, [9], 4),
          synth(9, [9], 2, 2, True, 4, 1, [9], 4)]
    assert not recognize(s0)["accepted"]  # r==s==9
    out["T8_r_eq_s"] = "reject"
    # T9/T10: threshold failures (make returns fail S; D/B also fail by design)
    th = [synth(1, [1], 1, 3, True, 7, 9, [1], 2),
          synth(2, [2], 1, 3, True, 6, 9, [2], 2),
          synth(3, [3], 1, 3, True, 6, 9, [3], 2),
          synth(9, [9], 2, 2, True, 4, 1, [9], 2),   # dA=2 <3: T9
          synth(4, [4], 2, 2, True, 4, 1, [4], 4)]
    r9 = recognize(th)
    assert not (r9["accepted"] and any(
        p["type"] == "AR-split" for p in r9["pieces"])), r9
    out["T9_first_threshold"] = "reject-as-S"
    th2 = [synth(1, [1], 1, 3, True, 7, 9, [1], 2),
           synth(2, [2], 1, 3, True, 6, 9, [2], 2),
           synth(3, [3], 1, 3, True, 6, 9, [3], 2),
           synth(9, [9], 2, 2, True, 4, 1, [9], 4),
           synth(4, [4], 2, 2, True, 4, 1, [4], 2)]  # dA=2 <3: T10
    r10 = recognize(th2)
    assert not (r10["accepted"] and any(
        p["type"] == "AR-split" for p in r10["pieces"])), r10
    out["T10_second_threshold"] = "reject-as-S"
    # T11: a_r>=p -> reject as S (Direct p=3 + return a=3 valid -> D accept ok)
    th3 = [synth(1, [1], 1, 3, True, 7, 9, [1], 2),
           synth(2, [2], 1, 3, True, 6, 9, [2], 2),
           synth(3, [3], 1, 3, True, 6, 9, [3], 2),
           synth(9, [9], 3, 2, True, 4, 1, [9], 6),
           synth(4, [4], 2, 2, True, 4, 1, [4], 4)]
    r11 = recognize(th3)
    assert not any(p["type"] == "AR-split" for p in r11.get("pieces", [])), r11
    out["T11_old_deep_sink"] = "no-S-piece"
    # T12: verifier catches fabricated overlapping cert
    fake = {"accepted": True,
            "pieces": [{"type": "AP-direct", "run": [0], "return": 1, "r": 9, "p": 1},
                       {"type": "AP-direct", "run": [1], "return": 2, "r": 8, "p": 1}],
            "singles": [], "cut": 0, "m": 3}
    assert not verify_cert(wb[:3], fake)
    out["T12_overlap_caught"] = "verifier-rejects"
    # T13/T14: uncovered positive / all-positive
    u1 = [synth(1, [1], 1, 3, True, 7, 9, [1], 2),
          synth(2, [2], 1, 0, False, None, 2, [], 1)]
    assert not recognize(u1)["accepted"]
    out["T13_uncovered"] = "reject"
    assert not recognize(
        [synth(1, [1], 1, 3, True, 7, 9, [1], 2) for _ in range(4)])["accepted"]
    out["T14_all_positive"] = "reject"
    # T15: old 14-key control (+1,+1,+1,-3,-2) fails essentiality
    ctrl = [synth(1, [1], 1, 3, True, 7, 9, [1], 2),
            synth(2, [2], 1, 3, True, 6, 9, [2], 2),
            synth(3, [3], 1, 3, True, 6, 9, [3], 2),
            synth(9, [9], 3, 3, True, 6, 1, [9], 6),
            synth(4, [4], 2, 2, True, 4, 1, [4], 4)]
    cp = {"p": 3, "ret1": 3, "ret2": 4}
    ce = essentiality(ctrl, cp)
    out["T15_14key_control"] = ce
    assert not ce["essential"] and ce["p+dr>0"] is False, ce
    json.dump(out, open(RDIR / '26AR_recognizer_selftests.json', 'w'), indent=1,
              default=str)
    print("26AR recognizer: witness SPLIT ACCEPT + essential; AP/AQ preserved; "
          "rotations ok; 15/15 self-tests PASS")
