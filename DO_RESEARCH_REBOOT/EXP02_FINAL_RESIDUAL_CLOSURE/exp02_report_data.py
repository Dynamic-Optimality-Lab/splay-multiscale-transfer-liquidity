"""Compact exact measurement tables, primary complete witness and static figure."""
import os,time,json
from fractions import Fraction
from exp02_distortion import *
from exp02_sources import interrupted_H


if __name__=="__main__":
    cpu=time.process_time();wall=time.perf_counter()
    bridge=json.loads((ROOT/"EXP02_COMMON_GRANDPARENT_CERTIFICATES.json").read_text())["sources"]
    distortion=json.loads((ROOT/"EXP02_INTERRUPTION_DISTORTION_RESULTS.json").read_text())["sources"]
    byname={s["source"]:s for s in distortion}
    gp=json.loads((ROOT/"EXP02_GRANDPARENT_DISTORTION.json").read_text())["sources"]
    gpbyname={s["source"]:s for s in gp}
    totals={origin:{k:sum(r[k] for r in bridge if r["origin"]==origin) for k in ("R6_other","adaptive_paid","bridge_paid","remaining")} for origin in ("EXP01","EXP02")}
    lines=["# Complete EXP-02 finite measurements","","All costs are full original periods. Ratios are reduced exact fractions. Delta is a separate B comparison; its A cost is never an original resource.","",
        "| Source | X | A | Q_B | R6 | other | adaptive | bridge | unpaid | delta+ | signed delta | Q_B/A | other/A |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in bridge:
        d=byname[r["source"]]
        lines.append(f"| {r['source']} | {r['population']} | {r['A']} | {r['Q_B']} | {d['R6']} | {r['R6_other']} | {r['adaptive_paid']} | {r['bridge_paid']} | {r['remaining']} | {d['sum_positive_delta']} | {d['sum_signed_delta']} | {Fraction(r['Q_B'],r['A'])} | {Fraction(r['R6_other'],r['A'])} |")
    (ROOT/"EXP02_FULL_MEASUREMENTS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    src=interrupted_H(4,2,(5,));r=Replay(src)
    direction,ret,other=residual(r);ad=adaptive(r)
    p=next(p for p in other if p["rho"]==[132,[72,3],[80,1]])
    row=event_inventory(r,p,ret,ad)
    b=r.boundaries[131]
    write("EXP02_PRIMARY_OBSTRUCTION.json",{"source":{**src,"closing_A":r.a.state(),"closing_B":r.b.state(),"trace_hash":digest(r.events)},
        "costs":{"A":r.A,"Q_B":r.Q,"operations":len(r.ops),"R6_other":len(other)},"original_event":row,
        "consuming_operation":{"t":132,"target":5,"pre_A":b["pre_A"],"post_A":b["post_A"],"pre_B":b["pre_B"],"post_B":b["post_B"],
            "A_path":b["A_path"],"B_path":b["B_path"],"A_cost":b["a"],"Q_B_cost":b["q"],
            "all_original_B_bits":r.events[b["post_A_time"]:b["end_time"]]},
        "shadow_comparison":byname[src["name"]],"final_membership":"unpaid_omitted; retained positive distortion is zero and cannot cover this omitted consumer",
        "qualification":"smallest positive omitted-first-hit example in the tested p=3,4,5,6 dyadic controls; no global minimality claim"})
    write("EXP02_RESEARCH_SUMMARY.json",{"classification":"SUBSTANTIVE PARTIAL QUANTITATIVE PASS","global_final_residual_closed":False,
        "source_count":171,"inherited_sources":133,"new_sources":38,"corpus_operations":76474,"coverage":totals,
        "theorems":{"adaptive":"R_adaptive <= 6 C_seq A","bridge":"R_bridge <= (6 C_seq + 3) A",
            "paid_union":"R_adaptive + R_bridge <= (12 C_seq + 3) A",
            "remaining_scalar_interface":"Q_B <= (35 + 30 C_seq) A + R_unhandled; R_unhandled has no absolute A bound here"},
        "new_physical_identity":"delta = number of actual-only double grandparents - number of shadow-only double grandparents, per retained original access",
        "unhandled_counts":{"omitted_consumers":10,"retained_missing_shadow_grandparents":4},
        "interpretation":"Finite corpus coverage is not universal theorem closure. The 14 new unhandled events are full original certified R6_other."})
    os.environ["MPLCONFIGDIR"]=str(ROOT/".mplconfig")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig,axes=plt.subplots(1,2,figsize=(11,4.3),constrained_layout=True)
    categories=[("adaptive_paid","Adaptive domains","#2864af"),("bridge_paid","Common-grandparent bridge","#36815b"),("remaining","Unpaid exact complement","#c65338")]
    bottoms=[0,0]
    for key,label,color in categories:
        values=[totals[o][key] for o in ("EXP01","EXP02")]
        axes[0].bar([0,1],values,bottom=bottoms,label=label,color=color,width=.55)
        bottoms=[b+v for b,v in zip(bottoms,values)]
    axes[0].set_xticks([0,1],["133 inherited sources","38 independent new sources"])
    axes[0].set(ylabel="Certified original R6_other events",title="Exact finite coverage; universal complement open")
    axes[0].legend(fontsize=8,loc="upper left")
    cases=["zig_distortion_n9_L4","IH_p4_q1_L3_z65_c1","IH_p5_q1_L3_z129_c1","IH_p6_q1_L3_z257_c1","IH_p7_q1_L3_z513_c1"]
    for name in cases:
        w=byname[name]["windows"][0]
        axes[1].scatter(w["omitted_Q"],w["delta"],s=42,color="#733a9a")
        axes[1].annotate(str(byname[name]["population"]),(w["omitted_Q"],w["delta"]),xytext=(5,4),textcoords="offset points",fontsize=8)
    axes[1].plot([0,5],[0,5],ls="--",color="gray",lw=1,label="delta = omitted Q_B")
    axes[1].set(xlabel="Actual B doubles in omitted interruption",ylabel="Retained actual minus shadow doubles",title="A B-only price with coefficient one fails")
    axes[1].legend(fontsize=8,loc="upper left")
    for ax in axes:ax.grid(alpha=.17);ax.set_axisbelow(True)
    fig.savefig(ROOT/"EXP02_DISCOVERY.png",dpi=170);fig.savefig(ROOT/"EXP02_DISCOVERY.svg");plt.close(fig)
    resource=json.loads((ROOT/"EXP02_RESOURCE_RECORD.json").read_text())
    resource.update(report_analysis_CPU_seconds=time.process_time()-cpu,report_analysis_wall_seconds=time.perf_counter()-wall,
        report_analysis_memory=memory());resource["recorded_CPU_subtotal"]+=resource["report_analysis_CPU_seconds"]
    write("EXP02_RESOURCE_RECORD.json",resource)
    print(json.dumps({"coverage":totals,"primary_A_path":b["A_path"],"primary_B_path":b["B_path"],
        "primary_receiver":row["parent_certificate"]["h"],"CPU":resource["recorded_CPU_subtotal"]},indent=2))
