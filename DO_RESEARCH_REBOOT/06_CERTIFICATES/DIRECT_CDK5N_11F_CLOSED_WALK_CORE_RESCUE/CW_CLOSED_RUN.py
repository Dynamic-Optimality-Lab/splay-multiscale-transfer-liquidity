# CW_CLOSED_RUN.py — Gate E/J evidence: admissible closed walks with S := stable C_M.
import sys, json, random, copy
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial, core_of
from CRA_segment_memberships import genuine_keys, keep_support
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial, depths_keys, AModel

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/'
RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'


def CM_of(B, M):
    dk = depths_keys(B)
    out = set()
    for m in M:
        if m not in dk:
            return None
        a = m
        while a is not None:
            out.add(a)
            a = dk[a][1]
    return out


def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(',')]


if __name__ == '__main__':
    d = DAG()
    L = build_slow(d, 'SL')
    print('built strict-low: nodes=%d' % d.count(), flush=True)
    rows = []
    for seed in ('concat35', 'mr33'):
        for l in open(RDIR + 'state_' + seed + '/survivors.jsonl'):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r['canon'], []).append(r)
    WORDS = sorted(bycanon)[:40]
    nok = nskip = 0
    skips = {}
    negs = []
    nwalks = 0
    for cwi, cw in enumerate(WORDS):
        if cwi % 10 == 0:
            print('... walk %d/%d ok=%d' % (cwi, len(WORDS), nok), flush=True)
        w = parse(cw)
        try:
            R = replay(w)
        except Exception:
            continue
        if not (R['S1'] == R['S0'] and R['agree']):
            continue
        G = set(genuine_keys(R['legs']))
        K = set(keep_support(R['legs']))
        if len(G) != 5 or K != G:
            continue
        # C_M constancy + 9-count (Gates B/C tripwires)
        first = None
        okc = True
        for ps in R['pairs']:
            c = CM_of(from_serial(ps[1]), G)
            if first is None:
                first = c
            if c != first:
                okc = False
                break
        if not okc or first is None or len(first) != 9:
            skips['nonconst-core'] = skips.get('nonconst-core', 0) + 1
            continue
        nwalks += 1
        Sset = set(first)
        Ss = sorted(Sset)
        mu_mask = sorted(Ss.index(m) for m in G)
        M = set(G)
        # segment at genuine KEEPs; certify each H<=2 segment with S := C_M
        segs = []
        cur = []
        for acc, l in zip(w, R['legs']):
            cur.append(acc)
            if l['m'] == 'K' and l['x'] in M and l['chg']:
                segs.append(list(cur))
                cur = []
        idx = 0
        nseg = 0
        for seg in segs:
            from PC_CONCRETIZE import serial as _serial
            A0ll = _serial(from_serial(R['pairs'][idx][0]))
            B0ll = _serial(from_serial(R['pairs'][idx][1]))
            idx += len(seg)
            seglegs = R['legs'][idx - len(seg):idx]
            H = sum(l['a'] for l in seglegs)
            if H > 2:
                nskip += 1
                skips['high-seg'] = skips.get('high-seg', 0) + 1
                continue
            nseg += 1
            if nseg > 6:
                skips['seg-cap'] = skips.get('seg-cap', 0) + 1
                continue
            import copy
            st, info = ssertify(d, L, copy.deepcopy(A0ll), copy.deepcopy(B0ll), Sset, M, seg, H)
            if st == 'skip':
                nskip += 1
                skips[info] = skips.get(info, 0) + 1
                continue
            if st == 'fail':
                print('CLOSED-FAIL', cw[:60], seg, str(info)[:150] if isinstance(info, dict) else info)
                raise AssertionError('closed-walk')
            nok += 1
            if info['w'] < 0 and len(negs) < 20:
                negs.append({'word': seg, 'H': info['H'], 'q': info['q'], 'w': info['w']})
    print('closed-walk: walks=%d grounded=%d skipped=%d negatives=%d skips=%s' % (nwalks, nok, nskip, len(negs), skips), flush=True)
    json.dump({'walks': nwalks, 'grounded': nok, 'skipped': nskip, 'skip_reasons': skips, 'negatives': negs},
              open(PDIR + 'CW_LOW_EDGE_RESULTS.json', 'w'), indent=1)
