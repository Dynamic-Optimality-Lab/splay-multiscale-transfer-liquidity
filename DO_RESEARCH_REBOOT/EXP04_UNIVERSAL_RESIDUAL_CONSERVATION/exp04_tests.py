"""Independent operand-tree checks, physical witness replay and legal prefixes."""
from exp04_core import *
from exp04_monotone import enriched
from exp04_density import density_analysis
from exp04_cycles import physical_lifecycles


def prefixes(s):
    diag=s.get('diagonal_initial',s['initial_A']);a=Tree(diag);b=Tree(diag)
    for tag,x in s.get('reaching_prefix',[]):
        Replay.plain_splay(a,x)
        if tag=='K':Replay.plain_splay(b,x)
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    return len(s.get('reaching_prefix',[]))


def check_shadow(r,w):
    full=Tree(w['initial_B']);J=set(w['J']);assert closure(full,w['targets'])==J
    def operand(tree):
        return Tree({'root':tree.root,'children':{str(k):[x if x in J else None for x in tree.ch[k]] for k in J}})
    small=operand(full);ind=r.as_tuple(small);q=0
    for t in w['retained']:
        x=r.ops[t-1][1];path=full.path(x);assert set(path)<=J and path==small.path(x)
        ind,events=r.ind.trace(ind,x);Replay.plain_splay(full,x);small=operand(full)
        assert ind==r.as_tuple(small);q+=sum(e[0]!='ZIG' for e in events)
    assert q==w['shadow_Q'];return len(w['retained'])


if __name__=='__main__':
    meter=Meter('EXP04_verification');checks=0;operations=0;prefixops=0;operand_accesses=0
    manifest=json.loads((ROOT/'EXP04_INPUT_MANIFEST.json').read_text())
    for path,h in manifest['EXP03_files'].items():assert file_hash(PREV/path)==h;checks+=1
    inheritedpins=json.loads((PREV/'EXP03_INPUT_MANIFEST.json').read_text())
    for path,h in inheritedpins['EXP02_complete_delivery_hashes_verified'].items():assert file_hash(OLD/path)==h;checks+=1
    archive=json.loads((ROOT/'EXP04_SOURCE_WITNESSES.json').read_text())
    new=json.loads((ROOT/'EXP04_NEW_SOURCE_CHECKPOINT.json').read_text())['sources']
    new+=json.loads((ROOT/'EXP04_ADVERSARIAL_SOURCES.json').read_text())+json.loads((ROOT/'EXP04_SPARSE_SOURCES.json').read_text())+json.loads((ROOT/'EXP04_FINAL_CYCLE_SOURCES.json').read_text())
    assert len(new)==120 and len({s['name'] for s in new})==120
    assert all(len(s['initial_A']['children'])<=513 and len(s['operations'])<=12000 for s in new)
    for s in archive['inherited_sources']+new:prefixops+=prefixes(s);checks+=1
    oldrows=json.loads((ROOT/'EXP04_RESIDUAL_INVENTORY.json').read_text())['inherited_sources']
    newrows=json.loads((ROOT/'EXP04_NEW_RESULTS.json').read_text())+json.loads((ROOT/'EXP04_ADVERSARIAL_RESULTS.json').read_text())+json.loads((ROOT/'EXP04_SPARSE_RESULTS.json').read_text())+json.loads((ROOT/'EXP04_FINAL_CYCLE_RESULTS.json').read_text())
    by={z['source']:z for z in oldrows+newrows}
    names={'IH_p4_q1_L2_z5_c1','Xprobe_p4_L3_hitNone_boundary1','mixed_p5_Gcopies2',
        'IH_p4_q1_L3_z1-65_c1_periods4','holes_p4_h4_z5_r1','mixed_p4_Gcopies2_protected5_cut258',
        'scramble_p5_dyadic','composed_p4_alternating_inside_m256','composed_p6_bitreverse_inside_m256',
        'leafscan_p3_sweep','sparseH_p5_hits5_hole4','osc_p4_m1024_inside_off0'}
    comparisons=[];causal=[]
    for s in archive['inherited_sources']+new:
        if s['name'] not in names:continue
        r=Replay(s);row=by[s['name']];assert digest(r.events)==s['trace_hash']==row['trace_hash']
        assert r.A==row['A'] and r.Q==row['Q_B'] and r.closed
        for e in row['events']:
            pair=next(p for p in r.pairs if p['rho']==e['rho']);assert pair['class']=='R6' and pair['parent']==e['original_parent']
        if row['R_star']:
            m=enriched(r,row)
            for z in m['monotone_comparison']['systems']:
                assert sum(w['domain_size'] for w in z['windows'])<=2*r.A
                for w in z['windows']:operand_accesses+=check_shadow(r,w)
            eps,ps=psi_episodes(r);den=density_analysis(r,row['events'],eps)
            assert sum(w['density_D'] for w in den['windows'])<=4*r.A
            assert sum(w['original_A'] for w in den['windows'])<=r.A
            for w in den['windows']:
                assert len(w['J'])+len(w['targets'])+w['integer_rank_travel']==w['density_D']
                assert w['density_D']<=4*w['original_A']
            lf=physical_lifecycles(r,row['events']);causal.append(lf)
            comparisons.append({'source':s['name'],'after_monotone':len(m['after_monotone']),
                'after_cycle_certificate':len(m['remaining']),'density_unpaid':len(den['remaining']),
                'operand_accesses_checked':sum(len(w['retained']) for z in m['monotone_comparison']['systems'] for w in z['windows'])})
            write(f"EXP04_VERIFIED_TRACE_{digest(s['name'])[:12]}.json",{'source':s,'events':r.events,'boundaries':r.boundaries,
                'original_R_star':row['events'],'class_comparisons':m,'density_windows':den,'lifecycles':lf})
        operations+=r.independent_checks;checks+=len(r.ops)+8
        print('verified',s['name'],flush=True);del r
    assert len(names)==12
    collision=next(s for s in causal if s['source']=='scramble_p5_dyadic')
    parent=next(p for p in collision['parents'] if p['original_parent']==[400,2])
    assert parent['B_continuous_from_last_A_loss'] is False
    assert parent['last_A_loss']['id']==['A',324,7,0]
    own=next(s for s in causal if s['source']=='composed_p6_bitreverse_inside_m256')
    assert any(p['original_parent']==[1032,1] and p['g'] in p['A_path'][:-1] for p in own['parents'])
    write('EXP04_CRITICAL_LIFECYCLE_VALIDATION.json',causal)
    write('EXP04_INDEPENDENT_OPERAND_VALIDATION.json',comparisons)
    write('EXP04_TEST_RESULTS.json',{'status':'PASS','checks':checks,'critical_sources_replayed':12,
        'additional_independent_original_operations':operations,'independent_pruned_operand_accesses':operand_accesses,
        'source_prefixes_checked':380,'prefix_operations':prefixops,
        'qualification':'Independent immutable tuple states/costs and pruned operand traces. Full Pi/cohort/R6 uses the inherited exact oracle, not a second independent symbolic classifier. Universal proofs are same-agent arguments conditional on inherited and cited external theorems.'})
    meter.success=True;meter.details.update(checks=checks,critical_sources=12,independent_operations=operations)
