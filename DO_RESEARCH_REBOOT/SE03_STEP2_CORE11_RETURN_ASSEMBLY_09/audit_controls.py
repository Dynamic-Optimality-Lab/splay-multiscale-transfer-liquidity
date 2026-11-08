"""Mandatory source controls plus NEW H2 and H1 timing normal-form predicates.
The accepted earlier source replay implementation is read-only reused.
"""
import collections,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_FINAL_PLUS_ONE_07'
spec=importlib.util.spec_from_file_location('source_replayer07',OLD/'audit_controls2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def normal_form(fam,refl):
    conv=d.reflect if refl else d.freeze;key=lambda k:12-k if refl else k
    word=[(v['mode'],v['key']) if isinstance(v,dict) else tuple(v) for v in fam['word']]
    word=[(mode,key(k)) for mode,k in word]
    raw=[{'occurrence':i,'genuine_F':r['genuine_F'],'a':r['a'],'qF':r['qF']} for i,r in enumerate(fam['rows'],1)]
    _,macros=d.packets(raw);counts=collections.Counter()
    for q in macros:
        H,Q=q['H'],q['Q'];occ=q['occ'];end=occ[-1];z=word[end-1][1]
        if (H,Q) not in ((1,1),(1,2),(2,3)):continue
        g=conv(fam['rows'][occ[0]-1]['before'][0])[0]
        assert g==conv(fam['rows'][occ[0]-1]['before'][1])[0] and g!=z
        positive=[i for i in occ if raw[i-1]['a']]
        assert len(fam['rows'][end-1]['BF_path'])==2*Q
        if H==1:
            assert len(positive)==1 and raw[positive[0]-1]['a']==1
            event=positive[0];assert word[event-1][1]==z
            seen=False
            for i in occ:
                if i==event:seen=True;continue
                if not seen:assert word[i-1][1]==g
                elif i!=end:assert word[i-1]==('D',z)
            counts[f'H1Q{Q}_event_{word[event-1][0]}']+=1
        elif len(positive)==1:
            event=positive[0];assert raw[event-1]['a']==2 and word[event-1][1]==z
            assert len(fam['rows'][event-1]['A_path']) in (3,4)
            pos=occ.index(event)
            assert all(word[i-1][1]==g for i in occ[:pos])
            assert all(word[i-1]==('D',z) for i in occ[pos+1:-1])
            counts['H2Q3_one_operation_two_events_'+word[event-1][0]]+=1
        else:
            assert len(positive)==2 and all(raw[i-1]['a']==1 for i in positive)
            first,second=positive;h=word[first-1][1]
            assert word[first-1][0]=='D' and h not in (g,z) and word[second-1][1]==z
            p,q=occ.index(first),occ.index(second)
            assert all(word[i-1][1]==g for i in occ[:p])
            assert all(word[i-1]==('D',h) for i in occ[p+1:q])
            assert all(word[i-1]==('D',z) for i in occ[q+1:-1])
            counts['H2Q3_two_one_event_operations_D'+word[second-1][0]]+=1
    return dict(counts)
def main():
    cold=json.loads((B.parent/'SE03_STEP2_COLD_NEG2_01/symbolic_replay.json').read_text())['families']
    controls=[(v['name'],v) for v in cold]
    for name,folder,file in [('Sigma_plus1_predecessor','SE03_STEP2_FORCED_ZERO_INCOMING_02','incoming_family_v2.json'),
        ('zero_restoration70','SE03_STEP2_LEAF_LOWERING_03','pattern_family.json'),
        ('E0_68','SE03_STEP2_FIRST_LOWERING_04','entry_family.json'),('E1_90','SE03_STEP2_FIRST_LOWERING_04','e1_family.json'),
        ('post_lowering96','SE03_STEP2_POST_LOWERING_05','partial_family.json')]:
        controls.append((name,json.loads((B.parent/folder/file).read_text())))
    old=json.loads((OLD/'delete_event_control.json').read_text());old['word']=old['source_word']
    controls.append(('Campaign07_DELETE_event',old));reports=[]
    for name,fam in controls:
        for refl in (False,True):
            r=d.replay(name,fam,refl);r['Campaign09_macro_predicates']=normal_form(fam,refl);reports.append(r)
    assert len(reports)==18 and all(r['original_CD_slack']>0 for r in reports)
    out('source_control_replay.json',{'status':'PASS_ALL_MANDATORY_CONTROLS_AND_NEW_NORMAL_FORMS','families':reports,
        'both_immutable_engines':True,'accepted06_and07_controls':'replayed unchanged, not reopened',
        'old_Sigma_corrected_leaves':3,'all_gap_variables':'same rigid ordered terms throughout; no population inference',
        'source_engine_calls':d.calls,'old_semantic_rows_replayed':d.replayed,'new_finite_tests':0,
        'new_theorem_proof_role':'controls only; symbolic lifting, closure and source shape separation prove universality'})
    print(json.dumps({'status':'PASS_ALL_MANDATORY_CONTROLS_AND_NEW_NORMAL_FORMS','cases':len(reports),
        'old_period_rows':d.replayed,'source_engine_calls':d.calls,
        'new_normal_form_totals':dict(sum((collections.Counter(v['Campaign09_macro_predicates']) for v in reports),collections.Counter()))}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_controls_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':d.calls,'old_semantic_rows_replayed':d.replayed,'new_finite_tests':0})
