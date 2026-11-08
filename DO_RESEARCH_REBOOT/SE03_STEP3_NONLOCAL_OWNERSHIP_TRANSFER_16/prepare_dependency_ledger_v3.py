"""Use the actually discovered C13 core7 seal, preserving both failed
metadata discovery attempts. No historical proof or source check is run.
"""
from pathlib import Path
p=Path(__file__).with_name('prepare_dependency_ledger.py')
source=p.read_text(encoding='utf-8').replace(
    "('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','FULL_PROOF.md')",
    "('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','CORE7_FULL_FUNDING.md')").replace(
    "('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','independent_audit.json')",
    "('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','core7_seal.json')")
exec(compile(source,str(p),'exec'))
