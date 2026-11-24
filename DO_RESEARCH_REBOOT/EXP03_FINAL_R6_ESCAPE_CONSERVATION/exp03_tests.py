"""End-to-end exact checks; no empirical bound is promoted to a theorem."""
from exp03_restart import *
from exp03_inheritance import file_hash


def verify_prefix(s):
    diagonal=s.get('diagonal_initial',s['initial_A'])
    if not s.get('reaching_prefix'):
        assert s['initial_A']==s['initial_B'];return 0
    a=Tree(diagonal);b=Tree(diagonal)
    for tag,x in s['reaching_prefix']:
        assert tag in ('K','D') and x in a.keys
        Replay.plain_splay(a,x)
        if tag=='K':Replay.plain_splay(b,x)
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    return len(s['reaching_prefix'])


def audit_gp(r):
    results=[]
    for wi,path in enumerate(sorted((ROOT/'EXP02_TRAJECTORIES').glob(digest(r.source['name'])[:16]+'_*.json'))):
        tr=json.loads(path.read_text());pool=tr['state_pool'];L=M=0;operation_rows=[]
        for acc in tr['retained_accesses']:
            t=acc['original_operation'];x=acc['target']
            def frames(actor):
                return frame_records(pool[acc[actor+'_pre']['state_sha256']],x,pool[acc[actor+'_post']['state_sha256']])
            ga=[f['g'] for f in frames('actual').values()];gs=[f['g'] for f in frames('shadow').values()]
            assert len(ga)==len(set(ga)) and len(gs)==len(set(gs))
            missing=sorted(set(ga)-set(gs));extra=sorted(set(gs)-set(ga))
            assert len(ga)-len(gs)==len(missing)-len(extra)==acc['difference']
            L+=len(missing);M+=len(extra)
            operation_rows.append({'operation':t,'G_actual':ga,'G_shadow':gs,'L':missing,'M':extra})
        assert L-M==tr['delta']
        results.append({'trajectory_file':str(path.relative_to(ROOT)),'sum_L':L,'sum_M':M,'delta':tr['delta'],'operations':operation_rows})
    return results


if __name__=='__main__':
    meter=Meter('tests');checks=0;ops_count=prefix_count=shadow_count=0
    manifest=json.loads((ROOT/'EXP03_INPUT_MANIFEST.json').read_text())
    for path,h in manifest['EXP02_complete_delivery_hashes_verified'].items():assert file_hash(OLD/path)==h;checks+=1
    for path,h in manifest['additional_repository_pins'].items():assert file_hash(REPO/path)==h;checks+=1
    archive=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
    data=json.loads((ROOT/'EXP03_CAUSAL_EPISODE_RESULTS.json').read_text())
    byname={s['source']:s for s in data['inherited_sources']+data['new_sources']}
    gp_audit=[];restart_validation=[]
    for s in archive['inherited_sources']+archive['new_sources']:
        prefix_count+=verify_prefix(s);checks+=1
        if s['name'] not in byname:continue # Other 163 already replayed in inheritance.
        z=byname[s['name']];r=Replay(s)
        assert digest(r.events)==s['trace_hash']==z['trace_hash']
        assert r.A==z['A'] and r.Q==z['Q_B'] and r.closed
        p=parent_sets(z['unhandled_events']);assert p==z['parent_interface']
        for e in z['unhandled_events']:
            pair=next(p0 for p0 in r.pairs if p0['rho']==e['rho'])
            assert pair['class']=='R6' and pair['parent']==e['original_parent']
        eps=actual_mismatch_episodes(r);assert eps==z['actual_mismatch_episodes']
        restart=restart_analysis(r,z['unhandled_events'],eps)
        assert restart['paid_original_gaps']==z['restart_comparison']['paid_original_gaps']
        assert restart['sum_J']==z['restart_comparison']['sum_J']<=2*r.A
        assert sum(w['domain_size'] for w in restart['windows'])<=2*restart['original_A_transition_count']
        # Verify complete physical original A pivots exhaust each target's prepath.
        for row in r.boundaries:
            pivots=[e['pivot'] for e in r.events[row['start_time']:row['post_A_time']]]
            assert len(pivots)==len(set(pivots)) and set(pivots)==set(row['A_path'][:-1])
        gp_audit.append({'source':s['name'],'windows':audit_gp(r)})
        for w in restart['windows']:shadow_count+=w['independently_checked_shadow_accesses']
        restart_validation.append({'source':s['name'],'windows':len(restart['windows']),'independent_shadow_accesses':sum(w['independently_checked_shadow_accesses'] for w in restart['windows']),
            'sum_J':restart['sum_J'],'A_transition_witnesses':restart['original_A_transition_count'],'paid':restart['paid_gap_count']})
        ops_count+=r.independent_checks;checks+=10+len(r.boundaries)
        print('verified',s['name'],flush=True)
        del r
    # Primary exact obligations and source-wide selector collision.
    primary=json.loads((ROOT/'EXP03_PRIMARY_LIFECYCLE.json').read_text())
    assert primary['costs']=={'A':259,'Q_B':110,'operations':259}
    assert primary['common_ancestors']==[2,4] and primary['B_only_ancestors']==[6,10,18,34,50]
    assert primary['last_A_loss']['id']==['A',113,1,0] and primary['last_A_loss']['original_SET_sign']==0
    assert sum(len(s['unhandled_events']) for s in data['inherited_sources'])==14
    assert sum(s['restart_comparison']['paid_gap_count'] for s in data['inherited_sources'])==4
    assert any(s['parent_interface']['counts']['X'] for s in data['new_sources'])
    assert any(s['last_loss_selector']['maximum_primitive_load']>1 for s in data['new_sources'])
    # Parametric first rotation on a full physical vine: n changed ordered
    # ancestry pairs for one original A StepEv; B remains untouched.
    ancestry_examples=[]
    for n in (9,17,33,65,129,257,513):
        tree=Tree(vine(range(1,n+1)));before={(u,x) for x in tree.keys for u in tree.path(x)[:-1]}
        tree.rotate(1,1);after={(u,x) for x in tree.keys for u in tree.path(x)[:-1]}
        assert len(before-after)==n-1 and len(after-before)==1
        ancestry_examples.append({'physical_population':n,'lost_pairs':n-1,'created_pairs':1,'A_StepEv':1,'disagreement_increase':n})
    write('EXP03_GRANDPARENT_SET_AUDIT.json',gp_audit)
    write('EXP03_RESTART_INDEPENDENT_VALIDATION.json',restart_validation)
    write('EXP03_ANCESTRY_MASS_REFUTATION.json',{'exact_rotation_examples':ancestry_examples,
        'parametric_complete_source':'IH_p_q1_L2_z5_c1, n=2^(p+2)+1, p>=3; first original operation DELETE2, first bit A(1,1,0). Complete period is the saved omitted family.'})
    result={'status':'PASS','checks':checks+7,'additional_independent_original_operations':ops_count,
        'independent_restart_shadow_accesses':shadow_count,'legal_prefix_operations':prefix_count,'sources_replayed':len(byname),
        'limitations':'Independent immutable tuple engine validates physical states/costs. Full Pi/cohort/R6 certification remains the inherited exact oracle, not a second independent symbolic certifier. New universal proofs are same-agent mathematical arguments, not formal or external certification.'}
    write('EXP03_TEST_RESULTS.json',result);meter.details.update(result);meter.success=True
    print(json.dumps(result,indent=2),flush=True)
