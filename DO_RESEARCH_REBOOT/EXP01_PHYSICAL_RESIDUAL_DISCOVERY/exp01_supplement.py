"""Targeted falsification and proof-interface audit after the discovery run."""
import json,time
from collections import Counter
from exp01_run import ROOT,write,reaching_check
from exp01_oracle import Replay,Tree,digest
from exp01_sources import nested_detour,reflect,G,H,detour_H
from exp01_diagnostics import physical_diagnostics,return_zig_reduction,normalized_certificate,lifecycle


def main():
    cpu=time.process_time();wall=time.perf_counter()
    data=json.loads((ROOT/"EXP01_RESULTS.json").read_text())
    archive=json.loads((ROOT/"EXP01_SOURCE_WITNESSES.json").read_text())
    sources=[nested_detour(d,t,h) for d,t,h in ((2,0,False),(5,0,False),(10,0,False),(30,0,False),
        (2,17,False),(5,63,False),(2,17,True),(5,63,True))]
    sources += [reflect(nested_detour(5,63,True))]
    for src in sources:
        reach=reaching_check(src)
        r=Replay(src)
        summary=r.summary();summary["family"]=src["family"];summary["reachability_check"]=reach
        summary["physical"]=physical_diagnostics(r)
        summary["zig_return_reductions"]=[return_zig_reduction(r,d) for d in (1,-1)]
        data["results"].append(summary)
        archive["sources"].append({**src,"closing_A":r.a.state(),"closing_B":r.b.state(),
            "costs":{"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"]},"trace_hash":summary["trace_hash"],
            "R6_certificates":[{**p,"endpoints":[r.U[tuple(p["rho"][j])] for j in (1,2)],
                "renewed_demand":r.U[tuple(p["parent"])]} for p in r.pairs if p["class"]=="R6"]})
        print(src["name"],r.A,r.Q,r.counts["R6"],flush=True)
    # Every finite theorem-interface certificate uses the exact canonical trace
    # already checked by the independent engine. Replay again without repeating
    # expensive history certification, and require the original full trace hash.
    certs=[]
    for src,summary in zip(archive["sources"],data["results"]):
        r=Replay(src,certify=False,independent=False)
        assert digest(r.events)==src["trace_hash"]
        r.pairs=summary["R6_events"]
        certs.append({"source":src["name"],"certificates":[normalized_certificate(r,z) for z in summary["zig_return_reductions"]]})
    # Brute snapshot check of the cyclic absence implementation, including the
    # previous-period Pi, independent of the interval-change query itself.
    brute=[]
    for name in ("G_4_1_L31_r1_z1","W_star"):
        src=next(s for s in archive["sources"] if s["name"]==name)
        r=Replay(src)
        a=Tree(src["initial_A"])
        snapshots=[set(a.labels(r.bits).values())-{0}]
        for ev in r.events:
            if ev["actor"]=="A":
                a.rotate(ev["pivot"],ev["side"])
            snapshots.append(set(a.labels(r.bits).values())-{0})
        compared=0
        for d in r.doubles.values():
            if "kappa" not in d:
                continue
            lo,hi=d["kappa"],d["post_A"]
            actual=any(d["F"] in snapshots[t%r.T] for t in range(lo+1,hi+1))
            assert actual==r.any_present(d["F"],lo,hi)
            compared+=1
        brute.append({"source":name,"full_Pi_snapshot_comparisons":compared})
        if name.startswith("G_"):
            write("EXP01_G_LIFECYCLE.json",lifecycle(r))
    # The alleged R6 signature is not determined by the physical prefix even
    # through its renewed receiver. Both sources have exactly that same prefix.
    base=Replay(H(4));detour=Replay(detour_H())
    upto=base.boundaries[159]["end_time"]
    assert base.events[:upto]==detour.events[:upto]
    rho=[132,[72,3],[80,1]]
    prefix_result={"through_original_operation":160,"primitive_prefix_hash":digest(base.events[:upto]),
        "same_complete_pair_prefix":True,
        "H_class":next(p["class"] for p in base.pairs if p["rho"]==rho),
        "detour_class":next(p["class"] for p in detour.pairs if p["rho"]==rho),
        "H_Q_B":base.Q,"detour_Q_B":detour.Q,"H_A":base.A,"detour_A":detour.A}
    # Recover the explicit growing relay rather than infer nesting by sizes.
    h6=Replay(H(6))
    relays=[]
    for p in h6.pairs:
        if p["class"] not in ("R_scan","R_fringe","R6"):
            continue
        d=h6.U[tuple(p["parent"])]
        if h6.label_keys(d["J"])==list(range(11,34)):
            for q in h6.pairs:
                if tuple(p["parent"]) in [tuple(q["rho"][1]),tuple(q["rho"][2])]:
                    nd=h6.doubles[tuple(q["parent"])]
                    if h6.label_keys(nd["J"])==list(range(19,130)):
                        relays.append({"first_pair":p,"first_output":[11,33],"next_pair":q,"next_output":[19,129]})
    assert relays,"H6 growing relay anchor not recovered"
    elapsed=time.process_time()-cpu
    resource=data["resources"]
    resource.update(supplement_process_cpu_seconds=elapsed,supplement_wall_seconds=time.perf_counter()-wall,
        total_recorded_process_cpu_seconds=resource["main_run_process_cpu_seconds"]+elapsed,
        source_count=len(data["results"]),total_operations=sum(x["operations"] for x in data["results"]),
        independent_operation_checks=sum(x["independent_operation_checks"] for x in data["results"]),
        theorem_interface_replays=len(certs))
    assert resource["total_recorded_process_cpu_seconds"]<600 and len(data["results"])<=200
    write("EXP01_THEOREM_CERTIFICATES.json",{"certificates":certs,"brute_Pi_checks":brute,
        "prefix_indistinguishability":prefix_result,"H6_growing_relays":relays,
        "scope":"Exact finite proof-interface tests; universal scoped argument is in the report, using the inherited sequential-access theorem and three-slot lemma."})
    write("EXP01_RESULTS.json",data)
    write("EXP01_SOURCE_WITNESSES.json",archive)
    write("EXP01_RESOURCE_RECORD.json",resource)
    print(json.dumps(resource,indent=2),flush=True)


if __name__=="__main__":
    main()
