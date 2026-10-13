# WQ regressions A/B/C (frozen canonical words).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]
rec = {}
words = {
    'A-SELR-OUT': ('D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9', (30, 52, 36)),
    'B-zeroGamma': ('D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,D3,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9', (31, 53, 36)),
    'C-zeroA': ('D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D1,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9', (29, 50, 36)),
}
for tag, (cw, ex) in words.items():
    R = replay(parse(cw), A0=T0, B0=T0)
    A = sum(l['a'] for l in R['legs'])
    Q = sum(l['q'] for l in R['legs'])
    assert (len(parse(cw)), A, Q) == ex, (tag, len(parse(cw)), A, Q)
    assert R['S1'] == R['S0'] and R['agree']
    rec[tag] = {'n': ex[0], 'A': A, 'Q': Q, 'closed': True}
print('A/B/C PASS', flush=True)
json.dump(rec, open(PDIR + 'WQ_REGRESSIONS.json', 'w'), indent=1)
