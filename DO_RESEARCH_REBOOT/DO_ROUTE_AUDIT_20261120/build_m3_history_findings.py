"""Write the semantic audit of the M3 transfer history without rerunning it."""
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
R = Path("\\\\?\\" + str(ROOT))
INPUTS = json.loads((OUT / "semantic_followup_chunks.json").read_text())["m3_history"]
BASE = "DO_RESEARCH_REBOOT/"
X21 = BASE + "M3_XFER21/"
RCD = BASE + "RESTRICTED_CD_STEP04/"


def ref(path, line, end, meaning):
    return {"path": path, "line": line, "end_line": end, "meaning": meaning}


def sha(path):
    return hashlib.sha256((R / path).read_bytes()).hexdigest()


def stage(number, result, meaning, lines):
    path = BASE + "M3_XFER" + str(number).zfill(2) + "/RESULT.md"
    return {"stage": number, "recorded_result": result, "portable_or_scope_note": meaning, "evidence": ref(path, lines[0], lines[1], result)}


stages = [
    stage(1,"LOW-safe opaque two-core Q saturation", "Public h=min(2,w_x+2), D_Q=max(Lambda,h); all Q-source LOW rows, restricted walks only.",(6,32)),
    stage(2,"Cut-separated marked-pair augmentation", "max(D,h_R) preserves every already-valid original LOW row, including helpers, for arbitrary compatible sigma.",(7,31)),
    stage(3,"Buried-cut L/T/S1 transfer", "Fresh witnesses need not retain formerly observed ports. S debt2 release still open at this stage.",(7,35)),
    stage(4,"Two J5/J6 debt2 zero-release families", "New public successor capacity proves exact outgoing rows and preserves old valid rows; anonymous/RR variants not yet covered.",(3,31)),
    stage(5,"P5/P6 RR zero releases", "Explicit K/C/Z return relay; other core arrangements and global coverage still open.",(3,29)),
    stage(6,"Anonymous P5/P6 zero releases", "Proxy-parent/final gap-leaf validity, not an assumed private completion, rules out cheap helper exits.",(3,32)),
    stage(7,"Direct half of S zero frontier", "Four upper words and true order-duals covered; local word counts are not percentages of M3.",(3,30)),
    stage(8,"All eight S-family upper zero words", "Only guarded S class completed; universal cheap Gamma1 restriction gives initial helper B depth<=2.",(3,32)),
    stage(9,"Outside-S interval-child class", "Real/anonymous middle roots and fresh exposure included; exact guard, incoming debt level, and arbitrary original signatures retained.",(3,42)),
    stage(10,"Four guarded unmarked-ancestor grandchild classes", "Actual source root need not be marked; all original raw G/unused fields remain, and V-empty is not a globally solved sink.",(3,44)),
    stage(11,"Marked-root/marked-parent central relay", "Explicit two-credit relay under extreme-pair/span/depth guards; helper terminal-only q and actual duals.",(3,46)),
    stage(12,"Depth4/5 central same-direction marked-ancestor class", "Span restriction removed within stated central geometry; nonextremal and shallow-helper complement remained.",(3,48)),
    stage(13,"Saved nonextremal exposure family", "Specific masks and their true duals, with arbitrary private upper terms; cap1 stages do not prove every already-debt2 auxiliary row.",(3,47)),
    stage(14,"Universal zero-LOW decision-tree partition", "36 H1+16 Gamma1 schematic leaves, not52 observed signatures/failures; partition was not signed closure.",(3,40)),
    stage(15,"Eight visible Gamma1 zero profiles", "Pure core-tree helper projection supplies target psi floor without inventing an intermediate graph vertex/private witness.",(3,40)),
    stage(16,"Eight hidden Gamma1 zero profiles", "Lower debt on a tall hidden public region after checking incoming rows; proves zeros for changed D_hid, not old failed values.",(3,37)),
    stage(17,"All unmarked-source LOW rows", "Destination is marked/synchronized, so normalize debt to zero on other source classes; preserve valid rows without asserting a false global psi floor.",(3,29)),
    stage(18,"Broader marked-source zero repayments", "Remaining failed zero H1 sources have exact psi seed debt; exhaustive complement still open at this stage.",(3,31)),
    stage(19,"ALL zero-weight LOW rows on frozen original graph", "Explicit3413-clause F;36972 clause/word obligations and6806 universal records, all378 critical role groups. This is a symbolic grammar certificate, not finite population coverage.",(3,45)),
    stage(21,"FULL M3 on frozen original graph", "Explicit common potential on every full ordinary/midpoint edge for all legal nine-core five-mark masks and all admissible ten-component sigma. Positive LOW obligations close.",(3,48)),
]

