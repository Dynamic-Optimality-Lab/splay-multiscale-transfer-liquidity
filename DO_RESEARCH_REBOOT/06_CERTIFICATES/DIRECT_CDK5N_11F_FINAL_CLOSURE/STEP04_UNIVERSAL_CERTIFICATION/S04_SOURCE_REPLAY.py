# S04_SOURCE_REPLAY.py — replay-based checks (E3/E4/corpus legs, gap-pop invariance,
# key-set conservation, rotation agreement). Importable + __main__ evidence.
import sys, json
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/'

import splay as S
from CRA_pointer_tuple_replay import replay, ReplayError

FAIL = []
RES = {}


def check(name, ok, detail=''):
    RES[name] = {'status': 'PASS' if ok else 'FAIL', 'detail': detail}
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


def _from(ps):
    if ps is None or ps == '.':
        return S.LEAF
    k, l, r = ps
    return S.node(k, _from(l), _from(r))


def gap_pops(keys, Sset):
    Ss = sorted(Sset)
    z = [0] * 10
    for k in keys:
        if k not in Sset:
            i = sum(1 for s in Ss if s < k)
            z[i] += 1
    return z


if __name__ == '__main__':
    corp = json.load(open(PDIR.replace('STEP04_UNIVERSAL_CERTIFICATION/', 'STEP02_FREE_WITNESS_SYNTHESIS/') + 'S02_GENERALIZATION_CORPUS.json'))
    nrep = nq = nkey = ngap = 0
    for c in corp:
        if c['grounded'] != 'ok':
            continue
        A = _from(c['A'])
        B = _from(c['B'])
        word = [tuple(w) for w in c['word']]
        try:
            R = replay(word, c['A'], c['B'])
        except Exception as e:
            check('replay ' + c['category'], False, repr(e)[:100])
            continue
        nrep += 1
        Sset = set(c['Sset'])
        for l in R['legs']:
            if l['m'] == 'K' and l['q'] != (l['dB'] // 2 if l['dB'] is not None else 0):
                check('q-shape ' + c['category'], False, str(l))
                break
        else:
            nq += 1
        # key-set conservation (KEEP-only words) + gap-pop invariance (all words)
        ks0 = set(S.inorder(A))
        for (pa, pb) in R['pairs']:
            ka = [k for k in S.inorder(_from(pa))]
            if set(ka) != ks0 and all(m == 'K' for (m, _) in word):
                check('keyset ' + c['category'], False, '')
                break
        else:
            nkey += 1
        pops0 = gap_pops(list(S.inorder(A)), Sset)
        okg = True
        for (pa, pb) in R['pairs']:
            if gap_pops(list(S.inorder(_from(pa))), Sset) != pops0:
                okg = False
                break
        ngap += okg
    check('replays agree', nrep == 10, '%d/10' % nrep)
    check('q-shape legs', nq == 10, '%d/10' % nq)
    check('key-set conservation', nkey == 10, '%d/10' % nkey)
    check('gap-pop invariance', ngap == 10, '%d/10' % ngap)
    json.dump(RES, open(PDIR + 'S04_SOURCE_REPLAY_RESULTS.json', 'w'), indent=1)
    assert not FAIL, FAIL
    print('SOURCE REPLAY PASS')
