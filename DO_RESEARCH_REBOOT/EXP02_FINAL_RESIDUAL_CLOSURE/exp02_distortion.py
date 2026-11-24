"""Actual original trajectories versus separately named B scan comparisons."""
from exp02_core import *


def shadow_candidate(r,bs,start,direction,limit):
    K=len(bs);S=sorted(r.S,reverse=direction<0)
    if not S or bs[start%K]["x"]!=S[0]:return None
    retained=[];targets=[];last_offset=0
    for delta in range(min(K,limit)):
        b=bs[(start+delta)%K]
        if len(targets)<len(S) and b["x"]==S[len(targets)]:
            retained.extend(b["ts"]);targets.append(b["x"]);last_offset=delta
        if len(targets)==len(S):break
    if len(targets)<2:return None
    tree=Tree(r.boundaries[retained[0]-1]["pre_B"])
    J=sorted(closure(tree,targets));ordered=sorted(J,reverse=direction<0)
    if ordered[:len(targets)]!=targets or len(targets)<(len(J)+1)//2+1:return None
    all_ts=[t for di in range(last_offset+1) for t in bs[(start+di)%K]["ts"]]
    return {"start_block":start%K,"block_span":last_offset+1,"direction":direction,"operations":all_ts,
        "retained":retained,"omitted":[t for t in all_ts if t not in set(retained)],"targets":targets,
        "ell":len(targets),"J":J,"domain_size":len(J),"initial_B":tree.state()}


def select_shadow_windows(r):
    bs=blocks(r);K=len(bs)
    if not K:return []
    directions=(orientation(r),)
    options={}
    for i in range(K):
        choices=[w for d in directions if (w:=shadow_candidate(r,bs,i,d,K))]
        if choices:options[i]=max(choices,key=lambda w:(w["ell"],w["block_span"],w["direction"]))
    if not options:return []
    start=min(options);i=start;end=start+K;windows=[];used=set();gaps=set()
    while i<end:
        choices=[w for d in directions if (w:=shadow_candidate(r,bs,i,d,end-i))]
        if not choices:i+=1;continue
        w=max(choices,key=lambda z:(z["ell"],z["block_span"],z["direction"]))
        assert not used.intersection(w["operations"]);used.update(w["operations"])
        retained_blocks=[]
        for t in w["retained"]:
            x=r.ops[t-1][1]
            if not retained_blocks or retained_blocks[-1]["x"]!=x:
                retained_blocks.append({"x":x,"ts":[]})
            retained_blocks[-1]["ts"].append(t)
        budget=[]
        for a,b in zip(retained_blocks,retained_blocks[1:]):
            event=A_gap(r,a["ts"][-1],b["ts"][0]);slot=tuple(event[1:3])
            assert slot not in gaps;gaps.add(slot);budget.append(event)
        w["original_A_transition_witnesses"]=budget
        windows.append(w);i+=w["block_span"]
    assert sum(w["domain_size"] for w in windows)<=2*len(gaps)<=2*r.A
    return windows


def operation_span(r,start,end):
    return list(range(start,end+1)) if end>=start else list(range(start,len(r.ops)+1))+list(range(1,end+1))


