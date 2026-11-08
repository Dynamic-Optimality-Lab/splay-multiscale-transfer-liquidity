"""New E1 first-loss3->2 source reaches the exact cold-B geometric frontier."""
import collections,json,sys,time
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
def repair(s,R):
    todo=collections.deque([s]);p={s:None}
    while todo:
        t=todo.popleft()
        if t==R:
            w=[]
            while p[t] is not None:t,x=p[t];w.append(x)
            return w[::-1],len(p)
        for x in M:
            if x==t[0]:continue
            n,_,e=step(t,x)
            if any(q['kind']!='DOUBLE' or q['case'] not in ('LL','RR') or q['G'] not in M or q['P'] in M for q in e):continue
            if labels(core(n,set(M)))!=set(range(1,12)) or n in p:continue
            assert len(p)<15000;p[n]=(t,x);todo.append(n)
    raise AssertionError('no bounded source repair')
def main():
    R=vine(11);V=[9,1,3,5,3,1,11,1,3,5,9,11,9,5,3,1]
    word=[('K',x) for x in V[:-1]]+[('D',x) for x in SCAN+[6,1]]+[('K',1)]
    assert len(word)==39
    word += [('K',x) for x in (7,1,3,5,1,11)]
    b=R
    for k,x in word:
        if k=='K':b=step(b,x)[0]
    ret,bstates=repair(b,R);kk=[x for k,x in word if k=='K']
    word += [('D',x) for x in SCAN+kk]+[('K',x) for x in ret]
    e=R;seen={};orbit=[];z=3
    for j in range(65):
        if e in seen:break
        seen[e]=j;orbit.append(e)
        for k,x in word:
            if k=='K' and x!=z:e=step(e,x)[0]
    else:raise AssertionError('BE recurrence beyond65 copies')
    u=seen[e];L=len(orbit)-u;rows,end=replay(R,word*L,z,orbit[u])
    account['source_engine_calls']+=sum(1+(r['mode']=='K')+(r['mode']=='K' and r['target']!=z) for r in rows)
    assert end==(R,R,orbit[u]);cc=charts(rows,list(M));pp=packets(rows);critical=[]
    for j in range(L):
        off=j*len(word);pk=[next(p for p in pp if p['end']==off+i) for i in range(40,46)]
        assert [(p['H'],p['Q'],p['w']) for p in pk]==[(1,4,-2),(1,1,1),(1,2,0),(1,2,0),(1,2,0),(4,4,4)]
        ll=[leaf(core(rows[off+i-1]['after'][1],set(M))) for i in range(40,46)]
        assert ll==[4,3,3,2,2,4]
        assert cc[off+39]['cold'] and cc[off+44]['cold']
        assert rows[off+43]['after'][0][0]==1 and len(rows[off+44]['A_path'])==8
        def state(n):
            r=rows[off+n-1];c=cc[off+n-1]
            return {'A':r['after'][0],'BF':r['after'][1],'BE':r['after'][2],'M':list(M),
                'erased':z,'recent':c['recent_after'],'packet_phase':'ready'}
        critical.append({'negative':pk[0],'before_first_loss_prefix':pk[1:3],'first_lowering':pk[3],
            'zero_suffix_to_geometric_frontier':[pk[4]],'probe':pk[5],
            'T_state':state(40),'entry_state':state(42),'post_first_loss':state(43),'frontier_state':state(44),
            'entry_prefix_weight':1,'remaining_budget':0,'leaf_counts':ll,
            'frontier_not_in_F11':'only cold target11 has A source depth8, so H>=4; no H1 NEG2 outgoing packet'})
    costs={k:sum(r[v] for r in rows) for k,v in [('A','a'),('QF','qF'),('QE','qE')]};costs['CD_slack']=2*costs['A']-costs['QF']
    assert costs['CD_slack']>0
    out('partial_family.json',{'status':'SOURCE_EXACT_E1_POSTLOSS3_TO2_AND_GEOMETRIC_FRONTIER','initial':R,
        'base_word':word,'word':word*L,'rows':rows,'charts':cc,'packets':pp,'critical':critical,
        'erased':z,'auxiliary_preperiod_base_copies':u,'auxiliary_period_base_copies':L,
        'auxiliary_recurrent_start':orbit[u],'reaching_prefix':word*u,'B_repair':ret,'B_repair_states':bstates,
        'costs':costs,'complete_A_BF_BE_recent_closure':True,'full_state_F11_reached':False,
        'only_relaxed_geometric_frontier_reached':True,'genuine_support':list(M),**account})
    print(json.dumps({'status':'SOURCE_EXACT_E1_POSTLOSS3_TO2_AND_GEOMETRIC_FRONTIER','period':len(word)*L,
        'B_repair':ret,'preperiod':u,'aux_period':L,'critical_occurrences':list(range(40,46)),
        'leaf_counts':[4,3,3,2,2,4],'costs':costs,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_partial_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
