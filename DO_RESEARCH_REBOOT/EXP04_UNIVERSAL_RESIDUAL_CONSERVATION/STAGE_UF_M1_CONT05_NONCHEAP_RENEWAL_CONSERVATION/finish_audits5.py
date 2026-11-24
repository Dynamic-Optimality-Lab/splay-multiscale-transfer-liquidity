from base5 import *
from catalog5 import entries
from physical_renewal5 import audit as physical_audit
from cohortc import decode_state
from physical1 import Edges
from bisect import bisect_right
from coercion import shapes,from_tuple
from exp01_oracle import Tree

def filtered_geometry(s,p,f,rec):
    ds={tuple(z['parent']):z for z in p['doubles']};vs={tuple(z['parent']):z for z in f['vertices']};T=len(p['events'])
    out=[];used=set()
    for e in rec['canonical_renewals']:
        u=tuple(e['earlier_parent']);v=tuple(e['later_parent']);g=e['old_g'];ulap=e['earlier_lap_offset']
        ru,rv=p['boundaries'][u[0]-1],p['boundaries'][v[0]-1]
        lo=ru['end_time']+ulap*T;hi=rv['post_A_time']
        interval=[]
        for z in p['events']:
            for shift in (-T,0):
                if lo<z['time']+shift<=hi:interval.append((z['time']+shift,z))
        interval.sort(key=lambda z:z[0])
        assert not any(z['actor']=='A' and z['pivot']==g for t,z in interval)
        promos=[(t,z) for t,z in interval if z['actor']=='B' and z['promoted']==g]
        a_u=Edges(decode_state(p,ru['post_A_state']));a_v=Edges(decode_state(p,rv['post_A_state']))
        assert a_u.component(g)==a_v.component(g)
        bu=Edges(decode_state(p,ru['post_B_state']));bv=Edges(decode_state(p,rv['pre_B_state']))
        Ju=bu.m[g];Fv=bv.m[g]
        beta=None
        if promos:
            t,beta=promos[-1];assert beta['case'] in ('LL','RR') and beta['id'][3]==0 and beta['target']!=g
            rid=tuple(beta['id'][1:3]);rd=ds[rid];assert rd['p']==g
            br=Edges(decode_state(p,rd['post_step_state']));P=br.m[g];assert Fv&~P==0
            donor=tuple(beta['id']);assert donor not in used;used.add(donor)
        else:assert Fv&~Ju==0
        out.append({**e,'transition':'promotion_mediated' if promos else 'promotion_free',
            'earlier_complete_A_component':a_u.component(g),'earlier_completed_physical_J':Ju,'later_complete_physical_frame':Fv,
            'actual_interval_A_StepEv':sorted({tuple(z['id'][:3]) for t,z in interval if z['actor']=='A'}),
            'actual_interval_B_promotions_of_g':[z['id'] for t,z in promos],'last_mediator_bit':beta,
            'original_interval_primitive_ids':[z['id'] for t,z in interval],
            'full_state_references':{'earlier_A':ru['post_A_state'],'earlier_B':ru['post_B_state'],'later_A':rv['post_A_state'],'later_B':rv['pre_B_state']}})
    return {'source':s['name'],'source_sha256':digest(s),'canonical_original_C_old_renewals':out,
        'mediator_injection_verified':True,'no_full_source_residual_inferred':True}

