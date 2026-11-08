"""New r7/core9 original source with repeated private helper, H1/Q4,
and a literal accepted six-key auxiliary owner receipt on the same period."""
import json,time,sys,importlib.util
from pathlib import Path
from one_helper_source_allocator import build
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def main():
    global queries
    sp=importlib.util.spec_from_file_location('private_source33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('SOURCE_CAP')
        queries+=1;return p0(t,x)
    S.path=path;anchors=[1,2]+list(range(4,11));G=[('D',4),('D',3),('D',1),('K',4),('K',1),('D',2),('D',1),('D',4),('D',2),('D',1)]
    gamma=[('K',x) for x in (3,5,7,9,7,5,3)]+[('D',9),('D',1),('K',1),('K',9),('D',2),('D',9)]+[('K',x) for x in (1,3,5,7,9,7,5,3,1)]
    marked=[1,2,3,5,6,7,9];tour=[('K',x) for x in marked[1:]+list(reversed(marked[:-1]))];word=G*2+[(m,anchors[x-1]) for m,x in gamma+tour];assert len(gamma)==22 and len(word)==54
    tail='F10'
    for k in range(10,4,-1):tail=(k,'F'+str(k-1),tail)
    T=(1,'F0',(2,'F1',(4,(3,'F2','F3'),tail)));state=(T,T,T);seen={};copies=[];j=0
    while state[2] not in seen:
        assert j<30;seen[state[2]]=j;rr=[]
        for local,(mode,x) in enumerate(word,1):
            t=j*len(word)+local;before=state;a,b,e=state;a,pa,ea=S.trace(a,x);pb=pe='';eb=ee=[]
            if mode=='K':b,pb,eb=S.trace(b,x)
            if mode=='K' and x!=10:e,pe,ee=S.trace(e,x)
            state=(a,b,e);rr.append({'occurrence':t,'mode':mode,'target':x,'genuine_F':mode=='K' and before[1][0]!=x,'before':before,'after':state,'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ee,'a':len(ea),'qF':len(pb)//2,'qE':len(pe)//2})
        assert state[:2]==(T,T);copies.append(rr);j+=1
    u=seen[state[2]];L=j-u;rows=sum(copies[u:j],[]);assert rows[0]['before']==rows[-1]['after']
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'));import cd6_allocator as C
    from source_funding import own_map,with_owners
    aux=[]
    for r in rows:
        mode='D' if r['mode']=='K' and r['target']==10 else r['mode'];aa,bb,ee=r['before'];at,bt,et=r['after'];aux.append(dict(r,mode=mode,genuine_F=mode=='K' and ee[0]!=r['target'],qF=r['qE'],before=(aa,ee,ee),after=(at,et,et),BF_path=r['BE_path'],BF_events=r['BE_events']))
    small=C.allocate(aux);assert len(small['marks'])==6 and small['core']<=7
    v=own_map(rows);full=build(rows,v['macros'],v['h0']);assert set(full['h'])==v['D'];v['h']=full['h'];owner=with_owners(v,small['D'],small['f']);a=owner['prior']['allocation'];final=owner['extension']['allocation']
    assert all(final[d]==un for d,un in a.items());critical=[r for r in full['receipt'] if (r['H'],r['Q'])==(1,4)];assert critical and all((r['D_source'],r['D_target'],r['signed_margin'])==(0,2,0) for r in critical)
    M={r['target'] for r in rows if r['genuine_F']};assert len(M)==7 and S.labels(S.core(rows[0]['before'][1],M))==set(anchors)
    out('one_helper_original_source_and_owners.json',{'status':'COMPLETE_ORIGINAL_R7_CORE9_ONE_HELPER_SOURCE_RECEIPT','initial_diagonal':T,'word':word,'reaching_prefix':word*u,'erased_key':10,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'M':sorted(M),'full_B_core':anchors,'full_B_core_size':9,'auxiliary_core_size':small['core'],'auxiliary_marks':sorted(small['marks']),'A':sum(r['a'] for r in rows),'QF':len(v['D']),'QE':len(small['D']),'h0':pack(v['h0']),'h':pack(full['h']),'actual_fE6':pack(small['f']),'old_effective_a':pack(a),'extension':pack(owner['extension']['additions']),'full_f':pack(final),'newly_funded_count':len(owner['extension']['additions']),'full_credit_receipt':full['receipt'],'working_peak':full['working_peak'],'max_debt':full['max_debt'],'cut_before_macro':full['cut_before_macro'],'critical_H1Q4_count':len(critical),'old_five_key_core9_domain':'absent: every nested erased ancestor core lies inside these seven auxiliary labels','actual_certified_fE6_literal_input':True,'all_old_values_fixed':True,'source_queries':queries,'principal_U33':'OPEN'})
    print(json.dumps({'status':'COMPLETE_ORIGINAL_R7_CORE9_ONE_HELPER_SOURCE_RECEIPT','A':sum(r['a'] for r in rows),'QF':len(v['D']),'QE':len(small['D']),'critical_H1Q4':len(critical),'old_effective_owners':len(a),'newly_funded':len(owner['extension']['additions']),'working':full['working_peak'],'aux_core':small['core'],'u':u,'L':L,'source_queries':queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core8_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
