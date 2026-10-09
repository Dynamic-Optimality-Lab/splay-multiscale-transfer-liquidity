"""PIVOT-25R-DISC collision ladder on access-UNPAID (n=5 exhaustive census).

Levels (all pre-state except T* trajectory levels):
 P0=(a,q,tw0); P1=+B summary (rootB,vineB,fuelB); P2=+A summary;
 T3=+orientation word; T4=+size sequences (expect ~zero: recomputation).
Ambiguity = same descriptor, different unpaid. Plus profile-shape census.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[DCL %s] %s" % (sid, msg), flush=True)


def main():
    Sh = O.shapes_of(list(range(1, 6)))
    nS = len(Sh)
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd, vn, md = {}, {}, {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])

        def is_vine(t):
            st = [t]
            while st:
                nd = st.pop()
                if nd is None:
                    continue
                if nd[1] is not None and nd[2] is not None:
                    return False
                st.append(nd[1])
                st.append(nd[2])
            return True

        def mxd(t):
            m = 0
            st = [(t, 0)]
            while st:
                nd, d = st.pop()
                if nd is None:
                    continue
                m = max(m, d)
                st.append((nd[1], d + 1))
                st.append((nd[2], d + 1))
            return m
        vn[ia] = is_vine(Sh[ia])
        md[ia] = mxd(Sh[ia])
    recs = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                       "0909c74a" / "dual_mine" /
                       "profiles5.json").read_text())["recs"]
    step("L", "records=%d" % len(recs))
    # profile-shape census
    from collections import Counter
    shape = Counter()
    for r in recs:
        if not r["dbl"]:
            shape["q0"] += 1
        elif r["minpref"] < 0:
            shape["borrower"] += 1
        else:
            shape["clean"] += 1
    step("P", "profiles: %s" % dict(shape))
    # ladders
    def keyP0(r):
        return (r["a"], r["q"], r["tw"][0])
    for name, fn in [
            ("P0", lambda r, i: keyP0(r)),
            ("P1", lambda r, i: (keyP0(r), rt[i[1]], vn[i[1]],
                                 md[i[1]] >= 4)),
            ("P2", lambda r, i: (keyP0(r), rt[i[1]], vn[i[1]],
                                 md[i[1]] >= 4, rt[i[0]], vn[i[0]],
                                 md[i[0]] >= 4)),
            ("T3", lambda r, i: (keyP0(r), tuple(d[0] for d in r["dbl"]))),
            ("T4", lambda r, i: (keyP0(r), tuple(
                (d[0], tuple(d[1])) for d in r["dbl"])))]:
        groups = defaultdict(list)
        for r, idx in zip(recs, [(r["ia"], r["ib"]) for r in recs]):
            groups[fn(r, idx)].append(r["unpaid"])
        amb = {k: v for k, v in groups.items() if len(set(v)) > 1}
        nev = sum(len(v) for v in amb.values())
        mx = max((max(v) - min(v) for v in amb.values()), default=0)
        step(name, "classes=%d amb=%d amb-events=%d maxspread=%s" %
             (len(groups), len(amb), nev, mx))
        if amb and name in ("P2", "T3"):
            k0 = min(amb, key=lambda k: len(amb[k]))
            step(name, "smallest amb class %s -> unpaid %s" %
                 (k0, sorted(set(amb[k0]))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
