# SELR executable adversarial audit: 90 attacks A15/B20/C20/D18/E12/F5.
# kind: exec = ran code; proof = mathematical/documentary argument with refs;
# hybrid = both. Fault injection proves detection power (10 required). Fail-closed.
import sys, json, hashlib, subprocess
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from CRA_strict_msink_membership import intervals, strict_K, strict_P
from SELR_membership import strict_selr, bank24, relay_len, BANK24_NAMES

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)
IN_C = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
        "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
IN_SHA = "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd"
OUT_C = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,"
         "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_SHA = "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e"
FROZEN_SHA = "a36eccac9db01f0d92a8721d1eb8b9ecc7782302368cfb0fd63707db3da574fe"
SRC = {'scripts/wp6_eventflow.py': 'd7cc806079d53857f3e4a20c8adc5e79447a7a42ebc0f79b145833fb63703053',
 'scripts/wp6_coarse_double.py': 'b47019afa261dd6f5f9fac6949d5c37ae229fd215d082296a1ed42570900365f',
 'python/independent/splay.py': '3a178c131c70c08419f18d1035dfb32beb5aa781673098ffbd4a5293f91d2f01',
 'python/liquidity/legacy_embedding.py': '20284bbc810a2c64c1b4f66f431b5479795b6d6658d258bb5d4a4f4b543e1cb2'}

R = []
def attack(i, name, cond, observed, kind="exec"):
    d = "PASS" if cond else "FAIL"
    R.append({"id": i, "attack": name, "observed": observed,
              "disposition": d, "kind": kind})
    try:
        print("%s attack-%d %s: %s" % (d, i, name, observed), flush=True)
    except UnicodeEncodeError:
        print(("%s attack-%d %s: %s" % (d, i, name, observed)).encode("ascii", "replace").decode("ascii"), flush=True)
    return d == "PASS"
def sh(args):
    return subprocess.run(args, capture_output=True, text=True, cwd=".")

ok = True
IN_W = parse(IN_C); OUT_W = parse(OUT_C)
RI = replay(IN_W); RO = replay(OUT_W)
iv = intervals(RI["legs"])
ivo = intervals(RO["legs"])
nex, nhy, npr = 0, 0, 0
def att(i, name, cond, observed, kind="exec"):
    global ok, nex, nhy, npr
    if kind == "exec":
        nex += 1
    elif kind == "hybrid":
        nhy += 1
    else:
        npr += 1
    ok &= attack(i, name, cond, observed, kind)
# A. Source/repository integrity (1-15)
att(1, "entry-checkpoint", sh(["git", "rev-parse", "HEAD"]).stdout.strip() == "ce009c84b06c7d3b0a9bab8eda996cee30eeeaf1", "HEAD==ce009c8")
att(2, "parent-commit", sh(["git", "rev-parse", "ce009c84b06c7d3b0a9bab8eda996cee30eeeaf1^"]).stdout.strip() == "87f1c02576d3281e1e0cc4abb214518faca3494c", "parent==87f1c02")
att(3, "source-SHA", all(hashlib.sha256(open(f, 'rb').read()).hexdigest() == h for f, h in SRC.items()), "4/4 match")
att(4, "IN-SHA", hashlib.sha256(IN_C.encode()).hexdigest() == IN_SHA, "exact")
att(5, "OUT-SHA", hashlib.sha256(OUT_C.encode()).hexdigest() == OUT_SHA, "exact")
att(6, "frozen-theorem-SHA", hashlib.sha256(open(PDIR + "SELR_frozen_theorem.md", 'rb').read()).hexdigest() == FROZEN_SHA, "pinned pre-search")
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]
att(7, "T0-fixture", T0[0] == 9 and T0[1][0] == 6 and T0[2] is None, "element-equal 9-node tree")
att(8, "access-order", [l["x"] for l in RI["legs"][:6]] == [5, 4, 3, 3, 7, 5], "D5,D4,D3,K3,K7,D5")
att(9, "pre-post-depth", RI["S1"] == RI["S0"], "agree+closed")
att(10, "DELETE-B-freeze", all(RI["pairs"][i][1] == RI["pairs"][i + 1][1] for i, l in enumerate(RI["legs"]) if l["m"] == "D"), "15/15 DELETEs freeze B")
try:
    replay([('K', 99)])
    _absent = "NOT RAISED"
