# CW_CLOSED_WALK_PROBE.py — Gate C/D measurements on exactly-closed corpus words.
import sys, json, random
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from CRA_pointer_tuple_replay import replay, from_serial, core_of
from CRA_segment_memberships import genuine_keys, keep_support
from PC_CONCRETIZE import depths_keys

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
    rows = []
    for seed in ('concat35', 'mr33'):
        for l in open(RDIR + 'state_' + seed + '/survivors.jsonl'):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r['canon'], []).append(r)
    WORDS = sorted(bycanon)[:200]
    nclosed = nadm = nkeqg = nconst = 0
    frinst = []
    for cw in WORDS:
        w = parse(cw)
        try:
            R = replay(w)
        except Exception:
            continue
        if not (R['S1'] == R['S0'] and R['agree']):
            continue
        nclosed += 1
        G = set(genuine_keys(R['legs']))
        K = set(keep_support(R['legs']))
        if len(G) != 5:
            continue
        # core-9 wrt G (not MSET): all pair states
        Sset = None
        ok9 = True
        for ps in R['pairs']:
            c = core_of(ps[1], G)
            if c is None or len(c) != 9:
                ok9 = False
                break
        if not ok9:
            continue
        nadm += 1
        if K != G:
            print('K!=G on admissible closed word!', cw[:80])
            continue
        nkeqg += 1
        # C_G constancy across pair states + size census
        first = None
        const = True
        sizes = set()
        for ps in R['pairs']:
            B = from_serial(ps[1])
            c = CM_of(B, G)
            if c is None:
                const = False
                break
            sizes.add(len(c))
            if first is None:
                first = c
            if c != first:
                const = False
        if const:
            nconst += 1
        if len(frinst) < 5:
            frinst.append({'word': cw[:60], 'Csize': sorted(sizes), 'const': const})
    print('closed=%d admissible(|G|=5,core9-G)=%d K==G:%d Cconst:%d' % (
        nclosed, nadm, nkeqg, nconst), flush=True)
    json.dump({'closed': nclosed, 'admissible': nadm, 'keqg': nkeqg, 'cconst': nconst,
               'samples': frinst},
              open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_CORE_INVARIANCE_TESTS.json', 'w'), indent=1)