def analyze_shadow(r,window):
    retained=window["retained"]
    keep_set=set(retained);J=set(window["J"])
    shadow_B=Tree(window["initial_B"])
    independent_shadow=r.as_tuple(shadow_B)
    pool={};accesses=[];omissions=[];gap_returns=[]
    def ref(namespace,state):
        key=digest(state);pool[key]=state
        return {"namespace":namespace,"state_sha256":key}
    def ancestors(tree):
        return {k:tree.path(k)[:-1] for k in r.keys}
    actual_q=shadow_q=0
    for index,t in enumerate(retained):
        row=r.boundaries[t-1];target=row["x"]
        before=shadow_B.state();path=shadow_B.path(target);q=(len(path)-1)//2
        assert set(path)<=J
        Replay.plain_splay(shadow_B,target)
        independent_shadow,ind_events=r.ind.trace(independent_shadow,target)
        assert independent_shadow==r.as_tuple(shadow_B)
        assert sum(e[0]!="ZIG" for e in ind_events)==q
        actual_q+=row["q"];shadow_q+=q
        actual_pre=Tree(row["pre_B"]);shadow_pre=Tree(before)
        actual_edges=actual_pre.edges();shadow_edges=shadow_pre.edges()
        accesses.append({"original_operation":t,"target":target,"actual_q":row["q"],"shadow_q":q,
            "difference":row["q"]-q,"actual_path":row["B_path"],"shadow_path":path,
            "actual_pre":ref("actual_B",row["pre_B"]),"actual_post":ref("actual_B",row["post_B"]),
            "shadow_pre":ref("shadow_B",before),"shadow_post":ref("shadow_B",shadow_B.state()),
            "actual_only_edges":sorted(actual_edges-shadow_edges),"shadow_only_edges":sorted(shadow_edges-actual_edges),
            "actual_A_work":row["a"],"actual_retained_outside_J_path_nodes":[k for k in row["B_path"] if k not in J]})
        if index:
            prev=retained[index-1]
            span=operation_span(r,prev,t)[1:-1]
            omitted_here=[u for u in span if r.ops[u-1][0]=="K" and u not in keep_set]
            if omitted_here:
                pre=r.boundaries[omitted_here[0]-1]["pre_B"]
                post=r.boundaries[omitted_here[-1]-1]["post_B"]
                returns=pre==post
                sync=all(r.boundaries[u-1]["A_path"]==r.boundaries[u-1]["B_path"] for u in omitted_here)
                if sync:assert sum(r.boundaries[u-1]["q"] for u in omitted_here)<=sum(r.boundaries[u-1]["a"] for u in omitted_here)
                gap_returns.append({"previous_retained":prev,"next_retained":t,"omitted_KEEP":omitted_here,
                    "all_original_intervening_operations":span,"complete_B_return":returns,"all_omitted_paths_synchronized":sync,
                    "A_intervening":sum(r.boundaries[u-1]["a"] for u in span),
                    "A_omitted_KEEP":sum(r.boundaries[u-1]["a"] for u in omitted_here),
                    "Q_omitted":sum(r.boundaries[u-1]["q"] for u in omitted_here),
                    "pre":ref("actual_B",pre),"post":ref("actual_B",post)})
    for t in window["omitted"]:
        row=r.boundaries[t-1]
        omissions.append({"operation":t,"target":row["x"],"A":row["a"],"Q_B":row["q"],
            "A_path":row["A_path"],"B_path":row["B_path"],"paths_synchronized":row["A_path"]==row["B_path"],
            "pre_B":ref("actual_B",row["pre_B"]),"post_B":ref("actual_B",row["post_B"]),
            "pre_A":ref("original_A",row["pre_A"]),"post_A":ref("original_A",row["post_A"]),
            "B_primitive_events":r.events[row["post_A_time"]:row["end_time"]]})
    delta=actual_q-shadow_q
    assert delta==sum(a["difference"] for a in accesses)
    sync_return=all(g["complete_B_return"] and g["all_omitted_paths_synchronized"] for g in gap_returns)
    if sync_return:assert delta==0
    continuation=[];closing_delta=0
    for t in operation_span(r,retained[-1],retained[0])[1:-1]:
        row=r.boundaries[t-1]
        if row["tag"]!="K":continue
        before=shadow_B.state();path=shadow_B.path(row["x"]);q=(len(path)-1)//2
        Replay.plain_splay(shadow_B,row["x"])
        independent_shadow,_=r.ind.trace(independent_shadow,row["x"])
        assert independent_shadow==r.as_tuple(shadow_B)
        closing_delta+=row["q"]-q
        continuation.append({"operation":t,"actual_q":row["q"],"shadow_q":q,"difference":row["q"]-q,
            "actual_pre":ref("actual_B",row["pre_B"]),"actual_post":ref("actual_B",row["post_B"]),
            "shadow_pre":ref("shadow_B",before),"shadow_post":ref("shadow_B",shadow_B.state())})
    result={**window,"actual_retained_Q":actual_q,"shadow_retained_Q":shadow_q,"delta":delta,"positive_delta":max(delta,0),
        "omitted_Q":sum(o["Q_B"] for o in omissions),"omitted_A_KEEP":sum(o["A"] for o in omissions),
        "synchronized_return_window":sync_return,"gap_episodes":gap_returns,"retained_accesses":accesses,
        "omitted_operations":omissions,"state_pool":pool,"shadow_is_original_source":False,
        "closing_continuation":continuation,"closing_delta":closing_delta,
        "signed_retained_plus_closing_delta":delta+closing_delta,
        "shadow_B_closes_after_actual_rest_of_period":shadow_B.state()==window["initial_B"],
        "independent_shadow_accesses":len(retained),"comparison_domain_extreme_and_rank_order_verified":True}
    return result


