"""Adaptive-domain diagnostics using the unchanged EXP-01 physical engine."""
from __future__ import annotations
from pathlib import Path
import sys,json,time,ctypes,hashlib
from collections import Counter

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/"EXP01_PHYSICAL_RESIDUAL_DISCOVERY"
REPO=ROOT.parent.parent
sys.path.insert(0,str(OLD))
from exp01_oracle import Replay,Tree,closure,digest
from exp01_diagnostics import return_zig_reduction,normalized_certificate


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def memory():
    class Counters(ctypes.Structure):
        _fields_=[("cb",ctypes.c_ulong),("PageFaultCount",ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in (
            "PeakWorkingSetSize","WorkingSetSize","QuotaPeakPagedPoolUsage","QuotaPagedPoolUsage",
            "QuotaPeakNonPagedPoolUsage","QuotaNonPagedPoolUsage","PagefileUsage","PeakPagefileUsage")]
    c=Counters();c.cb=ctypes.sizeof(c)
    kernel=ctypes.windll.kernel32;psapi=ctypes.windll.psapi
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(Counters),ctypes.c_ulong]
    psapi.GetProcessMemoryInfo.restype=ctypes.c_int
    assert psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(c),c.cb),"GetProcessMemoryInfo failed"
    return {"peak_working_set_bytes":c.PeakWorkingSetSize,"working_set_bytes":c.WorkingSetSize,"peak_pagefile_bytes":c.PeakPagefileUsage}


def orientation(r):
    if not r.S:
        return 1
    return 1 if 2*sorted(r.S).index(r.source["initial_B"]["root"])<len(r.S) else -1


def residual(r):
    d=orientation(r)
    ret=return_zig_reduction(r,d)
    covered={digest(p) for p in ret["covered_R6"]}
    other=[p for p in r.pairs if p["class"]=="R6" and digest(p["rho"]) not in covered]
    return d,ret,other


def blocks(r):
    keeps=[b for b in r.boundaries if b["tag"]=="K"]
    if not keeps:
        return []
    cut=next((i for i,k in enumerate(keeps) if k["x"]!=keeps[i-1]["x"]),0)
    keeps=keeps[cut:]+keeps[:cut]
    ans=[]
    for row in keeps:
        if not ans or ans[-1]["x"]!=row["x"]:
            ans.append({"x":row["x"],"ts":[]})
        ans[-1]["ts"].append(row["t"])
    return ans


def domain_window(r,bs,start,direction,limit):
    """All original KEEP blocks are retained, including root repeats.
    Return the longest eligible monotone prefix from this actual boundary.
    The union of initial physical paths is fixed separately for each tested
    candidate; accepted windows later fix one such domain for their full life.
    """
    K=len(bs)
    anchor=bs[start%K]
    tree=Tree(r.boundaries[anchor["ts"][0]-1]["pre_B"])
    targets=[];J=set();chosen=None;failures=[]
    for delta in range(min(limit,K)):
        block=bs[(start+delta)%K]
        x=block["x"]
        if targets and (x-targets[-1])*direction<=0:
            failures.append("rank_order_interruption");break
        targets.append(x);J.update(tree.path(x))
        ordered=sorted(J,reverse=direction<0)
        if ordered[0]!=targets[0]:
            failures.append("not_domain_extreme");break
        if ordered[:len(targets)]!=targets:
            failures.append("not_consecutive_domain_ranks");break
        threshold=(len(J)+1)//2+1
        if len(J)>=2 and len(targets)>=threshold:
            ts=[t for j in range(delta+1) for t in bs[(start+j)%K]["ts"]]
            chosen={"start_block":start%K,"block_length":delta+1,"direction":direction,
                "anchor":anchor["ts"][0],"operations":ts,"targets":list(targets),"J":sorted(J),
                "domain_size":len(J),"ell":len(targets),"threshold":threshold,
                "initial_B":tree.state(),"initial_paths":{str(y):tree.path(y) for y in targets}}
    if chosen is None and not failures:
        failures.append("insufficient_scan_length")
    return chosen,failures


