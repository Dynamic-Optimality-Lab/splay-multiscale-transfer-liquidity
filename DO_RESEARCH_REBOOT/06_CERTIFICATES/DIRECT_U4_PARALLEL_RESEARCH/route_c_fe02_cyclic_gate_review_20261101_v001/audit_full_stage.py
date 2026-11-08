"""Read-only long-path Stage11G inventory; explicit legacy baseline limits."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
REL='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
STAGE=Path('\\\\?\\'+str(ROOT))/REL
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT)


def main():
    pins=read(HERE/'entry_source_pins.json')
    actual={p.relative_to(STAGE).as_posix():p.read_bytes() for p in STAGE.rglob('*') if p.is_file()}
    assert len(actual)==528
    baseline=pins['stage_files']
    assert len(baseline)==125
    for p,h in baseline.items():assert p in actual and sha(actual[p])==h,p
    tracked={}
    for raw in git('ls-tree','-r','-z','HEAD','--',REL).split(b'\0'):
        if not raw:continue
        metadata,path=raw.split(b'\t',1);mode,type_,oid=metadata.decode().split()
        assert type_=='blob' and mode=='100644'
        path=path.decode();assert path.startswith(REL+'/')
        tracked[path[len(REL)+1:]]=oid
    assert len(tracked)==510 and set(tracked)<=set(actual)
    batch=subprocess.run(['git','--no-optional-locks','cat-file','--batch'],cwd=ROOT,
        input=('\n'.join(tracked.values())+'\n').encode(),stdout=subprocess.PIPE,check=True).stdout
    pos=0;records={};mismatches=[];raw_matches=0;eol_matches=0
    for path,oid in tracked.items():
        end=batch.index(b'\n',pos);header=batch[pos:end].decode().split();pos=end+1
        assert header[0]==oid and header[1]=='blob'
        n=int(header[2]);content=batch[pos:pos+n];pos+=n;assert batch[pos:pos+1]==b'\n';pos+=1
        work=actual[path];raw_match=work==content
        eol_only=not raw_match and work.replace(b'\r\n',b'\n')==content.replace(b'\r\n',b'\n')
        raw_matches+=raw_match;eol_matches+=eol_only
        if not (raw_match or eol_only):mismatches.append(path)
        records[path]=dict(worktree_sha256=sha(work),HEAD_blob_oid=oid,HEAD_raw_sha256=sha(content),
            raw_match=raw_match,only_CRLF_LF_difference=eol_only,entry_pinned=path in baseline)
    assert pos==len(batch)
    untracked=sorted(set(actual)-set(tracked))
    newly_visible=sorted(set(actual)-set(baseline))
    data=dict(status='PASS' if not mismatches else 'CONTENT_DIFFERENCE_REQUIRES_REVIEW',
        HEAD=pins['head'],native_long_path_inventory=True,actual_file_count=len(actual),
        legacy_entry_pinned_files=len(baseline),legacy_entry_pins_all_unchanged=True,
        newly_visible_file_count=len(newly_visible),tracked_HEAD_files=len(tracked),
        tracked_raw_HEAD_matches=raw_matches,tracked_EOL_only_matches=eol_matches,
        tracked_content_differences=mismatches,untracked_file_count=len(untracked),
        untracked_entry_pinned=[p for p in untracked if p in baseline],
        untracked_without_entry_pin=[p for p in untracked if p not in baseline],
        tracked_records=records,
        untracked_current_baseline={p:sha(actual[p]) for p in untracked},
        current_full_baseline={p:sha(b) for p,b in sorted(actual.items())},
        preservation_limit='Newly visible files without entry hashes have no raw before/after proof; tracked contents are independently compared to frozen HEAD. No Stage11G file was written by this work.',
        old_125_file_complete_inventory_claim='CORRECTED:125 was the path-limited subset, not the full inventory',
        source_file_writes=0,Git_writes=False)
    with (HERE/'full_stage_inventory_review.json').open('x',encoding='utf-8') as f:json.dump(data,f,indent=2);f.write('\n')
    print(json.dumps({k:data[k] for k in ['status','actual_file_count','legacy_entry_pinned_files',
        'newly_visible_file_count','tracked_HEAD_files','tracked_raw_HEAD_matches','tracked_EOL_only_matches',
        'untracked_file_count','untracked_without_entry_pin']},indent=2))


if __name__=='__main__':main()
