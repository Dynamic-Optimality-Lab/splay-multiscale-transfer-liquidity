"""Read-only inherited engines; every new output belongs to Continuation04."""
from pathlib import Path
import sys,json,time,atexit,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
C3B=ROOT.parent/'CONT03B_PACKET_OBSTRUCTIONS'
sys.path.insert(0,str(C3B))
import campaign3b as previous
from campaign3b import *
previous=sys.modules['campaign3b']
ROOT=Path(__file__).resolve().parent
C3B=ROOT.parent/'CONT03B_PACKET_OBSTRUCTIONS'
previous.ROOT=ROOT
previous.previous.ROOT=ROOT
previous.previous.c2base.ROOT=ROOT
previous.previous.c2base.inherited.ROOT=ROOT
previous.previous.c2base.inherited.frozen.ROOT=ROOT
previous.previous.c2base.inherited.frozen.prior.ROOT=ROOT
previous.previous.c2base.inherited.inherited_distortion.ROOT=ROOT
previous.previous.c2base.inherited.inherited_frame.ROOT=ROOT

def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')

class Meter:
    def __init__(self,stage):
        self.stage=stage;self.cpu=time.process_time();self.wall=time.perf_counter();self.success=False;self.details={}
        stem='RESOURCE_'+stage[:20];self.name=stem+'.json';i=2
        while (ROOT/self.name).exists():self.name=stem+f'_{i}.json';i+=1
        atexit.register(self.finish)
    def finish(self):
        write(self.name,{'stage':self.stage,'process_CPU_seconds':time.process_time()-self.cpu,
            'wall_seconds':time.perf_counter()-self.wall,'status':'completed' if self.success else 'failed_or_interrupted',
            'memory':memory(),**self.details})

def preservation():
    manifests=[(C3B,'CONT03B_DELIVERY_MANIFEST.json'),(C3,'CONT03_DELIVERY_MANIFEST.json'),
        (C2,'CONT02_DELIVERY_MANIFEST.json'),(C1,'CONT01_DELIVERY_MANIFEST.json'),
        (PARENT,'EXP04_DELIVERY_MANIFEST.json')]
    out=[]
    for d,name in manifests:
        m=json.loads((d/name).read_text())
        for p,h in m['files'].items():assert file_hash(d/p)==h,(d.name,p)
        out.append({'directory':str(d),'manifest':name,'sha256':file_hash(d/name),'verified_files':len(m['files'])})
    old=json.loads((C3B/'INPUT_MANIFEST.json').read_text())
    import checkpoint_finalize as pins
    pins.ROOT=C2
    prior=pins.inherited_pins()
    exp1=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    for p,h in old['EXP01_root_entry_inputs'].items():assert file_hash(exp1/p)==h,p
    return {'checkpoints':out,'transitive_preservation':prior,'EXP01_root_entry_inputs':old['EXP01_root_entry_inputs']}

if __name__=='__main__':
    meter=Meter('preflight');p=preservation()
    write('INPUT_MANIFEST.json',{**p,'date':'2026-11-11',
        'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        'branch':subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip(),
        'allocation':{'initial_research_CPU_seconds':600,'working_set_aim_bytes':3*1024**3,
            'initial_physical_population_ceiling':2051,'initial_source_operation_ceiling':16384,
            'reviewable_limits_not_theorem_assumptions':True},
        'original_interface':'47+48 C_seq+102 C_DF plus literal R_overflow'})
    meter.success=True;print('PASS inherited manifests and transitive pins',flush=True)
