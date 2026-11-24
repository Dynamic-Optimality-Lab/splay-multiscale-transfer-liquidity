from collections import Counter,defaultdict
from exp01_oracle import Tree,closure,digest


def incidence(r, classes):
    """Only physically necessary A root entries; no temporal-only edges."""
    demands=[]
    adjacency={}
    for p in r.pairs:
        if p["class"] not in classes:
            continue
        key=str(p["rho"])
        d=r.U[tuple(p["rho"][2])]
        lo,hi=d["nu"],d["hit_time"]
        candidates=set()
        for ev in r.events:
            if ev["actor"]!="A" or ev["external"] is not None:
                continue
            time=ev["time"]
            if time<=lo:
                time+=r.T
            if time<=hi and r.bits.get(ev["promoted"],0)&d["J"] and not r.bits.get(ev["pivot"],0)&d["J"]:
                candidates.add(tuple(ev["id"][1:3]))
        assert candidates,(r.source["name"],p)
        demands.append(key)
        adjacency[key]=candidates
    matched={}
    def augment(d,seen):
        for v in sorted(adjacency[d]):
            if v in seen:
                continue
            seen.add(v)
            if v not in matched or augment(matched[v],seen):
                matched[v]=d
                return True
        return False
    for d in demands:
        augment(d,set())
    assigned=set(matched.values())
    left=set(demands)-assigned
    right=set()
    todo=list(left)
    while todo:
        d=todo.pop()
        for v in adjacency[d]:
            if v not in right:
                right.add(v)
                if v in matched and matched[v] not in left:
                    left.add(matched[v]);todo.append(matched[v])
    firstloads=Counter(min(vs) for vs in adjacency.values())
    return {"demand_count":len(demands),"resource_count":len(set().union(*adjacency.values())) if adjacency else 0,
        "matching_size_capacity_one":len(matched),"deficiency":len(demands)-len(matched),
        "max_lexicographic_entry_StepEv_load":max(firstloads.values(),default=0),
        "hall_witness":{ "left":sorted(left),"right":[list(v) for v in sorted(right)],
            "deficiency":len(left)-len(right)},
        "edges":{k:[list(v) for v in sorted(vs)] for k,vs in adjacency.items()},
        "physical_reason":"A starts shared life rooted outside outer J and ends inside inner J; each edge is an actual outside-to-inside global-root rotation in that life. A StepEv is one resource."}


def physical_diagnostics(r):
    a,b=Tree(r.source["initial_A"]),Tree(r.source["initial_B"])
    def isolated(tree):
        return all(tree.par[k] is None or tree.par[k] in r.I for k in r.I)
    prev_isolated = isolated(b)
    changes=[]
    exterior=[]
    outside_bits=0
    recreated_without_A=0
    last_deleted={}
    a_serial=0
    for ev in r.events:
        tree=a if ev["actor"]=="A" else b
        old_edges=tree.edges()
        tree.rotate(ev["pivot"],ev["side"])
        new_edges=tree.edges()
        assert old_edges-new_edges==set(map(tuple,ev["deleted"]))
        assert new_edges-old_edges==set(map(tuple,ev["added"]))
        if ev["actor"]=="A":
            a_serial+=1
        else:
            outside_bits+=int(ev["pivot"] not in r.I or ev["promoted"] not in r.I)
            now=isolated(b)
            if now!=prev_isolated:
                changes.append({"id":ev["id"],"ancestor_closed_after":now})
            prev_isolated=now
            for edge in map(tuple,ev["deleted"]):
                last_deleted[edge]=(a_serial,ev["id"])
            for edge in map(tuple,ev["added"]):
                if edge in last_deleted and last_deleted[edge][0]==a_serial:
                    recreated_without_A+=1
    for p in r.pairs:
        if p["class"]!="R6":
            continue
        h=p["rho"][0]
        state=Tree(r.boundaries[h-1]["pre_B"])
        outer=r.U[tuple(p["rho"][2])]["g"]
        ancestors=state.path(outer)[:-1]
        exterior.append({"rho":p["rho"],"physical_exterior_ancestors":ancestors,
            "outside_fixed_I":[k for k in ancestors if k not in r.I],
            "frontier_size":len(ancestors),"A_work_at_consumption":r.boundaries[h-1]["a"]})
    return {"fixed_I_ancestor_closure_changes":changes,"fixed_I_closure_change_count":len(changes),
        "outside_I_B_real_bits":outside_bits,"physical_edge_recreations_without_A":recreated_without_A,
        "R6_frontiers":exterior,"root_entry_incidence_R6":incidence(r,{"R6"}),
        "root_entry_incidence_all_blind":incidence(r,{"R_sep","R_dec","R_mix","R_out","T","R_scan","R_fringe","R6"})}


