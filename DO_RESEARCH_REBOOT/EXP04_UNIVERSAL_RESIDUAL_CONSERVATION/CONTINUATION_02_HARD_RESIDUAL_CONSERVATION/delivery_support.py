from campaign import *


def source_archive():
    sources=[]; provenance={}; costs={}; scopes={}
    batches=['HELPER_SOURCES.json','DILATED_SOURCES.json','UPPER_SOURCES.json',
             'PRIVATE_ANCESTOR_SOURCES.json','ADAPTIVE_SOURCES.json','ADAPTIVE_LIFT_SOURCE.json']
    for batch in batches:
        zs=json.loads((ROOT/batch).read_text());zs=zs if isinstance(zs,list) else [zs]
        for s in zs:
            sources.append(s);provenance[s['name']]=batch
    control=json.loads((ROOT/'ROOT_COUPLING_COUNTEREXAMPLE.json').read_text())
    s=control['source'];sources.append(s);provenance[s['name']]='ROOT_COUPLING_COUNTEREXAMPLE.json'
    costs[s['name']]={k:control[k] for k in ('A','Q_B')}
    for batch in ['HELPER_RESULTS.json','DILATED_RESULTS.json','CURRENT_A_PAYMENT_RESULTS.json',
                  'PRIVATE_ANCESTOR_RESULTS.json','ADAPTIVE_RESULTS.json','ADAPTIVE_LIFT_RESULTS.json']:
        zs=json.loads((ROOT/batch).read_text());zs=zs if isinstance(zs,list) else [zs]
        for z in zs:
            name=z.get('source',z.get('name'));costs[name]={k:z[k] for k in ('A','Q_B')}
    full={
        'C02_helper5_before_K2':('HELPER_RESULTS.json','original_R_star'),
        'C02_dilate_65_stride9_copies3':('DILATED_RESULTS.json','original_R_star'),
        'C02_upper_bothosc_p8_l64_r64_bitreverse_ret1_low2':('CURRENT_A_PAYMENT_RESULTS.json','original_events'),
        'C02_private_h_stride3':('PRIVATE_ANCESTOR_RESULTS.json','original_R_star')}
    for s in sources:
        name=s['name'];s.update(costs[name]);s['delivery_source_batch']=provenance[name]
        if name in full:
            batch,key=full[name];zs=json.loads((ROOT/batch).read_text())
            z=next(z for z in zs if z['source']==name)
            # The helper result uses R_star rather than original_R_star.
            ev=z.get(key,z.get('R_star'))
            assert isinstance(ev,list),(name,list(z))
            scopes[name]={'original_R_star':ev,'full_original_Pi_U_cohorts_R6_classification':True,
                          'classification_artifact':batch,
                          'independent_second_full_SET_Pi_U_reconstruction':name=='C02_private_h_stride3'}
        elif name==control['source']['name']:
            # Every original parent is nonneutral in this tiny control; it has no R6 consumer.
            scopes[name]={'original_R_star':None,'full_original_Pi_U_cohorts_R6_classification':False,
                          'original_residual_zero_reason':'No fully neutral internal B double; verified by final physical replay.',
                          'classification_artifact':'ROOT_COUPLING_COUNTEREXAMPLE.json'}
        else:
            scopes[name]={'original_R_star':None,'full_original_Pi_U_cohorts_R6_classification':False,
                          'classification_artifact':None,'qualification':'Physical screening only; unrun Pi is not measured zero.'}
    assert len(sources)==18 and len({s['name'] for s in sources})==18
    return sources,scopes,provenance
