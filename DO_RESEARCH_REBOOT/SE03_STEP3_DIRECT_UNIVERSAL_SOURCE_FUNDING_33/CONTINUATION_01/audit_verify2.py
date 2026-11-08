"""Separate original-source, inventory, owner and bank check of core8 receipt."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def mapping(v):return {tuple(p['demand']):tuple(p['unit']) for p in v}
def main():
    global queries
    z=json.loads((B/'seven_mark_core8_source_and_owners.json').read_text());sp=importlib.util.spec_from_file_location('independent_fixture33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('INDEPENDENT_SOURCE_RESERVE')
        queries+=1
    I.tick=tick
    def shape(tree):
        def go(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,go(v.left,lo,v.key-1),go(v.right,v.key+1,hi))
        return go(tree.root,1,8)
    T=fr(z['initial_diagonal']);trees=[I.Tree(T) for _ in range(3)];u=z['u'];L=z['L'];rows=z['rows'];rowmap={r['occurrence']:r for r in rows};word=z['word'];D=set();E=set();U=set();seen=[]
    for t,(mode,x) in enumerate(z['reaching_prefix']+word*L,1):
        before=tuple(shape(v) for v in trees);pa,ea=trees[0].access(x);pb=pe='';eb=ee=[]
        if mode=='K':pb,eb=trees[1].access(x)
        if mode=='K' and x!=z['erased_key']:pe,ee=trees[2].access(x)
        after=tuple(shape(v) for v in trees)
        if t in rowmap:
            r=rowmap[t];seen.append(t);assert before==fr(r['before']) and after==fr(r['after'])
            assert (len(ea),len(pb)//2,len(pe)//2)==(r['a'],r['qF'],r['qE'])
            assert (pa,pb,pe)==(r['A_path'],r['BF_path'],r['BE_path'])
            D.update((t,k) for k in range(1,r['qF']+1));E.update((t,k) for k in range(1,r['qE']+1));U.update((t,j,b) for j in range(1,r['a']+1) for b in (0,1))
    assert len(seen)==len(rows) and fr(rows[0]['before'])==fr(rows[-1]['after'])
    h0,h,fe,a,f=(mapping(z[k]) for k in ('h0','h','fE6','old_a','full_f'))
    for m,domain in ((h,D),(fe,E),(f,D)):
        assert set(m)==domain and set(m.values())<=U and len(set(m.values()))==len(m)
    assert all(h[d]==v for d,v in h0.items()) and all(f[d]==v for d,v in a.items())
    assert all(f[d]==fe[d] for d in D&E)
    # Independently rebuild the natural cyclic macro partition from rows.
    ends=[i for i,r in enumerate(rows) if r['mode']=='K' and r['before'][1][0]!=r['target']];mm=[]
    for j,end in enumerate(ends):
        pre=ends[j-1];inds=list(range(pre+1,end+1)) if pre<end else list(range(pre+1,len(rows)))+list(range(end+1));seg=[rows[i] for i in inds]
        dd=[(r['occurrence'],k) for r in seg for k in range(1,r['qF']+1)];ev=[(r['occurrence'],j) for r in seg for j in range(1,r['a']+1)];units=[e+(b,) for e in ev for b in (0,1)]
        mm.append((seg,dd,ev));assert all(h0[d]==v for d,v in zip(dd,units))
    debt=json.loads((B/'eight_core_B_law_result.json').read_text())['D'];syntax=json.loads((B/'eight_core_B_source_relation.json').read_text());idx={fr(t):i for i,t in enumerate(syntax['trees'])};bank=[];paid={};released=set();selected_all=set();peak=0
    for rec in z['source_receipt']:
        i=rec['macro_index'];seg,dd,ev=mm[i];ds=debt[idx[fr(seg[0]['before'][1])]];dt=debt[idx[fr(seg[-1]['after'][1])]];K=z['source_debt_width'];c=min(len(ev),2)
        assert rec['ds']==ds and rec['dt']==dt and rec['c']==c and len(bank)==K-ds
        ss=[e+(b,) for e in ev[:c] for b in (0,1)];fixed={d:h0[d] for d in dd if d in h0};assert set(fixed.values())<=set(ss)
        assert 2*c-len(dd)+dt-ds>=0 and not selected_all.intersection(ss);selected_all.update(ss);peak=max(peak,len(bank)+len(ss));pool=bank+[v for v in ss if v not in fixed.values()];paid.update(fixed)
        for d in dd:
            if d not in fixed:paid[d]=pool.pop(0)
        keep=K-dt;released.update(pool[keep:]);bank=pool[:keep];assert bank==list(map(tuple,rec['carry']))
    assert not bank and paid==h and peak==z['full_source_working_peak']<=5 and not set(h.values())&released
    assert set(h.values())|released==selected_all
    # Original h/l exchange is independently reconstructed as paths, without
    # producer adapter imports; all earlier partial paths must be unchanged.
    locked={d:fe[d] for d in D&E};inv={v:d for d,v in locked.items()}
    def exchange(base):
        ans=dict(locked);paths={}
        for start in sorted(set(base)-locked.keys()):
            d=start;path=[];local=set()
            while True:
                assert d not in local;local.add(d);v=base[d];path.append((d,v))
                if v not in inv:ans[start]=v;paths[start]=path;break
                d=inv[v]
                if d not in base:break
        return ans,paths
    old,oldpaths=exchange(h0);new,newpaths=exchange(h);assert old==a and new==f and all(newpaths[k]==p for k,p in oldpaths.items())
    result={'status':'PASS_ORIGINAL_SEVEN_MARK_CORE8_SOURCE_AND_FROZEN_OWNERS','period':z['period'],'full_demands':len(D),'aux_demands':len(E),'frozen_successes':len(a),'working_peak':peak,'critical_H1Q3_present':any(len(ev)==1 and len(dd)==3 for _,dd,ev in mm),'all_source_IDs_and_closure':True,'new_source_queries':queries,'principal_U33':'OPEN','external_or_formal_verification':False,'producer_receipt_sha256':hashlib.sha256((B/'seven_mark_core8_source_and_owners.json').read_bytes()).hexdigest()}
    out('seven_mark_core8_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
