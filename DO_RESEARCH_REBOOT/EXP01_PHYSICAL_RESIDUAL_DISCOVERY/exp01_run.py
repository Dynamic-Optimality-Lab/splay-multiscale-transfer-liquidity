"""Deterministic staged EXP-01 corpus. Run with python -B exp01_run.py."""
import json
import os
from pathlib import Path
import subprocess
import time
import hashlib
from fractions import Fraction
from exp01_oracle import Replay,Tree,digest
from exp01_sources import H,W,G,W_star,H_dec,lifted_H,I_m_Z,warm_local,warm_marked,reflect,detour_H,cyclic_cut,campaign15,ops
from exp01_diagnostics import physical_diagnostics,return_zig_reduction,lifecycle
from exp01_validate import validation

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def inputs():
    paths=list((REPO/"DO_RESEARCH_REBOOT").glob("IAGS12*.md"))
    paths += [REPO/"DO_RESEARCH_REBOOT"/n for n in ("RESEARCH_RULES.md","RG01_PRIMITIVE_ACCOUNTING.md","RG04_GLOBAL_REGENERATION.md")]
    paths += [REPO/p for p in (
        "python/liquidity/legacy_embedding.py","python/independent/splay.py",
        "DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md",
        "DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md")]
    for directory in ("ROUTE02_ROUTE04_TF2_AUDIT_AMPLIFICATION_20261109","ROUTE02_ROUTE04_UNIVERSAL_SOURCE_WORK_20261109","ROUTE02_ROUTE04_REGENERATION_CONTINUATION_20261109"):
        paths += list((REPO/"DO_RESEARCH_REBOOT"/directory).glob("*.md"))
    for directory,names in (("SE03_STEP2_CD6_FINAL_ASSEMBLY_14",("SOURCE_SPEC.md","FINAL_VERDICT.md","FULL_PROOF.md","CD6_FINAL_CERTIFICATE.json")),
        ("SE03_STEP3_UNIFORM_DONOR_GROUPING_15",("SOURCE_SPEC.md","FINAL_VERDICT.md","ZERO_RUN_FAMILY_THEOREM.md","SOURCE_REPLAY.md","leaf_source_certificates2.json","zero_run_source_certificates.json","AUDIT_CAP_CHECKPOINT.md"))):
        paths += [REPO/"DO_RESEARCH_REBOOT"/directory/n for n in names]
    return {str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def reaching_check(src):
    prefix=src.get("reaching_prefix",[])
    if not prefix:
        assert src["initial_A"]==src["initial_B"]
        return {"operations":0,"excluded_A":0}
    diagonal=src["diagonal_initial"]
    a,b=Tree(diagonal),Tree(diagonal)
    cost=0
    for tag,x in prefix:
        cost+=len(a.path(x))//2
        Replay.plain_splay(a,x)
        if tag=="K":
            Replay.plain_splay(b,x)
    assert a.state()==src["initial_A"] and b.state()==src["initial_B"]
    return {"operations":len(prefix),"excluded_A":cost}


def corpus():
    out=[]
    # Discovery controls. Bounded generations, population and genuine supports.
    out += [H(p) for p in range(1,7)]
    out += [H(p,q) for p in (2,3,4) for q in (2,3)]
    out += [W(p,q) for p in (2,3,4,5) for q in (1,2)]
    out += [W(3,hit=k) for k in (3,5,7)]+[W_star(),H_dec()]
    out += [G(4,1,L,r) for L in (3,7,11,15,23,31) for r in (1,2,4)]
    out += [G(5,1,L,r) for L in (11,31,63) for r in (1,2)]
    out += [G(6,1,L) for L in (35,63,95,127)]
    out += [G(4,1,31,reset=z) for z in (2,15,30,32,65)]
    # A-only preparation and helpers: no claim that U memberships survive.
    for prep in (0,7,31):
        s=G();s["operations"]=s["operations"][64-prep:]
        # Rebuild partial preparation exactly, rather than preserve a suffix
        # with unintended starting key. Full closing scans ensure closure.
        baseline=G();s["operations"]=ops("D",range(2,prep+2))+baseline["operations"][64:]
        s.update(name=f"G_partial_prep_{prep}",family="G_partial_prep")
        out.append(s)
    for helpers in ([11,10],[33,2],[65,1],[40,20,10]):
        s=G();s["operations"][131:131]=ops("D",helpers)
        s.update(name="G_helpers_"+"_".join(map(str,helpers)),family="G_helpers")
        out.append(s)
    # Independent falsification: detours, repeated complete copies, cuts,
    # physical fringe lifts, warmed sources, reflections, actual C15 fixtures.
    for p in (4,5,6):
        n=2**(p+2)+1
        for positions in ((15,),(31,),tuple(range(7,n-1,8))):
            out.append(detour_H(p,positions=positions))
    out += [detour_H(4,positions=(31,),copies=c) for c in (2,4,8)]
    out += [detour_H(4,q=2,positions=(31,)),detour_H(5,q=2,positions=(31,))]
    for copies in (2,4):
        s=detour_H();s.update(name=f"DH_complete_repeats_{copies}",family="DH_repeats",operations=s["operations"]*copies)
        out.append(s)
    out += [lifted_H(p,r=r) for p in (2,3,4) for r in (2,3)]
    out += [I_m_Z(m) for m in (2,4,8)]
    out += [warm_marked(p,q) for p,q in ((4,1),(4,3),(6,1))]
    out += [warm_local(L,r) for L in (7,15) for r in (2,4)]
    out += campaign15()
    out += [reflect(s) for s in (G(),detour_H(),H(6),W_star(),W(3,hit=5),lifted_H(4))]
    return out


def run():
    wall=time.perf_counter();cpu=time.process_time()
    pins=inputs()
    write("EXP01_INPUT_MANIFEST.json",{"files":pins,"branch":subprocess.check_output(["git","branch","--show-current"],cwd=REPO,text=True).strip(),
        "HEAD":subprocess.check_output(["git","rev-parse","HEAD"],cwd=REPO,text=True).strip(),
        "read_scope":"Relevant mathematical passages read directly; complete files byte-pinned. No claim to re-audit all transitive historical proofs."})
    vc=time.process_time()
    checks=validation()
    validation_cpu=time.process_time()-vc
    print(f"Stage 0 PASS: {len(checks)} anchors; CPU {validation_cpu:.3f}s",flush=True)
    sources=corpus()
    results=[];witnesses=[]
    seen=set()
    index=0
    while index<len(sources):
        src=sources[index];index+=1
        if src["name"] in seen:
            continue
        seen.add(src["name"])
        assert len(seen)<=200 and len(src["initial_A"]["children"])<=257 and len(src["operations"])<=20000
        assert time.process_time()-cpu<600,"EXP01 main-run self-imposed CPU limit"
        t0=time.process_time()
        reach=reaching_check(src)
        r=Replay(src)
        summary=r.summary()
        summary["family"]=src["family"]
        summary["reachability_check"]=reach
        summary["physical"]=physical_diagnostics(r)
        summary["zig_return_reductions"]=[return_zig_reduction(r,d) for d in (1,-1)]
        # Separate original phase costs where the constructor supplies a boundary.
        if src["family"]=="G":
            n=len(r.keys);prep=n-1;descent=n;early=src["r"]*(src["L"]+1)
            cuts=[0,prep,prep+descent,prep+descent+early,prep+descent+early+n,len(r.ops)]
            summary["phase_costs"]={label:{"A":sum(b["a"] for b in r.boundaries[lo:hi]),"Q_B":sum(b["q"] for b in r.boundaries[lo:hi])}
                for label,lo,hi in zip(("preparation","descent","active_scan_and_reset","restoration_increasing","restoration_reverse"),cuts,cuts[1:])}
        if "inner_length" in src:
            cut=src["inner_length"]*src["r"]
            summary["phase_costs"]={"inner":{"A":sum(b["a"] for b in r.boundaries[:cut]),"Q_B":sum(b["q"] for b in r.boundaries[:cut])},
                "restoration":{"A":sum(b["a"] for b in r.boundaries[cut:]),"Q_B":sum(b["q"] for b in r.boundaries[cut:])}}
        summary["process_cpu_seconds"]=time.process_time()-t0
        results.append(summary)
        witnesses.append({**src,"closing_A":r.a.state(),"closing_B":r.b.state(),
            "costs":{"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"]},"trace_hash":summary["trace_hash"],
            "R6_certificates":[{**p,"endpoints":[r.U[tuple(p["rho"][j])] for j in (1,2)],
                "renewed_demand":r.U[tuple(p["parent"])]} for p in r.pairs if p["class"]=="R6"]})
        if src["name"]==G()["name"]:
            write("EXP01_G_LIFECYCLE.json",lifecycle(r))
            for cut in (65,129,160,161):
                sources.append(cyclic_cut(src,r,cut))
        if src["name"]==detour_H()["name"]:
            for cut in (65,129,160):
                sources.append(cyclic_cut(src,r,cut))
        print(f"{len(results):03d} {src['name']}: A={r.A} Q={r.Q} R6={r.counts['R6']} cpu={summary['process_cpu_seconds']:.3f}",flush=True)
        # Durable checkpoint: every completed row is paired-closed and certified.
        write("EXP01_RESULTS.checkpoint.json",{"status":"RUNNING","results":results})
    assert inputs()==pins,"a pinned historical input changed during execution"
    resource={"main_run_process_cpu_seconds":time.process_time()-cpu,"wall_seconds":time.perf_counter()-wall,
        "validation_cpu_seconds":validation_cpu,"source_count":len(results),
        "total_operations":sum(x["operations"] for x in results),
        "independent_operation_checks":sum(x["independent_operation_checks"] for x in results),
        "limits":{"population":257,"sources":200,"operations_per_source":20000,"main_run_CPU_seconds":600},
        "prior_exploratory_runs":"One validation invocation and two small reporting probes preceded the timed canonical run; their exact process CPU was not instrumented. Canonical run repeats all claims. No historical resource budget used.",
        "seed":"deterministic grid, no random sampling"}
    write("EXP01_RESULTS.json",{"status":"FINITE_EXACT","oracle_validation":checks,"resources":resource,"results":results})
    write("EXP01_SOURCE_WITNESSES.json",{"schema":"EXP01 complete physical sources v1","sources":witnesses,
        "reconstruction":"python -B exp01_inspect.py NAME --trace (default writes only into this isolated folder)",
        "event_sort":"actor, original operation, StepEv, real bit; numeric timeline separately recorded"})
    write("EXP01_RESOURCE_RECORD.json",resource)
    write("EXP01_RESULTS.checkpoint.json",{"status":"INITIAL_GRID_COMPLETE","superseded_by":"EXP01_RESULTS.json","results":results})
    print(json.dumps(resource,indent=2),flush=True)


if __name__=="__main__":
    run()
