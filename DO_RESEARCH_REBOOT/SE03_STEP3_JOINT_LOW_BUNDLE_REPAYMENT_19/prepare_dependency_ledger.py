"""Metadata-only exact scope/hash ledger. Never an independent audit."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
rows=[]
for x in read(OLD/'dependency_ledger.json')['rows']:
    y=dict(x);assert sha(ROOT/y['path'])==y['sha256'],y['path']
    y['C19_provenance']='inherited exact status/checks reused; metadata hash only'
    rows.append(y)
new=[
 ('FROZEN_LOW_BUNDLE_OBLIGATION.md','Exact C18 remaining obligation and parent U19 theorem, source scope and all ambiguity retained','FROZEN_OPEN_TARGET'),
 ('MULTIBUNDLE_REPAYMENT.md','F19 arbitrary finite mixed A80/B82 static physical comparison, global seam and algebraic original-owner preservation','RESTRICTED_PROVED-DERIVATION / AUDIT-PENDING'),
 ('COLLECTIVE_SOURCE_SUPPLY.md','T19 actual zero-death to distinct next same-key unary birth injection; alternative comparison preserves entire physical image','PROVED-DERIVATION / AUDIT-PENDING'),
 ('COMPARISON_SAFE_FRONTIERS.md','R19 H1 old-root birth plus at most one other; immediate direct targeting q1; marked-outer exception','PROVED-DERIVATION / AUDIT-PENDING'),
 ('LEAF_RECOVERY_BARRIER.md','Consecutive natural-zero run ending H=c has length<=r-1-2c; leaf recovery does not imply sufficient A spare','PROVED-DERIVATION / AUDIT-PENDING'),
 ('BIRTH_GROUP_REDUCTION.md','Group transported arrivals by actual birth macro; pay min(k,T) from source-disjoint own tails; concentrated residual remains','PROVED-DERIVATION / AUDIT-PENDING'),
 ('ADVERSARIAL_AUDIT.md','Exact restricted-first-reset and local-birth-tail strategy failures, not main theorem refutations','SCOPED_REFUTATIONS-DERIVATION / AUDIT-PENDING'),
 ('GATE_U_DISCHARGE.md','I6 and sufficient transfer reused; E_r2/general E_r3 and universal LOW incomplete','U-OPEN'),
 ('FINAL_VERDICT.md','Universal result unresolved; restricted family/source reductions only','UNRESOLVED')]
for name,statement,status in new:
    f=B/name
    rows.append({'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f),
      'exact_theorem_statement':statement,'result_state':status,
      'source_domain':'exact paper hypotheses; maximal-core source lemmas or specified r7 block family; never arbitrary-support funding by finite tests',
      'physical_event_semantics':'original ordinary splay; A StepEv ceil(depth/2) including zig; BF doubles floor(depth/2); DELETE A-only',
      'owner_policy':'fixed original a/common/fE under exact source license; alternative comparison is not an in-run mutation of immutable receipts',
      'audit_status':'producer derivation only; no independent run fits unchanged allowance',
      'proof_inspection':'C19 mathematical derivation and source profiles; distinct audit pending'})
out('dependency_ledger.json',{'status':'EXACT_SCOPE_METADATA_NOT_SEAL','rows':rows,
 'inherited_ledger':(OLD/'dependency_ledger.json').relative_to(ROOT).as_posix(),
 'universal_JOINT_LOW':'OPEN','metadata_CPU_excluded':time.process_time()})
print(json.dumps({'status':'DEPENDENCY_METADATA_PUBLISHED','rows':len(rows)}))
