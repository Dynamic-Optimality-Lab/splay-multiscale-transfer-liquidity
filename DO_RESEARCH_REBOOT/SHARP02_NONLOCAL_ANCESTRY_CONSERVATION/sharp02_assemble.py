"""Assemble exact deliverable datasets and verify selected search witnesses."""
from fractions import Fraction
from sharp02_common import *
from sharp02_graph import graph_data,solve
from sharp02_fast import evaluate,recurrent
from sharp02_search import zero_run,summary
from sharp01_oracle import replay
from sharp01_validate import validate

import sys
with Run(sys.argv[1] if len(sys.argv)>1 else 'assemble_datasets_v001',limit=90) as run:
    oldsources=read(OLD/'SHARP01_SOURCE_WITNESSES.json')['sources'];idx=read(OLD/'SHARP01_GAP_LEDGER.json')['ledgers']
    reconstruction=read(BASE/'SHARP02_RECONSTRUCTION.json');search=read(BASE/'SHARP02_SEARCH_RESULTS_v002.json')
    first=read(BASE/'SHARP02_SEARCH_RESULTS.json');assert first['counts']==search['counts']
    assert (BASE/'SHARP02_PRINCIPAL_COUNTEREXAMPLE_RAW.json').read_bytes()==(BASE/'SHARP02_PRINCIPAL_COUNTEREXAMPLE_RAW_v002.json').read_bytes()
    log=[json.loads(z) for z in (BASE/'SHARP02_SEARCH_LOG_v002.jsonl').read_text().splitlines()]
    assert len(log)==423 and sum(not z['vacuous'] for z in log)==214
    graphs=[]
    for it in idx:
        l=read(OLD/it['path']);d=graph_data(l)
        graphs.append({'source':it['name'],'demand_weights':d['weights'],'edges':{i:sorted(js) for i,js in d['adj'].items()},
            'named_incident_units':{j:d['free'][j] for j in set().union(*d['adj'].values())} if d['adj'] else {},
            'source_input_ledger':str((OLD/it['path']).relative_to(REPO)).replace('\\','/'),'ledger_sha256':it['sha256']})
    controls=read(BASE/'SHARP02_CONTROL_CERTIFICATES.json');principal=read(BASE/'SHARP02_PRINCIPAL_COUNTERCERTIFICATE.json')
    sources={s['name']:s for s in oldsources}
    sources.update({s['name']:s for s in read(BASE/'SHARP02_EXTRA_CONTROL_SOURCES.json')})
    sources[principal['source']['name']]=principal['source']
    sources[first['counterexample']['source']['name']]=first['counterexample']['source']
    verified=[]
    for z in search['elite']:
        s=z['source'];sources[s['name']]=s
        l=replay(s,features=False);validate(s,l);d=evaluate(s)
        assert all(d[k]==z['summary'][k] for k in ('A','Q','U','C','Delta','n','operations'))
        verified.append({'source':s['name'],'operations':len(s['operations']),'status':'PASS full pointer and immutable-frame replay'})
    # Recover the already-measured maximum-Q/A CONTROL from its exact scheduled
    # construction. This is not another search or a new candidate family.
    maxrow=max((z for z in log if z['A']),key=lambda z:Fraction(z['Q'],z['A']))
    assert maxrow['search_candidate']==43 and maxrow['method']=='remove_suffix_94'
    seed=zero_run(24);w=seed['operations'][:-94];s=recurrent(seed,w,maxrow['name'])
    key=hashlib.sha256(repr((s['initial_A'],s['initial_B'],s['operations'])).encode()).hexdigest()
    assert key==maxrow['word_sha256']
    l=replay(s,features=False);validate(s,l);d=evaluate(s);rr=solve(d['weights'],d['adj'],d['free'])
    assert Fraction(d['Q'],d['A'])==Fraction(14,13)
    sources[s['name']]=s;max_certificate={'source':s,'summary':summary(d,rr),'source_word_sha256':key,
        'verification':'full pointer and immutable-frame replay, identical to candidate 43 in recorded search'}
    write(BASE/'SHARP02_MAX_RATIO_CONTROL.json',max_certificate)
    # Explicit original-double to actual-accounting-unit injection after the ONE
    # legal per-gap reservation swap. The map is only for this named source.
    l=read(BASE/'SHARP02_MINIMAL_SOURCE_LEDGER.json');data=graph_data(l)
    swaps=principal['reservation_swaps'];unit_by_id={tuple(u['id']):j for j,u in data['units'].items()}
    reserved={j for j,u in data['units'].items() if u['reserved_chronological']}
    for swap in swaps:
        reserved.remove(unit_by_id[tuple(swap['release_from_baseline'])]);reserved.add(unit_by_id[tuple(swap['reserve_instead'])])
    injection=[]
    for g in l['gaps']:
        own=[j for j,u in data['units'].items() if u['gap_index']==g['gap_index'] and j in reserved]
        budget=min(g['q'],2*g['p']);assert len(own)==budget
        injection.extend({'B_double_id':sid,'A_accounting_unit':data['units'][j]['id'],'role':'own-gap baseline'} for sid,j in zip(g['B_double_ids'][:budget],own))
        if g['u']:
            donors=[j for i,j,n in principal['optimized_reservation']['assignment'] if i==str(g['gap_index'])]
            assert len(donors)==g['u']
            injection.extend({'B_double_id':sid,'A_accounting_unit':data['units'][j]['id'],'role':'actual nonlocal A-ancestry recreation'} for sid,j in zip(g['B_double_ids'][budget:],donors))
    assert len(injection)==24 and len({tuple(x['A_accounting_unit']) for x in injection})==24
    assert len({tuple(x['B_double_id']) for x in injection})==24
    write(BASE/'SHARP02_REPAIRED_SOURCE_INJECTION.json',{'source':principal['source']['name'],'map':injection,'baseline_units_reserved':len(reserved),
        'contract':'no inherited locked owners supplied; the exploratory baseline owner for B(2,2) changes within its own gap'})
    # A different, explicitly scoped physical repair keeps the original baseline
    # assignments and widens eligibility to the actual origin loss of the pair.
    lossid=('A',13,1,1);lossunit=unit_by_id[lossid]
    assert lossunit in data['free']
    loss_event=next(e for e in l['events'] if tuple(e['id'])==lossid)
    assert loss_event['ancestry_removed'][0]==8 and 9 in loss_event['ancestry_removed'][1]
    assert 8 in l['operations'][12]['B_path'][:-1] and l['operations'][12]['tag']=='D'
    oldbaseline=[]
    for gg in l['gaps']:
        own=[j for j,u in data['units'].items() if u['gap_index']==gg['gap_index'] and u['reserved_chronological']]
        oldbaseline.extend({'B_double_id':sid,'A_accounting_unit':data['units'][j]['id'],'role':'unchanged chronological own-gap baseline'} for sid,j in zip(gg['B_double_ids'],own))
    origin_map=oldbaseline+[{'B_double_id':['B',17,3],'A_accounting_unit':list(lossid),'role':'actual A-only origin loss of B-only relation 8->9'}]
    assert len(origin_map)==24 and len({tuple(z['A_accounting_unit']) for z in origin_map})==24
    origin_repair={'source':principal['source']['name'],'status':'FINITE-EXACT repair only; enlarged eligibility is not SHARP-HALL',
        'new_eligible_unit':data['free'][lossunit],'actual_pair_lost':[8,9],'B_relation_still_true_at_loss':True,
        'all_23_baseline_owners_preserved':True,'map':origin_map,
        'scope_limit':'This real unit destroys a relevant A relation and therefore is NOT eligible under the refuted all-recreation rule. No universal loss/gain law is asserted.'}
    write(BASE/'SHARP02_ORIGIN_LOSS_REPAIR.json',origin_repair)
    # The arithmetic extra double need not have a B-only path pivot.
    g=principal['deficient_gaps'][0];events={tuple(e['id']):e for e in l['events']};double_rows=[]
    for j,sid in enumerate(g['B_double_ids'],1):
        e0=events[tuple(sid+[0])];e1=events[tuple(sid+[1])]
        pair=[e0['pivot'],e0['promoted']] if e0['case'] in ('LL','RR') else [e1['pivot'],e0['pivot']]
        double_rows.append({'original_B_double':sid,'case':e0['case'],'old_grandparent_parent':pair,
                            'B_only_pivots':[v for v in pair if v in g['B_only_ancestors']],'after_2p_baseline':j>2*g['p']})
    assert double_rows[-1]['old_grandparent_parent']==[2,5] and not double_rows[-1]['B_only_pivots']
    write(BASE/'SHARP02_DEMAND_TOKENIZATION.json',{'universal_identity':'|Y|=2p+2u+epsilon_A+epsilon_B+|AncA(x) minus AncB(x)| for u>0',
         'epsilon_A':'2p-dA in {0,1}','epsilon_B':'dB-2q in {0,1}',
         'principal_source':principal['source']['name'],'gap':g,'actual_double_positions':double_rows,
         'token_model_counts':{mode:sum(s['token_models'][mode]['unmatched']>0 for s in reconstruction['sources']) for mode in ('outermost','innermost','extra_double')}})
    results={'scope':'SHARP-02 only; all costs exact integers, ratios reduced rationals','inherited_reconstruction':reconstruction,
        'inherited_actual_graphs':graphs,'search':{'counts':search['counts'],'seed':search['seed'],'all_complete_source_results':'SHARP02_SEARCH_LOG_v002.jsonl',
        'first_obstruction_candidate':452,'search_stopped_on_first_principal_failure':True,'two_runs_byte_exact_same_obstruction':True,
        'maximum_recorded_Q_over_A':max_certificate['summary']['Q_over_A']},
        'principal_counterexample':principal,'parametric_control_results':controls,'selected_search_witness_verification':verified,
        'finite_origin_loss_repair':origin_repair,
        'scalar_sharp_counterexample_found':False,'general_optimized_reservation_Hall_status':'OPEN; not investigated as a new campaign after fixed-model refutation'}
    write(BASE/'SHARP02_HALL_RESULTS.json',results)
    def source_hash(s):
        body={k:s[k] for k in ('initial_A','initial_B','operations')}
        body['diagonal_initial']=s.get('diagonal_initial',s['initial_A']);body['reaching_prefix']=s.get('reaching_prefix',[])
        return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    write(BASE/'SHARP02_SOURCE_WITNESSES.json',{'sources':list(sources.values()),'physical_execution_sha256':{name:source_hash(s) for name,s in sources.items()},
          'all_search_source_reconstruction':'Use deterministic seed 20261111 and the exact bounded driver; every complete candidate has a word hash and graph/cost row in the v002 log',
          'important_witnesses':{'principal':principal['source']['name'],'raw':first['counterexample']['source']['name'],'maximum_Q_over_A':max_certificate['source']['name']}})
    write(BASE/'SHARP02_COUNTEREXAMPLE_CERTIFICATES.json',{'principal_Type_II':principal,
        'parametric_family':{'definition':'append an arbitrary untouched >10 BST at key 10 right; repeat the 17-operation word r times',
            'r_domain':'all integers r>=1','hanger_domain':'any finite ordered >10 full physical BST, including empty',
            'costs':'A=35r,Q=24r,U=r,C=47r,Delta=-46r','fixed_Hall_deficiency':'r isolated weight-one demand nodes, zero eligible remaining neighbors',
            'repair':'one specified within-gap baseline exchange in every copy; all original IDs get copy offsets'},
        'tokenization':read(BASE/'SHARP02_DEMAND_TOKENIZATION.json'),
        'finite_origin_loss_repair':origin_repair,
        'inherited_first_restoration_reproductions':[z for z in controls['C15'] if 'first' in z],
        'claim_not_made':'No Type III counterexample; fixed-rule refutation does not refute all possible reservations or Universal Coarse-Double'})
    run.check(exported_sources=len(sources),selected_search_witnesses_independently_verified=len(verified))
    print(json.dumps({'exported_sources':len(sources),'elite_verified':len(verified),'maximum_ratio_control':max_certificate['summary'],
                      'repaired_injection_size':len(injection)}))
