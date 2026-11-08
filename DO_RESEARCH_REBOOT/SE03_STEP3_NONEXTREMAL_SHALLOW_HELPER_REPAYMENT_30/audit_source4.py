"""High-value three-query test of the next, first-root-return packet rule.
The paired-closed embedding is a source-word theorem, not an unrun replay.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=min(3,int(sys.argv[2]))
sp=importlib.util.spec_from_file_location('C30_first_return_source',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
def path(t,x):
    if C.queries>=QCAP:raise TimeoutError('three-query first-return control')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t
def main():
    r=json.loads((B/'nonextremal_source_countercertificate.json').read_text());comb=next(z for z in r['rows'] if z['occurrence']==119)
    new,end=C.replay(*fr(comb['after']),[('K',7)]);new[0]['occurrence']=120;z=new[0]
    assert z['a']==z['qF']==1 and all(e['case'] in ('LL','RR') for e in z['BF_events'])
    _,ch=C.L.marked_tree(fr(z['before'][1]),C.M);_,nc=C.L.marked_tree(fr(z['after'][1]),C.M);E=lambda cc:sum(max(len(v)-2,0) for v in cc.values())
    sigma=2-z['qF']+E(nc)-E(ch);assert sigma==0 and E(ch)==1 and E(nc)==0
    prefix_rows=r['prefix_rows']+r['rows'][:34]+new;word=r['reaching_prefix']+r['period'][:34]+[['K',7]];undo=[];receipts=[]
    for row in reversed(prefix_rows):
        if row['mode']!='K':continue
        pa=row['BF_path'];t=fr(row['before'][1]);anc=[C.p.at(t,pa[:i])[0] for i in range(0,len(pa),2)];inv=C.inverse(anc)
        assert len(inv)==2**len(anc)-1;undo += [('K',x) for x in inv];receipts.append({'old_occurrence':row['occurrence'],'root_first_ancestors':anc,'inverse_targets':inv})
    W=word+undo+[('D',x) for x in range(13,0,-1)]+[('D',3)]
    out('first_root_return_countercertificate.json',{'status':'EXACT_REACHABLE_PREFIX_PLUS_SYMBOLIC_A_FULL_B_CLOSED_EMBEDDING',
        'new_occurrence':z,'old_prefix_through119_reused':True,'counter_interval':[118,120],'counter_targets':[11,5,7],
        'Q':[2,3,1],'H':[1,1,1],'sigma_E':[-1,0,0],'first_return_target':7,'sum_sigma_E':-1,
        'original_diagonal_tree':r['original_diagonal_tree'],'exact_returning_word':W,'return_word_length':len(W),'inverse_receipts':receipts,
        'paired_start_end_A_B':[r['initial'][0],r['original_diagonal_tree']],
        'reaching_prefix':'the SAME exact_returning_word, from the stated common diagonal; verified original prefix then source inverse theorem and ordered reset proof',
        'erased_initial_tree':None,'erased_recurrence':'finite deterministic recurrence exists; no numerical u,L or normalized receipt is claimed',
        'closure_verification':'symbolic source inverse and ordered reset proof; full W NOT replayed',
        'refuted_candidate':'Every -1 helper is repaid by first subsequent genuine KEEP of its old full-B root',
        'main_NH30_refuted':False,'source_queries':C.queries})
    print(json.dumps({'status':'FIRST_ROOT_RETURN_LOCAL_COUNTER','queries':C.queries,'sum_sigma_E':-1,'embedding_word_length':len(W),'whole_embedding_not_replayed':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source4_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
