from campaign3b import *
from independent_Pi3 import check as independent_Pi
from independent_cohorts import verify as independent_pairs
from accounting import audit
from new_payments import intern_original_states
from verify_scoped_classes import subtree


if __name__=='__main__':
    meter=Meter('counterexample_verification');pool=intern_original_states()
    sources=json.loads((ROOT/'DILATED_PACKET_SOURCES.json').read_text());s=sources[-1]
    r=Replay(s);star,_,_=original_residual(r);saved=json.loads((ROOT/'DILATED_PACKET_RESULTS.json').read_text())[-1]
    assert star==saved['original_R_star'] and digest(r.events)==s['trace_hash']
    assert r.S==set(range(1,578)) and s['initial_A']==s['initial_B']==s['diagonal_initial'] and not s['reaching_prefix']
    if '--reuse-independent-phase' in sys.argv:
        z=json.loads((ROOT/'COUNTEREXAMPLE_INDEPENDENT_PI.json').read_text())
        pairs=json.loads((ROOT/'COUNTEREXAMPLE_INDEPENDENT_R6.json').read_text())
        assert z['source']==s['name'] and z['complete_immutable_primitive_rotations']==r.T
        assert set(z['independently_reconstructed_all_original_U'])=={str(k) for k in r.U}
        for key,d in r.U.items():assert all(d[k]==v for k,v in z['independently_reconstructed_all_original_U'][str(key)].items())
        orig={digest(p['rho']):p for p in r.pairs}
        assert len(orig)==len(pairs['independently_recomputed_all_original_pairs'])
        for p in pairs['independently_recomputed_all_original_pairs']:
            assert json.loads(json.dumps({k:orig[digest(p['rho'])][k] for k in p}))==p
    else:
        z=independent_Pi(r);write('COUNTEREXAMPLE_INDEPENDENT_PI.json',z)
        pairs=independent_pairs(r);write('COUNTEREXAMPLE_INDEPENDENT_R6.json',pairs)
    a=audit(r,star);assert json.loads(json.dumps(a))==saved['ordered_accounting']
    E=a['first_use_E_C'];assert len(E['packets'])==1
    packet=E['packets'][0]
    assert packet['actual_A_demotion_bit']==('A',133,24,1) and packet['old_g']==154
    assert packet['selected_first_parent']==(646,3) and packet['remaining_original_parents']==[(653,4)]
    assert len(E['repeat_original_gaps'])==2
    anchor=tuple(packet['actual_A_demotion_bit']);at=r.event_by_id[anchor]['time'];last=r.doubles[(653,4)]['events'][-1]
    aa=Tree(s['initial_A']);component=None;checks=0
    for ev in r.events[:last]:
        if ev['actor']=='A':aa.rotate(ev['pivot'],ev['side'])
        if ev['time']==at:component=subtree(aa,154)
        if component is not None:assert subtree(aa,154)==component;checks+=1
    assert min(component)==137 and max(component)==576
    relevant=[]
    gaps=keep_gaps(r)
    for h,j in [(646,3),(653,4)]:
        d=r.U[h,j];path=r.boundaries[h-1]['B_path'];assert path[-1-2*j]==154 and j>2*gaps[h]['A']
        assert 154 not in r.boundaries[h-1]['A_path']
        relevant.append({'parent':[h,j],'old_g':154,'A_gap':gaps[h]['A'],
            'actual_pre_A_path':r.boundaries[h-1]['A_path'],'actual_pre_B_path':path,
            'original_U':d,'original_parent_gap_demands':[e for e in star if e['original_parent']==[h,j]],
            'actual_gap_A_StepEv':gaps[h]['A_StepEv']})
    assert a['literal_requested_R_upper']==[] and a['positive_old_periodic_certificate']['eligible_periodic']
    write('COUNTEREXAMPLE_CERTIFICATE.json',{'source':s['name'],'population':len(r.keys),'operations':len(r.ops),
        'A':r.A,'Q_B':r.Q,'original_S':sorted(r.S),'original_R_star':star,
        'ordered_original_assignments':a['ordered_original_assignments'],
        'refuted_statement':'Every original C parent after frozen carrier/skipped and original B-prefix deductions is the first C use of its old grandparent in its A-demotion epoch.',
        'epoch_packet':packet,'original_parent_certificates':relevant,
        'rigid_complete_A_component':{'root':154,'children':component,'key_min':137,'key_max':576,'primitive_checks':checks},
        'independent_primitive_SET_Pi_U':'COUNTEREXAMPLE_INDEPENDENT_PI.json',
        'independent_full_cohort_R6_reconstruction':'COUNTEREXAMPLE_INDEPENDENT_R6.json',
        'independent_phase_reused_after_controller_fix':'--reuse-independent-phase' in sys.argv,
        'original_EXP02_EXP03_EXP04_selectors':'Unchanged pinned implementations, freshly replayed; not independently rewritten.',
        'old_periodic_certificate':{k:v for k,v in a['positive_old_periodic_certificate'].items() if k!='retained_original_operations'},
        'original_R_upper_escape':False,'universal_R_upper_O_A_refuted':False,
        'complete_original_source_artifact':'DILATED_PACKET_SOURCES.json','complete_original_trace':saved['trace_file']})
    print('PASS new prehybrid first-use counterexample; full independent Pi/U/R6;',r.T,'bits;',
          len(r.U),'U;',len(pairs['independently_recomputed_all_original_pairs']),'pairs; R_upper still old-periodic paid',flush=True)
    meter.success=True
