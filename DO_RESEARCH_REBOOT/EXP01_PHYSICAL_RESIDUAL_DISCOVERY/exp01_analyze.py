"""Exact tables, report appendix, a scientific figure and final artifact checks."""
import os,json,time,hashlib
from fractions import Fraction
from pathlib import Path
from exp01_oracle import Replay,digest

ROOT=Path(__file__).resolve().parent


def ratio(x,y):
    return str(Fraction(x,y)) if y else "0"


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    data=json.loads((ROOT/"EXP01_RESULTS.json").read_text())
    archive=json.loads((ROOT/"EXP01_SOURCE_WITNESSES.json").read_text())
    rows=data["results"]
    assert len(rows)==len(archive["sources"])==133
    assert len({r["name"] for r in rows})==133
    for r,s in zip(rows,archive["sources"]):
        assert r["name"]==s["name"]
        assert r["paired_closed"] and s["initial_A"]==s["closing_A"] and s["initial_B"]==s["closing_B"]
        assert r["R_A"]==2*r["A"]-r["V_A"]
        assert r["D_B"]==r["P_A"]-r["N_A"]
        assert r["R6"]<=r["Q_B"]
        assert r["trace_hash"]==s["trace_hash"]
    gaps=[]
    for name in ("G_4_1_L31_r1_z1","warm_marked_4_1_r3","C15_owner_r7_mirrorFalse","DW_5_1_at31"):
        src=next(s for s in archive["sources"] if s["name"]==name)
        r=Replay(src,certify=False,independent=False)
        assert digest(r.events)==src["trace_hash"]
        gaps.append({"source":name,"K_B":r.KB,"A":r.A,"original_gap_witnesses":r.cyclic_A_gap_witnesses()})
    (ROOT/"EXP01_G0_GAP_CERTIFICATES.json").write_text(json.dumps(gaps,indent=2,sort_keys=True)+"\n")
    table=["| Source | X | genuine KEEP | S | ops | A | Q_B | R6 | Q_B/A | R6/A | D5 | D6 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        table.append(f"| {r['name']} | {r['population']} | {len(r['M'])} | {len(r['S'])} | {r['operations']} | {r['A']} | {r['Q_B']} | {r['R6']} | {ratio(r['Q_B'],r['A'])} | {ratio(r['R6'],r['A'])} | {r['classes']['R_scan']} | {r['classes']['R_fringe']} |")
    (ROOT/"EXP01_FULL_MEASUREMENTS.md").write_text("# Complete finite measurements\n\nAll ratios are exact reduced fractions. D5/D6 columns count original gaps covered by their respective scan classes. Full predicates and physical diagnostics are in EXP01_RESULTS.json.\n\n"+"\n".join(table)+"\n",encoding="utf-8")
    os.environ["MPLCONFIGDIR"]=str(ROOT/".mplconfig")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig,ax=plt.subplots(1,2,figsize=(11,4.2),constrained_layout=True)
    styles={"G":("#2864af","o","G with reset"),"DH":("#c64c31","s","H with inverse zig returns"),"DW":("#367b45","^","W with inverse zig returns")}
    for fam,(color,marker,label) in styles.items():
        chosen=[r for r in rows if r["family"]==fam]
        ax[0].scatter([r["A"] for r in chosen],[r["R6"] for r in chosen],label=label,color=color,marker=marker,s=34,alpha=.8)
        ax[1].scatter([r["population"] for r in chosen],[float(Fraction(r["R6"],r["A"])) for r in chosen],color=color,marker=marker,s=34,alpha=.8)
    ax[0].set(xlabel="Complete original A cost",ylabel="Certified original R6 count",title="Residual demand includes full restoration cost")
    ax[1].set(xlabel="Complete physical population |X|",ylabel="R6 / A",title="Finite ratios; no asymptotic bound inferred")
    ax[0].legend(fontsize=8,loc="upper left")
    for a in ax:
        a.grid(alpha=.18);a.set_axisbelow(True);a.set_ylim(bottom=0)
    fig.savefig(ROOT/"EXP01_SCALING.png",dpi=170)
    fig.savefig(ROOT/"EXP01_SCALING.svg")
    plt.close(fig)
    resource=data["resources"]
    resource["final_analysis_process_cpu_seconds"]=time.process_time()-cpu
    resource["final_analysis_wall_seconds"]=time.perf_counter()-wall
    resource["total_recorded_process_cpu_seconds"]+=resource["final_analysis_process_cpu_seconds"]
    resource["extra_G0_replay_operations"]=sum(len(s["operations"]) for s in archive["sources"] if s["name"] in {g["source"] for g in gaps})
    data["final_verdict"]="NEW QUANTITATIVE THEOREM — RESTRICTED RETURN-NORMALIZED SCAN CLASS"
    data["global_R6_over_A_status"]="OPEN"
    data["new_scoped_bound"]={"R6_return":"<= 3 C_seq E_return <= 6 C_seq A", "E_return":"|S| times the number of disjoint long windows after verified inverse-zig B-return erasure; one fixed orientation per source", "proof_status":"same-agent symbolic; depends on inherited sequential-access theorem and three-slot lemma"}
    data["refutations"]=["Deep reset necessary for R6: false in DH_4_1_at31_c1", "One-to-one R6 root-entry A StepEv matching: false in DW_5_1_at31", "Load two root-entry rule: false in DW_6_1_at31", "Inverse-zig normalization covers all R6: false in original G"]
    (ROOT/"EXP01_RESULTS.json").write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    (ROOT/"EXP01_RESOURCE_RECORD.json").write_text(json.dumps(resource,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"verified_sources":len(rows),"resource_record":resource},indent=2))
