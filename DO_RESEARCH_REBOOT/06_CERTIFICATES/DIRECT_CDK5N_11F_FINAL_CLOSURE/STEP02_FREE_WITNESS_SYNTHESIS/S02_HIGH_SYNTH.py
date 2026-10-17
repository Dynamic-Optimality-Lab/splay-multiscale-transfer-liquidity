# S02_HIGH_SYNTH.py — high-cost witness synthesis (Gate H-low... Gate G18).
# High relation (build_shigh, tag SH): single witnessed genuine core B-KEEP s.b -> g.b
# (= t.b) + fiber (mu/sig from s; v = dest root index) + q from depth + w1 = 6-q.
# No A-transition in the relation (B-focused by design). All hidden values derived
# from (s,t,w) + B-simulation; Tier-1 verifies on the shared high handle.
# "H>=3" reading: the high edge carries a deep B-cost (q>=3, depth>=6); the recorded
# A-side access cost a=(dA+1)//2 of the containing macro is reported alongside.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
from S02_B_SIDE_PROPAGATOR import decode_btopo, topo_key, find_path, splay_ref

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


def _side_of_path(topo, node, par):
    kl, lr, kr, rr = topo[par]
    if kl == 0 and lr == node:
        return False  # left -> bdir False (NOT shouldL convention)
    if kr == 0 and rr == node:
        return True
    raise AssertionError(('not a ref-child', node, par))


def solve_high(s_pins, t_pins, w, dag, high, residual, time_cap=240):
    import time
    t0 = time.process_time()
    if any(s_pins.get('SHs_sg%d' % i) != t_pins.get('SHt_sg%d' % i) for i in range(10)):
        return {'status': UNSAT, 'reason': 'sig-mismatch', 'cpu_s': 0.0}
    if s_pins.get('SHs_mu') != t_pins.get('SHt_mu'):
        return {'status': UNSAT, 'reason': 'mu-mismatch', 'cpu_s': 0.0}
    mu = s_pins['SHs_mu']
    marked = set(i for i in range(9) if (mu >> i) & 1)
    if len(marked) != 5:
        return {'status': UNSAT, 'reason': 'marked-count!=5', 'cpu_s': 0.0}
    stopo, sroot = decode_btopo(s_pins, 'SHs')
    ttopo, troot = decode_btopo(t_pins, 'SHt')
    tkey = topo_key(ttopo, troot)
    cands = []
    for tgt in sorted(marked):
        if tgt == sroot:
            continue
        try:
            ntopo, nroot, d = splay_ref(dict(stopo), sroot, tgt)
        except AssertionError:
            continue
        if topo_key(ntopo, nroot) != tkey:
            continue
        q = d // 2
        if 2 * q <= d < 2 * q + 2 and 6 - q == w:
            path = find_path(stopo, sroot, tgt)
            cands.append({'tgt': tgt, 'd': d, 'q': q, 'path': path})
    if not cands:
        return {'status': UNSAT, 'reason': 'no-high-words', 'cpu_s': round(time.process_time() - t0, 1)}
    for cand in cands:
        if time.process_time() - t0 > time_cap:
            return {'status': UNKNOWN, 'reason': 'time-cap', 'cpu_s': round(time.process_time() - t0, 1)}
        tgt, d, q, path = cand['tgt'], cand['d'], cand['q'], cand['path']
        pins = {}
        for k, v in s_pins.items():
            pins[k] = v
        for k, v in t_pins.items():
            pins[k] = v
        pins['SHg_fmu'] = mu
        for i in range(10):
            pins['SHg_fsg%d' % i] = s_pins['SHs_sg%d' % i]
        # fiber B = destination B (copy t.b arrays into g.b)
        for i in range(19):
            pins['SHg_fb_bkl%d' % i] = t_pins['SHt_b_bkl%d' % i]
            pins['SHg_fb_brl%d' % i] = t_pins['SHt_b_brl%d' % i]
            pins['SHg_fb_bkr%d' % i] = t_pins['SHt_b_bkr%d' % i]
            pins['SHg_fb_brr%d' % i] = t_pins['SHt_b_brr%d' % i]
            pins['SHg_fb_blo%d' % i] = t_pins['SHt_b_blo%d' % i]
            pins['SHg_fb_bhi%d' % i] = t_pins['SHt_b_bhi%d' % i]
        pins['SHg_fb_broot'] = t_pins['SHt_b_broot']
        pins['SHg_fv'] = t_pins['SHt_aI0']
        # B-trace event 0: bottom-up path + sides
        bup = path[::-1]
        pins['SHbt_bT0'] = tgt
        pins['SHbt_bd0'] = d
        for k in range(d + 1):
            pins['SHbt_bp0_%d' % k] = bup[k]
        for k in range(d):
            node, par = bup[k], bup[k + 1]
            pins['SHbt_bdir0_%d' % k] = _side_of_path(stopo, node, par)
        pins['SHbt_q'] = q
        pins['SH_q'] = q
        pins['SH_w1'] = w
        r = residual.verify('shigh', pins)
        if r['status'] != SAT:
            continue
        cpu = round(time.process_time() - t0, 1)
        return {'status': SAT, 'reason': 'synthesized', 'cpu_s': cpu,
                'target': tgt, 'depth': d, 'q': q, 'w': w, 'v': t_pins['SHt_aI0'],
                'env': {k: (bool(v) if isinstance(v, bool) else int(v)) for k, v in pins.items()}}
    return {'status': UNSAT, 'reason': 'exhausted', 'cpu_s': round(time.process_time() - t0, 1)}
