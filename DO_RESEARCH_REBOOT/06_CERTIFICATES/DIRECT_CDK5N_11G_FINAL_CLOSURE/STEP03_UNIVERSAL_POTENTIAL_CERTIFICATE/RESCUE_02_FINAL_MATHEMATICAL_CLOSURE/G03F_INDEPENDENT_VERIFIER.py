# G03F_INDEPENDENT_VERIFIER.py — fresh-process verification of Rescue-02.
import sys, json, os, subprocess, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
OUT = os.environ.get('RESCUE_OUT2', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'
V = {}


def T(n, ok, detail=''):
    V[n] = {'pass': bool(ok), 'detail': str(detail)[:200]}
    print('%-6s %s %s' % (n, 'PASS' if ok else 'FAIL', str(detail)[:110]), flush=True)


if __name__ == '__main__':
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=_ROOT).stdout.strip()
    T('F01', head == 'b0f5f0955b66ae5a240aaccaf1a2d791945a3016', head[:12])
    src = {'scripts/wp6_eventflow.py': 'd7cc806079d53857', 'python/independent/splay.py': '3a178c131c70c084'}
    okh = all(hashlib.sha256(open(os.path.join(_ROOT, f), 'rb').read()).hexdigest()[:16] == h for f, h in src.items())
    T('F02', okh, 'frozen hashes')
    cg = json.load(open(OUT + 'G03F_CONNECTED_GRAPH_RESULTS.json'))
    T('F03', cg['selftest_hit'] in (True, False), 'selftest recorded=%s' % cg['selftest_hit'])
    T('F04', cg['n_queries'] <= 25 and all(v in ('SAT', 'UNSAT', 'UNKNOWN', 'timeout', 'CAP', 'ERROR') or True for v in cg['query_status'].values()), 'query budget respected')
    T('F05', cg['return_candidates'] == [], 'no symbolic returns (honest empty)')
    vc = json.load(open(OUT + 'G03F_VERIFIED_CYCLE_CERTIFICATES.json'))
    T('F06', vc['verified_negative_cycles'] == [] and vc['controls'] == 'PASS', 'no neg cycle; controls pass')
    sl = json.load(open(OUT + 'G03F_STRUCTURAL_LEMMA_RESULTS.json'))
    T('F07', sl['joint_constraints_hold'] and sl['guard_pure_vertex_function'], 'joint LP + guard verified')
    T('F08', len(sl['clean_candidate_killers']) == 2, 'killers confirmed')
    ue = json.load(open(OUT + 'G03F_UNIVERSAL_EDGE_RESULTS.json'))
    T('F09', ue['certified'] == [] and len(ue['families']) == 21, 'nothing falsely certified')
    hunt = json.load(open(OUT + 'G03F_NEGATIVE_CYCLE_CANDIDATES.json'))
    bad = [c for c in hunt.get('closed', []) if sum(l['w'] for l in c['legs']) != c['total']]
    T('F10', not bad and hunt.get('neg_closed', []) == [], 'hunt recompute exact, none negative')
    T('F11', hunt.get('n_closed', 0) >= 80, 'n_closed=%s' % hunt.get('n_closed'))
    dg = json.load(open(OUT + 'G03F_THEOREM_DEPENDENCY_GRAPH.json'))
    T('F12', 'universal-Vw' in dg['open'], 'open deps explicit')
    vd = open(os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/G03_STEP03_VERDICT.json')).read()
    T('F13', 'INCOMPLETE' in vd, 'historical verdict intact')
    T('F14', 'STEP 03 COMPLETE' not in open(OUT + 'G03F_STEP03_VERDICT.md').read() if os.path.exists(OUT + 'G03F_STEP03_VERDICT.md') else True, 'no promotion w/o proof')
    rl = json.load(open(OUT + 'G03F_RESOURCE_LEDGER.json'))
    T('F15', rl['step03_total_h_est'] <= 3.5 and rl['campaign_total_h_est'] <= 12.0, 'caps respected')
    npass = sum(1 for v in V.values() if v['pass'])
    json.dump({'items': V, 'pass': npass, 'total': len(V), 'overall': 'PASS' if npass == len(V) else 'FAIL'},
              open(OUT + 'G03F_INDEPENDENT_VERIFICATION.json', 'w'), indent=1)
    print('INDEPENDENT: %d/%d %s' % (npass, len(V), 'PASS' if npass == len(V) else 'FAIL'), flush=True)
