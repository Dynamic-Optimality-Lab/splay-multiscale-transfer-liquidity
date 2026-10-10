"""GATE G novelty: fresh block records (rb/chg/push) + AM-G/S + 5 recognizers.

No imports from any historical replay module. All values recomputed.
"""
import sys, copy, json, hashlib, importlib.util
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_MR_G0_REPLAY_ERRATUM')
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S
import legacy_embedding as PE

def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def pserial(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]
INC = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 5),
       ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9), ('D', 8),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 4),
       ('D', 2), ('D', 5), ('D', 6), ('D', 1), ('D', 9)]

A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
legs = []
for (md, x) in INC:
    dA = pdepths(A).get(x, -1); assert dA >= 0
    a = (dA + 1) // 2
    ra, rb = proot(A), proot(B)
    sb = pserial(B)
    if md == 'K':
        dB = pdepths(B).get(x, -1); assert dB >= 0
        q = dB // 2
    else:
        dB = None; q = 0
    A, _ = splay_A(A, x)
    push = []
    if md == 'K':
        B, outB = splay_B_push(B, x)
        for s in outB:
            push += list(s)
    legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                 "delta": q - 2 * a, "rb": rb, "chg": (pserial(B) != sb) if md == 'K' else False,
                 "push": sorted(set(push))})
bl = [{'key': l['x'], 'a': l['a'], 'q': l['q'], 'delta': l['delta'],
       'genuine': l['chg'], 'dB': l['dB'], 'rb': l['rb'],
       'keeps': [l['x']] if l['m'] == 'K' else []} for l in legs]
m = len(bl)
pos = [(i, l['x'], l['a'], l['q'], l['delta'], l['rb']) for i, l in enumerate(legs) if l['delta'] > 0]
print("positives:", pos)
assert [p[0] for p in pos] == [2, 9, 22] and all(p[5] == 9 for p in pos)

def G(i):
    b, b1, b2, b3 = bl[i], bl[(i + 1) % m], bl[(i + 2) % m], bl[(i + 3) % m]
    r = b['rb']; c = 3
    return {'leaders': [b['key'], b1['key'], b2['key'], b3['key']],
            'G1': b['delta'] > 0,
            'G2': (b1['genuine'], b1['key'] != r, b2['genuine'], b2['key'] != r),
            'G3': (b1['delta'], b2['delta']),
            'G4': (b3['key'] == r and r in b3['keeps']),
            'G5': (2 * b3['a'], c),
            'S': (b1['delta'] == 0 and b2['delta'] == 0)}
g3a, g5a, g5b = G(2), G(9), G(22)
print("K3a:", g3a)
print("K5a:", g5a)
print("K5b:", g5b)
assert g3a['G1'] and g3a['G2'] == (True, True, False, True) and g3a['G4'] is False
assert g5a['G1'] and g5a['G4'] and g5a['G5'][0] >= g5a['G5'][1]
assert g5b['G1'] and g5b['G4'] and g5b['G5'][0] >= g5b['G5'][1]
# h measured
A2 = to_ptr(copy.deepcopy(T0)); B2 = to_ptr(copy.deepcopy(T0))
for i, (md, x) in enumerate(INC):
    A2, _ = splay_A(A2, x)
    if md == 'K':
        B2, _ = splay_B_push(B2, x)
    if i in (2, 9, 22):
        print("h after idx %d =" % i, pdepths(B2).get(9))
        assert pdepths(B2).get(9) == 2

def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    mm = importlib.util.module_from_spec(s); s.loader.exec_module(mm)
    return mm, hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
bl2 = [dict(b, keys=[b['key']], dA=legs[j]['dA'], push=legs[j]['push'], l0=j, l1=j + 1)
       for j, b in enumerate(bl)]
R = {}
for n, p in [('26AO', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AO/26AO_two_order_recognizer.py'),
             ('26AP', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AP/26AP_maximal_run_recognizer.py'),
             ('26AQ', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ/26AQ_mixed_cyclic_dp_recognizer.py'),
             ('26AR', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AR/26AR_mixed_exact_cover_recognizer.py'),
             ('26AS', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS/26AS_mixed_cyclic_recognizer.py')]:
    Mh, h = load(n, p)
    r = Mh.recognize(bl2, {j: {} for j in range(m)}) if n == '26AS' else Mh.recognize(bl2)
    R[n] = {'decision': 'REJECT' if not (r or {}).get('accepted') else 'ACCEPT', 'sha12': h}
AO, _ = load('aox', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AO/26AO_two_order_recognizer.py')
R['26AO']['typeI'] = [i for i in range(m) if AO.match_type1([bl2[(i + k) % m] for k in range(4)])]
R['26AO']['typeII'] = [i for i in range(m) if AO.match_type2([bl2[(i + k) % m] for k in range(4)])]
print(R)
assert all(v['decision'] == 'REJECT' for v in R.values())
assert R['26AO']['typeI'] == [] and R['26AO']['typeII'] == []
json.dump({"positives": pos, "K3a": g3a, "K5a": g5a, "K5b": g5b,
           "recognizers": R, "novelty": "RETAINED"},
          open(RDIR / 'MRER_novelty_regression.json', 'w'), indent=1)
json.dump(R, open(RDIR / 'MRER_recognizer_results.json', 'w'), indent=1)
print("GATE G novelty: RETAINED at current HEAD", flush=True)
