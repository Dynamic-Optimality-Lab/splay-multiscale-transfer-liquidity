"""Fresh mutable original-source audit of max-contraction counterword."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def node(t):return isinstance(t,tuple)
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def renumber(t):
    def walk(v,hi):return 'F'+str(hi) if not node(v) else (v[0]//2,walk(v[1],v[0]//2-1),walk(v[2],hi))
    return walk(t,10)
def delete(t,z):
    if not node(t):return (t,)
    k,L,R=t
    if k!=z:return tuple((k,l,r) for l in delete(L,z) for r in delete(R,z))
    if not node(L):return (R,)
    if not node(R):return (L,)
    # Promote either child, delete z recursively in its remaining child.
    a,LL,LR=L;b,RL,RR=R
    left=[(a,LL,v) for v in delete((z,LR,R),z)];right=[(b,v,RR) for v in delete((z,L,RL),z)];return tuple(dict.fromkeys(left+right))
def main():
    global queries
    z=json.loads((B/'interior_max_contraction_closed_source.json').read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in z['input_sha256'].items());basis=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,basis['trees']));idx={t:i for i,t in enumerate(T)};N=len(T);mirror=basis['mirror'];export=json.loads((B/'native10_credit_certificate.json').read_text());level=dict(export['nonzero_debt']);debt=lambda a,b:level.get(min(a*N+b,mirror[a]*N+mirror[b]),0)
    candidate=z['candidate'];private=candidate['private_key'];before=fr(candidate['source_A']);after=fr(candidate['actual_A_target']);ps=tuple(sorted({idx[renumber(t)] for t in delete(before,private)}));pt=tuple(sorted({idx[renumber(t)] for t in delete(after,private)}));assert ps==tuple(sorted(candidate['all_source_projection_indices'])) and pt==tuple(sorted(candidate['all_target_projection_indices']));b,bt=candidate['source_B_core_index'],candidate['B_target_core_index'];ds=max(debt(a,b) for a in ps);dt=max(debt(a,bt) for a in pt);assert (ds,dt)==(2,0) and 2-candidate['Q']+dt-ds==-1
    sp=importlib.util.spec_from_file_location('independent_interior_contraction_source33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_ORIGINAL_SOURCE_CAP')
        queries+=1
    I.tick=tick;initial=fr(z['initial_common_A_B_BE']);keys=[2,private]+list(range(4,21,2));ranks={k:j+1 for j,k in enumerate(keys)}
    def shape(tree):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,ranks[v.key]-1),walk(v.right,hi))
        return walk(tree.root,11)
    A,F,E=I.Tree(initial),I.Tree(initial),I.Tree(initial);cf=();ce=();word=z['word'];n=len(word);period=z['period_rows'];period_by_t={r['absolute_t']:r for r in period};start=None;Acount=QF=QE=0;genuine=set();seam_before=None;seam_after=None;packet_seen=False
    def update(c,k):return (k,)+tuple(v for v in c if v!=k)
    for copy in range(z['source_prefix_copies']+z['period_copies']):
        for j,(mode,key) in enumerate(word):
            row=z['A_word_source_rows'][j];assert shape(A)==fr(row['before']);pa,ea=A.access(key);assert len(ea)==(len(pa)+1)//2==row['H'] and shape(A)==fr(row['after']);oldF,oldE=shape(F),shape(E);q=qe=0;oldcf,oldce=cf,ce
            absolute=copy*n+j+1
            if absolute==z['period'][0]:seam_before=(fr(row['before']),oldF,oldE,oldcf,oldce)
            if mode=='K':
                k=key//2;froot=F.root.key;pf,ef=F.access(key);q=len(pf)//2
                if froot!=key:cf=update(cf,k)
                if k!=10:
                    eroot=E.root.key;pe,ee=E.access(key);qe=len(pe)//2
                    if eroot!=key:ce=update(ce,k)
            if absolute in period_by_t:
                r=period_by_t[absolute];assert (r['word_index'],r['kind'],r['key'],r['H'],r['QF'],r['QE'])==(j,mode,key,len(ea),q,qe);assert (tuple(r['chartF_before']),tuple(r['chartF_after']),tuple(r['chartE_before']),tuple(r['chartE_after']))==(oldcf,cf,oldce,ce);assert renumber(delete(oldF,private)[0])==T[r['BF_before']] and renumber(delete(shape(F),private)[0])==T[r['BF_after']];assert renumber(delete(oldE,private)[0])==T[r['BE_before']] and renumber(delete(shape(E),private)[0])==T[r['BE_after']];Acount+=len(ea);QF+=q;QE+=qe
                if mode=='K' and oldF[0]!=key:genuine.add(key)
            if absolute==z['packet_absolute_t']:
                assert q==1 and len(ea)==1 and key==2 and shape(A)[0]==2;packet_seen=True
            if absolute==z['period'][1]:seam_after=(shape(A),shape(F),shape(E),cf,ce)
        assert shape(A)==shape(F)==initial
    assert packet_seen and seam_before==seam_after and (Acount,QF,QE)==(150,24,21) and len(genuine)==10
    out('interior_max_contraction_independent_audit.json',{'status':'PASS_SOURCE_EXACT_MAX_CONTRACTION_POTENTIAL_REFUTATION','period':z['period'],'packet_absolute_t':z['packet_absolute_t'],'word_length':n,'actual_original_A_accesses_replayed':n*(z['source_prefix_copies']+z['period_copies']),'fresh_kernel_calls_including_full_and_erased_B':queries,'source_queries':queries,'source_engine_calls':queries,'A_period':Acount,'QF_period':QF,'QE_period':QE,'CD_margin':2*Acount-QF,'source_debt':ds,'target_debt':dt,'packet_price':1,'signed_margin':-1,'all_A_B_BE_and_genuine_recency_orders_close':True,'genuine_KEEP_keys':sorted(genuine),'contractions_enumerated_by':'independent left/right child promotion and recursive anonymous elimination','only_candidate_refuted':'maximum of unchanged D10 over all anchor-only BST contractions','minimum_rule_status':'not refuted by this result; diagonal-zero attempted route rejected','frozen_allocations_changed':False,'not_a_Coarse_Double_counterexample':True,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('interior_max_contraction_closed_source.json','native10_credit_certificate.json')}});print(json.dumps({'status':'PASS_SOURCE_EXACT_MAX_CONTRACTION_POTENTIAL_REFUTATION','source_queries':queries,'period':[124,246],'packet_t':162,'costs':[150,24,21],'margin':276}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify37_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
