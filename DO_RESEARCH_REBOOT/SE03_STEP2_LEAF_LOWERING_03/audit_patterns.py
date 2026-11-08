"""Bounded actual-source construction of two leaf losses and zero restoration."""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import N,trace,core,labels,vine,replay,packets,charts,SCAN
M=(1,3,5,7,9,11);started=time.process_time();CAP=min(35,float(sys.argv[1])-3)
account={'source_engine_calls':0,'new_finite_tests':0};queries={'B_states':[],'A_states':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def limit():
    assert time.process_time()-started<CAP,'CPU discovery bound'
    assert account['source_engine_calls']<600000,'source replay bound'
@functools.lru_cache(maxsize=100000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:limit()
    return trace(t,x)
def legal(t,x):
    z,p,e=move(t,x)
    ok=all(q['kind']=='DOUBLE' and q['case'] in ('LL','RR') and q['G'] in M and q['P'] not in M for q in e)
    return z if ok and labels(core(z,set(M)))==set(range(1,12)) else None
def word_to(start,end):
    todo=collections.deque([start]);parent={start:None}
    while todo:
        limit();s=todo.popleft()
        if s==end:
            result=[]
            while parent[s] is not None:s,x=parent[s];result.append(x)
            queries['B_states'].append(len(parent));return result[::-1]
        for x in M:
            if x==s[0]:continue
            z=legal(s,x)
            if z is None or z in parent:continue
            assert len(parent)<15000,'B-state construction bound'
            parent[z]=(s,x);todo.append(z)
    raise AssertionError('no endpoint construction in legal source family')
def leaf(t):
    if t is None:return 0
    if t[1] is None and t[2] is None:return int(t[0] in M)
    return leaf(t[1])+leaf(t[2])
def prep_ok(a):
    if a[0]!=3:return False
    for x in (5,7,3):
        a,p,e=move(a,x)
        if len(e)!=1:return False
    return True
def preparation(start):
    # Exact DELETE words; the terminal genuine K3 is kept separately.
    todo=collections.deque([start]);parent={start:None}
    while todo:
        limit();s=todo.popleft()
        if prep_ok(s):
            result=[]
            while parent[s] is not None:s,x=parent[s];result.append(x)
            queries['A_states']=len(parent);return result[::-1]
        for x in (3,5,7,9,1,11,2,4,6,8,10):
            z=move(s,x)[0]
            if z in parent:continue
            assert len(parent)<10000,'A preparation bound'
            parent[z]=(s,x);todo.append(z)
    raise AssertionError('no one-event source preparation')
def main():
    F=['F'+str(i) for i in range(12)]
    S=N(3,N(2,N(1,F[0],F[1]),F[2]),N(4,F[3],N(9,N(6,N(5,F[4],F[5]),N(8,N(7,F[6],F[7]),F[8])),N(10,F[9],N(11,F[10],F[11])))))
    R=vine(11);reach=word_to(R,S);assert reach[-1]==3
    sequence=[5,7,3];b=S;pattern=[]
    for x in sequence:
        old=b;b,p,e=move(b,x)
        assert legal(old,x)==b and len(e)==2
        pattern.append({'target':x,'BF_before':old,'BF_after':b,'path':p,'leaf_before':leaf(core(old,set(M))),
            'leaf_after':leaf(core(b,set(M))),'q':2})
    assert [(r['leaf_before'],r['leaf_after']) for r in pattern]==[(4,3),(3,2),(2,3)]
    prep=preparation(R);ret=word_to(b,R)
    warm=[3,5,7,9,11,9,7,5,3,1]
    w=[('K',x) for x in warm+reach[:-1]]+[('D',x) for x in SCAN+prep]+[('K',3)]
    first=len(w)+1;w += [('K',x) for x in sequence]
    # Align A with the ACTUAL current BF by a deterministic replay from R11.
    w += [('D',x) for x in SCAN+reach+sequence]
    w += [('K',x) for x in ret]
    # Obtain the real erased recurrent period; no projected states spliced.
    z=11;be=R;seen={};orbit=[]
    for j in range(65):
        if be in seen:break
        seen[be]=j;orbit.append(be)
        for k,x in w:
            if k=='K' and x!=z:be=move(be,x)[0]
    else:raise AssertionError('erased recurrence exceeded declared65 states')
    u=seen[be];period=len(orbit)-u;assert period>=1
    fullword=w*period;rows,end=replay(R,fullword,z,orbit[u])
    account['source_engine_calls']+=sum(1+(r['mode']=='K')+(r['mode']=='K' and r['target']!=z) for r in rows)
    limit();assert end==(R,R,orbit[u])
    cc=charts(rows,list(M));ps=packets(rows);selected=[]
    for j in range(period):
        for off,p in enumerate(pattern):
            occ=j*len(w)+first+off;r=rows[occ-1]
            pk=next(q for q in ps if q['end']==occ)
            assert (r['a'],r['qF'],pk['H'],pk['Q'],pk['w'])==(1,2,1,2,0)
            selected.append({'occurrence':occ,'H':1,'Q':2,'w':0,'leaf_before':p['leaf_before'],
                'leaf_after':p['leaf_after'],'A_path':r['A_path'],'BF_path':r['BF_path'],
                'before':r['before'],'after':r['after'],'recent_before':cc[occ-1]['recent_before'],
                'recent_after':cc[occ-1]['recent_after']})
    out('pattern_family.json',{'status':'ACTUAL_CLOSED_TWO_LOSSES_AND_ZERO_RESTORATION',
        'initial_full_diagonal':R,'full_core_source':S,'B_reaching_word':reach,'A_preparation':prep,'B_return_word':ret,
        'base_word':w,'word':fullword,'base_word_length':len(w),'rows':rows,'charts':cc,'packets':ps,
        'erased':z,'auxiliary_preperiod_base_copies':u,'auxiliary_period_base_copies':period,
        'auxiliary_recurrent_start':orbit[u],'pattern':selected,
        'costs':{'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),
            'original_CD_slack':2*sum(r['a'] for r in rows)-sum(r['qF'] for r in rows)},
        'full_A_B_BE_recent_closure':True,'genuine_support':list(M),'free_gaps':'arbitrary finite ordered Fi; no gap interior requested',
        'T_to_F_return_claimed':False,'local_counterclaim':'two consecutive leaf-lowering H1Q2 zero packets CAN occur; zero restoration CAN follow',
        'finite_construction_search_limits':{'CPU':CAP,'B_states_per_BFS':15000,'A_states':10000,'splay_calls':600000},
        'queries':queries,**account})
    print(json.dumps({'status':'ACTUAL_CLOSED_TWO_LOSSES_AND_ZERO_RESTORATION','reach':reach,'prep':prep,'return':ret,
        'pattern_occurrences':[r['occurrence'] for r in selected],'leaf_counts':[4,3,2,3],
        'length':len(fullword),'aux_preperiod':u,'aux_period':period,'queries':queries,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_patterns_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
