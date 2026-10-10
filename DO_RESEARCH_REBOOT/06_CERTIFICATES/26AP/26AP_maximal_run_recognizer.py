"""26AP deterministic maximal-run recognizer (amended cut convention, O(m)).

Cut: if no positives ACCEPT; if all positive REJECT; else pick smallest-index
nonpositive j, linearize j+1..j (mod m), single left-to-right scan.
Run = maximal consecutive positives (each delta==1); return = immediately
following block: leader key==r (rb of run's first block), r in keeps, a>=p.
"""
import json
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP')

def recognize(blocks, j=None):
    m = len(blocks)
    if m == 0:
        return None
    pos = [i for i, b in enumerate(blocks) if b["delta"] > 0]
    if not pos:
        return {"accepted": True, "runs": [], "singles": list(range(m)),
                "cut": None, "m": m}
    if len(pos) == m:
        return {"accepted": False, "reason": "all-positive", "m": m}
    nonpos = [i for i in range(m) if blocks[i]["delta"] <= 0]
    if j is None:
        j = min(nonpos)
    assert blocks[j]["delta"] <= 0, "cut must follow a nonpositive block"
    lin = [(j + 1 + t) % m for t in range(m)]
    runs, singles, used = [], [], set()
    t = 0
    while t < m:
        o = lin[t]
        b = blocks[o]
        if b["delta"] <= 0:
            if o in used:
                return {"accepted": False, "reason": "reuse", "m": m}
            used.add(o); singles.append(o); t += 1
            continue
        # maximal positive run in linearized order
        run = []
        while t < m and blocks[lin[t]]["delta"] > 0:
            run.append(lin[t]); t += 1
        for o2 in run:
            if blocks[o2]["delta"] != 1:
                return {"accepted": False, "reason": "non-unit-positive", "m": m}
        p = len(run)
        if t >= m:
            return {"accepted": False, "reason": "run-at-end-no-return", "m": m}
        ro = lin[t]
        r = blocks[run[0]]["rb"]
        rb2 = blocks[ro]
        if not (rb2["key"] == r and r in rb2["keeps"] and rb2["a"] >= p):
            return {"accepted": False, "reason": "bad-return", "m": m}
        if ro in used or any(o2 in used for o2 in run):
            return {"accepted": False, "reason": "overlap", "m": m}
        if rb2["delta"] > 0:
            return {"accepted": False, "reason": "return-is-positive", "m": m}
        used.update(run); used.add(ro)
        runs.append({"start": run[0], "len": p, "return": ro, "r": r})
        t += 1
    if set(used) != set(range(m)):
        return {"accepted": False, "reason": "unconsumed", "m": m}
    return {"accepted": True, "runs": runs, "singles": sorted(singles),
            "cut": j, "m": m}

def synth(key, keys, a, q, genuine, dB, rb, keeps):
    return {"key": key, "keys": keys, "a": a, "q": q, "delta": q - 2 * a,
            "genuine": genuine, "dB": dB, "rb": rb, "keeps": keeps}

if __name__ == "__main__":
    out = {}
    cert = json.load(open(RDIR / '26AP_vine16_witness_certificate.json'))
    wb = cert["blocks"]
    r0 = recognize(wb)
    out["witness"] = r0
    assert r0["accepted"] and len(r0["runs"]) == 1, r0
    run = r0["runs"][0]
    assert (run["start"], run["len"], run["return"], run["r"]) == (0, 3, 3, 1), run
    assert cert["blocks"][3]["a"] == 3 and sum(
        cert["blocks"][i]["delta"] for i in [0, 1, 2, 3]) == -1
    # cut independence: every nonpositive j -> same decision + same cyclic runs
    nonpos = [i for i, b in enumerate(wb) if b["delta"] <= 0]
    cyc = sorted((rn["start"], rn["len"], rn["return"]) for rn in r0["runs"])
    cuts = {}
    for j in nonpos:
        rj = recognize(wb, j)
        assert rj["accepted"], (j, rj)
        assert sorted((rn["start"], rn["len"], rn["return"])
                      for rn in rj["runs"]) == cyc, (j, rj)
        cuts[str(j)] = {"accepted": True, "cut": rj["cut"]}
    out["cut_independence"] = {"n_cuts_tested": len(nonpos), "all_agree": True,
                               "cuts": cuts}
    # S1: no positives -> accept
    s1 = [synth(1, [1], 2, 1, True, 3, 9, [1]), synth(2, [2], 1, 0, False, None, 2, [])]
    assert recognize(s1)["accepted"]
    out["S1_no_positive"] = "accept"
    # S2: synthetic p=1 run + return
    s2 = [synth(5, [5], 1, 3, True, 7, 8, [5]),
          synth(8, [8], 1, 1, True, 2, 5, [8]),
          synth(3, [3], 2, 0, False, None, 3, [])]
    r2 = recognize(s2)
    assert r2["accepted"] and r2["runs"][0]["len"] == 1, r2
    out["S2_p1"] = "accept"
    # S3: all-positive -> reject
    s3 = [synth(1, [1], 1, 3, True, 7, 9, [1]) for _ in range(4)]
    assert not recognize(s3)["accepted"]
    out["S3_all_positive"] = "reject"
    # S4: positive without valid return -> reject
    s4 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(2, [2], 1, 0, False, None, 2, [])]
    assert not recognize(s4)["accepted"]
    out["S4_no_return"] = "reject"
    # S5: non-unit positive (+2) -> reject
    s5 = [synth(1, [1], 1, 4, True, 8, 9, [1]),
          synth(9, [9], 2, 1, True, 2, 1, [9])]
    assert not recognize(s5)["accepted"]
    out["S5_nonunit"] = "reject"
    # S6: return with a<p -> reject
    s6 = [synth(1, [1], 1, 3, True, 7, 9, [1]),
          synth(2, [2], 1, 3, True, 6, 1, [2]),
          synth(9, [9], 1, 1, True, 2, 1, [9])]
    assert not recognize(s6)["accepted"]
    out["S6_short_return"] = "reject"
    json.dump(out, open(RDIR / '26AP_recognizer_selftests.json', 'w'), indent=1,
              default=str)
    print("26AP recognizer: witness ACCEPT p=3; cuts tested=%d all agree; "
          "self-tests 6/6 PASS" % len(nonpos))
