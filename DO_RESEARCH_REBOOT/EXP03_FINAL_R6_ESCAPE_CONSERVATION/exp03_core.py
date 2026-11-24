"""Read-only imports of the validated original engines and selectors."""
from pathlib import Path
import sys,json,hashlib,atexit,time as timing
from collections import Counter,defaultdict
from fractions import Fraction

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/"EXP02_FINAL_RESIDUAL_CLOSURE"
OLDER=ROOT.parent/"EXP01_PHYSICAL_RESIDUAL_DISCOVERY"
REPO=ROOT.parent.parent
sys.path.insert(0,str(OLD));sys.path.insert(0,str(OLDER))
import exp02_core as inherited_core
import exp02_distortion as inherited_distortion
import exp02_frame_bridge as inherited_frame
from exp01_oracle import Replay,Tree,closure,digest,vine
from exp01_sources import H,W,G,source,ops,reflect
from exp02_sources import interrupted_H
from exp02_core import orientation,residual,blocks,adaptive,A_gap,memory,event_inventory
from exp02_distortion import select_shadow_windows,analyze_shadow
from exp02_frame_bridge import frame_records

# Redirect new diagnostic outputs only; historical files/modules stay immutable.
inherited_distortion.ROOT=ROOT
inherited_frame.ROOT=ROOT


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")


class Meter:
    def __init__(self,stage):
        self.stage=stage;self.cpu=timing.process_time();self.wall=timing.perf_counter();self.success=False;self.details={}
        atexit.register(self.finish)
    def finish(self):
        record={"stage":self.stage,"status":"completed" if self.success else "failed_or_interrupted",
            "process_CPU_seconds":timing.process_time()-self.cpu,"wall_seconds":timing.perf_counter()-self.wall,
            "memory":memory(),**self.details}
        write("EXP03_RESOURCE_"+self.stage+".json",record)


def current_classification(r,save=True):
    d,ret,other=residual(r);ad=adaptive(r)
    z=inherited_distortion.source_distortion(r,other,ad,save=save)
    z.update(origin="EXP03",population=len(r.keys),family=r.source.get("family","supplied"),
        R6=r.counts["R6"],R6_return=len(ret["covered_R6"]),adaptive_paid=len(other)-z["after_adaptive"])
    rows=[event_inventory(r,p,ret,ad) for p in other]
    raw=inherited_frame.bridge_source(z,rows)
    # The final EXP-02 rule is common GRANDPARENT, not equal whole frame.
    final=[];destinations={}
    for old in raw["events"]:
        e=dict(old)
        if e["category"]=="frame_matched_retained":e["category"]="common_grandparent_retained"
        elif e["category"]=="unmatched_retained":
            g=e["actual_frame"]["g"]
            matches=[s for s in e["available_shadow_frames"] if s["g"]==g]
            assert len(matches)<=1
            if matches:
                wi=next(i for i,w in enumerate(z["windows"]) if e["consumer"] in w["retained"])
                e.update(category="common_grandparent_retained",shadow_double=[wi,e["consumer"],matches[0]["j"]])
        if e["category"]=="common_grandparent_retained":
            dest=tuple(e["shadow_double"]);parent=tuple(e["original_parent"])
            assert dest not in destinations or destinations[dest]==parent
            destinations[dest]=parent
        final.append(e)
    unhandled=[e for e in final if e["category"] not in ("common_grandparent_retained","synchronized_omitted")]
    for e in unhandled:
        e["type"]="G" if e["category"]=="unmatched_retained" else "O" if e["category"]=="unpaid_omitted" else "X"
    return {"orientation":d,"return":ret,"other":other,"adaptive":ad,"comparison":z,
        "final_events":final,"unhandled":unhandled,"original_rows":rows}


def parent_sets(events):
    sets={kind:set() for kind in ("O","G","X")};loads=Counter()
    for e in events:
        parent=tuple(e["original_parent"])
        sets[e["type"]].add(parent);loads[parent]+=1
    assert not(sets["O"]&sets["G"] or sets["O"]&sets["X"] or sets["G"]&sets["X"])
    assert max(loads.values(),default=0)<=3
    assert len(events)<=3*sum(map(len,sets.values()))
    return {"sets":{k:[list(p) for p in sorted(v)] for k,v in sets.items()},
        "counts":{k:len(v) for k,v in sets.items()},"loads":{str(list(p)):v for p,v in loads.items()},
        "gap_count":len(events),"parent_count":len(loads),"maximum_load":max(loads.values(),default=0)}


def ancestor(tree,g,x):
    return g!=x and g in tree.path(x)[:-1]


def ancestry_history(r,g,x):
    a=Tree(r.source["initial_A"]);b=Tree(r.source["initial_B"])
    previous={"A":ancestor(a,g,x),"B":ancestor(b,g,x)}
    initial=dict(previous);changes=[]
    for e in r.events:
        tree=a if e["actor"]=="A" else b
        tree.rotate(e["pivot"],e["side"])
        now=ancestor(tree,g,x)
        if now!=previous[e["actor"]]:
            if not now:assert e["pivot"]==g
            changes.append({"id":e["id"],"time":e["time"],"present_after":now,
                "pivot":e["pivot"],"promoted":e["promoted"],"middle":e["middle"],"external":e["external"],
                "deleted":e["deleted"],"added":e["added"],"original_SET_sign":e["sign"]})
            previous[e["actor"]]=now
    assert previous==initial
    return {"g":g,"target":x,"initial_relation":initial,"changes":changes}


def last_A_loss(r,history,post_A_time):
    losses=[e for e in history["changes"] if e["id"][0]=="A" and not e["present_after"]]
    if not losses:return None
    def lift(e):return e["time"] if e["time"]<=post_A_time else e["time"]-r.T
    chosen=max(losses,key=lift)
    return {**chosen,"unrolled_time":lift(chosen),"previous_period":lift(chosen)<0}


def primary_record(r,cl):
    p=next(e for e in cl["unhandled"] if e["rho"]==[132,[72,3],[80,1]])
    pair=next(p0 for p0 in r.pairs if p0["rho"]==p["rho"])
    parent=r.U[tuple(p["original_parent"])];h=p["consumer"];row=r.boundaries[h-1]
    g=parent["g"];x=row["x"]
    history=ancestry_history(r,g,x)
    aset=set(row["A_path"][:-1]);bset=set(row["B_path"][:-1])
    return {"source":r.source,"costs":{"A":r.A,"Q_B":r.Q,"operations":len(r.ops)},"unhandled":p,
        "pair":pair,"parent":parent,"endpoints":[r.U[tuple(pair["rho"][j])] for j in (1,2)],
        "complete_first_hit_cohort":r.cohorts[h],"complete_receiver":r.cohorts[parent["h"]],
        "consuming_operation":row,"grandparent_ancestry_history":history,"last_A_loss":last_A_loss(r,history,row["post_A_time"]),
        "A_only_ancestors":sorted(aset-bset),"B_only_ancestors":sorted(bset-aset),"common_ancestors":sorted(aset&bset),
        "complete_original_events":r.events,"complete_original_boundaries":r.boundaries}
