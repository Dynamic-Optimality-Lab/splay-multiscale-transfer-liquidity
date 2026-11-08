"""Distinct source replay of the core13 frame and arbitrary-term return identities."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
from audit_verify36 import calc
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def node(v):return isinstance(v,tuple)
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    identities=json.loads((B/'framed_return_proxy_source_identities.json').read_text());A0=fr(identities['initial_unary_A']);C0=fr(identities['old_initial']);R,G,j,p=4,1,2,2.5
    A,h=calc(A0,R);A,h2=calc(A,G);C,c=calc(C0,R);C,c2=calc(C,G);assert (h,h2,c,c2)==(2,1,1,1) and A==fr(identities['framed_source']) and C==fr(identities['framed_comparison']);A,h=calc(A,p);A,h2=calc(A,R);C,c=calc(C,j);C,c2=calc(C,R);assert (h,h2,c,c2)==(1,1,1,1) and A==fr(identities['unprotected_destination']) and C==fr(identities['normalized_comparison_destination']);U,u=calc(A,G);V,v=calc(U,R);CU,cu=calc(C,G);CV,cv=calc(CU,R);assert (u,v,cu,cv)==(1,1,1,1) and V==A and CV==C;V,a=calc(U,p);V,b=calc(V,R);CV,c=calc(CU,j);CV,d=calc(CV,R);assert a==b==c==d==1 and V==A and CV==C
    z=json.loads((B/'core13_framed_activation_closed_source.json').read_text());G4=json.loads((B/'four_hull_source_basis_independent_audit.json').read_text());assert G4['status'].startswith('PASS');Gtrees=list(map(fr,G4['source_kernel']['trees']));kernel=G4['source_kernel'];physical=z['physical_keys'];rank={k:i+1 for i,k in enumerate(physical)};initial=fr(z['initial_common_A_B_BE']);n=len(z['word'])
    spec=importlib.util.spec_from_file_location('independent_core13_frame62',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
    def tick():
        global queries
        if queries>=int(sys.argv[2]) or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_FRAME_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,rank[v.key]-1),walk(v.right,hi))
        return walk(tree.root,len(physical))
    current=initial;H=[];hulls=0
    for (mode,key),row in zip(z['word'],z['A_word_source_rows']):
        before,after=fr(row['before']),fr(row['after']);assert before==current and (mode,key)==(row['mode'],row['key'])
        if 'hull_keys' in row:
            kk=row['hull_keys'];kr={k:i+1 for i,k in enumerate(kk)};payload={}
            def compress(v,hi):
                if not node(v) or v[0] not in kr:payload[hi]=v;return 'F'+str(hi)
                r=kr[v[0]];return r,compress(v[1],r-1),compress(v[2],hi)
            ct=compress(before,4);s=row['G4_before'];x=row['G4_key'];dest=row['G4_after'];assert ct==Gtrees[s] and key==kk[x-1] and dest==kernel['destinations'][s][x-1] and row['H']==kernel['H'][s][x-1]
            def expand(v):return payload[int(v[1:])] if not node(v) else (kk[v[0]-1],expand(v[1]),expand(v[2]))
            assert expand(Gtrees[dest])==after;hulls+=1
        elif before[0]==key:assert before==after and row['H']==0
        else:T=I.Tree(before);path,events=T.access(key);assert shape(T)==after and len(events)==row['H']==(len(path)+1)//2
        H.append(row['H']);current=after
    assert current==initial and len(H)==n
    BF=I.Tree(initial);BE=I.Tree(initial);cf=();ce=();period={r['absolute_t']:r for r in z['period_rows']};begin=end=None;A=QF=QE=0;genuine=set();verified=[]
    def upd(c,k):return (k,)+tuple(v for v in c if v!=k)
    for copy in range(z['source_prefix_copies']+z['period_copies']):
        for i,(mode,key) in enumerate(z['word']):
            absolute=copy*n+i+1;f0,e0=shape(BF),shape(BE);oldcf,oldce=cf,ce;q=qe=0;pf=pe=''
            if absolute==z['period'][0]:begin=(initial,f0,e0,cf,ce)
            if mode=='K':
                pf,ef=BF.access(key);q=len(pf)//2
                if key!=f0[0]:cf=upd(cf,key)
                if key!=z['erased_KEEP_key']:
                    pe,ee=BE.access(key);qe=len(pe)//2
                    if key!=e0[0]:ce=upd(ce,key)
            f1,e1=shape(BF),shape(BE)
            if absolute in period:
                r=period[absolute];assert (i,mode,key,H[i],q,qe)==(r['word_index'],r['kind'],r['key'],r['H'],r['QF'],r['QE']);assert (f0,f1,e0,e1)==tuple(fr(r[k]) for k in ('BF_before','BF_after','BE_before','BE_after'));assert (cf,ce,oldcf,oldce)==tuple(tuple(r[k]) for k in ('chartF_after','chartE_after','chartF_before','chartE_before'));assert pf==r['BF_path'] and pe==r['BE_path'];A+=H[i];QF+=q;QE+=qe
                if mode=='K' and key!=f0[0]:genuine.add(key)
                verified.append(r)
            if absolute==z['period'][1]:end=(initial,f1,e1,cf,ce)
        assert shape(BF)==initial
    assert begin==end and (A,QF,QE)==(159,36,30) and len(genuine)==7 and genuine==set(z['marked_KEEP_keys']);packet=[r for r in verified if r['absolute_t'] in z['cold_packet']['absolute_occurrences']];assert [r['absolute_t'] for r in packet]==[207,208] and sum(r['H'] for r in packet)==2 and sum(r['QF'] for r in packet)==6 and sum(r['QE'] for r in packet)==5
    ends=[i for i,r in enumerate(verified) if r['kind']=='K' and r['key']!=r['BF_before'][0]];at=next(k for k,i in enumerate(ends) if verified[i]['absolute_t']==208);left=ends[at-1];right=ends[at];assert verified[left]['absolute_t']==206 and right-left==2
    units=[(r['absolute_t'],j,b) for r in verified for j in range(1,r['H']+1) for b in (0,1)];demands=[(r['absolute_t'],j) for r in verified for j in range(1,r['QF']+1)];assert units==list(map(tuple,z['actual_A_units'])) and demands==list(map(tuple,z['full_B_demands'])) and len(units)==318 and len(demands)==36
    deps=('FRAMED_RETURN_SOURCE_BRIDGE.md','framed_return_proxy_source_identities.json','core13_framed_activation_closed_source.json','four_hull_source_basis_independent_audit.json')
    out('framed_return_and_core13_independent_audit.json',{'status':'PASS_UNIFORM_FRAME_RETURN_IDENTITIES_AND_ORIGINAL_CORE13_CLOSED_SOURCE','uniform_free_term_return_and_proxy_identities':True,'arbitrary_finite_repetition':'induction on two exact paired source/comparison states','original_period':[133,264],'all_A_full_B_erased_B_and_charts_closed':True,'genuine_KEEP_support':7,'all_original_operations_accounted_for':True,'A_period':A,'QF_period':QF,'QE_period':QE,'CD_margin':2*A-QF,'cold_packet':z['cold_packet'],'actual_units':len(units),'full_demands':len(demands),'G4_instances_checked':hulls,'fresh_mutable_source_queries':queries,'source_queries':queries,'source_engine_calls':queries,'no_frozen_owner_or_auxiliary_normalization_receipt_invented':True,'not_a_CD_counterexample':True,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}});print(json.dumps({'status':'PASS_UNIFORM_FRAME_AND_SOURCE_EXACT_CLOSED_CORE13','source_queries':queries,'A':A,'QF':QF,'QE':QE,'packet_margin':-2,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify62_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
