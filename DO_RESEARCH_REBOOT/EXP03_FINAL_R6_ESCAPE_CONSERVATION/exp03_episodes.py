"""Actual discrepancy components and comparison divergence, with original A IDs."""
from exp03_core import *


def actual_mismatch_episodes(r):
    n=len(r.ops)
    equal=[b["post_A"]==b["post_B"] for b in r.boundaries]
    # Every demoted B output persists for the rest of that one access. If
    # final A=B, every B bit's created label is therefore A-present.
    for row,eq in zip(r.boundaries,equal):
        if eq:assert all(e["sign"]==-1 for e in r.events[row["post_A_time"]:row["end_time"]])
    if not n:return []
    if not any(equal):
        return [{"id":0,"kind":"persistent_no_equality_cut","operations":list(range(1,n+1)),
            "A_StepEv":[e["id"] for e in r.events if e["actor"]=="A" and e["id"][3]==0],"A":r.A,
            "starts_on_common_pair":False,"ends_on_common_pair":False}]
    # If the designated cut is equal, keep it. Otherwise start after the
    # earliest actual post-operation equality, without changing source IDs.
    initial_equal=r.source["initial_A"]==r.source["initial_B"]
    start=0 if initial_equal else next(i+1 for i,v in enumerate(equal) if v)%n
    episodes=[];current=None
    for delta in range(n):
        i=(start+delta)%n;row=r.boundaries[i]
        if current is None:
            if equal[i]:continue
            current={"id":len(episodes),"kind":"between_actual_equal_pairs","operations":[],"starts_on_common_pair":True}
            assert row["pre_A"]==row["pre_B"]
        current["operations"].append(i+1)
        if equal[i]:
            current["ends_on_common_pair"]=True
            episodes.append(current);current=None
    assert current is None
    used=set();budget=0
    for ep in episodes:
        ts=set(ep["operations"]);steps=[e["id"] for e in r.events if e["actor"]=="A" and e["id"][3]==0 and e["id"][1] in ts]
        for e in steps:
            k=tuple(e[1:3]);assert k not in used;used.add(k)
        ep["A_StepEv"]=steps;ep["A"]=len(steps);budget+=len(steps)
        ep["initial_pair"]={"A":r.boundaries[ep["operations"][0]-1]["pre_A"],"B":r.boundaries[ep["operations"][0]-1]["pre_B"]}
        ep["ending_pair"]={"A":r.boundaries[ep["operations"][-1]-1]["post_A"],"B":r.boundaries[ep["operations"][-1]-1]["post_B"]}
    assert budget<=r.A
    return episodes


def comparison_divergence(r,window):
    ts=window["operations"];retained=set(window["retained"]);inside=set(ts)
    start=ts[0];order=list(range(start,len(r.ops)+1))+list(range(1,start))
    shadow=Tree(window["initial_B"]);episodes=[];current=None;boundaries=[]
    for t in order:
        row=r.boundaries[t-1]
        pre_equal=row["pre_B"]==shadow.state()
        if row["tag"]=="K" and (t not in inside or t in retained):Replay.plain_splay(shadow,row["x"])
        post_equal=row["post_B"]==shadow.state()
        if current is None and not post_equal:
            current={"id":len(episodes),"first_divergence_operation":t,"operations":[],"first_divergence_omitted":t in inside and t not in retained}
        if current is not None:
            current["operations"].append(t)
            if post_equal:
                current.update(recovered=True,recovery_operation=t)
                episodes.append(current);current=None
        boundaries.append({"operation":t,"pre_equal":pre_equal,"post_equal":post_equal,
            "original_A":row["a"],"actual_B_hash":digest(row["post_B"]),"comparison_B_hash":digest(shadow.state())})
    if current is not None:
        current.update(recovered=False,recovery_operation=None);episodes.append(current)
    for ep in episodes:
        # Interior A excludes the opening operation's A phase, which occurs
        # BEFORE that operation's B divergence. Incoming KEEP-gap work is separate.
        opening=ep["first_divergence_operation"]
        interior=set(ep["operations"][1:])
        ep["A_during_divergence"]=[e["id"] for e in r.events if e["actor"]=="A" and e["id"][3]==0 and e["id"][1] in interior]
        keeps=[b["t"] for b in r.boundaries if b["tag"]=="K"]
        assert opening in keeps
        previous=keeps[keeps.index(opening)-1]
        gap=list(range(previous+1,opening+1)) if opening>previous else list(range(previous+1,len(r.ops)+1))+list(range(1,opening+1))
        ep["incoming_A_gap"]=[e["id"] for e in r.events if e["actor"]=="A" and e["id"][3]==0 and e["id"][1] in set(gap)]
    return {"initial_operation":start,"window_operations":ts,"retained":window["retained"],"omitted":window["omitted"],
        "episodes":episodes,"all_original_boundaries":boundaries,"comparison_ends_equal":shadow.state()==window["initial_B"]}
