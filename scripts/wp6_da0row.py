"""Gate-I regression: H_y(B) = -R_B(y) + 4*(n-|sub(y)|) on da=0 rows.
Tests DA0-ROW: H(B)-H(B') >= D0(B) = R_B - 2(1-b). Expect 0 violations (theorem)."""
import sys, copy, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list

def subsize(T, x):
    nd = T
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    c = [0]
    def go(m):
        if m is None:
            return
        c[0] += 1
        go(m[1])
        go(m[2])
    go(nd)
    return c[0]

def main():
    import sys as _s
    import wp6_cycle_ratio as O
    ns = [int(x) for x in _s.argv[1:]] or [5, 6]
    out = {}
    for n in ns:
        Sh = O.shapes_of(list(range(1, n + 1)))
        nS = len(Sh)
        bad = 0
        tot = 0
        minslack = None
        maxslack = None
        tight = 0
        for ia in range(nS):
            for ib in range(nS):
                A, B = Sh[ia], Sh[ib]
                da = depths_list(A)
                for y in range(1, n + 1):
                    if da[y] != 0:
                        continue
                    rep = V.replay(A, B, [("K", y)])
                    Bp = rep["endB"]
                    R = R_static(B, y)
                    b = 1 if B[0] == y else 0
                    G = n - subsize(B, y)
                    Rp = R_static(Bp, y)
                    Gp = n - subsize(Bp, y)
                    D0 = R - 2 * (1 - b)
                    drop = (-R + 4 * G) - (-Rp + 4 * Gp)
                    slack = drop - D0
                    tot += 1
                    if slack < 0:
                        bad += 1
                        if bad <= 3:
                            print(f"[RG1] VIOL n={n} ia={ia} ib={ib} y={y} slack={slack} R={R} G={G} Rp={Rp} Gp={Gp} D0={D0}", flush=True)
                    else:
                        if minslack is None or slack < minslack:
                            minslack = slack
                        if maxslack is None or slack > maxslack:
                            maxslack = slack
                        if slack == 0:
                            tight += 1
        print(f"[RG1] n={n}: bad={bad}/{tot} minslack={minslack} maxslack={maxslack} tight={tight}", flush=True)
        out[n] = {"bad": bad, "tot": tot, "minslack": minslack,
                  "maxslack": maxslack, "tight": tight}
    json.dump(out, open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/da0row_reg.json", "w"), indent=1, default=str)
    return 0 if all(v["bad"] == 0 for v in out.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
