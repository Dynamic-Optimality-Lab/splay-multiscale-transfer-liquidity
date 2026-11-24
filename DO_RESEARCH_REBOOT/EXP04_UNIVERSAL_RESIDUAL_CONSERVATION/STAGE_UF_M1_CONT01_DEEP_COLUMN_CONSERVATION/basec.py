from pathlib import Path
import sys,json,hashlib,time,atexit,subprocess
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
M1=BASE/'STAGE_UF_M1_SAME_COLUMN_CONSERVATION';M0=BASE/'STAGE_UF_M0_GLOBAL_FOREST_FOUNDATION'
sys.path.insert(0,str(M1));sys.path.insert(0,str(M0))
import base1,base0
from base0 import REPO,Counter,defaultdict,SimpleNamespace

def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(n,x):(ROOT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def hfile(p):return base0.hfile(p)

class Meter:
    def __init__(self,stage):
        self.stage=stage;self.cpu=time.process_time();self.wall=time.perf_counter();self.ok=False;self.info={}
        self.name='CPU_'+stage+'.json';k=2
        while (ROOT/self.name).exists():self.name='CPU_'+stage+f'_{k}.json';k+=1
        atexit.register(self.close)
    def close(self):write(self.name,{'stage':self.stage,'completed':self.ok,'cpu_seconds':time.process_time()-self.cpu,
        'wall_seconds':time.perf_counter()-self.wall,'memory':base0.old.inherited.memory(),**self.info})

def preserve():
    m=load(M1/'M1_DELIVERY_MANIFEST.json')
    files={p.relative_to(M1).as_posix() for p in M1.rglob('*') if p.is_file() and p.name!='M1_DELIVERY_MANIFEST.json'}
    assert files==set(m['files'])
    for p,h in m['files'].items():assert hfile(M1/p)==h,p
    return {'M1_manifest_sha256':hfile(M1/'M1_DELIVERY_MANIFEST.json'),'M1_files_verified':len(files),
        'HEAD':m['HEAD'],'branch':m['branch'],'transitive':base1.preserve()}

def controls():
    old=load(M0/'SOURCE_CATALOG.json');new=load(M1/'NEW_SOURCE_CATALOG.json');out=[]
    for i,z in enumerate(old):
        out.append({'source':z['source'],'physical':str(M0/f'PHYS_{i:02}.json'),
            'forest':str(M0/f'FOREST_{i:02}.json'),'weights':str(M0/f'WEIGHTS_{i:02}.json'),
            'M1_audit':str(M1/f'HISTORICAL_AUDIT_{i:02}.json'),'origin':'M0','index':i})
    for i,s in enumerate(new):
        out.append({'source':s,'physical':str(M1/f'NEW_PHYS_{i:02}.json'),
            'forest':str(M1/f'NEW_FOREST_{i:02}.json'),'weights':str(M1/f'NEW_WEIGHTS_{i:02}.json'),
            'M1_audit':str(M1/f'NEW_AUDIT_{i:02}.json'),'origin':'M1','index':i})
    return out

if __name__=='__main__':
    m=Meter('preflight');write('INPUT_MANIFEST.json',preserve());m.ok=True
    print('PASS exact M1/M0 and transitive preservation',flush=True)