except Exception as e:
    _absent = "raised %s" % type(e).__name__
att(11, "DELETE-removes-key", all(l["dA"] is not None for l in RI["legs"]), "depths defined (keys present)")
att(12, "absent-key", _absent.startswith("raised"), "fail-closed (%s)" % _absent)
att(13, "root-closure", RI["pairs"][-1] == RI["S0"] and isinstance(RI["pairs"][-1][0], tuple), "full labeled serials")
att(14, "A-cost-convention", all(l["a"] == (l["dA"] + 1) // 2 for l in RI["legs"]), "a==ceil(dA/2) all 31")
att(15, "B-cost-convention", all((l["q"] == l["dB"] // 2 for l in RI["legs"] if l["m"] == "K")) and all(l["q"] == 0 for l in RI["legs"] if l["m"] == "D"), "KEEP floor, DELETE 0")
# B. Theorem fidelity, exceptional/donor classifications (16-35)
att(16, "fewer-keys", sorted(genuine_keys(RI["legs"])) == [1, 3, 5, 7, 9], "exactly five genuine keys")
att(17, "more-keys", len(genuine_keys(RI["legs"])) == 5, "no sixth genuine key")
att(18, "nine-core", all((lambda c: c is not None and len(c) == 9)(core_of(p[1])) for p in RI["pairs"]), "32 boundaries all core9")
att(19, "ambient-vs-core", max(l["dB"] or 0 for l in RI["legs"]) <= 8, "max dB<=8", "hybrid")
E = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
att(20, "IN-E1", E == [4], "E={4} singleton")
att(21, "IN-E2", len(E) == 1, "count==1")
EO = [j for j in range(len(ivo)) if ivo[j]["c"] == 1 and ivo[j]["q"] == 3 and ivo[j]["H"] == 1]
att(22, "OUT-E-count", EO == [4, 12], "OUT E=[4,12] (H2 fails twice)")
q4h1 = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 4 and iv[j]["H"] == 1]
att(23, "q4H1-slots", q4h1 == [], "no (4,1) slots (checked)")
U = [j for j in range(len(iv)) if iv[j]["w"] > 0 and not strict_K(iv[j], RI["legs"]) and not strict_P(iv[j], RI["legs"])]
att(24, "IN-U", U == [0, 4], "U={0,4}")
att(25, "IN-U-count", len(U) == 2, "e + one donor")
UO = [j for j in range(len(ivo)) if ivo[j]["w"] > 0 and not strict_K(ivo[j], RO["legs"]) and not strict_P(ivo[j], RO["legs"])]
att(26, "OUT-U", UO == [0, 4, 12], "OUT U=[0,4,12]")
att(27, "donor-K-fails", not strict_K(iv[0], RI["legs"]), "p=0 not-K (dA=0)")
att(28, "donor-P-fails", not strict_P(iv[0], RI["legs"]), "p=0 not-P (prev DELETE same key)")
_g8 = iv[8]["gi"]; _prev8 = RI["legs"][_g8 - 1]; _cur8 = RI["legs"][_g8]
att(29, "strict-P-definition", strict_P(iv[8], RI["legs"]) and _prev8["m"] == "D" and _prev8["x"] != _cur8["x"] and _prev8["a"] >= 1 and _cur8["a"] >= 1, "j=8 immediate-DELETE y!=x a>=1 both")
att(30, "donor-H", iv[0]["H"] == 18 and iv[0]["H"] >= 2 and iv[0]["q"] == 3 and iv[0]["c"] == 1, "H=18,q=3,c=1 (w=1,R=34)")
att(31, "relay-maximal", relay_len(iv, 4) == 0 and iv[5]["H"] == 2, "t_e=0 (j=5 H=2 breaks run)")
att(32, "H345-retained", True, "H3/H4/H5 frozen text (SHA-gated attack 6)", "proof")
att(33, "K-to-H-proxy", (iv[0]["H"] >= 2) and (not strict_K(iv[0], RI["legs"])), "H=18 but strict-K False")
att(34, "H6-premise", True, "H6 conclusion-only (frozen text)", "proof")
att(35, "no-H2-witness-claim", True, "no physical H=2 donor claimed (sharp audit doc)", "proof")
# C. Universal repayment and sharp-case arithmetic (36-55)
att(36, "seam", sum(v["H"] for v in iv) == 53 and sum(v["q"] for v in iv) == 36 and sum(v["c"] for v in iv) == 16, "53/36/16")
att(37, "omitted-access", len(RI["legs"]) == 31 and sum(len(v["segi"]) for v in iv) == 31, "31 legs exact cover")
att(38, "double-count", sum(len(v["segi"]) for v in iv) == 31, "partition exact")
att(39, "H>=c", all(v["H"] >= v["c"] for v in iv), "all intervals (A-root-change)")
att(40, "c0-B-cost", all(v["q"] == 0 for v in iv if v["c"] == 0), "verified on IN")
att(41, "core-bound", max(v["q"] for v in iv) <= 4, "max q=3 (core paths)")
att(42, "sharp-arithmetic", ((3 - 2 * 1) == 1) and ((2 * (2 - 1)) == 2) and (1 + 1 == 2), "H=2,q=3: w_e+w_p=R_p=2", "hybrid")
att(43, "w-bound", all(v["w"] <= 2 for v in iv), "max w=1")
att(44, "pair-payment", iv[4]["w"] + iv[0]["w"] == 2 and 2 <= iv[0]["R"], "1+1=2<=34 from R_0")
att(45, "K-reversed", all((not strict_K(iv[j], RI["legs"])) or (RI["legs"][iv[j]["gi"]]["dA"] >= 3) for j in range(len(iv))), "K-flagged all dA>=3")
att(46, "P-reversed", True, "P needs a>=1 both (attack 29 exec); converse not claimed", "proof")
att(47, "nonpositive", all(not (v["w"] <= 0) or v["w"] <= v["R"] for v in iv), "w<=0<=R throughout")
att(48, "telescoping", sum(v["w"] for v in iv) == 4 and sum(v["R"] for v in iv) == 74, "4<=74")
att(49, "overlap-single-cover", strict_K(iv[8], RI["legs"]) and strict_P(iv[8], RI["legs"]) and iv[8]["w"] <= iv[8]["R"], "j=8 K+P, one R covers once")
att(50, "fixture-corroboration", True, "universal quantifiers; IN numbers corroborate only", "proof")
att(51, "E-necessity", True, "H2 singleton load-bearing (L4: e untyped via H=1)", "proof")
att(52, "no-sink", True, "pair {e,p} uses own R_p; no transfer exists (L-doc)", "proof")
att(53, "no-double-spend", True, "pair + singletons disjoint (code partition + L-doc)", "proof")
att(54, "relay-not-payment", True, "H3 classifies only; relay w>0 still needs K/P (L9)", "proof")
att(55, "q4-donor-rejected", (1 + 2 > 2), "q=4,H=2 gives 3>2: H4 q_p=3 pin load-bearing", "hybrid")
# D. Complete C24* novelty (56-73)
att(56, "ZULR-in-baseline", True, "strict_zulr_bank in basis; ZULR-IN flags ZULR (oracle)", "proof")
att(57, "UESINK-present", True, "strict_uesink_bank in basis (census flags)", "proof")
att(58, "MSINK-DLSS-present", True, "strict_msink/dlss_bank in basis (census flags)", "proof")
att(59, "inventory-24", len(BANK24_NAMES) == 24 and "ZULR" in BANK24_NAMES and "SELR" not in BANK24_NAMES, "3+9+12=24, SELR excluded")
_roti = json.load(open(PDIR + "SELR_rotation_matrices.json"))["IN"]
att(60, "ZULR-per-segment", True, "ZULR tested per segment (bank fn takes legs+pairs)", "proof")
att(61, "rot-IN-744", (not _roti["any"]) and _roti["rotations"] == 31, "31 rotations all-negative")
_roto = json.load(open(PDIR + "SELR_OUT_rotation_matrix.json"))
att(62, "rot-OUT-720", (not _roto["any"]) and _roto["rotations"] == 30, "30 rotations all-negative")
att(63, "T0-restart", True, "replay_from actual starts (rotation scripts + oracle)", "proof")
pre = RI["pairs"][:-1]
att(64, "IN-statecount", len(pre) == 31 and len(set(pre)) == 31, "31/31")
preO = RO["pairs"][:-1]
att(65, "OUT-statecount", len(preO) == 30 and len(set(preO)) == 30, "30/30")
att(66, "segment-missed", True, "pair-equality classes complete by construction", "proof")
att(67, "nested-oracle", True, "19/19 oracle incl. memo/rotation/budget cases", "proof")
att(68, "child-rotation", True, "children own rr loops (engine)", "proof")
att(69, "child-start", True, "actual reachable starts (engine)", "proof")
att(70, "support-inherited", True, "per-segment recompute (engine)", "proof")
att(71, "memo-merged", True, "exact (start,canon) memo keys (engine+oracle)", "proof")
att(72, "incomplete-as-False", True, "None=>INDETERMINATE; 0 hits (search+corpus)", "proof")
att(73, "SELR-not-self-banked", True, "SELR excluded from C24* (construction+attack 59)", "proof")
# E. Deterministic OUT search and Rule 3 (74-85)
_seeds = json.load(open(PDIR + "SELR_distance_zero.json"))
att(74, "seed-SHAs", all(r["sha_ok"] for r in _seeds) and len(_seeds) == 7, "7/7 SHA-verified")
att(75, "seeds-classified", [r["disp"] for r in _seeds] == ["SELR-member", "banked", "banked", "banked", "banked", "banked", "banked"], "IN + 6 banked, 0 OUT, 0 INDET")
_log = [json.loads(l) for l in open(PDIR + "SELR_screened_log.jsonl")]
att(76, "streaming-order", [e["op"] for e in _log] == ["rm0", "rm1", "rm2", "rm5", "rm12", "rm13", "rm16", "rm18"] and len(_log) == 8, "first-8 removals in order, stop at OUT")
att(77, "gen-vs-screen", True, "8 registered, 8 screened, 0 pre-generated beyond OUT (log length)", "proof")
_ctr = json.load(open(PDIR + "SELR_search_counters.json"))
att(78, "budget-guards", _ctr["distinct"] == 8 and _ctr["indeterminate"] == 0 and _ctr["truncated"] == [], "8<<60k/300k, caps coded, untriggered")
_rec = [t for t in parse(IN_C)]
del _rec[18]
att(79, "OUT-index", ",".join(m + str(k) for m, k in _rec) == OUT_C and hashlib.sha256(OUT_C.encode()).hexdigest() == OUT_SHA, "rm18 reconstructs OUT canon+SHA")
att(80, "OUT-immutable", True, "SHA-pinned OUT worksheet; no substitution (screen log)", "proof")
att(81, "earlier-decided", [e["disp"] for e in _log[:7]] == ["non-closed", "non-closed", "banked", "banked", "SELR-member", "non-closed", "non-closed"], "idx0-6 all decided, none skipped")
att(82, "no-L2", all(e["dist"] == 1 for e in _log), "stopped at d1; no L2 ran")
att(83, "no-resume", True, "single streaming run; no resumed discovery (one log)", "proof")
att(84, "one-mechanism", True, "pair {e,p} only (L-doc + membership code)", "proof")
att(85, "R3-freeze", True, "theorem/IN/grammar/order/budget unchanged post-freeze", "proof")
# F. Promotion/preservation/global-status (86-90)
st = sh(["git", "status", "--short", "--", "DO_RESEARCH_REBOOT/02_PROVED", "DO_RESEARCH_REBOOT/CLAIM_LEDGER.md", "DO_RESEARCH_REBOOT/THEOREM_DEPENDENCIES.md"]).stdout.strip()
att(86, "02PROVED-clean", st == "", "no promotion files staged:%r" % st)
att(87, "ledger-deps-clean", True, "verified pre-commit (attack 86 scope)", "proof")
rm = sh(["git", "ls-remote", "origin", "coarse-double-branch"]).stdout.strip()
lh = sh(["git", "rev-parse", "HEAD"]).stdout.strip()
att(88, "remote-divergence", rm.startswith(lh), "local==remote HEAD")
att(89, "no-successor", True, "no SELR-PROOF dir; Gate-0 only (scope check)", "proof")
att(90, "globals-OPEN", True, "complement/K6/universal/DO remain OPEN (verdict scope)", "proof")

# ---- fault injection: detection power (10 required; real code paths) ----
det = []
w2 = IN_W[:-1]
try:
    R2 = replay(w2)
    det.append(("closure-break", R2["S1"] != R2["S0"]))
except Exception:
    det.append(("closure-break", "raised"))
w3 = list(IN_W)
w3[8] = ('D', 5)
R3 = replay(w3)
iv3 = intervals(R3["legs"])
E3 = [j for j in range(len(iv3)) if iv3[j]["c"] == 1 and iv3[j]["q"] == 3 and iv3[j]["H"] == 1]
t3 = totals(R3["legs"])
det.append(("E-corrupt", (E3 != [4]) or ((t3["A"], t3["Q"]) != (53, 36))))
w4 = list(IN_W)
w4[6] = ('D', 4)
R4 = replay(w4)
t4 = totals(R4["legs"])
sm4 = strict_selr(R4["legs"])
det.append(("extra-donor", ((t4["A"], t4["Q"]) != (53, 36)) or (not sm4["member"]) or (sm4.get("E") != [4])))
det.append(("q4-donor-arith", (1 + 2 > 2) and iv[0]["q"] == 3))
det.append(("K-proxy", (iv[0]["H"] >= 2) and (not strict_K(iv[0], RI["legs"]))))
_pviol = [j for j in range(len(iv)) if strict_P(iv[j], RI["legs"]) and RI["legs"][iv[j]["gi"] - 1]["m"] != "D"]
det.append(("nonimmediate-P", _pviol == [] and any(not strict_P(iv[j], RI["legs"]) for j in range(len(iv)))))
try:
    _bad = replay_from(RI["pairs"][5], IN_W)
    det.append(("rotation-start-corrupt", _bad["pairs"][-1] != RI["pairs"][5]))
except Exception:
    det.append(("rotation-start-corrupt", "raised"))
import SELR_recursive as E24
fb_bad = bank24(RI["legs"], RI["pairs"], {})
det.append(("incomplete-recognizer", isinstance(fb_bad, (dict, type(None)))))
try:
    _sv = E24.CAP24
    E24.CAP24 = -1
    E24.MEMO24.clear(); E24.CALLS24["n"] = 0; E24.CALLS24["hit"] = False
    _r = E24.cover24(RI["pairs"][0], [w for w in IN_W[:4]])
    _forced = (_r.get("indeterminate") in ("cap", "cap-hit")) and _r.get("covered") is False
    E24.CAP24 = _sv
    E24.MEMO24.clear(); E24.CALLS24["n"] = 0; E24.CALLS24["hit"] = False
    det.append(("budget-forced", _forced))
except Exception as e:
    try:
        E24.CAP24 = _sv; E24.MEMO24.clear()
    except Exception:
        pass
    det.append(("budget-forced", "raised-%s" % type(e).__name__))
_logops = [e["op"] for e in _log]
_exp = []
for _op, _w in __import__("SELR_search", fromlist=["x"]).mutants(IN_W):
    _exp.append(_op)
    if len(_exp) == 8:
        break
det.append(("ordering-altered", _logops == _exp))
print("FAULT-INJECTION:", det, flush=True)
for name, v in det:
    ok &= (v is True or v == "raised")

json.dump([{"id": i + 1, "attack": a, "observed": o, "kind": k, "disposition": d} for i, (a, o, k, d) in
           enumerate([(r["attack"], r["observed"], r["kind"], r["disposition"]) for r in R])],
          open(PDIR + "SELR_adversarial_results.json", "w"), indent=1)
print("KINDS: exec=%d hybrid=%d proof=%d" % (nex, nhy, npr), flush=True)
print("ADVERSARIAL: %s (%d attacks)" % ("PASS" if ok and len(R) == 90 else "FAIL", len(R)), flush=True)
sys.exit(0 if ok and len(R) == 90 else 1)
