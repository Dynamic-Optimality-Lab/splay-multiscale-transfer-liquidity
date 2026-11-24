"""Match complete physical double frames, never invent a shadow A donor."""
from exp02_distortion import *
from exp02_sources import interrupted_H,cheap_zero_Q_distortion
from exp01_sources import reflect


def subtree_state(tree,g):
    seen=set();todo=[g]
    while todo:
        k=todo.pop();seen.add(k)
        todo.extend(c for c in tree.ch[k] if c is not None)
    return {"root":g,"children":{str(k):list(tree.ch[k]) for k in sorted(seen)}}


def frame_records(state,target,expected_post):
    """Thin instrumentation of the EXISTING Tree rotations, checked against
    the complete post-state already independently certified in Stage D.
    No original source event stream is modified.
    """
    tree=Tree(state);j=0;ans={}
    while tree.par[target] is not None:
        j+=1;p=tree.par[target];g=tree.par[p];s=int(target>p)
        if g is None:
            tree.rotate(p,s);continue
        z=int(p>g);case=("R" if z else "L")+("R" if s else "L")
        frame=subtree_state(tree,g)
        ans[j]={"j":j,"g":g,"p":p,"target":target,"case":case,"frame":frame,
            "frame_hash":digest(frame),"external_parent":tree.par[g]}
        if s==z:
            tree.rotate(g,z);tree.rotate(p,s)
        else:
            tree.rotate(p,s);tree.rotate(g,z)
    assert tree.state()==expected_post
    return ans


