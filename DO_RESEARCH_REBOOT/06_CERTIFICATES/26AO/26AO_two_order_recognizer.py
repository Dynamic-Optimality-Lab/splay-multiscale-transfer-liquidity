"""26AO deterministic two-order cyclic packet recognizer (DP per cut, O(m^2)).

Block record fields: key (leader), keys (all accessed keys in block),
a, q, delta, genuine (block's B splay changed B), dB (pre-access B-depth of
that splay or None), rb (B-root before the block's first B splay),
keeps (keys KEEPed in block).
Type I matcher = exact banked 26AN-P P1-P7. Type II matcher = AO-P1-P7.
"""
import json
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AO')

def match_type1(b):
    """26AN-P: (+1, shallow<= -1, +1, r-return<= -1). b = 4 block records."""
    if not (b[0]['delta'] == 1 and b[0]['genuine']):
        return False
    x, r = b[0]['key'], b[0]['rb']
    if x == r:
        return False
    b1 = b[1]
    if not (b1['genuine'] and b1['key'] != x and b1['key'] != r):
        return False
    if not (b1['dB'] is not None and 1 <= b1['dB'] <= 3 and b1['a'] >= 1):
        return False
    b2 = b[2]
    if not (b2['genuine'] and b2['key'] != b1['key'] and b2['key'] != r):
        return False
    if b2['delta'] != 1:
        return False
    b3 = b[3]
    if not (b3['key'] == r and r in b3['keeps']):
        return False
    if r in b1['keys'] or r in b2['keys']:
        return False
    return b3['a'] >= 2

def match_type2(b):
    """AO-P: (+1, +1, shallow<= -1, r-return<= -1)."""
    if not (b[0]['delta'] == 1 and b[0]['genuine']):
        return False
    x, r = b[0]['key'], b[0]['rb']
    if x == r:
        return False
    b1 = b[1]
    if not (b1['genuine'] and b1['delta'] == 1 and b1['key'] != x
            and b1['key'] != r):
        return False
    b2 = b[2]
    if not (b2['genuine'] and b2['key'] != b1['key'] and b2['key'] != r):
        return False
    if not (b2['dB'] is not None and 1 <= b2['dB'] <= 3 and b2['a'] >= 1):
        return False
    b3 = b[3]
    if not (b3['key'] == r and r in b3['keeps']):
        return False
    if r in b1['keys'] or r in b2['keys']:
        return False
    return b3['a'] >= 2

def recognize(blocks):
    """Return cert dict or None. Deterministic: cuts ascending, DP with fixed
    option order (singleton, Type I, Type II). O(m^2) packet tests."""
    m = len(blocks)
    if m == 0:
        return None
    order = list(range(m))
    for cut in order:
        idx = [(cut + p) % m for p in range(m)]
        # DP over consumed-prefix length; memo[pos] = decision
        memo = {}
        def dp(p):
            if p == m:
                return ()
            if p in memo:
                return memo[p]
            o = idx[p]
            res = None
            if blocks[o]['delta'] <= 0:
                t = dp(p + 1)
                if t is not None:
                    res = (('S', o),) + t
            if res is None and p + 4 <= m:
                quad = [blocks[idx[p + k]] for k in range(4)]
                if match_type1(quad):
                    t = dp(p + 4)
                    if t is not None:
                        res = (('I', tuple(idx[p + k] for k in range(4))),) + t
            if res is None and p + 4 <= m:
                quad = [blocks[idx[p + k]] for k in range(4)]
                if match_type2(quad):
                    t = dp(p + 4)
                    if t is not None:
                        res = (('II', tuple(idx[p + k] for k in range(4))),) + t
            memo[p] = res
            return res
        path = dp(0)
        if path is not None:
            anchors, types, singles = [], [], []
            for typ, rng in path:
                if typ == 'S':
                    singles.append(rng)
                else:
                    anchors.append(rng[0]); types.append(typ)
            return {"cut": cut, "anchors": anchors, "types": types,
                    "singles": sorted(singles),
                    "m": m, "accepted": True}
    return None

def leg_to_block(lg):
    return {"key": lg["x"], "keys": [lg["x"]], "a": lg["a"], "q": lg["q"],
            "delta": lg["delta"], "genuine": bool(lg["bchanged"]),
            "dB": lg["dB"], "rb": lg["rb"],
            "keeps": [lg["x"]] if lg["m"] == "K" else []}

def synth(key, keys, a, q, genuine, dB, rb, keeps):
    return {"key": key, "keys": keys, "a": a, "q": q, "delta": q - 2 * a,
            "genuine": genuine, "dB": dB, "rb": rb, "keeps": keeps}

if __name__ == "__main__":
    results = {}
    # T1 (positive): real 26AO witness -> Type II anchor [0]
    cert = json.load(open(RDIR / '26AO_ten_key_witness_certificate.json'))
    wblocks = [leg_to_block(l) for l in cert["legs"]]
    r = recognize(wblocks)
    results["T1_witness_TypeII"] = r
    assert r and r["anchors"] == [0] and r["types"] == ["II"], r
    assert sorted(r["singles"]) == list(range(4, 18)), r
    # T2 (positive): synthetic Type I packet + nonpositive tail
    t1 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(2, [2], 1, 1, True, 3, 1, [2]),
          synth(3, [3], 1, 3, True, 6, 1, [3]),
          synth(9, [9], 2, 1, True, 2, 1, [9]),
          synth(4, [4], 1, 0, False, None, 4, [])]
    r2 = recognize(t1)
    results["T2_synthetic_TypeI"] = r2
    assert r2 and r2["anchors"] == [0] and r2["types"] == ["I"], r2
    # T3 (negative): consecutive positives, slot3 leader is not r
    t3 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(2, [2], 1, 3, True, 6, 1, [2]),
          synth(3, [3], 1, 1, True, 3, 1, [3]),
          synth(5, [5], 2, 1, True, 2, 1, [5])]
    r3 = recognize(t3)
    results["T3_negative_wrong_r"] = r3
    assert r3 is None, r3
    # T4 (negative): all-positive walk, no packet possible
    t4 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(2, [2], 1, 3, True, 6, 1, [2]),
          synth(3, [3], 1, 3, True, 7, 1, [3]),
          synth(4, [4], 1, 3, True, 6, 1, [4])]
    r4 = recognize(t4)
    results["T4_negative_all_positive"] = r4
    assert r4 is None, r4
    # T5: m<4 all-nonpositive accepted; with positive rejected
    t5a = [synth(1, [1], 2, 1, True, 3, 9, [1]),
           synth(2, [2], 1, 0, False, None, 2, [])]
    r5a = recognize(t5a)
    results["T5a_small_nonpositive"] = r5a
    assert r5a and r5a["anchors"] == [], r5a
    t5b = [synth(1, [1], 1, 3, True, 7, 9, [1]),
           synth(2, [2], 1, 0, False, None, 2, [])]
    r5b = recognize(t5b)
    results["T5b_small_positive"] = r5b
    assert r5b is None, r5b
    json.dump(results, open(RDIR / '26AO_recognizer_audit.json', 'w'), indent=1,
              default=str)
    print("recognizer self-tests: 5/5 PASS; witness ->", r["types"], r["anchors"])
