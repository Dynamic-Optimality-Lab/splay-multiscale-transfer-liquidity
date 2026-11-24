"""Exact 171-source inheritance, distinct parents, original ancestry histories."""
from exp03_core import *
import subprocess


def file_hash(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(2**20),b""):h.update(chunk)
    return h.hexdigest()


if __name__=="__main__":
    meter=Meter("inheritance")
    old_delivery=json.loads((OLD/"EXP02_DELIVERY_MANIFEST.json").read_text())
    for p,h in old_delivery["files"].items():assert file_hash(OLD/p)==h,p
    inherited_archive=json.loads((OLD/"EXP02_SOURCE_WITNESSES.json").read_text())
    all_sources=inherited_archive["inherited_sources"]+inherited_archive["new_sources"]
    old_final=json.loads((OLD/"EXP02_COMMON_GRANDPARENT_CERTIFICATES.json").read_text())["sources"]
    old_byname={s["source"]:s for s in old_final}
    # Read the full current inventory, retaining only the final unpaid rows.
    old_inventory=json.loads((OLD/"EXP02_REMAINING_R6_INVENTORY.json").read_text())
    old_unpaid={s["source"]:[e for e in s["events"] if e.get("final_class") in ("unmatched_retained","unpaid_omitted","outside_shadow_cover")] for s in old_inventory["sources"]+old_inventory["new_sources"]}
    assert sum(map(len,old_unpaid.values()))==14
    del old_inventory
    old_adaptive=json.loads((OLD/"EXP02_ADAPTIVE_DOMAIN_RESULTS.json").read_text())
    old_gp=json.loads((OLD/"EXP02_GRANDPARENT_DISTORTION.json").read_text())
    assert len(old_gp["sources"])==171
    del old_adaptive,old_gp
    pinfiles=[ROOT.parent/p for p in ("RESEARCH_RULES.md","IAGS12_D1_COLLISION_PROVENANCE.md","IAGS12_D2_RESIDUAL_REGENERATION_COST.md","IAGS12_D3_BLIND_GAP_COMPOSITION.md","IAGS12_D4_NEUTRAL_RENEWAL.md","IAGS12_D5_BRANCH_RENEWAL_COST.md","IAGS12_D6_INTERRUPTED_SCAN_COST.md","IAGS12_G0_QUANTITATIVE_BASELINE.md","RG01_PRIMITIVE_ACCOUNTING.md","RG04_GLOBAL_REGENERATION.md","IAGS12_PARALLEL_B_BOUNDARY_SURCHARGE.md")]
    pins={str(p.relative_to(REPO)):file_hash(p) for p in pinfiles}
    write("EXP03_INPUT_MANIFEST.json",{"EXP02_complete_delivery_hashes_verified":old_delivery["files"],"additional_repository_pins":pins,
        "HEAD":subprocess.check_output(["git","rev-parse","HEAD"],cwd=REPO,text=True).strip(),
        "branch":subprocess.check_output(["git","branch","--show-current"],cwd=REPO,text=True).strip()})
    inventory=[];omitted=[];missing=[];summaries=[];independent_ops=0
    for i,s in enumerate(all_sources):
        r=Replay(s)
        assert digest(r.events)==s["trace_hash"]
        prior=old_byname[s["name"]]
        expected=[e for e in prior["events"] if e["category"] not in ("common_grandparent_retained","synchronized_omitted")]
        actual_records=[]
        if expected:
            cl=current_classification(r)
            assert {digest(e["rho"]) for e in cl["unhandled"]}=={digest(e["rho"]) for e in expected}
            parents=parent_sets(cl["unhandled"])
            by_parent={tuple(e["original_parent"]):[] for e in cl["unhandled"]}
            for e in cl["unhandled"]:by_parent[tuple(e["original_parent"])].append(e)
            for parent,gaps in sorted(by_parent.items()):
                d=r.U[parent];h=parent[0];target=r.ops[h-1][1];g=d["g"]
                hist=ancestry_history(r,g,target);loss=last_A_loss(r,hist,r.boundaries[h-1]["post_A_time"])
                record={"source":s["name"],"original_parent":list(parent),"type":gaps[0]["type"],"g":g,"target":target,
                    "gap_multiplicity":len(gaps),"gaps":gaps,"parent_U_certificate":d,
                    "original_A_path":r.boundaries[h-1]["A_path"],"original_B_path":r.boundaries[h-1]["B_path"],
                    "ancestry_history":hist,"last_A_loss_not_a_payment":loss,
                    "A":r.A,"Q_B":r.Q,"old_first_hit_rows":[e for e in old_unpaid[s["name"]] if tuple(e["parent"])==parent]}
                actual_records.append(record)
                (omitted if record["type"]=="O" else missing).append(record)
            if s["name"]=="IH_p4_q1_L2_z5_c1":write("EXP03_PRIMARY_LIFECYCLE.json",primary_record(r,cl))
            inventory.append({"source":s["name"],"parent_interface":parents,"parents":actual_records})
        summaries.append({"source":s["name"],"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"],"R_unhandled":len(expected),
            "trace_hash":digest(r.events),"complete_paired_closure":r.closed,"independent_operations":r.independent_checks})
        independent_ops+=r.independent_checks
        print(f"{i+1:03d} {s['name']}: A={r.A} Q={r.Q} unhandled={len(expected)}",flush=True)
        del r
    assert len(all_sources)==171 and independent_ops==76474
    assert sum(s["parent_interface"]["gap_count"] for s in inventory)==14
    totals={k:sum(s["parent_interface"]["counts"][k] for s in inventory) for k in ("O","G","X")}
    write("EXP03_UNHANDLED_PARENT_INVENTORY.json",{"status":"FINITE_EXACT","inherited_sources":summaries,"sources_with_unhandled_parents":inventory,
        "totals":{"gaps":14,"parents":sum(totals.values()),"parent_types":totals},
        "universal_interface":"R_unhandled <= 3 (|P_O|+|P_G|+|P_X|); exact distinct original parent occurrences; no A bound inferred"})
    write("EXP03_OMITTED_HIT_EPISODES.json",{"stage":"initial exact inheritance; unified episodes follow","inherited_parent_records":omitted})
    write("EXP03_MISSING_GRANDPARENT_EPISODES.json",{"stage":"initial exact inheritance; actual/comparison divergence follows","inherited_parent_records":missing})
    write("EXP03_SOURCE_WITNESSES.json",{"inherited_sources":all_sources,"new_sources":[],"preservation":"Historical inputs read-only; complete initial/closing states and original words preserved."})
    meter.details.update(sources=171,independent_original_operations=independent_ops,unhandled_gaps=14,unhandled_parents=sum(totals.values()),parent_types=totals)
    meter.success=True
    print(json.dumps(meter.details,indent=2),flush=True)