def bridge_source(summary,inventory_rows):
    by_rho={digest(e["rho"]):e for e in inventory_rows}
    after=summary["assignments"]
    locations={};frames={};used_shadow={};out=[];Qshadow=sum(w["shadow_retained_Q"] for w in summary["windows"])
    for wi,w in enumerate(summary["windows"]):
        trace=json.loads((ROOT/w["physical_trajectory_file"]).read_text())
        pool=trace["state_pool"]
        for access in trace["retained_accesses"]:
            t=access["original_operation"]
            actual=frame_records(pool[access["actual_pre"]["state_sha256"]],access["target"],pool[access["actual_post"]["state_sha256"]])
            shadow=frame_records(pool[access["shadow_pre"]["state_sha256"]],access["target"],pool[access["shadow_post"]["state_sha256"]])
            frames[t]=(wi,actual,shadow)
    for item in after:
        row=by_rho[digest(item["rho"])];h=item["consumer"];parent=tuple(row["parent"])
        record={"rho":row["rho"],"original_parent":list(parent),"consumer":h}
        if h in frames:
            wi,actual,shadow=frames[h]
            actual_frame=actual[parent[1]]
            assert actual_frame["g"]==row["parent_certificate"]["g"]
            assert actual_frame["case"]==row["parent_certificate"]["case"]
            matches=[v for v in shadow.values() if v["frame_hash"]==actual_frame["frame_hash"] and v["case"]==actual_frame["case"] and v["p"]==actual_frame["p"]]
            assert len(matches)<=1
            if matches:
                dest=(wi,h,matches[0]["j"])
                assert dest not in used_shadow or used_shadow[dest]==parent
                used_shadow[dest]=parent
                record.update(category="frame_matched_retained",shadow_double=list(dest),
                    complete_frame_hash=actual_frame["frame_hash"],frame_root=actual_frame["g"],
                    original_external=actual_frame["external_parent"],shadow_external=matches[0]["external_parent"])
            else:
                record.update(category="unmatched_retained",actual_frame=actual_frame,
                    available_shadow_frames=[{k:v for k,v in sf.items() if k!="frame"} for sf in shadow.values()])
        elif item["category"]=="synchronized_omitted":
            record.update(category="synchronized_omitted",original_A_StepEv=list(parent))
        else:
            record.update(category=item["category"])
        out.append(record)
    loads=Counter(tuple(x["shadow_double"]) for x in out if x["category"]=="frame_matched_retained")
    assert max(loads.values(),default=0)<=3
    assert sum(loads.values())<=3*Qshadow
    counts=Counter(x["category"] for x in out)
    paid=counts["frame_matched_retained"]+counts["synchronized_omitted"]
    return {"source":summary["source"],"origin":summary["origin"],"population":summary["population"],
        "A":summary["A"],"Q_B":summary["Q_B"],"R6_other":summary["R6_other"],
        "adaptive_paid":summary["adaptive_paid"],"bridge_paid":paid,"remaining":len(out)-paid,
        "counts":dict(counts),"events":out,"max_shadow_double_load":max(loads.values(),default=0),
        "proof_coverage":"original R6_other = adaptive + bridge + explicitly unmatched; no reclassification of original gaps"}


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    archive=json.loads((ROOT/"EXP02_SOURCE_WITNESSES.json").read_text())
    data=json.loads((ROOT/"EXP02_INTERRUPTION_DISTORTION_RESULTS.json").read_text())
    inventory=json.loads((ROOT/"EXP02_REMAINING_R6_INVENTORY.json").read_text())
    adapters=json.loads((ROOT/"EXP02_ADAPTIVE_DOMAIN_RESULTS.json").read_text())
    resource=json.loads((ROOT/"EXP02_RESOURCE_RECORD.json").read_text())
    # Independent tests put the first hit INSIDE the omitted operation rather
    # than after it. The prior suffix-interruption corpus did not test this.
    extra=[interrupted_H(p,2,(z,)) for p,z in ((3,5),(4,5),(5,5),(6,5),(5,7),(5,11),(4,1),(4,2))]
    extra += [interrupted_H(4,2,(5,),q=2),reflect(interrupted_H(4,2,(5,)))]
    aux=cheap_zero_Q_distortion();aux["operations"][4][0]="D"
    aux.update(name="zig_distortion_auxiliary_closed_control",family="auxiliary_closure_control")
    extra.append(aux)
    new_ops=0
    for src in extra:
        r=Replay(src);direction,ret,other=residual(r);ad=adaptive(r);z=source_distortion(r,other,ad)
        z.update(origin="EXP02",population=len(r.keys),family=src["family"],R6=r.counts["R6"],R6_return=len(ret["covered_R6"]),
            adaptive_paid=len(other)-z["after_adaptive"],P_A=r.PA,N_A=r.NA,D_B=r.DB,
            actual_A_real_rotations=2*r.A-r.VA,full_source_paired_closed=True,
            independent_actual_operation_checks=r.independent_checks)
        data["sources"].append(z)
        inventory["new_sources"].append({"source":src["name"],"orientation":direction,"R6_other":len(other),"events":[event_inventory(r,p,ret,ad) for p in other]})
        adapters["new_sources"].append({"source":src["name"],"adaptive_certificate":ad})
        archive["new_sources"].append({**src,"closing_A":r.a.state(),"closing_B":r.b.state(),"trace_hash":digest(r.events),
            "costs":{"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"],"R6_other":len(other)}})
        new_ops+=r.independent_checks
        print("additional",src["name"],"other",len(other),"delta",z["sum_signed_delta"],flush=True)
    lookup={s["source"]:s["events"] for s in inventory["sources"]+inventory["new_sources"]}
    result=[]
    for s in data["sources"]:
        b=bridge_source(s,lookup[s["source"]]);result.append(b)
        if b["remaining"]:print("UNMATCHED",b["source"],b["remaining"],b["counts"],flush=True)
    write("EXP02_FRAME_BRIDGE_CERTIFICATES.json",{"sources":result,"finite_only":True,
        "symbolic_theorem":"See report: complete physical double-frame injection + original three-slot bound; disjoint original A intervals control shadow operand populations."})
    resource.update(frame_bridge_CPU_seconds=time.process_time()-cpu,frame_bridge_wall_seconds=time.perf_counter()-wall,
        frame_bridge_peak_memory=memory(),frame_bridge_additional_original_operations=new_ops,
        new_complete_sources=len(archive["new_sources"]),new_source_operations=sum(len(s["operations"]) for s in archive["new_sources"]))
    resource["recorded_CPU_subtotal"]+=resource["frame_bridge_CPU_seconds"]
    assert resource["recorded_CPU_subtotal"]<900 and resource["new_complete_sources"]<=100
    data["resources"]=resource
    write("EXP02_INTERRUPTION_DISTORTION_RESULTS.json",data)
    write("EXP02_REMAINING_R6_INVENTORY.json",inventory);write("EXP02_ADAPTIVE_DOMAIN_RESULTS.json",adapters)
    write("EXP02_SOURCE_WITNESSES.json",archive);write("EXP02_RESOURCE_RECORD.json",resource)
    print(json.dumps({"all_sources":len(result),"new_sources":len(archive["new_sources"]),"remaining":sum(r["remaining"] for r in result),"resource":resource},indent=2),flush=True)
