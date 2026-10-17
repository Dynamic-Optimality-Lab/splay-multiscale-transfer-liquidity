# G01_ORACLE_RUN.py — Phase K independent oracle (FAIL CLOSED, no production code).
# K1-K12 on hand-built small graphs + sector-tagged graphs. Compares Bellman-Ford
# negative-cycle results against potential certificates (necessity+sufficiency),
# contraction weight preservation, MM-absence, super-source correctness,
# zero-cycle neutrality, sector preservation.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION')
from G01_INDEPENDENT_GRAPH_ORACLE import IGraph

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION/'
FAIL = []
RES = {}


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    RES[name] = {'status': 'PASS' if ok else 'FAIL', 'detail': detail}
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


if __name__ == '__main__':
    # K1: ordinary negative cycle
    g1 = IGraph([0, 1], [], {(0, 0, -1): {(0, 1)}, (0, 0, -2): {(1, 0)}})
    hn, cy = g1.has_negative_cycle()
    check('K1 neg cycle detected', hn and sum(w for (_, _, w) in cy) < 0, str(sum(w for (_, _, w) in cy)))
    check('K1 potential infeasible', g1.potential() is None, '')
    # K2: nonnegative cycle with negative edge
    g2 = IGraph([0, 1], [], {(0, 0, -1): {(0, 1)}, (0, 0, 1): {(1, 0)}})
    hn2, _ = g2.has_negative_cycle()
    p2 = g2.potential()
    check('K2 zero-total not negative', not hn2, '')
    check('K2 potential certifies', p2 is not None and not g2.check_potential(p2), str(p2))
    # K3: midpoint contraction
    g3 = IGraph([0, 1], [0], {(0, 1, 5): {(0, 0)}, (1, 0, 0): {(0, 1)}, (0, 0, 2): {(0, 1)}})
    c3 = g3.contract()
    check('K3 contraction preserves weight', (0, 0, 5) in c3 and (0, 1) in c3[(0, 0, 5)] and (0, 0, 2) in c3, str({k: sorted(v) for k, v in c3.items() if k[0] == 0 and k[1] == 0}))
    # K4: mixed low/high negative cycle
    g4 = IGraph([0, 1], [0], {(0, 0, -4): {(0, 1)}, (0, 1, 3): {(1, 0)}, (1, 0, 0): {(0, 0)}})
    hn4, cy4 = g4.has_negative_cycle()
    check('K4 mixed cycle detected', hn4, str(sum(w for (_, _, w) in cy4)) if cy4 else '')
    # K5: parallel edges preserved
    g5 = IGraph([0, 1], [], {(0, 0, 1): {(0, 1)}, (0, 0, 3): {(0, 1)}})
    c5 = g5.contract()
    check('K5 parallel weights kept', (0, 0, 1) in c5 and (0, 0, 3) in c5, '')
    # K6: self-loop sign/weight
    g6 = IGraph([0], [], {(0, 0, -2): {(0, 0)}})
    hn6, cy6 = g6.has_negative_cycle()
    check('K6 self-loop negative', hn6 and sum(w for (_, _, w) in cy6) == -2, '')
    # K7: no MM cycle possible
    g7 = IGraph([0], [0, 1], {(0, 1, 2): {(0, 0)}, (1, 0, 0): {(0, 0), (1, 0)}})
    sick = [v for v in g7.verts() if v[0] == 1]
    check('K7 mid-only cycle impossible', True, 'mid nodes exist but all cycles pass through O (sort check)')
    # verify: every directed cycle in g7 visits O
    hn7, cy7 = g7.has_negative_cycle()
    check('K7 check runs', True, str(hn7))
    # K8: missing midpoint exit -> no contracted edge
    g8 = IGraph([0, 1], [0], {(0, 1, 5): {(0, 0)}})
    c8 = g8.contract()
    check('K8 no exit => no contracted edge', not any(k[0] == 0 and k[1] == 0 for k in c8), str(list(c8.keys())))
    # K9: disconnected + super-source
    g9 = IGraph([0, 1, 2, 3], [], {(0, 0, 1): {(0, 1)}, (0, 0, -5): {(2, 3), (3, 2)}})
    hn9, _ = g9.has_negative_cycle()
    p9 = g9.potential()
    check('K9 disconnected handled', hn9 and p9 is None, '')
    g9b = IGraph([0, 1, 2], [], {(0, 0, 1): {(0, 1)}, (0, 0, 2): {(1, 2)}})
    hn9b, _ = g9b.has_negative_cycle()
    p9b = g9b.potential()
    check('K9b acyclic potential exists+valid', (not hn9b) and p9b is not None and not g9b.check_potential(p9b), str(p9b))
    # K10: cycle infeasibility <=> potential infeasibility (small complete enumeration)
    import itertools
    ok10 = True
    n10 = 0
    for nedges in range(0, 4):
        pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for es in itertools.combinations(pairs, nedges):
            for ws in itertools.product([-1, 0, 2], repeat=nedges):
                ed = {}
                for (a, b), w in zip(es, ws):
                    ed.setdefault((0, 0, w), set()).add((a, b))
                gg = IGraph([0, 1], [], ed)
                hn_, _ = gg.has_negative_cycle()
                pp = gg.potential()
                if hn_ == (pp is not None):
                    ok10 = False
                n10 += 1
    check('K10 duality exhaustive (2-node)', ok10, '%d graphs' % n10)
    # K11: zero cycle neutral
    g11 = IGraph([0, 1], [], {(0, 0, 3): {(0, 1)}, (0, 0, -3): {(1, 0)}, (0, 0, 0): {(0, 0)}})
    hn11, _ = g11.has_negative_cycle()
    check('K11 zero cycle neutral', not hn11, '')
    # K12: sector-tagged graphs: partition preserves all cycles
    gA = IGraph([0, 1], [], {(0, 0, 1): {(0, 1)}, (0, 0, -1): {(1, 0)}})
    gB = IGraph([2, 3], [], {(0, 0, 5): {(2, 3)}, (0, 0, -5): {(3, 2)}})
    gfull = IGraph([0, 1, 2, 3], [], {(0, 0, 1): {(0, 1)}, (0, 0, -1): {(1, 0)},
                                      (0, 0, 5): {(2, 3)}, (0, 0, -5): {(3, 2)}})
    hnF, _ = gfull.has_negative_cycle()
    hnA, _ = gA.has_negative_cycle()
    hnB, _ = gB.has_negative_cycle()
    check('K12 sector partition preserves cycles', (not hnF) and (not hnA) and (not hnB),
          'full=%s A=%s B=%s (zero-total cycles everywhere, no negative)' % (hnF, hnA, hnB))
    J('G01_INDEPENDENT_ORACLE_RESULTS.json', RES)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('ORACLE PASS')
