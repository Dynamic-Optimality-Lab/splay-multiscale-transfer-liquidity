"""Metadata provenance only; exact accepted source scopes, no new proof run."""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
entries=[
('CD6 and I6 base','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json','PROVED','original six-key paired-closed full source; all full cores6–11','accepted immutable implementation, same agent; certificate and full proof inspected','base only, no arbitrary-r donor supply'),
('Exact I(r),E_r sufficient transfer','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md','PROVED_SUFFICIENT','arbitrary r conditional on source license and owner/period/storage clauses','proof inspected, current reconstruction','source clauses2/3 remain open; not an unconditional induction'),
('Marked-core density and set growth','SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED','all closed marked B supports and arbitrary private BSTs','source proof inspected/reused accepted receipt','does not prove source A credit supply'),
('Maximal all-SS','SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED','closed core2r-1, all r>=2','source proof inspected','not smaller nonmaximal cores'),
('Deep fan and ACTUAL successor','SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED','maximum-depth2r-2 in actual closed maximal core','source proof inspected','q1 successor includes all actual intervening operations'),
('Uniform Gamma source and repair','SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md','PROVED','arbitrary r and independent ordered BST gaps','source induction proof inspected, accepted source audits reused','cost/closure identity only, not arbitrary word funding'),
('Modified Gamma and width','SE03_STEP2_REPAY01/PAIRED_RANGE_TWO_TARGET.md','PROVED_NECESSARY_BOUND','actual paired H2/Qr source family, width>=r-4','source proof inspected','no width sufficiency inferred'),
('Uniform residual anchors','SE03_STEP2_FULL_FUNDING_CLOSURE_10/RESIDUAL_SLOT_THEOREM.md','PROVED','any finite support, actual source packets and supplied original owners','proof inspected; exact original exchange unchanged','anchors are demands, not donors'),
('All-paid source augmentation','SE03_STEP2_CORE7_SINGLE_EXCESS_11/NONLOCAL_DONOR_LEMMA.md','PROVED_INTERFACE','finite actual D/U, independently source-certified comparison and fixed paid map','source eligibility/path proof inspected','complete supply premise or explicit partial blocked frontier retained'),
('Arbitrary-count source funding','SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/CORE7_FULL_FUNDING.md','PROVED_RESTRICTED','six-key core7, all finite slot counts','accepted separate seal reused','one predecessor unit does not pay arbitrary-r deficits'),
('Core8 full source funding','SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/CORE8_FULL_FUNDING.md','PROVED_RESTRICTED','six-key core8,13 masks, all populations/counts','accepted immutable source seal reused','not arbitrary support by analogy'),
('Unrestricted six-key A/private lifting','SE03_STEP2_UNARY_A_LIFT_14/funding_seal.json','PROVED_RESTRICTED','six-key full cores9–11, all A ancestors/private BSTs','separate immutable frame/table/owner audit reused','no all-r signed law inferred'),
('Original period/frozen contracts','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md','PROVED_INTERFACE','same actual I, both-endpoint transport, original legal owner cuts','source proof/current Gamma replay inspected','never borrow a prefix or adjacent copy'),
('Gamma26 original control','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/gamma_period_replay.json','PROVED_CONTROL','original26 operations,9/10/12/13,forced cut restrictions','accepted immutable replay reused','not modified Gamma28'),
('Historical Sigma and reflection','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/independent_audit.json','PROVED_CONTROLS_ONLY','all accepted14 source controls and source-ID bridge','accepted14 replay/checker reused','not an all-r proof from finite controls')]
rows=[]
for title,path,status,scope,audit,condition in entries:
    p=P/path;assert p.exists(),path
    rows.append({'theorem':title,'path':'DO_RESEARCH_REBOOT/'+path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
        'status':status,'scope_and_assumptions':scope,'physical_semantics':'original ceil(depthA/2) StepEvs/two bits and floor(depthB/2) doubles; DELETE access only',
        'audit_and_inspection':audit,'conditions_for_arbitrary_support_use':condition})
with (B/'dependency_ledger.json').open('x',encoding='utf-8') as f:json.dump({'status':'EXACT_SOURCE_SCOPE_LEDGER','rows':rows},f,indent=2)
print(json.dumps({'status':'DEPENDENCY_LEDGER_RECORDED','theorems':len(rows)}))
