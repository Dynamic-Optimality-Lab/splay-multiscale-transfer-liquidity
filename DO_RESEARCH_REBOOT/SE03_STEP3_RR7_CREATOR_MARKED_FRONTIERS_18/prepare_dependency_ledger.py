"""Metadata-only scope/provenance publication, never a semantic audit."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_SOURCE_FORCED_MULTICOMPONENT_ESCAPE_17'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)

rows=[]
for x in read(OLD/'dependency_ledger.json')['rows']:
    y=dict(x)
    assert sha(ROOT/y['path'])==y['sha256'],y['path']
    y['inspection_provenance']='inherited C17 exact inspection/status; accepted checks reused, metadata hash checked only'
    rows.append(y)

new=[
 ('SOURCE_SPEC.md','Original source/cost/owner/period freeze','FROZEN_SPEC'),
 ('RR7_REFUTATION.md','Exact original-source counterexample to canonical RR7 protection, including full deep-root and erased-owner qualifiers','REFUTED-DERIVATION / AUDIT-PENDING'),
 ('MARKED_PARENT_THEOREM.md','Inner-edge barrier and joint at-most-two watched origins; marked creator protection refuted','PROVED-DERIVATION / AUDIT-PENDING'),
 ('HIGH_CREATOR_REDUCTION.md','g<=min(r-1,2H), protected macro-tail partial extension; high threshold closes comparison groups only','PROVED-DERIVATION / AUDIT-PENDING'),
 ('PREFIX_COLLISIONS_AND_LOW_CASES.md','Exact spent-prefix criterion and necessary LOW profiles','PROVED-DERIVATION / AUDIT-PENDING'),
 ('SOURCE_REPAIRS.md','Complete exact source maps; literal old effective/common owner preservation where supplied','PROVED-DERIVATION / AUDIT-PENDING'),
 ('LOW_OVERFLOW_AND_BUNDLE.md','Closed source refutes universal local tail capacity; exact nonlocal two-demand bundle repays this source','SOURCE-DERIVATION / AUDIT-PENDING'),
 ('FINAL_VERDICT.md','No universal escape promotion; remaining LOW supply and working/audit obligations','U-OPEN')]
for name,statement,status in new:
    p=B/name
    rows.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),
      'exact_theorem_statement':statement,'result_state':status,
      'audit_status':'no new independent run fits current allowance; metadata is not an audit',
      'inspection_provenance':'producer proof derivation and source calculations; distinct audit pending',
      'physical_event_semantics':'unchanged original ordinary splay; A StepEv ceil(depth/2), BF double floor(depth/2), DELETE A-only',
      'frozen_owner_assumptions':'actual same interval; supplied six-key license where asserted; old common/successful a fixed',
      'source_domain':'exact document scope; no extension from a finite repair to a universal supply theorem'})
out('dependency_ledger.json',{'status':'METADATA_SCOPE_LEDGER_NOT_PROOF_SEAL','rows':rows,
 'inherited_ledger':str((OLD/'dependency_ledger.json').relative_to(ROOT)).replace('\\','/'),
 'universal_source_forced_escape':'OPEN','metadata_CPU_excluded':time.process_time()})
print(json.dumps({'status':'DEPENDENCY_METADATA_PUBLISHED','rows':len(rows)}))
