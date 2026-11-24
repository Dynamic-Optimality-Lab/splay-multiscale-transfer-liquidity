from pathlib import Path
import sys,json,time,atexit,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent;C3=PARENT/'CONTINUATION_03_UPPER_PARENT'
sys.path.insert(0,str(C3))
import campaign3 as previous
from campaign3 import *
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;C3=PARENT/'CONTINUATION_03_UPPER_PARENT'
previous.ROOT=ROOT;previous.c2base.ROOT=ROOT;previous.c2base.inherited.ROOT=ROOT
previous.c2base.inherited.frozen.ROOT=ROOT;previous.c2base.inherited.frozen.prior.ROOT=ROOT
previous.c2base.inherited.inherited_distortion.ROOT=ROOT;previous.c2base.inherited.inherited_frame.ROOT=ROOT


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')


class Meter:
    def __init__(self,stage):
        self.stage=stage;self.cpu=time.process_time();self.wall=time.perf_counter();self.success=False;self.details={}
        base='RESOURCE_'+stage[:28];name=base+'.json';v=2
        while (ROOT/name).exists():name=base+f'_{v:03d}.json';v+=1
        self.name=name;atexit.register(self.finish)
    def finish(self):
        write(self.name,{'stage':self.stage,'process_CPU_seconds':time.process_time()-self.cpu,
            'wall_seconds':time.perf_counter()-self.wall,'status':'completed' if self.success else 'failed_or_interrupted',
            'memory':memory(),**self.details})


if __name__=='__main__':
    meter=Meter('preflight')
    m=json.loads((C3/'CONT03_DELIVERY_MANIFEST.json').read_text())
    for p,h in m['files'].items():assert file_hash(C3/p)==h,p
    c3=json.loads((C3/'INPUT_MANIFEST.json').read_text())
    assert file_hash(C2/'CONT02_DELIVERY_MANIFEST.json')==c3['C2_manifest_sha256']
    for p,h in c3['C2_files'].items():assert file_hash(C2/p)==h,p
    import checkpoint_finalize as c2verify
    c2verify.ROOT=C2;pins=c2verify.inherited_pins()
    write('INPUT_MANIFEST.json',{'C3_manifest_sha256':file_hash(C3/'CONT03_DELIVERY_MANIFEST.json'),
        'C3_files':m['files'],'C2_files':c3['C2_files'],'historical_pin_counts':pins,
        'EXP01_root_entry_inputs':c3['EXP01_root_entry_inputs'],
        'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        'original_R_upper_and_all_predicates_unchanged':True})
    meter.success=True;print('PASS C3/C2 and inherited preservation',flush=True)
