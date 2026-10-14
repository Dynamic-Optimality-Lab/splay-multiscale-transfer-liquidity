# PP_GUARD_CENSUS.py — distinct port-guard count over corpus H<=2 macros + scale projection.
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial, core_of
from CRA_segment_memberships import genuine_keys
from PP_PORT_ROTATION_TRANSDUCER import cut, splay_skel
from PP_JOINT_INVENTORY import gap_of

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'
RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'


def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(',')]


def skel_shape(skel, Sset):
    if skel[0] == 'E':
        return '.'
    if skel[0] == 'P':
        return 'P'
    _, k, l, r = skel
    tag = ('S%d' % sorted(Sset).index(k)) if k in Sset else 'F'
    return (tag, skel_shape(l, Sset), skel_shape(r, Sset))


if __name__ == '__main__':
    t0 = time.time()
    rows = []
    for l in open(RDIR + 'state_concat35/survivors.jsonl'):
        rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r['canon'], []).append(r)
    WORDS = sorted(bycanon)[:150]
    guards = set()
    nmacro = nclosed = 0
    masks_seen = set()
    flow_t = 0
    for cw in WORDS:
        w = parse(cw)
        try:
            R = replay(w)
        except Exception:
            continue
        if not (R['S1'] == R['S0'] and R['agree']):
            continue
        nclosed += 1
        Sset = core_of(R['pairs'][0][1])
        if Sset is None or len(Sset) != 9:
            continue
        Ss = sorted(Sset)
        rk = {k: i for i, k in enumerate(Ss)}
        gen = genuine_keys(R['legs'])
        # slice post-KEEP H<=2 macros between genuine KEEP legs
        cur = []
        H = 0
        A = from_serial(R['pairs'][0][0])
        segs = []
        # walk legs; accumulate until genuine KEEP boundary
        start_idx = 0
        for idx, l in enumerate(R['legs']):
            cur.append((l['m'], l['x']))
            H += l['a']
            if l['m'] == 'K' and l['x'] in gen and l['chg'] and idx > start_idx:
                segs.append((start_idx, list(cur)))
                cur = []
                H = 0
                start_idx = idx
        # evaluate segments with H<=2 (H from legs)
        for (s0, seg) in segs:
            Hseg = sum(R['legs'][s0 + j]['a'] for j in range(len(seg)))
            if Hseg > 2 or not seg:
                continue
            nmacro += 1
            A0 = from_serial(R['pairs'][s0][0])
            skel, ports = cut(A0, set(Sset))
            # word pattern in S-ranks (fringe-aware: rank or F)
            pat = tuple((m, rk[x] if x in rk else 'F') for (m, x) in seg)
            # rotation cases via port engine
            sk = skel
            cases = []
            for (m, x) in seg:
                sk, evs = splay_skel(sk, x)
                cases.extend(evs)
            hid = tuple(sorted((len(v['hidden_S']) for v in ports.values())))
            M = tuple(sorted({l['x'] for l in R['legs'][s0:s0 + len(seg)] if l['m'] == 'K' and l['chg']} & set(gen)))
            masks_seen.add(tuple(sorted(rk[x] for x in M))) if M and all(x in rk for x in M) else None
            guards.add((str(skel_shape(skel, set(Sset))), pat, tuple(cases), hid))
    dt = time.time() - t0
    print('words-closed=%d macros=%d distinct-guards=%d masks=%d time=%.1fs' % (nclosed, nmacro, len(guards), len(masks_seen), dt), flush=True)
    guards_9key = len(guards)
    # FRINGE scope: random universes n=10..24, sliding H<=2 windows (closure NOT required for guards)
    frng = random.Random(31)
    fmacro = 0
    for trial in range(400):
        n = frng.randint(10, 24)
        ks = list(range(1, n + 1))
        S9 = set(frng.sample(ks, 9))
        Ss = sorted(S9)
        rk = {k: i for i, k in enumerate(Ss)}
        t = S.LEAF
        ins = sorted(ks)
        if frng.random() < 0.5:
            frng.shuffle(ins)
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ins:
            t = _ins(t, k)
        def _tl(t):
            return None if t[0] == 'leaf' else [t[1], _tl(t[2]), _tl(t[3])]
        T = _tl(t)
        Sall = ks
        word = [(('K' if frng.random() < 0.7 else 'D'), frng.choice(Sall)) for _ in range(frng.randint(4, 12))]
        try:
            R = replay(word, A0=T, B0=T)
        except Exception:
            continue
        if not R['agree']:
            continue
        # sliding windows with sum(a)<=2 over K/D legs (A-side H)
        legs = R['legs']
        for s0 in range(len(legs)):
            H = 0
            seg = []
            for j in range(s0, len(legs)):
                H += legs[j]['a']
                if H > 2:
                    break
                seg.append((legs[j]['m'], legs[j]['x']))
                if seg:
                    A0 = from_serial(R['pairs'][s0][0])
                    try:
                        skel, ports = cut(A0, S9)
                    except Exception:
                        break
                    pat = tuple((m, rk[x] if x in rk else 'F') for (m, x) in seg)
                    sk = skel
                    cases = []
                    try:
                        for (m, x) in seg:
                            sk, evs = splay_skel(sk, x)
                            cases.extend(evs)
                    except Exception:
                        break
                    hid = tuple(sorted((len(v['hidden_S']) for v in ports.values())))
                    guards.add((str(skel_shape(skel, S9)), pat, tuple(cases), hid))
                    fmacro += 1
    dt2 = time.time() - t0
    print('fringe-macros=%d distinct-guards(total)=%d time=%.1fs' % (fmacro, len(guards), dt2), flush=True)
    # projection: 9-key guards scale (at minimum) with masks: 126/5 x guards_9key
    proj_masks = 126 * guards_9key // max(1, len(masks_seen))
    json.dump({'closed_words': nclosed, 'macros': nmacro, 'fringe_macros': fmacro,
               'distinct_guards_9key': guards_9key, 'distinct_guards': len(guards),
               'masks_seen': len(masks_seen), 'mask_projection_9key': proj_masks, 'time_s': round(dt2, 1)},
              open(PDIR + 'PP_GUARD_CENSUS.json', 'w'), indent=1)
