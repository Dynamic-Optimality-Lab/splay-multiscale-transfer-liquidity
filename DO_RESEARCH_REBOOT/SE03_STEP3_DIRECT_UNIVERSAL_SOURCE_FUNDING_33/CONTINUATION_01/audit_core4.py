"""One actual seven-mark/core8 critical source and licensed owner receipt.
Uses old accepted I6 as input comparison, not an invented seven-key base.
"""
import json,time,sys,importlib.util
from pathlib import Path
from core8_source_allocator_v2 import build
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def main():
    global queries
    sp=importlib.util.spec_from_file_location('native_core8_fixture33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>=CAP-3:raise TimeoutError('SOURCE_CAP')
        queries+=1;return p0(t,x)
    S.path=path
    gamma=[('K',x) for x in (3,5,7,5,3)]+[('D',7),('D',1),('K',1),('K',7),('D',2),('D',7)]+[('K',x) for x in (1,3,5,7,5,3,1)]
    M={1,2,3,5,6,7,8};asc=sorted(M-{1});walk=[('K',x) for x in asc+list(reversed([1]+asc[:-1]))];word=gamma+walk
    assert len(gamma)==18 and len(word)==30
    T=S.vine(8);state=(T,T,T);seen={};copies=[];copy=0
    while state[2] not in seen:
        assert copy<30;seen[state[2]]=copy;rr=[]
        for local,(mode,x) in enumerate(word,1):
            t=copy*len(word)+local;before=state;a,b,e=state;a,pa,ea=S.trace(a,x);pb=pe='';eb=ee=[]
            if mode=='K':b,pb,eb=S.trace(b,x)
            if mode=='K' and x!=3:e,pe,ee=S.trace(e,x)
            state=(a,b,e);rr.append({'occurrence':t,'mode':mode,'target':x,'genuine_F':mode=='K' and before[1][0]!=x,
                'before':before,'after':state,'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ee,'a':len(ea),'qF':len(pb)//2,'qE':len(pe)//2})
        assert state[:2]==(T,T);copies.append(rr);copy+=1
    u=seen[state[2]];L=copy-u;rows=sum(copies[u:copy],[]);assert rows[0]['before']==rows[-1]['after']
    assert {r['target'] for r in rows if r['genuine_F']}==M
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'));import cd6_allocator as A
    from source_funding import own_map,with_owners
    aux=[]
    for r in rows:
        mode='D' if r['mode']=='K' and r['target']==3 else r['mode'];aa,bb,ee=r['before'];at,bt,et=r['after']
        aux.append(dict(r,mode=mode,genuine_F=mode=='K' and ee[0]!=r['target'],qF=r['qE'],before=(aa,ee,ee),after=(at,et,et),BF_events=r['BE_events']))
    small=A.allocate(aux);assert len(small['marks'])==6 and small['core']<=8
    v=own_map(rows);full=build(rows,v['macros'],v['h0']);assert set(full['h'])==v['D']
    v.update(full);owner=with_owners(v,small['D'],small['f']);final=owner['extension']['allocation'];a=owner['prior']['allocation']
    assert all(final[d]==un for d,un in a.items()) and len(set(final.values()))==len(final)
    critical=[m for m in v['macros'] if m['Q']>2*m['H']];assert critical and all((m['H'],m['Q'])==(1,3) for m in critical)
    out('seven_mark_core8_source_and_owners.json',{'status':'COMPLETE_SEVEN_MARK_CORE8_SOURCE_RECEIPT','initial_diagonal':T,'word':word,'reaching_prefix':word*u,
        'erased_key':3,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'marks':sorted(M),
        'counts':{'A':sum(r['a'] for r in rows),'QF':len(v['D']),'QE':len(small['D'])},'h0':pack(v['h0']),'h':pack(full['h']),
        'fE6':pack(small['f']),'old_a':pack(a),'extension':pack(owner['extension']['additions']),'full_f':pack(final),
        'full_source_working_peak':full['working_peak'],'source_debt_width':full['maxD'],'source_receipt':full['receipt'],
        'auxiliary_core':small['core'],'old_five_core9_domain':'impossible: every nested marked core is a subset of these8 anchors',
        'canonical_raw_f6_at_its_actual_domain':True,'all_old_values_unchanged':True,'principal_U33':'OPEN','new_source_queries':queries})
    print(json.dumps({'status':'COMPLETE_SEVEN_MARK_CORE8_SOURCE_RECEIPT','u':u,'L':L,'working':full['working_peak'],'D':len(final),'old_a':len(a),'aux_core':small['core'],'queries':queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core4_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})

