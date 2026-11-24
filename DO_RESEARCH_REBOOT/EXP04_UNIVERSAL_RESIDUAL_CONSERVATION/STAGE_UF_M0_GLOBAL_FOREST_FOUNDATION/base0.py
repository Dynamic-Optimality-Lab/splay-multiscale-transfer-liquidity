from pathlib import Path
import sys,json,hashlib,time,atexit,subprocess
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
C5=BASE/'CONTINUATION_05_UNIVERSAL_RESTORATION_CLOSURE'
sys.path.insert(0,str(C5))
import stage5 as old
from stage5 import REPO
from collections import defaultdict,Counter
from types import SimpleNamespace

def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(n,x):(ROOT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def hfile(p):return old.filehash(p)

class Meter:
    def __init__(self,stage):
        self.stage=stage;self.cpu=time.process_time();self.wall=time.perf_counter();self.ok=False
        self.name='CPU_'+stage+'.json';k=2;self.info={}
        while (ROOT/self.name).exists():self.name='CPU_'+stage+f'_{k}.json';k+=1
        atexit.register(self.close)
    def close(self):
        write(self.name,{'stage':self.stage,'completed':self.ok,
            'cpu_seconds':time.process_time()-self.cpu,'wall_seconds':time.perf_counter()-self.wall,
            'memory':old.inherited.memory(),**self.info})

def preservation():
    m=load(C5/'CONT05_DELIVERY_MANIFEST.json')
    files={p.relative_to(C5).as_posix() for p in C5.rglob('*') if p.is_file()
           and p.name!='CONT05_DELIVERY_MANIFEST.json'}
    assert files==set(m['files'])
    for p,h in m['files'].items():assert hfile(C5/p)==h,p
    prior=old.preserve()
    inp=load(C5/'INPUT_MANIFEST.json')
    for p,h in inp['additional_file_hashes'].items():assert hfile(REPO/p)==h,p
    return {'C05_manifest_sha256':hfile(C5/'CONT05_DELIVERY_MANIFEST.json'),
            'C05_files_verified':len(files),'transitive':prior,
            'HEAD':m['HEAD'],'branch':m['branch']}

if __name__=='__main__':
    meter=Meter('preflight');p=preservation()
    deps=[
        'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
        'DO_RESEARCH_REBOOT/IAGS12_D4_NEUTRAL_RENEWAL.md',
        'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY/exp01_oracle.py',
        'DO_RESEARCH_REBOOT/EXP04_UNIVERSAL_RESIDUAL_CONSERVATION/CONTINUATION_03_UPPER_PARENT/epoch_payment.py',
        'DO_RESEARCH_REBOOT/EXP04_UNIVERSAL_RESIDUAL_CONSERVATION/CONT03B_PACKET_OBSTRUCTIONS/packet_payments.py',
        'DO_RESEARCH_REBOOT/EXP04_UNIVERSAL_RESIDUAL_CONSERVATION/CONTINUATION_04_PACKET_OVERFLOW/ACCOUNTING_AUDIT.md']
    p['M0_additional_pins']={x:hfile(REPO/x) for x in deps}
    write('INPUT_MANIFEST.json',p);meter.ok=True
    print('PASS C05 exact delivery and complete transitive pins',flush=True)
