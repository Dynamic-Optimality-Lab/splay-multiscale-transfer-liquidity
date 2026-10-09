"""U4-core: bubble-concentration probe. One fat DELETE dethroner + many keys
each (DELETE-setup + starved KEEP). Many unit-bubbles sharing few fat pools.
BFS-close at n=6,7, charge + classify Q-2A."""
from __future__ import annotations
import sys
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
from wp6_ovf_anal import vine


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 131
    rng = random.Random(seed)
    import wp6_close as CL
    for n in (6, 7):
        T0 = vine(n)
        Sh, Atrans, Btrans = CL.build_trans(n) if n == 7 else (None, None, None)
        if n == 6:
            import wp6_cycle_ratio as O
            G = O.build(6)
            Sh, adj, nS = G["Sh"], G["adj"], G["nS"]
            vj = json.dumps(T0, sort_keys=True)
            vi = next(i for i, s in enumerate(Sh)
                      if json.dumps(s, sort_keys=True) == vj)
            u0 = vi * nS + vi
        else:
            nS = len(Sh)
            vj = json.dumps(T0, sort_keys=True)
            vi = next(i for i, s in enumerate(Sh)
                      if json.dumps(s, sort_keys=True) == vj)
            u0 = vi * nS + vi
        V.step("G-0", "n=%d u0=%d" % (n, u0))
        done = 0
        tries = 0
        while done < 6 and tries < 60:
            tries += 1
            keys = list(range(1, n + 1))
            rng.shuffle(keys)
            w0, xstar = keys[0], keys[1:]
            # build B-depth for each starved key (round-robin deep KEEPs)
            w = []
            for _ in range(rng.randint(2, 4)):
                rng.shuffle(keys)
                w += [("K", k) for k in keys]
            w += [("D", w0)]  # the shared fat dethroner
            for x in xstar:
                w += [("D", x)]  # setups (A-root each, B frozen)
            for x in xstar:
                w += [("K", x)]  # starved KEEPs?
            rep = V.replay(T0, T0, w)
            legs = rep["accesses"]
            nst = sum(1 for a in legs if a["m"] == "K" and a["a"] == 0
                      and a["q"] >= 1)
            if nst < 2:
                continue
            u_end = CL.state_of_word(nS, Atrans, Btrans, u0, w) \
                if n == 7 else None
            if n == 6:
                u = u0
                for (md, xk) in w:
                    for (to, md2, x2, _a, _b) in adj[u]:
                        if md2 == md and x2 == xk:
                            u = to
                            break
                u_end = u
                import wp6_danger as DG
                closer = DG.bfs_close(adj, u_end, u0)
            else:
                closer = CL.bfs_close(nS, Atrans, Btrans, u_end, u0, n)
            if closer is None:
                continue
            wc = w + closer
            r = S.cyclic_test(T0, T0, wc)
            rep2 = V.replay(T0, T0, wc + wc)
            L = len(wc)
            no = sum(1 for a in rep2["accesses"][L:] if a["eps"] > 0)
            done += 1
            V.step("G-1", "n=%d closed len=%d nstarved_open=%d lap2full=%s "
                   "A=%d Q=%d WQ=%d novf Steady=%d" %
                   (n, len(wc), nst, r["lap2full"], r["A"], r["Q"],
                    r["WQ"], no))
            if not r["lap2full"]:
                V.step("G-1", "  HALL=%s" % (r.get("hall"),))
    return 0


if __name__ == "__main__":
    sys.exit(main())
