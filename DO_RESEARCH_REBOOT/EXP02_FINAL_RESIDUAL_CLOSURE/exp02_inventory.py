"""Stages 0--3: every inherited source, every exact remaining original R6."""
import time,json,hashlib,subprocess
from exp02_core import *
from exp01_diagnostics import incidence


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    old_archive=json.loads((OLD/"EXP01_SOURCE_WITNESSES.json").read_text())["sources"]
    old_results=json.loads((OLD/"EXP01_RESULTS.json").read_text())["results"]
    old_certs={x["source"]:x for x in json.loads((OLD/"EXP01_THEOREM_CERTIFICATES.json").read_text())["certificates"]}
    files=list(OLD.glob("*.py"))+[OLD/n for n in ("EXP01_DISCOVERY_REPORT.md","EXP01_RESULTS.json","EXP01_SOURCE_WITNESSES.json","EXP01_THEOREM_CERTIFICATES.json","EXP01_INCIDENCE_CERTIFICATES.json","EXP01_G_LIFECYCLE.json","EXP01_REPRODUCTION.md")]
    files += [ROOT.parent/n for n in ("RESEARCH_RULES.md","IAGS12_G0_QUANTITATIVE_BASELINE.md","IAGS12_D1_COLLISION_PROVENANCE.md","IAGS12_D2_RESIDUAL_REGENERATION_COST.md","IAGS12_D3_BLIND_GAP_COMPOSITION.md","IAGS12_D4_NEUTRAL_RENEWAL.md","IAGS12_D5_BRANCH_RENEWAL_COST.md","IAGS12_D6_INTERRUPTED_SCAN_COST.md","RG01_PRIMITIVE_ACCOUNTING.md","RG04_GLOBAL_REGENERATION.md","IAGS12_PARALLEL_B_BOUNDARY_SURCHARGE.md")]
    pins={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    write("EXP02_INPUT_MANIFEST.json",{"pins":pins,"HEAD":subprocess.check_output(["git","rev-parse","HEAD"],cwd=REPO,text=True).strip(),
        "authority":"current EXP-02 attachment; prior numerical runs are not borrowed as a new resource budget"})
    sources=[];inventory=[];adapts=[];ops=0
    for source,previous in zip(old_archive,old_results):
        assert source["name"]==previous["name"]
        r=Replay(source)
        assert digest(r.events)==source["trace_hash"]
        assert r.A==previous["A"] and r.Q==previous["Q_B"] and r.counts["R6"]==previous["R6"]
        direction,ret,other=residual(r)
        expected=next(c for c in old_certs[source["name"]]["certificates"] if c["direction"]==direction)
        cert=normalized_certificate(r,ret)
        assert cert==expected
        adapt=adaptive(r)
        resources=incidence(r,{"R6"})["edges"] if other else {}
        rows=[]
        for p in other:
            row=event_inventory(r,p,ret,adapt)
            row["original_A_root_entry_resources_not_payments"]=resources[str(p["rho"])]
            rows.append(row)
        other_ids={digest(p["rho"]) for p in other}
        paid=[p for p in other if p["rho"][0] in adapt["covered_consumers"]]
        left=[p for p in other if p["rho"][0] not in adapt["covered_consumers"]]
        assert len(paid)+len(left)==len(other_ids)
        Q=sum(w["actual_Q_B"] for w in adapt["windows"])
        assert len(paid)<=3*Q
        record={"source":source["name"],"family":source["family"],"population":len(r.keys),"M":sorted(r.M),"S":sorted(r.S),
            "A":r.A,"Q_B":r.Q,"R6":r.counts["R6"],"return_orientation":direction,"R6_return":len(ret["covered_R6"]),
            "R6_other":len(other),"adaptive_paid":len(paid),"after_adaptive":len(left),"E_J":adapt["E_J"],
            "global_original_A_gap_count":len(adapt["A_gap_witnesses"]),"independent_operation_checks":r.independent_checks,
            "trace_hash":digest(r.events),"paired_closed":r.closed}
        sources.append(record)
        inventory.append({"source":source["name"],"orientation":direction,"R6_other":len(other),"events":rows,
            "return_certificate":cert,"after_adaptive_events":left})
        adapts.append({**record,"adaptive_certificate":adapt})
        ops+=r.independent_checks
        print(f"{len(sources):03d} {source['name']}: R6={r.counts['R6']} return={len(ret['covered_R6'])} other={len(other)} adaptive={len(paid)} left={len(left)}",flush=True)
        assert time.process_time()-cpu<600,"inventory initial-stage CPU cap"
    assert len(sources)==133 and ops==55313
    g=next(i for i in inventory if i["source"]=="G_4_1_L31_r1_z1")
    assert g["R6_other"]==1 and g["events"][0]["adaptive_covered"]
    resource={"inventory_process_CPU_seconds":time.process_time()-cpu,"inventory_wall_seconds":time.perf_counter()-wall,
        "independently_checked_inherited_operations":ops,"inherited_sources":len(sources),"memory":memory(),
        "limits":{"new_sources":100,"population":513,"operations_per_source":20000,"recorded_Python_CPU_seconds":900},
        "initial_memory_probe_correction":"The first G-gate probe used an untyped Win32 handle and returned zeros. It was corrected before inventory; zeros are invalid measurements. The corrected G gate is rerun."}
    write("EXP02_REMAINING_R6_INVENTORY.json",{"status":"FINITE_EXACT","orientation_rule":"2*zero_based_rank(initial_B_root)<|S| => +1, otherwise -1; use ONE matching EXP01 certificate", "sources":inventory,"summary":sources,"resources":resource})
    write("EXP02_ADAPTIVE_DOMAIN_RESULTS.json",{"status":"FINITE_EXACT","sources":adapts,
        "totals":{k:sum(x[k] for x in sources) for k in ("R6","R6_return","R6_other","adaptive_paid","after_adaptive","E_J")},"resources":resource})
    write("EXP02_SOURCE_WITNESSES.json",{"inherited_sources":old_archive,"new_sources":[],"source_engine":"unchanged EXP01 exp01_oracle.py", "all_inherited_trace_hashes_verified":True})
    write("EXP02_RESOURCE_RECORD.json",resource)
    assert all(hashlib.sha256((REPO/p).read_bytes()).hexdigest()==h for p,h in pins.items())
    print(json.dumps({"totals":{k:sum(x[k] for x in sources) for k in ("R6","R6_return","R6_other","adaptive_paid","after_adaptive")},"resources":resource},indent=2),flush=True)
