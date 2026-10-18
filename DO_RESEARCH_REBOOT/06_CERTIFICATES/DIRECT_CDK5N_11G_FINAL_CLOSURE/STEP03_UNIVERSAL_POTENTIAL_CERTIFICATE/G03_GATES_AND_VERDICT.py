# G03_GATES_AND_VERDICT.py — honest Step-03 gate verdicts (no certificate claimed).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')
PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'

gates = [
    {'gate': 'G1 entry audit (HEAD/hashes/Z3/fixture)', 'verdict': 'PASS', 'detail': 'G03_ENTRY_AUDIT.json'},
    {'gate': 'G2 frozen-state feature library', 'verdict': 'PASS', 'detail': '16 features incl. subtree ranks; verified on grounded envs'},
    {'gate': 'G3 grounded seed corpus (ssertify-ok)', 'verdict': 'PASS', 'detail': '38 seeds + ~460 falsification edges'},
    {'gate': 'G4 CEGIS loop executed w/ targeted modes', 'verdict': 'PASS', 'detail': '11 rounds + root/deep targeting; G03_CEGIS_TRACE.json'},
    {'gate': 'G5 candidate survives fresh falsification', 'verdict': 'FAIL', 'detail': 'best refit-38: 15/60 violations (25%); coefficients diverged to 100s'},
    {'gate': 'G6 universal per-weight Z3 UNSAT (low+contracted-high)', 'verdict': 'FAIL', 'detail': 'not attempted: no surviving candidate; stub G03_UNIVERSAL_VERIFY.py retained'},
    {'gate': 'G7 potential certificate artifact', 'verdict': 'FAIL', 'detail': 'no certified Phi'},
    {'gate': 'G8 NonNegCycles(G_star) certified', 'verdict': 'FAIL', 'detail': 'conjecture stands (no grounded negative cycle found) but unproven'},
]
json.dump(gates, open(PDIR + 'G03_GATES.json', 'w'), indent=1)
verdict = {
    'step': '11G STEP03 UNIVERSAL POTENTIAL CERTIFICATE',
    'outcome': 'INCOMPLETE — universal potential NOT found; additive feature families exhausted by CEGIS falsification',
    'negative_results': [
        'affine-10base: round-4 refit UNSAT (bounds 8/16/64/unbounded) on 29-seed H<=2 set [recorded observation]',
        'poly-degree2: only 1e12-coefficient memorization fits; rejected',
        'rank-affine-15feat: clean candidates (rank_sum-depth_max [+a_marked]) stable on mix but systematically falsified by targeted modes; refits diverge; final 15/60 fresh violations',
    ],
    'deliverables': ['G03_ENTRY_AUDIT.json', 'G03_POTENTIAL_FEATURES.py (16 feats)', 'G03_CEGIS_SEEDS.json (38)',
                     'G03_CEGIS_TRACE.json', 'G03_FALSIFY_*.json', 'G03_STEP03_RECORD.json', 'G03_GATES.json',
                     'G03_CANDIDATE_POTENTIAL.json (last refit, UNCERTIFIED)', 'G03_GROUNDED_GRAPH_CHECK.py (9 edges, no grounded negative cycle)'],
    'next_directions': [
        'D1 piecewise/min-plus potential per (H-class x sector): case-split DAG, CEGIS per piece',
        'D2 exact log-rank + maxdepth with vertex-cover style case analysis (ST85 access-lemma shape)',
        'D3 direct combinatorial NonNegCycles argument from 11F ladder/climb structure (no potential)',
        'D4 A-side credit feature for shadow-mark jumps (killer: marked+2 @ w=0); H=0/H>=3 targeted sampling (rare in current sampler)',
    ],
    'program_impact': 'Stage 11G Step 03 open; 11F forward simulation (2A-Q_B per walk) unaffected; Bank-25 2A target still requires NonNegCycles(G_star) by another method',
}
json.dump(verdict, open(PDIR + 'G03_STEP03_VERDICT.json', 'w'), indent=1)
print('PASS:', sum(1 for g in gates if g['verdict'] == 'PASS'), 'FAIL:', sum(1 for g in gates if g['verdict'] == 'FAIL'))
