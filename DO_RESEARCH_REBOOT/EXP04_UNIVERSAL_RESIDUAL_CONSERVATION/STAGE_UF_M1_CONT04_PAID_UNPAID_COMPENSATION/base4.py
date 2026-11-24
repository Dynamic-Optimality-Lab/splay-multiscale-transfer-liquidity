from pathlib import Path
import sys,json,hashlib,time,atexit,subprocess,copy,ast,gc
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
C3=BASE/'STAGE_UF_M1_CONT03_PACKET_PACKING'
sys.path.insert(0,str(C3))
import base3 as prev
from base3 import REPO,C2,C1,M1,M0,Counter,defaultdict,SimpleNamespace

def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(n,x):(ROOT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def hfile(p):return prev.hfile(p)
def memory():return prev.prev.prev.base0.old.inherited.memory()

class Meter:
    def __init__(self,name):
        self.name=f'CPU_{name}.json';i=2
        while (ROOT/self.name).exists():self.name=f'CPU_{name}_{i}.json';i+=1
        self.cpu=time.process_time();self.wall=time.perf_counter();self.ok=False;self.info={}
        atexit.register(self.close)
    def close(self):write(self.name,{'completed':self.ok,'cpu_seconds':time.process_time()-self.cpu,
        'wall_seconds':time.perf_counter()-self.wall,'memory':memory(),**self.info})

def preserve():
    m=load(C3/'M1_CONT03_DELIVERY_MANIFEST.json')
    fs={p.relative_to(C3).as_posix() for p in C3.rglob('*') if p.is_file() and p.name!='M1_CONT03_DELIVERY_MANIFEST.json'}
    assert fs==set(m['files'])
    for n,h in m['files'].items():assert hfile(C3/n)==h,n
    p=prev.preserve();assert p==load(C3/'INPUT_MANIFEST.json')
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    return {'C3_manifest_sha256':hfile(C3/'M1_CONT03_DELIVERY_MANIFEST.json'),'C3_files_verified':len(fs),
        'HEAD':p['HEAD'],'branch':p['branch'],'transitive':p}

if __name__=='__main__':
    m=Meter('preflight');write('INPUT_MANIFEST.json',preserve());m.ok=True
    print('PASS C3 exact167-file seal and all transitive preservation',flush=True)
