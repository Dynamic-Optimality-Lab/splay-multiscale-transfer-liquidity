"""Full-source ancestry loss/restoration continuation; writes only beside this file."""
from __future__ import annotations
import sys,time,json,hashlib,random,traceback
from pathlib import Path
from collections import defaultdict,Counter
from bisect import bisect_left,bisect_right
START_CPU=time.process_time()
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OLD=ROOT.parent/"EXP01_PHYSICAL_RESIDUAL_DISCOVERY"
sys.path.insert(0,str(OLD))
from exp01_oracle import Tree,Replay,vine,digest
from exp01_sources import H,W,G,detour_H,nested_detour,reflect,cyclic_cut,source

def save(name,data):
    path=ROOT/name
    assert path.parent==ROOT or ROOT in path.parents
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def fragments(r):
    keeps=[(i+1,x) for i,(tag,x) in enumerate(r.ops) if tag=="K"]
    cut=next((i for i in range(len(keeps)) if keeps[i][1]!=keeps[i-1][1]),None)
    if cut is None:return []
    keeps=keeps[cut:]+keeps[:cut]
    blocks=[]
    for t,x in keeps:
        if not blocks or blocks[-1]["x"]!=x:blocks.append({"x":x,"ts":[]})
        blocks[-1]["ts"].append(t)
    rank={x:i for i,x in enumerate(sorted(r.S))}
    n=len(blocks)
    edge=[rank[blocks[(i+1)%n]["x"]]-rank[b["x"]] for i,b in enumerate(blocks)]
    edge=[e if abs(e)==1 else 0 for e in edge]
    run={}
    for i,e in enumerate(edge):
        if not e:continue
        a=i
        while edge[(a-1)%n]==e:
            a=(a-1)%n
            assert a!=i
        run[i]=a
    owner=[("run",run[i]) if i in run else ("run",run[(i-1)%n])
           if (i-1)%n in run else ("single",i) for i in range(n)]
    unmarked=[]
    for b in blocks:
        marks=[t in r.eligible_S for t in b["ts"]]
        assert all(z==marks[0] for z in marks)
        unmarked.append(not marks[0])
    out=[];owned=set()
    for i in range(n):
        if not unmarked[i] or (unmarked[(i-1)%n] and owner[i]==owner[(i-1)%n]):continue
        ids=[];j=i
        while unmarked[j] and owner[j]==owner[i]:
            assert j not in owned
            owned.add(j);ids.append(j);j=(j+1)%n
            assert j!=i
        ts=[t for k in ids for t in blocks[k]["ts"]]
        xs=[blocks[k]["x"] for k in ids]
        direct=1 if len(xs)==1 else (1 if xs[-1]>xs[0] else -1)
        assert all(rank[b]-rank[a]==direct for a,b in zip(xs,xs[1:]))
        prev=blocks[(i-1)%n]["ts"][-1]
        out.append({"index":len(out),"ts":ts,"targets":xs,"direction":direct,
                    "prev":prev,"first":ts[0],"last":ts[-1]})
    assert len(owned)==sum(unmarked)
    assert sum(r.boundaries[t-1]["q"] for f in out for t in f["ts"])==sum(
        b["q"] for b in r.boundaries if b["t"] not in r.eligible_S)
    assert sum(len(f["targets"]) for f in out)<=r.KB<=r.A
    return out

def bracket(events,t,which):
    if not events:return None
    times=[e["time"] for e in events]
    if which=="prev":
        i=bisect_right(times,t)-1
        return events[i] if i>=0 else events[-1]
    i=bisect_right(times,t)
    return events[i] if i<len(events) else events[0]

def after_in(events,start,end,T):
    assert 0<=(end-start)%T<T if T else True
    if end<start:end+=T
    candidates=[(e["time"]+(T if e["time"]<=start else 0),e) for e in events]
    candidates=[(t,e) for t,e in candidates if start<t<=end]
    assert candidates,(start,end,[e["id"] for e in events])
    return min(candidates,key=lambda z:z[0])[1]

