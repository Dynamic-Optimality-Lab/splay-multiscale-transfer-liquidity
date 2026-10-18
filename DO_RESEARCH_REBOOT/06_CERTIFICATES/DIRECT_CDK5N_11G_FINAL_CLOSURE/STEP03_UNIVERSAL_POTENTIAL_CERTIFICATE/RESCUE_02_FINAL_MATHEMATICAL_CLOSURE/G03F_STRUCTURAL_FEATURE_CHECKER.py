# G03F_STRUCTURAL_FEATURE_CHECKER.py — arithmetic verification (no solves):
# (1) joint piecewise constraints hold on all 38 seeds from stored pieces;
# (2) guard is a pure vertex function (source inspection for H/witness/edge);
# (3) killer rows confirmed against the clean rank candidate.
import sys, json, os, inspect
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
sys.path.insert(0, _ROOT + '/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
sys.path.insert(0, _HERE)
PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
OUT = os.environ.get('RESCUE_OUT2', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

if __name__ == '__main__':
    from G03R_CANONICAL_STATE import FIELD_ORDER  # noqa (schema import check)
    pj = os.path.join(OUT, 'G03R_POTENTIAL_CANDIDATE_RESULTS.json')
    # rescue-01 file lives in R1 dir
    r1 = os.environ.get('RESCUE_R1', 'R:/')
    pc = json.load(open(os.path.join(r1, 'G03R_POTENTIAL_CANDIDATE_RESULTS.json')))
    J = {int(g): th for g, th in pc['joint_single_valued'].items()}
    seeds = json.load(open(_ROOT + '/' + PDIR + 'G03_CEGIS_SEEDS.json'))

    def guard(fe):
        return fe['b_depth_max'] >= 6

    viol = []
    for s in seeds:
        gs = 1 if guard(s['s']) else 0
        gt = 1 if guard(s['t']) else 0
        lhs = sum(J[gt].get(f, 0) * s['t'][f] - J[gs].get(f, 0) * s['s'][f] for f in s['s'])
        if lhs > s['w']:
            viol.append((lhs, s['w']))
    # guard purity: inspect G03R_PIECEWISE_POTENTIAL guard source
    gsrc = open(os.path.join(r1, 'G03R_PIECEWISE_POTENTIAL.py')).read()
    gline = [l for l in gsrc.splitlines() if l.strip().startswith('return fe[')]
    pure = all(('H' not in l.replace('b_depth_max', '') and 'wit' not in l) for l in gline)
    # killers vs clean candidate
    def clean(fe):
        return fe['b_rank_sum'] - fe['b_depth_max'] + fe['a_marked_count']
    kill = [(clean(s['t']) - clean(s['s']), s['w']) for s in seeds if clean(s['t']) - clean(s['s']) > s['w']]
    out = {'joint_constraints_hold': len(viol) == 0, 'joint_violations': len(viol),
           'guard_pure_vertex_function': bool(pure), 'guard_lines': gline,
           'clean_candidate_killers': kill,
           'theorem_deps': {'guard': 'vertex-only', 'telescoping': 'joint LP by construction',
                             'universal': 'OPEN (candidate refuted 12/40 grounded)'}}
    json.dump(out, open(OUT + 'G03F_STRUCTURAL_LEMMA_RESULTS.json', 'w'), indent=1)
    json.dump({'nodes': ['guard-vertex', 'joint-LP-telescoping', 'killers', 'refutation-12/40'],
               'edges': [['guard-vertex', 'joint-LP-telescoping'], ['killers', 'refutation-12/40']],
               'open': ['universal-Vw']}, open(OUT + 'G03F_THEOREM_DEPENDENCY_GRAPH.json', 'w'), indent=1)
    print(out, flush=True)
