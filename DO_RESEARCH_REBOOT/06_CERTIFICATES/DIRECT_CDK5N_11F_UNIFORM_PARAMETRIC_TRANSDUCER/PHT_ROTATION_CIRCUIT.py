# PHT symbolic rotation transducer: slots + hole-refs + comparison branching + node counting.
# Trees: S.node form with hole markers ('H', hid) as leaves; holes dict hid -> {Ssub, gaplo, gaphi, nonempty}.
# Keys: S ranks (ints 1..9) or placeholders ('P', gap, seq). Comparisons: exact except sat-vs-sat (branch).
import sys, json

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_UNIFORM_PARAMETRIC_TRANSDUCER/'

class Counter:
    def __init__(self):
        self.n = 0  # transducer primitive-operation count (proxy for circuit nodes)
    def tick(self, k=1):
        self.n += k

def key_lt(a, b, ctr):
    # returns True/False/None(undetermined: sat-vs-sat placeholder order); ticks comparisons
    ctr.tick(1)
    va = a if isinstance(a, int) else None
    vb = b if isinstance(b, int) else None
    if va is not None and vb is not None:
        return va < vb
    # placeholders: ('P', gap, seq, sat?) with sat flag for saturated-count origin
    if isinstance(a, tuple) and isinstance(b, tuple):
        if a[1] != b[1]:
            return a[1] < b[1]  # different gaps: ordered
        if not a[3] and not b[3]:
            return a[2] < b[2]  # both exact-seq: ordered
        return None  # saturated-involved: undetermined -> branch
    return None

def descend(t, x, holes, ctr, bound=60):
    # returns (path, branches): path = list of (nodekey, side) + target depth info; branches on undetermined comparisons
    # branch state: list of assumed outcomes; explore depth-first with cap
    results = []
    stack = [(t, [], 0, {})]  # (subtree, path, depth, assumptions)
    while stack and len(results) < bound:
        cur, path, d, asm = stack.pop()
        if cur[0] == 'leaf':
            continue
        if isinstance(cur, tuple) and cur[0] == 'H':
            # opaque hole on path: expand (branch over root key: Ssub members + fresh placeholder)
            hid = cur[1]
            h = holes[hid]
            opts = [('S', s) for s in sorted(h['Ssub'])]
            opts.append(('P', hid))
            for o in opts:
                results.append(('hole-expand', hid, o, tuple(path), d, dict(asm)))
            continue
        _, k, l, r = cur
        if _keyeq(k, x):
            results.append(('found', tuple(path), d, dict(asm)))
            continue
        c = key_lt(x, k, ctr) if False else _cmp(x, k, ctr)
        if c is True:
            stack.append((l, path + [(k, 'L')], d + 1, asm))
        elif c is False:
            stack.append((r, path + [(k, 'R')], d + 1, asm))
        else:
            a2 = dict(asm)
            a2[('lt', _kstr(x), _kstr(k))] = True
            stack.append((l, path + [(k, 'L')], d + 1, a2))
            asm[('lt', _kstr(x), _kstr(k))] = False
            stack.append((r, path + [(k, 'R')], d + 1, asm))
    return results

def _keyeq(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    return a == b

def _kstr(k):
    return str(k)

def _cmp(x, k, ctr):
    ctr.tick(1)
    if isinstance(x, int) and isinstance(k, int):
        return x < k
    if isinstance(x, tuple) and isinstance(k, tuple) and x[0] == 'P' and k[0] == 'P':
        if x[1] != k[1]:
            return x[1] < k[1]
        if not x[3] and not k[3]:
            return x[2] < k[2]
        return None
    return None

if __name__ == "__main__":
    ctr = Counter()
    # smoke: concrete tree (no holes/placeholders) behaves exactly like source
    import sys as _s
    _s.path.insert(0, 'python/independent')
    import splay as S
    t = S.node(5, S.node(3, S.node(1, S.LEAF, S.LEAF), S.node(4, S.LEAF, S.LEAF)),
               S.node(7, S.node(6, S.LEAF, S.LEAF), S.node(9, S.node(8, S.LEAF, S.LEAF), S.node(10, S.LEAF, S.LEAF))))
    r = descend(t, 8, {}, ctr)
    print("concrete descend branches=%d ops=%d" % (len(r), ctr.n), flush=True)
    print("first:", r[0][0], r[0][2], flush=True)
    json.dump({"branches": len(r), "ops": ctr.n}, open(PDIR + "PHT_TRANSDUCER_SMOKE.json", "w"), indent=1)
