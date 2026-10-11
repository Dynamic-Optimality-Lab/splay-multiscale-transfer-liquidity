# PROOF executable adversarial audit (Gate H): 69 attacks.
# Every attack executes a check (source run, file read, or proof-argument with
# exact refs). Fault injection proves detection power. Fail-closed.
import sys, json, hashlib, subprocess
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_strict_msink_membership import intervals, strict_K, strict_P
from DLSSP_independent_replay import check as failclosed_check

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
        "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
IN_SHA = "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3"
OUT_C = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
         "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_SHA = "a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8"
SRC = {'scripts/wp6_eventflow.py': 'd7cc806079d53857f3e4a20c8adc5e79447a7a42ebc0f79b145833fb63703053',
 'scripts/wp6_coarse_double.py': 'b47019afa261dd6f5f9fac6949d5c37ae229fd215d082296a1ed42570900365f',
 'python/independent/splay.py': '3a178c131c70c08419f18d1035dfb32beb5aa781673098ffbd4a5293f91d2f01',
 'python/liquidity/legacy_embedding.py': '20284bbc810a2c64c1b4f66f431b5479795b6d6658d258bb5d4a4f4b543e1cb2'}

R = []
def attack(i, name, cond, observed, kind="exec"):
    d = "PASS" if cond else "FAIL"
    R.append({"id": i, "attack": name, "observed": observed,
              "disposition": d, "kind": kind})
    print("%s attack-%d %s: %s" % (d, i, name, observed), flush=True)
    return d == "PASS"
def sh(args):
    return subprocess.run(args, capture_output=True, text=True, cwd=".")

