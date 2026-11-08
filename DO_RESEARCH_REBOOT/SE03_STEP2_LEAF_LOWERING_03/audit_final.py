"""Independent new-variant replay and final source/ownership interface audit."""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as f
account={'source_engine_calls':0,'new_finite_tests':0};M={1,3,5,7,9,11}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as g:json.dump(v,g,indent=2)
def term(v):return ('leaf',v) if isinstance(v,str) else f.node(v[0],term(v[1]),term(v[2]))
def mirror(v):
    if isinstance(v,str):return 'F'+str(11-int(v[1:]))
    return [12-v[0],mirror(v[2]),mirror(v[1])]
def step(v,x):
    account['source_engine_calls']+=1
    return f.trace(v,x)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def leaf(t):
    if t[0]=='leaf':return 0
    return int(t[1] in M and not marked(t[2]) and not marked(t[3]))+leaf(t[2])+leaf(t[3])
def marked(t):return t[0]!='leaf' and (t[1] in M or marked(t[2]) or marked(t[3]))
def main():
    data=json.loads((B/'varied_sources.json').read_text());records=[]
    assert len(data['starts'])==32 and data['candidate'] is None
    for i,s in enumerate(data['starts']):
        for refl in (False,True):
            conv=mirror if refl else lambda q:q
            a=b=term(conv(s['initial']));e=term(conv(s['erased_start']));z=9 if refl else 3
            lru=[]
            for mode,x in reversed(s['word']):
                if mode=='K' and x not in lru:lru.append(x)
            if refl:lru=[12-x for x in lru]
            initial_lru=lru[:];critical=s['negative_packet']['occurrences'];costs=[]
            for occ,(mode,k) in enumerate(s['word'],1):
                x=12-k if refl else k;aa,ae=step(a,x);a=aa;be=[]
                if mode=='K':
                    b,be=step(b,x);lru.remove(x);lru.insert(0,x)
                    if x!=z:e,_=step(e,x)
                if occ in critical:costs.append([len(ae),sum(q[0]!='ZIG' for q in be)])
                if occ==s['negative_packet']['end']:
                    old=s['start_T'];assert (a,b,e)==tuple(term(conv(q)) for q in old[:3])
                    assert tuple(lru)==tuple(12-x for x in old[3]) if refl else tuple(lru)==tuple(old[3])
            assert a==b==term(conv(s['initial'])) and e==term(conv(s['erased_start']))
            assert lru==initial_lru and costs==[[1,5],[1,1]]
        records.append({'start':i,'whole_word_and_mirror_closed':True,'negative_packet_actual_costs':[[1,5],[1,1]],
            'complete_T_state_equal':True})
    fam=json.loads((B/'pattern_family.json').read_text());cover={};eventids=[]
    for p in fam['packets']:
        for x in p['occurrences']:cover[x]=cover.get(x,0)+1
    assert cover=={i:1 for i in range(1,71)}
    for r in fam['rows']:
        occ=r['occurrence'];units=[(occ,j,bit) for j in range(1,r['a']+1) for bit in (0,1)]
        demands=[(occ,j) for j,e in enumerate(r['BF_events'],1) if e['kind']=='DOUBLE']
        eventids.append({'absolute_occurrence':occ,'mode':r['mode'],'key':r['target'],
            'A_bit_units':units,'BF_double_demands':demands})
    assert sum(len(q['A_bit_units']) for q in eventids)==166
    assert sum(len(q['BF_double_demands']) for q in eventids)==26
    assert sum(p['H'] for p in fam['packets'])==83 and sum(p['Q'] for p in fam['packets'])==26
    assert fam['charts'][0]['recent_before']==fam['charts'][-1]['recent_after']
    assert all(p['Q']!=5 for p in fam['packets'])
    out('absolute_source_ids.json',{'period_length':70,'prefix_length':0,'auxiliary_preperiod':0,
        'operations':eventids,'no_unit_assigned_or_spent':True,'all_source_occurrences_covered_once':True})
    pins=json.loads((B/'dependency_pins.json').read_text());bad=[]
    for p in pins['pins']:
        q=ROOT/p['path']
        if not q.is_file() or h(q)!=p['sha256']:bad.append(p['path'])
    for p in pins['external_pins']:
        if h(Path(p['path']))!=p['sha256']:bad.append(p['path'])
    assert not bad
    required=['SOURCE_SPEC.md','LEAF_LOWERING_CLASSIFICATION.md','REGENERATION_AND_REPETITION.md','ZERO_RETURN.md',
        'ONE_PLUS_RETURN.md','SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md']
    assert all((B/n).is_file() for n in required)
    out('dependency_revalidation.json',{'status':'PASS','pins_verified':len(pins['pins']),
        'external_pins_verified':len(pins['external_pins']),'mismatches':bad})
    out('final_audit.json',{'status':'PASS_PARTIAL_SOURCE_RESULT_ONLY','terminal_outcome':'D',
        'new32_T_source_families_independently_closed':records,'pattern_word_original_ownership_once':True,
        'source_period_events_83_units166_Bdemands26':True,'all_known_term_closures_independently_checked':'independent_audit.json',
        'universal_first_loss_prefix_proof_review':{
            'source_leaf_bound':'q proper marked ancestors are nonleaves, hence L<=6-q',
            'prefix_lower_bound':'before first zero loss all zeros nondecreasing and at most one positive edge loses at most1: L>=3',
            'no_H2_zero':'q4 requires L<=2, q5 pair requires L1',
            'positive_one_before_first_loss':'before sole positive edge L>=4, excluding q3 (L<=3)',
            'arbitrary_anonymous_helpers':'positive accesses target marks in H1 prefix; anonymous A parents remain allowed',
            'global_conclusion':'first-loss entry remains OPEN; no existence/potential claim'},
        'Sigma_leaf_count_erratum_nonessential':True,'general_R0_R1':'OPEN','Step2':'OPEN','Universal_CD':'OPEN',
        'new_frozen_graph_or_solver':False,'audit_kind':'same-agent separate immutable source engine and derivation; not external peer review',
        **account})
    print(json.dumps({'status':'PASS_PARTIAL_SOURCE_RESULT_ONLY','outcome':'D','pins':len(pins['pins']),
        'new_source_families':32,'mirrors':True,'period_A_bits':166,'BF_demands':26,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_final_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