claims = [
    {
        "id":"m3_fixed_domain", "label":"Frozen M3 graph has nine cores and five marked bits",
        "statement":"The domain is each original9-bit mask with exactly5 marked core keys (126 masks), every admissible ten-component sigma, unchanged147-coordinate ordinary and127-coordinate midpoint states and all original edges.",
        "meaning_of_multisupport":"Multiple nonzero components of the ten-gap signature are permitted. This does NOT mean arbitrarily many genuine KEEP targets or an unbounded number of marked core keys.",
        "evidence":[ref(X21+"FULL_M3_PROOF.md",9,34,"Exact graph and function quantifiers"),ref(X21+"M3_CERTIFICATE.json",1,1,"Structured domain: mask, signature, coordinate counts; JSON field reference, not a prose proof line")]
    },
    {
        "id":"m3_failed_uniform_candidates", "label":"Early uniform transport formulas failed only at their exact relation scope",
        "statement":"UNIFORM01's one-step incoming closure and UNIFORM02's nonnegative-closure/negative-run formula are refuted on their saved proof superrelations. Original-root lift attempts were rejected, so no original transition counterexample, original negative cycle or refutation of M3 followed.",
        "version_rule":"Those specified formulas remain failed at their recorded scopes. XFER21 supplies a different valid formula; it does not retroactively validate them.",
        "evidence":[ref(BASE+"M3_UNIFORM01/RESULT.md",3,16,"One-step formula obstruction and rejected original lift"),ref(BASE+"M3_UNIFORM02/RESULT.md",3,14,"Sign-run failure and precise original-validity limit")]
    },
    {
        "id":"m3_safe_signed_augmentation", "label":"Public clause changes preserve every completed signed row",
        "statement":"Accepted debt changes are proved on their actual source guards. New maxima audit all outgoing negative/zero/+1 rows at the maximum active changed-source debt; unchanged sources can only gain target debt. Safe downward ceilings require incoming-row checks. No global old-feasibility premise or private completion history is used.",
        "portability":"A proof method potentially reusable on an expanded source representation; no all-support certificate follows automatically.",
        "evidence":[ref(BASE+"M3_XFER02/RESULT.md",12,30,"Already-valid row preservation under max on arbitrary compatible signatures"),ref(BASE+"M3_XFER16/RESULT.md",13,37,"Incoming-row audit before lowering source values"),ref(X21+"FULL_M3_PROOF.md",36,68,"Maximum-source signed theorem and exact retained prefix")]
    },
    {
        "id":"m3_zero_rows_complete", "label":"XFER19 completed every zero LOW row",
        "statement":"A fixed explicit ordinary F with3413 public clauses proves all original zero-weight LOW edges for every legal mask and compatible independent private witness in the frozen nine-core graph. It preserves all completed negative/+1 rows from its actual lineage.",
        "recorded_status":"PROVED_UNIVERSAL_STEP4_ZERO_LOW_SIGNED_REPAYMENT; separate same-campaign audit, not external peer review or compiler formalization.",
        "version_rule":"XFER01..18 OPEN full-Step4 statements are historical frontier snapshots. Their properly scoped theorems remain valid; their broader open claim is superseded by XFER19.",
        "evidence":[ref(BASE+"M3_XFER19/RESULT.md",3,45,"Complete zero closure, audit counts and remaining positive task")]
    },
    {
        "id":"m3_full_pointwise_potential", "label":"XFER21 proved one explicit potential on every original M3 edge",
        "statement":"D=max(F4,1_(P&N&C1),2*1_(P&N&C2)) lies in[0,2]. W(O)=-D(O)-5chi8(O.b), W(M)=-5chi8(M.b), with chi8=(b.kr[8]==0 AND b.rr[8]==19), satisfies w(s,t)>=W(t)-W(s) on EVERY original edge.",
        "global_budget":"Every finite walk has weight>=W(end)-W(start)>=-7; within fixed chi8 region>=-2; every FULLY CLOSED walk has nonnegative total weight. No deficit-count or bounded transfer horizon premise.",
        "exact_scope":"All original legal five-mark masks and arbitrary admissible ten-component sigma on unchanged frozen graph. D uses ordinary public current-state fields; no private inventory, selected completion, event history or invented midpoint alpha.",
        "recorded_status":"M3_CERTIFICATE status PROVED_UNIVERSAL_FULL_M3. Parent Step4+4359 completion clauses,69084 signed clause/word obligations,4152 critical helper word obligations, zero missing; completed universal UNSAT conclusions reused. Not external review or full compiler formalization.",
        "evidence":[ref(X21+"M3_POTENTIAL_SPEC.md",3,40,"Exact explicit formula, raw predicates and state arguments"),ref(X21+"FULL_M3_PROOF.md",9,68,"Pointwise theorem and quantifier/source proof"),ref(X21+"FULL_M3_PROOF.md",70,121,"Exhaustive LOW classification and remaining positive helper proof"),ref(X21+"FULL_M3_PROOF.md",123,161,"HIGH/two-sort telescoping and trust boundary")]
    },
    {
        "id":"m3_source_grammar_lift", "label":"Symbolic source completeness makes finite clause records universal",
        "statement":"The source grammar covers each actual original witness after forgetting selected counts, retains both observations, real operand ancestry, literal old-owner/current-child G reads, anonymous gap order including equal-gap nodes on both sides, PORT versus EMPTY and free unused fields. Universal UNSAT negations therefore cover arbitrary original signatures/private completions.",
        "not_claimed":"A SAT model of the overapproximation is not automatically a realizable original transition or closed source. An exact-mask proof does not validate a broadened mask guard; each broader source predicate needs its own signed obligations.",
        "portability":"Forward source coverage plus universal pointwise inequalities avoids reverse realization and hidden witness concatenation; expanding to arbitrary support still requires a new correct representation and proof.",
        "evidence":[ref(X21+"FULL_M3_PROOF.md",47,68,"Exact source overapproximation and guard broadening limits"),ref(X21+"FULL_M3_PROOF.md",117,142,"Failed kernel status not imported; full midpoint remains shared")]
    },
    {
        "id":"m3_original_low_contract", "label":"Original LOW budget and Gamma0 law are retained",
        "statement":"Original LOW requires macro_H=H_v and H_v<=2 with its own at-most-five-event macro bound. Genuine H0 is impossible; at most one changing fringe helper occurs, so H1 and H2/Gamma0/Gamma1 are exhaustive. Terminal q and price2H_v-q are literal original quantities.",
        "important_floor":"Gamma0 needs the marked DESTINATION psi floor and D(source)<=2; no globally valid D>=psi on unmarked sources. Actual preterminal9-core C and negative-core law give psi(destination)>=q-2 for q3/4.",
        "evidence":[ref(X21+"ORIGINAL_BUDGET_AND_FLOOR_ADDENDUM.md",3,39,"Original compiler conjuncts and exact Gamma0 coefficient proof")]
    },
    {
        "id":"m3_trial_status_preserved", "label":"XFER20 trial phases are not an independent full-M3 seal",
        "statement":"There is no M3_XFER20/RESULT.md in the selected history. It contains the positive-anchor/H1 completion and helper trial phases. XFER21 explicitly retains a2963-clause prefix and discards34 unproved trial clauses; a failed/capped kernel's topology/depth facts are used only at already certified scopes, never as a signed theorem.",
        "evidence":[ref(BASE+"M3_XFER20/H1_CLOSURE.md",3,31,"H1 completion and separate remaining helper/global audit gate"),ref(BASE+"M3_XFER20/JOINT_HELPER_COMPLETION.md",14,28,"Suggested source cubes are provisional until every new-source obligation and global audit pass"),ref(X21+"FULL_M3_PROOF.md",65,68,"Exact retained prefix and discarded trial clauses"),ref(X21+"FULL_M3_PROOF.md",117,121,"FAILED_SIGNED_EXTENSION is not a signed premise")]
    },
    {
        "id":"restricted_cd_from_m3", "label":"M3 plus11F proves original CD on W_5^9",
        "statement":"For every original W with five genuine KEEP keys and nine-core in frozen W_5^9, 11F supplies a FULLY CLOSED graph image P with w(P)<=2A(W)-Q_B(W). Universal M3 gives w(P)>=0, hence Q_B(W)<=2A(W).",
        "source_quantifiers":"Forall W exists P, and forall fully closed P nonnegative. No reverse source realization or a common private completion for an entire abstract walk is required.",
        "budget":"LOW macro weight2H-q for H<=2; HIGH macro weight6-q<=2H-q for H>=3. T266 is per macro, not a bound on source word length.",
        "recorded_status":"RESTRICTED_CD_CERTIFICATE status PROVED_UNIVERSAL_RESTRICTED_COARSE_DOUBLE_W5_CORE9. All126 masks, arbitrary admissible fringe/signatures, helpers, repetitions, zero/nongenuine events, primitive/nonprimitive walks and exact paired closure included. Separate symbolic composition audit; not formal/external certification.",
        "evidence":[ref(RCD+"RESTRICTED_CD_PROOF.md",5,35,"Original-source forward lift and graph potential"),ref(RCD+"RESTRICTED_CD_PROOF.md",37,90,"Closed full graph telescoping and exact original-source conclusion"),ref(RCD+"RESULT.md",3,37,"Scope, publication seal and unrestricted claim boundary")]
    },
    {
        "id":"m3_first_unsupported_all_support_lift", "label":"Nine-core M3 is not an all-support Coarse-Double theorem",
        "statement":"The completed M3 potential controls its fixed nine-core/five-mark graph. Its genuine original-source lift is W_5^9, the nine-core leaf of CD5. Arbitrary multi-component sigma removes population restrictions inside that representation, not the bounded number of genuine KEEP target keys.",
        "first_missing_implication":"Every arbitrary-support exactly paired-closed original source admits either an exact source reduction into the already certified domains with globally controlled cost corrections, or a new support-uniform necessary representation with universally valid potential/source-work inequalities. No such theorem follows from these results.",
        "why_not_copy_potential":"The negative-core psi, clause inventories, marked-mask cardinality, fixed raw chi8 and ordinary/midpoint interfaces all belong to the frozen representation. A larger-support graph requires its own state/source/cost/closure and global sign proofs.",
        "evidence":[ref(X21+"FULL_M3_PROOF.md",9,19,"Explicit fixed graph domain"),ref(RCD+"RESTRICTED_CD_PROOF.md",87,90,"No genuine-support expansion"),ref(BASE+"CD5_BASE01/CD5_PROOF.md",123,128,"Completed support<=5 base explicitly lacks support lifting")]
    }
]

