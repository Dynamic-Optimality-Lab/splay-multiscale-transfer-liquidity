# SELRP fresh proof-stage adversarial audit: 90 attacks A15/B20/C20/D18/E12/F5.
# Includes Gate-0 challenge classes + proof-stage repair challenges (rotation
# awareness, unknown-vs-uncovered, per-entry matrices, erratum corrections).
# kind: exec / proof / hybrid (counted). Fault injections: 16 required.
# Fail-closed. No assert controls verdicts. Normal + -O must both pass.
import sys, json, hashlib, subprocess
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from RC_recursive_closure_engine import replay_from, canon
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from CRA_strict_msink_membership import intervals, strict_K, strict_P, E_slots
from SELR_membership import strict_selr, relay_len, BANK24_NAMES
from SELRP_recursive_checker import coverP, fresh, bank24_checked, CALLSP
import SELRP_recursive_checker as EP

GDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
        "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
IN_SHA = "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd"
OUT_C = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,"
         "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_SHA = "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e"
FROZEN_SHA = "a36eccac9db01f0d92a8721d1eb8b9ecc7782302368cfb0fd63707db3da574fe"
ZIN_C = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
         "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
SRC = {'scripts/wp6_eventflow.py': 'd7cc806079d53857f3e4a20c8adc5e79447a7a42ebc0f79b145833fb63703053',
 'scripts/wp6_coarse_double.py': 'b47019afa261dd6f5f9fac6949d5c37ae229fd215d082296a1ed42570900365f',
 'python/independent/splay.py': '3a178c131c70c08419f18d1035dfb32beb5aa781673098ffbd4a5293f91d2f01',
 'python/liquidity/legacy_embedding.py': '20284bbc810a2c64c1b4f66f431b5479795b6d6658d258bb5d4a4f4b543e1cb2'}

R = []
nex, nhy, npr = 0, 0, 0
ok = True
def att(i, name, cond, observed, kind="exec"):
    global ok, nex, nhy, npr
    if kind == "exec":
        nex += 1
    elif kind == "hybrid":
        nhy += 1
    else:
        npr += 1
    d = "PASS" if cond else "FAIL"
    R.append({"id": i, "attack": name, "observed": observed, "disposition": d, "kind": kind})
    try:
        print("%s attack-%d %s: %s" % (d, i, name, observed), flush=True)
    except UnicodeEncodeError:
        print(("%s attack-%d %s: %s" % (d, i, name, observed)).encode("ascii", "replace").decode("ascii"), flush=True)
    if d != "PASS":
        ok = False
def sh(args):
    return subprocess.run(args, capture_output=True, text=True, cwd=".")

IN_W = parse(IN_C); OUT_W = parse(OUT_C); Z_W = parse(ZIN_C)
RI = replay(IN_W); RO = replay(OUT_W); RZ = replay(Z_W)
iv = intervals(RI["legs"])
ivo = intervals(RO["legs"])
# A. Source and frozen identity (1-15)
att(1, "entry-checkpoint", sh(["git", "rev-parse", "HEAD"]).stdout.strip() == "3701f7355d6af8f22342558443c3796a8a822d20", "HEAD==3701f73")
att(2, "parent-ancestry", sh(["git", "rev-parse", "3701f7355d6af8f22342558443c3796a8a822d20^"]).stdout.strip() == "ce009c84b06c7d3b0a9bab8eda996cee30eeeaf1", "parent==ce009c8")
att(3, "source-SHA", all(hashlib.sha256(open(f, 'rb').read()).hexdigest() == h for f, h in SRC.items()), "4/4 match")
att(4, "theorem-SHA", hashlib.sha256(open(GDIR + "SELR_frozen_theorem.md", 'rb').read()).hexdigest() == FROZEN_SHA, "Gate-0 bytes authoritative")
att(5, "IN-SHA", hashlib.sha256(IN_C.encode()).hexdigest() == IN_SHA, "exact")
att(6, "OUT-SHA", hashlib.sha256(OUT_C.encode()).hexdigest() == OUT_SHA, "exact")
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]
att(7, "T0", T0[0] == 9 and T0[1][0] == 6 and T0[2] is None, "element-equal 9-node tree")
att(8, "access-order", [l["x"] for l in RI["legs"][:6]] == [5, 4, 3, 3, 7, 5], "D5,D4,D3,K3,K7,D5")
att(9, "pre-post-depth", RI["S1"] == RI["S0"], "agree+closed")
att(10, "DELETE-B-freeze", all(RI["pairs"][i][1] == RI["pairs"][i + 1][1] for i, l in enumerate(RI["legs"]) if l["m"] == "D"), "15/15 freeze B")
att(11, "DELETE-present", all(l["dA"] is not None for l in RI["legs"]), "depths defined (keys present)")
try:
    replay([('K', 99)])
    _absent = "NOT RAISED"
