from pathlib import Path
import sys,json,hashlib,time,atexit,subprocess,copy,ast,gc
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
C6=BASE/'STAGE_UF_M1_CONT06_NESTED_RENEWAL_CONSERVATION'
sys.path.insert(0,str(C6))
import base6 as prev
from base6 import REPO,C5,C4,C3,C2,C1,M1,M0,Counter,defaultdict,SimpleNamespace

MANIFEST='M1_CONT07_DELIVERY_MANIFEST.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(n,x):(ROOT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def hfile(p):return prev.hfile(p)
def memory():return prev.memory()
def unsealed():assert not (ROOT/MANIFEST).exists(),'Sealed stage; use finalize7.py --verify-only.'
class Meter:
    def __init__(self,name):
        self.name=f'CPU_{name}.json';i=2
        while (ROOT/self.name).exists():self.name=f'CPU_{name}_{i}.json';i+=1
        self.cpu=time.process_time();self.wall=time.perf_counter();self.ok=False;self.info={};atexit.register(self.close)
    def close(self):write(self.name,{'completed':self.ok,'cpu_seconds':time.process_time()-self.cpu,'wall_seconds':time.perf_counter()-self.wall,'memory':memory(),**self.info})
def preserve():
    m=load(C6/'M1_CONT06_DELIVERY_MANIFEST.json')
    fs={p.relative_to(C6).as_posix() for p in C6.rglob('*') if p.is_file() and p.name!='M1_CONT06_DELIVERY_MANIFEST.json'}
    assert fs==set(m['files'])
    for n,h in m['files'].items():assert hfile(C6/n)==h,n
    p=prev.preserve();assert p==load(C6/'INPUT_MANIFEST.json')
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    return {'C6_manifest_sha256':hfile(C6/'M1_CONT06_DELIVERY_MANIFEST.json'),'C6_files_verified':len(fs),'HEAD':p['HEAD'],'branch':p['branch'],'transitive':p}
if __name__=='__main__':
    unsealed();m=Meter('preflight');write('INPUT_MANIFEST.json',preserve());m.ok=True;print('PASS exact C6 seal and full inherited history/Git state',flush=True)
