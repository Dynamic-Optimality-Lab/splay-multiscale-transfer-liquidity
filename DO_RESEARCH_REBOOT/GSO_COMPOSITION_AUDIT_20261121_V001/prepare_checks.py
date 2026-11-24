"""Use the sealed original-event interface; write only new companion artifacts."""
import importlib.util
import json
import sys
import composition as M
K=M.K
sys.path.insert(0,str(M.PREVIOUS))
spec=importlib.util.spec_from_file_location('composition_pinned_source_audit',M.PREVIOUS/'source_audit.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
sys.path.pop(0)


def main():
    folder=M.HERE/'original_event_companions';folder.mkdir(exist_ok=True)
    for path in sorted(M.HERE.glob('source_*.json.gz')):
        old=K.load(path);s=old['source'];selected={1,2} if path.name in ('source_01.json.gz','source_02.json.gz') else set()
        if (folder/path.name).exists():
            rep=K.load(folder/path.name);assert rep['source']==s and rep['A']==old['A'] and rep['Q_B']==old['Q_B'] and rep['original_U']==old['original_U'];continue
        rep=audit.audit(s,selected);assert rep['A']==old['A'] and rep['Q_B']==old['Q_B'] and json.loads(json.dumps(rep['original_U']))==old['original_U']
        M.write('original_event_companions/'+path.name,rep)
    print('Prepared13 complete original-event companions without writing old checkpoints.')


if __name__=='__main__':main()
