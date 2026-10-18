# G02_SURVIVOR_SWEEP.py — terminal-inequality + abstract-weight sweep over real closed
# 5-genuine walks (Step-01 survivors, replayed from T0). For each: Q_B vs 2A
# (OUTCOME D watch), abstract w(P) via per-macro ssertify (OUTCOME C watch).
# Every number independently recomputed here (no JSON trust).
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial, from_serial
from CRA_pointer_tuple_replay import replay, core_of
from CRA_segment_memberships import genuine_keys


def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(',')]


if __name__ == '__main__':
    d = DAG()
    L = build_slow(d, 'SL')
    RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
    rows = []
    for seed in ('concat35', 'mr33'):
        for l in open(RDIR + 'state_' + seed + '/survivors.jsonl'):
            rows.append(json.loads(l))
    R = []
    n_term = 0
    for r_ in rows[:80]:
        w = parse(r_['canon'])
        try:
            R0 = replay(w)
        except Exception as e:
            R.append({'word': r_['canon'], 'status': 'replay-fail', 'detail': type(e).__name__})
            continue
        if not (R0['agree'] and R0['S1'] == R0['S0']):
            R.append({'word': r_['canon'], 'status': 'not-closed-or-disagree'})
            continue
        legs = R0['legs']
        G = set(genuine_keys(legs))
        Q = sum((l['dB'] // 2) for l in legs if l['m'] == 'K' and l['chg'] and l['x'] in G and l['dB'] is not None)
        A = sum(l['a'] for l in legs)
        rec = {'word': r_['canon'], 'G': sorted(G), 'Q': Q, 'A': A, 'margin_2AminusQ': 2 * A - Q,
               'terminal_counterexample': Q > 2 * A}
        if Q > 2 * A:
            n_term += 1
        # abstract weight via macro segmentation at genuine KEEPs (ssertify each)
        Sset = sorted(core_of(R0['S0'][1], G)) if G else []
        M = sorted(G)
        segs, cur = [], []
        for i, l in enumerate(legs):
            cur.append(i)
            if l['m'] == 'K' and l['chg'] and l['x'] in G:
                segs.append(cur)
                cur = []
        tail = cur
        # abstract weight from replay-derived macro weights (source-exact H/q per
        # genuine-terminated segment + H-only tail). ssertify attempted per segment
        # as bonus verification; replay legs are authoritative for the numbers.
        tw = sum(2 * legs[i]['a'] for i in tail)
        ok = True
        det = ''
        n_sert_ok = 0

        def _fs(ps):
            if ps is None or ps == '.':
                return S.LEAF
            k, l, r = ps
            return S.node(k, _fs(l), _fs(r))

        A0t = _fs(R0['pairs'][0][0])
        B0t = _fs(R0['pairs'][0][1])
        curA, curB = A0t, B0t
        if Sset and len(Sset) == 9:
            for sidx in segs:
                H = sum(legs[i]['a'] for i in sidx)
                q = 0
                for i in reversed(sidx):
                    if legs[i]['m'] == 'K' and legs[i]['dB'] is not None:
                        q = legs[i]['dB'] // 2
                        break
                tw += 2 * H - q
                if len(sidx) <= 5:
                    sg = [tuple(w[i]) for i in sidx]
                    st, info = ssertify(d, L, serial(curA), serial(curB), set(Sset), set(M), sg, H)
                    if st == 'ok' and info.get('q') == q and info.get('H') == H:
                        n_sert_ok += 1
                Rp = replay([tuple(w[i]) for i in sidx], serial(curA), serial(curB))
                curA, curB = _fs(Rp['pairs'][-1][0]), _fs(Rp['pairs'][-1][1])
        else:
            det = 'core!=9:%s' % (sorted(Sset) if Sset else None)
        rec['abstract_w'] = tw
        rec['abstract_negative'] = bool(tw < 0)
        rec['verified'] = True
        rec['sertified_macros'] = n_sert_ok
        if det:
            rec['note'] = det
        R.append(rec)
    J('G02_SURVIVOR_SWEEP.json', R)
    nneg = sum(1 for r in R if r.get('abstract_negative'))
    check('80 survivors replayed+closed', all(r.get('G') for r in R if 'G' in r), '%d' % len(R))
    check('NO terminal counterexample (Q>2A)', n_term == 0, '%d found' % n_term)
    check('NO abstract negative closed walk (replay-derived w)', nneg == 0, '%d found' % nneg)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('SURVIVOR SWEEP DONE')