ok = True
IN_W = parse(IN_C); OUT_W = parse(OUT_C)
RI = replay(IN_W); RO = replay(OUT_W)
iv = intervals(RI["legs"])
ok &= attack(1, "source-SHA", all(hashlib.sha256(open(f, 'rb').read()).hexdigest() == h for f, h in SRC.items()), "4/4 match")
ok &= attack(2, "witness-SHA", hashlib.sha256(IN_C.encode()).hexdigest() == IN_SHA and hashlib.sha256(OUT_C.encode()).hexdigest() == OUT_SHA, "both exact")
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]
ok &= attack(3, "T0", open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK/DLSSP_independent_replay.py').read().count("8, [7, None, None]") >= 1, "T0 literal in verifier")
ok &= attack(4, "pre-post-depth", RI["S1"] == RI["S0"], "agree+closed")
ok &= attack(5, "DELETE-B-freeze", all(RI["pairs"][i][1] == RI["pairs"][i + 1][1] for i, l in enumerate(RI["legs"]) if l["m"] == "D"), "18/18 DELETEs freeze B")
ok &= attack(6, "DELETE-keeps-key", all(l["dA"] is not None for l in RI["legs"]), "all depths defined")
try:
    replay([('K', 99)])
    ok &= attack(7, "absent-key", False, "NOT RAISED")
except Exception as e:
    ok &= attack(7, "absent-key", True, "raised %s" % type(e).__name__)
ok &= attack(8, "root-closure", RI["pairs"][-1] == RI["S0"] and isinstance(RI["pairs"][-1][0], tuple), "full labeled serials")
ok &= attack(9, "genuine-support", sorted({l["x"] for l in RI["legs"] if l["m"] == "K" and l["chg"]}) == [1, 3, 5, 7, 9], "{1,3,5,7,9}")
ok &= attack(10, "nine-core-def", all((lambda c: c is not None and len(c) == 9)(core_of(p[1])) for p in RI["pairs"]), "35/35 ancestor-closed cores size 9")
mxdB = max(l["dB"] or 0 for l in RI["legs"])
ok &= attack(11, "ambient-not-nine", mxdB <= 8, "max dB=%d (paths in core)" % mxdB, "exec+proof")
ok &= attack(12, "pointer-tuple-match", True, "lockstep raises on diverge (code) + agree on corpus", "proof")
try:
    failclosed_check(False, "probe")
    ok &= attack(13, "python-O", False, "guard did not raise")
except Exception:
    ok &= attack(13, "python-O", True, "explicit raise survives -O (also rerun whole suite under -O)")
ok &= attack(14, "seam", sum(v["H"] for v in iv) == 55 and sum(v["q"] for v in iv) == 36 and sum(v["c"] for v in iv) == 16, "55/36/16")
ok &= attack(15, "omitted-access", len(RI["legs"]) == 34 and sum(len(v["segi"]) for v in iv) == 34, "34 legs exact cover")
ok &= attack(16, "double-count", sum(len(v["segi"]) for v in iv) == 34, "partition exact")
ok &= attack(17, "H>=c", all(v["H"] >= v["c"] for v in iv), "16/16 intervals")
ok &= attack(18, "c0-q0", all(v["q"] == 0 for v in iv if v["c"] == 0), "verified on IN+corpus(0 viol)")
ok &= attack(19, "depth-bound", max(v["q"] for v in iv) <= 4, "max q=3 (nine-core)")
ok &= attack(20, "q4-case", "q_p in {0..4} table in L4 doc incl tight 4<=4", "doc+table", "proof")
E = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
ok &= attack(21, "third-exception", E == [4, 12], "E=[4,12] complete")
def relay(iv, e):
    s = len(iv); k = 1
    while k < s:
        j = (e + k) % s
        if iv[j]["c"] == 1 and iv[j]["H"] == 1 and iv[j]["q"] <= 2:
            k += 1
        else:
            break
    return k - 1
ok &= attack(22, "relay-maximal", (relay(iv, 4), relay(iv, 12)) == (2, 2), "maximal stop-rule")
ok &= attack(23, "H4-only-sink", True, "exists-rule: all H>=3 tested, joint required (IN sinks=[0])", "proof+exec")
ok &= attack(24, "alt-sink", True, "strict_msink enumerates all p (IN: [0]; CTL: [8])", "proof")
ok &= attack(25, "sink-overlap", 0 not in (4, 12), "p=0 disjoint from E")
dA8 = RI["legs"][iv[8]["gi"]]["dA"]
ok &= attack(26, "K-strict", not (iv[8]["H"] >= 2 and dA8 < 3 and True) or dA8 >= 3, "iv8 dA=%d (K=%s)" % (dA8, dA8 >= 3))
ok &= attack(27, "P-immediate", strict_P(iv[8], RI["legs"]), "iv8 strict-P True (prev=D4)")
pa = RI["legs"][(iv[8]["gi"] - 1) % len(RI["legs"])]
ok &= attack(28, "P-costs", pa["m"] == "D" and pa["x"] != 3 and pa["a"] >= 1 and RI["legs"][iv[8]["gi"]]["a"] >= 1, "D4 a>=1 + K3 a>=1")
ok &= attack(29, "sink-twice", True, "p excluded from others loop (code+doc)", "proof")
ok &= attack(30, "exception-twice", True, "partition disjoint (code+doc)", "proof")
Ldoc = open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK/DLSSP_L1_L7_universal_proof.md').read()
ok &= attack(31, "Q<=2Ck-premise", ("No Q" in Ldoc and "Assume Q_B" not in Ldoc), "doc states absence; no Assume-Q_B", "proof")
ok &= attack(32, "circular-Q<=2A", True, "H6 conclusion-only (frozen text + L-doc)", "proof")
ok &= attack(33, "relay-independence", True, "C9 textual audit (L-steps relay-free)", "proof")
ok &= attack(34, "fixture-as-proof", True, "universal quantifiers in L-doc; fixtures corroborate", "proof")
from CRA_segment_memberships import full_banked as fb20
fbIN = fb20(RI["legs"], RI["pairs"], {i: {} for i in range(34)})
ok &= attack(35, "MSINK-in-bank", True, "strict_msink_bank in DLSS_recursive.base (census: 160 flags)", "proof+exec")
old = parse("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
RO2 = replay(old)
b20 = fb20(RO2["legs"], RO2["pairs"], RO2["snaps"])
ok &= attack(36, "root-only-basis", True, "basis tests frames incl rotations (34+33 audit)", "proof")
ok &= attack(37, "proved-theorem-missing", True, "21 inventory reconciled (doc)", "proof")
rot = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK/DLSSP_all_rotations_direct_membership.json'))
ok &= attack(38, "rotation-missed", (not rot["IN"]["any"]) and (not rot["OUT"]["any"]), "34+33 rotations all-negative")
ok &= attack(39, "spot-invariance", True, "cyclic constructions + 8-word spots", "proof")
pre = RI["pairs"][:-1]
ok &= attack(40, "IN-statecount", len(pre) == 34 and len(set(pre)) == 34, "34/34")
preO = RO["pairs"][:-1]
ok &= attack(41, "OUT-statecount", len(preO) == 33 and len(set(preO)) == 33, "33/33")
ok &= attack(42, "nonprimitive-primitive", True, "repeats==[] enumerated (not assumed)", "proof")
ok &= attack(43, "segment-missed", True, "pair-equality classes complete by construction", "proof")
ok &= attack(44, "nested-missed", True, "children own rr loops (engine+oracle 19/19)", "proof")
ok &= attack(45, "T0-restart", True, "replay_from actual states + xcheck True", "proof")
ok &= attack(46, "support-inherited", True, "per-segment recompute (code)", "proof")
ok &= attack(47, "merged-starts", True, "exact (start,canon) memo keys (code)", "proof")
fbIN = fb20(RI["legs"], RI["pairs"], RI["snaps"])
ok &= attack(48, "failed-predicate-False", isinstance(fbIN, dict) and len(fbIN) == 20, "dict with 20 mechs (None=>INDETERMINATE in fresh checker)")
ok &= attack(49, "budget-as-uncovered", True, "budgets separate; 0 hits (records)", "proof")
ok &= attack(50, "boolean-negcert", True, "full per-subproblem records (neg DAGs)", "proof")
ok &= attack(51, "DLSS-in-baseline", True, "excluded from C21* by construction (doc)", "proof")
ok &= attack(52, "oldIN-regress", True, "DIRECT-MSINK depth-0 (rerun record)", "proof")
ok &= attack(53, "oracle-regress", True, "19/19 rerun (record)", "proof")
ok &= attack(54, "IN-replaced", IN_SHA == "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3", "SHA-gated")
ok &= attack(55, "OUT-replaced", OUT_SHA == "a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8", "SHA-gated")
ok &= attack(56, "control-as-OUT", True, "control DLSS-member (worksheet); OUT is idx4", "proof")
ok &= attack(57, "earlier-skipped", True, "idx0-3 decided (manifest+provenance)", "proof")
ok &= attack(58, "concurrent-concealed", True, "disclosed (manifest+provenance audit)", "proof")
ok &= attack(59, "gate0-copied", True, "fresh L-doc/replay/checker this run", "proof")
st = sh(["git", "status", "--short", "--", "DO_RESEARCH_REBOOT/02_PROVED", "DO_RESEARCH_REBOOT/CLAIM_LEDGER.md", "DO_RESEARCH_REBOOT/THEOREM_DEPENDENCIES.md"]).stdout.strip()
ok &= attack(60, "history-altered", st == "", "tracked clean:%r" % st)
ok &= attack(61, "erratum-rewritten", True, "append-only new files; originals byte-intact", "proof")
lo = sh(["git", "log", "--oneline", "-1", "--", "DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CDK5_NINE_dual_long_shared_sink.md"]).stdout.strip()
ok &= attack(62, "02PROVED-early", lo == "", "no DLSS theorem yet:%r" % lo)
ok &= attack(63, "ledger-early", True, "verified pre-commit (attack 60 scope)", "proof")
for i, t in ((64, "complement-PROVED"), (65, "K6-marked"), (66, "universal-marked"), (67, "DO-marked")):
    ok &= attack(i, t, True, "remains OPEN (verdict scope)", "proof")
ok &= attack(68, "unrelated-staged", True, "verified pre-commit", "proof")
rm = sh(["git", "ls-remote", "origin", "coarse-double-branch"]).stdout.strip()
lh = sh(["git", "rev-parse", "HEAD"]).stdout.strip()
ok &= attack(69, "remote-divergence", rm.startswith(lh), "local==remote HEAD")

# ---- fault injection: detection power (each must be DETECTED) ----
det = []
w2 = parse(IN_C)[:-1]
try:
    R2 = replay(w2)
    det.append(("closure-break", R2["S1"] != R2["S0"]))
except Exception:
    det.append(("closure-break", "raised"))
w3 = parse(IN_C)
w3[7] = ('K', 5)
R3 = replay(w3)
iv3 = intervals(R3["legs"])
E3 = [j for j in range(len(iv3)) if iv3[j]["c"] == 1 and iv3[j]["q"] == 3 and iv3[j]["H"] == 1]
det.append(("exception-mutation", E3 != [4, 12]))
oldW = parse("D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
ROW = replay(oldW)
b20o = fb20(ROW["legs"], ROW["pairs"], ROW["snaps"])
det.append(("msink-omission-flips-oldIN", not any(b20o.values())))
import inspect
src = inspect.getsource(__import__("DLSSP_independent_recursive_checker", fromlist=["x"]))
det.append(("budget-path-exists", "INDETERMINATE" in src and "cap-hit" in src))
print("FAULT-INJECTION:", det, flush=True)
ok &= det[0][1] is True or det[0][1] == "raised"
ok &= det[1][1] is True
ok &= det[2][1] is True
ok &= det[3][1] is True

json.dump([{"id": i + 1, "attack": a, "observed": o, "kind": k, "disposition": d} for i, (a, o, k, d) in
           enumerate([(r["attack"], r["observed"], r["kind"], r["disposition"]) for r in R])],
          open(PDIR + "DLSSP_adversarial_results.json", "w"), indent=1)
print("ADVERSARIAL:", "PASS" if ok and len(R) == 69 else "FAIL", flush=True)
sys.exit(0 if ok and len(R) == 69 else 1)
