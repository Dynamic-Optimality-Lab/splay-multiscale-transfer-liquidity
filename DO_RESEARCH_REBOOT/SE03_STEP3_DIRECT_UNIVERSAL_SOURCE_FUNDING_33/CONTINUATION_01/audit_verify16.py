"""Independent original-source audit of the natural width2 refutation."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    z=json.loads((B/'native10_width2_source_countercertificate.json').read_text());sp=importlib.util.spec_from_file_location('independent_native10_width_source33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_SOURCE_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def go(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,go(v.left,lo,v.key-1),go(v.right,v.key+1,hi))
        return go(tree.root,1,10)
    T=fr(z['initial_diagonal']);tt=[I.Tree(T) for _ in range(3)];rows={r['occurrence']:r for r in z['rows']};seen=[];lru=[];elru=[];start_lru=start_elru=None
    for t,(mode,x) in enumerate(z['reaching_prefix']+z['word']*z['L'],1):
        if t==z['period'][0]:start_lru=lru[:];start_elru=elru[:]
        before=tuple(shape(v) for v in tt);pa,ea=tt[0].access(x);pb=pe='';eb=ee=[]
        if mode=='K':pb,eb=tt[1].access(x)
        if mode=='K' and x!=z['erased_key']:pe,ee=tt[2].access(x)
        after=tuple(shape(v) for v in tt)
        if mode=='K':
            if x in lru:lru.remove(x)
            lru.insert(0,x)
            if x!=z['erased_key']:
                if x in elru:elru.remove(x)
                elru.insert(0,x)
        if t in rows:
            r=rows[t];seen.append(t);assert before==fr(r['before']) and after==fr(r['after']) and (pa,pb,pe)==(r['A_path'],r['BF_path'],r['BE_path'])
            assert (len(ea),len(pb)//2,len(pe)//2)==(r['a'],r['qF'],r['qE'])
            assert r['genuine_F']==(mode=='K' and before[1][0]!=x)
    assert len(seen)==len(z['rows']) and fr(z['rows'][0]['before'])==fr(z['rows'][-1]['after']) and start_lru==lru and start_elru==elru
    M={r['target'] for r in z['rows'] if r['genuine_F']};assert M==set(range(1,11))
    rr=z['rows'];ends=[i for i,r in enumerate(rr) if r['genuine_F']];mm=[]
    for j,end in enumerate(ends):
        p=ends[j-1];seg=rr[p+1:end+1] if p<end else rr[p+1:]+rr[:end+1];assert not any(r['qF'] for r in seg[:-1]);h=sum(r['a'] for r in seg);q=sum(r['qF'] for r in seg);mm.append((seg,h,q))
    actual=[]
    for p in z['window_packets']:
        s,h,q=next((s,h,q) for s,h,q in mm if [r['occurrence'] for r in s]==p['occurrences']);assert (h,q)==(p['H'],p['Q']);actual.append((h,q,2*h-q))
    assert actual==[(1,4,-2),(1,3,-1)] and rows[44]['genuine_F'] and z['window']==[45,46]
    residual=[(r['occurrence'],k) for p in z['window_packets'] for r in [rows[p['occurrences'][-1]]] for k in range(2*r['a']+1,r['qF']+1)];assert residual==[(45,3),(45,4),(46,3)]
    A=sum(r['a'] for r in rr);Q=sum(r['qF'] for r in rr);E=sum(r['qE'] for r in rr);assert (A,Q,E)==(53,27,21)
    result={'status':'PASS_SOURCE_EXACT_NATIVE10_WIDTH_THREE_LOWER_BOUND','period':z['period'],'genuine_KEEP_support':10,'actual_consecutive_natural_packets':actual,'window':[45,46],'window_weight':-3,'necessary_debt_range_at_least':3,'A':A,'QF':Q,'QE':E,'CD_margin':2*A-Q,'full_and_erased_chart_seam_closed':True,'all_three_trees_closed':True,'original_source_operations_per_period':len(rr),'new_source_queries':queries,'refuted_scope':'ALL-state range2 law on natural packets; not CD or original GateU14','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_width2_source_countercertificate.json','NATIVE10_WIDTH_THREE_LOWER_BOUND.md')},'principal_U33':'OPEN'}
    out('native10_width3_lower_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify16_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