manifest_path = X21+"final_manifest.json"
manifest = json.loads((R/manifest_path).read_text())
pin_checks=[]
for item in manifest["files"]:
    p=X21+item["file"]
    actual=sha(p)
    pin_checks.append({"path":p,"expected_sha256":item["sha256"],"actual_sha256":actual,"match":actual==item["sha256"]})

extra_full=[X21+"M3_POTENTIAL_SPEC.md",X21+"FULL_M3_PROOF.md",X21+"ORIGINAL_BUDGET_AND_FLOOR_ADDENDUM.md",RCD+"RESTRICTED_CD_PROOF.md",BASE+"M3_XFER20/H1_CLOSURE.md",BASE+"M3_XFER20/JOINT_HELPER_COMPLETION.md",BASE+"M3_XFER20/POSITIVE_SOURCE_AND_WORD_REDUCTION.md",BASE+"M3_XFER20/RETAINED_CEILING_SOURCE.md",BASE+"M3_XFER20/VISIBLE_CAPACITY_EXCLUSION.md"]
findings={
    "audit_date":"2026-11-20", "scope":"Static semantic audit of all23 requested RESULT reports and listed extra proofs; no semantic engine, solver, primitive source replay, proof-assistant or historic certificate recompilation.",
    "primary_files":[{"path":p,"sha256":sha(p),"coverage":"complete RESULT statement/body"} for p in INPUTS],
    "additional_full_reads":[{"path":p,"sha256":sha(p)} for p in extra_full],
    "additional_partial_reads":[{"path":BASE+"M3_XFER20/INDEPENDENT_FULL_M3_AUDIT_GATE.md","coverage":"audit requirements and exact-mask-versus-broader-guard clauses; not used as a completed theorem"}],
    "certificate_reads":[{"path":p,"coverage":"domain/status/formula/publication fields; clause data not independently re-solved"} for p in [BASE+"M3_XFER19/STEP4_CERTIFICATE.json",X21+"M3_CERTIFICATE.json",RCD+"RESTRICTED_CD_CERTIFICATE.json"]],
    "publication_integrity":{"source":manifest_path,"status":manifest["status"],"entries":len(pin_checks),"all_match":all(e["match"] for e in pin_checks),"records":pin_checks,"caveat":"Byte identity only, not a rerun of universal clause or source proofs."},
    "stage_ledger":stages,
    "claims":claims,
    "useful_portable_mechanisms":["Pointwise potential on original full states: no witness compatibility needed beyond the exact shared midpoint.","Universal necessary source grammar plus symbolic UNSAT proof records; population coverage comes from the lift, not tested counts.","Preserve individually valid signed rows under every accepted max/ceiling operation, checking fresh-source outgoing or changed-target incoming rows.","Separate source capacity c from psi seed and retain failure-domain ceilings accurately; no false global potential floor.","Use correct full endpoint closure and forward forall-source-exists-image quantifiers; no reverse graph-realization claim.","Carry exact original LOW/HIGH prices and the h0 actual0/declared18/q9/w=-3 correction through two-sort telescoping."],
    "route_assessment":{"positive_progress":"M3 is a genuinely completed universal symbolic theorem at its exact frozen graph scope, and produces the full original five-key/nine-core CD leaf. It must not be left marked globally OPEN because early RESULT snapshots say so.","limit":"This evidence does not establish that lifting the potential to arbitrary support is easier than aggregate conservation. The certificate is large but finite and tied to fixed marked/core cardinality.","practical_use":"Reuse this completed base and its proof-engineering lessons. For DO retain the relaxed absolute-constant target; do not restart failed transport-horizon fits or treat arbitrary signature support as unbounded KEEP-support closure."},
    "token_accounting":{"available":False,"graph_zero_fields_mean":"unavailable, not measured zero"}
}

