import time
from exp02_core import *
from exp01_sources import G

if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    r=Replay(G())
    d,ret,other=residual(r)
    assert any(p["rho"]==[132,[72,3],[80,1]] for p in other)
    bs=blocks(r)
    i=next(i for i,b in enumerate(bs) if b["ts"][0]==130)
    tree=Tree(r.boundaries[129]["pre_B"])
    ts=list(range(130,161));targets=list(range(1,32))
    J=sorted(closure(tree,targets))
    window={"operations":ts,"targets":targets,"J":J,"domain_size":len(J),"ell":31,
        "threshold":(len(J)+1)//2+1,"initial_B":tree.state(),"anchor":130,
        "initial_paths":{str(x):tree.path(x) for x in targets}}
    order=sorted(J)[:31]==targets
    eligible=order and min(J)==1 and 31>=window["threshold"]
    if eligible:verify_window(r,window)
    write("EXP02_G_ADAPTIVE_GATE.json",{"source":r.source,"original_costs":{"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"]},
        "EXP01_orientation":d,"R6_other":other,"candidate_window":window,"consecutive_J_ranks":order,
        "extreme_anchored":min(J)==1,"eligible":eligible,"consumer_in_window":132 in ts,
        "CPU_seconds":time.process_time()-cpu,"wall_seconds":time.perf_counter()-wall,"memory":memory()})
    print(json.dumps({"G_J":J,"domain_size":len(J),"ell":31,"threshold":window["threshold"],"eligible":eligible,
        "actual_Q":window.get("actual_Q_B"),"CPU":time.process_time()-cpu,"memory":memory()},indent=2))
