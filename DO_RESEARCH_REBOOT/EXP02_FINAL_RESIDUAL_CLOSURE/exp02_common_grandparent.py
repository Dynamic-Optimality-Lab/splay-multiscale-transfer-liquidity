"""A stronger proved comparison: a common physical grandparent is sufficient.

Complete-frame equality was a deliberately strong discovery diagnostic. For
the counting proof, each physical grandparent can occur in only one double
of a given splay. Matching that labelled vertex already supplies injection,
even if its components or orientation differ. It does not cover omissions.
"""
import json,time
from collections import Counter
from exp02_core import ROOT,write

if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    raw=json.loads((ROOT/"EXP02_FRAME_BRIDGE_CERTIFICATES.json").read_text())["sources"]
    comparisons={s["source"]:s for s in json.loads((ROOT/"EXP02_INTERRUPTION_DISTORTION_RESULTS.json").read_text())["sources"]}
    output=[]
    for source in raw:
        events=[];destinations={};loads=Counter();changed_count=0
        for old in source["events"]:
            e=dict(old);category=e["category"]
            if category=="frame_matched_retained":
                e["category"]="common_grandparent_retained"
                e["full_frame_also_matches"]=True
            elif category=="unmatched_retained":
                g=e["actual_frame"]["g"]
                matched=[s for s in e["available_shadow_frames"] if s["g"]==g]
                assert len(matched)<=1
                if matched:
                    wi=next(i for i,w in enumerate(comparisons[source["source"]]["windows"]) if e["consumer"] in w["retained"])
                    e.update(category="common_grandparent_retained",shadow_double=[wi,e["consumer"],matched[0]["j"]],
                        frame_root=g,full_frame_also_matches=False)
                    changed_count+=1
            if e["category"]=="common_grandparent_retained":
                dest=tuple(e["shadow_double"]);parent=tuple(e["original_parent"])
                assert dest not in destinations or destinations[dest]==parent
                destinations[dest]=parent;loads[dest]+=1
            events.append(e)
        assert max(loads.values(),default=0)<=3
        counts=Counter(e["category"] for e in events)
        paid=counts["common_grandparent_retained"]+counts["synchronized_omitted"]
        output.append({**source,"events":events,"counts":dict(counts),"bridge_paid":paid,"remaining":len(events)-paid,
            "additional_paid_by_common_grandparent":changed_count,"max_shadow_double_load":max(loads.values(),default=0)})
    write("EXP02_COMMON_GRANDPARENT_CERTIFICATES.json",{"sources":output,
        "proof_status":"Restricted source-uniform injection proved in report; finite certificates alone do not prove full residual coverage.",
        "physical_rule":"same original consuming operation and same labelled old grandparent, present in one shadow double; all full original demand predicates retained"})
    resource=json.loads((ROOT/"EXP02_RESOURCE_RECORD.json").read_text())
    resource.update(common_grandparent_CPU_seconds=time.process_time()-cpu,common_grandparent_wall_seconds=time.perf_counter()-wall)
    resource["recorded_CPU_subtotal"]+=resource["common_grandparent_CPU_seconds"]
    write("EXP02_RESOURCE_RECORD.json",resource)
    print(json.dumps({"remaining":sum(s["remaining"] for s in output),"additional_paid":sum(s["additional_paid_by_common_grandparent"] for s in output),
        "remaining_sources":[(s["source"],s["remaining"],s["counts"]) for s in output if s["remaining"]]},indent=2))