def ancestry_audit(r):
    fs=fragments(r); tickets=[]; need=defaultdict(set)
    for f in fs:
        b=Tree(r.boundaries[f["first"]-1]["pre_B"])
        a=Tree(r.boundaries[f["prev"]-1]["post_A"])
        first,last=f["targets"][0],f["targets"][-1]
        paths=[b.path(x) for x in f["targets"]]
        U=set().union(*map(set,paths))
        frontier=sorted(u for u in U if u>last) if f["direction"]==1 else sorted(u for u in U if u<last)
        roles=[("P",first,b.path(first)[:-1]),("F",last,frontier)]
        for role,v,us in roles:
            for u in us:
                assert u in b.path(v)[:-1]
                q={"fragment":f["index"],"role":role,"u":u,"v":v,
                   "A_present_at_window_start":u in a.path(v)[:-1],
                   "first":f["first"],"last":f["last"],"prev":f["prev"]}
                tickets.append(q);need[u].add(v)
    bits={k:1<<i for i,k in enumerate(r.keys)}
    losses={"A":defaultdict(list),"B":defaultdict(list)}
    gains={"A":defaultdict(list),"B":defaultdict(list)}
    trees={"A":Tree(r.source["initial_A"]),"B":Tree(r.source["initial_B"])}
    physical=[]
    for ev in r.events:
        tr=trees[ev["actor"]];g=ev["pivot"];p=ev["promoted"];s=ev["side"]
        before=tr.labels(bits)
        assert tr.ch[g][s]==p
        lost=bits[p]|before.get(tr.ch[p][s],0)
        gained=bits[g]|before.get(tr.ch[g][1-s],0)
        tr.rotate(g,s)
        after=tr.labels(bits)
        assert before[g]&~after[g]==lost and not after[g]&~before[g]
        assert after[p]&~before[p]==gained and not before[p]&~after[p]
        assert all(before[k]==after[k] for k in r.keys if k not in (g,p))
        row={k:ev[k] for k in ("id","time","actor","pivot","promoted","sign","case","target")}
        row.update(lost_wing=[k for k in r.keys if lost&bits[k]],
                   gained_wing=[k for k in r.keys if gained&bits[k]])
        physical.append(row)
        for v in need[g]:
            if lost&bits[v]:losses[ev["actor"]][g,v].append(row)
        for v in need[p]:
            if gained&bits[v]:gains[ev["actor"]][p,v].append(row)
    for actor in ("A","B"):assert trees[actor].state()==r.source["initial_"+actor]
    alpha=Counter();blossload=Counter();prevload=Counter();nextload=Counter();both=Counter()
    absent_forever=[];matched=0
    for q in tickets:
        uv=q["u"],q["v"];f=fs[q["fragment"]]
        start=r.boundaries[f["prev"]-1]["end_time"]
        stop=r.boundaries[(f["first"] if q["role"]=="P" else f["last"])-1]["post_A_time"]
        bstart=r.boundaries[f["first"]-1]["post_A_time"]
        bstop=r.boundaries[(f["first"] if q["role"]=="P" else f["last"])-1]["end_time"]
        b_loss=after_in(losses["B"][uv],bstart,bstop,r.T)
        b_gain=bracket(gains["B"][uv],bstart,"prev")
        assert b_gain is not None
        q["B_loss"]=b_loss["id"];q["B_gain"]=b_gain["id"]
        q["B_gain_sign"]=b_gain["sign"];q["B_loss_sign"]=b_loss["sign"]
        blossload[tuple(b_loss["id"]),q["role"]]+=1
        if q["A_present_at_window_start"]:
            e=after_in(losses["A"][uv],start,stop,r.T)
            q["A_first_loss"]=e["id"]
            alpha[tuple(e["id"]),q["role"]]+=1;matched+=1
        else:
            e=bracket(losses["A"][uv],start,"prev")
            z=bracket(gains["A"][uv],start,"next")
            assert (e is None)==(z is None)
            if e is None:
                q["A_ever_present"]=False;absent_forever.append(q)
            else:
                q["A_ever_present"]=True
                q["A_previous_loss"]=e["id"];q["A_next_restoration"]=z["id"]
                q["A_previous_loss_sign"]=e["sign"];q["A_next_restoration_sign"]=z["sign"]
                prevload[tuple(e["id"])]+=1;nextload[tuple(z["id"])]+=1
                both[tuple(e["id"]),tuple(z["id"])]+=1
    assert max(alpha.values(),default=0)<=1
    assert max(blossload.values(),default=0)<=1
    r6=[p for p in r.pairs if p["class"]=="R6"]
    byop=Counter(p["rho"][0] for p in r6)
    fragrecords=[]
    for f in fs:
        fragrecords.append({**f,"R6":sum(byop[t] for t in f["ts"]),
                            "A_operations":cyclic_operations(f["prev"],f["last"],len(r.ops))})
    selectedloss=max(prevload,key=lambda k:prevload[k],default=None)
    selectedboth=max(both,key=lambda k:both[k],default=None)
    stats={"tickets":len(tickets),"initial_A_matched":matched,"initial_A_absent":len(tickets)-matched,
           "never_A_present":len(absent_forever),"max_previous_A_loss_load":max(prevload.values(),default=0),
           "max_next_A_restoration_load":max(nextload.values(),default=0),
           "max_same_loss_restoration_pair_load":max(both.values(),default=0),
           "neutral_B_regenerations":sum(q["B_gain_sign"]==0 for q in tickets),
           "max_matched_per_role_per_A_bit":max(alpha.values(),default=0),
           "max_all_per_role_per_B_bit":max(blossload.values(),default=0),
           "largest_loss_event":None if selectedloss is None else list(selectedloss),
           "largest_loss_tickets":[q for q in tickets if q.get("A_previous_loss")==list(selectedloss or [])],
           "largest_event_pair":None if selectedboth is None else [list(e) for e in selectedboth]}
    used_r6_ids=set(tuple(p["rho"][1]) for p in r6)|set(tuple(p["rho"][2]) for p in r6)|set(tuple(p["parent"]) for p in r6)
    for p in r6:
        d=r.U[tuple(p["parent"])]
        used_r6_ids.update(r.cohorts[d["h"]])
    cert={"summary":r.summary(),"boundary_stats":stats,"fragments":fragrecords,"tickets":tickets,
          "R6_demand_records":[r.U[k] for k in sorted(used_r6_ids)],
          "all_physical_ancestry_events":physical}
    windowload=Counter()
    for q in tickets:
        f=fs[q["fragment"]]
        start=r.boundaries[f["prev"]-1]["end_time"]
        stop=r.boundaries[(f["first"] if q["role"]=="P" else f["last"])-1]["post_A_time"]
        span=(stop-start)%r.T
        if q["A_present_at_window_start"]:
            q["A_window_loss"]=q["A_first_loss"]
        elif q.get("A_ever_present"):
            restore=r.event_by_id[tuple(q["A_next_restoration"])]["time"]
            offset=(restore-start)%r.T
            if 0<offset<=span:
                q["A_window_loss"]=after_in(losses["A"][q["u"],q["v"]],restore,stop,r.T)["id"]
        if "A_window_loss" in q:
            windowload[tuple(q["A_window_loss"]),q["role"]]+=1
        q["needed_fragment"]=fragrecords[q["fragment"]]["R6"]>0
    assert max(windowload.values(),default=0)<=1
    stats["A_whole_window_absent"]=sum("A_window_loss" not in q for q in tickets)
    stats["R6_fragment_tickets"]=sum(q["needed_fragment"] for q in tickets)
    stats["R6_fragment_unpaid_neutral_loss"]=sum(q["needed_fragment"] and "A_window_loss" not in q and q["B_loss_sign"]==0 for q in tickets)
    return cert

