# UFRL regressions A-C replays (+ D/E/F refs recorded from COST-CONE campaign).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]
rec = {}
words = {
    'A-SELR-OUT': 'D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9',
    'B-zeroGamma': 'D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,D3,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9',
    'C-zeroA': 'D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D1,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9',
}
for tag, cw in words.items():
    R = replay(parse(cw), A0=T0, B0=T0)
    A = sum(l['a'] for l in R['legs'])
    Q = sum(l['q'] for l in R['legs'])
    rec[tag] = {'n': len(parse(cw)), 'A': A, 'Q': Q,
                'closed': bool(R['S1'] == R['S0'] and R['agree'])}
rec['D-vine-Q14'] = {'ref': 'COST-CONE CC_regress.py PASS (depths 8,2,4,4,4,2,2,2)'}
rec['E-rootswitch-Q18'] = {'ref': 'COST-CONE CC_regress.py PASS (unique 9-key start 1/4862)'}
rec['F-projection'] = {'ref': 'COST-CONE CC_regress.py PASS (prune/splay non-commute reproduced)'}
rec['G-frontier-multiplicity'] = {'fuzz': '52 cases, 0 mismatch (this campaign)'}
rec['H-hidden-core'] = {'fuzz': 'comb + vine cases in UFRL_FUZZ/FUZZ_ADV, 0 mismatch'}
rec['I-saturation'] = {'fuzz': 'gaps 264/265/266/267/600/2000 in UFRL_FUZZ_ADV, 0 mismatch'}
rec['J-two-access-cone'] = {'fuzz': '8 cross-type (LL/ZIG/LR/RL/RR) cases, 0 mismatch'}
print(rec, flush=True)
assert rec['A-SELR-OUT']['A'] == 52 and rec['A-SELR-OUT']['Q'] == 36
assert rec['B-zeroGamma']['A'] == 53 and rec['B-zeroGamma']['Q'] == 36
assert rec['C-zeroA']['A'] == 50 and rec['C-zeroA']['Q'] == 36
json.dump(rec, open(PDIR + 'UFRL_REGRESSIONS.json', 'w'), indent=1)
print('REGRESSIONS: PASS', flush=True)
