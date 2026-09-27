"""WP-2 STEP 60: 16 section-38 mutants, each introduced + rejected."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
EV = '{"case": "LL", "lo": 1, "hi": 3, "orient": "-"}'
PROBE_DIFF = """
import sys; sys.path.insert(0, %r); sys.path.append(%r)
from liquidity import activation as A, profiles as PR
from independent import ledger as I
led = [[%r, 1, 2, True] for _ in range(5)] + [[%r, 2, 3, False] for _ in range(2)] + [["SPENT", 0, 1, True] for _ in range(2)]
prof = PR.%s(%d)
ev = %s
a = A.t5_rho([list(c) for c in led], 'P_all', prof, 'KEEP', ev)
b, _ = I.activate_bounded(([tuple(c) for c in led], 0), I.rho_cap(prof.as_pair(), (ev['case'], ev['lo'], ev['hi'], ev['orient'])), 'KEEP', ev)
print('MISMATCH' if [tuple(c) for c in a] != b or A.pools(a) != I.pools(b) or A.energy(a) != I.energy_of(b) else 'AGREE')
"""
PROBE_N28 = """
import sys; sys.path.insert(0, %r); sys.path.append(%r)
from liquidity import legacy_embedding as P
rp, _ = P.exec_hist(P.vine_right(28), [('DELETE', 27), ('DELETE', 28), ('KEEP', 28), ('KEEP', 27)], 28)
s0, g = rp[0], rp[3]
ok = (s0['L1'], s0['P1'], s0['rA']) == (65, 13, 13) and (g['a'], g['y'], g['need'], g['paid'], g['margin']) == (2, 15, 11, 10, -1)
print('MISMATCH' if not ok else 'AGREE')
"""
PROBE_MU = """
import sys; sys.path.insert(0, %r); sys.path.append(%r)
from liquidity import legacy_embedding as P
from liquidity import multiplicity as MU
t, evs = P.splay_trace(P.vine_right(9), 9)
print('MISMATCH' if MU.trace_sum(evs) != P.splay_cost(P.vine_right(9), 9) - 1 else 'AGREE')
"""

MUTS = [
    ("M01-double-2to1", "python/liquidity/multiplicity.py", "    return 2", "    return 1", "mu", ()),
    ("M02-zig-cap", "python/liquidity/profiles.py", "        if cls == \"ZIG\":\n            return self._z", "        if cls == \"ZIG\":\n            return self._d", "diff", ("ROT", 3, "LATENT", "ACTIVE", "{}", "ZIG")),
    ("M03-rho-on-n", "python/liquidity/profiles.py", "        if cls == \"ROOT\":\n            return 0", "        if cls == \"ROOT\":\n            return 0\n        if isinstance(ev, dict) and \"n\" in ev:\n            return self._z + ev[\"n\"]", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{'n': 5}", "LL")),
    ("M04-rho-on-need", "python/liquidity/profiles.py", "        if cls == \"ROOT\":\n            return 0", "        if cls == \"ROOT\":\n            return 0\n        if isinstance(ev, dict) and \"need\" in ev:\n            return self._z + ev[\"need\"]", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{'need': 4}", "LL")),
    ("M05-rho-on-future", "python/liquidity/profiles.py", "        if cls == \"ROOT\":\n            return 0", "        if cls == \"ROOT\":\n            return 0\n        if isinstance(ev, dict) and \"future\" in ev:\n            return self._z + 1", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{'future': 9}", "LL")),
    ("M06-rho-on-residual", "python/liquidity/profiles.py", "        if cls == \"ROOT\":\n            return 0", "        if cls == \"ROOT\":\n            return 0\n        if isinstance(ev, dict) and \"residual\" in ev:\n            return self._z + ev[\"residual\"]", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{'residual': 3}", "LL")),
    ("M07-creates-credit", "python/liquidity/activation.py", "    for _ in range(cap):", "    out.append([\"LATENT\", 0, 0, True])\n    for _ in range(cap):", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{}", "LL")),
    ("M08-support", "python/liquidity/activation.py", "    out[i][0] = ACTIVE", "    out[i][0] = ACTIVE\n    out[i][1], out[i][2] = out[i][2], out[i][1]", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{}", "LL")),
    ("M09-reorder", "python/liquidity/activation.py", "    out = [list(c) for c in ledger]\n    for _ in range(cap):", "    out = [list(c) for c in reversed(ledger)]\n    for _ in range(cap):", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{}", "LL")),
    ("M10-resurrect", "python/liquidity/activation.py", "    return [i for i, c in enumerate(ledger) if c[0] == LATENT]", "    return [i for i, c in enumerate(ledger) if c[0] in (LATENT, \"SPENT\")]", "diff", ("ROT", 4, "LATENT", "ACTIVE", "{}", "LL")),
    ("M11-last-latent", "python/liquidity/activation.py", "    i = idx[0]", "    i = idx[-1]", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{}", "LL")),
    ("M12-extra-iter", "python/liquidity/activation.py", "    for _ in range(cap):", "    for _ in range(cap + 1):", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{}", "LL")),
    ("M13-unbounded", "python/liquidity/activation.py", "    for _ in range(cap):\n        new = t5_one(out, predicate, mode, ev)\n        if new == out:\n            break\n        out = new", "    while True:\n        new = t5_one(out, predicate, mode, ev)\n        if new == out:\n            break\n        out = new", "diff", ("FLAT", 2, "LATENT", "ACTIVE", "{}", "LL")),
    ("M14-t7-coeff", "python/liquidity/legacy_embedding.py", "    picks = [ss[(cursor + j) % len(ss)] for j in range(K_FROZEN)]", "    picks = [ss[(cursor + j) % len(ss)] for j in range(K_FROZEN + 1)]", "n28", ()),
    ("M15-t6-latent", "python/liquidity/legacy_embedding.py", "        if rem > 0 and c[0] == ACTIVE:", "        if rem > 0 and c[0] in (ACTIVE, LATENT):", "n28", ()),
    ("M16-flat1-diverge", "python/liquidity/activation.py", "    cap = profile.capacity(ev)", "    cap = profile.capacity(ev)\n    if cap == 1:\n        return [list(c) for c in ledger]", "diff", ("FLAT", 1, "LATENT", "ACTIVE", "{}", "ZIG")),
]


def main():
    print("[WP-2][STEP 60] Introducing 16 section-38 mutants; each must be rejected")
    res = {}
    for mid, rel, old, new, kind, args in MUTS:
        tmp = Path(tempfile.mkdtemp(prefix="wp2mut_"))
        shutil.copytree(ROOT / "python", tmp / "python")
        p = tmp / rel
        data = p.read_text(encoding="utf-8")
        assert old in data, (mid, "pattern missing")
        p.write_text(data.replace(old, new, 1), encoding="utf-8")
        probe = tmp / "probe.py"
        if kind == "diff":
            fam, r, la, ac, extra, evcase = args
            ev_src = '{"case": "%s", "lo": 1, "hi": 3, "orient": "-", **%s}' % (evcase, extra)
            probe.write_text(PROBE_DIFF % (str(tmp / "python"), str(ROOT / "python"), la, ac, fam, r, ev_src), encoding="utf-8")
        elif kind == "mu":
            probe.write_text(PROBE_MU % (str(tmp / "python"), str(ROOT / "python")), encoding="utf-8")
        else:
            probe.write_text(PROBE_N28 % (str(tmp / "python"), str(ROOT / "python")), encoding="utf-8")
        rr = subprocess.run([PY, str(probe)], capture_output=True, text=True)
        killed = "MISMATCH" in (rr.stdout or "")
        if not killed:
            print("[WP-2][STEP 60] %s probe stderr: %s" % (mid, (rr.stderr or "")[-300:]))
        res[mid] = "KILLED" if killed else "SURVIVED"
        print("[WP-2][STEP 60] %s: %s" % (mid, res[mid]))
        shutil.rmtree(tmp, ignore_errors=True)
    bad = [k for k, v in res.items() if v != "KILLED"]
    if bad:
        print("[WP-2][STEP 60] SURVIVORS: %s" % bad)
        return 1
    print("[WP-2][STEP 60] ALL_16_KILLED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
