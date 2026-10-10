"""26AK constructive triple + BFS closure. Tuple engine for search."""
import sys, copy, json, random
from collections import deque
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AK')
LOG = open(RDIR / 'ak_close.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush()
import wp6_cycle_ratio as O
import splay as S
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def depths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d
        go(l, d + 1)
        go(r, d + 1)
    go(t, 0)
    return out
def serial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, serial(l), serial(r))
def step_state(A, B, md, x):
    dA = depths(A).get(x, -1)
    if dA < 0:
        return None
    a = (dA + 1) // 2
    if md == 'K':
        dB = depths(B).get(x, -1)
        if dB < 0:
            return None
        q = dB // 2
    else:
        dB = None; q = 0
    ra, rb = A[1], B[1]
    A2, _ = S.trace(A, x)
    if md == 'K':
        B2, _ = S.trace(B, x)
    else:
        B2 = B
    return (A2, B2, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "ra": ra, "rb": rb})
def vine(n):
    t = S.LEAF
    for k in range(n, 0, -1):
        t = S.node(k, S.LEAF, t)
    return t
# FIXED constructive triple on n=9 vine: prefix D9,D8; K7(pos); K8(interv); K1(delayed)
n = 9
T0 = vine(n)
A, B = T0, T0
hist = []
for (md, x) in [('D', 9), ('D', 8)]:
    r = step_state(A, B, md, x)
    A, B = r[0], r[1]
S0 = (serial(A), serial(B))
for (md, x) in [('K', 7), ('K', 8), ('K', 1)]:
    r = step_state(A, B, md, x)
    hist.append(r[2])
    A, B = r[0], r[1]
log(f"[AKC] triple legs: {[(h['m'],h['x'],h['dA'],h['dB'],h['a'],h['q']) for h in hist]}")
# verify triple structure: block0 positive; former root; opposite; genuine; delayed
d0 = hist[0]['q'] - 2 * hist[0]['a']
log(f"[AKC] block0 delta={d0} (need >0); former root rb={hist[0]['rb']} (need !=7)")
# B-root==7 at intervening KEEP?
log(f"[AKC] rb at KEEP8 = {hist[1]['rb']} (need 7 for genuine+lemma scope)")
# BFS tail from current (A,B) back to S0
start = (serial(A), serial(B))
log(f"[AKC] start==S0 already? {start == S0}")
target = S0
prev = {start: None}
act = {start: None}
dq = deque([start])
states = {start: (A, B)}
found_tail = None
expanded = 0
NODECAP = 400000
while dq and expanded < NODECAP:
    s = dq.popleft()
    Acur, Bcur = states[s]
    if s == target and s != start:
        found_tail = s
        break
    for md in ('K', 'D'):
        for x in range(1, n + 1):
            r = step_state(Acur, Bcur, md, x)
            if r is None:
                continue
            # skip full no-ops
            if r[2]['dA'] == 0 and (md == 'D' or r[2]['dB'] == 0):
                continue
            ns = (serial(r[0]), serial(r[1]))
            if ns not in states:
                states[ns] = (r[0], r[1])
                prev[ns] = s
                act[ns] = (md, x)
                dq.append(ns)
                expanded += 1
                if expanded >= NODECAP:
                    break
        if expanded >= NODECAP:
            break
log(f"[AKC] BFS expanded={expanded} target_found={found_tail is not None}")
if found_tail:
    tail = []
    s = found_tail
    while prev[s] is not None:
        tail.append(act[s])
        s = prev[s]
    tail = list(reversed(tail))
    log(f"[AKC] TAIL len={len(tail)}: {tail}")
    json.dump({"tail": tail}, open(RDIR / "26AK_tail.json", "w"), indent=1, default=str)
log("[AKC] done")
LOG.close()
