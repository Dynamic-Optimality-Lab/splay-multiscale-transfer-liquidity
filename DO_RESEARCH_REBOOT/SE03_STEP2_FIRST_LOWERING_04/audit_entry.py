"""Source-exact E0 entry, rebased to the original eleven distinguished keys."""
import collections,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import trace,vine,core,labels,replay,packets,charts,SCAN
M=(1,3,5,7,9,11);account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def step(t,x):
    account['source_engine_calls']+=1
    return trace(t,x)
def leaf(t):return 0 if t is None else int(t[0] in M) if t[1] is None and t[2] is None else leaf(t[1])+leaf(t[2])
def b_return(s,R):
    todo=collections.deque([s]);parent={s:None}
    while todo:
        b=todo.popleft()
        if b==R:
            w=[]
            while parent[b] is not None:b,x=parent[b];w.append(x)
            return w[::-1],len(parent)
        for x in M:
            if x==b[0]:continue
            nb,_,ev=step(b,x)
            if not all(e['kind']=='DOUBLE' and e['case'] in ('LL','RR') and e['G'] in M and e['P'] not in M for e in ev):continue
            if labels(core(nb,set(M)))!=set(range(1,12)) or nb in parent:continue
            assert len(parent)<15000
            parent[nb]=(b,x);todo.append(nb)
    raise AssertionError('no closed B repair in bounded construction')
def main():
    R=vine(11);a=R
    for x in (10,1):a=step(a,x)[0]
    for x in (11,1,3,5):
        a,_,ev=step(a,x);assert len(ev)==1
    b=R
    for x in (11,1,3,5):b=step(b,x)[0]
    ret,visited=b_return(b,R)
    warm=[3,5,7,9,11,9,7,5,3,1]
    word=[('K',x) for x in warm[:-1]]+[('D',x) for x in SCAN+[10,1]]
    word += [('K',1),('K',11),('K',1),('K',3),('K',5)]
    assert len(word)==37
    word += [('D',x) for x in SCAN+[11,1,3,5]]+[('K',x) for x in ret]
    z=3;e=R;seen={};orbit=[]
    for j in range(65):
        if e in seen:break
        seen[e]=j;orbit.append(e)
        for k,x in word:
            if k=='K' and x!=z:e=step(e,x)[0]
    else:raise AssertionError('erased recurrence exceeds65-copy construction cap')
    u=seen[e];L=len(orbit)-u;assert L>=1
    rows,end=replay(R,word*L,z,orbit[u]);account['source_engine_calls']+=sum(1+(r['mode']=='K')+(r['mode']=='K' and r['target']!=z) for r in rows)
    assert end==(R,R,orbit[u])
    cc=charts(rows,list(M));pp=packets(rows);crit=[]
    for j in range(L):
        off=j*len(word);neg=next(p for p in pp if p['end']==off+35)
        N=next(p for p in pp if p['end']==off+36);lower=next(p for p in pp if p['end']==off+37)
        assert (neg['H'],neg['Q'],neg['w'])==(2,6,-2) and neg['occurrences']==[off+34,off+35]
        assert cc[off+33]['cold'] and cc[off+33]['recent_before']==[1,3,5,7,9,11]
        assert (N['H'],N['Q'],N['w'],lower['H'],lower['Q'],lower['w'])==(1,2,0,1,2,0)
        rT,rL,rP=rows[off+34],rows[off+35],rows[off+36]
        assert leaf(core(rT['after'][1],set(M)))==leaf(core(rL['after'][1],set(M)))==4
        assert leaf(core(rP['after'][1],set(M)))==3
        for r in (rT,rL,rP):assert labels(core(r['after'][1],set(M)))==set(range(1,12))
        def state(r,c):return {'A':r['after'][0],'BF':r['after'][1],'BE':r['after'][2],
            'M':list(M),'erased':z,'recent':c['recent_after'],'packet_phase':'ready'}
        crit.append({'negative_packet':neg,'entry_prefix':[N],'first_lowering':lower,'entry_class':'E0',
            'prefix_weight':0,'T_state':state(rT,cc[off+34]),'L_state':state(rL,cc[off+35]),
            'post_lowering_state':state(rP,cc[off+36]),'leaf_counts':[4,4,3],
            'actual_absolute_occurrences_after_reaching_prefix':[u*len(word)+off+i for i in (34,35,36,37)]})
    costs={'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows)}
    costs['original_CD_slack']=2*costs['A']-costs['QF']
    assert costs['original_CD_slack']>0
    out('entry_family.json',{'status':'SOURCE_EXACT_E0_ENTRY_REALIZED','initial_full_diagonal':R,
        'base_word':word,'word':word*L,'base_word_length':len(word),'rows':rows,'charts':cc,'packets':pp,
        'erased':z,'auxiliary_preperiod_base_copies':u,'auxiliary_period_base_copies':L,
        'auxiliary_recurrent_start':orbit[u],'reaching_prefix':word*u,
        'critical':crit,'B_repair_word':ret,'B_repair_states':visited,'costs':costs,
        'full_A_BF_BE_recent_closure':True,'source_core_labels':list(range(1,12)),'genuine_KEEP_support':list(M),
        'extra_private_key12_needed':False,'all_gaps':'F0..F11 arbitrary finite ordered BSTs',
        'complete_cheap_return_claimed':False,'width_two_obstruction_claimed':False,**account})
    print(json.dumps({'status':'SOURCE_EXACT_E0_ENTRY_REALIZED','length':len(word)*L,'B_repair':ret,
        'aux_preperiod':u,'aux_period':L,'costs':costs,'critical_occurrences':[34,35,36,37],
        'E0_prefix_weight':0,'leaf_counts':[4,4,3],**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_entry_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