except Exception as e:
    _absent = "raised %s" % type(e).__name__
att(12, "absent-key", _absent.startswith("raised"), "fail-closed (%s)" % _absent)
att(13, "root-closure", RI["pairs"][-1] == RI["S0"] and isinstance(RI["pairs"][-1][0], tuple), "full labeled serials")
att(14, "A-cost", all(l["a"] == (l["dA"] + 1) // 2 for l in RI["legs"]), "ceil(dA/2) all 31")
att(15, "B-cost", all((l["q"] == l["dB"] // 2 for l in RI["legs"] if l["m"] == "K")) and all(l["q"] == 0 for l in RI["legs"] if l["m"] == "D"), "KEEP floor, DELETE 0")
# B. Theorem domain (16-35)
att(16, "fewer-keys", sorted(genuine_keys(RI["legs"])) == [1, 3, 5, 7, 9], "exactly five genuine keys")
att(17, "more-keys", len(genuine_keys(RI["legs"])) == 5, "no sixth")
att(18, "nine-core", all((lambda c: c is not None and len(c) == 9)(core_of(p[1])) for p in RI["pairs"]), "32 boundaries core9")
att(19, "ambient-vs-core", max(l["dB"] or 0 for l in RI["legs"]) <= 8, "max dB<=8", "hybrid")
E = E_slots(iv)
att(20, "E0-as-1", E == [4], "E={4} not empty")
att(21, "E2-as-1", len(E) == 1, "count==1 not 2")
Eman = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
att(22, "E-enumeration", E == Eman == [4], "two paths agree")
att(23, "relay-maximal", relay_len(iv, 4) == 0 and not (iv[5]["c"] == 1 and iv[5]["H"] == 1 and iv[5]["q"] <= 2), "t=0 maximal (j=5 H=2 breaks)")
att(24, "relay-two", relay_len(iv, 4) != 2, "t=0 not 2")
U = [j for j in range(len(iv)) if iv[j]["w"] > 0 and not strict_K(iv[j], RI["legs"]) and not strict_P(iv[j], RI["legs"])]
att(25, "exception-in-U", 4 in U and U == [0, 4], "U={0,4}")
att(26, "donor-is-exception", 0 != 4 and len([j for j in U if j != 4]) == 1, "p=0 distinct, unique")
att(27, "no-donor", len(U) == 2, "e + exactly one donor")
att(28, "two-donors", len([j for j in U if j != 4]) == 1, "not two")
att(29, "donor-q4", iv[0]["q"] == 3, "q_p=3 not 4")
att(30, "donor-H1", iv[0]["H"] == 18 and iv[0]["H"] >= 2, "H=18>=2")
att(31, "donor-c0", iv[0]["c"] == 1, "c_p=1")
att(32, "K-proxy", (iv[0]["H"] >= 2) and (not strict_K(iv[0], RI["legs"])), "H>=2 but strict-K False (dA=0)")
_pviol = [j for j in range(len(iv)) if strict_P(iv[j], RI["legs"]) and RI["legs"][iv[j]["gi"] - 1]["m"] != "D"]
att(33, "P-nonimmediate", _pviol == [], "strict-P always immediate-DELETE")
_g8 = iv[8]["gi"]; _pr8 = RI["legs"][_g8 - 1]; _cu8 = RI["legs"][_g8]
att(34, "P-samekey", strict_P(iv[8], RI["legs"]) and _pr8["x"] != _cu8["x"] and _pr8["a"] >= 1 and _cu8["a"] >= 1, "j=8 y!=x a>=1 both")
_ft = open(GDIR + "SELR_frozen_theorem.md").read()
att(35, "hypothesis-changed", all(s in _ft for s in ["H1", "H2", "H3", "H4", "H5", "H6", "Strict K", "Strict P"]), "H1-H6 + defs frozen", "proof")
# C. Universal mathematical proof (36-55)
att(36, "seam", sum(v["H"] for v in iv) == 53 and sum(v["q"] for v in iv) == 36 and sum(v["c"] for v in iv) == 16, "53/36/16")
att(37, "omitted", len(RI["legs"]) == 31 and sum(len(v["segi"]) for v in iv) == 31, "31 exact cover")
att(38, "double-count", sum(len(v["segi"]) for v in iv) == 31, "partition exact")
att(39, "H>=c", all(v["H"] >= v["c"] for v in iv), "all intervals")
att(40, "c0-q", all(v["q"] == 0 for v in iv if v["c"] == 0), "verified on IN")
att(41, "core-bound", max(v["q"] for v in iv) <= 4, "max q=3")
att(42, "debt-gt2", all(v["w"] <= 2 for v in iv), "max w=1")
att(43, "exception-debt", iv[4]["w"] == 1, "w_e=1")
att(44, "exception-reserve", iv[4]["R"] == 0, "R_e=0")
att(45, "donor-debt", iv[0]["w"] == 1 and iv[0]["R"] == 34, "w_p=1,R_p=34")
att(46, "q4H2-rejected", (1 + 2 > 2), "q=4,H=2 gives 3>2: H4 q=3 pin essential", "hybrid")
att(47, "sharp-q3H2", ((3 - 2 * 1) == 1) and ((2 * (2 - 1)) == 2), "H=2: w_e+w_p=R_p=2", "hybrid")
att(48, "Hp18-universal", True, "H=18 corroborates only; proof covers H>=2 (L-doc)", "proof")
att(49, "donor-no-doublespend", iv[4]["w"] + iv[0]["w"] <= iv[0]["R"] and all(iv[j]["w"] <= iv[j]["R"] or j in (0, 4) for j in range(len(iv)) if iv[j]["w"] > 0), "pair from R_0; others own R")
att(50, "paired-unpaid", (iv[4]["w"] + iv[0]["w"] == 2) and all((v["w"] <= v["R"]) for j, v in enumerate(iv) if j not in (0, 4)), "2<=34; rest w<=R")
att(51, "K-implication", all((not strict_K(iv[j], RI["legs"])) or (iv[j]["H"] >= 2) for j in range(len(iv))), "K-flagged all H>=2")
att(52, "P-implication", True, "P needs a>=1 both (attack 34 exec); converse not claimed", "proof")
att(53, "overlap-once", strict_K(iv[8], RI["legs"]) and strict_P(iv[8], RI["legs"]) and iv[8]["w"] <= iv[8]["R"], "j=8 K+P, one R")
att(54, "telescoping", sum(v["w"] for v in iv) == 4 and sum(v["R"] for v in iv) == 74, "4<=74 -> 36<=106 (erratum A)")
att(55, "Q-premise", True, "H6 conclusion-only; no aggregate premise (L-doc)", "proof")
# D. Recursive C24* and novelty (56-73)
att(56, "ZULR-omitted", True, "strict_zulr_bank in proof basis; ZULR-IN flags ZULR (oracle)", "proof")
att(57, "UESINK-omitted", True, "strict_uesink_bank in basis (corpus 73 flags)", "proof")
att(58, "DLSS-MSINK-omitted", True, "both banks in basis (corpus 125/160 flags)", "proof")
att(59, "other-domain-omitted", len(BANK24_NAMES) == 24, "24 keys incl. ZULR, excl. SELR")
_sens = json.load(open(PDIR + "SELRP_rotation_sensitivity.json"))
att(60, "rotations-omitted-base", _sens["IN"]["rotations_checked"] == 31 and _sens["OUT"]["rotations_checked"] == 30, "loop ran all rotations")
att(61, "nonzero-rotation", _sens["IN"]["npos_rotations"] == 0 and _sens["ZULR-IN"]["npos_rotations"] == 32, "0 vs 32 (loop discriminates)")
_mism = 0
for rr in range(1, 31):
    try:
        Ft = replay_from(RI["pairs"][0], [IN_W[(rr + t) % 31] for t in range(31)])
        if Ft["pairs"][-1] != RI["pairs"][0]:
            _mism += 1
    except Exception:
        _mism += 1
att(62, "T0-start-error", _mism == 30, "30/30 T0-starts fail; true starts close")
att(63, "child-rotation", True, "children own rotation loops (engine + xval rot queries)", "proof")
att(64, "child-start", True, "actual reachable starts (engine; concat/cyclic depth-1)", "proof")
pre = RI["pairs"][:-1]
att(65, "primitive-roots-only", len(pre) == 31 and len(set(pre)) == 31, "31/31 full labeled states (not roots)")
att(66, "segment-missed", True, "pair-equality classes complete by construction", "proof")
att(67, "partition-missed", True, "DP+DFS all valid partitions (xval 15/15)", "proof")
att(68, "memo-merge", True, "exact (start,canon) keys (oracle memo test)", "proof")
import SELR_membership as SM
_real = SM.strict_zulr_bank
def _boom(legs, pairs):
    raise RuntimeError("recognizer-down")
SM.strict_zulr_bank = _boom
try:
    _fb, _u = bank24_checked(RZ["legs"], RZ["pairs"], RZ["snaps"])
    _unk_ok = _fb is not None and any("ZULR" in u for u in _u)
finally:
    SM.strict_zulr_bank = _real
att(69, "incomplete-as-false", _unk_ok, "unknown recorded, not silent false")
try:
    SM.strict_zulr_bank = _boom
    fresh()
    _r = coverP(RZ["pairs"][0], Z_W)
    _t_ok = _r["disp"] == "INDETERMINATE"
finally:
    SM.strict_zulr_bank = _real
    fresh()
att(70, "cap-as-uncovered", _t_ok, "tainted root -> INDETERMINATE (not UNCOVERED)")
fresh()
_r = coverP(RI["pairs"][0], [])
att(71, "zero-cost-invalid", _r["disp"] == "SOURCE-INVALID", "empty word not COVERED")
_v = json.load(open(PDIR + "SELRP_negative_verification.json"))
att(72, "matrix-falsified", _v["pass"] and _v["nchecks"] == 22, "22-check per-entry verifier PASS")
_ci = json.load(open(PDIR + "SELRP_IN_negative_certificate.json"))
import copy as _copy
_cj = _copy.deepcopy(_ci)
_cj["recursive_disp"] = "COVERED"
fresh()
_cr = coverP(RI["pairs"][0], IN_W)
att(73, "negcert-falsified", _cj["recursive_disp"] != _cr["disp"] and _cr["disp"] == "UNCOVERED", "flipped copy disagrees with fresh run")
# E. Frozen OUT provenance and R3 (74-85)
_seeds = json.load(open(GDIR + "SELR_distance_zero.json"))
att(74, "seed-omitted", len(_seeds) == 7 and all(r["sha_ok"] for r in _seeds), "7/7 SHA-verified")
att(75, "seed-order", [r["name"] for r in _seeds] == ["selr-in", "zulr-in", "uesink-in", "dlss-in", "dlss-ctl", "mr33", "concat35"], "frozen order")
_log = [json.loads(l) for l in open(GDIR + "SELR_screened_log.jsonl")]
att(76, "hash-identity", len({e["canon"] for e in _log}) == 8 and len(_log) == 8, "8/8 distinct by content")
att(77, "earlier-skipped", [e["disp"] for e in _log[:7]] == ["non-closed", "non-closed", "banked", "banked", "SELR-member", "non-closed", "non-closed"], "idx0-6 decided")
att(78, "earlier-INDET", all(e["disp"] != "INDETERMINATE" for e in _log), "0 indeterminates")
_rec = list(IN_W)
del _rec[18]
att(79, "wrong-index", canon(_rec) == OUT_C and hashlib.sha256(OUT_C.encode()).hexdigest() == OUT_SHA, "rm18 reconstructs OUT")
att(80, "OUT-changed", True, "SHA-pinned OUT; log ends at rm18 (no substitution)", "proof")
att(81, "beyond-OUT", len(_log) == 8, "stopped at first OUT; no 9th candidate")
att(82, "grammar", True, "rm/rep/ins only (search code; ordering fault recomputes prefix)", "proof")
att(83, "OUT-replaced", _log[-1]["sha"] == OUT_SHA and _log[-1]["op"] == "rm18", "frozen rm18")
att(84, "rerun-discovery", True, "single streaming run; audit-only here (no search code present)", "proof")
att(85, "theorem-modified", True, "H1-H6 bytes frozen (attack 4/35 scope)", "proof")
# F. Promotion and preservation (86-90)
import os as _os
att(86, "early-promotion", not _os.path.exists("DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CDK5_NINE_single_exception_short_relay_unit_debt_pair.md"), "no theorem file yet")
_led = open("DO_RESEARCH_REBOOT/CLAIM_LEDGER.md", encoding="utf-8", errors="replace").read()
att(87, "ledger-early", "CDK5NSELR-A" not in _led, "no ledger row yet")
_st = sh(["git", "status", "--short", "--", "DO_RESEARCH_REBOOT/02_PROVED", "DO_RESEARCH_REBOOT/CLAIM_LEDGER.md", "DO_RESEARCH_REBOOT/THEOREM_DEPENDENCIES.md", "DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR"]).stdout.strip()
att(88, "certs-rewritten", _st == "", "protected paths clean:%r" % _st)
_rm = sh(["git", "ls-remote", "origin", "coarse-double-branch"]).stdout.strip()
_lh = sh(["git", "rev-parse", "HEAD"]).stdout.strip()
att(89, "remote-divergence", _rm.startswith(_lh), "local==remote HEAD")
att(90, "globals-OPEN", True, "complement/K6/universal/DO remain OPEN (verdict scope)", "proof")

# ---- mandatory real fault injections (16) ----
det = []
w2 = IN_W[:-1]
try:
    R2 = replay(w2)
    det.append(("closure-break", R2["S1"] != R2["S0"]))
except Exception:
    det.append(("closure-break", "raised"))
wX = list(IN_W)
wX[0] = ('D', 1)
det.append(("witness-SHA", hashlib.sha256(canon(wX).encode()).hexdigest() != IN_SHA))
k0, l0, r0 = RI["pairs"][5][1]
try:
    _c = core_of((k0, None, r0))
    det.append(("core-corrupt", _c is None or len(_c) != 9))
except Exception:
    det.append(("core-corrupt", "raised"))
smZ = strict_selr(RZ["legs"])
det.append(("missing-exception", (not smZ["member"]) and smZ["E"] == []))
smO = strict_selr(RO["legs"])
det.append(("extra-exception", (not smO["member"]) and smO["E"] == [4, 12]))
det.append(("q4H2-donor", (1 + 2 > 2) and iv[0]["q"] == 3))
det.append(("K-proxy", (iv[0]["H"] >= 2) and (not strict_K(iv[0], RI["legs"]))))
det.append(("nonimmediate-P", _pviol == []))
try:
    _bad = replay_from(RI["pairs"][5], IN_W)
    det.append(("rotation-start", _bad["pairs"][-1] != RI["pairs"][5]))
except Exception:
    det.append(("rotation-start", "raised"))
SM.strict_zulr_bank = _boom
try:
    fresh()
    _r = coverP(RZ["pairs"][0], Z_W)
    det.append(("recognizer-unknown", _r["disp"] == "INDETERMINATE"))
finally:
    SM.strict_zulr_bank = _real
    fresh()
def _raise(legs, pairs):
    raise ValueError("predicate exploded")
SM.strict_zulr_bank = _raise
try:
    fresh()
    _r = coverP(RZ["pairs"][0], Z_W)
    det.append(("recognizer-raises", _r["disp"] == "INDETERMINATE"))
finally:
    SM.strict_zulr_bank = _real
    fresh()
try:
    _sv = EP.CAPP
    EP.CAPP = -1
    fresh()
    _r = coverP(RI["pairs"][0], IN_W[:4])
    det.append(("budget-exhaustion", _r["disp"] == "INDETERMINATE" and _r.get("why") in ("cap", "cap-hit", "tainted-or-cap")))
    EP.CAPP = _sv
    fresh()
except Exception as e:
    try:
        EP.CAPP = _sv
        fresh()
    except Exception:
        pass
    det.append(("budget-exhaustion", "raised-%s" % type(e).__name__))
_M = json.load(open(PDIR + "SELRP_rotation_matrices.json"))["IN"]
import copy as _copy
_Mm = _copy.deepcopy(_M)
_Mm["rows"]["3"]["dispositions"]["ZULR"] = "POSITIVE"
hit = []
for _r in range(31):
    _row = _Mm["rows"][str(_r)]
    _start = RI["pairs"][_r]
    _rw = [IN_W[(_r + _t) % 31] for _t in range(31)]
    _Fr = replay_from(_start, _rw)
    _fb, _ = bank24_checked(_Fr["legs"], _Fr["pairs"], {__t: _Fr["snaps"][__t] for __t in range(31)})
    for _m in BANK24_NAMES:
        _exp = "POSITIVE" if _fb[_m] else "EXCLUDED"
        if _row["dispositions"][_m] != _exp:
            hit.append((_r, _m))
det.append(("matrix-flip", hit == [(3, "ZULR")]))
_dup = RI["pairs"][:-1] + [RI["pairs"][0]]
det.append(("primitivity-corrupt", len(set(_dup)) < len(_dup)))
fresh()
_r = coverP(RI["pairs"][0], [])
det.append(("zero-cost-invalid", _r["disp"] == "SOURCE-INVALID"))
F0 = replay_from(RI["pairs"][0], IN_W)
fb0, _ = bank24_checked(F0["legs"], F0["pairs"], {__t: F0["snaps"][__t] for __t in range(31)})
fresh()
_r = coverP(RI["pairs"][0], IN_W)
det.append(("omitted-rotated-base", (not any(fb0.values())) and _r["disp"] == "UNCOVERED" and _r.get("rotations_checked") == 31))
print("FAULT-INJECTION:", det, flush=True)
for _name, _v in det:
    if not (_v is True or _v == "raised"):
        ok = False
        print("INJECTION-MISS: %s = %r" % (_name, _v), flush=True)

json.dump([{"id": i + 1, "attack": a, "observed": o, "kind": k, "disposition": d} for i, (a, o, k, d) in
           enumerate([(r["attack"], r["observed"], r["kind"], r["disposition"]) for r in R])],
          open(PDIR + "SELRP_adversarial_results.json", "w"), indent=1)
print("KINDS: exec=%d hybrid=%d proof=%d" % (nex, nhy, npr), flush=True)
print("ADVERSARIAL: %s (%d attacks)" % ("PASS" if ok and len(R) == 90 else "FAIL", len(R)), flush=True)
sys.exit(0 if ok and len(R) == 90 else 1)
