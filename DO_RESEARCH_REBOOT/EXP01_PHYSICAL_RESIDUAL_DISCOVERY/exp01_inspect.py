import argparse,json
from pathlib import Path
from exp01_oracle import Replay,digest
from exp01_diagnostics import physical_diagnostics


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--trace",action="store_true")
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    sources=json.loads((root/"EXP01_SOURCE_WITNESSES.json").read_text())["sources"]
    src=next(s for s in sources if s["name"]==args.name)
    r=Replay(src)
    assert digest(r.events)==src["trace_hash"]
    assert r.a.state()==src["closing_A"] and r.b.state()==src["closing_B"]
    assert {"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"]}==src["costs"]
    out={"summary":r.summary(),"physical":physical_diagnostics(r),
        "cohorts":{str(k):v for k,v in r.cohorts.items()},"U_int":list(r.U.values()),"pairs":r.pairs}
    if args.trace:
        out.update(boundaries=r.boundaries,primitive_events=r.events)
    path=root/("inspection_"+digest(args.name)[:12]+".json")
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"verified":args.name,"A":r.A,"Q_B":r.Q,"R6":r.counts["R6"],"output":str(path)}))
