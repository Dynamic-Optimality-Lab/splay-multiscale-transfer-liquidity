"""DIRECT-U1-05: archived coverage audit from FROZEN 26AS generator (no family change).

Regenerate closed words, select <=1000 per charter rule, classify with banked
recognizers, record W signs. Full AJ-AS audits (<=3) only for qualifiers."""
import sys, copy, json, itertools, importlib.util
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U1')
from collections import Counter

def load_banked(name, rel):
    spec = importlib.util.spec_from_file_location(
        name, str(Path('DO_RESEARCH_REBOOT/06_CERTIFICATES') / rel))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
AO = load_banked('aoB', '26AO/26AO_two_order_recognizer.py')
AP = load_banked('apB', '26AP/26AP_maximal_run_recognizer.py')
AQ = load_banked('aqB', '26AQ/26AQ_mixed_cyclic_dp_recognizer.py')
AR = load_banked('arB', '26AR/26AR_mixed_exact_cover_recognizer.py')
AS = load_banked('asB', '26AS/26AS_mixed_cyclic_recognizer.py')
spec = importlib.util.spec_from_file_location(
    'gen26AS', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS/26AS_fixed_witness_generator.py')
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

def canon_rot(word):
    rots = [tuple(word[i:] + word[:i]) for i in range(len(word))]
    return min(rots)

closed = {}
for name, sd in G.SEEDS.items():
    head0 = sd['cycle'][:6]; tail = sd['cycle'][6:]
    S0 = G.SEEDSTATE[name]['S0']; npre = G.SEEDSTATE[name]['npre']
    for tag, head in G.gen_heads(head0):
        st = G.SEEDSTATE[name]
        A = copy.deepcopy(st['A0']); B = copy.deepcopy(st['B0'])
        r1 = G.replay_pair(A, B, head, npre)
        if r1 is None:
            continue
        l1, s1, A, B = r1
        r2 = G.replay_pair(A, B, tail, npre + len(head))
        if r2 is None:
            continue
        l2, s2, A, B = r2
        if (G.pserial(A), G.pserial(B)) != S0:
            continue
        legs = l1 + l2
        words = head + tail
        Btmp = copy.deepcopy(st['B0'])
        for lg, (md, x) in zip(legs, words):
            if md == 'K':
                sb = G.pserial(Btmp)
                Btmp, _ = G.splay_B_push(Btmp, x)
                lg['_chg'] = (G.pserial(Btmp) != sb)
            else:
                lg['_chg'] = False
        bl = G.build_blocks(legs)
        if bl is None:
            continue
        W = sum(b['delta'] for b in bl)
        npos = sum(1 for b in bl if b['delta'] > 0)
        if npos == 0:
            continue
        # maximal +1 runs count
        runs = 0; i = 0; m = len(bl); ok = True
        while i < m:
            if bl[i]['delta'] == 1:
                runs += 1
                while i < m and bl[i]['delta'] == 1:
                    i += 1
            else:
                if bl[i]['delta'] > 1:
                    ok = False; break
                i += 1
        if not ok:
            continue
        key = (name, canon_rot(words))
        if key in closed:
            continue
        snaps = dict(s1); snaps.update(s2)
        closed[key] = {"seed": name, "tag": tag, "word": words, "W": W,
                       "npos": npos, "nruns": runs, "nblocks": m,
                       "blocks": bl, "snaps": snaps, "legs": legs}
print("distinct closed positive walks:", len(closed), flush=True)
Ws = Counter(w["W"] for w in closed.values())
print("W>0 count:", sum(1 for w in closed.values() if w["W"] > 0), flush=True)
print("W distribution:", dict(sorted(Ws.items())[:5]), "...", flush=True)
# selection per charter
sel = sorted(closed.values(),
             key=lambda w: (-w["nruns"], -w["npos"], w["nblocks"],
                            canon_rot(w["word"])))[:1000]
print("selected:", len(sel), flush=True)
json.dump([{"seed": w["seed"], "tag": w["tag"], "word": w["word"], "W": w["W"],
            "npos": w["npos"], "nruns": w["nruns"], "nblocks": w["nblocks"]}
           for w in sel],
          open(RDIR / 'DIRECT_U1_26AS_archive_selection.json', 'w'), indent=1)
# classify with banked recognizers
stat = Counter()
uncovered = []
for w in sel:
    bl, snaps = w["blocks"], w["snaps"]
    cov = []
    if AO.recognize(bl) and AO.recognize(bl).get("accepted"):
        cov.append("26AO")
    rp = AP.recognize(bl)
    if rp and rp.get("accepted"):
        cov.append("26AP")
    rq = AQ.recognize(bl)
    if rq and rq.get("accepted"):
        cov.append("26AQ")
    rr = AR.recognize(bl)
    if rr and rr.get("accepted"):
        cov.append("26AR")
    rs = AS.recognize(bl, snaps)
    if rs and rs.get("accepted"):
        cov.append("26AS")
    stat["n"] += 1
    w["covered_by"] = cov
    if cov:
        stat["banked_covered"] += 1
    else:
        stat["potentially_uncovered"] += 1
        uncovered.append(w)
print(dict(stat), flush=True)
json.dump({"n": stat["n"], "banked_covered": stat["banked_covered"],
           "potentially_uncovered": stat["potentially_uncovered"]},
          open(RDIR / 'DIRECT_U1_26AS_archive_coverage_audit.json', 'w'), indent=1)
json.dump([{"seed": w["seed"], "tag": w["tag"], "word": w["word"], "W": w["W"],
            "npos": w["npos"], "nruns": w["nruns"]} for w in uncovered[:20]],
          open(RDIR / 'DIRECT_U1_potentially_uncovered.json', 'w'), indent=1)
print("potentially uncovered (excl AR/AS so far):", len(uncovered), flush=True)
