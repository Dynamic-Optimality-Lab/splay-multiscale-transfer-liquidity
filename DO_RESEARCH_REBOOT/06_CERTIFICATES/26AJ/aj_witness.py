"""26AJ witness: seven-key closed walk vs authoritative engine + lemma probe."""
import sys, copy, json, random
sys.path.insert(0, 'scripts')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AJ')
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
ev = load('wp6_eventflow')
adv = load('wp6_adv')
cd = load('wp6_coarse_double')
def serial(t):
    if t is None: return '.'
    return (t['k'], serial(t.get('l')), serial(t.get('r')))
def vine(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
T0 = vine(7)
A = ev.to_ptr(copy.deepcopy(T0)); B = ev.to_ptr(copy.deepcopy(T0))
def step(md, x):
    global A, B
    assert adv.depths_of(copy.deepcopy(A)).get(x, None) is not None
    assert adv.depths_of(copy.deepcopy(B)).get(x, None) is not None
    dA = adv.depths_of(copy.deepcopy(A)).get(x, 0)
    a = (dA + 1) // 2
    if md == 'K':
        dB = adv.depths_of(copy.deepcopy(B)).get(x, 0)
        q, z = dB // 2, dB % 2
    else:
        dB = None; q = z = 0
    A, _ = ev.splay_A(A, x)
    if md == 'K':
        B, _ = ev.splay_B_push(B, x)
    return {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q, "z": z}
prefix = [('D', 7), ('D', 6)]
word = [('K', 7), ('K', 1), ('K', 4), ('K', 5), ('K', 3), ('K', 1), ('D', 7), ('D', 6)]
for md, x in prefix:
    step(md, x)
A1, B1 = serial(A), serial(B)
legs = [step(md, x) for (md, x) in word]
A2, B2 = serial(A), serial(B)
print(f"[AJ] closed A: {A1 == A2}, closed B: {B1 == B2}", flush=True)
exp = [(1, 3, 1), (2, 1, -3), (2, 1, -3), (1, 1, -1), (2, 2, -2), (1, 1, -1), (3, 0, -6), (2, 0, -4)]
ok = True
for i, l in enumerate(legs):
    e = exp[i]
    good = (l['a'], l['q'], l['q'] - 2 * l['a']) == e
    ok = ok and good
    if not good: print(f"[AJ] MISMATCH leg {i}: got {(l['a'],l['q'],l['q']-2*l['a'])} want {e}", flush=True)
print(f"[AJ] cost table matches: {ok}", flush=True)
A3 = sum(l['a'] for l in legs); Q3 = sum(l['q'] for l in legs)
print(f"[AJ] totals A={A3} Q={Q3} W={Q3-2*A3} (expect 14/9/-19)", flush=True)
print(f"[AJ] max dB in cycle: {max(l['dB'] for l in legs if l['dB'] is not None)} (expect 6)", flush=True)
# cross-check vs authoritative replay() on concatenated word (same engine + formulas)
ref = cd.replay(copy.deepcopy(T0), prefix + word)
rl = ref["legs"][len(prefix):]
same = len(rl) == len(legs) and all((rl[i]["a"], rl[i]["q"], rl[i]["z"], rl[i]["dA"], rl[i].get("dB")) ==
           (legs[i]["a"], legs[i]["q"], legs[i]["z"], legs[i]["dA"], legs[i]["dB"]) for i in range(len(legs)))
print(f"[AJ] replay() cross-check identical: {same}", flush=True)
# block partition (cyclic leaders a>0)
m = len(legs)
leaders = [i for i in range(m) if legs[i]['a'] > 0]
print(f"[AJ] leaders at {leaders} (expect all 8: all a>=1)", flush=True)
# per-block: single key, <=1 nontrivial B KEEP, deficits, successor condition
def blocks():
    bs = []
    L = sorted(leaders)
    for k, s in enumerate(L):
        e = L[(k + 1) % len(L)]
        idx = []
        i = s
        while True:
            idx.append(i)
            if (i + 1) % m == e:
                break
            i = (i + 1) % m
        bs.append(idx)
    return bs
bs = blocks()
deltas = []
for b in bs:
    ks = {legs[i]['x'] for i in b}
    nk = sum(1 for i in b if legs[i]['m'] == 'K' and (legs[i]['dB'] or 0) > 0)
    dd = sum(legs[i]['q'] - 2 * legs[i]['a'] for i in b)
    deltas.append(dd)
    assert len(ks) == 1, ks
    assert nk <= 1, nk
print(f"[AJ] blocks single-key + <=1 nontrivial KEEP each: True; deficits={deltas}", flush=True)
print(f"[AJ] former-root depth after block0 splay (legs[1] dB<=2): {legs[1]['dB']}", flush=True)
pos = [i for i, d in enumerate(deltas) if d > 0]
print(f"[AJ] positive blocks: {pos} (expect [0] with delta=+1)", flush=True)
# former-root checks for block 0: replay B1 state to first KEEP
# B after prefix = T0 (DELETEs freeze B); B-root before KEEP7:
Bpre = ev.to_ptr(vine(7))
print(f"[AJ] B-root before KEEP7: {ev.root_key(Bpre)} (expect 1... check table premise)", flush=True)
out = {"closed_A": A1 == A2, "closed_B": B1 == B2, "costs_match": ok,
       "totals": [A3, Q3, Q3 - 2 * A3], "legs": legs}
json.dump(out, open(RDIR / "26AJ_witness_replay.json", "w"), indent=1, default=str)
# former-root depth lemma falsification probe (both engines)
import wp6_cycle_ratio as O
bad = 0; worst = 0; tried = 0
rng = random.Random(7)
for n in range(1, 10):
    for T in O.shapes_of(list(range(1, n + 1)))[:40]:
        for fn in (ev.splay_A, ev.splay_B_push):
            for x in range(1, n + 1):
                t = ev.to_ptr(copy.deepcopy(T))
                r0 = ev.root_key(t)
                t2, _ = fn(t, x)
                d = adv.depths_of(copy.deepcopy(t2)).get(r0, 999)
                tried += 1
                worst = max(worst, d)
                if d > 2:
                    bad += 1
                    if bad < 4: print(f"[AJ] VIOLATION n={n} x={x} oldroot={r0} depth={d}", flush=True)
print(f"[AJ] depth-lemma probe: tried={tried} violations={bad} maxdepth={worst}", flush=True)
json.dump({"tried": tried, "violations": bad, "maxdepth": worst}, open(RDIR / "26AJ_depth_lemma_probe.json", "w"), indent=1)
print("[AJ] done", flush=True)
