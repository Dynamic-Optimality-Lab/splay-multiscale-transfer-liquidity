"""WP-6 VARHOLE: variation-emptiness hunt — the TRUE hole atom (C61).

Atom: B-heavy access (e_B > 3f) with E1-EMPTY (repeat/trivial-A) AND new-old = 0,
where new = sources adjacent at this access never adjacent at any earlier access.
Such an atom adds demand with ZERO new supply (pure stock-sharing). Sustained atoms
sharing capped stock = kill. Pressure-17 counted stock<=2 (not new); this counts new.
If atoms never occur over 100k+ accesses, variation holds finitely-strong.
Also record: heavy+E1empty with new>0 distribution (how much new typically).
Artifact: varhole.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3
from wp6_tightest import vine, Rng
from solver import encode as E


def step(sid, msg):
    print("[WP-6][VARHOLE %s] %s" % (sid, msg), flush=True)


from collections import defaultdict, Counter


def main() -> int:
    import json
    step("VH-00", "variation-emptiness hunt")
    heavy = 0
    heavy_e1empty = 0
    atoms = 0
    newdist = Counter()
    atomex = []
    kill = 0
    access_total = 0
    cfgs = [(b"vh1", [16, 32, 64], 8, 24), (b"vh2", [64, 128], 10, 30), (b"vh3", [8, 24, 48], 10, 28)]
    for tag, nset, Llo, Lhi in cfgs:
        for t in range(120):
            rng = Rng(("v%d" % t).encode(), tag)
            r = rng(0)
            n = nset[r % len(nset)]
            T0 = vine(n, (r >> 8) % 2 == 0)
            L = Llo + (r >> 16) % (Lhi - Llo + 1)
            x = 1 + (r >> 24) % n
            H = []
            for i in range(L):
                rr = Rng(("v%d" % t).encode(), tag + b"h%d" % i)
                q = rr(1000 + i)
                if i % 5 == 4:
                    y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
                    H.append(["DELETE", y if y != x else 1])
                    H.append(["KEEP", x])
                else:
                    H.append(["KEEP" if q % 3 else "DELETE", x])
                x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
            G = build_graph(n, T0, H)
            if G is None:
                continue
            f, nb, _ = maxflow_cap3(G)
            if nb - f > 0:
                kill += 1
                continue
            Aevs, Bevs = G["Aevs"], G["Bevs"]
            pre = G["pre"]
            byacc = defaultdict(list)
            for j in range(len(Bevs)):
                byacc[Bevs[j][0]].append(j)
            seenN = set()
            for acc in sorted(byacc):
                js = byacc[acc]
                access_total += 1
                e = G["elig"][js[0]]
                E1s = set(i for i in e["E1"] if Aevs[i][1])
                E4s = set(i for i in e["E4"] if Aevs[i][1])
                f_ = len(E4s) if (acc > 0 and pre[acc - 1]["x"] == pre[acc]["x"]) else len(E1s)
                Nacc = set()
                for j in js:
                    Nacc |= G["adj"][j]
                new = Nacc - seenN
                seenN |= Nacc
                if len(js) > 3 * f_:
                    heavy += 1
                    if len(E1s) == 0:
                        heavy_e1empty += 1
                        newdist[len(new)] += 1
                        if len(new) == 0:
                            atoms += 1
                            if len(atomex) < 10:
                                atomex.append({"t": t, "tag": tag.decode(), "n": n, "acc": acc,
                                               "x": pre[acc]["x"], "eB": len(js), "N": len(Nacc)})
    step("VH-01", "access=%d heavy=%d heavyE1empty=%d ATOMS=%d kills=%d" % (
        access_total, heavy, heavy_e1empty, atoms, kill))
    step("VH-02", "newdist@heavyE1empty=%s ex=%s" % (dict(sorted(newdist.items())), atomex[:4]))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "varhole.json").write_text(
        json.dumps({"access": access_total, "heavy": heavy, "heavyE1empty": heavy_e1empty,
                    "atoms": atoms, "kills": kill, "newdist": dict(sorted(newdist.items())),
                    "atomex": atomex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 2 if kill else 0


if __name__ == "__main__":
    sys.exit(main())
