"""Three prespecified cross-chain controls; no old artifact is changed."""
from pathlib import Path
import sys,time,json,traceback
START=time.process_time();ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]/"EXP01_PHYSICAL_RESIDUAL_DISCOVERY"))
from exp01_sources import H
from exp01_oracle import Replay
from audit_alternative_work import analyze
def save(name,x):(ROOT/name).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
receipt=json.loads((ROOT/"RESOURCE_RECEIPT.json").read_text());prior=receipt["cumulative_recorded_CPU_seconds"]
records=[];failure=None
try:
    for p,q in ((3,3),(4,3),(5,3)):
        if time.process_time()-START>180-prior-5:raise RuntimeError("continued CPU ceiling")
        src=H(p,q);N=len(src["initial_A"]["children"])
        bs=[N-2**p*(2*i+1) for i in range(q+1)]
        for b in bs:
            t=2*N-b
            assert src["operations"][t-1]==["D",b];src["operations"][t-1]=["K",b]
        src.update(name=f"multichain_first_hit_p{p}_q{q}",family="multichain_first_hit",b_values=bs)
        r=Replay(src,independent=True)
        assert r.A==4*(N-1) and r.VA==r.A
        selected=[];preps=[];restores=[];immediate=[]
        for i,b in enumerate(bs):
            h=2*N-b
            for j in range(1,p-1):
                a=(N-1+2**j,2**(p-j-1)*(2*i+1))
                c=(N-1+2**(j+1),2**(p-j-2)*(2*i+1))
                pair=next(x for x in r.pairs if x["rho"]==[h,list(a),list(c)])
                assert pair["class"]=="R6"
                seed=b-2**(j+1);prep=["A",seed,1,0];restore=["A",4*N-seed,1,0]
                nxt=["A",N+2**(j+1),1,0]
                assert r.event_by_id[tuple(prep)]["sign"]==1
                assert r.event_by_id[tuple(restore)]["sign"]==1
                assert r.event_by_id[tuple(nxt)]["target"]>b
                preps.append(tuple(prep));restores.append(tuple(restore));immediate.append(tuple(nxt))
                selected.append({"rho":pair["rho"],"preparation":prep,"restoration":restore,"immediate_after_producer":nxt})
        assert len(selected)==(q+1)*(p-2)
        assert len(set(preps))==len(preps) and len(set(restores))==len(restores)
        from collections import Counter
        assert max(Counter(immediate).values())==q+1
        tag=f"p{p}_q{q}"
        save("SOURCE_multi_"+tag+".json",src)
        cert={"summary":r.summary(),"R6_demand_records":list(r.U.values()),"all_physical_ancestry_events":r.events}
        save("CERTIFICATE_multi_"+tag+".json",cert)
        audit=analyze(ROOT/("SOURCE_multi_"+tag+".json"),ROOT/("CERTIFICATE_multi_"+tag+".json"))
        assert audit["minimum_integer_global_bit_congestion"]==1
        record={"name":src["name"],"p":p,"q":q,"A":r.A,"R6":r.counts["R6"],"selected_R6":len(selected),
            "immediate_after_producer_max_load":q+1,"preparation_max_load":1,"restoration_max_load":1,
            "global_real_bit_congestion":audit["minimum_integer_global_bit_congestion"],"selected":selected,
            "source":"SOURCE_multi_"+tag+".json","certificate":"CERTIFICATE_multi_"+tag+".json",
            "global_assignments":audit}
        records.append(record)
        print(json.dumps({k:record[k] for k in ("name","A","R6","selected_R6","immediate_after_producer_max_load","preparation_max_load","restoration_max_load")}),flush=True)
    save("CROSS_CHAIN_CONTROLS.json",{"status":"FINITE-EXACT; general formula proved in report","records":records})
except BaseException:
    failure=traceback.format_exc();print(failure,flush=True);save("FAILED_CROSS_CHAIN.json",{"failure":failure})
finally:
    cpu=time.process_time()-START
    receipt.setdefault("continuations",[]).append({"phase":"prespecified_cross_chain_overlap","process_CPU_seconds":cpu,
        "new_source_replays":len(records),"failure":failure})
    receipt["cumulative_recorded_CPU_seconds"]=prior+cpu
    receipt["total_new_source_replays"]=8+len(records)
    save("RESOURCE_RECEIPT.json",receipt);assert prior+cpu<=180
if failure:sys.exit(1)