if __name__=='__main__':
    m=Meter('final_filtered_geometry_and_adversarial_audits');physical=load(ROOT/'PHYSICAL_RENEWAL_RESULTS.json');assert len(physical)==102
    refs=entries()
    for i,s in enumerate(load(ROOT/'FRINGE_SOURCE_CATALOG.json')):
        e={'source':s,'physical':str(ROOT/f'FRINGE_PHYS_{i:02}.json'),'origin':'C5_FRINGE'}
        physical.append(physical_audit(e));refs.append(e);gc.collect()
    write('PHYSICAL_RENEWAL_RESULTS_FINAL.json',physical);write('ALL_CONTROL_REFERENCES_FINAL.json',[{**e,'source_sha256':digest(e['source']),
        'physical_sha256':hfile(e['physical']) if e.get('physical') else None} for e in refs]);assert len(physical)==104
    # Old exact native chain provides a genuine original C_old repeat, not an
    # index-only use. Every new original accounting receives the same check.
    out=[]
    for stem in ('NEW','RENEW','FRINGE'):
        for i,s in enumerate(load(ROOT/f'{stem}_SOURCE_CATALOG.json')):
            out.append(filtered_geometry(s,load(ROOT/f'{stem}_PHYS_{i:02}.json'),load(ROOT/f'{stem}_FOREST_{i:02}.json'),load(ROOT/f'{stem}_RENEWAL_{i:02}.json')))
    old=load(ROOT/'RN1_REDUCTION_AUDIT.json')
    for i in range(3):
        s=load(C2/'RUN_B_SOURCE_CATALOG.json')[i];rec=next(e for e in old if e['source']==s['name'])
        out.append(filtered_geometry(s,load(C2/f'RUN_B_PHYS_{i:02}.json'),load(C2/f'RUN_B_FOREST_{i:02}.json'),rec))
    write('FILTERED_RENEWAL_GEOMETRY.json',out)
    # Exact converse obstruction: previous physical noncheap use is not C_old.
    s=load(ROOT/'NEW_SOURCE_CATALOG.json')[1];p=load(ROOT/'NEW_PHYS_01.json');b=load(ROOT/'NEW_BIRTH_01.json');acc=load(ROOT/'NEW_ORDERED_01.json')
    ds={tuple(z['parent']):z for z in p['doubles']};h=s['critical_operation'];v=next(tuple(z['original_parent']) for z in acc['E_old'] if z['consumer']==h and z['original_parent'][1]>2)
    u=tuple(b['U'][str(v)]['creator']);assert u[0]==s['creator_operation'] and u[1]>2 and v[1]>2
    assert not any(z['consumer']==u[0] for z in acc['native_original_R_star'])
    assert b['original_cohorts'].get(str(u[0]),[])==[]
    witness={'source':s,'source_sha256':digest(s),'earlier_physical_noncheap_parent':ds[u],'later_parent':ds[v],
        'creator_A_gap':1,'later_A_gap':1,'earlier_receiving_cohort':[],
        'earlier_original_R_star':[],'later_E_old_gaps':[z for z in acc['E_old'] if z['original_parent']==list(v)],
        'later_U_data':b['U'][str(v)],'earlier_U_data':b['U'].get(str(u)),
        'refuted_claim':'An earlier physical index-noncheap use of the same column necessarily exhausts original E_old before the later use.',
        'actual_S_UU':[],'scope':'Exact renewal-reduction converse refutation, not a posthybrid survivor.'}
    write('EXACT_NONCHEAP_VERSUS_C_OLD_OBSTRUCTION.json',witness)
    # Ownership-only potential cannot debit repeated original F/E-negative
    # demands at their B renewal event; H/actual quota still pay the source.
    s=load(ROOT/'RENEW_SOURCE_CATALOG.json')[1];p=load(ROOT/'RENEW_PHYS_01.json');rn=load(ROOT/'RENEW_RENEWAL_01.json');acc=load(ROOT/'RENEW_ORDERED_01.json')
    edge=next(e for e in rn['canonical_renewals'] if e['later_sigma']);v=tuple(edge['later_parent']);own={};aa,bt=Edges(s['initial_A']),Edges(s['initial_B'])
    from residual0 import gap_costs
    gs=gap_costs(s,p['boundaries']);ds={tuple(z['parent']):z for z in p['doubles']};saved=None
    for lap in range(2):
        for e in p['events']:
            before=dict(own)
            if e['actor']=='A':own[e['pivot']]=False
            elif e['case']!='ZIG' and e['id'][3]==0 and e['id'][2]>2*gs[e['id'][1]]:
                g=ds[tuple(e['id'][1:3])]['g'];own[g]=True
            if lap and e['id']==['B',v[0],v[1],0]:
                assert before==own and own[ds[v]['g']]
                saved={'original_event':e,'ownership_before':before,'ownership_after':dict(own),
                    'A_before':format(aa.code(),'x'),'B_before':format(bt.code(),'x')}
            (aa if e['actor']=='A' else bt).step(e)
            if saved and lap and e['id']==['B',v[0],v[1],0]:saved.update(A_after=format(aa.code(),'x'),B_after=format(bt.code(),'x'))
    assert saved
    write('EXACT_OWNERSHIP_DEBIT_OBSTRUCTION.json',{'source_sha256':digest(s),'source_catalog':'RENEW_SOURCE_CATALOG.json','catalog_index':1,
        'original_C_old_renewal':edge,'state':saved,'candidate_r_at_event':1,'delta_any_function_of_ownership_vector':0,'A_at_B_event':0,
        'refuted_claim':'Every repeated F/E_old-negative sigma renewal supplies a positive local decrease of a potential depending only on the binary epoch-ownership vector.',
        'actual_posthybrid_r_at_event':0,'remaining_payment':'Positive raw H_all, and counterfactual no-H distinct-parent quota also selects it.',
        'scope':'Refutes this debit law before H/quota, not the all-source actual S_UU bound or every possible potential.'})
    # All primitive types checked with arbitrary marked subsets on exact local
    # full trees. These are microstate checks, not fresh paired-source claims.
    cases=Counter();rotations=0
    for shape in shapes(1,4):
        for target in range(1,5):
            t=Tree(from_tuple(shape));bits={j:1<<(j-1) for j in range(1,5)}
            while t.par[target] is not None:
                pp=t.par[target];g=t.par[pp];side=int(target>pp)
                if g is None:rs=[(pp,side)];case='ZIG'
                else:
                    z=int(pp>g);case=('R' if z else 'L')+('R' if side else 'L');F=t.labels(bits)[g]
                    rs=[(g,z),(pp,side)] if side==z else [(pp,side),(g,z)]
                for u,ss in rs:
                    before=t.labels(bits);v0=t.ch[u][ss];t.rotate(u,ss);after=t.labels(bits)
                    assert after[u]&~before[u]==0 and before[v0]&~after[v0]==0
                    assert all(before[q]==after[q] for q in bits if q not in (u,v0));rotations+=1
                if case!='ZIG':
                    J=t.labels(bits)[g];P=t.labels(bits)[pp];assert not J&bits[target] and not P&bits[target]
                    for S in range(1,16):
                        if S&bits[target]:assert (J&S)!=(F&S) and (P&S)!=(F&S)
                cases[case]+=1
    assert all(cases[c]>0 for c in ('LL','RR','LR','RL','ZIG'))
    write('LOCAL_PRIMITIVE_TABLE_AUDIT.json',{'four_key_shapes':14,'target_traces':56,'real_rotations':rotations,'cases':dict(cases),
        'scope':'Complete local physical table and marked-subset strictness; universal proof uses intact-component algebra, not finite enumeration.'})
    # Exact invariant requested for the two long/short identity families.
    index={z['source']:z for z in physical};pairs=[]
    for marker,long_marker in (('M1C2_guarded_padded_with_extreme_identity_T1','M1C2_guarded_padded_with_extreme_identity_T141843'),
        ('M1C4_protected_half_s256_extreme_identity_T1','M1C4_protected_half_s256_extreme_identity_T39954')):
        a,c=index[marker],index[long_marker]
        assert a['noncheap_renewal_counts']==c['noncheap_renewal_counts']
        assert a['ownership_potential']==c['ownership_potential'] or (
            a['ownership_potential']['first_noncheap_B_increments']==c['ownership_potential']['first_noncheap_B_increments'] and
            a['ownership_potential']['repeated_noncheap_zero_change_events']==c['ownership_potential']['repeated_noncheap_zero_change_events'])
        pairs.append({'short':marker,'long':long_marker,'renewal_counts':a['noncheap_renewal_counts'],
            'scope':'Physical index-noncheap graph/mediation invariance; no unsupported F/R_* or C_old selector invariance.'})
    write('REPLICATION_RENEWAL_INVARIANCE.json',pairs)
    m.info.update(complete_sources=104,new_complete_sources=8);m.ok=True
    print('PASS104-source renewal audit, exact C_old geometry, two exact obstructions, all primitive cases and replication invariance',flush=True)
