"""WP-1 STEP 33: engine mutants M-WP1-01..04 — each must be rejected (mismatches found)."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
PROBE = """
import sys; sys.path.insert(0, %r); sys.path.append(%r)
from liquidity import legacy_embedding as P
from independent import ledger as I, splay as S
bad = 0
for n, H in [(5, [('KEEP', 3), ('DELETE', 1)]), (6, [('DELETE', 5), ('KEEP', 6), ('KEEP', 4)]), (28, [('DELETE', 27), ('DELETE', 28), ('KEEP', 28), ('KEEP', 27)])]:
    rp, _ = P.exec_hist(P.vine_right(n), H, n)
    ri, _ = I.run(S.vine(n), H, n)
    if rp != ri:
        bad += 1
print('MISMATCH_EPISODES=' + str(bad))
"""

MUTS = {
    "M-WP1-01-skip-activation": ("python/liquidity/legacy_embedding.py", "ledger[i][0] = ACTIVE", "ledger[i][0] = LATENT"),
    "M-WP1-02-flip-zig": ("python/liquidity/legacy_embedding.py", '"case": "ZIG"', '"case": "ZIGX"'),
    "M-WP1-03-spend-latent": ("python/liquidity/legacy_embedding.py", "if rem > 0 and c[0] == ACTIVE:", "if rem > 0 and c[0] in (ACTIVE, LATENT):"),
    "M-WP1-04-activate-on-empty": ("python/liquidity/legacy_embedding.py", "for ev in evs:\n        before = active_pool(e[0])", "for ev in evs + [{'case': 'ZIG', 'lo': 1, 'hi': 2, 'orient': 'L'}]:\n        before = active_pool(e[0])"),
}


def main():
    print("[WP-1][STEP 33] Introducing engine mutants; each must be rejected")
    results = {}
    for mid, (rel, old, new) in MUTS.items():
        tmp = Path(tempfile.mkdtemp(prefix="wp1mut_"))
        shutil.copytree(ROOT / "python", tmp / "python")
        p = tmp / rel
        data = p.read_text(encoding="utf-8")
        assert old in data, (mid, "pattern missing")
        p.write_text(data.replace(old, new, 1), encoding="utf-8")
        probe = tmp / "probe.py"
        probe.write_text(PROBE % (str(tmp / "python"), str(ROOT / "python")), encoding="utf-8")
        r = subprocess.run([PY, str(probe)], capture_output=True, text=True)
        killed = "MISMATCH_EPISODES=" in (r.stdout or "") and not (r.stdout or "").strip().endswith("=0")
        results[mid] = "KILLED" if killed else "SURVIVED"
        print("[WP-1][STEP 33] %s: %s" % (mid, results[mid]))
        shutil.rmtree(tmp, ignore_errors=True)
    # NOTE: probe inserts mutant python FIRST, so mutant primary diverges from pristine independent.
    # M-WP1-02 caveat: ZIGX breaks event-class emission; differential records diverge via rA/rB (activation still fires
    # since p_all ignores class) — if it ever survives, LEG-06 (normalization) is the backstop detector.
    if any(v != "KILLED" for v in results.values()):
        print("[WP-1][STEP 33] SURVIVORS: %s" % [k for k, v in results.items() if v != "KILLED"])
        return 1
    print("[WP-1][STEP 33] ALL_4_KILLED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
