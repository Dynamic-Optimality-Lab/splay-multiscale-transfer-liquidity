"""Independent source-exact support7/core9 countercertificate for2-Q only."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    z=json.loads((B/'nine_core_B_only_seven_mark_bridge.json').read_text())['answer'];assert z is not None
    sp=importlib.util.spec_from_file_location('independent_B_only_counter33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('INDEPENDENT_SOURCE_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def go(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,go(v.left,lo,v.key-1),go(v.right,v.key+1,hi))
        return go(tree.root,1,9)
    T=fr(z['initial']);trees=[I.Tree(T) for _ in range(3)];word=z['word'];M=set(z['M']);erased=2;seen={};copies=[];copy=0
    def core(t):
        if isinstance(t,str):return set()
        k,l,r=t;L=core(l);R=core(r)
        return L|R|{k} if k in M or L or R else set()
    while shape(trees[2]) not in seen:
        assert copy<50;seen[shape(trees[2])]=copy;rows=[]
        for local,(mode,x) in enumerate(word,1):
            assert mode=='K';t=copy*len(word)+local;before=tuple(shape(v) for v in trees);pa,ea=trees[0].access(x);pb,eb=trees[1].access(x);pe='';ee=[]
            if x!=erased:pe,ee=trees[2].access(x)
            after=tuple(shape(v) for v in trees);assert after[0]==after[1] and core(before[1])==set(range(1,10))
            rows.append({'occurrence':t,'mode':mode,'target':x,'before':before,'after':after,'A_path':pa,'BF_path':pb,'BE_path':pe,'a':len(ea),'qF':sum(e['kind']=='DOUBLE' for e in eb),'qE':sum(e['kind']=='DOUBLE' for e in ee),'A_events':ea,'BF_events':eb,'BE_events':ee,'genuine_F':before[1][0]!=x})
        assert shape(trees[0])==shape(trees[1])==T;copies.append(rows);copy+=1
    u=seen[shape(trees[2])];L=copy-u;rows=sum(copies[u:copy],[]);assert rows[0]['before']==rows[-1]['after']
    assert all(r['genuine_F'] for r in rows) and {r['target'] for r in rows}==M
    qsum=sum(r['qF'] for r in rows);asum=sum(r['a'] for r in rows);rawprice=2*len(rows)-qsum;assert rawprice==-2*L and 2*asum-qsum==134*L
    h0=[{'demand':(r['occurrence'],k),'unit':(r['occurrence'],(k-1)//2+1,(k-1)%2)} for r in rows for k in range(1,r['qF']+1)]
    assert len({tuple(v['unit']) for v in h0})==qsum and all(v['unit'][1]<=next(r['a'] for r in rows if r['occurrence']==v['unit'][0]) for v in h0)
    result={'status':'PASS_SOURCE_EXACT_SEVEN_KEEP_CORE9_REFUTATION_OF_2_MINUS_Q','initial_diagonal':T,'word':word,'reaching_prefix':word*u,'erased_key':erased,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'M':sorted(M),'full_core':list(range(1,10)),'A':asum,'QF':qsum,'QE':sum(r['qE'] for r in rows),'B_only_price':rawprice,'actual_price':2*asum-qsum,'actual_full_h0':h0,'paired_and_erased_closed':True,'all_original_demands_funded_locally':True,'refuted_claim':'2-Q+DeltaD>=0 on every genuine natural macro, for ANY seam-closed state debt; not2H-Q','principal_U33':'OPEN','new_source_queries':queries,'external_or_formal_verification':False,'producer_input_sha256':hashlib.sha256((B/'nine_core_B_only_seven_mark_bridge.json').read_bytes()).hexdigest()}
    out('nine_core_B_only_source_independent_audit.json',result);print(json.dumps({k:result[k] for k in ('status','u','L','A','QF','B_only_price','actual_price','new_source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
