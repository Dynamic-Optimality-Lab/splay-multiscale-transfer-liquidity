"""Postprocess saved exact certificates; does not replay a source."""
import sys,time,json,hashlib
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
START=time.process_time()
ROOT=Path(__file__).resolve().parent
receipt=json.loads((ROOT/"RESOURCE_RECEIPT.json").read_text())
rows=[];permanent=[];unpaid_examples=[];all_checks=0
for path in sorted(ROOT.glob("certificate_*.json")):
    c=json.loads(path.read_text());s=c["summary"];ev=c["all_physical_ancestry_events"]
    n=s["operations"];byop=defaultdict(list)
    loss=defaultdict(list)
    for e in ev:
        byop[e["id"][1]].append(e)
        if e["actor"]=="A":
            for v in e["lost_wing"]:loss[e["pivot"],v].append(e)
    ends=[0]*(n+1);posta=[0]*(n+1)
    for t in range(1,n+1):
        posta[t]=max([e["time"] for e in byop[t] if e["actor"]=="A"] or [ends[t-1]])
        ends[t]=max([e["time"] for e in byop[t]] or [ends[t-1]])
    T=ends[-1];role_load=Counter();b_load=Counter();prev=Counter();nxt=Counter();pair=Counter()
    fs={f["index"]:f for f in c["fragments"]}
    selected=[]
    stats=Counter()
    for q in c["tickets"]:
        f=fs[q["fragment"]];needed=f["R6"]>0
        start=ends[f["prev"]];stop=posta[f["first"] if q["role"]=="P" else f["last"]]
        if stop<start:stop+=T
        choices=[(e["time"]+(T if e["time"]<=start else 0),e) for e in loss[q["u"],q["v"]]]
        choices=[(t,e) for t,e in choices if start<t<=stop]
        window_loss=min(choices,key=lambda z:z[0])[1]["id"] if choices else None
        if window_loss is not None:role_load[tuple(window_loss),q["role"]]+=1
        if not needed:continue
        stats["needed_tickets"]+=1
        record={**q,"A_window_loss":window_loss,"certificate":path.name,"name":s["name"]}
        if window_loss is not None:
            stats["A_window_paid"]+=1
        elif q["B_loss_sign"]==-1:
            stats["B_decrease_paid"]+=1;b_load[tuple(q["B_loss"]),q["role"]]+=1
        else:
            stats["unpaid_neutral"]+=1;selected.append(record)
            if "A_previous_loss" in q:
                prev[tuple(q["A_previous_loss"])]+=1
                nxt[tuple(q["A_next_restoration"])]+=1
                pair[tuple(q["A_previous_loss"]),tuple(q["A_next_restoration"])]+=1
            else:stats["needed_never_A_present"]+=1
        if q.get("A_ever_present") is False:permanent.append(record)
    assert max(role_load.values(),default=0)<=1 and max(b_load.values(),default=0)<=1
    for q in c["tickets"]:
        if q.get("A_ever_present") is False and not fs[q["fragment"]]["R6"]:
            permanent.append({**q,"certificate":path.name,"name":s["name"],"needed_fragment":False})
    all_checks+=s["independent_operation_checks"]
    rows.append({"name":s["name"],"A":s["A"],"Q_B":s["Q_B"],"R6":s["R6"],
                 "operations":s["operations"],"population":s["population"],**stats,
                 "unpaid_max_A_loss_load":max(prev.values(),default=0),
                 "unpaid_max_A_restoration_load":max(nxt.values(),default=0),
                 "unpaid_max_same_pair_load":max(pair.values(),default=0),
                 "certificate":path.name})
    if selected:unpaid_examples.extend(selected)
max_ratio=max((Fraction(r["R6"],r["A"]) for r in rows if r["A"]),default=Fraction(0))
out={"scope":"FINITE-EXACT saved complete sources only; no universal ratio conclusion",
     "sources":len(rows),"operations":sum(r["operations"] for r in rows),
     "independent_operation_checks":all_checks,"sources_with_R6":sum(r["R6"]>0 for r in rows),
     "R6_total":sum(r["R6"] for r in rows),"max_R6_over_A":{"numerator":max_ratio.numerator,"denominator":max_ratio.denominator},
     "permanently_A_absent_tickets":permanent,"unpaid_needed_tickets":unpaid_examples,"rows":rows}
(ROOT/"GLOBAL_MULTIPLICITY_AUDIT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
cpu=time.process_time()-START
receipt["runs"].append({"phase":"final_saved_global_audit","process_CPU_seconds":cpu,"sources":0,"operations":0,"failure":None})
receipt["total_process_CPU_seconds"]+=cpu
(ROOT/"RESOURCE_RECEIPT.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
assert receipt["total_process_CPU_seconds"]<=180
print(json.dumps({k:out[k] for k in ("sources","operations","independent_operation_checks","sources_with_R6","R6_total","max_R6_over_A")}))
print(json.dumps({"permanently_absent":len(permanent),"needed_unpaid":len(unpaid_examples),"CPU_recorded":receipt["total_process_CPU_seconds"],
                  "needed_unpaid_max_prevload":max(r["unpaid_max_A_loss_load"] for r in rows),
                  "needed_unpaid_max_restoreload":max(r["unpaid_max_A_restoration_load"] for r in rows)}))
for r in rows:
    if r.get("unpaid_neutral",0):print(json.dumps(r))