def A_gap(r,previous,current):
    lo=r.boundaries[previous-1]["post_A_time"]
    hi=r.boundaries[current-1]["post_A_time"]+(r.T if current<=previous else 0)
    candidates=[]
    for e in r.events:
        if e["actor"]!="A" or e["id"][3]!=0:
            continue
        t=e["time"]+(r.T if e["time"]<=lo else 0)
        if t<=hi:
            candidates.append((t,e))
    assert candidates,(previous,current)
    return min(candidates,key=lambda x:x[0])[1]["id"]


def verify_window(r,window):
    J=set(window["J"]);tree=Tree(window["initial_B"])
    assert closure(tree,J)==J
    outside={k:list(tree.ch[k]) for k in r.keys if k not in J}
    ids=[];q=0
    for t in window["operations"]:
        row=r.boundaries[t-1]
        assert tree.state()==row["pre_B"]
        assert set(row["B_path"])<=J
        for e in r.events[row["post_A_time"]:row["end_time"]]:
            assert e["actor"]=="B" and e["pivot"] in J and e["promoted"] in J
            assert e["external"] is None or e["external"] in J
            tree.rotate(e["pivot"],e["side"])
            assert all(tree.par[k] is None or tree.par[k] in J for k in J)
            assert all(tree.ch[k]==v for k,v in outside.items())
            ids.append(e["id"])
        assert tree.state()==row["post_B"]
        q+=row["q"]
    assert window["domain_size"]<=2*(window["ell"]-1)
    window.update(physical_path_isolation=True,complete_outside_components_preserved=True,
        actual_Q_B=q,primitive_B_ids=ids,ending_B=tree.state())
    return window


def adaptive(r):
    bs=blocks(r);K=len(bs)
    if not K:
        return {"windows":[],"covered_consumers":[],"E_J":0,"A_gap_witnesses":[],"rejections":[]}
    options={};reject={}
    for i in range(K):
        choices=[];why=[]
        for direction in (1,-1):
            choice,reasons=domain_window(r,bs,i,direction,K)
            if choice:
                choices.append(choice)
            why.extend(reasons)
        if choices:
            options[i]=max(choices,key=lambda w:(w["block_length"],w["direction"]))
        reject[i]=sorted(set(why))
    if not options:
        return {"windows":[],"covered_consumers":[],"E_J":0,"A_gap_witnesses":[],
            "rejections":[{"block":i,"operations":b["ts"],"reasons":reject[i]} for i,b in enumerate(bs)],
            "all_candidate_coverable_consumers":[]}
    pivot=min(options)
    i=pivot;end=pivot+K
    windows=[];rejections=[];allslots=set();covered=set()
    while i<end:
        choices=[]
        for direction in (1,-1):
            w,_=domain_window(r,bs,i,direction,end-i)
            if w:
                choices.append(w)
        if not choices:
            rejections.append({"block":i%K,"operations":bs[i%K]["ts"],"reasons":reject[i%K] or ["cyclic_selection_boundary"]})
            i+=1;continue
        w=max(choices,key=lambda z:(z["block_length"],z["direction"]))
        verify_window(r,w)
        ws=[]
        for j in range(w["block_length"]-1):
            a,b=bs[(i+j)%K],bs[(i+j+1)%K]
            event=A_gap(r,a["ts"][-1],b["ts"][0])
            slot=tuple(event[1:3]);assert slot not in allslots
            allslots.add(slot);ws.append(event)
        w["original_A_gap_witnesses"]=ws
        assert not covered.intersection(w["operations"])
        covered.update(w["operations"]);windows.append(w)
        i+=w["block_length"]
    E=sum(w["domain_size"] for w in windows)
    assert E<=2*len(allslots)<=2*r.A
    return {"selection":"earliest eligible cyclic block, longest eligible direction/prefix, then advance past entire window; one lap",
        "pivot_block":pivot,"windows":windows,"covered_consumers":sorted(covered),"E_J":E,
        "A_gap_witnesses":[list(s) for s in sorted(allslots)],"A_gap_load":1,
        "rejections":rejections,"all_candidate_coverable_consumers":sorted({t for w in options.values() for t in w["operations"]})}


def snapshot(r,time):
    time%=r.T
    return {"time_mod_period":time,"A":r.state_after("A",time).state(),"B":r.state_after("B",time).state()}


