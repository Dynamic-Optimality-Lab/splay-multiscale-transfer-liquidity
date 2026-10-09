"""Check handbook completeness and finite verification outputs; no source writes."""
import json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1]
required=['README.md','START_HERE.md','CURRENT_STATE.md','ORIGINAL_PIPELINE.md',
 'THEOREM_DEPENDENCIES.md','CLAIM_LEDGER.md','EVIDENCE_INDEX.md','RECONSTRUCTION_REPORT.md',
 'RESEARCH_RULES.md','PIVOT_APPROVAL_GATE.md','STRATEGY_REVIEW.md','NEXT_ACTION.md','WORKLOG.md']
assert all((W/p).is_file() and (W/p).stat().st_size>0 for p in required)
fields=['THEOREM ID','NAME','EXACT STATEMENT','QUANTIFIERS','CONSTANTS','DEFINITIONS','PREREQUISITES',
 'KNOWN PROOFS','KNOWN FINITE EVIDENCE','KNOWN COUNTEREXAMPLES','UNVERIFIED ASSUMPTIONS',
 'CURRENT STATUS','SOURCE LOCATIONS','HOW IT ADVANCES DO','STAGE COMPLETION','PROOF VERIFICATION']
stages=list((W/'01_MAIN_PIPELINE').glob('*.md'))
assert len(stages)==11
for p in stages:
    txt=p.read_text(encoding='utf-8')
    assert all('**'+f+':' in txt for f in fields),p
broken=[]
for p in W.rglob('*.md'):
    txt=p.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',txt):
        if '://' in target or target.startswith('#'):continue
        if not (p.parent/target.split('#')[0]).exists():broken.append([str(p.relative_to(W)),target])
assert not broken,broken
vr=json.loads((W/'10_EXPERIMENTS/verification_results.json').read_text())
assert vr['status']=='PASS'
lr=json.loads((W/'06_CERTIFICATES/LRF_EXACT_RECHECK.json').read_text())
assert lr['zero_residual'] and lr['positive_rhs']=='9/34'
cr=json.loads((W/'06_CERTIFICATES/C0_RANK_EXACT_RECHECK.json').read_text())
assert cr['rank_Q']==48 and cr['rational_nullity']==31 and cr['full_exact_zero_residual']
hashes=json.loads((W/'11_REPRODUCIBILITY/source_hashes.json').read_text())
baseline=json.loads((W/'11_REPRODUCIBILITY/baseline.json').read_text())
assert all(baseline['files'][h['path']]['sha256']==h['sha256'] for h in hashes)
out={'status':'PASS','mandatory_core_documents':len(required),'stage_references':len(stages),
 'source_hashes_match_entry_baseline':len(hashes),'broken_local_links':broken,
 'scope':'deliverable completeness and output consistency, not independent formal theorem verification',
 'files_under_workspace':len([p for p in W.rglob('*') if p.is_file()])}
(W/'11_REPRODUCIBILITY/workspace_validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
