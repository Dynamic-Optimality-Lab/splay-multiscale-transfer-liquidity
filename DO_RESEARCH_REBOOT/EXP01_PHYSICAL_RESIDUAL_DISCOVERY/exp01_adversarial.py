"""Independent falsification of the finite R6 root-entry matching observation."""
import json,time
from exp01_run import ROOT,write,reaching_check
from exp01_oracle import Replay
from exp01_sources import detour_W,reflect
from exp01_diagnostics import physical_diagnostics,return_zig_reduction,normalized_certificate


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    data=json.loads((ROOT/"EXP01_RESULTS.json").read_text())
    archive=json.loads((ROOT/"EXP01_SOURCE_WITNESSES.json").read_text())
    certs=json.loads((ROOT/"EXP01_THEOREM_CERTIFICATES.json").read_text())
    srcs=[detour_W(p,q) for p,q in ((4,1),(4,2),(5,1),(5,2),(6,1))]
    srcs += [reflect(detour_W(5))]
    for src in srcs:
        r=Replay(src)
        summary=r.summary();summary["family"]=src["family"];summary["reachability_check"]=reaching_check(src)
        summary["physical"]=physical_diagnostics(r)
        summary["zig_return_reductions"]=[return_zig_reduction(r,d) for d in (1,-1)]
        data["results"].append(summary)
        archive["sources"].append({**src,"closing_A":r.a.state(),"closing_B":r.b.state(),
            "costs":{"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"]},"trace_hash":summary["trace_hash"],
            "R6_certificates":[{**p,"endpoints":[r.U[tuple(p["rho"][j])] for j in (1,2)],
                "renewed_demand":r.U[tuple(p["parent"])]} for p in r.pairs if p["class"]=="R6"]})
        certs["certificates"].append({"source":src["name"],"certificates":[normalized_certificate(r,z) for z in summary["zig_return_reductions"]]})
        print(src["name"],"A",r.A,"Q",r.Q,"R6",r.counts["R6"],"R6 matching deficiency",summary["physical"]["root_entry_incidence_R6"]["deficiency"],flush=True)
    resource=data["resources"]
    elapsed=time.process_time()-cpu
    resource.update(adversarial_process_cpu_seconds=elapsed,adversarial_wall_seconds=time.perf_counter()-wall,
        total_recorded_process_cpu_seconds=resource["total_recorded_process_cpu_seconds"]+elapsed,
        source_count=len(data["results"]),total_operations=sum(x["operations"] for x in data["results"]),
        independent_operation_checks=sum(x["independent_operation_checks"] for x in data["results"]),
        theorem_interface_replays=len(certs["certificates"]))
    assert resource["total_recorded_process_cpu_seconds"]<600
    write("EXP01_RESULTS.json",data);write("EXP01_SOURCE_WITNESSES.json",archive)
    write("EXP01_THEOREM_CERTIFICATES.json",certs);write("EXP01_RESOURCE_RECORD.json",resource)
