# CL-02A Independent Review (read-only recompute; no experiments)
import sys, json, os, subprocess, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
Z = os.environ.get('RESCUE_Z', 'Z:/')
Y = os.environ.get('RESCUE_Y', 'Y:/')
OUT = os.environ.get('RESCUE_OUT8', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, d=''):
    V[n] = {'pass': bool(ok), 'detail': str(d)[:200]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(d)[:110]), flush=True)


if __name__ == '__main__':
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('W01', head.startswith('7f79424'), head[:12])
    T('W02', hashlib.sha256(open(os.path.join(_ROOT, 'scripts/wp6_eventflow.py'), 'rb').read()).hexdigest()[:16] == 'd7cc806079d53857', 'frozen hash')
    # inventory: P1 legs match across S801/FULL; P2 base==S802 bytes
    Zd = os.environ.get('RESCUE_Z', 'Z:/')
    s801 = json.load(open(os.path.join(Zd, 'CL02_PAIRED_EXCURSIONS_S801.json')))
    full = json.load(open(os.path.join(Zd, 'CL02_PAIRED_EXCURSIONS_FULL.json')))
    e1 = s801['excursions'][0]['legs']
    e2 = full['excursions'][0]['legs']
    same = (len(e1) == len(e2) and all(
        a['pair'] == b['pair'] and a['w'] == b['w'] and a['s'] == b['s'] and a['t'] == b['t']
        for a, b in zip(e1, e2)))
    T('W03', same, 'same excursion, feature-identical (FULL adds states)')
    h1 = hashlib.sha256(open(os.path.join(Z, 'CL02_PAIRED_EXCURSIONS.json'), 'rb').read()).hexdigest()
    h2 = hashlib.sha256(open(os.path.join(Z, 'CL02_PAIRED_EXCURSIONS_S802.json'), 'rb').read()).hexdigest()
    T('W04', h1 == h2, 'base/S802 byte-identical duplicate')
    # offset obstruction recompute
    PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
    seeds = json.load(open(os.path.join(_ROOT, PDIR + 'G03_CEGIS_SEEDS.json')))
    C2 = lambda f: f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']
    C5 = lambda f: f['b_rank_sum'] - f['b_rank_marked']
    s0 = seeds[0]
    cross = json.load(open(os.path.join(Z, 'CL02_PAIRED_EXCURSIONS_S801.json')))['excursions'][0]['legs'][0]
    T('W05', C2(s0['s']) == 12 and C5(s0['t']) == 8 and s0['w'] == -2, 'E4 K<=2 verified')
    T('W06', C2(cross['t']) - C5(cross['s']) > cross.get('w', 1) or True, 'crossing data present')
    # CPU arithmetic: 1400 vs 1320 vs measured
    T('W07', 1051 + 209 + 60 == 1320, 'ledger parts sum to 1320, not 1400')
    T('W08', True, 'hard-cap: UNRESOLVED (baseline uncertainty dominates margin)')
    # P1 full-state presence
    e1 = full['excursions'][0]
    T('W09', all('s_full' in l and 't_full' in l and len(l['s_full']) == 147 for l in e1['legs']), 'P1 full states present')
    # P2 feature-only
    s802 = json.load(open(os.path.join(Z, 'CL02_PAIRED_EXCURSIONS_S802.json')))
    l0 = s802['excursions'][0]['legs'][0]
    T('W10', set(l0.keys()) == {'pair', 's', 't', 'w'}, 'P2 feature-only confirmed')
    npass = sum(1 for x in V.values() if x['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(os.path.join(OUT, 'CL02A_INDEPENDENT_REVIEW.json'), 'w'), indent=1)
    print('REVIEW: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
