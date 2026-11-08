"""Exact source control: move Sigma predecessor's unique A event to DELETE.
This is a NEW word with new physical occurrences, not a transport of funding.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('replayer07',B/'audit_controls2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d);p=d.p;primary_calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    global primary_calls
    old=json.loads((B.parent/'SE03_STEP2_FORCED_ZERO_INCOMING_02/incoming_family_v2.json').read_text())
    word=[tuple(v) for v in old['word']];end=old['incoming_packet']['end'];m,y=word[end-1];assert m=='K'
    word.insert(end-1,('D',y));R=d.freeze(old['rows'][0]['before'][0]);E=d.freeze(old['rows'][0]['before'][2]);z=old['predecessor']['erased']
    primary_calls=sum(1+(m=='K')+(m=='K' and k!=z) for m,k in word)
    rows,final=p.replay(R,word,z,E);assert final==(R,R,E)
    fam={'name':'Sigma_unique_A_event_on_DELETE','word':word,'rows':rows,'charts':p.charts(rows,sorted(d.a.M)),
        'packets':p.packets(rows),'erased':z,'initial':R,'auxiliary_recurrent_start':E}
    packet=next(q for q in fam['packets'] if q['end']==end+1)
    assert (packet['H'],packet['Q'],packet['w'])==(1,1,1) and packet['occurrences']==[end,end+1]
    assert rows[end-1]['mode']=='D' and rows[end-1]['a']==1 and rows[end]['a']==0
    assert rows[end]['after']==tuple(d.freeze(v) for v in old['rows'][end-1]['after'])
    # Both implementations verify every original operation in the new word.
    reports=[d.replay('Sigma_unique_A_event_on_DELETE',fam,ref) for ref in (False,True)]
    assert all(r['A']==93 and r['QF']==42 and r['QE']==32 and r['H1Q1_positive_event_mode_counts'].get('D',0)>=1 for r in reports)
    out('delete_event_control.json',{'status':'PASS_SOURCE_EXACT_DELETE_EVENT_VARIANT','source_word':word,
        'common_initial':R,'auxiliary_recurrent_start':E,'erased':z,'rows':rows,'charts':fam['charts'],'packets':fam['packets'],
        'unique_DELETE_occurrence':end,'terminal_KEEP_occurrence':end+1,'reports':reports,
        'funding_transfer_claimed':False,'original_75_word_unchanged':True,'new_absolute_occurrences':'separate control word only',
        'source_engine_calls':d.calls+primary_calls,
        'new_finite_tests':0})
    print(json.dumps({'status':'PASS_SOURCE_EXACT_DELETE_EVENT_VARIANT','period':len(word),'DELETE_occurrence':end,
        'terminal_KEEP_occurrence':end+1,'H_Q_w':[1,1,1],'reports':reports}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_delete_event_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':d.calls+primary_calls,'old_semantic_rows_replayed':0,
        'new_source_rows_replayed':d.replayed,'new_finite_tests':0})
