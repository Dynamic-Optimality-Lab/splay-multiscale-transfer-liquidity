"""New source family: an actual +1 incoming edge at the Sigma forced-zero state.
The old controls are read as receipts, not re-executed. All holes stay opaque.
"""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import replay,packets,charts,shadow,trace,core,labels,SCAN
account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(freeze(x) for x in v) if isinstance(v,list) else v
def ident(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def state(r,c,z):return {'A':r[0],'BF':r[1],'BE':r[2],'M':[1,3,5,7,9,11],
                       'erased':z,'recent':c,'packet_phase':'ready'}
def reflect(t):
    if isinstance(t,str):return 'F'+str(11-int(t[1:]))
    return (12-t[0],reflect(t[2]),reflect(t[1]))
def main():
    old=json.loads((OLD/'symbolic_replay.json').read_text())['families'][2]
    w=[('K',x) for x in [9,1,3,5,3,1,11,1,3,5,9,11,9,5,3,1]]
    w += [('D',x) for x in SCAN+[4,1,7,1,7,3]]
    w += [('K',3),('K',1),('K',7)]
    w += [('D',x) for x in SCAN+[7]]
    w += [('K',x) for x in [1,3,5,7,5,3,1]]
    assert len(w)==75
    initial=freeze(old['initial_full_diagonal']);estart=freeze(old['auxiliary_recurrent_start'])
    rows,end=replay(initial,w,7,estart);account['source_engine_calls']+=sum(1+(r['mode']=='K')+(r['mode']=='K' and r['target']!=7) for r in rows)
    assert end==(initial,initial,estart)
    cc=charts(rows,[1,3,5,7,9,11]);ps=packets(rows)
    # Natural boundary44 is K3;45 is K1;46 is cold K7.
    before=state(rows[43]['after'],cc[43]['recent_after'],7)
    forced=state(rows[44]['after'],cc[44]['recent_after'],7)
    target=state(rows[45]['after'],cc[45]['recent_after'],7)
    known=next(r for r in json.loads((B/'forced_regions.json').read_text())['records'] if r['family']=='Sigma_singleton')
    assert forced==known['F_state'] and target==known['T_state']
    pin=next(p for p in ps if p['end']==45);neg=next(p for p in ps if p['end']==46)
    assert (pin['H'],pin['Q'],pin['w'],pin['occurrences'])==(1,1,1,[45])
    assert (neg['H'],neg['Q'],neg['w'],neg['occurrences'])==(1,4,-2,[46]) and cc[45]['cold']
    assert rows[43]['a']==0 and rows[44]['a']==1
    # This is NOT a forced-two predecessor. Its BF has only two marked leaves.
    def leaves(t):
        return 0 if t is None else (int(t[0] in (1,3,5,7,9,11)) if t[1] is None and t[2] is None else leaves(t[1])+leaves(t[2]))
    assert leaves(core(freeze(before['BF']),{1,3,5,7,9,11}))<4
    # Fresh family has the SAME B KEEP word, hence same proven BE recurrence.
    assert [x for k,x in w if k=='K']==[r['key'] for r in old['word'] if r['mode']=='K']
    mirrored=reflect(initial);er=reflect(estart);mw=[(k,12-x) for k,x in w]
    mr,me=replay(mirrored,mw,5,er);account['source_engine_calls']+=sum(1+(r['mode']=='K')+(r['mode']=='K' and r['target']!=5) for r in mr)
    assert me==(mirrored,mirrored,er)
    for r,m in zip(rows,mr):
        assert tuple(reflect(t) for t in r['after'])==m['after']
        assert (r['a'],r['qF'],r['qE'])==(m['a'],m['qF'],m['qE'])
    out('incoming_family.json',{'name':'Sigma_incoming_plus_one','word':w,'initial_A_B':initial,'auxiliary_recurrent_start':estart,
        'rows':rows,'charts':cc,'packets':ps,'incoming_packet':pin,'negative_packet':neg,
        'predecessor':before,'F_state':forced,'T_state':target,
        'predecessor_id':ident(before),'F_id':ident(forced),'T_id':ident(target),
        'costs':{'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),
                 'CD_slack':2*sum(r['a'] for r in rows)-sum(r['qF'] for r in rows)},
        'closure':{'A':True,'BF':True,'BE':True,'recent':True,'legal_reaching_prefix':'one original period of the inherited Sigma KEEP word; B word unchanged'},
        'reflection_proved':True,'universal_gap_substitution':'all Fi arbitrary finite ordered BSTs; no request enters a hole',
        'new_constraint':'Dstar(predecessor)<=1 conditional on feasibility; no independent forced-two claim',
        'old_Dhat_at_predecessor':'not inferred; no additional normalization failure claimed',**account})
    print(json.dumps({'status':'PASS_NEW_EXACT_PLUS_ONE_INCOMING_FAMILY','incoming_H_Q_w':[1,1,1],
        'negative_H_Q_w':[1,4,-2],'same_exact_Sigma_F_T':True,'A':sum(r['a'] for r in rows),
        'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),**account}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_incoming_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
