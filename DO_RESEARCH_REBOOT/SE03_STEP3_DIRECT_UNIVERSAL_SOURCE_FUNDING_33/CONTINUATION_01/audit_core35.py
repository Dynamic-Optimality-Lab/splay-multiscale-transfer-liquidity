"""Original seven-KEEP/core13 closed frame activation, full physical ledger."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
from four_hull_source_reuse import from_kernel
from interior_projection_source_tools import fr,isnode
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    sp=importlib.util.spec_from_file_location('frame_original_source35',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);basepath=S.path
    def counted(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('FRAME_SOURCE_CAP')
        queries+=1;return basepath(t,x)
    S.path=counted;N=13;private=5;erased=6;physical=sorted(list(range(2,2*N+1,2))+[private]);rank={k:i+1 for i,k in enumerate(physical)}
    def norm(t):
        def walk(v,hi):return 'F'+str(hi) if not isnode(v) else (v[0],walk(v[1],rank[v[0]]-1),walk(v[2],hi))
        return walk(t,len(physical))
    def vine(lo,hi):return 'E' if lo>hi else (2*lo,'E',vine(lo+1,hi))
    def insert(v):
        if not isnode(v):return v
        return (v[0],(private,'E','E') if v[0]==6 else insert(v[1]),insert(v[2]))
    initial=norm(insert(vine(1,N)));X=vine(3,N-1);A0=norm((2,'E',(4,'E',(private,'E',(2*N,X,'E')))));G=from_kernel(json.loads((B/'interior_max_contraction_closed_source.json').read_text())['four_hull_source_kernel']);A=initial;word=[];arows=[]
    def access(mode,key):
        nonlocal A
        old=A;A,path,ev=S.trace(A,key);word.append((mode,key));arows.append({'mode':mode,'key':key,'before':old,'after':A,'H':len(ev),'path':path,'events':ev,'method':'fresh ordinary14-node A source'})
    def compiled(target):
        nonlocal A
        for row in G.compile(A,target):word.append(('D',row['key']));arows.append({'mode':'D',**row})
        A=target
    W=list(range(3,N+1,2))+list(range(N-2,0,-2));H=[N,1]+list(range(3,N+1,2))+list(range(N-2,0,-2));assert len(W)==12 and len(H)==14
    for k in W[:-1]:access('K',2*k)
    compiled(A0);creator_index=len(word);access('D',2*N);access('D',2);source_frame=A;assert [r['H'] for r in arows[-2:]]==[2,1]
    access('K',2);assert arows[-1]['H']==0;packet_start=len(word);access('D',private);access('K',2*N);packet_end=len(word)-1;destination_frame=A;assert [r['H'] for r in arows[-2:]]==[1,1]
    for k in H[1:]:access('K',2*k)
    compiled(initial);assert A==initial
    F=E=initial;cf=();ce=();seen={};copies=[]
    def upd(c,k):return (k,)+tuple(v for v in c if v!=k)
    while (E,cf,ce) not in seen:
        copy=len(copies);seen[E,cf,ce]=copy;before=(E,cf,ce);rows=[];F=initial
        for i,(mode,key) in enumerate(word):
            f0,e0=F,E;oldcf,oldce=cf,ce;q=qe=0;bfpath=bepath=''
            if mode=='K':
                F,bfpath,_=S.trace(F,key);q=len(bfpath)//2
                if key!=f0[0]:cf=upd(cf,key)
                if key!=erased:
                    E,bepath,_=S.trace(E,key);qe=len(bepath)//2
                    if key!=e0[0]:ce=upd(ce,key)
            rows.append({'absolute_t':copy*len(word)+i+1,'word_index':i,'kind':mode,'key':key,'H':arows[i]['H'],'QF':q,'QE':qe,'BF_before':f0,'BF_after':F,'BE_before':e0,'BE_after':E,'BF_path':bfpath,'BE_path':bepath,'chartF_before':oldcf,'chartF_after':cf,'chartE_before':oldce,'chartE_after':ce})
        assert F==initial;copies.append({'start':before,'end':(E,cf,ce),'rows':rows})
    u=seen[E,cf,ce];L=len(copies)-u;period=sum((c['rows'] for c in copies[u:]),[]);assert u==L==1 and copies[u]['start']==copies[-1]['end'];packet=[r for r in period if packet_start<=r['word_index']<=packet_end];assert len(packet)==2 and sum(r['H'] for r in packet)==2 and sum(r['QF'] for r in packet)==6 and sum(r['QE'] for r in packet)==5
    preceding=period[packet[0]['word_index']-1];assert preceding['key']==2 and preceding['kind']=='K' and preceding['BF_before'][0]!=2 and preceding['H']==0
    aa=sum(r['H'] for r in period);qf=sum(r['QF'] for r in period);qe=sum(r['QE'] for r in period);assert qf==36 and qe==30;units=[(r['absolute_t'],j,b) for r in period for j in range(1,r['H']+1) for b in (0,1)];demands=[(r['absolute_t'],j) for r in period for j in range(1,r['QF']+1)];assert len(units)==2*aa and len(demands)==qf
    result={'status':'EXACT_PAIRED_CLOSED_SEVEN_KEEP_CORE13_FRAME_ACTIVATION','initial_common_A_B_BE':initial,'physical_keys':physical,'marked_KEEP_keys':list(range(2,2*N+1,4)),'erased_KEEP_key':erased,'private_DELETE_key':private,'word':word,'A_word_source_rows':arows,'four_hull_source_kernel':{'trees':G.T,'destinations':G.dest,'H':G.H},'G4_rigid_term_instantiations':G.instantiations,'creator_word_indices':[creator_index,creator_index+1],'packet_word_indices':[packet_start,packet_end],'source_frame':source_frame,'destination_frame':destination_frame,'source_prefix_copies':u,'period_copies':L,'period':[period[0]['absolute_t'],period[-1]['absolute_t']],'period_rows':period,'cold_packet':{'absolute_occurrences':[r['absolute_t'] for r in packet],'H':2,'QF':6,'QE':5,'weight':-2,'comparison_discrepancy':1,'predecessor_genuine_KEEP':preceding['absolute_t']},'actual_A_units':units,'full_B_demands':demands,'A_period':aa,'QF_period':qf,'QE_period':qe,'CD_margin':2*aa-qf,'all_original_operations_and_charts_close':True,'no_fixed_allocation_changed_or_created':True,'refutes':'closure of weak local-fringe predicate under private activation; saturated-source hypothesis deliberately fails due the outside anchor1','not_refuted':'saturated theorem, source Coarse-Double, GateU or Dynamic Optimality','source_queries':queries,'source_engine_calls':queries,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('four_hull_source_basis_independent_audit.json','framed_return_proxy_source_identities.json')}};out('core13_framed_activation_closed_source.json',result);print(json.dumps({k:result[k] for k in ('status','period','A_period','QF_period','QE_period','CD_margin','cold_packet','source_queries','G4_rigid_term_instantiations')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core35_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
