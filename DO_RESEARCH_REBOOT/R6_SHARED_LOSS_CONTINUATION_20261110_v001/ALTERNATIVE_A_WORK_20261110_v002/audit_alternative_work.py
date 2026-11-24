"""Global alternative A-work audit on ALL original saved R6 demands."""
from pathlib import Path
import time,json,sys,traceback,hashlib
from collections import Counter,defaultdict
from bisect import bisect_left,bisect_right
from fractions import Fraction
START=time.process_time()
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
BASE_CPU=109.25
CAP=180.0
def save(name,x):(ROOT/name).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def sha(b):return hashlib.sha256(b).hexdigest()
def interval_match(ds,m,capacity):
    # Sort by right endpoint and use the earliest available resource.
    used=[0]*m;parent=list(range(m+1));ans={}
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    for d in sorted(ds,key=lambda d:(d["right"],d["left"],d["key"])):
        i=find(d["left"])
        if i>d["right"]:return None
        ans[d["key"]]=i;used[i]+=1
        if used[i]==capacity:parent[i]=find(i+1)
    return ans
def arbitrary_match(adj,m,capacity):
    owners=[[] for _ in range(m)]
    def add(d,seen):
        for r in adj[d]:
            if r in seen:continue
            seen.add(r)
            if len(owners[r])<capacity:
                owners[r].append(d);return True
            for i,old in enumerate(list(owners[r])):
                if add(old,seen):
                    owners[r][i]=d;return True
        return False
    for d in sorted(adj,key=lambda d:(len(adj[d]),d)):
        if not add(d,set()):return None
    return {d:r for r,ds in enumerate(owners) for d in ds}
def integer_congestion(adj,m):
    if not adj:return 0,{}
    hi=1
    while True:
        a=arbitrary_match(adj,m,hi)
        if a is not None:break
        hi*=2
        assert hi<=2*len(adj)
    lo=1
    while lo<hi:
        k=(lo+hi)//2
        a=arbitrary_match(adj,m,k)
        if a is None:lo=k+1
        else:hi=k
    return lo,arbitrary_match(adj,m,lo)
def work_density(ds,resources):
    # Every nonempty optimum can be shrunk to demand endpoints.
    keys=[e["promoted"] for e in resources]
    worst=Fraction(0);witness=None
    for a in sorted({d["minimum"] for d in ds}):
        for b in sorted({d["maximum"] for d in ds}):
            if b<a:continue
            demand=[d["key"] for d in ds if a<=d["minimum"] and d["maximum"]<=b]
            if not demand:continue
            count=bisect_right(keys,b)-bisect_left(keys,a)
            assert count>0,"source eligibility empty"
            ratio=Fraction(len(demand),count)
            if ratio>worst:
                worst=ratio;witness={"interval":[a,b],"demands":demand,"demand_count":len(demand),"actual_A_real_bits":count}
    return worst,witness
