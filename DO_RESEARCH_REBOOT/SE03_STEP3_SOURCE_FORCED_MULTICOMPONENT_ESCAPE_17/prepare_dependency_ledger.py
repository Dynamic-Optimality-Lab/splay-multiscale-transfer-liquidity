"""Exact theorem provenance metadata; no independent proof recheck."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
rows=[]
def row(folder,name,statement,domain,status,conclusion,owners,signed,closure,audit,inspection):
    p=B.parent/folder/name
    rows.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),
        'exact_theorem_statement':statement,'source_domain':domain,
        'physical_event_semantics':'original ceil(edge-depthA/2) StepEvs incl zig, two bits each; floor(edge-depthBF/2) doubles; DELETE A-only, no physical deletion',
        'frozen_owner_assumptions':owners,'signed_accounting_assumptions':signed,
        'closure_reachability_hypotheses':closure,'conclusion_and_qualification':conclusion,
        'result_state':status,'audit_status':audit,
        'accepted_or_provisional':'accepted at stated scope' if status=='SEALED' else 'provisional with exact scope; no seal promotion',
        'proof_inspection':inspection})
base='SE03_STEP2_CD6_FINAL_ASSEMBLY_14';old='SE03_STEP3_UNIFORM_DONOR_GROUPING_15';prev='SE03_STEP3_NONLOCAL_OWNERSHIP_TRANSFER_16'
closed='original reachable exactly labeled A/BF paired-closed finite history; actual BE recurrence/alignment where owner map used'
owners='same actual I; certified supplied fE at its source scope; all common ordinals and successful old a values fixed; E-only retirement only in alternative full ledger'
signed='all actual qF,qE,H, C/P/N corrections, chart endpoints, genuine boundaries and legal cuts retained'
row(base,'CD6_FINAL_CERTIFICATE.json','Every original six-genuine-key W has an explicit actual-period full injection, hence QF<=2A',
 'six keys, every full core6..11, arbitrary original helpers/private BSTs','SEALED','CD6/I6 base only; no unrestricted induction',owners,signed,closed,
 'accepted C14 final distinct immutable/source/owner/period/dependency certificate and successful resume3', 'certificate and final proof/verdict scope reconstructed; completed checks reused')
row(base,'UNIFORM_R_TRANSFER.md','I(r-1)+E_r=>I(r) with specified local source license and original physical working contract',
 'arbitrary r under EXACT E_r1/2/3','SEALED','sufficient implication; universal source hypotheses OPEN',owners,signed,closed,
 'accepted sufficient source/interface theorem; no unconditional source supply receipt','full definition/clauses inspected')
row(old,'UNIFORM_LEAF_CHANNEL_THEOREM.md','Q=u+beta, DeltaL=u-z; distinct physical leaf channels; h_Lambda domain D minus explicit branch holes',
 'actual closed maximal full core2r-1, r>=7, arbitrary populations/word length','PROVED-DERIVATION / AUDIT-PENDING',
 'raw channels/partial frontier reduction, not post-owner universal funding',owners,signed,closed,
 'C15 source/owner checks completed; final integrity suffix interrupted','source argument and allocation rule inspected/reused')
row(old,'ZERO_RUN_FAMILY_THEOREM.md','Gamma_r C_run,r has r-4 consecutive H1/Q2 zero holes; actual disjoint reset repairs them',
 'explicit all-r/repetition/free-gap/reflected family','PROVED-DERIVATION / AUDIT-PENDING',
 'restricted family counting/block funding, not general reset or Bank25 realization',owners,signed,closed,
 'completed old source checks; final seal pending','parameter source proof inspected, reused without semantic replay')
for name,statement,conclusion in (
 ('ZERO_TRANSFER_GRAMMAR.md','Natural Q=2c hole iff H=c,z1,u0; one slot and r>=4H+1','local natural-maximal test only; complete ownership grammar OPEN'),
 ('NONLOCAL_AUGMENTATION.md','Fresh-image SOURCE recipe at each reached hole implies finite fixed-owner simultaneous augmentation','CONDITIONAL on universal source recipe; not U16/U17'),
 ('GLOBAL_NONOVERLAP.md','Current-image exclusion and unique predecessors give collective distinct terminals under source recipe','conditional collective algebra and restricted one-tail candidate lower bound'),
 ('FROZEN_OWNER_PRESERVATION.md','Appending only free effective terminals fixes every original a/common value','preservation interface; no new donor existence'),
 ('GROUPING_TO_NONLOCAL_BRIDGE.md','Own comparison image first min(2H,beta+z) bits','physical tail locations only; no freedom/eligibility inference'),
 ('deep_tail_candidate_obstruction.json','Actual erased13 source has two blocked components but only one originating deep-tail bit','specified monotone single-bit candidate fails; U17 not refuted')):
    row(prev,name,statement,'exact stated maximal-source/typed-map or actual r7 scope',
        'PROVED-DERIVATION / AUDIT-PENDING',conclusion,owners,signed,closed,
        'no C16 independent process; producer construction only','exact papers/certificate and source references reconstructed')
row(old,'owner_image_source_audit.json','All seven actual erasures of the recorded r7 source supply their own BE/f6/a and exact u,L',
 'one pinned64-operation original source; seven actual owner alternatives','PROVED-DERIVATION / AUDIT-PENDING',
 'finite exact source/owner cases only; erased13 u0 and others u1',owners,signed,closed,
 'source/owner immutable checks completed; C15 final suffix pending','actual record fields and new coordinate references inspected; no old semantic check rerun')
row(prev,'ABSOLUTE_PERIOD_VALIDITY.md','Both-endpoint original-period correspondence; prose blanket u1 qualification corrected in C17',
 'exact actual owner interval per case','PROVED-DERIVATION / AUDIT-PENDING',
 'use authoritative C15 per-case u; do not apply blanket C16 r7 u1 wording to erased13',owners,signed,closed,
 'C16 prose/derivation unaudited; per-case C17 producer transport pending audit','overbroad wording identified and qualified without altering old artifact')
for name in ('PREPARATION_TAIL_THEOREM.md','CORE_ORIGIN_BARRIER.md','EDGE_CREATOR_THEOREM.md','SATURATED_COMPONENT_NORMAL_FORM.md'):
    row(B.name,name,'Exact new symbolic theorem in this named paper','scope and exclusions stated in the paper',
        'PROVED-DERIVATION / AUDIT-PENDING','does not establish principal U17-ESCAPE',owners,signed,closed,
        'new symbolic producer/author derivation, no distinct audit capacity','new proof fully written; source constructions checked by producer only')
out('dependency_ledger.json',{'status':'THREE_STATE_EXACT_SOURCE_LEDGER','rows':rows,
    'OPEN_claims':['universal source-complete escape relation','universal joint escape supply','full E_r2/E_r3 and Bank25 realization'],
    'source_provenance':'local current worktree; no remote snapshot substituted'})
out('metadata_preparation.json',{'metadata_CPU_excluded':time.process_time(),'operation':'exact path/hash/status ledger publication only'})
print(json.dumps({'status':'LEDGER_PUBLISHED','rows':len(rows)}),flush=True)
