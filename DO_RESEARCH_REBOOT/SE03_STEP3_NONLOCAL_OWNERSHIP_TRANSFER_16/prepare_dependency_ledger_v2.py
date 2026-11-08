"""Correct the discovery anchor; preserve failed metadata-only attempt1.
C13 has CORE7_FULL_FUNDING.md, not the anticipated FULL_PROOF.md.
No inherited artifact is changed and no proof check is rerun.
"""
from pathlib import Path
p=Path(__file__).with_name('prepare_dependency_ledger.py')
source=p.read_text(encoding='utf-8').replace(
    "('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','FULL_PROOF.md')",
    "('SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13','CORE7_FULL_FUNDING.md')")
exec(compile(source,str(p),'exec'))
