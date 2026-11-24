from pathlib import Path
import sys,json,hashlib,time,atexit,subprocess,copy
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
C1=BASE/'STAGE_UF_M1_CONT01_DEEP_COLUMN_CONSERVATION'
sys.path.insert(0,str(C1))
import basec as prev
from basec import REPO,M1,M0,Counter,defaultdict,SimpleNamespace

def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(n,x):(ROOT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def hfile(p):return prev.hfile(p)

class Meter:
    def __init__(self,name):
        self.name='CPU_'+name+'.json';i=2
        while (ROOT/self.name).exists():self.name=f'CPU_{name}_{i}.json';i+=1
        self.cpu=time.process_time();self.wall=time.perf_counter();self.ok=False;self.info={}
        atexit.register(self.close)
    def close(self):write(self.name,{'completed':self.ok,'cpu_seconds':time.process_time()-self.cpu,
        'wall_seconds':time.perf_counter()-self.wall,'memory':prev.base0.old.inherited.memory(),**self.info})

def preserve():
    m=load(C1/'M1_CONT01_DELIVERY_MANIFEST.json')
    fs={p.relative_to(C1).as_posix() for p in C1.rglob('*') if p.is_file() and p.name!='M1_CONT01_DELIVERY_MANIFEST.json'}
    assert fs==set(m['files'])
    for n,h in m['files'].items():assert hfile(C1/n)==h,n
    p=prev.preserve();assert p==load(C1/'INPUT_MANIFEST.json')
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    return {'C1_manifest_sha256':hfile(C1/'M1_CONT01_DELIVERY_MANIFEST.json'),'C1_files_verified':len(fs),
        'HEAD':p['HEAD'],'branch':p['branch'],'transitive':p}

def controls():
    out=[{**z,'birth':str(C1/f'BIRTH_{i:02}.json')} for i,z in enumerate(prev.controls())]
    for stem,cat in (('NEW','NEW_SOURCE_CATALOG.json'),('GUARDED','GUARDED_SOURCES.json')):
        for i,s in enumerate(load(C1/cat)):
            out.append({'source':s,'physical':str(C1/f'{stem}_PHYS_{i:02}.json'),
                'forest':str(C1/f'{stem}_FOREST_{i:02}.json'),'weights':str(C1/f'{stem}_WEIGHTS_{i:02}.json'),
                'M1_audit':str(C1/f'{stem}_M1_AUDIT_{i:02}.json'),'birth':str(C1/f'{stem}_BIRTH_{i:02}.json'),
                'origin':'C1_'+stem,'index':i})
    return out

if __name__=='__main__':
    m=Meter('preflight');write('INPUT_MANIFEST.json',preserve());m.ok=True
    print('PASS C1/M1/M0 exact seals and transitive preservation',flush=True)
