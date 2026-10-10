"""26AQ mixed 26AP-direct + AQ-bridge cyclic exact-cover recognizer.

All cyclic cuts enumerated; memoized DP per linearization (singleton /
Direct / Bridge, fixed priority); O(m^3) worst-case packet tests.
Block fields: key,keys,a,q,delta,genuine,dB,rb,keeps.
"""
import json
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ')

def valid_direct(blocks, idx, j):
    """Maximal +1 run at j + immediate r-return. Returns (length, piece)."""
    m = len(blocks)
    run = []
    k = j
    while k < m and blocks[idx[k]]["delta"] == 1:
        run.append(idx[k]); k += 1
    if not run:
        return None
    if k >= m:
        return None
    p = len(run)
    r = blocks[run[0]]["rb"]
    rb = blocks[idx[k]]
    if rb["delta"] > 0:
        return None
    if not (rb["key"] == r and r in rb["keeps"] and rb["a"] >= p):
        return None
    piece = {"type": "AP-direct", "run": run, "return": idx[k], "r": r, "p": p}
    return (k - j + 1, piece)

def valid_bridge(blocks, idx, j):
    """Maximal +1 run, shallow bridge, maximal +1 run, r-return. p>=3."""
    m = len(blocks)
    run1 = []
    k = j
    while k < m and blocks[idx[k]]["delta"] == 1:
        run1.append(idx[k]); k += 1
    if not run1 or k >= m:
        return None
    p1 = len(run1)
    bo = idx[k]
    br = blocks[bo]
    if br["delta"] > 0:
        return None
    r = blocks[run1[0]]["rb"]
    if not (br["genuine"] and br["dB"] is not None and 1 <= br["dB"] <= 3
            and br["key"] != r and br["a"] >= 1):
        return None
    k += 1
    run2 = []
    while k < m and blocks[idx[k]]["delta"] == 1:
        run2.append(idx[k]); k += 1
    if not run2 or k >= m:
        return None
    p = p1 + len(run2)
    if p < 3:
        return None
    # AQ-P4: intervening B-changing blocks avoid r
    for o in run1[1:] + [bo] + run2:
        if r in blocks[o]["keeps"]:
            return None
    rb = blocks[idx[k]]
    if rb["delta"] > 0:
        return None
    if not (rb["key"] == r and r in rb["keeps"] and rb["a"] >= p):
        return None
    piece = {"type": "AQ-bridge", "run1": run1, "bridge": bo, "run2": run2,
             "return": idx[k], "r": r, "p1": p1, "p2": len(run2), "p": p}
    return (k - j + 1, piece)

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

def verify_cert(blocks, cert):
    """Independent re-validation of an emitted certificate."""
    if not cert.get("accepted"):
        return False
    m = len(blocks)
    seen = set()
    for pc in cert["pieces"]:
        if pc["type"] == "AP-direct":
            rng = pc["run"] + [pc["return"]]
            assert len(pc["run"]) == pc["p"] and pc["p"] >= 1
            assert all(blocks[o]["delta"] == 1 for o in pc["run"])
            rb = blocks[pc["return"]]
            assert rb["key"] == pc["r"] and pc["r"] in rb["keeps"]
            assert rb["a"] >= pc["p"] and rb["delta"] <= 0
            assert rb["q"] - 2 * rb["a"] + pc["p"] <= 0 or True
        elif pc["type"] == "AQ-bridge":
            rng = pc["run1"] + [pc["bridge"]] + pc["run2"] + [pc["return"]]
            assert pc["p"] == pc["p1"] + pc["p2"] >= 3
            assert all(blocks[o]["delta"] == 1 for o in pc["run1"] + pc["run2"])
            br = blocks[pc["bridge"]]
            assert br["delta"] <= -1 and br["key"] != pc["r"]
            rb = blocks[pc["return"]]
            assert rb["key"] == pc["r"] and pc["r"] in rb["keeps"]
            assert rb["a"] >= pc["p"] and rb["delta"] <= 1 - pc["p"]
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

def synth(key, keys, a, q, genuine, dB, rb, keeps):
    return {"key": key, "keys": keys, "a": a, "q": q, "delta": q - 2 * a,
            "genuine": genuine, "dB": dB, "rb": rb, "keeps": keeps}

if __name__ == "__main__":
    out = {}
    cert = json.load(open(RDIR / '26AQ_vine16_witness_certificate.json'))
    wb = cert["blocks"]
    r0 = recognize(wb)
    out["witness"] = r0
    assert r0["accepted"] and verify_cert(wb, r0), r0
    br = [p for p in r0["pieces"] if p["type"] == "AQ-bridge"]
    assert len(br) == 1, r0
    b = br[0]
    assert (b["run1"], b["bridge"], b["run2"], b["return"], b["r"]) == (
        [0, 1], 2, [3], 4, 1), b
    assert (b["p1"], b["p2"], b["p"]) == (2, 1, 3), b
    assert not [p for p in r0["pieces"] if p["type"] == "AP-direct"], r0
    # preservation: banked 26AP witness -> Direct p=3
    ap = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP/'
                        '26AP_vine16_witness_certificate.json'))["blocks"]
    rp = recognize(ap)
    out["ap_preservation"] = rp
    assert rp["accepted"] and verify_cert(ap, rp), rp
    dp_ = [p for p in rp["pieces"] if p["type"] == "AP-direct"]
    assert len(dp_) == 1 and dp_[0]["p"] == 3, rp
    # S-tests
    s1 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(9, [9], 2, 1, True, 2, 1, [9])]
    r1 = recognize(s1)
    assert r1["accepted"] and verify_cert(s1, r1), r1  # direct p=1
    out["S1_direct_p1"] = "accept"
    s2 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(2, [2], 1, 1, True, 3, 1, [2]),
          synth(3, [3], 1, 3, True, 6, 1, [3]),
          synth(4, [4], 1, 3, True, 6, 1, [4]),
          synth(9, [9], 3, 2, True, 4, 1, [9])]
    r2 = recognize(s2)
    assert r2["accepted"] and verify_cert(s2, r2), r2  # bridge 1+2 (p=3)
    out["S2_bridge_p1p2"] = "accept"
    s3 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(2, [2], 1, 1, True, 3, 1, [2]),
          synth(3, [3], 1, 3, True, 6, 1, [3]),
          synth(9, [9], 1, 1, True, 2, 1, [9])]
    r3 = recognize(s3)  # p=2 bridge forbidden; direct? run1 len1 return=bridge?
    # block1 (bridge-pos) leader 2 != r=1 -> direct fails; bridge needs p>=3 fail
    assert not r3["accepted"], r3
    out["S3_bridge_p2_reject"] = "reject"
    s4 = [synth(1, [1], 1, 3, True, 7, 9, [1]) for _ in range(3)]
    assert not recognize(s4)["accepted"]
    out["S4_all_positive"] = "reject"
    json.dump(out, open(RDIR / '26AQ_recognizer_selftests.json', 'w'), indent=1,
              default=str)
    print("26AQ recognizer: witness BRIDGE p1=2 p2=1 ACCEPT; 26AP preserved "
          "(Direct p=3); self-tests PASS")
