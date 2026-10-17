# S02_WITNESS_EXTRACTOR.py — complete model reconstruction (Gate I, 18 items).
# Source data (candidate A0/B0/Sset/M/word + replay legs/pairs + verified env) is
# reorganized into the mandated certificate; nothing is invented (all values measured
# from the replay/env). Core validated via core_of; w=2H-q checked arithmetically.
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
import splay as S
from CRA_pointer_tuple_replay import core_of


def _path_on(tree, key):
    """BST search path root->key (keys) or None."""
    path = []
    n = tree
    while n[0] != 'leaf':
        _, k, l, r = n
        path.append(k)
        if key == k:
            return path
        n = l if key < k else r
    return None


def _from_serial(ps):
    if ps is None or ps == '.':
        return S.LEAF
    k, l, r = ps
    return S.node(k, _from_serial(l), _from_serial(r))


def _to_dot(n):
    if n[0] == 'leaf':
        return '.'
    _, k, l, r = n
    return (k, _to_dot(l), _to_dot(r))


def extract_certificate(result, s_pins, t_pins):
    """result: engine SAT dict. Returns 18-item certificate (raises on any check)."""
    A0 = _from_serial(result['A0'])
    B0 = _from_serial(result['B0'])
    word = [tuple(w) for w in result['word']]
    Sset = set(result['Sset'])
    M = set(result['M'])
    legs = result['replay']
    # pairs recomputed by fresh replay in S02_INDEPENDENT_REPLAY; paths here:
    pairs = result.get('pairs')
    cert = {}
    cert['A0'] = result['A0']
    cert['B0'] = result['B0']
    universe = sorted(S.inorder(A0))
    assert set(universe) == set(S.inorder(B0)), 'A/B universe mismatch'
    cert['universe'] = universe
    cert['M'] = sorted(M)
    core = core_of(_to_dot(B0), M)
    # Edge-level core: marked paths (C_M of this edge's B_0). The nine-core invariant
    # (|C_M|=9) holds for admissible CLOSED walks (Step-04 territory), not single edges:
    # even the historical fixture has a 7-core here. Require M ⊆ core ⊆ universe.
    assert core is not None and set(core) >= M and set(core) <= set(universe), ('core', core)
    assert len(core) <= 9
    cert['core'] = sorted(core)
    cert['fringe'] = sorted(set(universe) - Sset)
    cert['events'] = [{'mode': m, 'key': k} for (m, k) in word]
    cert['accessed_keys'] = [k for (_, k) in word]
    cert['modes'] = [m for (m, _) in word]
    # per-event A paths+depths from the RECORDED intermediate trees (same trees the
    # authoritative replay used) via BST descent; cross-checked against replay depths.
    # (No independent splay reimplementation: replay is authoritative.)
    assert pairs is not None and len(pairs) == len(word) + 1, (len(pairs) if pairs else None, len(word))
    aper = []
    for i, (m, k) in enumerate(word):
        tree_i = _from_serial(pairs[i][0])
        p = _path_on(tree_i, k)
        assert p is not None, ('A key absent pre-access', i, k)
        assert len(p) - 1 == legs[i]['dA'], ('A-depth mismatch vs replay', i)
        aper.append(p)
    cert['A_path_depths'] = [{'path': p, 'depth': len(p) - 1} for p in aper]
    bdep = [l['dB'] for l in legs if l['m'] == 'K']
    cert['B_depths'] = bdep
    cert['rotation_trace'] = [{'event': i, 'push': l.get('push', [])} for i, l in enumerate(legs)]
    cert['intermediates'] = pairs
    H, q, w = result['H'], result['q'], result['w'] if 'w' in result else None
    cert['H'] = H
    cert['q'] = q
    cert['w'] = w
    assert w == 2 * H - q, ('w!=2H-q', w, H, q)
    cert['dest_trees'] = pairs[-1] if pairs else None
    cert['dest_abstract'] = dict(t_pins)
    assert all(v is not None for v in cert.values())
    assert len(cert) == 18, len(cert)
    return cert
