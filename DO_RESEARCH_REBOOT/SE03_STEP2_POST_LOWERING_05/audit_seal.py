"""Final exact-period, source-ID and proof-interface audit; no old replay."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    fam=json.loads((B/'partial_family.json').read_text());owners={};physical=[]
    for i,p in enumerate(fam['packets']):
        assert p['Q']<=4 or (p['Q']==6 and len(p['macro_indices'])==2)
        for occ in p['occurrences']:
            assert occ not in owners;owners[occ]=i
    assert set(owners)==set(range(1,97));prefix=len(fam['reaching_prefix']);assert prefix==96
    for r in fam['rows']:
        n=prefix+r['occurrence'];physical.append({'absolute_occurrence':n,'period_occurrence':r['occurrence'],
            'mode':r['mode'],'key':r['target'],'packet_owner':owners[r['occurrence']],
            'A_bit_units':[(n,j,b) for j in range(1,r['a']+1) for b in (0,1)],
            'BF_double_demands':[(n,j) for j,e in enumerate(r['BF_events'],1) if e['kind']=='DOUBLE']})
    assert sum(len(r['A_bit_units']) for r in physical)==278
    assert sum(len(r['BF_double_demands']) for r in physical)==54
    assert sum(p['H'] for p in fam['packets'])==139 and sum(p['Q'] for p in fam['packets'])==54
    assert fam['charts'][0]['recent_before']==fam['charts'][-1]['recent_after']
    out('absolute_source_ids.json',{'reaching_prefix_length':prefix,'period_length':96,
        'period':physical,'no_allocation_created_or_unit_spent':True,'absolute_critical_occurrences':list(range(136,142))})
    pins=json.loads((B/'dependency_pins.json').read_text());bad=[]
    for p in pins['pins']:
        q=ROOT/p['path']
        if not q.is_file() or sha(q)!=p['sha256']:bad.append(p['path'])
    for p in pins['external_pins']:
        if sha(Path(p['path']))!=p['sha256']:bad.append(p['path'])
    assert not bad
    out('dependency_revalidation.json',{'status':'PASS','pins_verified':len(pins['pins']),
        'external_pins_verified':len(pins['external_pins']),'mismatches':bad})
    needed=['SOURCE_SPEC.md','POST_LOWERING_NORMAL_FORM.md','FORCED_ZERO_BACKWARD_FRONTIER.md','E1_ZERO_SUFFIX.md',
        'E0_ZERO_SUFFIX.md','E0_PLUS_ONE_SUFFIX.md','SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md']
    assert all((B/f).is_file() for f in needed)
    ind=json.loads((B/'independent_audit.json').read_text());assert ind['status']=='PASS_STRUCTURAL_SUFFIX_REDUCTION_AND_NEW_SOURCE_WITNESS'
    assert all(r['restricted_zero_suffix_exclusion'] for r in ind['new_source_cases'])
    out('seal_audit.json',{'status':'PASS_PARTIAL_UNIVERSAL_SOURCE_RESTRICTIONS_ONLY','terminal_outcome':'D',
        'new_word_operations_covered_once':96,'actual_A_bit_units':278,'actual_BF_demands':54,
        'new_source_replay_mirror_and_gap_lift':'PASS','old_mandatory_fixture_receipts':'reused pinned, new predicates checked',
        'proof_scope_review':{
            'post_loss_branches':'nearest-marked-parent subtrees; same physical side explicitly allowed',
            'cold_leaf':'recency heap from actual parent-edge creation; source complement theorem agrees',
            'zero_frontier':'root degree and deltaL prove only neutralL2 final zero, no q5 or stem zero entry',
            'terminal_pair':'any preceding zero into J2 is loss3->2; K2 has no zero predecessor',
            'paired_zero':'sourceL1 inaccessible by zero; sole +1 needed immediately before exceptional pair',
            'turnaround':'six source one-event root-exposure cases force LL return and exact four-hanger term',
            'shield':'all accesses below cut only; upper crossings explicitly OPEN, not assigned positive price',
            'no_finite_promotion':'40000-state failure inconclusive; universal results have symbolic source proofs',
            'relaxed_frontier':'not actual F11 or B0 membership; no zero/one return certified'},
        'general_E1_zero_suffix':'OPEN','general_E0_zero_suffix':'OPEN','general_E0_plus_one_suffix':'OPEN',
        'complete_cheap_return':False,'new_debt_or_frozen_graph':False,'Step2':'OPEN','Universal_CD':'OPEN',**account})
    print(json.dumps({'status':'PASS_PARTIAL_UNIVERSAL_SOURCE_RESTRICTIONS_ONLY','outcome':'D',
        'pins':len(pins['pins']),'A_bit_units':278,'BF_demands':54,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
