"""Distinct mutable source replay and universal burst-certificate check.
No producer kernel or raw allocator is imported. Existing rotation class
is reused with a generic ordered-gap dumper and a cumulative charge hook.
"""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    proof=json.loads((B/'Gamma55_original_source.json').read_text());r=55;n=109
    s=importlib.util.spec_from_file_location('separate_mutable33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
    I=importlib.util.module_from_spec(s);s.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>=CAP-2:raise TimeoutError('independent cap')
        queries+=1
    I.tick=tick
    word=[]
    for x in range(3,110,2):word.append(('K',x))
    for x in range(107,2,-2):word.append(('K',x))
    word.extend([('D',109),('D',1),('K',1),('K',109),('D',2),('D',109),('K',1)])
    for x in range(3,110,2):word.append(('K',x))
    for x in range(107,0,-2):word.append(('K',x))
    assert word==list(map(tuple,proof['word'])) and len(word)==222
    initial='F109'
    for x in range(109,0,-1):initial=(x,'F'+str(x-1),initial)
    assert initial==fr(proof['initial_diagonal'])
    tt=[I.Tree(initial) for _ in range(3)]
    def dump(tree):
        def go(v,lo,hi):return 'F'+str(lo) if v is None else (v.key,go(v.left,lo,v.key),go(v.right,v.key,hi))
        return go(tree.root,0,110)
    previous=None;rows=[];states=[]
    for copy in range(2):
        start=tuple(dump(t) for t in tt)
        for j,(mode,x) in enumerate(word,1):
            before=tuple(dump(t) for t in tt);pa,ea=tt[0].access(x);pb=pe='';eb=ee=[]
            if mode=='K':pb,eb=tt[1].access(x)
            if mode=='K' and x!=3:pe,ee=tt[2].access(x)
            if copy:
                row={'occurrence':222+j,'local':j,'mode':mode,'target':x,'a':len(ea),'qF':sum(e['kind']=='DOUBLE' for e in eb),'qE':sum(e['kind']=='DOUBLE' for e in ee),
                     'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ee,'genuine_F':mode=='K' and before[1][0]!=x,'genuine_E':mode=='K' and x!=3 and before[2][0]!=x}
                assert row==proof['rows'][j-1],j;rows.append(row)
                if row['occurrence']==proof['critical']['occurrence']:
                    assert before==fr(proof['critical']['before']) and tuple(dump(t) for t in tt)==fr(proof['critical']['after'])
        end=tuple(dump(t) for t in tt);assert end[:2]==(initial,initial)
        if copy:assert end==start==previous==fr(proof['period_initial'])==fr(proof['period_final'])
        previous=end
    U={(v['occurrence'],j,b) for v in rows for j in range(1,v['a']+1) for b in (0,1)}
    F={(v['occurrence'],j) for v in rows for j in range(1,v['qF']+1)};E={(v['occurrence'],j) for v in rows for j in range(1,v['qE']+1)}
    assert U==set(map(tuple,proof['U'])) and F==set(map(tuple,proof['DF'])) and E==set(map(tuple,proof['DE']))
    assert {v['target'] for v in rows if v['genuine_F']}==set(range(1,110,2))
    assert {v['target'] for v in rows if v['genuine_E']}==set(range(1,110,2))-{3}
    assert (len(U),len(F),len(E))==(656,324,318) and len(U)-len(F)==332
    crit=next(v for v in rows if v['occurrence']==333)
    assert crit['target']==109 and crit['a']==1 and crit['qF']==54 and crit['qE']==53
    # Every input count map is complete/injective using ONE original period.
    profiles={}
    for name,D,qfield in [('H_count',F,'qF'),('fE_count',E,'qE')]:
        mp={tuple(v['demand']):tuple(v['unit']) for v in proof[name]}
        assert set(mp)==D and len(set(mp.values()))==len(mp) and set(mp.values())<=U
        assert all(223<=t<=444 for t,_,_ in mp.values())
        timeline=[]
        for v in rows:
            timeline.extend(('U',v['occurrence'],j,b) for j in range(1,v['a']+1) for b in (0,1))
            timeline.extend(('D',v['occurrence'],j) for j in range(1,v[qfield]+1))
        ranks={v:i for i,v in enumerate(timeline)};delta=[0]*(len(timeline)+1)
        for d,u in mp.items():
            a,b=sorted((ranks[('D',)+d],ranks[('U',)+u]));delta[a]+=1;delta[b]-=1
        cur=peak=0
        for d in delta:cur+=d;peak=max(peak,cur)
        assert cur==0;profiles[name]=peak
    # Universal certificate: if both endpoint banks were<=25, at most50
    # outside donors could fund the burst. But at least52/51 are required.
    assert 54-2==52>2*25 and 53-2==51>2*25
    assert (52+1)//2==26 and (51+1)//2==26
    result={'status':'PASS_GAMMA55_SOURCE_AND_ALL_MATCHING_ENDPOINT_OBSTRUCTION','original_A_full_erased_closure':True,
        'period':[223,444],'support':55,'erased_support':54,'critical':{'occurrence':333,'target':109,'a':1,'qF':54,'qE':53},
        'counts':{'A':328,'QF':324,'QE':318,'U':656,'scalar_slack':332},'raw_count_map_profiles':profiles,
        'all_full_matchings_endpoint_peak_lower_bound':26,'all_common_owner_injections_endpoint_peak_lower_bound':26,
        'original_GateU14_working_bank_refuted':False,'normalized_owner_receipt_invented':False,
        'source_queries':queries,'trust':'separate source implementation operated by same agent; algebraic all-matching proof; no external/formal verification',
        'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'Gamma55_original_source.json',B/'ENDPOINT_BURST_THEOREM.md']}}
    out('endpoint_obstruction_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
