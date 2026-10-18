# G03_CEGIS_LOOP.py — bounded CEGIS iterations (affine family).
# fit -> falsify-on-random-grounded -> add violations -> refit (<=3 rounds).
# Outcome: stable candidate or TEMPLATE-INSUFFICIENT with obstruction data.
import sys, json, subprocess
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'

from G03_CANDIDATE_SYNTHESIS import fit_affine_on, RANK_FEATS

PY = 'python'

USE_FEATS = RANK_FEATS


def run_falsify(n, seed, mode='mix'):
    r = subprocess.run([PY, PDIR + 'G03_GROUNDED_FALSIFY.py', str(n), str(seed), mode],
                       capture_output=True, text=True, timeout=1700)
    print(r.stdout[-500:], flush=True)
    if r.returncode != 0:
        print('FALSIFY-ERR', r.stderr[-2000:], flush=True)
        return None
    return json.load(open(PDIR + 'G03_FALSIFY_RUN.json'))


if __name__ == '__main__':
    import sys as _s
    nrounds = int(_s.argv[1]) if len(_s.argv) > 1 else 3
    seedbase = int(_s.argv[2]) if len(_s.argv) > 2 else 100
    modes = (_s.argv[3] if len(_s.argv) > 3 else 'mix').split(',')
    seeds = json.load(open(PDIR + 'G03_CEGIS_SEEDS.json'))
    try:
        trace = json.load(open(PDIR + 'G03_CEGIS_TRACE.json'))
        hist = trace.get('history', [])
    except Exception:
        hist = [{'round': 0, 'nseeds': 10, 'result': 'init'}]
    seen = set()
    for s in seeds:
        seen.add(json.dumps([s['s'], s['t'], s['w']], sort_keys=True))
    rnd0 = max([h.get('round', 0) for h in hist] + [0])
    cand = None
    stable = False
    for rnd in range(rnd0 + 1, rnd0 + 1 + nrounds):
        got, why = fit_affine_on(seeds, USE_FEATS, bound=None)
        if got is None:
            hist.append({'round': rnd, 'nseeds': len(seeds), 'result': 'UNSAT-refit', 'detail': why})
            cand = None
            break
        cand = got
        json.dump({'family': 'rank-affine', 'theta': got[0], 'c': got[1]}, open(PDIR + 'G03_CANDIDATE_POTENTIAL.json', 'w'))
        print('round %d fit nseeds=%d:' % (rnd, len(seeds)),
              {k: v for k, v in got[0].items() if v != 0}, got[1], flush=True)
        fr = run_falsify(30, seedbase + rnd, modes[(rnd - rnd0 - 1) % len(modes)])
        if fr is None:
            hist.append({'round': rnd, 'result': 'falsify-error'})
            break
        hist.append({'round': rnd, 'result': 'falsified', 'tried': fr['tried'],
                     'ok': fr['ok'], 'nviol': len(fr['violations'])})
        new = 0
        for v in fr['violations']:
            key = json.dumps([v['s'], v['t'], v['w']], sort_keys=True)
            if key not in seen:
                seen.add(key)
                seeds.append({'s': v['s'], 't': v['t'], 'w': v['w'], 'origin': 'cegis-r%d' % rnd})
                new += 1
        print('round %d: %d new violations added (total seeds %d)' % (rnd, new, len(seeds)), flush=True)
        if new == 0 and fr['tried'] > 0 and len(fr['violations']) == 0:
            stable = True
            hist.append({'round': rnd, 'result': 'STABLE-40-random'})
            break
        if new == 0:
            break
    json.dump({'history': hist, 'stable': stable, 'nseeds': len(seeds),
               'candidate': {'theta': cand[0], 'c': cand[1]} if cand else None},
              open(PDIR + 'G03_CEGIS_TRACE.json', 'w'), indent=1)
    json.dump(seeds, open(PDIR + 'G03_CEGIS_SEEDS.json', 'w'), indent=1)
    print('done stable=%s nseeds=%d' % (stable, len(seeds)), flush=True)