def return_zig_reduction(r,direction=1):
    """Comparison only: greedily erase actual inverse zig pairs.
    Every erased pair is a complete B identity with zero doubles. DELETEs
    remain in W; their costs are never subtracted from A. Direction selects
    downward spurs during an increasing scan, or the reflected rule.
    """
    keep=[b for b in r.boundaries if b["tag"]=="K"]
    stack=[]
    erased=[]
    for b in keep:
        if stack:
            p=stack[-1]
            if len(p["B_path"])==len(b["B_path"])==2 and (b["x"]-p["x"])*direction>0 and p["pre_B"]==b["post_B"]:
                stack.pop()
                erased.append({"operations":[p["t"],b["t"]],"physical_B_identity":True,
                    "Q_B":0,"A":p["a"]+b["a"],"state_hash":digest(p["pre_B"])})
                continue
        stack.append(b)
    # Maximal consecutive S rank windows in the comparison word.
    domain=sorted(r.S)
    if len(domain)<2:
        return {"direction":direction,"erased":erased,"eligible_windows":[],"covered_R6":[]}
    rank={k:i for i,k in enumerate(domain)}
    eligible=[]
    covered=set()
    i=0
    while i<len(stack):
        anchor=domain[0] if direction==1 else domain[-1]
        if stack[i]["x"]!=anchor:
            i+=1;continue
        j=i+1
        distinct=1
        last=stack[i]["x"]
        while j<len(stack):
            x=stack[j]["x"]
            if x==last:
                j+=1;continue
            if rank[x]!=rank[last]+direction:
                break
            distinct+=1;last=x;j+=1
        if distinct>=(len(domain)+1)//2+1:
            ts=[b["t"] for b in stack[i:j]]
            eligible.append({"anchor":stack[i]["t"],"length":distinct,"operations":ts})
            covered.update(ts)
        i=max(i+1,j)
    return {"direction":direction,"erased":erased,"eligible_windows":eligible,
        "covered_R6":[p["rho"] for p in r.pairs if p["class"]=="R6" and p["rho"][0] in covered]}


