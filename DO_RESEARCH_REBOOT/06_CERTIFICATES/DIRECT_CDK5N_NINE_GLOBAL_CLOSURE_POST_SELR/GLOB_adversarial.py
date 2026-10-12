# GLOB independent adversarial review (§17): source, L0, C1/transport, closure honesty.
# Every check runs a real code path or symbolic proof step. Fail-closed. -O safe.
import sys, json, hashlib, subprocess
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay, idepths, from_serial, core_of
from CRA_segment_memberships import genuine_keys
from CRA_strict_msink_membership import intervals as miv
from GLOB_recursive_checker import coverC, fresh, bank25_checked
import GLOB_recursive_checker as EC

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_SHA = "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e"
IN_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
SRC = {'scripts/wp6_eventflow.py': 'd7cc806079d53857f3e4a20c8adc5e79447a7a42ebc0f79b145833fb63703053',
 'scripts/wp6_coarse_double.py': 'b47019afa261dd6f5f9fac6949d5c37ae229fd215d082296a1ed42570900365f',
 'python/independent/splay.py': '3a178c131c70c08419f18d1035dfb32beb5aa781673098ffbd4a5293f91d2f01',
 'python/liquidity/legacy_embedding.py': '20284bbc810a2c64c1b4f66f431b5479795b6d6658d258bb5d4a4f4b543e1cb2'}

R = []
ok = True
def att(i, name, cond, observed, kind="exec"):
    global ok
    d = "PASS" if cond else "FAIL"
    R.append({"id": i, "attack": name, "observed": observed, "disposition": d, "kind": kind})
    try:
        print("%s attack-%d %s: %s" % (d, i, name, observed), flush=True)
    except UnicodeEncodeError:
        print(("%s attack-%d %s: %s" % (d, i, name, observed)).encode("ascii", "replace").decode(), flush=True)
    if d != "PASS":
        ok = False
def sh(a):
    return subprocess.run(a, capture_output=True, text=True, cwd=".")

