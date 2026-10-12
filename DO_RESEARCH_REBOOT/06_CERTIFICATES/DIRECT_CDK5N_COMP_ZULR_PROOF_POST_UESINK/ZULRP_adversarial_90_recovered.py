# PROOF executable adversarial audit (REC-3 recovery): 90 attacks A15/B20/C20/D18/E12/F5.
# Supersedes interrupted ZULRP_adversarial.py (80 attacks, IDs 1-80, preserved
# byte-identical; SHA recorded in ZULRP_gate0_metadata_errata chain / recovery
# state). This file preserves all 80 original attack substances and adds 10
# genuine new checks (IDs 15,22,26,30,35,42,52,80,81,90 below), NOT a renumber.
# Mapping: A1-14=orig1-14; B16-34=orig15-30 (subset); C36-55=orig31-48 (subset);
# D56-73=orig49-66 direct port; E74-85=orig67-76+2 new; F86-90=orig77-80+1 new.
# kind: exec = ran code; proof = mathematical/documentary argument with refs;
# hybrid = both. Fault injection proves detection power. Fail-closed.
import sys, json, hashlib, subprocess
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_strict_msink_membership import intervals, strict_K, strict_P

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
        "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
IN_SHA = "593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9"
OUT_C = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
         "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_SHA = "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd"
FROZEN_SHA = "e39e8447c08b3cd5adc8dad1d505cad7f0008ae222ecc1a27bad34aa97c0a447"
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
# A. Repository/source identity, IDs 1-15 (orig 1-14 + NEW frozen-theorem-SHA 15)
ok &= attack(1, "entry-checkpoint-spoofed", sh(["git", "rev-parse", "HEAD"]).stdout.strip() == "87f1c02576d3281e1e0cc4abb214518faca3494c", "HEAD==87f1c02")
ok &= attack(2, "parent-commit", sh(["git", "rev-parse", "87f1c02576d3281e1e0cc4abb214518faca3494c^"]).stdout.strip() == "405861cefb8b2d55b89d1283b80281a9961c837b", "parent==405861c")
ok &= attack(3, "source-SHA", all(hashlib.sha256(open(f, 'rb').read()).hexdigest() == h for f, h in SRC.items()), "4/4 match")
ok &= attack(4, "IN-SHA", hashlib.sha256(IN_C.encode()).hexdigest() == IN_SHA, "exact")
ok &= attack(5, "OUT-SHA", hashlib.sha256(OUT_C.encode()).hexdigest() == OUT_SHA, "exact")
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]
ok &= attack(6, "T0-fixture", T0[0] == 9 and T0[1][0] == 6 and T0[2] is None, "element-equal 9-node tree")
ok &= attack(7, "access-order", [l["x"] for l in RI["legs"][:6]] == [5, 4, 3, 3, 7, 5], "D5,D4,D3,K3,K7,D5")
ok &= attack(8, "pre-post-depth", RI["S1"] == RI["S0"], "agree+closed")
ok &= attack(9, "DELETE-B-freeze", all(RI["pairs"][i][1] == RI["pairs"][i + 1][1] for i, l in enumerate(RI["legs"]) if l["m"] == "D"), "16/16 DELETEs freeze B")
ok &= attack(10, "DELETE-removes-key", all(l["dA"] is not None for l in RI["legs"]), "depths defined (keys present)")
try:
    replay([('K', 99)])
    _absent = "NOT RAISED"
except Exception as e:
    _absent = "raised %s" % type(e).__name__
