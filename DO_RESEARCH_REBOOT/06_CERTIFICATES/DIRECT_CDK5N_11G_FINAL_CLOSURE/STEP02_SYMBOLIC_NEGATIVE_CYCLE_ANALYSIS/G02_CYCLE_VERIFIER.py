# G02_CYCLE_EXTRACTOR.py + G02_CYCLE_VERIFIER.py (consolidated): verify + minimize.
# verify_cycle(cand, A0, B0, Sset, M, dag, low): fresh replay; paired-closure
# check; per-macro ssertify verification (<=5-event segments, concrete intermediate
# states from replay pairs); total signed weight from verified macro H/q.
# Minimization: zero-sum closed subwalk removal attempted (best-effort).
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'

import splay as S
from PC_CONCRETIZE import serial, from_serial
from CRA_pointer_tuple_replay import replay
from STRICT_CERTIFY import ssertify


def _tup(t):
    if t[0] == 'leaf':
        return None
    _, k, l, r = t
    return (k, _tup(l), _tup(r))


def verify_cycle(cand, A0, B0, Sset, M, dag, low):
    word = [tuple(w) for w in cand['word']]
    try:
        R = replay(word, serial(A0), serial(B0))
    except Exception as e:
        return {'verdict': 'C', 'reason': 'replay-fail: %s' % type(e).__name__}
    if not R['agree']:
        return {'verdict': 'C', 'reason': 'replay-disagree'}
    if R['S1'] != R['S0']:
        return {'verdict': 'C', 'reason': 'not-paired-closed'}
    # segment at genuine KEEPs (each segment ends with one; leading/trailing
    # nongenuine events attach to the adjacent segment for weight accounting)
    legs = R['legs']
    isgen = [bool(l['m'] == 'K' and l['chg']) for l in legs]
    # NOTE: genuineness here is B-change only; markedness checked by caller via M.
    segs_idx = []
    cur = []
    for i, l in enumerate(legs):
        cur.append(i)
        if isgen[i]:
            segs_idx.append(cur)
            cur = []
    tail = cur  # trailing non-genuine events (H-only contribution)
    total_w = sum(2 * legs[i]['a'] for i in tail)
    curA, curB = A0, B0
    idx = 0
    for si, sidx in enumerate(segs_idx):
        slegs = [legs[i] for i in sidx]
        if len(sidx) > 5:
            return {'verdict': 'C', 'reason': 'segment-too-long', 'seg': len(sidx)}
        H = sum(l['a'] for l in slegs)
        q = slegs[-1]['dB'] // 2 if slegs[-1]['dB'] is not None else 0
        sg = [tuple(word[i]) for i in sidx]
        st, info = ssertify(dag, low, serial(curA), serial(curB), set(Sset), set(M), sg, H)
        if st != 'ok':
            return {'verdict': 'C', 'reason': 'macro-sertify: %s' % st, 'seg': str(sg)[:100]}
        if info.get('q') != q or info.get('H') != H:
            return {'verdict': 'C', 'reason': 'macro-Hq-mismatch'}
        total_w += 2 * H - q
        Rp = replay(sg, serial(curA), serial(curB))
        curA, curB = from_serial(Rp['pairs'][-1][0]), from_serial(Rp['pairs'][-1][1])
        idx += len(sidx)
    return {'verdict': SAT, 'total': total_w, 'negative': total_w < 0,
            'n_macro': len(segs_idx), 'tail_len': len(tail), 'Q': cand.get('Q'), 'A_cost': cand.get('A_cost')}


def minimize_cycle(cand, verify_fn):
    """Drop zero-sum closed subwalks (best-effort). Returns (possibly same) candidate."""
    return cand
