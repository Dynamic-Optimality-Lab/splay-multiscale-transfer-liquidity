from pathlib import Path
import sys,json,time,atexit,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent;C2=PARENT/'CONTINUATION_02_HARD_RESIDUAL_CONSERVATION'
C1=PARENT/'CONTINUATION_01_COVERAGE_PROOF';REPO=ROOT.parents[2]
sys.path.insert(0,str(C2))
import campaign as c2base
from campaign import *
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent;C2=PARENT/'CONTINUATION_02_HARD_RESIDUAL_CONSERVATION'
C1=PARENT/'CONTINUATION_01_COVERAGE_PROOF';REPO=ROOT.parents[2]
c2base.ROOT=ROOT;c2base.inherited.ROOT=ROOT
c2base.inherited.frozen.ROOT=ROOT;c2base.inherited.frozen.prior.ROOT=ROOT
c2base.inherited.inherited_distortion.ROOT=ROOT;c2base.inherited.inherited_frame.ROOT=ROOT


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')


class Meter:
    def __init__(self,stage):
        self.stage=stage;self.cpu=time.process_time();self.wall=time.perf_counter();self.success=False;self.details={}
        base='RESOURCE_'+stage[:32];name=base+'.json';v=2
        while (ROOT/name).exists():name=base+f'_v{v:03d}.json';v+=1
        self.name=name;atexit.register(self.finish)
    def finish(self):
        write(self.name,{'stage':self.stage,'status':'completed' if self.success else 'failed_or_interrupted',
            'process_CPU_seconds':time.process_time()-self.cpu,'wall_seconds':time.perf_counter()-self.wall,
            'memory':memory(),**self.details})


if __name__=='__main__':
    meter=Meter('preflight')
    manifest=json.loads((C2/'CONT02_DELIVERY_MANIFEST.json').read_text())
    for p,h in manifest['files'].items():assert file_hash(C2/p)==h,p
    import checkpoint_finalize as previous
    previous.ROOT=C2
    pins=previous.inherited_pins()
    exp1=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    refs=['EXP01_DISCOVERY_REPORT.md','EXP01_SOURCE_WITNESSES.json','EXP01_INCIDENCE_CERTIFICATES.json',
          'exp01_diagnostics.py','exp01_sources.py','exp01_incidence.py']
    write('INPUT_MANIFEST.json',{'C2_manifest_sha256':file_hash(C2/'CONT02_DELIVERY_MANIFEST.json'),
        'C2_files':manifest['files'],'historical_pin_counts':pins,
        'EXP01_root_entry_inputs':{p:file_hash(exp1/p) for p in refs},
        'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        'requested_R_upper_equals_C2_R_upper':True,
        'primary_interface':'Q_B<=(47+48 C_seq+102 C_DF)A+R_upper'})
    meter.success=True;meter.details.update(C2_files=len(manifest['files']),historical_pin_counts=pins)
    print('PASS C2 preservation and transitive pins',pins,flush=True)
