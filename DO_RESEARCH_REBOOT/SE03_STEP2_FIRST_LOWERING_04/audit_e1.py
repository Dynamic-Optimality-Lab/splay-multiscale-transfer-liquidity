"""Original closed E1 entry with singleton cold NEG2 and one +1 intervention."""
import json,sys,time,collections
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import trace,vine,core,labels,replay,packets,charts,SCAN
M=(1,3,5,7,9,11);account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def step(t,x):
    account['source_engine_calls']+=1;return trace(t,x)
def leaf(t):return 0 if t is None else int(t[0] in M) if t[1] is None and t[2] is None else leaf(t[1])+leaf(t[2])
def breturn(s,R):
    todo=collections.deque([s]);p={s:None}
    while todo:
        t=todo.popleft()
        if t==R:
            w=[]
            while p[t] is not None:t,x=p[t];w.append(x)
            return w[::-1],len(p)
        for x in M:
            if x==t[0]:continue
            n,_,ev=step(t,x)
            if not all(q['kind']=='DOUBLE' and q['case'] in ('LL','RR') and q['G'] in M and q['P'] not in M for q in ev):continue
            if labels(core(n,set(M)))!=set(range(1,12)) or n in p:continue
            assert len(p)<15000;p[n]=(t,x);todo.append(n)
    raise AssertionError('no bounded B source repair')
def main():
    R=vine(11);prep=json.loads((B/'e1_preparation.json').read_text())['candidate']['preparation']
    warm=[9,1,3,5,3,1,11,1,3,5,9,11,9,5,3,1]
    w=[('K',x) for x in warm[:-1]]+[('D',x) for x in SCAN+prep]+[('K',1),('K',7),('K',9),('K',1)]
    negend=15+21+len(prep)+2;posend=negend+1;lowend=negend+2
    b=R
    for k,x in w:
        if k=='K':b=step(b,x)[0]
    ret,bstates=breturn(b,R);keep=[x for k,x in w if k=='K']
    w += [('D',x) for x in SCAN+keep]+[('K',x) for x in ret]
    z=3;e=R;seen={};orbit=[]
    for j in range(65):
        if e in seen:break
        seen[e]=j;orbit.append(e)
        for k,x in w:
            if k=='K' and x!=z:e=step(e,x)[0]
    else:raise AssertionError('BE recurrence beyond65 states')
    u=seen[e];L=len(orbit)-u
    rows,end=replay(R,w*L,z,orbit[u]);account['source_engine_calls']+=sum(1+(r['mode']=='K')+(r['mode']=='K' and r['target']!=z) for r in rows)
    assert end==(R,R,orbit[u]);cc=charts(rows,list(M));pp=packets(rows);crit=[]
    for j in range(L):
        off=j*len(w);neg=next(p for p in pp if p['end']==off+negend)
        pos=next(p for p in pp if p['end']==off+posend);low=next(p for p in pp if p['end']==off+lowend)
        assert (neg['H'],neg['Q'],neg['w'])==(1,4,-2) and cc[off+negend-1]['cold']
        assert (pos['H'],pos['Q'],pos['w'],low['H'],low['Q'],low['w'])==(1,1,1,1,2,0)
        rT,rL,rP=[rows[off+k-1] for k in (negend,posend,lowend)]
        ll=[leaf(core(r['after'][1],set(M))) for r in (rT,rL,rP)];assert ll==[4,4,3]
        def state(r,c):return {'A':r['after'][0],'BF':r['after'][1],'BE':r['after'][2],
            'M':list(M),'erased':z,'recent':c['recent_after'],'packet_phase':'ready'}
        crit.append({'negative_packet':neg,'entry_prefix':[pos],'first_lowering':low,'entry_class':'E1',
            'prefix_weight':1,'T_state':state(rT,cc[off+negend-1]),'L_state':state(rL,cc[off+posend-1]),
            'post_lowering_state':state(rP,cc[off+lowend-1]),'leaf_counts':ll,
            'actual_absolute_occurrences_after_reaching_prefix':[u*len(w)+off+k for k in (negend,posend,lowend)]})
    costs={k:sum(r[v] for r in rows) for k,v in [('A','a'),('QF','qF'),('QE','qE')]};costs['original_CD_slack']=2*costs['A']-costs['QF']
    assert costs['original_CD_slack']>0
    out('e1_family.json',{'status':'SOURCE_EXACT_E1_ENTRY_REALIZED','initial_full_diagonal':R,
        'base_word':w,'word':w*L,'base_word_length':len(w),'rows':rows,'charts':cc,'packets':pp,
        'erased':z,'auxiliary_preperiod_base_copies':u,'auxiliary_period_base_copies':L,
        'auxiliary_recurrent_start':orbit[u],'reaching_prefix':w*u,'critical':crit,'B_repair_word':ret,
        'B_repair_states':bstates,'costs':costs,'full_A_BF_BE_recent_closure':True,
        'genuine_KEEP_support':list(M),'source_core_labels':list(range(1,12)),
        'all_gaps':'F0..F11 arbitrary finite ordered BSTs','complete_cheap_return_claimed':False,
        'width_two_obstruction_claimed':False,**account})
    print(json.dumps({'status':'SOURCE_EXACT_E1_ENTRY_REALIZED','prep':prep,'length':len(w)*L,
        'critical_occurrences':[negend,posend,lowend],'B_repair':ret,'aux_preperiod':u,'aux_period':L,
        'costs':costs,'leaf_counts':[4,4,3],**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_e1_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
