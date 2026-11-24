"""Independent finite audit: explicit subset Hall counts and actual event loads."""
from pathlib import Path
import json,time,sys,traceback
from collections import Counter
from fractions import Fraction
START=time.process_time();ROOT=Path(__file__).resolve().parent;P=ROOT.parent
receipt=json.loads((ROOT/"RESOURCE_RECEIPT.json").read_text());prior=receipt["cumulative_recorded_CPU_seconds"]
def save(name,x):(ROOT/name).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
old=json.loads((ROOT/"ALL_R6_ALTERNATIVE_WORK.json").read_text())
new=json.loads((ROOT/"DESCENDING_FIRST_HIT_COUNTEREXAMPLES.json").read_text())
multi=json.loads((ROOT/"CROSS_CHAIN_CONTROLS.json").read_text())
results=[];failure=None
try:
    cases=[]
    inventory=json.loads((P/"GLOBAL_MULTIPLICITY_AUDIT.json").read_text())
    cert_for={r["name"]:r["certificate"] for r in inventory["rows"]}
    for row in old["results"]:cases.append((row,P/cert_for[row["name"]]))
    for row in new["results"]:cases.append((row,ROOT/row["certificate"]))
    for row in multi["records"]:cases.append((row["global_assignments"],ROOT/row["certificate"]))
    subset_checks=0;total=0
    for row,path in cases:
        if time.process_time()-START>180-prior-3:raise RuntimeError("CPU ceiling")
        c=json.loads(path.read_text());e_by_id={tuple(e["id"]):e for e in c["all_physical_ancestry_events"]}
        resources=[e for e in c["all_physical_ancestry_events"] if e["actor"]=="A" and e["promoted"] in c["summary"]["S"]]
        loads=Counter();steps=Counter();neigh=[]
        for d in row["assignments"]:
            e=e_by_id[tuple(d["assigned_original_A_bit"])]
            assert e["actor"]=="A" and e["promoted"] in d["outer_J"]
            loads[tuple(e["id"])]+=1;steps[tuple(e["id"][:3])]+=1
            mask=0
            for i,r in enumerate(resources):
                if r["promoted"] in d["outer_J"]:mask|=1<<i
            assert mask;neigh.append(mask)
        assert len(neigh)==c["summary"]["R6"]==row["R6"]
        assert max(loads.values(),default=0)<=1 and max(steps.values(),default=0)<=1
        unions=[0]*(1<<len(neigh));best=Fraction(0)
        for subset in range(1,len(unions)):
            bit=subset&-subset;idx=bit.bit_length()-1
            unions[subset]=unions[subset^bit]|neigh[idx]
            ratio=Fraction(subset.bit_count(),unions[subset].bit_count())
            if ratio>best:best=ratio
        stated=row["exact_global_fractional_congestion"]
        assert best==Fraction(stated["numerator"],stated["denominator"])
        subset_checks+=len(unions)-1;total+=row["R6"]
        results.append({"name":row["name"],"R6":row["R6"],"all_demand_subsets_checked":len(unions)-1,
            "actual_A_real_bit_max_load":max(loads.values(),default=0),"actual_A_StepEv_max_load":max(steps.values(),default=0),
            "exact_Hall_ratio":stated,"source_registry_equal":True})
    c=json.loads((ROOT/"CERTIFICATE_p3_original.json").read_text())
    e=next(e for e in c["all_physical_ancestry_events"] if e["id"]==["B",36,1,0])
    decode=lambda lab:[k for k in range(1,34) if lab&(1<<(k-1))]
    lost=[decode(lab) for lab in e["lost"]];created=[decode(lab) for lab in e["created"]]
    assert lost==[list(range(23,32))] and created==[list(range(19,26))] and e["sign"]==0
    assert e["pivot"]==22 and e["promoted"]==26 and e["target"]==30
    localized={"source":"SOURCE_p3_original.json","original_B_event":e["id"],
        "I":[19,25],"lost_original_SET_label":lost[0],"created_original_SET_label":created[0],
        "pivot":22,"promoted":26,"target":30,"global_Psi_delta":0,
        "inside_I_missing_SET_inventory_delta":1,
        "reason_A_absent":"A is the complete two-vine state rooted at 30; proper labels are prefixes/suffixes.",
        "note":"Diagnostic showing why global SET conservation does not restrict to an interval; not a new potential or bound."}
    save("FIRST_LITERAL_INTERVAL_INFLOW.json",localized)
    save("INDEPENDENT_EVENT_LOAD_VERIFICATION.json",{"status":"FINITE-EXACT ONLY",
        "original_sources_represented":126,"sources_with_R6":len(cases),"all_R6":total,
        "Hall_demand_subsets_checked":subset_checks,"universal_bound":"OPEN","results":results})
    print(json.dumps({"sources":126,"sources_with_R6":len(cases),"R6":total,"Hall_subsets":subset_checks,
                      "max_actual_A_StepEv_load":1,"localized_neutral_B_inflow_verified":True}))
except BaseException:
    failure=traceback.format_exc();print(failure,flush=True);save("FAILED_VERIFICATION.json",{"failure":failure})
finally:
    cpu=time.process_time()-START
    receipt.setdefault("continuations",[]).append({"phase":"independent_saved_event_load_verification","process_CPU_seconds":cpu,
        "new_source_replays":0,"failure":failure})
    receipt["cumulative_recorded_CPU_seconds"]=prior+cpu
    save("RESOURCE_RECEIPT.json",receipt);assert prior+cpu<=180
if failure:sys.exit(1)

