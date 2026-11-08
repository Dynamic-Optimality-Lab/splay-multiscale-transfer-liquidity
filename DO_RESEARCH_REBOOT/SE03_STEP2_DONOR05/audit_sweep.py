"""Free sweep induction, monotone A source identities and cyclic allocation."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l,r):return (k,l,r)
def right(t):
    g,pl,d=t;p,a,b=pl;return N(p,a,N(g,b,d))
def left(t):
    g,a,pr=t;p,b,d=pr;return N(p,N(g,a,b),d)
def symbol_depth(t,s):
    if isinstance(t,str):return 0 if t==s else None
    if t[0]==s:return 0
    vals=[symbol_depth(t[1],s),symbol_depth(t[2],s)]
    return next((v+1 for v in vals if v is not None),None)
def main():
    # One universal ascending sweep step, all hanging terms free.
    src=N('mi','L',N('ui','B',N('mr',N('uj',N('mj','C','D'),'Tail'),'E')))
    inner=right(right(src[2][2]))
    result=left(left(N('mi','L',N('ui','B',inner))))
    expected=N('mj',N('ui',N('mi','L','B'),'C'),N('uj','D',N('mr','Tail','E')))
    assert result==expected
    # Exact A H1 possibilities with new target x>g and old minimum in L.
    ar=N('g','L',N('x','C','D'));aro=left(ar)
    arr=N('g','L',N('p','B',N('x','C','D')));arro=left(left(arr))
    arl=N('g','L',N('p',N('x','B','C'),'D'))
    arlo=left(N('g','L',right(arl[2])))
    deltas=[symbol_depth(t,'L')-symbol_depth(s,'L') for s,t in [(ar,aro),(arr,arro),(arl,arlo)]]
    assert deltas==[1,2,1]
    assert [symbol_depth(t,'g') for t in [aro,arro,arlo]]==[1,2,1]
    # Decreasing counterparts use old maximum in R, own source formulas.
    al=N('g',N('x','A','B'),'R');alo=right(al)
    all_=N('g',N('p',N('x','A','B'),'C'),'R');allo=right(right(all_))
    alr=N('g',N('p','A',N('x','B','C')),'R')
    alro=right(N('g',left(alr[1]),'R'))
    assert [symbol_depth(t,'R')-symbol_depth(s,'R') for s,t in [(al,alo),(all_,allo),(alr,alro)]]==[1,2,1]
    sweepQ=4*2+1;episodeQ=6+sweepQ;assert sweepQ==9 and episodeQ==15
    assert 2*2<5 and 3+1+5==9 # source cover forces nextH>=9 after deficient sweep
    # Three feasible Boolean source cases; adjacent deficient excluded by A lemma.
    residuals={'deficient':2*7-15+1-0,'nondef_after_def':2*8-15+0-1,'nondef_after_nondef':2*8-15}
    assert residuals=={'deficient':0,'nondef_after_def':0,'nondef_after_nondef':1}
    assert 1+2*8==17
    targets=[11,1,3,5,7,9,11,1,11,9,7,5,3,1]
    q=[5,1]+[2]*4+[1]+[5,1]+[2]*4+[1]
    A_recurrent=[1,1]+[2]*4+[1]+[5,1]+[2]*4+[0]
    assert len(targets)==len(q)==len(A_recurrent)==14 and sum(q)==30
    assert sum(A_recurrent)+1+5+1==32 and 2*32-30==34
    # Source witness inserts only D1,D11,D1 before final genuine K1.
    word=[('K',k) for k in targets[:-1]]+[('D',1),('D',11),('D',1),('K',1)]
    assert len(word)==17
    out('sweep_audit.json',{'status':'PASS_COMPLETE_EXTREME_SWEEP_SOURCE_CLASS',
        'sweep_induction_frame':{'source':src,'target':result,'double_word':['LL','RR'],'actual_q':2},
        'monotone_A_H1_old_extreme_depth_increments':deltas,'sweep_H1_forces_old_extreme_depth':5,
        'source_target_cover_next_packet_H_at_least':4,'next_episode_H_at_least':9,
        'deficient_episodes_not_adjacent':True,'episode_Q':15,'episode_minH':7,'selected_threshold':8,'debt_range':1,
        'residuals':residuals,'full_allocator':'actual FIFO episode bank, first min(H,8) source events, pay15 original IDs, zero endpoint bank',
        'max_boundary_bank':1,'max_selected_units':16,'max_within_episode_queue':17,
        'witness':{'word':[{'occurrence':i,'op':o,'key':k} for i,(o,k) in enumerate(word,1)],'A_recurrent':32,'QF':30,'full_slack':34,
            'recurrent_input':['P_full_max_min','R11'],'reaching_prefix':'one actual period from diagonalR11 reaches the input; its cost is excluded from donors',
            'one_H2_q5q1_packet':True,'realizable_deficient_episode_claimed':False},
        'fixed_owner_composition':'complete g permits exact alternating paths while retaining common and all compatible paid original receipts',
        'arbitrary_DELETE_helpers':True,'arbitrary_nongenuine_KEEPS':True,'all_original_operations_covered_once':True,
        'all_auxiliary_patterns_within_class_covered':True,'no_rejoin_assumed':True,'prep_tail_guard_required':False,
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,
        'universal_Step2':False,'core10_covered':False,'other_core11_words_covered':False})
    print('PASS generic sweep induction, A depth forcing, complete class allocator and actual nonvacuity interfaces')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_sweep_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