def lifecycle(r):
    rho=[132,[72,3],[80,1]]
    p=next(p for p in r.pairs if p["rho"]==rho)
    demanded=[(72,3),(80,1),(132,2),(66,13),(68,6)]
    ledger=[]
    for key in demanded:
        d=r.U[key]
        ledger.append({k:(r.label_keys(v) if k in ("F","J") else v) for k,v in d.items()})
    snapshots=[]
    times=sorted(set([r.U[k]["nu"] for k in demanded]+[r.U[k]["post_A"] for k in demanded]+[
        r.boundaries[t-1]["post_A_time"] for t in (129,130,131,132,139,140,160,161,162,170,193,226,290)]))
    for time in times:
        a,b=r.state_after("A",time),r.state_after("B",time)
        roots=(10,18)
        snapshots.append({"time":time,"at_event":r.events[time-1]["id"] if time else None,
            "A":a.state(),"B":b.state(),
            "A_paths_to_old_roots":{str(k):a.path(k) for k in roots},
            "B_paths_to_old_roots":{str(k):b.path(k) for k in roots},
            "common_physical_edges":sorted(a.edges()&b.edges()),
            "A_only_edges":sorted(a.edges()-b.edges()),"B_only_edges":sorted(b.edges()-a.edges())})
    witness_events=[e for e in r.events if e["id"][0]=="B" and e["id"][1] in (72,80,132,140,161)]
    close=sum(b["a"] for b in r.boundaries[161:226])
    return {"rho":rho,"pair":p,"demand_ledger":ledger,"snapshots":snapshots,
        "complete_cohorts":{str(k):v for k,v in r.cohorts.items()},"complete_pairs":r.pairs,
        "all_U_int_records":list(r.U.values()),
        "physical_events_at_births_hits_reset":witness_events,
        "complete_operation_boundaries":r.boundaries,"complete_primitive_events":r.events,
        "costs":{"preparation":64,"descent":64,"short_scan":30,"reset":15,
            "closing_increasing":close,"closing_reverse":64,"A_total":r.A,"Q_B":r.Q},
        "reset_existing_accounting":{"A_real_bits":30,"A_positive_bits":sum(e["sign"]==1 for e in r.events if e["actor"]=="A" and e["id"][1]==161),
            "B_decreasing_bits":sum(e["sign"]==-1 for e in r.events if e["actor"]=="B" and e["id"][1]==161),
            "owner_status":"not audited or changed; P_A/D_B membership is not unused capacity"}}


def normalized_certificate(r,reduction):
    """Independently check the theorem's original-A interval budget.
    No value of the external C_seq is estimated or required by this audit.
    """
    erased=set(t for p in reduction["erased"] for t in p["operations"])
    for p in reduction["erased"]:
        lo,hi=p["operations"]
        assert sum(b["q"] for b in r.boundaries[lo-1:hi])==0
        assert r.boundaries[lo-1]["pre_B"]==r.boundaries[hi-1]["post_B"]
    b=Tree(r.source["initial_B"])
    for original in r.boundaries:
        if original["tag"]!="K" or original["t"] in erased:
            continue
        assert b.state()==original["pre_B"]
        r.plain_splay(b,original["x"])
        assert b.state()==original["post_B"]
    slots=set();windows=[];operations=set()
    for window in reduction["eligible_windows"]:
        ts=window["operations"]
        assert all(t not in erased for t in ts)
        blocks=[]
        for t in ts:
            row=r.boundaries[t-1]
            if not blocks or blocks[-1]["x"]!=row["x"]:
                blocks.append({"x":row["x"],"ts":[]})
            blocks[-1]["ts"].append(t)
        assert len(blocks)==window["length"]
        selected=[]
        for a,b in zip(blocks,blocks[1:]):
            lo=r.boundaries[a["ts"][-1]-1]["post_A_time"]
            hi=r.boundaries[b["ts"][0]-1]["post_A_time"]
            event=next(e for e in r.events[lo:hi] if e["actor"]=="A" and e["id"][3]==0)
            slot=tuple(event["id"][1:3])
            assert slot not in slots,"duplicated original A budget"
            slots.add(slot);selected.append(list(slot))
        assert len(r.S)<=2*(len(blocks)-1)
        Q=sum(r.boundaries[t-1]["q"] for t in ts)
        actual_Q=sum(r.boundaries[t-1]["q"] for t in range(ts[0],ts[-1]+1))
        assert Q==actual_Q
        assert not operations.intersection(ts)
        operations.update(ts)
        windows.append({"anchor":ts[0],"skeleton_length":len(blocks),"operand_population":len(r.S),
            "actual_Q_B":Q,"original_A_StepEv_budget":selected})
    covered=[p for p in r.pairs if p["class"]=="R6" and p["rho"][0] in operations]
    assert len(covered)<=3*sum(w["actual_Q_B"] for w in windows)
    assert len(slots)<=r.A
    return {"direction":reduction["direction"],"E_return":len(r.S)*len(windows),
        "distinct_original_A_StepEv":len(slots),"covered_R6":len(covered),"windows":windows,
        "B_comparison_verified":True,"global_A_nonduplication_verified":True}
