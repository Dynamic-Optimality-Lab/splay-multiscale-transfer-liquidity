from epoch_payment import *
from verify_checkpoint import independent_Pi
from new_payments import compact_trace
from exp01_diagnostics import incidence


if __name__=='__main__':
    meter=Meter('epoch_obstruction_check')
    base=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    archive=json.loads((base/'EXP01_SOURCE_WITNESSES.json').read_text())['sources']
    s=next(s for s in archive if s['name']=='DW_5_1_at31');r=Replay(s)
    assert digest(r.events)==s['trace_hash']
    star,_,_=original_residual(r)
    ds=[{'rho':p['rho'],'consumer':p['rho'][0],'original_parent':p['parent'],'type':'R6'} for p in r.pairs if p['class']=='R6']
    z=from_replay(r,ds);packet=next(p for p in z['packets'] if p['original_parent_count']>1)
    assert packet['actual_A_demotion_bit']==('A',162,8,0)
    assert packet['selected_first_parent']==(171,2) and packet['remaining_original_parents']==[(179,2)]
    cert=independent_Pi(r);write('OBSTRUCTION_INDEPENDENT_PI.json',cert)
    compact_trace(r,star,'OBSTRUCTION_FULL_TRACE.json')
    parents=[packet['selected_first_parent']]+packet['remaining_original_parents'];records=[]
    for parent in parents:
        d=r.U[parent];g=d['g'];h,j=parent;x=r.ops[h-1][1]
        records.append({'original_parent':parent,'old_g':g,'target':x,'original_U':d,
            'all_original_R6_at_parent':[p for p in r.pairs if p['class']=='R6' and tuple(p['parent'])==parent],
            'A_path':r.boundaries[h-1]['A_path'],'B_path':r.boundaries[h-1]['B_path'],
            'original_ancestry_lifecycle':ancestry_history(r,g,x)})
    root=incidence(r,{'R6'})
    write('EPOCH_OBSTRUCTION_CERTIFICATE.json',{'source':s['name'],'complete_original_source':s,
        'A':r.A,'Q_B':r.Q,'population':len(r.keys),'operations':len(r.ops),
        'refuted_statement':'Every original R6 parent is the first R6 use of its old grandparent in its cyclic A-demotion epoch.',
        'original_packet':packet,'original_parent_certificates':records,
        'original_R_star':star,'R_upper_escape_claimed':False,
        'independently_verified_primitive_rotations':cert['immutable_tuple_primitive_rotations'],
        'independently_verified_original_U':cert['independently_verified_original_U'],
        'root_entry_unit_capacity_deficiency':root['deficiency'],'root_entry_Hall_witness':root['hall_witness'],
        'independent_full_Pi_artifact':'OBSTRUCTION_INDEPENDENT_PI.json',
        'full_trace_artifact':'OBSTRUCTION_FULL_TRACE.json',
        'qualification':'This is a new refuted statement on a preserved historical complete source. Its original R_star is empty; it is not an upper residual escape.'})
    print('PASS new epoch-exhaustiveness obstruction on original DW5; second Pi/U checked',cert['immutable_tuple_primitive_rotations'],'bits',flush=True)
    meter.success=True
