"""Persistent resource accounting and immutable SHARP-02 provenance."""
from pathlib import Path
import ctypes,hashlib,json,os,time,traceback
BASE=Path(__file__).resolve().parent
REPO=BASE.parents[1]
OLD=BASE.parent/'SHARP01_EXACT_2A_CONSERVATION'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,x):
    p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(x,separators=(',',':')),encoding='utf-8');tmp.replace(p)

def peak_memory():
    if os.name!='nt':
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    from ctypes import wintypes
    class PMC(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(s,ctypes.c_size_t) for s in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
    p=PMC();p.cb=ctypes.sizeof(p)
    ctypes.windll.kernel32.GetCurrentProcess.restype=wintypes.HANDLE
    f=ctypes.windll.psapi.GetProcessMemoryInfo;f.argtypes=[wintypes.HANDLE,ctypes.POINTER(PMC),wintypes.DWORD];f.restype=wintypes.BOOL
    if not f(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(p),p.cb):raise ctypes.WinError()
    return p.PeakWorkingSetSize

class Run:
    def __init__(self,name,limit=120,**parameters):
        (BASE/'receipts').mkdir(exist_ok=True)
        self.path=BASE/'receipts'/f'{name}.json';assert not self.path.exists(),('use a new versioned run name',name)
        self.name=name;self.t=time.process_time();self.w=time.perf_counter();self.limit=limit;self.parameters=parameters
        self.prior=sum(read(p).get('cpu_seconds',0) for p in (BASE/'receipts').glob('*.json'))
        self.data={};self.save('RUNNING')
    def save(self,status,**kw):
        self.data.update(kw)
        write(self.path,{'name':self.name,'status':status,'cpu_seconds':time.process_time()-self.t,'wall_seconds':time.perf_counter()-self.w,
                         'peak_working_set_bytes':peak_memory(),'prior_recorded_cpu_seconds':self.prior,'parameters':self.parameters,**self.data})
    def check(self,**kw):
        self.save('RUNNING',**kw)
        assert time.process_time()-self.t<self.limit,'stage CPU ceiling'
        assert self.prior+time.process_time()-self.t<900,'new cumulative SHARP-02 CPU ceiling'
        assert peak_memory()<1024**3,'SHARP-02 peak-memory ceiling'
    def __enter__(self):return self
    def __exit__(self,t,e,tb):
        self.save('PASS' if e is None else 'FAILED',error=None if e is None else ''.join(traceback.format_exception(t,e,tb)))

def bootstrap():
    delivery=read(OLD/'SHARP01_DELIVERY_MANIFEST.json');bad=[]
    for item in delivery['files']:
        p=OLD/item['path']
        if not p.exists() or sha(p)!=item['sha256']:bad.append(item['path'])
    assert not bad,bad
    vendored=['sharp01_oracle.py','sharp01_tuple_reference.py','sharp01_validate.py','sharp01_sources.py']
    for name in vendored:
        dest=BASE/name
        if not dest.exists():dest.write_bytes((OLD/name).read_bytes())
        assert sha(dest)==sha(OLD/name)
    # Pin actual bytes. All mathematical historical reading remains information,
    # never new authorization or an instruction to start another campaign.
    paths=[OLD/i['path'] for i in delivery['files']]
    names=['RESEARCH_RULES.md','IAGS12_BB02_DISCOUNTED_SUPPORT_SWITCHING.md','IAGS12_CD6_TRANSFER_TRIAD.md','RG01_PRIMITIVE_ACCOUNTING.md','RG04_GLOBAL_REGENERATION.md',
        '06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md',
        'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md',
        'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FROZEN_OWNER_COMPATIBILITY.md','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
        'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_THEOREM.md','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json',
        'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/PHYSICAL_GROUP_SEEDS.md','SE03_STEP3_UNIFORM_DONOR_GROUPING_15/ZERO_RUN_FAMILY_THEOREM.md',
        'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md','SE03_STEP3_UNIFORM_DONOR_GROUPING_15/AUDIT_CAP_CHECKPOINT.md']
    paths.extend(BASE.parent/n for n in names)
    write(BASE/'SHARP02_INPUT_HASHES.json',{'source_commit':'6d532b2c795c0778f57d8023b23b5fedfc48b010',
        'sha256':{str(p.relative_to(REPO)).replace('\\','/'):sha(p) for p in paths},'vendored_byte_exact':vendored,
        'old_resource_limitations':'SHARP-01 first-run exact CPU and peak memory unrecorded; not retroactively supplied'})
    return len(paths)

if __name__=='__main__':
    with Run('bootstrap_v001',limit=30) as run:run.check(pinned_files=bootstrap())