def cyclic_operations(prev,last,n):
    return [((prev+i-1)%n)+1 for i in range(1,((last-prev-1)%n)+2)]

def small_literal():
    ch={"0":[None,1],"1":[None,6],"2":[None,3],"3":[None,None],
        "4":[2,5],"5":[None,None],"6":[4,7],"7":[None,None]}
    return source("literal_14",8,[["D",2],["K",7],["K",1],["K",2]]+
                  [["K",k] for k in range(8)]+[["K",1],["K",0]],{"root":0,"children":ch},family="literal")

def generic(n,seed):
    rng=random.Random(seed)
    word=[["K" if rng.randrange(4)==0 else "D",rng.randrange(1,n+1)] for _ in range(3*n)]
    word += [["K",k] for k in range(1,n+1)]+[["K",k] for k in range(n-1,0,-1)]
    return source(f"generic_n{n}_seed{seed}",n,word,family="generic",seed=seed)

def helper_attack(p,kind,short):
    s=G(p,L=11)
    n=len(s["initial_A"]["children"]);m=n+1-2**p
    mark_index=next(i for i,(tag,x) in enumerate(s["operations"]) if tag=="K" and x==m)
    helpers={"min":[1],"min2":[2,1],"min4":[4,2,1],"zig":[1,2,1],
             "mid":[m//2,1],"split":[11,1]}[kind]
    s["operations"][mark_index:mark_index]=[["D",x] for x in helpers]
    if short:
        # Delete only A occurrences from the unmarked descending tail;
        # B is frozen there. New source IDs and full Pi are recomputed.
        stop=mark_index+len(helpers)+1
        assert s["operations"][stop:stop+m-1]==[["D",x] for x in range(m-1,0,-1)]
        del s["operations"][stop:stop+m-1]
    s.update(name=f"helper_p{p}_{kind}_short{int(short)}",family="helper",p=p,short=short,helper=kind)
    return s

def recurrent(n,seed):
    rng=random.Random(seed)
    initial=vine(range(1,n+1))
    kept=list(range(2,n+1,2));allowed=list(range(1,n+1))
    # One unrequested physical key can remain a genuine Steiner operand.
    omit=n//2
    allowed=[x for x in allowed if x!=omit]
    base=[["K",rng.choice(kept)] if rng.randrange(3)==0 else ["D",rng.choice(allowed)] for _ in range(2*n)]
    a,b=Tree(initial),Tree(initial);seen={}
    for copy in range(40):
        key=digest([a.state(),b.state()])
        if key in seen:
            old,ia,ib=seen[key]
            return {"name":f"recurrent_n{n}_seed{seed}","family":"recurrent",
                    "initial_A":ia,"initial_B":ib,"operations":base*(copy-old),
                    "diagonal_initial":initial,"reaching_prefix":base*old,
                    "reachability":"literal repeated source from common diagonal; complete pair cycle detected"}
        seen[key]=(copy,a.state(),b.state())
        for tag,x in base:
            Replay.plain_splay(a,x)
            if tag=="K":Replay.plain_splay(b,x)
    raise AssertionError("no bounded recurrent pair",n,seed)

def banded(p,width,jmin):
    s=H(p);n=len(s["initial_A"]["children"])
    extra=set()
    for j in range(jmin,p+1):
        x=n+1-2**j
        extra.update(range(x-width,x+1))
    for i in range(n-1,2*n-1):
        tag,x=s["operations"][i]
        if x in extra:s["operations"][i]=["K",x]
    s.update(name=f"banded_p{p}_w{width}_j{jmin}",family="banded",width=width,jmin=jmin)
    return s

def recurrent_lift(n,seed,copies):
    core=recurrent(n,seed)
    return lift_core(core,n,copies)

def lift_core(core,n,copies):
    aa=Tree(core["initial_B"]);prep=[]
    for tag,x in core["reaching_prefix"]:
        Replay.plain_splay(aa,x);prep.append(["D",x])
    for count in range(41):
        if aa.state()==core["initial_A"]:break
        for tag,x in core["operations"]:
            Replay.plain_splay(aa,x);prep.append(["D",x])
    else:raise AssertionError("A preparation construction failed",core["name"])
    reset=[["K",x] for x in range(1,n+1)]+[["K",x] for x in range(n-1,0,-1)]
    bbuild=[["K",x] for tag,x in core["reaching_prefix"] if tag=="K"]
    word=core["operations"]*copies+reset+bbuild+prep
    return {**core,"name":core["name"]+f"_lift_m{copies}","family":"recurrent_lift",
            "operations":word,"inner_word":core["operations"],"inner_copies":copies,
            "return_word":reset+bbuild+prep,"A_preparation_length":len(prep)}

def even_scan_cycle(active,seed):
    n=2*active+1;rng=random.Random(seed);initial=vine(range(1,n+1))
    xs=list(range(2,2*active+1,2))+list(range(2*active-2,1,-2))
    base=[["K" if rng.randrange(3)==0 else "D",x] for x in xs]
    a,b=Tree(initial),Tree(initial);seen={}
    for copy in range(40):
        key=digest([a.state(),b.state()])
        if key in seen:
            old,ia,ib=seen[key]
            return {"name":f"even_scan_a{active}_seed{seed}","family":"even_scan",
                    "initial_A":ia,"initial_B":ib,"operations":base*(copy-old),
                    "diagonal_initial":initial,"reaching_prefix":base*old,
                    "reachability":"literal repeated even-key physical scans from common diagonal"}
        seen[key]=(copy,a.state(),b.state())
        for tag,x in base:
            Replay.plain_splay(a,x)
            if tag=="K":Replay.plain_splay(b,x)
    raise AssertionError("even cycle missing",active,seed)

def sources(phase):
    if phase=="pilot":
        yield small_literal()
        for p in (3,4,5):
            yield G(p,L=11)
            yield detour_H(p,positions=(7,),copies=1)
        for n in (9,17,33):
            for seed in (1,2):yield generic(n,seed)
    elif phase=="even_cycles":
        for seed in range(6):yield even_scan_cycle(32,seed)
    elif phase=="even_lift":
        for seed in range(6):yield lift_core(even_scan_cycle(32,seed),65,3)
    elif phase=="repeat_lift":
        for copies in (2,4,8):yield recurrent_lift(33,12,copies)
    elif phase=="bands":
        for p in (5,6):
            for width in (7,15):yield banded(p,width,4)
    elif phase=="dense":
        for p in (4,5,6):
            n=2**(p+2)+1
            s=detour_H(p,positions=tuple(range(7,n,8)),copies=1)
            yield s
            yield reflect(s)
    elif phase=="attacks":
        for p in (4,5):
            for kind in ("min","min2","min4","zig","mid","split"):
                yield helper_attack(p,kind,True)
        for n in (9,17,33):
            for seed in range(10,16):yield recurrent(n,seed)
    else:
        for p in (4,5,6):
            for L in (11,19,31):
                for copies in (1,2):yield G(p,L=L,r=copies)
            for pos in ((7,),(15,),(7,15,23,31)):
                yield detour_H(p,positions=pos,copies=1)
        for n in (9,17,33,65):
            for seed in range(3,8):yield generic(n,seed)
        for p in (4,5):
            yield reflect(G(p,L=11))
            yield reflect(detour_H(p,positions=(7,),copies=2))
        for depth in (2,3):
            yield nested_detour(depth=depth,tail=0,helpers=False)

def sanity(r,cert):
    name=r.source["name"]
    if name=="literal_14":
        f=next(f for f in cert["fragments"] if f["ts"]==[3,4])
        qs=[q for q in cert["tickets"] if q["fragment"]==f["index"]]
        for u,e in [(6,["A",1,1,0]),(4,["A",1,1,1])]:
            q=next(q for q in qs if q["role"]=="F" and q["u"]==u)
            assert q["A_previous_loss"]==e and not q["A_present_at_window_start"]
        qs=[q for q in qs if q.get("A_first_loss")==["A",3,1,0]]
        assert len(qs)==2 and {q["role"] for q in qs}=={"P","F"}
    p=r.source.get("p")
    if r.source.get("family")=="G" and r.source["L"]==11 and r.source["r"]==1 and p>=4:
        N=len(r.keys);h=2*N+2
        assert sum(q["rho"][0]==h and q["class"]=="R6" for q in r.pairs)>=p-3
        for j in range(3,p):
            astar=2**(j+1)+1
            ev=r.event_by_id["A",4*N+12-astar,1,0]
            assert ev["sign"]==1 and ev["case"]=="ZIG"
        assert r.boundaries[2*N+10]["a"]==5

def main(phase):
    receipt_path=ROOT/"RESOURCE_RECEIPT.json"
    receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else {"runs":[],"total_process_CPU_seconds":0.0,"total_sources":0,"total_operations":0}
    cap=60 if phase=="pilot" else 180-receipt["total_process_CPU_seconds"]
    records=[];failure=None
    try:
        for src in sources(phase):
            if time.process_time()-START_CPU>cap-6:break
            if len(records)>=32 and phase=="pilot":break
            assert len(src["initial_A"]["children"])<=257 and len(src["operations"])<=10000
            r=Replay(src,independent=True)
            if "diagonal_initial" in src:
                a,b=Tree(src["diagonal_initial"]),Tree(src["diagonal_initial"])
                for tag,x in src["reaching_prefix"]:
                    Replay.plain_splay(a,x)
                    if tag=="K":Replay.plain_splay(b,x)
                assert a.state()==src["initial_A"] and b.state()==src["initial_B"]
            cert=ancestry_audit(r);sanity(r,cert)
            i=receipt["total_sources"]+len(records)
            save(f"source_{i:03d}.json",src)
            save(f"certificate_{i:03d}.json",cert)
            short={k:cert["summary"][k] for k in ("name","population","operations","A","Q_B","R6","D_B","independent_operation_checks","trace_hash")}
            short.update({k:v for k,v in cert["boundary_stats"].items() if k not in ("largest_loss_tickets",)})
            short["certificate"]=f"certificate_{i:03d}.json";short["source"]=f"source_{i:03d}.json"
            records.append(short)
            print(json.dumps({k:short[k] for k in ("name","A","Q_B","R6","tickets","initial_A_absent","never_A_present","max_previous_A_loss_load","max_next_A_restoration_load","max_same_loss_restoration_pair_load")}),flush=True)
    except BaseException:
        failure=traceback.format_exc()
        print(failure,flush=True)
    finally:
        cpu=time.process_time()-START_CPU
        receipt["runs"].append({"phase":phase,"process_CPU_seconds":cpu,"sources":len(records),"operations":sum(x["operations"] for x in records),"failure":failure})
        receipt["total_process_CPU_seconds"]+=cpu;receipt["total_sources"]+=len(records);receipt["total_operations"]+=sum(x["operations"] for x in records)
        save("RESOURCE_RECEIPT.json",receipt)
        save("RESULTS_"+phase+".json",{"status":"FINITE-EXACT" if failure is None else "FAILED-STOPPED","records":records,"failure":failure,"resources":receipt})
        assert receipt["total_process_CPU_seconds"]<=180
    if failure:sys.exit(1)


def audit_saved():
    old=json.loads((ROOT/"RESOURCE_RECEIPT.json").read_text())
    rows=[]
    for path in sorted(ROOT.glob("certificate_*.json")):
        c=json.loads(path.read_text());qs=c["tickets"]
        def detail(pred):
            selected=[q for q in qs if pred(q)]
            prev=Counter(tuple(q["A_previous_loss"]) for q in selected if "A_previous_loss" in q)
            nxt=Counter(tuple(q["A_next_restoration"]) for q in selected if "A_next_restoration" in q)
            both=Counter((tuple(q["A_previous_loss"]),tuple(q["A_next_restoration"])) for q in selected if "A_previous_loss" in q)
            bg=Counter(tuple(q["B_gain"]) for q in selected)
            worst=max(prev,key=lambda e:prev[e],default=None)
            return {"count":len(selected),"max_previous_loss":max(prev.values(),default=0),
                    "max_restoration":max(nxt.values(),default=0),"max_same_pair":max(both.values(),default=0),
                    "max_B_gain":max(bg.values(),default=0),
                    "worst_previous_loss":None if worst is None else list(worst),
                    "worst_tickets":[q for q in selected if q.get("A_previous_loss")==list(worst or [])]}
        rows.append({"name":c["summary"]["name"],"R6":c["summary"]["R6"],
                     "all":detail(lambda q:True),
                     "unmatched_neutral_loss":detail(lambda q:not q["A_present_at_window_start"] and q["B_loss_sign"]==0),
                     "unmatched_neutral_gain_loss":detail(lambda q:not q["A_present_at_window_start"] and q["B_loss_sign"]==0 and q["B_gain_sign"]==0)})
    cpu=time.process_time()-START_CPU
    old["runs"].append({"phase":"audit_saved","process_CPU_seconds":cpu,"sources":0,"operations":0,"failure":None})
    old["total_process_CPU_seconds"]+=cpu
    save("RESOURCE_RECEIPT.json",old);save("JOINT_A_B_AUDIT.json",rows)
    for row in rows:
        print(json.dumps({"name":row["name"],"R6":row["R6"],
            **{k:{z:v for z,v in row[k].items() if z!="worst_tickets"} for k in ("unmatched_neutral_loss","unmatched_neutral_gain_loss")}}),flush=True)

if __name__=="__main__":
    phase=sys.argv[1] if len(sys.argv)>1 else "pilot"
    audit_saved() if phase=="audit_saved" else main(phase)

