"""Independent triage of the first all-recreation Hall obstruction."""
from sharp02_common import *
from sharp01_oracle import replay
from sharp01_validate import validate
from sharp02_graph import graph_data,solve

with Run('confirm_raw_witness_v001',limit=60) as run:
    raw=read(BASE/'SHARP02_PRINCIPAL_COUNTEREXAMPLE_RAW.json');src=raw['source']
    led=replay(src,features=False);validate(src,led);data=graph_data(led)
    broad=solve(data['weights'],data['adj'],data['free'])
    optimized=solve(data['weights'],data['all_adj'],data['units'],data['capacities'])
    assert broad['unmatched']>0 and led['summary']['Delta']<0
    assert not optimized['unmatched']
    write(BASE/'SHARP02_RAW_WITNESS_LEDGER.json',led)
    write(BASE/'SHARP02_RAW_WITNESS_CONFIRMATION.json',{'source':src,'summary':led['summary'],'broad':broad,
        'optimized':optimized,'deficient_gaps':[g for g in led['gaps'] if str(g['gap_index']) in broad['deficient_subset']],
        'all_units':data['units'],'all_eligibility':{i:sorted(js) for i,js in data['all_adj'].items()},
        'classification':'Type II: chronological reservation refutes fixed SHARP-HALL; a different exact per-gap reservation repairs it',
        'independent_check':'frozen complete pointer oracle and separate immutable-frame replay agree on every operation'})
    run.check(operations_verified=len(src['operations']),broad_unmatched=broad['unmatched'])
    print(json.dumps({'CONFIRMED':'Type II','A':led['summary']['A'],'Q':led['summary']['Q'],'broad':broad,
        'eligible_reserved_units':{i:[data['units'][j] for j in js] for i,js in data['all_adj'].items()}}))
