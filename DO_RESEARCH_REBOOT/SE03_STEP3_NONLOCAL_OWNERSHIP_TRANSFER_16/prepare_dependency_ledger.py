"""Publication metadata and literal source-record reuse, not proof checking."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
C14=B.parent/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'
C15=B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
rows=[]
def row(p,status,inspection,scope):
    rows.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),
        'status':status,'inspection':inspection,'scope':scope})
for name in ('FULL_PROOF.md','CD6_FINAL_CERTIFICATE.json','UNIFORM_R_TRANSFER.md',
             'FROZEN_OWNER_COMPATIBILITY.md','GLOBAL_PHYSICAL_INJECTION.md',
             'ABSOLUTE_PERIOD_ALIGNMENT.md','INDEPENDENT_AUDIT.md','CHECKPOINT.md'):
    row(C14/name,'ACCEPTED_SEALED_INHERITED', 'C16 paper/certificate read; old exhaustive checks reused',
        'exact original six-key domain or stated uniform conditional interface only')
for name in ('run_resume3_result.json','independent_audit.json','gamma_period_replay.json'):
    row(C14/name,'ACCEPTED_OLD_RECEIPT','accepted receipt reused, no new semantic replay',
        'final assembly and exact source controls at their certified scopes')
for name in ('FINAL_VERDICT.md','CHECKPOINT.md','GATE_U14_RECONSTRUCTION.md',
 'DEEP_PACKET_CLASSIFICATION.md','DONOR_GROUPING_CONSTRUCTION.md','PHYSICAL_GROUP_SEEDS.md',
 'GLOBAL_GROUP_NONOVERLAP.md','FROZEN_OWNER_EXCHANGE.md','ABSOLUTE_PERIOD_GROUPING.md',
 'WIDTH_GROWTH_AUDIT.md','GROUPING_TO_TRANSFER_BRIDGE.md','INDEPENDENT_AUDIT.md',
 'ADVERSARIAL_AUDIT.md','UNIFORM_LEAF_CHANNEL_THEOREM.md','ZERO_RUN_FAMILY_THEOREM.md',
 'RESTRICTED_FAMILY_FUNDING.md','SOURCE_OWNER_IMAGE_AUDIT.md','GROUP_SIGNED_ACCOUNTING.md'):
    row(C15/name,'INHERITED_PARTIAL_PAPER_SOURCE_CHECKS_COMPLETED_FINAL_SEAL_PENDING',
        'source argument reconstructed/read; no promotion of unfinished final bundle',
        'stated maximal-core lemmas, restricted source families and explicit limitations')
for name in ('independent_audit.json','run_independent_result.json','resources_checkpoint.json',
             'leaf_source_certificates2.json','zero_run_source_certificates.json','owner_image_source_audit.json'):
    row(C15/name,'SOURCE_RECEIPT_REUSED_FINAL_INTEGRITY_SEAL_PENDING',
        'receipt/current-byte provenance read; source operations not recomputed',
        'eight histories/seven owner variants only; no all-r induction from finite controls')
for dirname,name in (
 ('SE03_STEP2_REPAY01','CLOSED_CORE_SUBTREE_DENSITY.md'),
 ('SE03_STEP2_DONOR05','CLOSED_MAXIMAL_SAME_SIDE.md'),
 ('SE03_STEP2_REPAY01','MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md'),
 ('SE03_STEP2_CORE7_SINGLE_EXCESS_11','NONLOCAL_DONOR_LEMMA.md')):
    p=B.parent/dirname/name
    row(p,'ACCEPTED_INHERITED_SCOPED_SOURCE_LEMMA','paper argument inspected/reconstructed; old receipts reused',
        'exact closed maximal source or stated finite source-certified comparison interface')
for dirname,name in (
 ('SE03_STEP2_CORE7_TWO_EXCESS_12','independent_audit.json'),
 ('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','FULL_PROOF.md'),
 ('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','independent_audit.json')):
    p=B.parent/dirname/name
    row(p,'ACCEPTED_OLD_CONTROL_REUSED','accepted provenance imported via C14/C15; NOT re-proved in C16',
        'two-slot collisions or arbitrary-count six-key funding; not arbitrary-r supply')
for name in ('ORIGINAL_PIPELINE.md','RESEARCH_RULES.md'):
    p=B.parent/name
    row(p,'SOURCE_DEFINITION','permanent rules read; original pipeline definitions inherited through C14',
        'original mathematical/source contract; historical OPEN labels do not override later seals')
out('dependency_ledger.json',{'status':'EXACT_SCOPES_AND_INSPECTION_ATTRIBUTES','rows':rows,
    'no_missing_dependency_invented':True,'not_a_new_independent_verification':True})
source=read(C15/'leaf_source_certificates2.json')
out('seven_key_source_reuse.json',{'status':'LITERAL_REUSE_OF_OLD_SOURCE_RECORDS_NO_NEW_REPLAY',
    'source_path':(C15/'leaf_source_certificates2.json').relative_to(ROOT).as_posix(),
    'source_sha256':sha(C15/'leaf_source_certificates2.json'),
    'C15_final_integrity_seal':'PENDING_CAP','reports':source['reports'][:2]})
out('metadata_preparation.json',{'CPU_excluded_under_inherited_metadata_convention':time.process_time(),
    'work':'dependency provenance and literal old JSON record projection only'})
print(json.dumps({'status':'METADATA_PUBLISHED','ledger_rows':len(rows),'old_source_records_copied':2}),flush=True)
