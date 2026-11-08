"""Final proof/interface audit; no old source replay or solver call."""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    pins=json.loads((B/'dependency_pins.json').read_text())['pins'];bad=[]
    for p in pins:
        q=Path(p['path']);q=q if q.is_absolute() else ROOT/q
        if not q.is_file() or sha(q)!=p['sha256']:bad.append(p['path'])
    assert not bad
    required=['FZ_SOURCE_SPEC.md','FORCED_REGION_RECONSTRUCTION.md','ZERO_PREDECESSOR_CLOSURE.md',
        'PLUS_ONE_PREDECESSORS.md','RETURN_BARRIER.md','EXACT_SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md']
    assert all((B/q).is_file() for q in required)
    f=json.loads((B/'incoming_family_v2.json').read_text());ind=json.loads((B/'independent_audit.json').read_text())
    assert ind['status']=='PASS_SEPARATE_SOURCE_AND_FRAME_DERIVATIONS'
    counts={}
    for p in f['packets']:
        for n in p['occurrences']:counts[n]=counts.get(n,0)+1
    assert counts=={i:1 for i in range(1,76)}
    assert sum(p['H'] for p in f['packets'])==93 and sum(p['Q'] for p in f['packets'])==42
    # Last and first boundaries do not hide an unpaired q5 at the cyclic seam.
    assert all(p['Q']!=5 for p in f['packets'])
    assert f['charts'][0]['recent_before']==f['charts'][-1]['recent_after']
    assert all(f['closure'].get(q) is True for q in ('A','BF','BE','recent'))
    # New word KEEP sequence equals the accepted old word, so BE map is exactly the same.
    old=json.loads((B.parent/'SE03_STEP2_COLD_NEG2_01/symbolic_replay.json').read_text())['families'][2]
    prefix=[(r['mode'],r['key']) for r in old['word']]
    assert [x for k,x in prefix if k=='K']==[x for k,x in f['word'] if k=='K']
    base=len(prefix);ids=[]
    for r in f['rows']:
        occ=base+r['occurrence'];bits=[];demands=[]
        for j,e in enumerate(r['A_events'],1):
            bits.extend([{'absolute_occurrence':occ,'StepEv':j,'bit':b} for b in (0,1)])
        for j,e in enumerate(r['BF_events'],1):
            if e['kind']=='DOUBLE':demands.append({'absolute_occurrence':occ,'BF_StepEv':j})
        ids.append({'absolute_occurrence':occ,'period_occurrence':r['occurrence'],'mode':r['mode'],
                    'target':r['target'],'A_bit_units':bits,'BF_double_demands':demands})
    assert sum(len(q['A_bit_units']) for q in ids)==186
    assert sum(len(q['BF_double_demands']) for q in ids)==42
    out('absolute_source_ids.json',{'reaching_prefix_word':prefix,'reaching_prefix_length':base,
        'prefix_provenance':'accepted original Sigma period, endpoints/auxiliary transient inherited without replay',
        'actual_recurrent_period_word':f['word'],'predecessor_absolute_boundary':base+44,
        'F_absolute_boundary':base+45,'T_absolute_boundary':base+46,'period_operations':ids,
        'physical_allocation_created':False,'no_unit_assigned_or_spent':True})
    search=json.loads((B/'search_result.json').read_text());assert search['candidate'] is None
    assert search['states_total']==12 and search['candidate_packet_proposals']==20
    # The proof review is explicit about the induction/lifting needed beyond code assertions.
    checks={
        'forced_range_endpoints':'range endpoints are forced by -2; no old formula used',
        'arbitrary_zero_predecessors':'finite-path telescoping and no-last-edge proof for restricted C11',
        'cost_exhaustion':'singleton Q<=4,H>=1; pair Q6,H>=2; large H automatic',
        'core_constancy':'labeled set inclusion along every original KEEP and exact closure',
        'first_entry':'fan q_next<=6-q excludes q3/q4 outputs before q4/q5; pair output q_next<=2',
        'U_unary_extreme':'two independent SS identities plus processed-subtree persistence',
        'marked_leaf_identity':'off-path parents fixed; only target and its old ancestors can change leaf status',
        'leaf_return_bound':'six marks give F<=2,T>=4; only H1q1/q2 may lose leaves along cheap paths; count losses',
        'source_hangers':'new word never enters holes; source claims lift by structural substitution induction',
        'limits':'search does not cover anonymous helper targets; universal parent barrier explicitly remains OPEN',
        'ownership':'no allocation created; every new word operation has one packet owner and absolute IDs',
        'scope':'core11 lemmas do not exclude core9/10 or identify changing recent-five charts'}
    out('dependency_revalidation.json',{'status':'PASS','pins_verified':len(pins),'mismatches':bad})
    out('seal_audit.json',{'status':'PASS_PARTIAL_SOURCE_RESULT_ONLY','outcome':'D',
        'files_present':required,'all_new_source_operations_covered_exactly_once':True,
        'current_family_absolute_period_ids':True,'complete_actual_state_closure':True,
        'proof_review':checks,'scope_universal_barrier':'OPEN','width2_existence':'OPEN',
        'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','new_frozen_graph_or_solver':False,
        'audit_kind':'same-agent independent source engine and separately checked mathematical derivation; not external review',**account})
    print(json.dumps({'status':'PASS_PARTIAL_SOURCE_RESULT_ONLY','outcome':'D','pins_verified':len(pins),
        'original_occurrences_covered_once':75,'A_bit_units':186,'BF_double_demands':42,**account}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
