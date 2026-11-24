"""Complete original event inventories and independently inspect final budgets."""
import time,json,hashlib
from exp02_core import *


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    archive=json.loads((ROOT/"EXP02_SOURCE_WITNESSES.json").read_text())
    inventory=json.loads((ROOT/"EXP02_REMAINING_R6_INVENTORY.json").read_text())
    resource=json.loads((ROOT/"EXP02_RESOURCE_RECORD.json").read_text())
    bridge=json.loads((ROOT/"EXP02_COMMON_GRANDPARENT_CERTIFICATES.json").read_text())
    bridge_lookup={s["source"]:{digest(e["rho"]):e for e in s["events"]} for s in bridge["sources"]}
    lookup={s["name"]:s for s in archive["inherited_sources"]+archive["new_sources"]}
    folder=ROOT/"EXP02_ORIGINAL_STATES";folder.mkdir(exist_ok=True)
    replay_ops=0
    for group in (inventory["sources"],inventory["new_sources"]):
        for source in group:
            if not source["events"]:continue
            src=lookup[source["source"]];r=Replay(src,certify=False,independent=False)
            assert digest(r.events)==src["trace_hash"]
            replay_ops+=len(r.ops)
            pool={}
            filename=f"EXP02_ORIGINAL_STATES/{digest(src['name'])[:16]}.json"
            def ref(actor,state):
                h=digest(state);pool[h]=state
                return {"namespace":actor,"state_sha256":h,"pool_file":filename}
            for row in source["events"]:
                h=row["rho"][0];receiver=row["parent_certificate"]["h"]
                for label,t in (("consuming_operation",h),("renewed_receiver_operation",receiver)):
                    b=r.boundaries[t-1]
                    row[label+"_states"]={key:ref("original_A" if key.endswith("A") else "actual_B",b[key]) for key in ("pre_A","pre_B","post_A","post_B")}
                outer=row["endpoint_certificates"][1];lo=outer["nu"];hi=outer["hit_time"]
                shared=[];entries=set()
                for e in r.events:
                    if e["actor"]!="A":continue
                    lifted_time=e["time"]+(r.T if e["time"]<=lo else 0)
                    if lifted_time<=hi:
                        shared.append(e)
                        if e["external"] is None and r.bits.get(e["promoted"],0)&outer["J"] and not r.bits.get(e["pivot"],0)&outer["J"]:
                            entries.add(tuple(e["id"][1:3]))
                steps=sorted({tuple(e["id"][1:3]) for e in shared})
                row["original_A_root_entry_resources_not_payments"]=[list(k) for k in sorted(entries)]
                row["original_A_shared_life_work"]={"StepEv": [list(k) for k in steps],"cost":len(steps),
                    "real_rotations":[e["id"] for e in shared],"sign_counts":dict(Counter(e["sign"] for e in shared)),
                    "outside_shared_life_original_A_cost":r.A-len(steps),
                    "qualification":"These are actual source events, possibly already used by inherited accounting. Shared across histories; not declared unused or independently payable."}
                row["fixed_D6_domain"]=sorted(r.I)
                for f in row["maximal_monotone_fragments_through_consumer"]:
                    init=Tree(r.boundaries[f["operations"][0]-1]["pre_B"])
                    f["fixed_I_ancestor_closed_at_initialization"]=closure(init,r.I)==r.I
                    f["outside_I_targets"]=[t for t in f["operations"] if r.ops[t-1][1] not in r.I]
                    last=f["operations"][-1];keeps=[b for b in r.boundaries if b["tag"]=="K"]
                    ki=next(i for i,b in enumerate(keeps) if b["t"]==last)
                    nextrow=keeps[(ki+1)%len(keeps)]
                    f["following_transition"]={"operation":nextrow["t"],"target":nextrow["x"],"A":nextrow["a"],"Q_B":nextrow["q"],
                        "complete_B_changed":nextrow["pre_B"]!=nextrow["post_B"],
                        "pre_B":ref("actual_B",nextrow["pre_B"]),"post_B":ref("actual_B",nextrow["post_B"])}
                match=bridge_lookup[source["source"]].get(digest(row["rho"]))
                row["final_class"]="adaptive_paid" if row["adaptive_covered"] else match["category"]
            (ROOT/filename).write_text(json.dumps({"source":src["name"],"state_pool":pool},separators=(",",":"),sort_keys=True)+"\n")
            del r
    resource.update(inventory_enrichment_CPU_seconds=time.process_time()-cpu,inventory_enrichment_wall_seconds=time.perf_counter()-wall,
        inventory_enrichment_hash_verified_operations=replay_ops,inventory_enrichment_memory=memory(),
        g_gate_CPU_seconds=json.loads((ROOT/"EXP02_G_ADAPTIVE_GATE.json").read_text())["CPU_seconds"],
        initial_invalid_memory_probe_CPU_seconds=0.15625,
        unmetered_pilots="four-source two-direction pilot; five-source one-direction pilot; five-source first-hit-in-omission pilot. Final timed runs repeat all consequential cases.")
    resource["failed_finalization_record"]="One prior finalization replay finished but its timer write failed because an integer variable shadowed the time module. No canonical results were written by that failed attempt. Its exact CPU was not captured. The corrected finalization repeats the affected data extraction."
    resource["recorded_CPU_subtotal"]+=resource["inventory_enrichment_CPU_seconds"]+resource["g_gate_CPU_seconds"]+resource["initial_invalid_memory_probe_CPU_seconds"]
    assert resource["recorded_CPU_subtotal"]<900
    inventory["final_source_defined_partition"]=dict(Counter(e["final_class"] for s in inventory["sources"]+inventory["new_sources"] for e in s["events"]))
    inventory["global_final_residual_closed"]=False
    write("EXP02_REMAINING_R6_INVENTORY.json",inventory);write("EXP02_RESOURCE_RECORD.json",resource)
    print(json.dumps({"partition":inventory["final_source_defined_partition"],"resources":resource},indent=2))
