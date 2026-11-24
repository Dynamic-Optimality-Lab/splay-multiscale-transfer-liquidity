"""Physical, R6-independent lost/common/new grandparent identity."""
import time,json
from exp02_frame_bridge import frame_records
from exp02_core import ROOT,write,memory

if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    data=json.loads((ROOT/"EXP02_INTERRUPTION_DISTORTION_RESULTS.json").read_text())
    output=[]
    for source in data["sources"]:
        windows=[]
        for w in source["windows"]:
            trace=json.loads((ROOT/w["physical_trajectory_file"]).read_text());pool=trace["state_pool"]
            accesses=[];L=M=0
            for a in trace["retained_accesses"]:
                actual=frame_records(pool[a["actual_pre"]["state_sha256"]],a["target"],pool[a["actual_post"]["state_sha256"]])
                shadow=frame_records(pool[a["shadow_pre"]["state_sha256"]],a["target"],pool[a["shadow_post"]["state_sha256"]])
                ga={f["g"] for f in actual.values()};gs={f["g"] for f in shadow.values()}
                assert len(ga)==a["actual_q"] and len(gs)==a["shadow_q"]
                lost=sorted(ga-gs);gained=sorted(gs-ga)
                assert a["difference"]==len(lost)-len(gained)
                L+=len(lost);M+=len(gained)
                accesses.append({"operation":a["original_operation"],"actual_grandparents":sorted(ga),"shadow_grandparents":sorted(gs),
                    "actual_only_grandparents":lost,"shadow_only_grandparents":gained,
                    "signed_double_difference":a["difference"]})
            assert w["delta"]==L-M
            windows.append({"trajectory_file":w["physical_trajectory_file"],"L_actual_only":L,"M_shadow_only":M,
                "delta":L-M,"accesses":accesses})
        output.append({"source":source["source"],"A":source["A"],"windows":windows,
            "L_actual_only":sum(w["L_actual_only"] for w in windows),"M_shadow_only":sum(w["M_shadow_only"] for w in windows)})
    write("EXP02_GRANDPARENT_DISTORTION.json",{"sources":output,"identity":"delta_window = L_window - M_window",
        "objects":"Every labelled old grandparent of a double, per retained original KEEP occurrence, counted once in that splay; independent of R6 membership.",
        "A_bound_status":"OPEN. This signed physical identity does not identify original A payments or prove cancellation across periods."})
    resource=json.loads((ROOT/"EXP02_RESOURCE_RECORD.json").read_text())
    resource.update(grandparent_identity_CPU_seconds=time.process_time()-cpu,grandparent_identity_wall_seconds=time.perf_counter()-wall,
        grandparent_identity_memory=memory());resource["recorded_CPU_subtotal"]+=resource["grandparent_identity_CPU_seconds"]
    write("EXP02_RESOURCE_RECORD.json",resource)
    print(json.dumps({"sources":len(output),"CPU_seconds":resource["grandparent_identity_CPU_seconds"]}))