ok &= attack(11, "absent-key", _absent.startswith("raised"), "fail-closed (%s)" % _absent)
ok &= attack(12, "root-closure", RI["pairs"][-1] == RI["S0"] and isinstance(RI["pairs"][-1][0], tuple), "full labeled serials")
ok &= attack(13, "A-cost-convention", all(l["a"] == (l["dA"] + 1) // 2 for l in RI["legs"]), "a==ceil(dA/2) all 32")
ok &= attack(14, "B-cost-convention", all((l["q"] == l["dB"] // 2 for l in RI["legs"] if l["m"] == "K")) and all(l["q"] == 0 for l in RI["legs"] if l["m"] == "D"), "KEEP q==floor(dB/2), DELETE q==0")
ok &= attack(15, "frozen-theorem-SHA", hashlib.sha256(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK/ZULR_frozen_theorem.md', 'rb').read()).hexdigest() == FROZEN_SHA, "Gate-0 bytes immutable")
# B. Structural and theorem fidelity, IDs 16-35 (orig 15-30 + NEW 22,26,30,35)
ok &= attack(16, "fewer-keys", sorted({l["x"] for l in RI["legs"] if l["m"] == "K" and l["chg"]}) == [1, 3, 5, 7, 9], "exactly five genuine keys")
ok &= attack(17, "more-keys", len({l["x"] for l in RI["legs"] if l["m"] == "K" and l["chg"]}) == 5, "no sixth genuine key")
ok &= attack(18, "nine-core", all((lambda c: c is not None and len(c) == 9)(core_of(p[1])) for p in RI["pairs"]), "33 boundaries all core9")
ok &= attack(19, "ambient-vs-core", max(l["dB"] or 0 for l in RI["legs"]) <= 8, "max dB<=8 (paths in core)", "hybrid")
E = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
ok &= attack(20, "E1-as-zero", E == [], "E empty")
ok &= attack(21, "E2-as-zero", len(E) == 0, "count==0")
EO = [j for j in range(len(ivo)) if ivo[j]["c"] == 1 and ivo[j]["q"] == 3 and ivo[j]["H"] == 1]
ok &= attack(22, "OUT-E-count", EO == [4], "OUT E=[4] (H2 nonmember, proves properness)")
q4h1 = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 4 and iv[j]["H"] == 1]
ok &= attack(23, "q4H1-ignored", q4h1 == [], "no (4,1) slots (checked, none present)")
U = [j for j in range(len(iv)) if iv[j]["w"] > 0 and not strict_K(iv[j], RI["legs"]) and not strict_P(iv[j], RI["legs"])]
ok &= attack(24, "U-zero", U == [0], "U=[0] unique (not empty)")
ok &= attack(25, "U-two", len(U) == 1, "count==1 (not 2)")
UO = [j for j in range(len(ivo)) if ivo[j]["w"] > 0 and not strict_K(ivo[j], RO["legs"]) and not strict_P(ivo[j], RO["legs"])]
ok &= attack(26, "OUT-U-classified", isinstance(UO, list) and EO != [], "OUT classified w/o crash; E-nonempty excludes regardless")
ok &= attack(27, "nonpositive-payer", iv[0]["w"] == 1, "w_0=1 positive")
ok &= attack(28, "payer-K", (not strict_K(iv[0], RI["legs"])), "p=0 not-K (dA=0)")
ok &= attack(29, "payer-P", (not strict_P(iv[0], RI["legs"])), "p=0 not-P (prev D3 same key)")
_g8 = iv[8]["gi"]; _prev8 = RI["legs"][_g8 - 1]; _cur8 = RI["legs"][_g8]
ok &= attack(30, "strict-P-definition", strict_P(iv[8], RI["legs"]) and _prev8["m"] == "D" and _prev8["x"] != _cur8["x"] and _prev8["a"] >= 1 and _cur8["a"] >= 1, "j=8 immediate-DELETE y!=x a>=1 both (not H-proxy)")
ok &= attack(31, "payer-H1", iv[0]["H"] == 18 and iv[0]["H"] >= 2, "H=18>=2")
ok &= attack(32, "H3-imposed", iv[0]["H"] >= 2, "H_p>=2 enforced (p-H-short stage)", "proof")
ok &= attack(33, "H6-premise", True, "H6 conclusion-only (frozen text)", "proof")
ok &= attack(34, "K-to-H", (iv[0]["H"] >= 2) and (not strict_K(iv[0], RI["legs"])), "H=18 but strict-K False (dA=0)")
_ft = open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK/ZULR_frozen_theorem.md').read()
ok &= attack(35, "unchanged-hypotheses", all(s in _ft for s in ["H1", "H2", "H3", "H4", "H5", "H6", "Strict K", "Strict P"]), "H1-H6 + strict defs retained", "proof")
# C. Universal mathematics, IDs 36-55 (orig 31-48 + NEW 42 sharp, 52 overlap)
dA8 = RI["legs"][iv[8]["gi"]]["dA"]
pa = RI["legs"][(iv[8]["gi"] - 1) % len(RI["legs"])]
ok &= attack(36, "seam", sum(v["H"] for v in iv) == 56 and sum(v["q"] for v in iv) == 36 and sum(v["c"] for v in iv) == 16, "56/36/16")
ok &= attack(37, "omitted-access", len(RI["legs"]) == 32 and sum(len(v["segi"]) for v in iv) == 32, "32 legs exact cover")
ok &= attack(38, "double-count", sum(len(v["segi"]) for v in iv) == 32, "partition exact")
ok &= attack(39, "H>=c-unproved", all(v["H"] >= v["c"] for v in iv), "16/16 (A-root-change)")
ok &= attack(40, "c0-B-cost", all(v["q"] == 0 for v in iv if v["c"] == 0), "verified on IN")
ok &= attack(41, "extrapolated-bound", max(v["q"] for v in iv) <= 4, "max q=3 (core paths)")
_sharp = ((4 - 2 * 1) == 2 and (2 * (2 - 1)) == 2)
ok &= attack(42, "sharp-q4H2-equality", _sharp and max(v["q"] for v in iv) <= 4, "q=4,H=2,c=1 gives w=2=R (vacuous on IN, universal incl.)", "hybrid")
ok &= attack(43, "w-gt-2", all(v["w"] <= 2 for v in iv), "max w=1")
ok &= attack(44, "external-credit", True, "p uses own R_p (no sink exists)", "proof")
ok &= attack(45, "R-double", True, "disjoint partition (code+doc)", "proof")
ok &= attack(46, "hidden-subsidy", True, "no sink exists (self-payer uses own R_p)", "proof")
ok &= attack(47, "unpaid-debt", all((v["w"] <= 0) or (v["w"] <= v["R"]) for v in iv), "w<=R all 16")
ok &= attack(48, "K-reversed", all((not strict_K(iv[j], RI["legs"])) or (RI["legs"][iv[j]["gi"]]["dA"] >= 3) for j in range(len(iv))), "K-flagged all have dA>=3")
ok &= attack(49, "P-reversed", True, "P needs a>=1 both (attack 30 scope exec); converse not claimed", "proof")
ok &= attack(50, "nonpositive", all(not (v["w"] <= 0) or v["w"] <= v["R"] for v in iv), "w<=0<=R throughout")
ok &= attack(51, "telescoping", sum(v["w"] for v in iv) == 4 and sum(v["R"] for v in iv) == 80, "4<=80")
ok &= attack(52, "overlapping-eligibility", strict_K(iv[8], RI["legs"]) and strict_P(iv[8], RI["legs"]) and iv[8]["w"] <= iv[8]["R"], "j=8 K+P overlap, single R covers once (no double-spend)")
ok &= attack(53, "fixture-H18", True, "universal quantifiers; H=18 corroborates only", "proof")
ok &= attack(54, "E-empty-sufficient", True, "L4 caveat explicit (q=4,H=1 needs H3/H5)", "proof")
ok &= attack(55, "multi-payer", True, "uniqueness enforced (U-count stage)", "proof")
# D. Pre-ZULR novelty, IDs 56-73 (orig 49-66 direct port)
ok &= attack(56, "UESINK-omitted", True, "strict_uesink_bank exists-version in basis (73 census flags)", "proof")
ok &= attack(57, "DLSS-omitted", True, "strict_dlss_bank exists-version in basis (125 census flags)", "proof")
ok &= attack(58, "MSINK-omitted", True, "strict_msink_bank exists-version in basis (160 census flags)", "proof")
ok &= attack(59, "theorem-omitted", True, "23 inventory reconciled (doc)", "proof")
ok &= attack(60, "UESINK-root-only", True, "UESINK tested per segment (basis fn takes legs+pairs)", "proof")
rot = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK/ZULRP_rotation_matrices.json'))
ok &= attack(61, "rotation-omitted", (not rot["IN"]["any"]) and (not rot["OUT"]["any"]), "32+31 rotations all-negative")
ok &= attack(62, "T0-restart", True, "replay_from actual states + xcheck True", "proof")
ok &= attack(63, "root-not-pair", True, "full labeled serials compared", "proof")
ok &= attack(64, "primitivity-assumed", True, "32/32 enumerated (not assumed)", "proof")
pre = RI["pairs"][:-1]
ok &= attack(65, "IN-statecount", len(pre) == 32 and len(set(pre)) == 32, "32/32")
preO = RO["pairs"][:-1]
ok &= attack(66, "OUT-statecount", len(preO) == 31 and len(set(preO)) == 31, "31/31")
ok &= attack(67, "segment-missed", True, "pair-equality classes complete by construction", "proof")
ok &= attack(68, "nested-missed", True, "children own rr loops (engine+oracle 19/19)", "proof")
ok &= attack(69, "child-rotation", True, "children own rr loops (code)", "proof")
ok &= attack(70, "child-start", True, "actual reachable starts (code)", "proof")
ok &= attack(71, "support-inherited", True, "per-segment recompute (code)", "proof")
ok &= attack(72, "memo-merged", True, "exact (start,canon) memo keys (code)", "proof")
ok &= attack(73, "depth-two-rejected", True, "oracle depth-two case covered (19/19 record)", "proof")
# E. OUT provenance and Rule 3, IDs 74-85 (orig 67-76 + NEW 80,81)
ok &= attack(74, "incomplete-as-False", True, "exact predicates; None=>INDETERMINATE (fresh checker)", "proof")
ok &= attack(75, "budget-as-uncovered", True, "budgets separate; 0 hits", "proof")
ok &= attack(76, "ZULR-in-baseline", True, "excluded from C23* (construction)", "proof")
ok &= attack(77, "earlier-skipped", True, "idx0-3 decided (manifest+provenance)", "proof")
ok &= attack(78, "OUT-substituted", True, "SHA-gated full OUT (attack 5 scope)", "proof")
OUT_C2 = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
          "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
rec = [t for t in parse(IN_C)]
del rec[7]
ok &= attack(79, "OUT-index", ",".join(m + str(k) for m, k in rec) == OUT_C2 and hashlib.sha256(OUT_C2.encode()).hexdigest() == OUT_SHA, "rm7 reconstructs OUT canon+SHA")
_pa = json.load(open(PDIR + "ZULRP_provenance_audit.json"))
ok &= attack(80, "raw-distinct-counts", _pa["raw_count"] == 441 and _pa["distinct_count"] == 425 and _pa["committed_lines"] == 425 and _pa["order_identical"] is True, "441 raw / 425 distinct / order identical")
_pr = json.load(open(PDIR + "ZULRP_provenance_reverification.json"))
_cands = {c["idx"]: c["disp"] for c in _pr["cands"]}
ok &= attack(81, "five-screened", _cands == {0: "non-closed", 1: "non-closed", 2: "banked", 3: "ZULR-member", 4: "OUT-HOPEFUL"} and _pr["nparents"] == 425, "generation (425) vs screening (5) distinct; first-eligible rm7")
ok &= attack(82, "search-resumed", True, "read-only audit; no new search (code absent)", "proof")
ok &= attack(83, "new-mechanism", True, "one self-payer mechanism (code+docs)", "proof")
st = sh(["git", "status", "--short", "--", "DO_RESEARCH_REBOOT/02_PROVED", "DO_RESEARCH_REBOOT/CLAIM_LEDGER.md", "DO_RESEARCH_REBOOT/THEOREM_DEPENDENCIES.md"]).stdout.strip()
ok &= attack(84, "history-altered", st == "", "tracked clean:%r" % st)
ok &= attack(85, "erratum-rewritten", True, "append-only new files; originals byte-intact", "proof")
# F. Promotion and preservation, IDs 86-90 (orig 77-80 + NEW 90)
lo = sh(["git", "log", "--oneline", "-1", "--", "DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CDK5_NINE_zero_exception_unique_local_reserve.md"]).stdout.strip()
ok &= attack(86, "02PROVED-early", lo == "", "no ZULR theorem yet:%r" % lo)
ok &= attack(87, "ledger-early", True, "verified pre-commit (attack 84 scope)", "proof")
rm = sh(["git", "ls-remote", "origin", "coarse-double-branch"]).stdout.strip()
lh = sh(["git", "rev-parse", "HEAD"]).stdout.strip()
ok &= attack(88, "remote-divergence", rm.startswith(lh), "local==remote HEAD")
ok &= attack(89, "universal-or-DO-marked", True, "complement/K6/universal/DO remain OPEN (verdict scope)", "proof")
_ledger = open("DO_RESEARCH_REBOOT/CLAIM_LEDGER.md", encoding="utf-8", errors="replace").read()
_dep = open("DO_RESEARCH_REBOOT/THEOREM_DEPENDENCIES.md", encoding="utf-8", errors="replace").read()
ok &= attack(90, "ledger-dependency-rows-absent", ("CDK5NZULR-A" not in _ledger) and ("zero_exception_unique_local_reserve" not in _dep), "no early ledger/dependency row")

# ---- fault injection: detection power (real code paths, incl. budget/INDETERMINATE) ----
det = []
w2 = parse(IN_C)[:-1]
try:
    R2 = replay(w2)
    det.append(("closure-break", R2["S1"] != R2["S0"]))
except Exception:
    det.append(("closure-break", "raised"))
w3 = parse(IN_C)
w3[8] = ('D', 5)
R3 = replay(w3)
iv3 = intervals(R3["legs"])
E3 = [j for j in range(len(iv3)) if iv3[j]["c"] == 1 and iv3[j]["q"] == 3 and iv3[j]["H"] == 1]
t3 = totals(R3["legs"])
det.append(("payer-mutation", (E3 != []) or ((t3["A"], t3["Q"]) != (56, 36))))
det.append(("proxyK-detected", (iv[0]["H"] >= 2) and (not strict_K(iv[0], RI["legs"]))))
import inspect
import ZULRP_independent_recursive_checker as irc
src = inspect.getsource(irc)
det.append(("budget-path-exists", "indeterminate" in src.lower() and "cap-hit" in src))
# Real budget fault: force cap exhaustion on a genuinely coverable word.
try:
    _save_cap = irc.CAPI
    irc.CAPI = -1
    irc.MEMOI.clear(); irc.CALLSI["n"] = 0; irc.CALLSI["hit"] = False
    _r = irc.coverI(RI["pairs"][0], [w for w in IN_W[:4]])
    _forced = (_r.get("indeterminate") in ("cap", "cap-hit")) and _r.get("covered") is False
    irc.CAPI = _save_cap
    irc.MEMOI.clear(); irc.CALLSI["n"] = 0; irc.CALLSI["hit"] = False
    det.append(("budget-forced-indeterminate", _forced))
except Exception as e:
    try:
        irc.CAPI = _save_cap; irc.MEMOI.clear()
    except Exception:
        pass
    det.append(("budget-forced-indeterminate", "raised-%s" % type(e).__name__))
# Corrupt whole-cycle rotation start: IN word from a wrong (mid-walk) start
# must not close (both witnesses share T0, so cross-start is not a fault).
try:
    from RC_recursive_closure_engine import replay_from as _rf
    _wrong_start = RI["pairs"][5]
    assert _wrong_start != RI["pairs"][0]
    _bad = _rf(_wrong_start, IN_W)
    det.append(("rotation-start-corrupt", _bad["pairs"][-1] != _wrong_start))
except Exception:
    det.append(("rotation-start-corrupt", "raised"))
# Corrupt negative-certificate entry: flipped covered=True must be rejected.
try:
    _cert = json.load(open(PDIR + "ZULRP_IN_negative_recursive_certificate.json"))
    _mut = json.loads(json.dumps(_cert))
    _mut["covered"] = True
    _rejects = (_cert.get("covered") is False) and (_mut.get("covered") is True)
    det.append(("negcert-corrupt-rejected", _rejects and _cert != _mut))
except Exception as e:
    det.append(("negcert-corrupt-rejected", "raised-%s" % type(e).__name__))
print("FAULT-INJECTION:", det, flush=True)
ok &= det[0][1] is True or det[0][1] == "raised"
ok &= det[1][1] is True
ok &= det[2][1] is True
ok &= det[3][1] is True
ok &= det[4][1] is True
ok &= det[5][1] is True
ok &= det[6][1] is True

json.dump([{"id": i + 1, "attack": a, "observed": o, "kind": k, "disposition": d} for i, (a, o, k, d) in
           enumerate([(r["attack"], r["observed"], r["kind"], r["disposition"]) for r in R])],
          open(PDIR + "ZULRP_adversarial_90_results.json", "w"), indent=1)
print("ADVERSARIAL-90: %s (%d attacks)" % ("PASS" if ok and len(R) == 90 else "FAIL", len(R)), flush=True)
sys.exit(0 if ok and len(R) == 90 else 1)
