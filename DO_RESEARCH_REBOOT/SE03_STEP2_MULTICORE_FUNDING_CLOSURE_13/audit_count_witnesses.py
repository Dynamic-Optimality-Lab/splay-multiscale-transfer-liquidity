"""Explicit source witnesses with exactly ONE slot for cores9..11.
All other macros are physically overfunded by real A-only accesses.
Final A reset uses a recorded actual DELETE path, never an abstract splice.
Independent immutable search and original-source replay are both retained.
"""
import collections,importlib.util,json,time
from pathlib import Path
from source_funding import X,extend
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
I=load('immutable_count13',ROOT/'python/independent/splay.py')
p=load('original_count13',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py');calls=0;pcalls=0;original=p.trace
def move(t,x):
    global calls
    calls+=1;assert calls+pcalls<1900000 and I.lookup(t,x)[0];return I.trace(t,x)
def ptrace(t,x):
    global pcalls
    pcalls+=1;assert calls+pcalls<1900000;return original(t,x)
p.trace=ptrace
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def tree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],tree(t[1]),tree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def serial(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [serial(x) for x in v]
    return v
def reset_path(start,end,k):
    q=collections.deque([start]);prev={start:None}
    while end not in prev:
        assert q and len(prev)<100000,'bounded source reset unavailable';a=q.popleft()
        for x in range(1,k+1):
            if x==a[1]:continue
            b=move(a,x)[0]
            if b not in prev:prev[b]=(a,x);q.append(b)
    path=[];v=end
    while v!=start:a,x=prev[v];path.append(x);v=a
    return list(reversed(path)),len(prev)
def main():
    ref=json.loads((B/'bf_source_refinement.json').read_text());reports=[]
    for source in ref['reports']:
        k=source['core'];R=tree(source['initial_A_BF']);bw=[tuple(v) for v in source['source_word']]
        critical=next(i for i,r in enumerate(source['rows']) if 1<i<len(bw)-1 and r['qF']==3);xcrit=bw[critical][1]
        word=[];oldroot=R[1]
        for j,(m,x) in enumerate(bw):
            assert x!=oldroot
            if j==critical:word.append(('K',x))
            else:
                word += [('D',oldroot),('D',x),('D',oldroot),('D',x)]
                if j==critical-1:word += [('D',xcrit),('D',x)]
                word.append(('K',x))
            oldroot=x
        A=R
        for m,x in word:A=move(A,x)[0]
        reset,visited=reset_path(A,R,k);word += [('D',x) for x in reset]
        for reflected in (False,True):
            def mirror(t):return ('leaf','F'+str(k-int(t[1][1:]))) if t[0]=='leaf' else I.node(k+1-t[1],mirror(t[3]),mirror(t[2]))
            R0=mirror(R) if reflected else R;ww=[(m,k+1-x if reflected else x) for m,x in word]
            marks={x for m,x in ww if m=='K'};erased_runs=[];rows0=None
            for z in sorted(marks):
                E=R0;seen={};j=0
                while E not in seen:
                    assert j<30;seen[E]=j;j+=1
                    for m,x in ww:
                        if m=='K' and x!=z:E=move(E,x)[0]
                L=j-seen[E]
                if L!=1:
                    erased_runs.append({'erased':z,'L':L,'one_slot_claim':False});continue
                E0=E;rows,end=p.replay(plain(R0),ww,erased=z,erased_start=plain(E0));assert end==(plain(R0),plain(R0),plain(E0))
                assert {r['target'] for r in rows if r['genuine_F']}==marks and len(marks)==6
                assert all(len(p.labels(p.core(r['before'][1],marks)))==k for r in rows)
                packets=p.packets(rows);Rset=[];h0={};allU=set();D=set();spares=[]
                for pp in packets:
                    rr=[rows[t-1] for t in pp['occurrences']];uu=[(r['occurrence'],j,b) for r in rr for j in range(1,r['a']+1) for b in (0,1)]
                    dd=[(r['occurrence'],j) for r in rr for j in range(1,r['qF']+1)];n=min(len(uu),len(dd));h0.update(zip(dd[:n],uu[:n]));Rset+=dd[n:]
                    allU.update(uu);D.update(dd)
                    if len(uu)>len(dd):spares+=uu[len(dd):]
                assert len(Rset)==1 and rows[Rset[0][0]-1]['qF']==3 and spares
                h={**h0,Rset[0]:spares[0]};assert set(h)==D and len(set(h.values()))==len(h)
                Eids={(r['occurrence'],j) for r in rows for j in range(1,r['qE']+1)};us=sorted(allU);fE=dict(zip(sorted(Eids),us));C=D&Eids;l={d:fE[d] for d in C}
                prior=X.exchange(D,allU,l,h0);ex=extend(D,allU,prior['allocation'],h);licensed=X.exchange(D,allU,l,h)
                assert ex['allocation']==licensed['allocation'] and all(ex['allocation'][d]==u for d,u in prior['allocation'].items())
                erased_runs.append({'erased':z,'L':1,'preperiod_word_copies':seen[E0],'initial_BE':plain(E0),
                    'rows':rows,'packets':packets,'R':Rset,'h0':pack(h0),'h':pack(h),
                    'logical_owner_fixture_not_numeric_sealed_fE':True,'fE':pack(fE),'paid':pack(prior['allocation']),
                    'extension_paths':ex['paths'],'final':pack(ex['allocation'])})
                if rows0 is None:rows0=rows
            assert rows0 is not None
            reports.append({'core':k,'reflected':reflected,'initial_A_BF':plain(R0),'word':ww,
                'critical_BF_original_index':critical+1,'source_A_reset_DELETE_path':[k+1-x if reflected else x for x in reset],
                'reset_search_states':visited,'A':sum(r['a'] for r in rows0),'QF':sum(r['qF'] for r in rows0),
                'exact_physical_slot_count':1,'all_six_genuine_keys':sorted(marks),'erased_runs':erased_runs,
                'reachability':'start at diagonal R0; direct original word returns A/BF to R0; actual erased recurrence recorded',
                'lifting':'all gaps are individually named free terms; explicit source rotations preserve each ordered gap, so arbitrary-gap substitution commutes'})
    out('slot_count_witnesses.json',serial({'status':'ACTUAL_ONE_SLOT_WITNESSES_CORE9_10_11',
        'reports':reports,'count_range_proof':'zero by all-KEEP closed BF source, one by these explicit A/BF/BE closed words, m by repeating one aligned L1 interval',
        'not_claimed':'funding all sources at these cores; these are explicit overprepared source families only',
        'immutable_calls':calls,'original_source_calls':pcalls,'source_engine_calls':calls+pcalls}))
    print(json.dumps({'status':'PASS_EXACT_SLOT_RANGE_WITNESSES','reports':len(reports),'calls':calls+pcalls,
        'cores':[{k:v for k,v in r.items() if k in ('core','reflected','A','QF','reset_search_states')} for r in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_count_witnesses_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls+pcalls})
