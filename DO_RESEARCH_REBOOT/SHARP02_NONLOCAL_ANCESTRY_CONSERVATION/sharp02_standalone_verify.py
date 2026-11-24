"""No historical files required: independently check the complete principal case."""
import sys
from sharp02_common import *
from sharp01_oracle import replay
from sharp01_validate import tuple_state,ref
from sharp02_independent import verify
from sharp02_graph import graph_data,solve

with Run(sys.argv[1] if len(sys.argv)>1 else 'standalone_replay_v001',limit=30) as run:
    cert=read(BASE/'SHARP02_PRINCIPAL_COUNTERCERTIFICATE.json');src=cert['source'];l=replay(src,features=False)
    independent=verify(l);data=graph_data(l);rr=solve(data['weights'],data['adj'],data['free'])
    oo=solve(data['weights'],data['all_adj'],data['units'],data['capacities'])
    assert rr['flow']==0 and rr['unmatched']==1 and rr['deficiency']==1
    assert oo['flow']==1 and len(data['all_adj']['16'])==6
    assert all(data['units'][j]['reserved_chronological'] for j in data['all_adj']['16'])
    assert l['summary']['A']==35 and l['summary']['Q']==24 and l['summary']['U']==1 and l['summary']['C']==47
    # Independently verify the optional right-vine reaching prefix; its work is
    # excluded from the period and from BOTH repaired counting maps.
    a=b=tuple_state(src['alternate_right_vine_diagonal'])
    for tag,x in src['alternate_reaching_prefix']:
        a,_=ref.trace(a,x)
        if tag=='K':b,_=ref.trace(b,x)
    assert a==tuple_state(src['initial_A']) and b==tuple_state(src['initial_B'])
    gainmap={tuple(e['id']):set(map(tuple,e['created_pairs'])) for e in independent['A_real_rotation_geometry']}
    allnamed={tuple(u['id']):u for u in data['units'].values()};allB={tuple(s['id']) for s in l['steps'] if s['id'][0]=='B' and s['case']!='ZIG'}
    for filename in ('SHARP02_REPAIRED_SOURCE_INJECTION.json','SHARP02_ORIGIN_LOSS_REPAIR.json'):
        result=read(BASE/filename);mapping=result['map'];seen=set()
        assert {tuple(z['B_double_id']) for z in mapping}==allB
        for z in mapping:
            uid=tuple(z['A_accounting_unit']);assert uid in allnamed and uid not in seen;seen.add(uid)
        assert len(mapping)==24
    for j in data['all_adj']['16']:
        u=data['units'][j];ps=gainmap[tuple(u['rotation_witness'])]
        assert any((y,9) in ps for y in (6,7,8,10))
    result={'status':'PASS','period_operations':17,'physical_keys':10,'complete_closed_common_diagonal':True,
        'A':35,'Q_B':24,'U':1,'C':47,'fixed_Hall_neighbors':0,'fixed_Hall_deficiency':1,
        'all_eligible_gain_units':6,'all_six_reserved':True,'optimized_repair_flow':1,
        'both_explicit_24_double_injections_checked':True,'optional_right_vine_prefix_independently_checked':True,
        'immutable_primitive_rotations_checked':independent['primitive_rotations_checked'],
        'conclusion':'Type II refutation of stipulated reservation plus all-recreation graph; no scalar Q>2A violation'}
    write(BASE/'SHARP02_STANDALONE_VERIFICATION.json',result)
    run.check(primitive_rotations_verified=117);print(json.dumps(result))
