"""All 16 deterministic source recipes. Default: grammar check without splaying.

--replay is allowed only in a fresh version with no existing witnesses or seal.
This keeps the bounded original run and its history immutable.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lifecycle_recipes', HERE/'lifecycle.py')
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)


def recipes():
    cases = [(1,1,1,3,'I',False,False), (1,1,1,3,'J',False,False),
             (1,1,2,3,'I',False,False), (1,1,2,3,'J',False,False),
             (1,1,3,2,'J',False,False), (1,1,2,2,'J',True,False),
             (3,1,1,2,'J',False,False), (2,5,1,2,'I',False,False),
             (3,5,1,2,'I',False,False), (2,5,1,2,'J',False,False),
             (1,5,1,2,'I',False,False), (3,1,1,2,'J',False,True),
             (1,1,2,2,'I',True,True), (1,2,1,2,'J',False,False),
             (1,2,2,2,'I',False,False)]
    result = [L.source(*case) for case in cases]
    s = L.source(3,1,1,2,'J')
    word, seen = [], set()
    for phase, mode, target in s['word']:
        if phase.endswith(':restore_down') and phase not in seen:
            seen.add(phase)
            word.extend([(phase.split(':')[0]+':unstructured','K',2*x) for x in [3,31,4,30]])
        word.append((phase, mode, target))
    s.update(word=word, altered_restore=True, restoration_splice=[3,31,4,30])
    result.append(s)
    return result


def normalized(s):
    s = dict(s)
    s.setdefault('helpers', False)
    return json.loads(json.dumps(s))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--source-only', action='store_true')
    args = parser.parse_args()
    sources = recipes()
    if args.replay:
        assert not (HERE/'FINAL_MANIFEST.json').exists() and not list(HERE.glob('*_complete_witness.json'))
        rows = [L.run(s, save=True) for s in sources]
        (HERE/'ALL_SOURCE_AUDIT.json').write_text(json.dumps({'sources':rows,'real_rotations':L.TOTAL_ROTATIONS},indent=2),encoding='utf-8')
        return
    witnesses = list(HERE.glob('*_complete_witness.json'))
    assert len(sources) == len(witnesses) == 16
    expected = {json.dumps(normalized(s),sort_keys=True) for s in sources}
    actual = {json.dumps(normalized(json.loads(f.read_text(encoding='utf-8'))['source']),sort_keys=True) for f in witnesses}
    assert actual == expected
    out = {'passed':True,'complete_source_recipes':16,'all_saved_original_words_and_initial_full_trees_match':True,'additional_splay_rotations':0}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'SOURCE_GRAMMAR_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
