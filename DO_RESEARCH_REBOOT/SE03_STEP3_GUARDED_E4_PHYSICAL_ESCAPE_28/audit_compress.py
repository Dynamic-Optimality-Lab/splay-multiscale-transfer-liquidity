"""Separate source control: shorten DELETE preparations, preserving all
physical A states at KEEPs. The frozen W199 is never modified."""
import collections,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();calls=0
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C28_producer_source',OLD/'audit_construct.py');entry=json.loads((B/'entry.json').read_text());limit=min(165000,entry['remaining_conservative_queries']-10000)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(z) for z in t) if isinstance(t,list) else t
cache={}
def splay(t,x):
    if (t,x) not in cache:
        if C.queries>=limit or time.process_time()-START>=CAP-1:raise TimeoutError('source-control limit')
        cache[t,x]=C.tr(t,x)[0]
    return cache[t,x]
def run(t,w):
    for x in w:t=splay(t,x)
    return t
def main():
    c=json.loads((OLD/'aligned_source_and_owners.json').read_text());rr=c['rows'];initial=fr(c['initial']);word=[tuple(z) for z in c['period']]
    # Independently retained periods are new source objects. Tags move only
    # in this separate object; old source and old owner receipts stay literal.
    intervals=[];i=0
    while i<len(word):
        if word[i][0]=='K':i+=1;continue
        j=i
        while j<len(word) and word[j][0]=='D':j+=1
        intervals.append((i,j));i=j
    new=[];cursor=0;report=[]
    for a,b in intervals:
        new.extend((i,word[i]) for i in range(cursor,a));oldkeys=[x for mode,x in word[a:b]];start=fr(rr[a]['before'][0]);goal=fr(rr[b-1]['after'][0]);best=oldkeys[:]
        # Exact endpoints first: single deletions and removed contiguous runs.
        changed=True
        while changed:
            changed=False
            for span in range(min(8,len(best)),0,-1):
                for j in range(len(best)-span+1):
                    z=best[:j]+best[j+span:]
                    if run(start,z)==goal:best=z;changed=True;break
                if changed:break
        # Beam over DELETE subsequences. This is a bounded discovery tool,
        # not a completeness proof about all A preparations.
        states={start:(0,[])};width=600
        if len(oldkeys)>=10:
            for x in oldkeys:
                nxt=dict(states)
                for t,(cost,route) in states.items():
                    z=splay(t,x);w=C.original_path(t,x);v=(cost+(len(w)+1)//2,route+[x])
                    if z not in nxt or (v[0],len(v[1]))<(nxt[z][0],len(nxt[z][1])):nxt[z]=v
                # Keep exact observed target and old partial trajectories,
                # plus low-cost states. No absence inference from pruning.
                states=dict(sorted(nxt.items(),key=lambda z:(z[1][0],len(z[1][1])))[:width])
                if goal in nxt:states[goal]=nxt[goal]
            if goal in states:
                alt=states[goal][1]
                def cost(seq):
                    t=start;n=0
                    for x in seq:n+=(len(C.original_path(t,x))+1)//2;t=splay(t,x)
                    return n
                if (cost(alt),len(alt))<(cost(best),len(best)):best=alt
        assert run(start,best)==goal
        # Values are a subsequence, retain only corresponding old positions.
        pos=a
        for x in best:
            while word[pos]!=('D',x):pos+=1
            new.append((pos,word[pos]));pos+=1
        report.append({'old_positions':[a+1,b],'old_length':len(oldkeys),'new_length':len(best),'new_word':best})
        cursor=b
    new.extend((i,word[i]) for i in range(cursor,len(word)));newword=[z for _,z in new]
    rows,end=C.replay(*initial,newword);assert end==initial
    old_to_new={old+573:i+573 for i,(old,z) in enumerate(new)}
    tags={k:old_to_new[v] for k,v in c['tags'].items()}
    for r in rows:r['occurrence']+=572
    for r in rows:
        if r['mode']=='K':
            old=next(old for old,z in new if old_to_new[old+573]==r['occurrence'])
            assert r['after'][0]==fr(rr[old]['after'][0]) and r['A_path']==rr[old]['A_path']
    v,profile,cp,tr=C.selection(rows);at_e=[z for z in tr if z['birth'][0]==tags['e']]
    # Complete valid source data are preserved even if the full conjunction
    # fails. Additional selected arrivals must not silently be excluded.
    guards=len(at_e)==2 and {z['key'] for z in at_e}=={5,9}
    aux=[]
    for r in rows:
        mode='D' if r['mode']=='K' and r['target']==11 else r['mode'];bb,aa=r['before'],r['after']
        aux.append(dict(r,mode=mode,genuine_F=mode=='K' and bb[2][0]!=r['target'],qF=r['qE'],qE=0,
                        before=(bb[0],bb[2],bb[2]),after=(aa[0],aa[2],aa[2])))
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
    from cd6_allocator import allocate
    from branch_funding import build
    small=allocate(aux);raw=build([dict(r,occurrence=i+1) for i,r in enumerate(aux)]);f6=small['f']
    assert f6[(tags['e'],4)]==(tags['v'],1,1)
    mm=C.L.macros(rows);mreport=[{'end':m['occurrences'][-1],'H':m['H'],'Q':m['Q'],
        'clean':all(r['mode']=='D' for r in m['rows'][:-1])} for m in mm]
    old_cost=sum(r['a'] for r in rr);new_cost=sum(r['a'] for r in rows)
    out('shortened_source_control.json',{'status':'SEPARATE_REACHABLE_CLOSED_SOURCE_CONTROL_NOT_W199_MUTATION',
        'source_id':'C28-shortened-01','original_reaching_prefix':c['reaching_prefix'],'initial':initial,'period':newword,
        'rows':rows,'tags':tags,'selected_at_e':at_e,'two_arrival_guard':guards,'creator_pairs':cp,
        'selected_transports':tr,'f6':[{'demand':d,'unit':u} for d,u in sorted(f6.items())],
        'raw_cut':raw['full_cut_before_packet'],'raw_working':raw['working_units'],'raw_max_debt':raw['max_debt_on_period'],
        'macros':mreport,'old_A':old_cost,'new_A':new_cost,'old_length':199,'new_length':len(newword),
        'DELETE_blocks':report,'all_KEEP_A_states_and_paths_preserved':True,
        'search_scope':'greedy plus bounded subsequence beam; no universal/minimum proof',
        'strong_full_guard_status':'requires new full owner/working receipt; do not promote from geometry alone'})
    print(json.dumps({'status':'SHORTENED_SEPARATE_SOURCE','length':len(newword),'A':new_cost,'QF':sum(r['qF'] for r in rows),
        'two_arrivals':guards,'max_clean_H':max(m['H'] for m in mreport if m['clean']),
        'critical_preparations':[(k,next(m['H'] for m in mreport if m['end']==tags[k])) for k in ('gap1','gap7','j')],
        'queries':C.queries,'candidate_not_universal_theorem':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_compress_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries})
