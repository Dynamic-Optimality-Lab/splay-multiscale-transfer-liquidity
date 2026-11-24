"""Targeted all-R6 locality falsification; original sources are not edited."""
from pathlib import Path
import sys,time,json,traceback
START=time.process_time()
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
sys.path.insert(0,str(ROOT.parents[1]/"EXP01_PHYSICAL_RESIDUAL_DISCOVERY"))
from exp01_oracle import Replay
from exp01_sources import H,reflect
from audit_alternative_work import analyze
def save(name,x):(ROOT/name).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
receipt=json.loads((ROOT/"RESOURCE_RECEIPT.json").read_text())
prior=receipt["cumulative_recorded_CPU_seconds"]
def make(p):
    s=H(p);N=len(s["initial_A"]["children"]);b=N-2**p;h=2*N-b
    assert s["operations"][h-1]==["D",b]
    s["operations"][h-1]=["K",b]
    s.update(name=f"descending_first_hit_p{p}",family="descending_first_hit",p=p,b=b,h=h)
    return s
results=[];failure=None
try:
    for p in (3,4,5,6):
        base=make(p)
        for mirrored in (False,True):
            if time.process_time()-START>180-prior-5:raise RuntimeError("cumulative CPU ceiling")
            s=reflect(base) if mirrored else base
            r=Replay(s,independent=True)
            N=len(r.keys);h=base["h"]
            assert r.A==4*(N-1) and r.VA==r.A
            assert r.counts["R6"]==p-2
            pairs=[q for q in r.pairs if q["class"]=="R6"]
            assert all(q["rho"][0]==h for q in pairs)
            b=base["b"];selected=[]
            for j in range(1,p-1):
                a=(N-1+2**j,2**(p-j-1))
                c=(N-1+2**(j+1),2**(p-j-2))
                pair=next(q for q in pairs if q["rho"]==[h,list(a),list(c)])
                sidx=(j+1)//2
                assert pair["beta"]==["B",h,sidx,0]
                seed=b-2**(j+1)
                prepared=b-2**(j+1)+1
                assert r.event_by_id["A",prepared-1,1,0]["sign"]==1
                assert r.event_by_id["A",4*N-seed,1,0]["sign"]==1
                selected.append({"rho":pair["rho"],"actual_preparation":["A",prepared-1,1,0],
                    "actual_restoration":["A",4*N-seed,1,0]})
            cert={"summary":r.summary(),"R6_demand_records":list(r.U.values()),
                  "all_physical_ancestry_events":r.events}
            tag=f"p{p}_"+("reflected" if mirrored else "original")
            sp=ROOT/("SOURCE_"+tag+".json");cp=ROOT/("CERTIFICATE_"+tag+".json")
            save(sp.name,s);save(cp.name,cert)
            audit=analyze(sp,cp)
            assert audit["minimum_integer_global_bit_congestion"]==1
            assert audit["minimum_integer_causal_bit_congestion"]==p-2
            assert all(d["causal_choices"]==1 for d in audit["assignments"])
            assert {tuple(d["causal_assignment_original_A_bit"]) for d in audit["assignments"]}=={("A",h,1,0)}
            audit["actual_preparation_restoration"]=selected
            audit["source"]=sp.name;audit["certificate"]=cp.name
            results.append(audit)
            print(json.dumps({"source":s["name"],"A":r.A,"R6":r.counts["R6"],"h":h,
                "global_congestion":1,"causal_congestion":p-2,"unique_causal_event":["A",h,1,0]}),flush=True)
    save("DESCENDING_FIRST_HIT_COUNTEREXAMPLES.json",{"status":"FINITE-EXACT controls; all-p argument in report",
        "scope":"Counterexample to an in-label AND in-lifetime A pool, not to R6<=cA","results":results})
except BaseException:
    failure=traceback.format_exc();print(failure,flush=True);save("FAILED_LOCALITY.json",{"failure":failure})
finally:
    cpu=time.process_time()-START
    receipt.setdefault("continuations",[]).append({"phase":"descending_first_hit","process_CPU_seconds":cpu,
        "new_source_replays":len(results),"operations":sum(json.loads((ROOT/r["source"]).read_text())["operations"].__len__() for r in results),"failure":failure})
    receipt["cumulative_recorded_CPU_seconds"]=prior+cpu
    receipt["total_new_source_replays"]=len(results)
    save("RESOURCE_RECEIPT.json",receipt)
    assert prior+cpu<=180
if failure:sys.exit(1)