def event_inventory(r,p,ret,adapt):
    h=p["rho"][0]
    endpoints=[r.U[tuple(p["rho"][j])] for j in (1,2)]
    parent=r.U[tuple(p["parent"])]
    times={d["nu"]%r.T for d in endpoints+[parent]}
    times.update((r.boundaries[h-1]["post_A_time"],r.boundaries[h-1]["end_time"],
        r.boundaries[parent["h"]-1]["post_A_time"],r.boundaries[parent["h"]-1]["end_time"]))
    original_S=[w for w in r.windows_S if h in w["operations"]]
    original_I=[w for w in r.windows_I if h in w["operations"]]
    bs=blocks(r)
    bi=next(i for i,b in enumerate(bs) if h in b["ts"])
    nextblock=bs[(bi+1)%len(bs)]
    failures=[]
    if original_S and all(not w["eligible"] for w in original_S):failures.append("D5_insufficient_length")
    if not original_S:failures.append("D5_anchor_or_rank_requirement")
    if original_I and all(not w["eligible"] for w in original_I):
        if any(w["length"]<w["threshold"] for w in original_I):failures.append("D6_insufficient_length")
        if any(not w["isolated"] for w in original_I):failures.append("D6_physical_domain_failure")
    if not original_I:failures.append("D6_anchor_barrier_or_rank_requirement")
    if h not in adapt["all_candidate_coverable_consumers"]:failures.append("no_eligible_adaptive_candidate")
    elif h not in adapt["covered_consumers"]:failures.append("adaptive_selection_overlap_or_seam_rejection")
    else:failures.append("adaptive_covered")
    fragments=[]
    for direction in (1,-1):
        start=bi
        for _ in range(len(bs)-1):
            previous=(start-1)%len(bs)
            if (bs[start]["x"]-bs[previous]["x"])*direction<=0:break
            start=previous
        chosen=[]
        for delta in range(len(bs)):
            block=bs[(start+delta)%len(bs)]
            if chosen and (block["x"]-chosen[-1]["x"])*direction<=0:break
            chosen.append(block)
        ts=[t for b in chosen for t in b["ts"]]
        tree=Tree(r.boundaries[ts[0]-1]["pre_B"])
        targets=[b["x"] for b in chosen]
        J=sorted(closure(tree,targets));ordered=sorted(J,reverse=direction<0)
        fragments.append({"direction":direction,"operations":ts,"targets":targets,"J":J,
            "domain_size":len(J),"ell":len(targets),"threshold":(len(J)+1)//2+1,
            "extreme_anchored":ordered[0]==targets[0],"consecutive_J_ranks":ordered[:len(targets)]==targets,
            "long":len(targets)>=(len(J)+1)//2+1})
    taxonomy="adaptive_covered" if h in adapt["covered_consumers"] else "eligible_but_selection_rejected" if h in adapt["all_candidate_coverable_consumers"] else "no_eligible_adaptive_candidate"
    return {**p,"diagnostics":failures,"taxonomy":taxonomy,"maximal_monotone_fragments_through_consumer":fragments,
        "endpoint_certificates":endpoints,"parent_certificate":parent,
        "full_first_hit_cohort":r.cohorts[h],"full_receiver_cohort":r.cohorts[parent["h"]],
        "consuming_A_path":r.boundaries[h-1]["A_path"],"consuming_B_path":r.boundaries[h-1]["B_path"],
        "snapshots":[snapshot(r,t) for t in sorted(times)],
        "D5_windows_through_consumer":original_S,"D6_windows_through_consumer":original_I,
        "return_normalization_failure":{"selected_orientation":ret["direction"],"consumer_in_no_eligible_skeleton_window":True,
            "eligible_window_anchors":[w["anchor"] for w in ret["eligible_windows"]],
            "erased_return_pairs":ret["erased"]},
        "following_KEEP_block":{"target":nextblock["x"],"operations":nextblock["ts"]},
        "original_A_root_entry_resources_not_payments":[],
        "source_costs":{"A":r.A,"Q_B":r.Q},"adaptive_covered":h in adapt["covered_consumers"]}