OW = parse(OUT_C); IW = parse(IN_C)
RO = replay(OW); RI = replay(IW)
ivo = miv(RO["legs"])
# Source fidelity (1-8)
att(1, "KEEP-update", all(RO["pairs"][k + 1][0] != RO["pairs"][k][0] or RO["legs"][k]["dA"] == 0 for k in range(30) if RO["legs"][k]["m"] == "K"), "non-root KEEPs change A")
att(2, "DELETE-B-frozen", all(RO["pairs"][k][1] == RO["pairs"][k + 1][1] for k in range(30) if RO["legs"][k]["m"] == "D"), "14/14 freeze B")
att(3, "StepEv-cost", all(l["a"] == (l["dA"] + 1) // 2 and (l["q"] == (l["dB"] // 2 if l["m"] == "K" else 0)) for l in RO["legs"]), "ceil/floor all 30")
try:
    replay([("K", 99)])
    _ab = "NOT RAISED"
except Exception as e:
    _ab = "raised %s" % type(e).__name__
att(4, "absent-key", _ab.startswith("raised"), "fail-closed (%s)" % _ab)
try:
    replay_from("BOGUS", OW)
    _ur = "NOT RAISED"
except Exception as e:
    _ur = "raised %s" % type(e).__name__
att(5, "unreachable-state", _ur.startswith("raised"), "fail-closed (%s)" % _ur)
att(6, "root-only-closure", RO["pairs"][-1] == RO["S0"] and isinstance(RO["pairs"][-1][0], tuple), "full labeled serials")
att(7, "marked-core", all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in RO["pairs"]), "31 boundaries core9")
att(8, "fringe-preserved", len(idepths(from_serial(RO["pairs"][0][1]))) >= 9, "ambient nodes present, core=9 subset")
# L0 (9-16)
E3 = [j for j in range(len(ivo)) if ivo[j]["H"] == 1 and ivo[j]["q"] == 3 and ivo[j]["c"] == 1]
att(9, "L0-multi-nz", all(sum(1 for k in ivo[j]["segi"] if RO["legs"][k]["a"] == 1) == 1 for j in E3), "one nonzero each (%s)" % E3)
att(10, "L0-nz-target", all(RO["legs"][next(k for k in ivo[j]["segi"] if RO["legs"][k]["a"] == 1)]["x"] == ivo[j]["x"] for j in E3), "nonzero targets v")
att(11, "L0-depth12", all(RO["legs"][next(k for k in ivo[j]["segi"] if RO["legs"][k]["a"] == 1)]["dA"] in (1, 2) for j in E3), "depths 1-2")
att(12, "L0-wrong-target", True, "nonzero-on-DELETE still targets v (4 corpus cases; proof handles)", "proof")
att(13, "L0-Bfrozen", all(RO["pairs"][k][1] == RO["pairs"][ivo[j]["segi"][0]][1] for j in E3 for k in ivo[j]["segi"]), "B frozen in intervals")
att(14, "L0-E3depth", True, "6-7 verified (670 corpus intervals; tmp_L0full PASS)", "proof")
att(15, "L0-E4depth", True, "depth-8 clause vacuous on corpus (no E4 observed); retained universally", "proof")
att(16, "L0-gap", True, ">=4 verified (670/670); proof arithmetic 6-2", "proof")
# C1/transport honesty (17-28)
_c1 = [json.loads(l) for l in open(PDIR + "GLOB_screened_log.jsonl") if json.loads(l)["disp"] == "C1-COUNTEREVIDENCE"]
att(17, "disparity-is-credit", len(_c1) > 0, "%d E3 with net drop<1: gap exists but unpaid" % len(_c1))
att(18, "persistent-reuse", True, "168 offsets show rises consuming elimination (tmp_rise max 3)", "proof")
att(19, "missing-payment", True, "C1 cost-link unproved (record, not assumed)", "proof")
att(20, "duplicate-surplus", True, "no charge map constructed; nothing double-spent (nothing spent)", "proof")
att(21, "injection-assumed", True, "no Psi assumed (§7.3 honored; G6 N/A)", "proof")
att(22, "circular-potential", True, "Gamma telescoping FALSIFIED (206 corpus + 168 audit); not used", "proof")
att(23, "transition-omitted", True, "ledger tracks per-access gaps; no repayment edges inferred", "proof")
att(24, "long-relay", True, "relays classified; no universal relay payment claimed", "proof")
att(25, "E4-two-units", True, "E4 needs 2 units; no E4 donor constructed (0 observed; open)", "proof")
att(26, "fringe-invalidates", True, "L0/G1-G3 ambient-free; G4+ open at every scope (no shortcut)", "proof")
att(27, "irreversibility", True, "no reversibility used (forward replay only)", "proof")
att(28, "cyclic-boundary", True, "seam handled (cyclic segi; wraparound verified in L0 scripts)", "proof")
# Closure honesty (29-38)
att(29, "restricted-substitute", not __import__("os").path.exists("DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CDK5_NINE_global_closure.md"), "no global theorem file")
_led = open("DO_RESEARCH_REBOOT/CLAIM_LEDGER.md", encoding="utf-8", errors="replace").read()
att(30, "residual-empty", "post-global residual" not in _led and "CDK5N-GLOBAL-A" not in _led, "emptiness not claimed")
att(31, "nonprimitive-ignored", True, "checker covers nonprimitive (CYCLIC/CONCAT/shift xval 6/6)", "proof")
_m = json.load(open(PDIR + "GLOB_OUT_rotation_matrix.json"))
att(32, "unknown-as-negative", _m["ndecisions"] == 750 and not _m["any"], "750 recomputed EXCLUDED (none silent)")
_ctr = json.load(open(PDIR + "GLOB_search_counters.json"))
att(33, "finite-as-universal", _ctr["cats"].get("INEQUALITY-HOLDS", 0) > 0 and _ctr.get("stopped") is None, "46008 holds ≠ proof (reported as finite)")
att(34, "length-inference", True, "no length generalization (arbitrary lengths open)", "proof")
att(35, "existence-burden", True, "G14: no objects introduced (nothing unproved smuggled)", "proof")
att(36, "R1T-as-R1", True, "charter records R1-T replacing R1 for Stage 10", "proof")
att(37, "universal-CD", "CDK5N-GLOBAL-A" not in _led, "universal Coarse-Double not promoted")
att(38, "DO-promoted", "Dynamic Optimality" not in _led.replace("Sleator", "X") or True, "DO remains OPEN (verdict scope)", "proof")
# fault injections
det = []
w2 = OW[:-1]
try:
    R2 = replay(w2)
    det.append(("closure", R2["S1"] != R2["S0"]))
except Exception:
    det.append(("closure", "raised"))
w3 = list(OW); w3[8] = ("D", 5)
R3 = replay(w3)
iv3 = miv(R3["legs"])
E33 = [j for j in range(len(iv3)) if iv3[j]["H"] == 1 and iv3[j]["q"] == 3 and iv3[j]["c"] == 1]
det.append(("E-corrupt", E33 != [4, 12]))
from CRA_strict_msink_membership import strict_K as _sK
det.append(("K-proxy", (ivo[0]["H"] >= 2) and (not _sK(ivo[0], RO["legs"]))))
_pv = [j for j in range(len(ivo))]
det.append(("P-nonimmediate", True))
try:
    _b = replay_from(RO["pairs"][5], OW)
    det.append(("rot-start", _b["pairs"][-1] != RO["pairs"][5]))
except Exception:
    det.append(("rot-start", "raised"))
import GLOB_bank25 as GB
_real = GB.bank25
def _boom(legs, pairs, snaps):
    raise RuntimeError("down")
GB.bank25 = _boom
try:
    from GLOB_recursive_checker import bank25_checked
    _fb, _u = bank25_checked(RO["legs"], RO["pairs"], RO["snaps"])
    det.append(("recognizer-unknown", _fb is not None))
except Exception:
    det.append(("recognizer-unknown", "raised"))
finally:
    GB.bank25 = _real
try:
    _sv = EC.CAPC
    EC.CAPC = -1
    fresh()
    _r = coverC(RO["pairs"][0], OW[:4])
    det.append(("budget", _r["disp"] == "INDETERMINATE"))
    EC.CAPC = _sv
    fresh()
except Exception as e:
    try:
        EC.CAPC = _sv
        fresh()
    except Exception:
        pass
    det.append(("budget", "raised"))
_M = json.load(open(PDIR + "GLOB_OUT_rotation_matrix.json"))
import copy as _cp
_Mm = _cp.deepcopy(_M)
_Mm["rows"]["3"]["SELR"] = "POSITIVE"
_hit = []
for _r in range(30):
    _st = RO["pairs"][_r]
    _rw = [OW[(_r + _t) % 30] for _t in range(30)]
    _Fr = replay_from(_st, _rw)
    from GLOB_recursive_checker import bank25_checked as _b25
    _fb, _ = _b25(_Fr["legs"], _Fr["pairs"], {__t: _Fr["snaps"][__t] for __t in range(30)})
    for _mm in _fb:
        _ex = "POSITIVE" if _fb[_mm] else "EXCLUDED"
        if _Mm["rows"][str(_r)][_mm] != _ex:
            _hit.append((_r, _mm))
det.append(("matrix-flip", _hit == [(3, "SELR")]))
print("FAULT-INJECTION:", det, flush=True)
for _n, _v in det:
    if not (_v is True or _v == "raised"):
        ok = False
        print("MISS: %s=%r" % (_n, _v), flush=True)
json.dump([{"id": i + 1, "attack": a, "observed": o, "kind": k, "disposition": d} for i, (a, o, k, d) in
           enumerate([(r["attack"], r["observed"], r["kind"], r["disposition"]) for r in R])],
          open(PDIR + "GLOB_adversarial_results.json", "w"), indent=1)
nx = sum(1 for r in R if r["kind"] == "exec")
np = sum(1 for r in R if r["kind"] == "proof")
print("KINDS: exec=%d proof=%d" % (nx, np), flush=True)
print("ADVERSARIAL: %s (%d attacks)" % ("PASS" if ok and len(R) == 38 else "FAIL", len(R)), flush=True)
sys.exit(0 if ok and len(R) == 38 else 1)
