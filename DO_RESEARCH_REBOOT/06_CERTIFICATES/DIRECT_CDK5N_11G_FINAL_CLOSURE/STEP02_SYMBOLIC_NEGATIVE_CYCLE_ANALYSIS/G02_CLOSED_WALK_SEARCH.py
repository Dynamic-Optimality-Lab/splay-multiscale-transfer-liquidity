# G02_CLOSED_WALK_SEARCH.py — source-level closed-walk enumerator (primary search).
# BFS over concrete (A,B) pairs with visited-set + depth cap (preregistered).
# B-evolution is exact splay; A-evolution is exact replay; G = genuine KEEP set.
# Every reported closed walk is fully replayed (TYPE A by construction).
# UNSAT = bounded-exhaustive (depth cap + visited dedup, both documented);
# UNKNOWN = cap/truncation hit. No Z3 graph unrolling (cap-safe by design).
import sys, time, itertools
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, ReplayError

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


def _ser(t):
    return None if t[0] == 'leaf' else (t[1], _ser(t[2]), _ser(t[3]))


def _from_serial(ps):
    if ps is None or ps == '.':
        return ('leaf',)
    k, l, r = ps
    return ('node', k, _from_serial(l), _from_serial(r))


def _tup(t):
    if t[0] == 'leaf':
        return None
    _, k, l, r = t
    return (k, _tup(l), _tup(r))


class ClosedWalkSearch:
    def __init__(self, max_depth=8, max_states=50000, max_results=200):
        self.max_depth = max_depth
        self.max_states = max_states
        self.max_results = max_results
        self.stats = {}

    def search(self, A0, B0, keys, time_cap=120):
        """BFS words; returns (status, closed_list, stats). Closed = paired closure.
        Each closed walk is replay-verified (agree), with legs (dA/dB/a/q/chg)."""
        t0 = time.process_time()
        s0 = (_tup(A0), _tup(B0))
        seen = {s0}
        frontier = [(A0, B0, [])]
        closed = []
        nvis = 0
        truncated = False
        while frontier:
            if time.process_time() - t0 > time_cap:
                truncated = True
                break
            if len(seen) > self.max_states:
                truncated = True
                break
            A, B, w = frontier.pop()
            if len(w) >= self.max_depth:
                continue
            for md in ('K', 'D'):
                for x in keys:
                    nw = w + [(md, x)]
                    try:
                        R = replay(nw, serial(A), serial(B))
                    except Exception:
                        continue
                    if not R['agree']:
                        continue
                    A2 = _from_serial(R['pairs'][-1][0])
                    B2 = _from_serial(R['pairs'][-1][1])
                    key = (_tup(A2), _tup(B2))
                    if _tup(A2) == _tup(A0) and _tup(B2) == _tup(B0) and nw:
                        closed.append({'word': nw, 'legs': R['legs']})
                        if len(closed) >= self.max_results:
                            truncated = True
                            break
                    if key not in seen and len(nw) < self.max_depth:
                        seen.add(key)
                        nvis += 1
                        frontier.append((A2, B2, nw))
                if truncated:
                    break
        self.stats = {'visited': len(seen), 'closed': len(closed), 'truncated': truncated,
                      'cpu_s': round(time.process_time() - t0, 1)}
        if truncated:
            return (UNKNOWN, closed, self.stats)
        return ('EXHAUSTED', closed, self.stats)


def serial(t):
    if t[0] == 'leaf':
        return None
    _, k, l, r = t
    return [k, serial(l), serial(r)]
