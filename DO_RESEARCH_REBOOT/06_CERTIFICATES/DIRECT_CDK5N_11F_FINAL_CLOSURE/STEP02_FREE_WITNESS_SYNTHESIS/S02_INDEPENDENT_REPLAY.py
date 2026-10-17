# S02_INDEPENDENT_REPLAY.py — fresh-process witness replay (Gate I verification side).
# Replays the certified word on the certified trees with the untouched source replay
# engine and checks: finals equal recorded destinations, per-leg depths/q/change match,
# start serials match, w=2H-q. Abstract-endpoint agreement was established at synthesis
# (abstract-match) and is re-checked by the verification runner against stored pins.
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay


def _norm(x):
    if x is None:
        return '.'
    if isinstance(x, (list, tuple)):
        return tuple(_norm(v) for v in x)
    return x


def verify_certificate(cert):
    """Returns (True, detail) or raises. No solver imports (pure replay)."""
    word = [(e['mode'], e['key']) for e in cert['events']]
    rr = replay(word, cert['A0'], cert['B0'])
    if _norm(rr['S0'][0]) != _norm(cert['A0']) or _norm(rr['S0'][1]) != _norm(cert['B0']):
        raise AssertionError('start mismatch')
    if _norm(rr['S1'][0]) != _norm(cert['dest_trees'][0]) or _norm(rr['S1'][1]) != _norm(cert['dest_trees'][1]):
        raise AssertionError('final mismatch')
    for i, l in enumerate(rr['legs']):
        rl = cert['rotation_trace'][i] if 'rotation_trace' in cert else None
        if rl is not None and sorted(l.get('push', [])) != sorted(rl.get('push', [])):
            raise AssertionError(('push mismatch', i))
    if [l['dB'] for l in rr['legs'] if l['m'] == 'K'] != cert['B_depths']:
        raise AssertionError('B-depths mismatch')
    if [l['dA'] for l in rr['legs']] != [p['depth'] for p in cert['A_path_depths']]:
        raise AssertionError('A-depths mismatch')
    H, q, w = cert['H'], cert['q'], cert['w']
    if w != 2 * H - q:
        raise AssertionError('w!=2H-q')
    for l in rr['legs']:
        if l['m'] == 'K' and l['q'] != l['dB'] // 2:
            raise AssertionError(('leg q', l))
    return True, {'events': len(word), 'H': H, 'q': q, 'w': w}
