"""Verify all saved complete source grammars without repeating splay work."""
import importlib.util
import json
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('new_source_recipes',HERE/'replay.py')
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
results=[]
for file in sorted(HERE.glob('*_complete_witness.json')):
    saved=json.loads(file.read_text())['source']
    actual=R.source(*(saved[k] for k in ['h','radius','interleavings','copies','reflected']))
    assert json.loads(json.dumps(actual))==saved
    results.append({'file':file.name,'complete_word_and_full_initial_tree_match':True})
out={'passed':True,'sources':results,'additional_splay_rotations':0}
if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'SOURCE_GRAMMAR_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'passed':True,'complete_source_grammars':len(results),'additional_splay_rotations':0}))
