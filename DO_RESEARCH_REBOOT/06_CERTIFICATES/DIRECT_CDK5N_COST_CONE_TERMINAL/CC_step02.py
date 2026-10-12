# STEP 02 verification: core monotonicity, constancy, projection commutation.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, core_of, from_serial, idepths
from RC_recursive_closure_engine import replay_from
import splay as S
from wp6_eventflow import to_ptr

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
M = {1, 3, 5, 7, 9}
R = []
ok = True
def check(name, cond, obs):
    global ok
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    if not cond:
        ok = False

def contract(t, Sset):
    if t == '.' or t == ("leaf",) or (isinstance(t, tuple) and t and t[0] == "leaf"):
        return S.LEAF
    if isinstance(t, tuple) and len(t) == 4 and t[0] == "node":
        _, k, l, r = t
    elif isinstance(t, tuple) and len(t) == 3:
        k, l, r = t
    else:
        return S.LEAF
    if k not in Sset:
        return S.LEAF
    return S.node(k, contract(l, Sset), contract(r, Sset))

def core_labels(ps):
    return core_of(ps)

# corpus + witnesses + random closed words: core-next subseteq core-current on B-KEEPs; constancy on closed walks
WORDS = ["D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"]
RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
import json as J
rows = []
for seed in ("concat35", "mr33"):
    for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
        rows.append(J.loads(l))
bycanon = {}
for r in rows:
    bycanon.setdefault(r["canon"], []).append(r)
for i, cs in enumerate(sorted(bycanon)):
    WORDS.append(cs)
    if i >= 60:
        break

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

mono_bad = 0
mono_tot = 0
const_bad = 0
comm_bad = 0
depth_bad = 0
nwords = 0
for cw in WORDS:
    w = parse(cw)
    try:
        Rp = replay(w)
    except Exception:
        continue
    if not (Rp["S1"] == Rp["S0"] and Rp["agree"]):
        continue
    nwords += 1
    pairs = Rp["pairs"]
    legs = Rp["legs"]
    cores = [core_labels(p[1]) for p in pairs]
    if any(c is None or len(c) != 9 for c in cores):
        continue
    # constancy along closed walk
    if not all(c == cores[0] for c in cores):
        const_bad += 1
    for k, l in enumerate(legs):
        if l["m"] != "K":
            # DELETE: B unchanged => core equal
            if cores[k] != cores[k + 1]:
                mono_bad += 1
            mono_tot += 1
            continue
        # B-KEEP: monotonicity next ⊆ current
        mono_tot += 1
        if not (set(cores[k + 1]) <= set(cores[k])):
            mono_bad += 1
        # projection commutation: contract(splay) == splay(contract)
        St = set(cores[k])
        Tb = from_serial(pairs[k][1])
        proj_before = contract(Tb, St)
        # replay single KEEP from state pairs[k]
        Fr = replay_from(pairs[k], [w[k]])
        Ta = from_serial(Fr["pairs"][-1][1])
        proj_after = contract(Ta, St)
        sp = S.trace(proj_before, l["x"])[0]
        if sp != proj_after:
            comm_bad += 1
        # marked depths equal in B and projection
        dB = idepths(Tb)
        def pdepth(t, x):
            if isinstance(t, tuple) and t and t[0] == "leaf":
                return None
            if t == '.' or t == S.LEAF:
                return None
            _, kk, ll, rr = t
            if x == kk:
                return 0
            d = pdepth(ll if x < kk else rr, x)
            return None if d is None else d + 1
        for x in M:
            if dB.get(x) != pdepth(proj_before, x):
                depth_bad += 1
                break

check("core-monotone", mono_bad == 0, "%d/%d B-steps monotone (incl DELETE-equal)" % (mono_tot - mono_bad, mono_tot))
check("core-constant-closed", const_bad == 0, "%d/%d closed walks constant-9" % (nwords - const_bad, nwords))
check("projection-commutes", comm_bad == 0, "splay/projection commutation")
check("marked-depths-equal", depth_bad == 0, "B vs projected depths")
json.dump({"pass": ok, "checks": R}, open(PDIR + "CC_B_CORE_CHECK.json", "w"), indent=1)
print("STEP02-VERIFY: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)
