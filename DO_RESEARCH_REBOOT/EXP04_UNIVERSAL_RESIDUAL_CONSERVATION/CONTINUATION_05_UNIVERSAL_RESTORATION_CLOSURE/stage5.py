"""Preflight and deterministic receipts; no historical producer is run."""
from pathlib import Path
import hashlib, json, subprocess, sys, time, atexit

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
C4 = BASE / 'CONTINUATION_04_PACKET_OVERFLOW'
REPO = BASE.parents[1]
sys.path.insert(0, str(C4))
import campaign4 as inherited

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':'), sort_keys=True).encode()).hexdigest()

def filehash(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

class Meter:
    def __init__(self, stage):
        self.stage=stage; self.cpu=time.process_time(); self.wall=time.perf_counter()
        self.success=False; self.details={}
        self.name='CPU_'+stage+'.json'; k=2
        while (ROOT/self.name).exists():
            self.name='CPU_'+stage+f'_{k}.json'; k+=1
        atexit.register(self.finish)
    def finish(self):
        write(self.name, {'stage':self.stage,'completed':self.success,
            'cpu_seconds':time.process_time()-self.cpu,'wall_seconds':time.perf_counter()-self.wall,
            'memory':inherited.memory(), **self.details})

def preserve():
    m=load(C4/'CONT04_DELIVERY_MANIFEST.json')
    actual={p.relative_to(C4).as_posix() for p in C4.rglob('*') if p.is_file()
            and p.name!='CONT04_DELIVERY_MANIFEST.json'}
    assert actual==set(m['files'])
    for p,h in m['files'].items():
        assert filehash(C4/p)==h,p
    old=inherited.preservation()
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head==m['HEAD']=='6d532b2c795c0778f57d8023b23b5fedfc48b010'
    assert branch==m['branch']=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    return {'C04_manifest_sha256':filehash(C4/'CONT04_DELIVERY_MANIFEST.json'),
            'C04_files_verified':len(actual),'transitive':old,'HEAD':head,'branch':branch}

if __name__=='__main__':
    meter=Meter('preflight')
    manifest=preserve()
    r=REPO/'DO_RESEARCH_REBOOT'
    dependencies=[
        r/'RESEARCH_RULES.md',r/'ORIGINAL_PIPELINE.md',
        r/'02_PROVED/PIVOT2_CONDITIONAL_REDUCTION.md',r/'02_PROVED/C_ZIG_RECONSTRUCTED.md',
        r/'01_MAIN_PIPELINE/stage_01_levy_tarjan.md',
        r/'ROUTE04_RELAXED_UNIVERSAL_CD_20261108/RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md',
        r/'06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md',
        REPO/'python/independent/splay.py',
        REPO/'v03/history/external/papers/L3_levy_tarjan_foundation_1907.06310.pdf',
    ]
    manifest['additional_file_hashes']={p.relative_to(REPO).as_posix():filehash(p) for p in dependencies}
    write('INPUT_MANIFEST.json',manifest)
    meter.success=True; print('PASS C04 exact file set and transitive dependencies',flush=True)
