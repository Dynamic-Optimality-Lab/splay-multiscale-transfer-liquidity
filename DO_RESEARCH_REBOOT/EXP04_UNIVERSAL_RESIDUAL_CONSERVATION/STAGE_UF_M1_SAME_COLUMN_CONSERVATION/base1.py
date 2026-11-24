from pathlib import Path
import sys,json,hashlib,time,atexit,subprocess
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
M0=BASE/'STAGE_UF_M0_GLOBAL_FOREST_FOUNDATION'
sys.path.insert(0,str(M0))
import base0
from base0 import REPO,Counter,defaultdict,SimpleNamespace

def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(name,obj):(ROOT/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def hfile(p):return base0.hfile(p)

class Meter:
    def __init__(self,stage):
        self.cpu=time.process_time();self.wall=time.perf_counter();self.stage=stage;self.ok=False;self.info={}
        self.name='CPU_'+stage+'.json';k=2
        while (ROOT/self.name).exists():self.name='CPU_'+stage+f'_{k}.json';k+=1
        atexit.register(self.close)
    def close(self):
        write(self.name,{'stage':self.stage,'completed':self.ok,'cpu_seconds':time.process_time()-self.cpu,
            'wall_seconds':time.perf_counter()-self.wall,'memory':base0.old.inherited.memory(),**self.info})

def preserve():
    manifest=load(M0/'M0_DELIVERY_MANIFEST.json')
    actual={p.relative_to(M0).as_posix() for p in M0.rglob('*') if p.is_file() and p.name!='M0_DELIVERY_MANIFEST.json'}
    assert actual==set(manifest['files'])
    for n,h in manifest['files'].items():assert hfile(M0/n)==h,n
    old=base0.preservation()
    for n,h in load(M0/'INPUT_MANIFEST.json')['M0_additional_pins'].items():assert hfile(REPO/n)==h,n
    assert manifest['HEAD']==old['HEAD'] and manifest['branch']==old['branch']
    return {'M0_manifest_sha256':hfile(M0/'M0_DELIVERY_MANIFEST.json'),'M0_files_verified':len(actual),
            'HEAD':manifest['HEAD'],'branch':manifest['branch'],'transitive':old}

if __name__=='__main__':
    meter=Meter('preflight');write('INPUT_MANIFEST.json',preserve());meter.ok=True
    print('PASS M0 exact seal and all transitive historical pins',flush=True)
