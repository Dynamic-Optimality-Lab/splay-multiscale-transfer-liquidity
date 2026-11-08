"""Independent actual source, I6 instance, signed bank and owner interface."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def rd(p):return json.loads(p.read_text())
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def main():
    global queries
    z=rd(B/'one_helper_original_source_and_owners.json');sp=importlib.util.spec_from_file_location('independent_full_one_helper33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('INDEPENDENT_SOURCE_CAP')
        queries+=1
    I.tick=tick
    def shape(tree,n=10):
        def walk(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,lo,v.key-1),walk(v.right,v.key+1,hi))
        return walk(tree.root,1,n)
    T=fr(z['initial_diagonal']);tt=[I.Tree(T) for _ in range(3)];rr={r['occurrence']:r for r in z['rows']};seen=[]
    for t,(mode,x) in enumerate(z['reaching_prefix']+z['word']*z['L'],1):
        before=tuple(shape(v) for v in tt);pa,ea=tt[0].access(x);pb=pe='';eb=ee=[]
        if mode=='K':pb,eb=tt[1].access(x)
        if mode=='K' and x!=z['erased_key']:pe,ee=tt[2].access(x)
        after=tuple(shape(v) for v in tt)
        if t in rr:
            r=rr[t];seen.append(t);assert before==fr(r['before']) and after==fr(r['after'])
            assert (pa,pb,pe)==(r['A_path'],r['BF_path'],r['BE_path']) and (len(ea),len(pb)//2,len(pe)//2)==(r['a'],r['qF'],r['qE'])
    rows=z['rows'];assert len(seen)==len(rows) and fr(rows[0]['before'])==fr(rows[-1]['after']) and z['u']==0 and z['L']==1
    M={r['target'] for r in rows if r['genuine_F']};EM={r['target'] for r in rows if r['mode']=='K' and r['target']!=10 and r['before'][2][0]!=r['target']};assert len(M)==7 and len(EM)==6
    def core(v,marks):
        if isinstance(v,str):return set()
        k,l,r=v;L=core(l,marks);R=core(r,marks);return L|R|{k} if k in marks or L or R else set()
    assert len(core(rows[0]['before'][1],M))==9 and len(core(rows[0]['before'][2],EM))==7
    def macros(which):
        ix=1 if which=='F' else 2;key='q'+which;ends=[i for i,r in enumerate(rows) if r['mode']=='K' and (which=='F' or r['target']!=10) and r['before'][ix][0]!=r['target']];out=[]
        for j,end in enumerate(ends):
            prev=ends[j-1];seg=rows[prev+1:end+1] if prev<end else rows[prev+1:]+rows[:end+1];D=[(r['occurrence'],k) for r in seg for k in range(1,r[key]+1)];U=[(r['occurrence'],i,b) for r in seg for i in range(1,r['a']+1) for b in (0,1)];out.append({'rows':seg,'D':D,'U':U,'H':len(U)//2,'Q':len(D)})
        return out
    fm=macros('F');em=macros('E');h0={d:u for m in fm for d,u in zip(m['D'],m['U'])};e0={d:u for m in em for d,u in zip(m['D'],m['U'])};ef=dict(e0)
    for j,m in enumerate(em):
        if m['Q']>2*m['H']:
            pre=em[(j-1)%len(em)];assert (m['H'],m['Q'])==(1,3) and pre['Q']<=1;ef[m['D'][2]]=pre['U'][pre['Q']]
    assert ef==mp(z['actual_fE6']) and h0==mp(z['h0'])
    D={d for m in fm for d in m['D']};E={d for m in em for d in m['D']};U={u for m in fm for u in m['U']};h=mp(z['h']);a=mp(z['old_effective_a']);f=mp(z['full_f']);assert len(D)==32 and len(E)==18 and len(U)==136
    for value,domain in ((h,D),(ef,E),(f,D)):
        assert set(value)==domain and len(set(value.values()))==len(value) and set(value.values())<=U
    assert all(h[d]==v for d,v in h0.items()) and all(f[d]==v for d,v in a.items())
    AT=rd(B/'ten_anchor_LOW_source_schemas.json')['trees'];BT=rd(B/'nine_label_native_action_cache.json')['trees'];AI={fr(t):i for i,t in enumerate(AT)};BI={fr(t):i for i,t in enumerate(BT)};C=rd(B/'one_helper_p3_certificate.json');L=dict(C['nonzero_debt']);anchors=[1,2]+list(range(4,11));rank={k:i+1 for i,k in enumerate(anchors)}
    def project(v,upper=9):
        if isinstance(v,str):return 'F'+str(upper)
        k,l,r=v
        if k==3:assert isinstance(l,str) and isinstance(r,str);return 'F'+str(upper)
        key=rank[k];return key,project(l,key-1),project(r,upper)
    def debt(state):return L.get(AI[fr(state[0])]*4862+BI[project(state[1])],0)
    bank=[];paid={};released=set();selected_all=set();peak=0;crit=0
    for r in z['full_credit_receipt']:
        m=fm[r['macro_index']];seg=m['rows'];ds=debt(seg[0]['before']);dt=debt(seg[-1]['after']);c=min(m['H'],3);K=z['max_debt'];assert (ds,dt,c)==(r['D_source'],r['D_target'],r['c']) and len(bank)==K-ds
        selected=m['U'][:2*c];fixed={d:h0[d] for d in m['D'] if d in h0};assert set(fixed.values())<=set(selected);assert 2*c-m['Q']+dt-ds==r['signed_margin']>=0
        peak=max(peak,len(bank)+len(selected));pool=bank+[u for u in selected if u not in fixed.values()];paid.update(fixed)
        for d in m['D']:
            if d not in fixed:paid[d]=pool.pop(0)
        keep=K-dt;released.update(pool[keep:]);bank=pool[:keep];assert bank==list(map(tuple,r['carry']));selected_all.update(selected)
        if (m['H'],m['Q'])==(1,4):assert (ds,dt)==(0,2);crit+=1
    assert not bank and paid==h and peak==z['working_peak']==8 and crit==1 and set(h.values())|released==selected_all and not set(h.values())&released
    locked={d:ef[d] for d in D&E};inverse={u:d for d,u in locked.items()}
    def exchange(base):
        answer=dict(locked);paths={}
        for start in sorted(set(base)-locked.keys()):
            d=start;vis=set();path=[]
            while d in base:
                assert d not in vis;vis.add(d);u=base[d];path.append((d,u))
                if u not in inverse:answer[start]=u;paths[start]=path;break
                d=inverse[u]
        return answer,paths
    prior,pp=exchange(h0);final,fp=exchange(h);assert prior==a and final==f and all(fp[d]==v for d,v in pp.items()) and len(D-set(a))==2
    result={'status':'PASS_ORIGINAL_R7_CORE9_ONE_HELPER_SOURCE_OWNER_AND_BANK','period':z['period'],'all_original_operations':len(rows),'A':68,'QF':32,'QE':18,'auxiliary_core':7,'critical_H1Q4':1,'critical_debt_endpoints':[0,2],'frozen_effective_owners_preserved':30,'new_distinct_owners':2,'working_peak':8,'same_actual_period_and_closure':True,'new_source_queries':queries,'external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('one_helper_original_source_and_owners.json','one_helper_p3_certificate.json')},'principal_U33':'OPEN'}
    out('one_helper_original_source_independent_audit.json',result)
    registry=rd(B/'one_helper_source_registry.json');audit_cases=[]
    for p in range(1,6):
        path=B/('one_helper_p%d_independent_audit.json'%p);q=rd(path);assert q['status']=='PASS_COMPLETE_ONE_HELPER_SOURCE_CASE';audit_cases.append({'helper':p,'audit':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'coefficients':q['nonzero_coefficients']})
    out('one_helper_complete_independent_registry.json',{'status':'COMPLETE_ONE_HELPER_SOURCE_THEOREM_ALL_TEN_ORDERED_GAPS','direct_case_audits':audit_cases,'reflections':registry['all_ordered_helper_positions'],'primitive_lift_audit':'ten_anchor_schema_independent_audit.json','actual_owner_source_audit':'one_helper_original_source_independent_audit.json','width':2,'working_bound':8,'all_quantifiers':'exactly the backbone/private-gap scope of ONE_HELPER_SOURCE_THEOREM.md','principal_U33':'OPEN','independent_review':'distinct implementations operated by same agent; not external or formal certification'})
    print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify14_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
