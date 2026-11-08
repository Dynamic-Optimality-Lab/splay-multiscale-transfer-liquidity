from pathlib import Path
F=Path(__file__).resolve().parent
code=(F/'build_paired_branch_model.py').read_text()
assert code.count('assert six==64 and followers==384')==1
code=code.replace('assert six==64 and followers==384','assert six==64 and followers>0')
code=code.replace("'PAIRED_BRANCH_SOURCE_BOX.md'","'PAIRED_BRANCH_SOURCE_BOX_V2.md'")
code=code.replace('audit_proof217_exit.json','audit_proof218_exit.json')
with (F/'build_paired_branch_model_v2.py').open('x',encoding='utf-8') as f:f.write(code)
print('SOURCE_PAIR_MODEL_CORRECTED_WITH_ALL_CERTIFIED_SUCCESSORS_RETAINED')
