"""Check the exact new proof witnesses, including full cyclic Pi snapshots."""
from pathlib import Path
import sys,time,json
from collections import defaultdict
START=time.process_time();ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/"EXP01_PHYSICAL_RESIDUAL_DISCOVERY"))
from exp01_oracle import Tree,Replay,digest
def dump(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
receipt=json.loads((ROOT/"RESOURCE_RECEIPT.json").read_text())
result={};failure=None
try:
    src=json.loads((ROOT/"source_069.json").read_text());r=Replay(src,independent=True)
    assert (r.A,r.Q,r.counts["R6"],len(r.ops))==(298,120,1,224)
    p=next(p for p in r.pairs if p["class"]=="R6")
    assert p["rho"]==[86,[72,3],[83,1]] and p["beta"]==["B",86,2,0]
    required={tuple(p["rho"][1]),tuple(p["rho"][2]),tuple(p["parent"])}
    parent=r.U[tuple(p["parent"])]
    required.update(r.cohorts[parent["h"]])
    a=Tree(src["initial_A"]);snaps=[set(a.labels(r.bits).values())-{0}]
    rel={(14,11):[14 in a.path(11)[:-1]],(34,11):[34 in a.path(11)[:-1]]}
    for e in r.events:
        if e["actor"]=="A":a.rotate(e["pivot"],e["side"])
        snaps.append(set(a.labels(r.bits).values())-{0})
        for uv,seq in rel.items():seq.append(uv[0] in a.path(uv[1])[:-1])
    checks=[]
    for key in sorted(required):
        d=r.U[key];lo,hi=d["kappa"],d["post_A"]
        assert all(d["F"] not in snaps[t%r.T] for t in range(lo,hi+1))
        eid=lambda t:r.events[(t-1)%r.T]["id"]
        checks.append({"demand":list(key),"F":r.label_keys(d["F"]),"J":r.label_keys(d["J"]),
            "Gamma":eid(d["Gamma"]),"kappa":eid(lo),"post_A_time":hi,
            "all_full_Pi_snapshots_A_absent":True,"first_hit":d["h"]})
    for key in (tuple(p["rho"][1]),tuple(p["rho"][2])):
        d=r.U[key]
        assert all(d["J"] not in snaps[t%r.T] for t in range(d["nu"],d["hit_time"]+1))
    start=r.boundaries[82]["end_time"];stop=r.boundaries[93]["post_A_time"]
    assert all(not seq[t] for seq in rel.values() for t in range(start,stop+1))
    c=json.loads((ROOT/"certificate_069.json").read_text())
    relevant=[q for q in c["tickets"] if q["needed_fragment"] and q["u"] in (14,34) and q["role"]=="F"]
    assert len(relevant)==2 and all(q["B_gain_sign"]==q["B_loss_sign"]==0 for q in relevant)
    result["genuine_R6_witness"]={"name":src["name"],"source":"source_069.json",
        "population":len(r.keys),"operations":len(r.ops),"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"],
        "rho":p,"required_full_Pi_checks":checks,"whole_preparation_window_absent_ancestries":[[14,11],[34,11]],
        "unpaid_tickets":relevant,"complete_consuming_cohort":[list(k) for k in r.cohorts[86]],
        "complete_receiver":[list(k) for k in r.cohorts[parent["h"]]],
        "A_cost_at_consumption":r.boundaries[85]["a"],
        "paired_closed":r.closed,"trace_hash":digest(r.events)}
    dump("GENUINE_R6_COUNTERCONFIGURATION.json",result["genuine_R6_witness"])
    src=json.loads((ROOT/"source_106.json").read_text());r=Replay(src,independent=True)
    V=src["inner_word"];R=src["return_word"];L=len(V)
    assert L==66 and len(R)==245 and src["operations"]==V*2+R
    assert r.S==set(range(1,34))
    assert r.boundaries[L-1]["post_A"]==src["initial_A"] and r.boundaries[L-1]["post_B"]==src["initial_B"]
    assert all(x%2==0 for tag,x in V if tag=="K")
    A_V=sum(b["a"] for b in r.boundaries[:L]);Q_V=sum(b["q"] for b in r.boundaries[:L])
    assert (A_V,Q_V,r.A-2*A_V,r.Q-2*Q_V)==(157,28,513,113)
    a=Tree(src["initial_A"]);last=False;losses=[];gains=[]
    assert 17 not in a.path(12)[:-1]
    for e in r.events:
        if e["actor"]=="A":
            a.rotate(e["pivot"],e["side"])
            now=17 in a.path(12)[:-1]
            if now and not last:gains.append(e["id"])
            if last and not now:losses.append(e["id"])
            last=now
        if e["id"][1]<=2*L:assert not last
    assert gains[0]==["A",2*L+17,2,0] and losses[-1]==["A",2*L+108,1,0]
    for op,j,bit in [(31,1,0),(56,1,0)]:
        assert r.event_by_id["B",op,j,bit]["sign"]==0
    assert 17 in Tree(r.boundaries[55]["pre_B"]).path(12)[:-1]
    previous_keep=max(t for t,(tag,x) in enumerate(V,1) if tag=="K" and t<56)
    gap_start=r.boundaries[previous_keep-1]["end_time"]
    gap_stop=r.boundaries[55]["post_A_time"]
    gap_event=next(e for e in r.events[gap_start:gap_stop] if e["actor"]=="A" and e["id"][3]==0)
    assert V[previous_keep-1][1]!=12
    proto={"scope":"Parametric refutation of universal ancestry-bracket charging only, not R6<=cA",
        "diagonal_initial":src["diagonal_initial"],"reaching_prefix":src["reaching_prefix"],
        "initial_A":src["initial_A"],"initial_B":src["initial_B"],"V":V,"R":R,
        "V_length":66,"R_length":245,"V_is_complete_pair_return":True,
        "A_17_ancestor_12_absent_at_every_V_snapshot":True,
        "A_V":157,"Q_V":28,"A_R":513,"Q_R":113,
        "D_B_V":sum(e["actor"]=="B" and e["sign"]==-1 and e["id"][1]<=L for e in r.events),
        "actual_other_A_gap_payment":{"preceding_KEEP":previous_keep,"consuming_KEEP":56,
            "event":gap_event["id"],"target":gap_event["target"],
            "multiplicity_on_this_m_ticket_set":1,"changes_17_ancestor_12":False},
        "for_all_integer_m_ge_1":{"source_word":"V^m R","A":"157m+513","Q_B":"28m+113",
            "ticket":"P, u=17, v=12, operation 66i+56 for i=0,...,m-1",
            "actual_neutral_B_gain":["B","66i+31",1,0],"actual_neutral_B_loss":["B","66i+56",1,0],
            "shared_original_A_loss":["A","66m+108",1,0],"shared_original_A_restoration":["A","66m+17",2,0],
            "minimum_unweighted_congestion_on_two_bracket_events":"m/2",
            "minimum_P_weight_congestion_on_two_bracket_events":"m/4"},
        "sampled_R6":{"m2":0,"m4":0,"m8":0},"trace_hash_m2":digest(r.events)}
    dump("PERIODIC_BRACKET_COUNTEREXAMPLE.json",proto);result["parametric_bracket"]=proto
    result["status"]="FINITE-EXACT witnesses plus induction on an exactly returning block; universal R6 target OPEN"
except BaseException:
    import traceback
    failure=traceback.format_exc();result["failure"]=failure
finally:
    cpu=time.process_time()-START
    receipt["runs"].append({"phase":"verify_new_witnesses","process_CPU_seconds":cpu,"sources":0,"operations":0,"failure":failure})
    receipt["total_process_CPU_seconds"]+=cpu
    dump("RESOURCE_RECEIPT.json",receipt);dump("WITNESS_VERIFICATION.json",result)
    assert receipt["total_process_CPU_seconds"]<=180
if failure:
    print(failure);sys.exit(1)
print(json.dumps({"status":result["status"],"R6_full_Pi_demands_checked":len(result["genuine_R6_witness"]["required_full_Pi_checks"]),
                  "process_CPU_seconds":cpu,"recorded_total_CPU_seconds":receipt["total_process_CPU_seconds"]}))

