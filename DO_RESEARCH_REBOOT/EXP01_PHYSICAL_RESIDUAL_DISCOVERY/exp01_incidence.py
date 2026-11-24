"""Exact finite fractional congestion on physically justified incidence edges."""
from collections import deque
from fractions import Fraction
import json,time
from pathlib import Path


class Flow:
    def __init__(self,n):
        self.g=[[] for _ in range(n)]
    def edge(self,u,v,c):
        a=[v,c,None,c];b=[u,0,a,0];a[2]=b
        self.g[u].append(a);self.g[v].append(b)
        return a
    def solve(self,s,t):
        total=0
        while True:
            level=[-1]*len(self.g);level[s]=0;q=deque([s])
            while q:
                u=q.popleft()
                for v,c,_,_ in self.g[u]:
                    if c and level[v]<0:
                        level[v]=level[u]+1;q.append(v)
            if level[t]<0:
                self.reachable={i for i,l in enumerate(level) if l>=0}
                return total
            ptr=[0]*len(self.g)
            def push(u,f):
                if u==t:
                    return f
                while ptr[u]<len(self.g[u]):
                    e=self.g[u][ptr[u]];v,c,back,_=e
                    if c and level[v]==level[u]+1:
                        z=push(v,min(f,c))
                        if z:
                            e[1]-=z;back[1]+=z;return z
                    ptr[u]+=1
                return 0
            while True:
                z=push(s,10**12)
                if not z:
                    break
                total+=z


def optimum(graph):
    adj=graph["edges"]
    ds=sorted(adj)
    rs=sorted({tuple(r) for vs in adj.values() for r in vs})
    if not ds:
        return {"minimum_fractional_max_load":{"numerator":0,"denominator":1},"flow":{},"tight_Hall_set":None}
    dn={d:i+1 for i,d in enumerate(ds)}
    rn={r:i+1+len(ds) for i,r in enumerate(rs)}
    sink=len(ds)+len(rs)+1
    lam=Fraction(0)
    tight=None
    iterations=0
    while True:
        iterations+=1
        net=Flow(sink+1)
        p,q=lam.numerator,lam.denominator
        edges={}
        for d in ds:
            net.edge(0,dn[d],q)
            for r in adj[d]:
                r=tuple(r);edges[(d,r)]=net.edge(dn[d],rn[r],len(ds)*q+1)
        for r in rs:
            net.edge(rn[r],sink,p)
        value=net.solve(0,sink)
        if value==len(ds)*q:
            result={d:[] for d in ds}
            loads={r:Fraction(0) for r in rs}
            for (d,r),e in edges.items():
                f=Fraction(e[3]-e[1],q)
                if f:
                    result[d].append({"resource":list(r),"numerator":f.numerator,"denominator":f.denominator})
                    loads[r]+=f
            assert all(sum(Fraction(e["numerator"],e["denominator"]) for e in vs)==1 for vs in result.values())
            assert max(loads.values())==lam
            return {"minimum_fractional_max_load":{"numerator":p,"denominator":q},
                "flow":result,"tight_Hall_set":tight,"integer_flow_queries":iterations}
        left=[d for d in ds if dn[d] in net.reachable]
        right=[r for r in rs if rn[r] in net.reachable]
        assert right
        lower=Fraction(len(left),len(right))
        assert lower>lam
        lam=lower
        tight={"left":left,"right":[list(r) for r in right],"demand":len(left),"resources":len(right)}


if __name__=="__main__":
    root=Path(__file__).resolve().parent
    cpu=time.process_time();wall=time.perf_counter()
    data=json.loads((root/"EXP01_RESULTS.json").read_text())
    output=[]
    for r in data["results"]:
        output.append({"source":r["name"],"R6":optimum(r["physical"]["root_entry_incidence_R6"]),
            "all_blind":optimum(r["physical"]["root_entry_incidence_all_blind"])})
    resources=data["resources"]
    resources["fractional_incidence_CPU_seconds"]=time.process_time()-cpu
    resources.setdefault("fractional_incidence_run_CPU_seconds",[]).append(resources["fractional_incidence_CPU_seconds"])
    resources["fractional_incidence_wall_seconds"]=time.perf_counter()-wall
    resources["total_recorded_process_cpu_seconds"]+=resources["fractional_incidence_CPU_seconds"]
    (root/"EXP01_INCIDENCE_CERTIFICATES.json").write_text(json.dumps({"certificates":output,
        "meaning":"Minimum exact fractional load in these finite source-justified root-entry graphs only. Tight Hall sets prove lower bounds; rational flows prove upper bounds. No universal charging rule is inferred."},indent=2,sort_keys=True)+"\n")
    (root/"EXP01_RESULTS.json").write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    (root/"EXP01_RESOURCE_RECORD.json").write_text(json.dumps(resources,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"source_graph_pairs":len(output),"CPU":resources["fractional_incidence_CPU_seconds"]}))
