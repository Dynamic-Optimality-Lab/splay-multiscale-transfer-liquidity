# G03F_UNIVERSAL_EDGE_CHECKER.py — per-family certification ledger. With no
# surviving candidate there is nothing to certify: every family is honestly
# OPEN. A candidate may only enter this ledger after exact grounded
# falsification survival (none has). Machinery readiness evidenced by the
# Rescue-01 1.6M-node product compile + family-root probe (UNKNOWN recorded).
import sys, json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.environ.get('RESCUE_ROOT', _HERE)
try:
    os.chdir(_ROOT)
except Exception:
    pass
OUT = os.environ.get('RESCUE_OUT2', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

if __name__ == '__main__':
    fams = {}
    for w in range(-4, 5):
        fams['low_OO_w=%d' % w] = 'OPEN-no-candidate'
    for w in range(-4, 7):
        fams['high_contracted_w=%d' % w] = 'OPEN-no-candidate'
    fams['high_w=-3'] = 'OPEN-conditional-UNKNOWN-retained'
    out = {'families': fams, 'certified': [], 'rule': 'no sample-only promotion; UNKNOWN maintained',
           'machinery': 'product compiles (1.6M nodes); family roots present; probes UNKNOWN (Rescue-01)'}
    json.dump(out, open(OUT + 'G03F_UNIVERSAL_EDGE_RESULTS.json', 'w'), indent=1)
    json.dump({'candidates': [], 'status': 'none-surviving',
               'refuted': ['affine-10base', 'poly-degree2', 'rank-affine-15feat', 'depth-guarded-joint-piecewise']},
              open(OUT + 'G03F_POTENTIAL_CANDIDATES.json', 'w'), indent=1)
    print('families OPEN:', len(fams), 'certified: 0', flush=True)
