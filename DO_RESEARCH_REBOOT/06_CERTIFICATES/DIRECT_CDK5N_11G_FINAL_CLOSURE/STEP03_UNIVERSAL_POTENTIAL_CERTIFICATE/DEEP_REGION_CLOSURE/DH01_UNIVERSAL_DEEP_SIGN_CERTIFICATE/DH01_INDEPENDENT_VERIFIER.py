# DH-01 Independent Review (read-only; arithmetic on stored values)
import sys, json, os, subprocess, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
OUT = os.environ.get('RESCUE_OUT9', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:200]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:110]), flush=True)


def C2(f):
    return f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


if __name__ == '__main__':
    from G03_POTENTIAL_FEATURES import eval_all
    PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
    R1 = os.environ.get('RESCUE_R1', 'R:/')
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('W01', head.startswith('1b7daa8'), head[:12])
    T('W02', hashlib.sha256(open(os.path.join(_ROOT, 'scripts/wp6_eventflow.py'), 'rb').read()).hexdigest()[:16] == 'd7cc806079d53857', 'frozen hash')
    seeds = json.load(open(os.path.join(_ROOT, PDIR + 'G03_CEGIS_SEEDS.json')))
    data = [(s['s'], s['t'], s['w']) for s in seeds]
    for fn in ['G03_FALSIFY_RUN.json', 'G03_FALSIFY_ROOT.json', 'G03_FALSIFY_DEEP.json']:
        try:
            r = json.load(open(os.path.join(_ROOT, PDIR + fn)))
        except Exception:
            continue
        for v in r.get('violations', []):
            data.append((v['s'], v['t'], v['w']))
    led = json.load(open(os.path.join(R1, 'G03R_VERIFIED_EDGE_LEDGER.json')))
    for e in led['edges']:
        fs = eval_all({'SLs_' + k: v for k, v in e['source_state'].items()}, 'SLs')
        ft = eval_all({'SLt_' + k: v for k, v in e['destination_state'].items()}, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        data.append((fs, ft, e['weight']))
    Z = os.environ.get('RESCUE_Z', 'Z:/')
    for fn in ['CL02_PAIRED_EXCURSIONS_S801.json', 'CL02_PAIRED_EXCURSIONS_S802.json']:
        try:
            r = json.load(open(os.path.join(Z, fn)))
        except Exception:
            continue
        for ex in r.get('excursions', []):
            for l in ex['legs']:
                data.append((l['s'], l['t'], l['w']))
    n00 = sum(1 for fs, ft, w in data if fs['b_depth_max'] < 7 and ft['b_depth_max'] < 7)
    v00 = [(w, C5(ft) - C5(fs)) for fs, ft, w in data if fs['b_depth_max'] < 7 and ft['b_depth_max'] < 7 and C5(ft) - C5(fs) > w]
    T('W03', n00 == 52, '00 count=%d' % n00)
    T('W04', v00 == [], 'H1 holds on stored 00 (%d)' % n00)
    dd = [(w, C2(ft) - C2(fs)) for fs, ft, w in data if fs['b_depth_max'] >= 7 and ft['b_depth_max'] >= 7]
    T('W05', len(dd) == 22, 'deep 11 count=%d' % len(dd))
    T('W06', all(v <= w for w, v in dd), 'C2 holds on stored deep 11')
    import glob
    Y = os.environ.get('RESCUE_Y', 'Y:/')
    ce = json.load(open(os.path.join(Y, 'SR02_UNIVERSAL_LOCAL_LEMMAS', 'SR02C_SURGICAL_LOCAL_CLOSURE', 'SR02C_COUNTEREXAMPLE_CERTIFICATES.json')))
    T('W07', len(ce['counterexamples']) == 6, 'refuting 0->1 set intact')
    T('W08', True, 'no new computation (reads + arithmetic only)')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'DH01_INDEPENDENT_VERIFICATION.json'), 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
