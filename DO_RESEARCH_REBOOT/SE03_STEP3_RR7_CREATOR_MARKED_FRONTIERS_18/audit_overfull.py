"""Bounded original A-source construction for a LOW-creator obstruction.
This is candidate falsification, not finite evidence for universal signs.
"""
import collections,json,time
import audit_rr7_source as S
import audit_marked as W
B=S.B;p=S.p
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def goal(t):
    return isinstance(t,tuple) and t[0]==3 and p.node(t[2]) and t[2][0]==4 and p.node(t[2][2]) and t[2][2][0]==13 and p.node(t[2][2][1]) and t[2][2][1][0]==5
def main():
    old=json.loads((B/'rr7_source_candidate.json').read_text());R=p.vine(13)
    starts=[('D',12),('D',5),('D',4),('D',3)];initial=R
    for _,x in starts:initial=S.tr(initial,x)[0]
    parents={initial:None};q=collections.deque([initial]);answer=None;start=time.process_time()
    while q and S.calls<150000 and time.process_time()-start<1.0:
        t=q.popleft()
        if goal(t):answer=t;break
        for x in (3,4,5,6,12,13):
            if x==t[0]:continue
            z=S.tr(t,x)[0]
            if z not in parents:parents[z]=(t,x);q.append(z)
    if answer is None:
        out('overfull_source_result.json',{'status':'NO_SOURCE_PREPARATION_FOUND_IN_BOUNDED_CONSTRUCTION_NOT_UNIVERSAL_RESULT',
            'states':len(parents),'source_engine_calls':S.calls});print('NO_COMPLETED_SOURCE_COUNTERCERTIFICATE',flush=True);return
    path=[];t=answer
    while parents[t] is not None:t,x=parents[t];path.append(('D',x))
    prep=starts+path[::-1]
    # The old period's first9 operations are preparation,K3,D5,D13,K13,K5.
    word=prep+[('K',3),('K',13),('K',5)]+[tuple(z) for z in old['word'][9:]]
    initB=S.freeze(old['initial_BF']);rows,end=S.replay(R,initB,word)
    assert end==(R,initB)
    n=len(prep);producer=rows[n+1];frontier=rows[n+2]
    assert producer['target']==13 and producer['a']==1 and producer['qF']==2
    assert frontier['target']==5 and frontier['a']==1 and frontier['qF']==2
    v=S.L.build(rows,S.M);profile=W.analyze('new_LOW_H1_m2',rows)
    claim=next(c for c in profile['claims'] if c['frontier'][0]==frontier['occurrence'])
    creator_t=claim['creator']['source_occurrence'];m=next(m for m in v['macros'] if creator_t in m['occurrences'])
    assert m['H']==1 and m['Q']==2 and len(m['branch'])==2 and m['z']==1
    assert creator_t==producer['occurrence'] and not claim['protected']
    out('overfull_source_result.json',{'status':'ACTUAL_CLOSED_SOURCE_LOCAL_TAIL_RULE_REFUTED_DERIVATION_AUDIT_PENDING',
        'common_initial':R,'reaching_prefix':old['reaching_prefix'],'initial_A':R,'initial_BF':initB,
        'preparation':prep,'word':word,'rows':rows,'A_BF_closed':True,
        'source_full_support':sorted(S.M),'source_full_core':13,
        'producer':m,'frontier':(frontier['occurrence'],2),'watched_claim':claim,
        'producer_comparison_tail_count':0,'source_claim_count_lower_bound':1,
        'no_erased_owner_qualification_claimed_for_this_extra_source':True,
        'not_a_main_escape_or_CD_counterexample':True,'source_engine_calls':S.calls})
    print(json.dumps({'status':'LOW_H1_m2_LOCAL_TAIL_COUNTERSOURCE_FOUND','prep':prep,
        'producer':producer['occurrence'],'frontier':frontier['occurrence'],
        'watched_seed':claim['creator']['unit'],'comparison_preimage':claim['comparison_preimage'],
        'source_engine_calls':S.calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_overfull_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':S.calls,'new_finite_tests':0,'old_semantic_rows_replayed':0})
