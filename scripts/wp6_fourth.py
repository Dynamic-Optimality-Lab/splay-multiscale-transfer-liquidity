"""WP-6 STEP FT-00: fourth-use ascent + episode-tax probe (reuse-growth attack).

For each history, Q = full-B and tight-Qs (min-cut/access/K slices):
  per source a with deg_Q(a) >= 4:
    first_Q(a) (earliest B-index in Q adjacent);
    companion? exists c != a in N(Q) with first_Q(c) > first_Q(a) (strict);
    pure-W? rotated(a) disjoint from ALL neighbor splay-keys;
    episodes = distinct neighbor accesses (splays); later-nonrepeat-episode?
    class of a at first neighbor (E1/E2/E3/W/E4/K/E7 by tagged sets).
  ASCENT verdict per source; failures classified by class (§27.8).
  W-tax check: pure-W + deg>=4 => multi-episode? later-nonrepeat? companion?
  REPEAT-HOLE hunt: pure-W deg>=4 with all later episodes at repeat-accesses
  (E1 empty) + E4-early + no dormant-returners => persist hole witness.
Kill: Delta(Q)>=1 on any tested Q (hallkill + §24 path).
NEW artifact: fourth.json (+hallkill.json on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_eventflow_abl import build_tagged
from wp6_tightest import vine, Rng, H_walk
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


from collections import defaultdict


def analyze_Q(n, T0, H, Q, G=None, aux=None):
    """Returns per-deg>=4-source records + ascent verdicts."""
    if G is None:
        G = build_graph(n, T0, H)
        if G is None:
            return None
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre = G["pre"]
    if aux is None:
        aux = build_aux(n, T0, pre)
    Arot, acc_of = aux
    Q = sorted(Q)
    N = set()
    for j in Q:
        N |= G["adj"][j]
    first = {}
    for i in N:
        for j in Q:
            if i in G["adj"][j]:
                first[i] = j
                break
    recs = []
    for i in N:
        # degree within Q
        nbrs = [j for j in Q if i in G["adj"][j]]
        if len(nbrs) < 4:
            continue
        # incidence mix: E3-only neighbors (eligible ONLY via E3 at that B-event)
        e3only = 0
        for j in nbrs:
            e = G["elig"][j]
            inE3 = i in e["E3"]
            inother = (i in e["E1"]) or (i in e["E2"]) or (i in e["E4"]) or (i in e["E7"])
            if inE3 and not inother:
                e3only += 1
        # K-inc vs W-inc split, incidence-exact:
        #   K-inc(b): x_b in S(a) with ai<=acc(b), sited (complete per access).
        #   W-inc(b): x_b NOT in S(a) but a in E3(b) (transient overlap only).
        #   W-inc per splay <= |S| <= 3 by OCCUPANCY (each z in S in <=1 triple).
        #   others (E1/E2/E4/E7-nonE3): complete-class, no forcing.
        S = Arot.get(i, frozenset())
        ai, sited = Aevs[i]
        kinc = 0
        winc = 0
        for j in nbrs:
            e = G["elig"][j]
            xx = pre[Bevs[j][0]]["x"]
            accb = Bevs[j][0]
            if S and xx in S and ai <= accb and sited:
                kinc += 1
            elif xx not in S and (i in e["E3"]):
                winc += 1
        # pure-W? rotated(a) disjoint from ALL neighbor splay-keys AND E3-only>0
        xkeys = set(pre[Bevs[j][0]]["x"] for j in nbrs)
        pureW = S.isdisjoint(xkeys) and winc > 0
        eps = sorted(set(Bevs[j][0] for j in nbrs))
        # later nonrepeat episode?
        f0 = first[i]
        laterep = []
        for a in eps:
            if a <= Bevs[f0][0]:
                continue
            eA = sum(1 for z in pre[a]["sites"] if z)
            laterep.append((a, eA > 0))
        # companion?
        comp = [c for c in N if c != i and first.get(c, -1) > f0]
        # class at first neighbor
        e = G["elig"][f0]
        cls = sorted(k for k in e if i in e[k])
        recs.append({"aev": i, "ai": Aevs[i][0], "deg": len(nbrs),
                     "e3only": e3only, "kinc": kinc, "winc": winc,
                     "first": f0, "pureW": pureW, "episodes": eps,
                     "later_ep": laterep,
                     "companion": bool(comp), "ncomp": len(comp),
                     "cls": cls})
    return recs


def build_aux(n, T0, pre):
    from wp6_eventflow import to_ptr, splay_A, splay_B_push
    A, B = to_ptr(T0), to_ptr(T0)
    Arot = {}
    acc_of = {}
    aid = 0
    for idx, acc in enumerate(pre):
        A, invs = splay_A(A, acc["x"])
        for (S, sited) in zip(invs, acc["sites"]):
            Arot[aid] = frozenset(S)
            acc_of[aid] = idx
            aid += 1
        if acc["mode"] == "KEEP":
            B, _ = splay_B_push(B, acc["x"])
    return Arot, acc_of


def main() -> int:
    step("FT-00", "Fourth-use ascent + episode-tax probe")
    import json
    from collections import Counter
    ascfail = Counter()
    asctot = Counter()
    pureW_multi = 0
    pureW_single = 0
    e3only4_multi = 0
    e3only4_nocomp = 0
    winc4 = 0
    winc4_multi = 0
    winc4_nocomp = 0
    rephole = 0
    rephole_ex = []
    e2k_multi = 0
    e2k_nocomp = 0
    holes = []
    holes_e3 = []
    ndeg4 = 0
    nQ = 0
    for t in range(200):
        tag = b"ft" if t % 2 == 0 else b"ft2"
        rng = Rng(("s%d" % t).encode(), tag)
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % t).encode(), tag + b"h")
        H = H_walk(rr, n, 12 + (r >> 16) % 20, 1 + (r >> 24) % n)
        G = build_graph(n, T0, H)
        if G is None:
            continue
        f, nb, lv = maxflow_cap3(G)
        if nb - f > 0:
            step("FT-KILL", "HALL t=%d" % t)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        # Q variants: full-B + per-access slices
        byacc = defaultdict(list)
        for j in range(nb):
            byacc[G["Bevs"][j][0]].append(j)
        Qs = [list(range(nb))] + list(byacc.values())
        aux = None
        for Q in Qs:
            d, N = delta_of(G, set(Q))
            if d > 0:
                step("FT-KILL", "HALL-Q t=%d" % t)
                return 2
            if aux is None:
                aux = build_aux(n, T0, G["pre"])
            recs = analyze_Q(n, T0, H, Q, G, aux)
            nQ += 1
            for rc in recs:
                ndeg4 += 1
                key = "|".join(rc["cls"]) if rc["cls"] else "?"
                asctot[key] += 1
                if not rc["companion"]:
                    ascfail[key] += 1
                if rc["pureW"]:
                    # multi-episode? episodes list length>1
                    if len(rc["episodes"]) > 1:
                        pureW_multi += 1
                    else:
                        pureW_single += 1
                if rc["e3only"] >= 4:
                    # E3-only incidences force multi-splay (STEPS<=3/splay): check episodes
                    if len(rc["episodes"]) > 1:
                        e3only4_multi += 1
                    if not rc["companion"]:
                        e3only4_nocomp += 1
                        if len(holes_e3) < 10:
                            holes_e3.append({"t": t, "Qkind": ("full" if len(Q) == nb else "acc"),
                                             "rec": rc, "H": H, "n": n, "kind": "e3only4-nocomp"})
                        continue
                # W-incidence tax: pure-transient (S disjoint from neighbor keys)
                # incidences are <=3 per splay (OCC); >=4 forces multi-episode.
                if rc["winc"] >= 4:
                    winc4 += 1
                    if len(rc["episodes"]) > 1:
                        winc4_multi += 1
                    if not rc["companion"]:
                        winc4_nocomp += 1
                        if len(holes_e3) < 14:
                            holes_e3.append({"t": t, "Qkind": ("full" if len(Q) == nb else "acc"),
                                             "rec": rc, "H": H, "n": n, "kind": "winc4-nocomp"})
                # REPEAT-HOLE: W-inc>=4, multi-episode, ALL later episodes at
                # repeat-accesses (same key as previous access => E1 empty).
                first_acc = min(rc["episodes"]) if rc["episodes"] else None
                later_eps = [a for a in rc["episodes"] if first_acc is not None and a > first_acc]
                if rc["winc"] >= 4 and len(rc["episodes"]) > 1 and later_eps:
                    allrep = all(a > 0 and H[a][1] == H[a - 1][1] for a in later_eps)
                    if allrep and not rc["companion"]:
                        rephole += 1
                        if len(rephole_ex) < 8:
                            rephole_ex.append({"t": t, "rec": rc, "H": H, "n": n})
                # E2/K-EPISODE-TAX: K-incidence>0 (or E2-class) + multi-access
                # episodes -> companion?
                if rc["kinc"] > 0 and len(rc["episodes"]) > 1:
                    e2k_multi += 1
                    if not rc["companion"]:
                        e2k_nocomp += 1
                if not rc["companion"] and len(holes) < 10:
                    holes.append({"t": t, "Qkind": ("full" if len(Q) == nb else "acc"),
                                  "rec": rc, "H": H, "n": n, "kind": "nocomp"})
    step("FT-01", "Q=%d deg4=%d ascent-fail=%s" % (nQ, ndeg4, dict(ascfail)))
    step("FT-02", "ascent-tot=%s pureW multi=%d single=%d e3only4: multi=%d nocomp=%d winc4=%d multi=%d nocomp=%d" % (
        dict(asctot), pureW_multi, pureW_single, e3only4_multi, e3only4_nocomp,
        winc4, winc4_multi, winc4_nocomp))
    step("FT-03", "repeat-hole=%d e2k-episode: multi=%d nocomp=%d" % (rephole, e2k_multi, e2k_nocomp))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "fourth.json").write_text(
        json.dumps({"Q": nQ, "deg4": ndeg4, "ascent_fail": dict(ascfail),
                    "ascent_tot": dict(asctot), "pureW_multi": pureW_multi,
                    "pureW_single": pureW_single, "e3only4_multi": e3only4_multi,
                    "e3only4_nocomp": e3only4_nocomp, "winc4": winc4,
                    "winc4_multi": winc4_multi, "winc4_nocomp": winc4_nocomp,
                    "rephole": rephole, "rephole_ex": rephole_ex,
                    "e2k_multi": e2k_multi, "e2k_nocomp": e2k_nocomp,
                    "holes": (holes_e3 + holes)[:14]},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
