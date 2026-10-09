"""Gate-II finite test: residual identity D_KEEP=D0+D_DEL + ROW-SWITCH
H_r(B)-H_x(B) >= D_DEL with H=-R+kappa*G. Kappa scan for feasible interval."""
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
    args = _s.argv[1:]
    ns = [int(a) for a in args if not a.startswith("k=")] or [5]
    kappas = [float(a[2:]) for a in args if a.startswith("k=")] or [4.0]
    out = {}
    for n in ns:
        Sh = O.shapes_of(list(range(1, n + 1)))
        nS = len(Sh)
        # §20 identity check + row-switch per kappa
        idbad = 0
        idtot = 0
        rows = []  # (Hr-Hx, DDEL, a, br, bx, Rr, Rx, Gr, Gx)
        for ia in range(nS):
            for ib in range(nS):
                A, B = Sh[ia], Sh[ib]
                r = A[0]
                da = depths_list(B)
                br = 1 if da.get(r) == 0 else 0  # careful: root(B)==r?
                br = 1 if B[0] == r else 0
                for x in range(1, n + 1):
                    daA = depths_list(A)
                    a = (daA[x] + 1) // 2
                    t = 1 if A[0] == B[0] else 0
                    Dk = R_static(B, x) - 2 * a - 2 * (1 - t)
                    D0 = R_static(B, x) - 2 * (1 - (1 if B[0] == x else 0))
                    # D_DEL = -2a -2(bx-br)
                    bx = 1 if B[0] == x else 0
                    Dd = -2 * a - 2 * (bx - br)
                    idtot += 1
                    if Dk != D0 + Dd:
                        idbad += 1
                        if idbad <= 3:
                            print(f"[RSI] IDENTITY VIOL n={n} ia={ia} ib={ib} x={x}: Dk={Dk} D0={D0} Dd={Dd}", flush=True)
                    # row-switch quantities (B-only + A scalars)
                    Rr = R_static(B, r)
                    Rx = R_static(B, x)
                    Gr = n - subsize(B, r)
                    Gx = n - subsize(B, x)
                    rows.append((Rr, Rx, Gr, Gx, a, br, bx, Dd))
        print(f"[RSI] n={n}: identity bad={idbad}/{idtot}", flush=True)
        out[n] = {"idbad": idbad, "idtot": idtot}
        for ka in kappas:
            bad = 0
            tot = 0
            minslack = None
            worst = None
            for (Rr, Rx, Gr, Gx, a, br, bx, Dd) in rows:
                drop = (-Rr + ka * Gr) - (-Rx + ka * Gx)
                slack = drop - Dd
                tot += 1
                if slack < 0:
                    bad += 1
                    if worst is None or slack < worst[0]:
                        worst = (slack, Rr, Rx, Gr, Gx, a, br, bx, Dd)
                elif minslack is None or slack < minslack:
                    minslack = slack
            print(f"[RSW] n={n} kappa={ka}: bad={bad}/{tot} minslack={minslack} worst={worst}", flush=True)
            out[n][f"k{ka}"] = {"bad": bad, "tot": tot,
                                "minslack": minslack, "worst": worst}
    json.dump(out, open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/rowswitch.json", "w"), indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
