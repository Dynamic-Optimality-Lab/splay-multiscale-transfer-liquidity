"""Meaningful gate checks: independent transitions and historical anchors."""
import json
from exp01_oracle import Replay, Tree, vine
from exp01_sources import H,W,G,W_star,H_dec,lifted_H,detour_H


def validation():
    checks=[]
    def ok(name,condition):
        assert condition,name
        checks.append(name)
    # Independent engines on all four orientations and a terminal zig.
    from exp01_sources import source
    shapes=[(3,{"1":[None,2],"2":[None,None],"3":[1,None]},2,"LR"),
        (1,{"1":[None,3],"2":[None,None],"3":[2,None]},2,"RL")]
    for root,ch,x,case in shapes:
        tr=Tree({"root":root,"children":ch})
        Replay.plain_splay(tr,x)
        ok(case+" hand shape",tr.state()=={"root":2,"children":{"1":[None,None],"2":[1,3],"3":[None,None]}})
    src=source("hand",3,[["K",3],["K",2],["K",1]])
    rr=Replay(src)
    ok("RR one double, terminal zigs and closure",(rr.A,rr.Q,rr.VA)==(3,1,2))
    for p in range(1,5):
        rr=Replay(H(p))
        n=len(rr.keys)
        ok(f"H{p} all-A-zig cost",rr.A==4*(n-1) and rr.VA==rr.A)
        hit=2*n+2
        selected=[(n-1+2**j,2**(p-j)*2-1) for j in range(1,p+1)]
        ok(f"H{p} complete selected cohort",rr.cohorts[hit]==selected)
    rr=Replay(W_star())
    ok("W_star exact full costs",len(rr.ops)==235 and rr.A==282)
    ok("W_star full-Pi exclusion",(72,3) not in rr.U and (34,7) in rr.U and (76,1) in rr.U)
    ok("W_star intermediate separator",any(p["rho"]==[173,[34,7],[76,1]] and p["class"]=="R_sep" for p in rr.pairs))
    rr=Replay(H_dec())
    ok("H_dec exact cost",rr.A==139)
    ok("H_dec two gaps same decreasing bit",sum(p["beta"]==["B",70,1,0] and p["class"]=="R_dec" for p in rr.pairs)==2)
    rr=Replay(W(3,hit=5))
    ev=rr.event_by_id[("B",41,2,1)]
    ok("W5 same-hit edge recreation",[10,6,0] in [list(x) for x in ev["added"]])
    rr=Replay(G())
    witness=next(p for p in rr.pairs if p["rho"]==[132,[72,3],[80,1]])
    ok("G 290 original operations",len(rr.ops)==290)
    ok("G original residual witness",witness["class"]=="R6" and witness["beta"]==["B",132,2,0])
    ok("G receiver full cohort",rr.cohorts[140]==[(66,13),(68,6),(132,2)])
    ok("G reset exact cost and full path",rr.boundaries[160]["a"]==15 and len(rr.boundaries[160]["A_path"])==31)
    close=sum(b["a"] for b in rr.boundaries[161:226])
    ok("G full closing cost decomposition",rr.A==237+close)
    rr=Replay(lifted_H(4,r=2))
    ok("D6 full fringe coverage nonempty",rr.counts["R_fringe"]>=1)
    rr=Replay(detour_H())
    ok("cheap detour paired closure and all-A-zigs",rr.A==258 and rr.VA==rr.A)
    ok("cheap detour G anchor still R6",any(p["rho"]==[132,[72,3],[80,1]] and p["class"]=="R6" for p in rr.pairs))
    return checks


if __name__=="__main__":
    print(json.dumps({"passed":validation()},indent=2))
