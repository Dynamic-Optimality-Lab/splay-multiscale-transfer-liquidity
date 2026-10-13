# H=1 negative-edge kernel: template enumeration over canonical shadows + guard schema.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'python/independent')
import splay as S
from AFSP_canonical import canonical_shadow

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'

def shapes(keys):
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in shapes(keys[:i]):
            for r in shapes(keys[i + 1:]):
                out.append(S.node(k, l, r))
    return out

def depth(t, x):
    d = 0
    cur = t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return d
        cur = l if x < k else r
        d += 1
    return None

# H=1 templates: single KEEP(v) a=1 (d 1-2); [D(y) a=1, K(v) a=0]; over canonical 9-key shadows.
# Count distinct (shadow, u, v, word-pattern, dA, step-case) with q in {3,4} placeholder (B-side separate).
ALL9 = shapes(list(range(1, 10)))
templates = set()
Srank = set(range(1, 10))
for t in ALL9:
    # shadow over S=1..9 (all keys core for kernel census)
    try:
        sh = canonical_shadow(t, Srank)
    except Exception:
        continue
    # root u must be marked-ish: record all roots (mask applied at product level)
    if t[0] == 'leaf':
        continue
    u = t[1]
    for v in range(1, 10):
        if v == u:
            continue
        d = depth(t, v)
        if d not in (1, 2):
            continue
        t1, evs = S.trace(t, v)
        steps = tuple(e[0] for e in evs)
        templates.add((sh['vis'], u, v, (('K',),), d, steps))
        # [D(v), K(v)] with a=1+0 (nonzero-on-DELETE; y==v forced: DELETE(y) roots y, KEEP at root needs v==y)
        if d in (1, 2):
            tA, evsA = S.trace(t, v)
            # DELETE(v) splays v identically (same operation, B untouched); KEEP(v) then at root, a=0
            templates.add((sh['vis'], u, v, (('D',), ('K',)), (d, 0), steps))
print("H=1 kernel templates (9-key canonical shadows): %d" % len(templates), flush=True)
# guard schema per template: AF-2 allocation over (holes of shadow, S-subsets, signature) — schema recorded, not solved here
import collections
pat = collections.Counter()
for (vis, u, v, wp, d, st) in templates:
    pat[(wp, st)] += 1
print("pattern x step-case:", dict(pat), flush=True)
json.dump({"templates": len(templates),
           "patterns": {str(k): v for k, v in pat.items()},
           "note": "q in {3,4} via B-controller depths 6,7,8; guards = AF-2 allocation over shadow holes + signature (solver-verified separately)"},
          open(PDIR + "AFSP_NEGATIVE_EDGE_KERNEL.json", "w"), indent=1)
