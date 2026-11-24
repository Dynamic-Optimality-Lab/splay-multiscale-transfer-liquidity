"""Canonical distortion corpus, independent new-source falsification and closure audit."""
import time,json,hashlib
from exp02_distortion import *
from exp02_sources import new_corpus,interrupted_H


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    archive=json.loads((ROOT/"EXP02_SOURCE_WITNESSES.json").read_text())
    inherited=archive["inherited_sources"]
    previous=json.loads((ROOT/"EXP02_ADAPTIVE_DOMAIN_RESULTS.json").read_text())
    old_adapt={s["source"]:s["adaptive_certificate"] for s in previous["sources"]}
    resource=json.loads((ROOT/"EXP02_RESOURCE_RECORD.json").read_text())
    output=[];new_inventory=[];new_adapts=[];new_witnesses=[]
    all_sources=inherited+new_corpus()+[interrupted_H(7,3,(513,))]
    operations=shadow_operations=0
    for i,src in enumerate(all_sources):
        r=Replay(src)
        if i<len(inherited):assert digest(r.events)==src["trace_hash"]
        direction,ret,other=residual(r)
        adapt=old_adapt.get(src["name"])
        if adapt is None:adapt=adaptive(r)
        z=source_distortion(r,other,adapt)
        z.update(origin="EXP01" if i<len(inherited) else "EXP02",population=len(r.keys),family=src["family"],
            R6=r.counts["R6"],R6_return=len(ret["covered_R6"]),adaptive_paid=len(other)-z["after_adaptive"],
            P_A=r.PA,N_A=r.NA,D_B=r.DB,actual_A_real_rotations=2*r.A-r.VA,
            full_source_paired_closed=True,independent_actual_operation_checks=r.independent_checks)
        output.append(z);operations+=r.independent_checks;shadow_operations+=z["independent_shadow_accesses"]
        if i>=len(inherited):
            rows=[event_inventory(r,p,ret,adapt) for p in other]
            new_inventory.append({"source":src["name"],"orientation":direction,"R6_other":len(other),"events":rows})
            new_adapts.append({"source":src["name"],"adaptive_certificate":adapt})
            new_witnesses.append({**src,"closing_A":r.a.state(),"closing_B":r.b.state(),"trace_hash":digest(r.events),
                "costs":{"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"],"R6_other":len(other)}})
        print(f"{i+1:03d} {src['name']}: other={len(other)} adaptive={z['adaptive_paid']} delta+={z['sum_positive_delta']} return-paid={z['synchronized_return_paid']} remaining={z['after_both_proved_classes']} omitted/uncovered={z['unpaid_omitted_or_uncovered']}",flush=True)
        assert resource["inventory_process_CPU_seconds"]+time.process_time()-cpu<850,"EXP02 computation reserve"
        del r
    resource.update(distortion_process_CPU_seconds=time.process_time()-cpu,distortion_wall_seconds=time.perf_counter()-wall,
        distortion_actual_operation_checks=operations,independent_shadow_scan_accesses=shadow_operations,
        new_complete_sources=len(new_witnesses),new_source_operations=sum(len(s["operations"]) for s in new_witnesses),
        distortion_peak_memory=memory(),unmetered_pilots="four-source two-direction shadow pilot, then five-source one-direction diagnostic pilot; final run repeats every consequential case")
    resource["recorded_CPU_subtotal"]=resource["inventory_process_CPU_seconds"]+resource["distortion_process_CPU_seconds"]
    write("EXP02_INTERRUPTION_DISTORTION_RESULTS.json",{"status":"FINITE_EXACT","sources":output,"resources":resource,
        "selection":"single inherited original-root orientation; earliest cyclic extreme anchor, first expected S-rank occurrences; disjoint original spans",
        "shadow_status":"B comparison only, not original A credit; continuous closing continuation separately records whether its B state returns"})
    old_inventory=json.loads((ROOT/"EXP02_REMAINING_R6_INVENTORY.json").read_text());old_inventory["new_sources"]=new_inventory
    write("EXP02_REMAINING_R6_INVENTORY.json",old_inventory)
    previous["new_sources"]=new_adapts;write("EXP02_ADAPTIVE_DOMAIN_RESULTS.json",previous)
    archive["new_sources"]=new_witnesses;write("EXP02_SOURCE_WITNESSES.json",archive)
    write("EXP02_RESOURCE_RECORD.json",resource)
    print(json.dumps(resource,indent=2),flush=True)