nodes=[];edges=[];seen=set()
def add(n):
    if n["id"] not in seen:nodes.append(n);seen.add(n["id"])
def did(p):return "m3_doc_"+hashlib.sha256(p.encode()).hexdigest()[:12]
for p in INPUTS:
    add({"id":did(p),"label":p.split("/")[-2]+" result","file_type":"document","source_file":p,"source_location":"1","source_url":None,"captured_at":"2026-11-20","author":None,"contributor":None})
for c in claims:
    first=c["evidence"][0]
    add({"id":c["id"],"label":c["label"],"file_type":"document","source_file":first["path"],"source_location":str(first["line"]),"source_url":None,"captured_at":"2026-11-20","author":None,"contributor":None,"statement":c["statement"],"recorded_status":c.get("recorded_status","Precisely scoped source-recorded result; independent re-verification not performed")})
    for e in c["evidence"]:
        add({"id":did(e["path"]),"label":Path(e["path"]).stem,"file_type":"document","source_file":e["path"],"source_location":"1","source_url":None,"captured_at":"2026-11-20","author":None,"contributor":None})
        edges.append({"source":did(e["path"]),"target":c["id"],"relation":"references","confidence":"EXTRACTED","confidence_score":1.0,"source_file":e["path"],"source_location":str(e["line"]),"weight":1.0,"scope_note":e["meaning"]})
