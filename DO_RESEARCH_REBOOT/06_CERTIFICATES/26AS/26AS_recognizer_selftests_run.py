"""26AS recognizer self-tests (imports the recognizer module)."""
import json, importlib.util
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS')
spec = importlib.util.spec_from_file_location(
    'as26', str(RDIR / '26AS_mixed_cyclic_recognizer.py'))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

def S(key, keys, a, q, genuine, dB, rb, keeps, dA, push=None, l0=0, l1=1):
    return M.synth(key, keys, a, q, genuine, dB, rb, keeps, dA, push, l0, l1)

out = {}
# T1: synthetic AS accept (mr=ms=1, dr0=ds0=2, W dual-push, CW=1)
as1 = [S(1, [1], 1, 3, True, 7, 9, [1], 2, [], 0, 1),
       S(5, [5], 1, 0, False, None, 5, [], 1, [], 1, 2),
       S(3, [3], 1, 3, True, 6, 2, [3], 2, [], 2, 3),
       S(4, [4], 1, 1, True, 2, 1, [4], 1, [9, 2], 3, 4),
       S(9, [9], 1, 0, True, 2, 5, [9], 1, [], 4, 5),
       S(2, [2], 2, 1, True, 2, 4, [2], 3, [], 5, 6)]
sn1 = {2: {9: 2, 2: 2}}
r1 = M.recognize(as1, sn1)
out["T1_synth_AS"] = r1
assert r1["accepted"] and M.verify_cert(as1, r1), r1
ac = [p for p in r1["pieces"] if p["type"] == "AS-shared"]
assert len(ac) == 1 and ac[0]["kap"] == 1, r1
assert ac[0]["CW"] == 1, r1
cr = M.criticality(as1, sn1, ac[0])
out["T1_criticality"] = cr
# T2: W without dual push -> REJECT (no other cover)
as2 = [dict(b) for b in as1]
as2[3] = dict(as2[3]); as2[3]["push"] = [9]
r2 = M.recognize(as2, sn1)
out["T2_no_dualpush"] = r2
assert not r2["accepted"], r2
# T3: kappa=0 (both odd) -> REJECT
sn3 = {2: {9: 3, 2: 3}}
r3 = M.recognize(as1, sn3)
out["T3_kappa0"] = r3
assert not r3["accepted"], r3
# T4: R threshold fail (Ur=3 needs dA>=3; give dA=1... use dr0=4 variant)
as4 = [S(1, [1], 1, 3, True, 7, 9, [1], 2, [], 0, 1),
       S(5, [5], 1, 0, False, None, 5, [], 1, [], 1, 2),
       S(3, [3], 1, 3, True, 6, 2, [3], 2, [], 2, 3),
       S(4, [4], 1, 1, True, 2, 1, [4], 1, [9, 2], 3, 4),
       S(9, [9], 1, 0, True, 2, 5, [9], 1, [], 4, 5),
       S(2, [2], 2, 1, True, 2, 4, [2], 3, [], 5, 6)]
sn4 = {2: {9: 4, 2: 2}}
r4 = M.recognize(as4, sn4)
out["T4_R_threshold"] = r4
assert not (r4["accepted"] and any(
    p["type"] == "AS-shared" for p in r4["pieces"])), r4
# T5: rotation of T1 still ACCEPTS (t0acc is leg-index-based: same snaps)
r5 = M.recognize(as1[2:] + as1[:2], sn1)
out["T5_rotation"] = r5["accepted"]
assert r5["accepted"] and M.verify_cert(as1[2:] + as1[:2], r5), r5

def enrich(certpath):
    c = json.load(open(certpath))
    legs = c["legs"]; out, li = [], 0
    for b in c["blocks"]:
        b = dict(b)
        b["dA"] = legs[li]["dA"]
        b["push"] = []
        b["l0"] = li
        li += b.get("nleg", 1)
        b["l1"] = li
        out.append(b)
    return out
# T6/T7/T8: banked AP/AQ/AR preserved with same packet types
ap = enrich('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP/26AP_vine16_witness_certificate.json')
rp = M.recognize(ap, {})
out["T6_AP"] = rp["accepted"]
assert rp["accepted"] and M.verify_cert(ap, rp), rp
assert any(p["type"] == "AP-direct" and p["p"] == 3 for p in rp["pieces"]), rp
aq = enrich('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ/26AQ_vine16_witness_certificate.json')
rq = M.recognize(aq, {})
out["T7_AQ"] = rq["accepted"]
assert rq["accepted"] and M.verify_cert(aq, rq), rq
assert any(p["type"] == "AQ-bridge" for p in rq["pieces"]), rq
ar = enrich('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AR/26AR_vine16_closed_witness.json')
rr = M.recognize(ar, {})
out["T8_AR"] = rr["accepted"]
assert rr["accepted"] and M.verify_cert(ar, rr), rr
assert any(p["type"] == "AR-split" for p in rr["pieces"]), rr
# T9: verifier catches fabricated overlapping cert
fake = {"accepted": True,
        "pieces": [{"type": "AP-direct", "run": [0], "return": 1, "r": 9, "p": 1},
                   {"type": "AP-direct", "run": [1], "return": 2, "r": 8, "p": 1}],
        "singles": [], "cut": 0, "m": 3}
assert not M.verify_cert(as1[:3], fake)
out["T9_overlap"] = "verifier-rejects"
# T10: all-positive rejects
assert not M.recognize(
    [S(1, [1], 1, 3, True, 7, 9, [1], 2) for _ in range(4)], {})["accepted"]
out["T10_allpos"] = "reject"
json.dump(out, open(RDIR / '26AS_recognizer_selftests.json', 'w'), indent=1,
          default=str)
print("26AS recognizer self-tests: 10/10 PASS (AS accept, no-push/kappa/threshold rejects, rotation, AP/AQ/AR preserved, verifier, all-pos)")
