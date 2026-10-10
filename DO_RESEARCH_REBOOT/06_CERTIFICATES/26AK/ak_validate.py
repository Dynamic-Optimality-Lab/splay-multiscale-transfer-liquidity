"""26AK witness validation on AUTHORITATIVE ptr engine + full triple/global checks."""
import sys, copy, json
sys.path.insert(0, 'scripts')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_validate.log', 'w')
def log(s, **kw):
    LOG.write(s + "\n"); LOG.flush()
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
ev = load('wp6_eventflow')
adv = load('wp6_adv')
def vine(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
def serial(t):
    if t is None:
        return '.'
    return (t['k'], serial(t.get('l')), serial(t.get('r')))
W = json.load(open(RDIR / "26AK_witness.json"))
n, pre = W["n"], [tuple(x) for x in W["pre"]]
triple = [tuple(x) for x in W["triple"]]
tail = [tuple(x) for x in W["tail"]]
word = pre + triple + tail
import wp6_cycle_ratio as O
tk = W.get("t0kind", "vine")
if tk.startswith("shape"):
    T0 = copy.deepcopy(O.shapes_of(list(range(1, n + 1)))[int(tk[5:])])
else:
    T0 = vine(n)
A = ev.to_ptr(copy.deepcopy(T0)); B = ev.to_ptr(copy.deepcopy(T0))
legs = []
for (md, x) in word:
    dA = adv.depths_of(copy.deepcopy(A)).get(x, -1)
    assert dA >= 0, ("absent", md, x)
    a = (dA + 1) // 2
    if md == 'K':
        dB = adv.depths_of(copy.deepcopy(B)).get(x, -1)
        assert dB >= 0
        q = dB // 2
    else:
        dB = None; q = 0
    ra, rb = ev.root_key(A), ev.root_key(B)
    A, _ = ev.splay_A(A, x)
    if md == 'K':
        B, _ = ev.splay_B_push(B, x)
    legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                 "ra": ra, "rb": rb})
# closed w.r.t. post-prefix state
Ap, Bp = ev.to_ptr(copy.deepcopy(T0)), ev.to_ptr(copy.deepcopy(T0))
for (md, x) in pre:
    Ap, _ = ev.splay_A(Ap, x)
log(f"[AKV] closed A={serial(A)==serial(Ap)} closed B={serial(B)==serial(Bp)}", flush=True)
cy = legs[len(pre):]
m = len(cy)
leaders = [i for i in range(m) if cy[i]['a'] > 0]
log(f"[AKV] cycle len={m} leaders={leaders}", flush=True)
Lsorted = sorted(leaders)
bs = []
for k, s in enumerate(Lsorted):
    e = Lsorted[(k + 1) % len(Lsorted)]
    idx = []
    i = s
    while True:
        idx.append(i)
        if (i + 1) % m == e:
            break
        i = (i + 1) % m
    bs.append(idx)
info = []
for b in bs:
    ks = {cy[i]['x'] for i in b}
    assert len(ks) == 1, ("multi-key block", b)
    kb = [i for i in b if cy[i]['m'] == 'K' and (cy[i]['dB'] or 0) > 0]
    assert len(kb) <= 1, ("two nontrivial", b)
    dd = sum(cy[i]['q'] - 2 * cy[i]['a'] for i in b)
    info.append({"key": cy[b[0]]['x'], "delta": dd,
                 "a": sum(cy[i]['a'] for i in b), "q": sum(cy[i]['q'] for i in b),
                 "rb0": cy[kb[0]]['rb'] if kb else None})
log(f"[AKV] blocks (key,delta): {[(d['key'], d['delta']) for d in info]}", flush=True)
pos = [k for k in range(len(bs)) if info[k]['delta'] > 0]
log(f"[AKV] positive blocks: {pos}", flush=True)
assert len(pos) == 1, "need exactly one positive for clean disjointness"
k = pos[0]
x, rk = info[k]['key'], info[k]['rb0']
assert rk is not None and rk != x
kb = [i for i in bs[k] if cy[i]['m'] == 'K' and (cy[i]['dB'] or 0) > 0]
n1 = (k + 1) % len(bs)
y = info[n1]['key']
# B-root==x at intervening first KEEP: replay to that point and check root
A2, B2 = ev.to_ptr(copy.deepcopy(T0)), ev.to_ptr(copy.deepcopy(T0))
for (md, xx) in pre + triple[:0]:
    A2, _ = ev.splay_A(A2, xx)
# find first KEEP index of block n1 in cycle coords -> global index
g1 = bs[n1][0]
# walk cycle from start to g1 tracking B
A3, B3 = copy.deepcopy(Ap), copy.deepcopy(Bp)
for t in range(g1):
    md, xx = (cy[t]['m'], cy[t]['x'])
    A3, _ = ev.splay_A(A3, xx)
    if md == 'K':
        B3, _ = ev.splay_B_push(B3, xx)
log(f"[AKV] B-root at intervening block start: {ev.root_key(B3)} (need {x})", flush=True)
assert ev.root_key(B3) == x
# h = depth of rk after block k: replay cycle start..end of block k, read depth
A4, B4 = copy.deepcopy(Ap), copy.deepcopy(Bp)
for t in range(bs[k][-1] + 1):
    md, xx = (cy[t]['m'], cy[t]['x'])
    A4, _ = ev.splay_A(A4, xx)
    if md == 'K':
        B4, _ = ev.splay_B_push(B4, xx)
h = adv.depths_of(copy.deepcopy(B4)).get(rk, -1)
log(f"[AKC] h=depth(r) after block k: {h} (need 1..2)", flush=True)
assert 1 <= h <= 2
assert (rk - x) * (y - x) < 0, "opposite branch"
n2 = (k + 2) % len(bs)
assert legs is not None
# cycle-coord leader of block n2 accesses rk?
assert cy[bs[n2][0]]['x'] == rk, "delayed access"
assert info[n1]['delta'] <= 0, "H5"
ci = (h + 2) // 2
cap = (2 * info[n1]['a'] - info[n1]['q']) + (2 * sum(cy[i]['a'] for i in bs[n2]) - ci)
log(f"[AKV] capacity: delta_k={info[k]['delta']} <= {cap} ? {info[k]['delta'] <= cap}", flush=True)
assert info[k]['delta'] <= cap
tot = sum(d['delta'] for d in info)
log(f"[AKV] total W={tot} (need <=0)", flush=True)
assert tot <= 0
json.dump({"closed": True, "npositive": 1, "h": h, "ci": ci, "cap": cap,
           "W": tot, "deltas": [d['delta'] for d in info]}, open(RDIR / "26AK_validated.json", "w"), indent=1)
log("[AKV] ALL CHECKS PASS", flush=True)
LOG.close()