def analyze(source_path,cert_path):
    sb=source_path.read_bytes();cb=cert_path.read_bytes()
    s=json.loads(sb);c=json.loads(cb)
    summary=c["summary"];S=set(summary["S"])
    physical=sorted(map(int,s["initial_A"]["children"]))
    resources=sorted((e for e in c["all_physical_ancestry_events"] if e["actor"]=="A" and e["promoted"] in S),
                     key=lambda e:(e["promoted"],e["id"]))
    assert len({tuple(e["id"]) for e in resources})==len(resources)
    rkeys=[e["promoted"] for e in resources]
    U={tuple(d["id"]):d for d in c["R6_demand_records"]}
    ds=[];adj={}
    T=len(c["all_physical_ancestry_events"])
    for pair in summary["R6_events"]:
        outer=U[tuple(pair["rho"][2])]
        J=[k for i,k in enumerate(physical) if outer["J"]&(1<<i)]
        assert J and set(J)=={k for k in S if min(J)<=k<=max(J)}
        key=json.dumps(pair["rho"],separators=(",",":"))
        left=bisect_left(rkeys,min(J));right=bisect_right(rkeys,max(J))-1
        assert left<=right
        eligible=list(range(left,right+1))
        assert all(resources[i]["promoted"] in J for i in eligible)
        causal=[]
        for i in eligible:
            t=resources[i]["time"]
            if t<=outer["nu"]:t+=T
            if outer["nu"]<t<=outer["hit_time"]:causal.append(i)
        assert causal,"missing source-forced A promotion in actual outer life"
        adj[key]=causal
        ds.append({"key":key,"rho":pair["rho"],"outer_J":J,"minimum":min(J),"maximum":max(J),
                   "left":left,"right":right,"outer_birth":outer["nu"],"original_first_hit":outer["h"],
                   "hit_time":outer["hit_time"],"causal_choices":len(causal),"global_choices":len(eligible)})
    assert len(ds)==summary["R6"]
    density,witness=work_density(ds,resources)
    K=(density.numerator+density.denominator-1)//density.denominator if ds else 0
    assignment=interval_match(ds,len(resources),K) if K else {}
    assert assignment is not None
    if K>1:assert interval_match(ds,len(resources),K-1) is None
    causalK,causal_assign=integer_congestion(adj,len(resources))
    records=[];load=Counter();step=Counter();phase=Counter()
    for d in ds:
        i=assignment[d["key"]];e=resources[i]
        load[tuple(e["id"])]+=1;step[tuple(e["id"][:3])]+=1
        causal_t=e["time"]+(T if e["time"]<=d["outer_birth"] else 0)
        in_life=d["outer_birth"]<causal_t<=d["hit_time"]
        phase["within_original_life" if in_life else "outside_original_life"]+=1
        records.append({**d,"assigned_original_A_bit":e["id"],"promoted":e["promoted"],"sign":e["sign"],
                        "within_original_outer_life":in_life,
                        "causal_assignment_original_A_bit":resources[causal_assign[d["key"]]]["id"]})
    assert max(load.values(),default=0)<=K and max(step.values(),default=0)<=2*K
    return {"name":summary["name"],"A":summary["A"],"R6":summary["R6"],"Q_B":summary["Q_B"],
            "source_sha256":sha(sb),"certificate_sha256":sha(cb),"actual_S_promoting_A_bits":len(resources),
            "minimum_integer_global_bit_congestion":K,"minimum_integer_causal_bit_congestion":causalK,
            "exact_global_fractional_congestion":{"numerator":density.numerator,"denominator":density.denominator},
            "tight_key_interval":witness,"max_actual_A_real_bit_load":max(load.values(),default=0),
            "max_actual_A_StepEv_load":max(step.values(),default=0),"chosen_assignment_phases":dict(phase),
            "assignments":records}
def main():
    results=[];failure=None
    try:
        inventory=json.loads((PARENT/"GLOBAL_MULTIPLICITY_AUDIT.json").read_text())
        total=0
        for row in inventory["rows"]:
            if time.process_time()-START>CAP-BASE_CPU-4:raise RuntimeError("continued CPU ceiling reached")
            total+=row["R6"]
            if not row["R6"]:continue
            cp=PARENT/row["certificate"];idx=cp.stem.split("_")[-1]
            x=analyze(PARENT/f"source_{idx}.json",cp)
            results.append(x)
        assert total==inventory["R6_total"]==sum(x["R6"] for x in results)
        save("ALL_R6_ALTERNATIVE_WORK.json",{"status":"FINITE-EXACT ONLY","original_source_count":inventory["sources"],
            "sources_with_R6":len(results),"all_original_R6_count":total,"results":results,
            "universal_source_density":"UNPROVED","uniform_R6_bound":"OPEN"})
        print(json.dumps({"source_count":inventory["sources"],"sources_with_R6":len(results),"R6":total,
                          "max_global_bit_congestion":max(x["minimum_integer_global_bit_congestion"] for x in results),
                          "max_causal_bit_congestion":max(x["minimum_integer_causal_bit_congestion"] for x in results),
                          "max_StepEv_load":max(x["max_actual_A_StepEv_load"] for x in results)}),flush=True)
    except BaseException:
        failure=traceback.format_exc();print(failure,flush=True);save("FAILED.json",{"failure":failure})
    finally:
        cpu=time.process_time()-START
        save("RESOURCE_RECEIPT.json",{"prior_recorded_CPU_seconds":BASE_CPU,"new_process_CPU_seconds":cpu,
            "cumulative_recorded_CPU_seconds":BASE_CPU+cpu,"cumulative_ceiling":CAP,"source_replays":0,
            "saved_original_R6_audited":sum(x["R6"] for x in results),"failure":failure,
            "note":"Old receipts preserved; CPU includes saved-certificate decoding, physical event graph construction and exact combinatorial matching."})
        assert BASE_CPU+cpu<=CAP
    if failure:sys.exit(1)
if __name__=="__main__":main()

