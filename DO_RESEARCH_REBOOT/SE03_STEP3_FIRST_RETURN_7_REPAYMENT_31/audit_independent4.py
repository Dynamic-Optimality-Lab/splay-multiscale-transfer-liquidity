"""Static revision bridge: no tree engine, source call or accepted replay.

The revised closure manuscript explains the distinction between the replayed
short BE trace and the later periodized BE orbit. Check the exact new word
descriptor, literal shallow-frame variation and source-clock arithmetic;
do not misrepresent these checks as executing the symbolic closed period.
"""
import json,hashlib,math,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    c=read(B/'prefix_first_return_countercertificate_v2.json')
    a=read(B/'final_independent_proof_audit.json')
    old=read(P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json')
    # Previous evaluated inputs except the manuscript are unchanged.
    for n,h in a['input_sha256'].items():
        if n!='CLOSED_COUNTEREXAMPLE_PROOF.md':assert sha(B/n)==h
    current=sha(B/'CLOSED_COUNTEREXAMPLE_PROOF.md');previous=a['input_sha256']['CLOSED_COUNTEREXAMPLE_PROOF.md']
    assert previous!=current
    oldframe=next(z for z in old['rows'] if z['occurrence']==117)['before'][0]
    newframe=c['new_rows'][7]['before'][0]
    assert oldframe[0]==newframe[0]==13 and oldframe[1][0]==newframe[1][0]==7
    assert oldframe[1][1]==newframe[1][1]
    old11=oldframe[1][2];new11=newframe[1][2]
    assert old11[0]==new11[0]==11 and old11[2]==new11[2] and oldframe[2]==newframe[2]
    assert old11[1]==[8,'F7',[10,[9,'F8','F9'],'F10']]
    assert new11[1]==[9,[8,'F7','F8'],[10,'F9','F10']]
    # Literal source word; all support keys genuinely changing by the
    # already checked source/inverse identities, not inferred from this set.
    assert c['closed_block_W']==c['P_word']+c['inverse_word']+c['support_loop']+c['last_A_reset']
    assert tuple(map(len,(c['P_word'],c['inverse_word'],c['support_loop'],c['last_A_reset'])))==(45,40,2,14)
    assert c['support_loop']==[['K',1],['K',3]]
    assert c['last_A_reset']==[['D',x] for x in range(13,0,-1)]+[['D',3]]
    s=c['symbolic_closed_history'];C=math.comb(26,13)//14
    assert C==s['C']==742900
    assert s['M_expression']=={'op':'factorial','argument':C}
    assert s['reaching_word']=={'concat':['known_reaching_prefix_N',{'repeat':'closed_block_W','times':C}]}
    assert s['source_period']=={'repeat':'closed_block_W','times':{'op':'factorial','argument':C}}
    assert s['initial_BE']=={'iterate':'F_E','times':C,'seed':'known_erased_seed_E0'}
    assert len(c['known_reaching_prefix_N'])==85
    for kind,pos in [('helper',39),('upper',41),('return',44)]:
        assert s['first_counter_'+kind+'_absolute']==85+101*C+pos
    # No factorial is expanded and no F iterate is evaluated. The general
    # orbit/divisibility implication is the written mathematical proof.
    text=(B/'CLOSED_COUNTEREXAMPLE_PROOF.md').read_text(encoding='utf-8')
    assert 'They are NOT asserted to be the' in text and 'erased states in the later periodized copy' in text
    out('revision_bridge_audit.json',{'status':'PASS_STATIC_MANUSCRIPT_REVISION_BRIDGE',
        'new_source_queries':0,'new_tree_operations':0,'previous_manuscript_sha256':previous,
        'current_manuscript_sha256':current,'source_counter_descriptor_unchanged':True,
        'exact_A_scope_difference':'ONLY the ordered subtree below11 changes:8(.,10(9,.)) to9(8,10)',
        'literal_word_and_clock_checked':True,'short_BE_periodized_BE_distinction_explicit':True,
        'W101_or_full_period_executed':False,
        'scope':'static literal-descriptor/frame/arithmetic provenance; mathematical inverse/reset/orbit induction is a written proof, not checked by a formal proof assistant',
        'input_sha256':{n:sha(B/n) for n in ('prefix_first_return_countercertificate_v2.json','CLOSED_COUNTEREXAMPLE_PROOF.md','FIX_9_activation_control.json')}})
    print(json.dumps({'status':'REVISION_BRIDGE_PASS','source_queries':0,'A_scope_difference':'only below11','full_period_replayed':False}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent4_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
