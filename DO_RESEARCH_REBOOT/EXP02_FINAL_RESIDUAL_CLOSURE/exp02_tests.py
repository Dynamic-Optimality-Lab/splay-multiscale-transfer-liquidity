"""Consequential regressions, exact obstructions and global original-unit budgets."""
import time,json,hashlib
from exp02_core import *


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    checks=[]
    def test(name,condition):
        assert condition,name
        checks.append(name)
    gate=json.loads((ROOT/"EXP02_G_ADAPTIVE_GATE.json").read_text())
    test("G exact minimal physical domain",gate["candidate_window"]["J"]==list(range(1,33))+[34,50])
    test("G threshold 18 and exact primitive isolation",gate["candidate_window"]["threshold"]==18 and gate["candidate_window"]["physical_path_isolation"])
    frame_only=json.loads((ROOT/"EXP02_FRAME_BRIDGE_CERTIFICATES.json").read_text())["sources"]
    bridge=json.loads((ROOT/"EXP02_COMMON_GRANDPARENT_CERTIFICATES.json").read_text())["sources"]
    d=json.loads((ROOT/"EXP02_INTERRUPTION_DISTORTION_RESULTS.json").read_text())["sources"]
    a=json.loads((ROOT/"EXP02_ADAPTIVE_DOMAIN_RESULTS.json").read_text())
    byname={r["source"]:r for r in d}
    for r in a["sources"]+a["new_sources"]:
        cert=r["adaptive_certificate"];slots=[]
        for w in cert["windows"]:
            slots.extend(tuple(e[1:3]) for e in w["original_A_gap_witnesses"])
            test("window physical paths "+r["source"]+str(w["anchor"]),w["physical_path_isolation"] and w["complete_outside_components_preserved"])
        test("global adaptive original-A disjointness "+r["source"],len(slots)==len(set(slots)) and cert["E_J"]<=2*len(slots)<=2*byname[r["source"]]["A"])
    test("all inherited exact complement events paid by new classes",sum(r["remaining"] for r in bridge if r["origin"]=="EXP01")==0)
    test("new falsification cases retain a strict unpaid complement",sum(r["remaining"] for r in bridge if r["origin"]=="EXP02")==14)
    cheap=byname["zig_distortion_n9_L4"];w=cheap["windows"][0]
    test("positive distortion with zero omitted doubles",cheap["A"]==17 and cheap["Q_B"]==1 and w["delta"]==1 and w["omitted_Q"]==0)
    test("positive distortion survives complete B closing",w["closing_delta"]==0 and w["signed_retained_plus_closing_delta"]==1 and w["shadow_B_closes_after_actual_rest_of_period"])
    aux=byname["zig_distortion_auxiliary_closed_control"]
    test("same-A auxiliary closure is real, without lending original units",aux["A"]==17 and aux["Q_B"]==0 and aux["full_source_paired_closed"])
    high=byname["IH_p4_q1_L3_z65_c1"]["windows"][0]
    test("raw distortion not bounded by omitted double count with coefficient one",high["delta"]==8 and high["omitted_Q"]==3)
    hard=next(r for r in bridge if r["source"]=="IH_p4_q1_L2_z5_c1")
    test("omitted first hit is genuine complete-source unpaid R6",hard["A"]==259 and hard["Q_B"]==110 and hard["remaining"]==1 and hard["events"][0]["rho"]==[132,[72,3],[80,1]] and hard["events"][0]["category"]=="unpaid_omitted")
    test("negative retained distortion does not cover omitted consumers",byname[hard["source"]]["sum_signed_delta"]==-2 and byname[hard["source"]]["unpaid_omitted_or_uncovered"]==1)
    changed=next(r for r in frame_only if r["source"]=="IH_p6_q1_L3_z257_c1")
    test("full-frame-only cover has an exact strict limitation",changed["counts"]["unmatched_retained"]==2)
    test("common-grandparent proof genuinely broadens frame-equality cover",sum(r["additional_paid_by_common_grandparent"] for r in bridge)==10)
    test("frame injection has global original gap load at most three",all(r["max_shadow_double_load"]<=3 for r in bridge))
    pins=json.loads((ROOT/"EXP02_INPUT_MANIFEST.json").read_text())["pins"]
    test("all pinned historical dependencies unchanged",all(hashlib.sha256((REPO/p).read_bytes()).hexdigest()==h for p,h in pins.items()))
    archive=json.loads((ROOT/"EXP02_SOURCE_WITNESSES.json").read_text())
    allsrc=archive["inherited_sources"]+archive["new_sources"]
    test("exact complete physical closure of every saved source",all(s["initial_A"]==s["closing_A"] and s["initial_B"]==s["closing_B"] for s in allsrc))
    test("171 unique complete sources and 76474 distinct operations",len(allsrc)==171 and len({s["name"] for s in allsrc})==171 and sum(len(s["operations"]) for s in allsrc)==76474)
    resource=json.loads((ROOT/"EXP02_RESOURCE_RECORD.json").read_text())
    resource["final_tests_CPU_seconds"]=time.process_time()-cpu
    resource["final_tests_wall_seconds"]=time.perf_counter()-wall
    resource["final_tests_memory"]=memory();resource["recorded_CPU_subtotal"]+=resource["final_tests_CPU_seconds"]
    write("EXP02_TEST_RESULTS.json",{"status":"PASS","checks":checks,"count":len(checks)})
    write("EXP02_RESOURCE_RECORD.json",resource)
    print(json.dumps({"status":"PASS","checks":len(checks),"recorded_CPU_seconds":resource["recorded_CPU_subtotal"]}))
