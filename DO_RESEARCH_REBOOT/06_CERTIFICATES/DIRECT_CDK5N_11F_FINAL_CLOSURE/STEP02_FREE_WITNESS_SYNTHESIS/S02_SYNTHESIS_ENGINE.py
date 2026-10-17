# S02_SYNTHESIS_ENGINE.py — source-guided staged synthesis (Gates C-F).
# solve_edge(s_pins, t_pins, w): validate -> B-BFS words -> canonical completions ->
# replay filter -> ssertify -> abstract-match -> Tier-1 verify -> witness.
# No H/q/hidden pins from fixtures: q/H derived from B-depths + w=2H-q; skeletons from
# B-words; completions canonical-first bounded. Exhaustion = genuine UNSAT (finite,
# explicitly bounded space) subject to the time cap.
import sys, time, itertools
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
import splay as S
from PC_CONCRETIZE import serial
from STRICT_CERTIFY import ssertify
from S02_B_SIDE_PROPAGATOR import decode_btopo, topo_key, b_bfs
from S02_A_PREFIX_SYNTHESIS import CK, gap_pool, build_A0, build_B0, count_alternatives
from CRA_pointer_tuple_replay import replay, ReplayError

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


class SynthesisEngine:
    def __init__(self, dag, low, residual, max_words=500, max_alts=32, max_dkey=200,
                 orders=('asc', 'desc', 'balanced'), max_completions=96, time_cap=240):
        self.d = dag
        self.L = low
        self.rs = residual
        self.max_words = max_words
        self.max_alts = max_alts
        self.max_dkey = max_dkey
        self.orders = orders
        self.max_completions = max_completions
        self.time_cap = time_cap
        self.log = []

    def _note(self, msg):
        self.log.append(msg)

    def solve_edge(self, s_pins, t_pins, w):
        t0 = time.process_time()
        # 1. validate abstract query (necessary filters, all source-justified)
        if any(s_pins.get('SLs_sg%d' % i) != t_pins.get('SLt_sg%d' % i) for i in range(10)):
            return {'status': UNSAT, 'reason': 'sig-mismatch', 'cpu_s': 0.0}
        if s_pins.get('SLs_mu') != t_pins.get('SLt_mu'):
            return {'status': UNSAT, 'reason': 'mu-mismatch', 'cpu_s': 0.0}
        mu = s_pins['SLs_mu']
        marked = set(i for i in range(9) if (mu >> i) & 1)
        if len(marked) != 5:
            return {'status': UNSAT, 'reason': 'marked-count!=5', 'cpu_s': 0.0}
        # 2. B-words (q/H derived)
        stopo, sroot = decode_btopo(s_pins, 'SLs')
        ttopo, troot = decode_btopo(t_pins, 'SLt')
        try:
            words, n_found = b_bfs(stopo, sroot, topo_key(ttopo, troot), marked, w)
        except AssertionError as e:
            return {'status': UNSAT, 'reason': 'b-decode: %s' % (e,), 'cpu_s': 0.0}
        words.sort(key=lambda r: (len(r['word']), str(r['word'])))
        if not words:
            return {'status': UNSAT, 'reason': 'no-b-words', 'cpu_s': round(time.process_time() - t0, 1)}
        truncated = n_found > self.max_words
        words = words[:self.max_words]
        # 3. canonical universe
        Sset = set(CK)
        M = set(CK[i] for i in marked)
        fringe = {g: gap_pool(g, s_pins['SLs_sg%d' % g]) for g in range(10)}
        fkeys = [k for pool in fringe.values() for k in pool]
        n_alt_total = count_alternatives(s_pins, fringe)
        tried = skipped = failed_replay = failed_sert = mismatch = 0
        for cand in words:
            if time.process_time() - t0 > self.time_cap:
                return {'status': UNKNOWN, 'reason': 'time-cap', 'cpu_s': round(time.process_time() - t0, 1),
                        'tried': tried, 'words': len(words)}
            word0 = cand['word']
            # expand DELETE keys over canonical A keys (bounded)
            ds = [i for i, (m, _) in enumerate(word0) if m == 'D']
            akeys = sorted(Sset) + sorted(fkeys)
            dprod = list(itertools.product(akeys, repeat=len(ds)))[:self.max_dkey]
            if len(ds) and len(list(itertools.product(akeys, repeat=len(ds)))) > self.max_dkey:
                self._note('dkey-truncated')
            for dkeys in dprod or [()]:
                wfull = []
                di = 0
                for (m, k) in word0:
                    if m == 'D':
                        wfull.append(('D', dkeys[di]))
                        di += 1
                    else:
                        wfull.append(('K', CK[k]))
                n_alt = min(max(1, n_alt_total), self.max_alts)
                combos = [(o, a) for o in self.orders for a in range(n_alt)][:self.max_completions]
                for (order, alt) in combos:
                    if time.process_time() - t0 > self.time_cap:
                        return {'status': UNKNOWN, 'reason': 'time-cap', 'cpu_s': round(time.process_time() - t0, 1), 'tried': tried}
                    A0, _ = build_A0(s_pins, Sset, {g: list(v) for g, v in fringe.items()}, alt, order)
                    if A0 is None:
                        continue
                    B0 = build_B0(s_pins, fkeys, order)
                    try:
                        rr = replay(wfull, serial(A0), serial(B0))
                    except Exception:
                        failed_replay += 1
                        continue
                    if any(l['dA'] > 4 for l in rr['legs'] if l['m'] == 'K'):
                        continue
                    tried += 1
                    st, info = ssertify(self.d, self.L, serial(A0), serial(B0), Sset, M, wfull, cand['H'])
                    if st == 'skip':
                        skipped += 1
                        continue
                    if st != 'ok':
                        failed_sert += 1
                        continue
                    # abstract-match: derived s/t pins must equal query pins
                    env = info['env']
                    bad = [k for k in s_pins if env.get(k) != s_pins[k]] + \
                          [k for k in t_pins if env.get(k) != t_pins[k]]
                    if bad:
                        mismatch += 1
                        continue
                    if info.get('q') != cand['q'] or info.get('H') != cand['H'] or info.get('w') != w:
                        mismatch += 1
                        continue
                    # Tier-1 verify full env on shared handle
                    r = self.rs.verify('slow', dict(env))
                    if r['status'] != SAT:
                        failed_sert += 1
                        continue
                    cpu = round(time.process_time() - t0, 1)
                    return {'status': SAT, 'reason': 'synthesized', 'cpu_s': cpu,
                            'word': wfull, 'H': cand['H'], 'q': cand['q'], 'w': w,
                            'depths': cand['depths'], 'env': {k: (bool(v) if isinstance(v, bool) else int(v)) for k, v in env.items()},
                            'A0': serial(A0), 'B0': serial(B0), 'Sset': sorted(Sset),
                            'M': sorted(M), 'replay': rr['legs'], 'pairs': rr['pairs'],
                            'tried': tried, 'skipped': skipped}
        cpu = round(time.process_time() - t0, 1)
        # Soundness scoping (Gate J): UNSAT is claimed ONLY for B-level/validation
        # exclusions (no-b-words and friends). A-shape completion space (insertion
        # orders) is ordering-bounded, not exhaustive: A-level exhaustion is UNKNOWN
        # with exact counts, never UNSAT.
        if truncated:
            # word space larger than the cap: exhaustion is NOT a complete exclusion.
            return {'status': UNKNOWN, 'reason': 'word-truncated', 'cpu_s': cpu, 'tried': tried,
                    'skipped': skipped, 'mismatch': mismatch, 'failed_replay': failed_replay,
                    'failed_sert': failed_sert, 'words': len(words), 'n_found': n_found}
        return {'status': UNKNOWN, 'reason': 'a-incomplete', 'cpu_s': cpu, 'tried': tried,
                'skipped': skipped, 'mismatch': mismatch, 'failed_replay': failed_replay,
                'failed_sert': failed_sert, 'words': len(words)}
