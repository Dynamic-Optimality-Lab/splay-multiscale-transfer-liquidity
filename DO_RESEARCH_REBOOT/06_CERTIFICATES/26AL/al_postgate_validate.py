"""26AL post-gate: engine cross-check (21 transitions) + S-membership + novelty."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AL')
LOG = open(RDIR / 'al_postgate_validate.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush()
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
ev = load('wp6_eventflow')
adv = load('wp6_adv')
import splay as S
def to_tup(t):
    return S.LEAF if t is None else S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def tdep(t):
    out = {}
    def go(nd, d):
        if nd[0] == 'leaf':
            return
        _, k, l, r = nd
        out[k] = d
        go(l, d + 1)
        go(r, d + 1)
    go(t, 0)
    return out
def tser(t):
    return '.' if t[0] == 'leaf' else (t[1], tser(t[2]), tser(t[3]))
def pser(t):
    return '.' if t is None else (t['k'], pser(t.get('l')), pser(t.get('r')))
def vine(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
W = json.load(open(RDIR / "26AL_postgate_witness_replay.json"))
legs = W["legs"]
assert len(legs) == 17, "cycle has 17 accesses"
pre = [('D', 5), ('D', 7), ('D', 3), ('D', 2)]
word = [(l['m'], l['x']) for l in legs]
T0 = vine(7)
# ptr replay with per-transition capture
A = ev.to_ptr(copy.deepcopy(T0)); B = ev.to_ptr(copy.deepcopy(T0))
# tuple replay in lockstep
At, Bt = to_tup(copy.deepcopy(T0)), to_tup(copy.deepcopy(T0))
agree = 0
for i, (md, x) in enumerate(pre + word):
    dAp = adv.depths_of(copy.deepcopy(A)).get(x, -1)
    dBp = adv.depths_of(copy.deepcopy(B)).get(x, -1) if md == 'K' else None
    dAt = tdep(At).get(x, -1)
    dBt = tdep(Bt).get(x, -1) if md == 'K' else None
    ok = (dAp == dAt) and (dBp == dBt)
    A, _ = ev.splay_A(A, x)
    At, _ = S.trace(At, x)
    if md == 'K':
        B, _ = ev.splay_B_push(B, x)
        Bt, _ = S.trace(Bt, x)
    ok = ok and (pser(A) == tser(At)) and (pser(B) == tser(Bt))
    if ok:
        agree += 1
    else:
        log(f"[ALV] TRANSITION MISMATCH idx={i} {(md,x)}")
log(f"[ALV] engine agreement: {agree}/21 (need 21/21)")
assert agree == 21
cmp = {"transitions_compared": 21, "agree": agree}
json.dump(cmp, open(RDIR / "26AL_postgate_engine_comparison.json", "w"), indent=1)
# S-membership on cycle legs (indices 0..16 of `legs`)
cy = legs
m = len(cy)
leaders = [i for i in range(m) if cy[i]['a'] > 0]
assert leaders == list(range(m)), "all 17 accesses are leaders"
deltas = [l['q'] - 2 * l['a'] for l in cy]
pos = [i for i, d in enumerate(deltas) if d > 0]
log(f"[ALV] positive blocks: {pos} (need [0])")
assert pos == [0]
assert deltas[0] == 1 and deltas[1] == 0 and cy[2]['a'] >= 2
assert (deltas[0], deltas[1], deltas[2]) == (1, 0, -3)
x0, y0 = cy[0]['x'], cy[1]['x']
# former root r = B-root before access 0: replay prefix, read root
Ap, Bp = ev.to_ptr(copy.deepcopy(T0)), ev.to_ptr(copy.deepcopy(T0))
for (md, x) in pre:
    Ap, _ = ev.splay_A(Ap, x)
r0 = ev.root_key(Bp)
log(f"[ALV] former root r={r0} (need 1); x={x0} y={y0}")
assert r0 == 1 and x0 == 7 and y0 == 5
assert (r0 - x0) * (y0 - x0) > 0, "same-side"
assert cy[1]['rb'] == x0, "B-root==x at intervening KEEP"
# h = depth of r after block0: replay prefix + access0 on B
Bh = ev.to_ptr(copy.deepcopy(T0))
_, _ = ev.splay_A(ev.to_ptr(copy.deepcopy(T0)), 0) if False else (None, None)
for (md, x) in pre:
    pass
Bh, _ = ev.splay_B_push(Bh, 7)
h = adv.depths_of(copy.deepcopy(Bh)).get(1, -1)
log(f"[ALV] h=depth(r) after block0: {h} (need 0..2)")
assert 0 <= h <= 2
assert cy[1]['dB'] is not None and cy[1]['dB'] > 0, "genuine intervening B splay"
ci = (h + 2) // 2
assert deltas[0] <= (2 * cy[1]['a'] - cy[1]['q']) + (2 * cy[2]['a'] - ci), "G-capacity"
# q at delayed access + capacity + disjointness(global single positive already)
assert cy[2]['x'] == r0
log(f"[ALV] delayed access key ok; q2={cy[2]['q']} a2={cy[2]['a']}")
assert cy[2]['q'] - 2 * cy[2]['a'] <= -2
# novelty: successor != r
assert cy[1]['x'] != r0
# B-depth at positive access
assert cy[0]['dB'] == 6, "B-depth 6 (outside depth-5)"
log("[ALV] S-MEMBERSHIP + NOVELTY PRECHECKS ALL PASS")
LOG.close()
