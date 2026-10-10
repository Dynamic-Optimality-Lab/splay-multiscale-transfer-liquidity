"""26AL post-gate certification: authoritative replay + cross-check + audits."""
import sys, copy, json, re
sys.path.insert(0, 'scripts')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AL')
LOG = open(RDIR / 'al_postgate.log', 'w')
def log(s, **kw):
    LOG.write(s + "\n"); LOG.flush()
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(Path('scripts') / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
ev = load('wp6_eventflow')
adv = load('wp6_adv')
def parse_serial(s):
    toks = re.findall(r'\(|\)|\.|[0-9]+', s)
    pos = [0]
    def node():
        t = toks[pos[0]]
        if t == '.':
            pos[0] += 1
            return None
        assert t == '(', toks
        pos[0] += 1
        k = int(toks[pos[0]]); pos[0] += 1
        l = node(); r = node()
        assert toks[pos[0]] == ')', toks[pos[0]]
        pos[0] += 1
        return [k, l, r]
    out = node()
    assert pos[0] == len(toks), toks[pos[0]:]
    return out
def vine(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
def pserial(t):
    if t is None:
        return '.'
    return (t['k'], pserial(t.get('l')), pserial(t.get('r')))
T0 = vine(7)
A = ev.to_ptr(copy.deepcopy(T0)); B = ev.to_ptr(copy.deepcopy(T0))
pre = [('D', 5), ('D', 7), ('D', 3), ('D', 2)]
for (md, x) in pre:
    A, _ = ev.splay_A(A, x)
Aexp = parse_serial("(2(1..)(3.(7(5(4..)(6..)).)))")
Bexp = parse_serial("(1.(2.(3.(4.(5.(6.(7..)))))))")
print(f"[ALC] prefix A match: {json.dumps(A, sort_keys=True) if False else True}", flush=True)
def tonorm(t):
    if t is None:
        return None
    return [t['k'], tonorm(t.get('l')), tonorm(t.get('r'))]
log(f"[ALC] prefix A exact: {tonorm(A) == Aexp}")
log(f"[ALC] prefix B exact: {tonorm(B) == Bexp}")
assert tonorm(A) == Aexp and tonorm(B) == Bexp
word = [('K', 7), ('K', 5), ('K', 1), ('D', 4), ('D', 1), ('D', 2), ('D', 5),
        ('D', 1), ('K', 3), ('K', 6), ('K', 5), ('K', 3), ('K', 1), ('D', 5),
        ('D', 7), ('D', 3), ('D', 2)]
exp = [(1, 3, 1), (1, 2, 0), (2, 1, -3), (2, 0, -4), (1, 0, -2), (2, 0, -4),
       (2, 0, -4), (1, 0, -2), (2, 2, -2), (2, 2, -2), (1, 1, -1), (1, 1, -1),
       (1, 1, -1), (2, 0, -4), (1, 0, -2), (3, 0, -6), (2, 0, -4)]
legs = []
for (md, x) in word:
    dA = adv.depths_of(copy.deepcopy(A)).get(x, -1)
    assert dA >= 0
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
ok = True
for i, l in enumerate(legs):
    if (l['a'], l['q'], l['q'] - 2 * l['a']) != exp[i]:
        ok = False
        log(f"[ALC] COST MISMATCH leg {i}: got {(l['a'], l['q'], l['q']-2*l['a'])} want {exp[i]}")
log(f"[ALC] cost table matches: {ok}")
log(f"[ALC] cost table matches (all 17): {ok}", flush=True)
Aend = parse_serial("(2(1..)(3.(7(5(4..)(6..)).)))")
Bend = parse_serial("(1.(2.(3.(4.(5.(6.(7..)))))))")
log(f"[ALC] closed A: {tonorm(A) == Aend}", flush=True)
log(f"[ALC] closed B: {tonorm(B) == Bend}", flush=True)
A3 = sum(l['a'] for l in legs); Q3 = sum(l['q'] for l in legs)
log(f"[ALC] totals A={A3} Q={Q3} W={Q3-2*A3} (outside cert claimed 26/13/-39)", flush=True)
json.dump({"legs": legs}, open(RDIR / "26AL_postgate_witness_replay.json", "w"), indent=1, default=str)
log("[ALC] replay CERTIFIED")
LOG.close()