for s in stages:
    p=s["evidence"]["path"]
    edges.append({"source":did(p),"target":"m3_full_pointwise_potential","relation":"conceptually_related_to","confidence":"EXTRACTED","confidence_score":1.0,"source_file":X21+"FULL_M3_PROOF.md","source_location":"78","weight":1.0,"scope_note":"Historical stage of the explicit signed-row lineage; final full M3 supersedes broader OPEN frontier snapshots while preserving accepted scoped rows. No old failed formula is made valid."})
for a,b,p,line,note in [
    ("m3_zero_rows_complete","m3_full_pointwise_potential",X21+"FULL_M3_PROOF.md",78,"Step4 zero rows inherited; XFER21 separately closes positive rows"),
    ("m3_full_pointwise_potential","restricted_cd_from_m3",RCD+"RESTRICTED_CD_PROOF.md",67,"Together with11F forward source lift, yields original-source sharp CD on W_5^9"),
    ("restricted_cd_from_m3","m3_first_unsupported_all_support_lift",RCD+"RESTRICTED_CD_PROOF.md",87,"Source theorem explicitly does not expand genuine KEEP count"),
    ("m3_source_grammar_lift","m3_full_pointwise_potential",X21+"FULL_M3_PROOF.md",47,"Source completeness gives universal signatures/private completions at fixed graph scope"),
    ("m3_safe_signed_augmentation","m3_full_pointwise_potential",X21+"FULL_M3_PROOF.md",38,"Every changed source paid directly, previously valid signed rows retained"),
]:edges.append({"source":a,"target":b,"relation":"conceptually_related_to","confidence":"EXTRACTED","confidence_score":1.0,"source_file":p,"source_location":str(line),"weight":1.0,"scope_note":note})
graph={"nodes":nodes,"edges":edges,"hyperedges":[],"input_tokens":0,"output_tokens":0,"token_accounting_unavailable":True}
(OUT/"m3_history_findings.json").write_text(json.dumps(findings,ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"m3_history_graph.json").write_text(json.dumps(graph,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"reports":len(INPUTS),"stages":len(stages),"claims":len(claims),"nodes":len(nodes),"edges":len(edges),"publication_pins":len(pin_checks),"pins_all_match":all(e["match"] for e in pin_checks)},indent=2))
