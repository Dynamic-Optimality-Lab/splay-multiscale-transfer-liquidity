"""One precise PREFIX witness. New preparation occurs BEFORE the synchronizing
KEEP13, so the critical j macro remains H1. Old original prefix facts reused.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2])
sp=importlib.util.spec_from_file_location('FR31_source_engine',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
def path(t,x):
    if C.queries>=QCAP:raise TimeoutError('FR31 source query cap')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t
def main():
    old=json.loads((P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json').read_text())
    row=next(z for z in old['rows'] if z['occurrence']==116);start=fr(row['before'])
    word=[('D',x) for x in (11,7,9,11,7,13)]+[('K',x) for x in (13,7,11,5,11,9,7,11)]
    rows,end=C.replay(*start,word)
    for z in rows:z['occurrence']+=115
    tags=dict(zip(('prep','j','helper','comb','upper11','activate9','return7','recovery11'),range(122,130)))
    ledger=[]
    for name in ('j','helper','comb','upper11','activate9','return7','recovery11'):
        z=next(z for z in rows if z['occurrence']==tags[name]);x=z['target'];pa,ch=C.L.marked_tree(z['before'][1],C.M);_,nc=C.L.marked_tree(z['after'][1],C.M);anc=[];v=pa[x]
        while v is not None:anc.append(v);v=pa[v]
        E=lambda cc:sum(max(len(v)-2,0) for v in cc.values());beta=sum(len(ch[v])>=2 for v in anc);k3=sum(len(ch[v])>=3 for v in anc);leaf=int(not ch[x]);c=min(z['a'],3)
        assert z['a']==1
        ledger.append({'name':name,'occurrence':z['occurrence'],'target':x,'H':z['a'],'QF':z['qF'],'QE':z['qE'],'beta':beta,'z':leaf,'k3':k3,
            'rho':2*c-beta-leaf,'E_before':E(ch),'E_after':E(nc),'sigma_E':2*c-z['qF']+E(nc)-E(ch),
            'A_path':z['A_path'],'BF_path':z['BF_path'],'marked_before':ch,'marked_after':nc})
    assert [z['QF'] for z in ledger]==[2,2,3,1,3,1,2]
    assert [z['sigma_E'] for z in ledger]==[0,-1,0,0,0,0,1]
    assert all(C.p.labels(C.p.core(z['before'][1],C.M))==set(range(1,14)) and C.p.labels(C.p.core(z['after'][1],C.M))==set(range(1,14)) for z in rows)
    assert all(e['case'] in ('LL','RR') and e['G'] in C.M and e['P'] not in C.M for z in rows for e in z['BF_events'])
    assert sum(z['sigma_E'] for z in ledger[1:6])==-1 and sum(z['sigma_E'] for z in ledger[1:])==0
    # Complete concrete word of95 original operations, using the source-
    # exact root-first SS inverse. Its closure is a symbolic theorem;
    # the inverse A/E trajectories have NOT been replayed in this phase.
    prefix_rows=old['rows'][:30]+rows;prefix_word=old['period'][:30]+word;undo=[];inverse=[]
    for z in reversed(prefix_rows):
        if z['mode']!='K':continue
        pa=z['BF_path'];bt=fr(z['before'][1]);anc=[C.p.at(bt,pa[:i])[0] for i in range(0,len(pa),2)];targets=C.inverse(anc)
        assert len(targets)==2**len(anc)-1
        undo += [('K',x) for x in targets];inverse.append({'prefix_occurrence':z['occurrence']-85,'old_root_first_ancestors':anc,'q':len(anc),'targets':targets})
    reset=[('D',x) for x in range(13,0,-1)]+[('D',3)];W=prefix_word+undo+reset
    assert len(prefix_word)==44 and len(undo)==37 and len(W)==95
    assert max(z['q'] for z in inverse)==3 and sum(z['q']==3 for z in inverse)==2
    data={'status':'EXACT_REACHABLE_PREFIX_COUNTER_WITH_SYMBOLIC_CLOSED_COMPLETION_PENDING_AUDIT',
        'source_scope':'FR31-PREFIX; deeper A subtree varies; FR31-FIX not refuted',
        'original_diagonal_tree':old['original_diagonal_tree'],'accepted_reaching_word':old['reaching_prefix'],
        'cached_prefix_word':old['period'][:30],'cached_prefix_rows':old['rows'][:30],'start_after115':start,'new_word':word,'new_rows':rows,'tags':tags,'ledger':ledger,
        'first_upper':126,'first_return':128,'helper':124,'low_phase':[],'D_entry':1,'R_return':0,'sum_helper_through_first_return':-1,
        'later_recovery':129,'sum_helper_through_recovery':0,'preparation_placed_before_keep13':True,'original_A_StepEv_ids_retained':True,
        'period_word_W':W,'prefix_P':prefix_word,'inverse_receipts':inverse,'final_A_reset':reset,'W_length':95,
        'A_start_end':old['initial'][0],'BF_start_end':old['original_diagonal_tree'],'erased_seed_E0':old['initial'][2],
        'closed_history_encoding':{'C':742900,'M':'factorial(742900)','source_reaching_prefix':'accepted85-word N, followed by W^C',
            'source_period':'W^M','initial_A':'A_start_end','initial_BF':'BF_start_end','initial_BE':'F_E^C(erased_seed_E0)',
            'F_E':'ordinary bottom-up B execution of W retaining exactly KEEPs other than11',
            'closure_proof':'SS inverse restores BF; ordered A reset restores A; finite13-anchor BST functional orbit has <=Catalan13=C states, and its eventual period divides C!'},
        'whole_closed_history_replayed':False,'all_actual_A_B_BE_new_rows_replayed':True,'old_source_owners_modified':False,
        'claim_refuted':'source-uniform FR31-PREFIX sum sigma_E from helper through first genuine KEEP7 is nonnegative',
        'not_refuted':['FR31-FIX','Coarse-Double','Universal CD','Dynamic Optimality']}
    out('prefix_first_return_countercertificate.json',data)
    print(json.dumps({'status':'FR31_PREFIX_COUNTER_CONSTRUCTED','queries':C.queries,'first_return_sigma':-1,'later_recovery_sigma':0,'W_length':95,
        'ledger':[{k:z[k] for k in ('name','occurrence','target','H','QF','sigma_E')} for z in ledger]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
