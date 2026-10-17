# S02_MACRO_SKELETONS.py — symbolic macro-skeleton family (Gate C3 + Tier-2 fallback).
# Skeletons = (nev, evK[0..4]) pin-sets with terminal KEEP. Family: nev 1..5,
# evK patterns with evK[nev-1]=1: 1+2+4+8+16 = 31 skeletons. COMPLETE over the
# relation-allowed (nev,evK) space by the relation's own bounds (nev<=5 from
# LE(wit.nev,5); terminal KEEP asserted via mux_ref(evK,last)). Grammar norms
# (DELETE-before-KEEP, repeats, nongenuine, zero-cost, 1-2-access, 3-5-event) are
# ORDERING within the 31 (norm-first), never exclusion: full family always available.
import itertools

NORMS = ['single-keep', 'zero-cost-root', 'delkeep', 'repeat', 'nongenuine', 'multi']


def classify(nev, evK):
    n = nev
    pat = tuple(evK[:n])
    if n == 1 and pat == (1,):
        return 'single-keep'
    if n == 2 and pat == (0, 1):
        return 'delkeep'
    if len(set(pat)) == 1 and pat[0] == 1 and n > 1:
        return 'repeat'
    return 'multi'


def skeletons(order='norm-first'):
    fams = []
    for nev in range(1, 6):
        for bits in itertools.product([0, 1], repeat=nev - 1):
            evK = tuple(list(bits) + [1])
            fams.append((nev, evK, classify(nev, evK)))
    if order == 'norm-first':
        rank = {'single-keep': 0, 'zero-cost-root': 1, 'delkeep': 1, 'repeat': 2,
                'nongenuine': 2, 'multi': 3}
        fams.sort(key=lambda s: (rank.get(s[2], 3), s[0], s[1]))
    return fams


def skeleton_pins(nev, evK, H=None, q=None):
    pins = {'SLw_nev': nev}
    for e in range(5):
        pins['SLw_eK%d' % e] = bool(evK[e]) if e < len(evK) else False
    if H is not None:
        pins['SL_H'] = H
    if q is not None:
        pins['SLbt_q'] = q
    return pins


def coverage():
    fams = skeletons()
    assert len(fams) == 31
    assert all(f[1][f[0] - 1] == 1 for f in fams)  # terminal KEEP throughout
    assert all(sum(1 for f in fams if f[0] == n) == 2 ** (n - 1) for n in range(1, 6))
    return {'n': 31, 'by_nev': {n: 2 ** (n - 1) for n in range(1, 6)}, 'terminal_keep': True}