def source_distortion(r,other,adapt,save=True):
    windows=select_shadow_windows(r)
    detailed=[];summaries=[];retained=set();omitted=set();syncpaid=set();sync_return_covered=set()
    folder=ROOT/"EXP02_TRAJECTORIES"
    if save:folder.mkdir(exist_ok=True)
    for index,w in enumerate(windows):
        z=analyze_shadow(r,w)
        assert not retained.intersection(w["retained"]);retained.update(w["retained"])
        assert not omitted.intersection(w["omitted"]);omitted.update(w["omitted"])
        syncpaid.update(o["operation"] for o in z["omitted_operations"] if o["paths_synchronized"])
        if z["synchronized_return_window"]:sync_return_covered.update(w["operations"])
        file=f"EXP02_TRAJECTORIES/{digest(r.source['name'])[:16]}_{index}.json"
        if save:(ROOT/file).write_text(json.dumps(z,separators=(",",":"),sort_keys=True)+"\n")
        summary={k:v for k,v in z.items() if k not in ("state_pool","retained_accesses","omitted_operations","closing_continuation")}
        summary["physical_trajectory_file"]=file
        summaries.append(summary)
    Acovered=set(adapt["covered_consumers"])
    after=[p for p in other if p["rho"][0] not in Acovered]
    assignment=[]
    for p in after:
        h=p["rho"][0]
        kind="shadow_retained" if h in retained else "synchronized_omitted" if h in syncpaid else "unpaid_omitted" if h in omitted else "outside_shadow_cover"
        assignment.append({"rho":p["rho"],"consumer":h,"category":kind,
            "synchronized_return_paid":h in sync_return_covered})
    counts=Counter(a["category"] for a in assignment)
    assert sum(counts.values())==len(after)
    assert counts["shadow_retained"]<=3*sum(w["actual_retained_Q"] for w in summaries)
    total_synchronized_omitted_A=sum(r.boundaries[t-1]["a"] for t in syncpaid)
    assert counts["synchronized_omitted"]<=3*total_synchronized_omitted_A
    return {"source":r.source["name"],"A":r.A,"Q_B":r.Q,"R6_other":len(other),"after_adaptive":len(after),
        "windows":summaries,"sum_J":sum(w["domain_size"] for w in summaries),
        "sum_positive_delta":sum(w["positive_delta"] for w in summaries),"sum_signed_delta":sum(w["delta"] for w in summaries),
        "counts":dict(counts),"assignments":assignment,"synchronized_return_paid":sum(a["synchronized_return_paid"] for a in assignment),
        "after_both_proved_classes":sum(not a["synchronized_return_paid"] and a["category"]!="synchronized_omitted" for a in assignment),
        "unpaid_omitted_or_uncovered":counts["unpaid_omitted"]+counts["outside_shadow_cover"],
        "independent_shadow_accesses":sum(w["independent_shadow_accesses"] for w in summaries)}
