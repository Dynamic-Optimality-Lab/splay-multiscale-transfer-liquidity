"""Full source/cut/reservation certificates for the minimized principal failure."""
from collections import defaultdict
from sharp02_common import *
from sharp01_oracle import replay
from sharp02_graph import graph_data,solve
from sharp02_independent import verify

import sys
with Run(sys.argv[1] if len(sys.argv)>1 else 'minimal_countercertificate_v001',limit=60) as run:
    minimized=read(BASE/'SHARP02_MINIMIZED_COUNTEREXAMPLE.json');src=minimized['source']
    if src['initial_A']==src['initial_B']:
        # Any complete BST is an admissible common diagonal. The construction
        # prefix is an optional additional reachability proof, never capacity.
        src['alternate_right_vine_diagonal']=src['diagonal_initial'];src['alternate_reaching_prefix']=src['reaching_prefix']
        src['diagonal_initial']=src['initial_A'];src['reaching_prefix']=[]
        src['alternate_construction_orbit_preperiod']=src.get('orbit_preperiod')
        src['orbit_preperiod']=0;src['orbit_period']=1
        src['reachability']='common diagonal, empty paid/excluded prefix; alternate right-vine construction retained separately'
    l=replay(src,features=False);v=verify(l);d=graph_data(l)
    broad=solve(d['weights'],d['adj'],d['free']);opt=solve(d['weights'],d['all_adj'],d['units'],d['capacities'])
    assert broad['unmatched']==1 and opt['unmatched']==0 and l['summary']['Delta']<0
    independent_units={tuple(e['id']):e for e in v['A_real_rotation_geometry']}
    for j,unit in d['units'].items():
        created=set(map(tuple,independent_units[tuple(unit['rotation_witness'])]['created_pairs']))
        assert created=={(unit['created_ancestor'],x) for x in unit['created_targets']}
    eligible={i:[j for j,unit in d['units'].items() if any((y,next(g['target'] for g in l['gaps'] if str(g['gap_index'])==i)) in set(map(tuple,independent_units[tuple(unit['rotation_witness'])]['created_pairs'])) for y in next(g['B_only_ancestors'] for g in l['gaps'] if str(g['gap_index'])==i))] for i in d['weights']}
    assert all(set(eligible[i])==d['all_adj'][i] for i in eligible)
    assert not any(j in d['free'] for js in eligible.values() for j in js)
    chosen=[j for i,j,n in opt['assignment']];swaps=[];occupied=set(chosen)
    for j in chosen:
        unit=d['units'][j]
        if unit['reserved_chronological']:
            replacement=next(k for k,other in d['free'].items() if other['gap_index']==unit['gap_index'] and k not in occupied)
            occupied.add(replacement)
            swaps.append({'gap_index':unit['gap_index'],'release_from_baseline':unit['id'],'reserve_instead':d['units'][replacement]['id'],
                          'excess_assignment':next(i for i,k,n in opt['assignment'] if k==j)})
    cert={'classification':'Type II — exact fixed-chronological-reservation SHARP-HALL refutation',
          'source':src,'summary':l['summary'],'broad':broad,'optimized_reservation':opt,'reservation_swaps':swaps,
          'deficient_gaps':[g for g in l['gaps'] if str(g['gap_index']) in broad['deficient_subset']],
          'all_eligible_units':{i:[d['units'][j] for j in js] for i,js in eligible.items()},
          'all_named_units':d['units'],'old_owners':'none imported or changed; baseline is exploratory and has only per-gap cardinality constraints',
          'minimality':'one-demand minimum Hall subset; source is greedily locally minimized, not proved globally shortest',
          'verification':{'full_pointer_and_immutable_replay':True,'immutable_primitive_checks':v['primitive_rotations_checked'],'complete_geometry_file':'SHARP02_MINIMAL_INDEPENDENT_GEOMETRY.json'}}
    write(BASE/'SHARP02_MINIMAL_SOURCE_LEDGER.json',l);write(BASE/'SHARP02_MINIMAL_INDEPENDENT_GEOMETRY.json',v)
    write(BASE/'SHARP02_PRINCIPAL_COUNTERCERTIFICATE.json',cert)
    print(json.dumps({'word':src['operations'],'summary':l['summary'],'gap':cert['deficient_gaps'],
                      'eligible':cert['all_eligible_units'],'swaps':swaps,'primitive_checks':v['primitive_rotations_checked']}))
