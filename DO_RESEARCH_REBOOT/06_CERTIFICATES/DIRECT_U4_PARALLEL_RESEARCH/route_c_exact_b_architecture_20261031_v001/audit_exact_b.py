"""One frozen completion-fiber minor. No potential fitting; exact integer dual audit."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PARENT = HERE.parent
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, obj):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def main():
    old = PARENT / 'route_c_root_step_refutation_20261031_v001/entry_source_pins.json'
    inherited = json.loads(old.read_text(encoding='utf-8'))
    files = dict(inherited['files'])
    for p in PARENT.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            files[p.relative_to(ROOT).as_posix()] = sha(p)
    for p in STAGE.rglob('*'):
        if p.is_file():
            files[p.relative_to(ROOT).as_posix()] = sha(p)
    for rel, value in files.items():
        assert sha(ROOT / rel) == value, rel
    stage_files = {p.relative_to(STAGE).as_posix(): sha(p)
                   for p in STAGE.rglob('*') if p.is_file()}
    pins = dict(date='2026-10-31', head=git('rev-parse', 'HEAD'),
                branch=git('branch', '--show-current'),
                tracked_status=git('status', '--porcelain=v1', '--untracked-files=no'),
                files=files, stage_files=stage_files,
                inherited_pin_count=len(inherited['files']))
    assert not pins['tracked_status']
    save('entry_source_pins.json', pins)

    spec = importlib.util.spec_from_file_location('tuple_source', ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    L = s.LEAF
    def leaf(k):
        return s.node(k, L, L)
    @lru_cache(None)
    def trees(lo, hi):
        if lo > hi:
            return (L,)
        return tuple(s.node(k, a, b) for k in range(lo, hi+1)
                     for a in trees(lo, k-1) for b in trees(k+1, hi))
    core = (1, 3, 7)
    fringes = (L, leaf(2), s.node(5, leaf(4), leaf(6)), L)
    @lru_cache(None)
    def a_trees(i, j):
        if i == j:
            return (fringes[i],)
        return tuple(s.node(core[k], a, b) for k in range(i, j)
                     for a in a_trees(i, k) for b in a_trees(k+1, j))
    aa = a_trees(0, 3)
    bb = trees(1, 7)
    assert len(aa) == 5 and len(bb) == 429 and len(set(bb)) == 429
    assert all(s.inorder(t) == list(range(1, 8)) for t in aa+bb)
    ai = {t: i for i, t in enumerate(aa)}
    bi = {t: i for i, t in enumerate(bb)}
    completions = {}
    for j, b in enumerate(bb):
        for x in core:
            c, ev = s.trace(b, x)
            found, d = s.lookup(b, x)
            assert found and len(ev) == (d+1)//2
            assert sum(e[0] != 'ZIG' for e in ev) == d//2
            assert c[1] == x and c in bi
            completions[j, x] = (bi[c], d, d//2, ev)
    nodes, ni, rows = [], {}, []
    def vertex(i, j):
        assert aa[i][1] == bb[j][1]
        v = (i, j)
        if v not in ni:
            ni[v] = len(nodes)
            nodes.append(v)
        return ni[v]
    noop = 0
    for i, a in enumerate(aa):
        r = a[1]
        for j, b in enumerate(bb):
            for x in core:
                ap, aev = s.trace(a, x)
                da = s.lookup(a, x)[1]
                assert ap in ai and da <= 2
                if da == 0:
                    noop += 1
                    continue
                cr, dr, qr, _ = completions[j, r]
                cx, dx, qx, _ = completions[j, x]
                u, v = vertex(i, cr), vertex(ai[ap], cx)
                weight = 2*((da+1)//2)+qr-qx
                rows.append(dict(A=i, B=j, request=x, source=u, target=v,
                                 d_A=da, a=(da+1)//2, Q_source=qr, Q_target=qx,
                                 d_B_source_root=dr, d_B_target_root=dx, weight=weight))
    assert len(rows) == 4290 and noop == 2145
    # Super-source of weight zero to every vertex, implemented by all-zero distances.
    dist, pred = [0]*len(nodes), [None]*len(nodes)
    last = None
    passes = 0
    for _ in range(len(nodes)):
        last = None
        passes += 1
        for ei, e in enumerate(rows):
            u, v, w = e['source'], e['target'], e['weight']
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                pred[v] = ei
                last = v
        if last is None:
            break
    cycle = []
    if last is not None:
        v = last
        for _ in nodes:
            assert pred[v] is not None
            v = rows[pred[v]]['source']
        start = v
        while True:
            ei = pred[v]
            cycle.append(ei)
            v = rows[ei]['source']
            if v == start:
                break
        cycle.reverse()
        assert sum(rows[ei]['weight'] for ei in cycle) < 0
        assert all(rows[cycle[k]]['target'] == rows[cycle[(k+1)%len(cycle)]]['source']
                   for k in range(len(cycle)))
    else:
        assert all(dist[e['target']] <= dist[e['source']]+e['weight'] for e in rows)
    def raw(t):
        return None if t == L else [t[1], raw(t[2]), raw(t[3])]
    witness = []
    for ei in cycle:
        e = rows[ei]
        i, j, x = e['A'], e['B'], e['request']
        r = aa[i][1]
        ap, aev = s.trace(aa[i], x)
        cr, _, _, rev = completions[j, r]
        cx, _, _, xev = completions[j, x]
        witness.append(dict(edge_index=ei, **e, actual_A=raw(aa[i]), actual_B=raw(bb[j]),
                            actual_A_after=raw(ap), source_completed_B=raw(bb[cr]),
                            target_completed_B=raw(bb[cx]), A_events=aev,
                            source_completion_events=rev, target_completion_events=xev,
                            actual_q=0, actual_z=0, multiplier=1))
    cert = dict(schema='exact-b-completion-fiber-dual-v1', n=7, core=list(core),
                A_trees=[raw(t) for t in aa], B_trees=[raw(t) for t in bb],
                terminal_nodes=nodes, rows=rows, noop_rows=noop,
                bellman_ford_passes=passes,
                negative_cycle=cycle, cycle_weight=sum(rows[i]['weight'] for i in cycle),
                witness=witness,
                feasible_minor_labels=None if cycle else dist,
                status='REFUTED-EXACT' if cycle else 'FINITE-EXACT-NO-NEGATIVE-CYCLE')
    save('exact_b_architecture_certificate.json', cert)
    print(json.dumps(dict(status=cert['status'], nodes=len(nodes), edges=len(rows),
                          cycle_length=len(cycle), cycle_weight=cert['cycle_weight'],
                          cycle_rows=[{k:e[k] for k in ('A','B','request','Q_source','Q_target','weight')} for e in witness],
                          stage_files=len(stage_files), preserved_files=len(files)), indent=2))

if __name__ == '__main__':
    main()
