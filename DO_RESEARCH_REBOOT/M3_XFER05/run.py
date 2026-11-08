"""Bounded new symbolic audit controller. No experiment or old-check replay."""
import ctypes,json,subprocess,sys,time
from ctypes import wintypes
from pathlib import Path
BASE=Path(__file__).resolve().parent
PRIOR=757.515625

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)

def child_cpu(process):
    c,e,k,u=(wintypes.FILETIME() for _ in range(4))
    ok=ctypes.windll.kernel32.GetProcessTimes(wintypes.HANDLE(int(process._handle)),ctypes.byref(c),ctypes.byref(e),ctypes.byref(k),ctypes.byref(u))
    if not ok:raise ctypes.WinError()
    return ((k.dwHighDateTime<<32)+k.dwLowDateTime+(u.dwHighDateTime<<32)+u.dwLowDateTime)/10000000

class MemoryCounters(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(name,ctypes.c_size_t) for name in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]

def child_memory(process):
    obj=MemoryCounters();obj.cb=ctypes.sizeof(obj)
    ok=ctypes.windll.psapi.GetProcessMemoryInfo(wintypes.HANDLE(int(process._handle)),ctypes.byref(obj),obj.cb)
    if not ok:raise ctypes.WinError()
    return obj.PeakWorkingSetSize

def main():
    assert (BASE/'entry_baseline.json').exists()
    cap=min(120.0,7200-PRIOR-time.process_time()-5)
    assert cap>0
    peak=0;terminated=None
    with (BASE/'log_symbolic_audit.txt').open('x',encoding='utf-8') as stream:
        p=subprocess.Popen([sys.executable,'-B',str(BASE/'audit.py'),str(cap)],stdout=stream,stderr=subprocess.STDOUT)
        start=time.monotonic()
        try:
            while p.poll() is None:
                used=child_cpu(p);peak=max(peak,child_memory(p))
                if used>=cap or peak>32*1024**3 or time.monotonic()-start>=12*3600:
                    terminated='CPU_OR_MEMORY_OR_INHERITED_WALL_CAP';p.kill();break
                time.sleep(0.02)
            p.wait()
            used=child_cpu(p)
        finally:
            if p.poll() is None:p.kill();p.wait()
    ex=json.loads((BASE/'symbolic_audit_exit.json').read_text()) if (BASE/'symbolic_audit_exit.json').exists() else {}
    a=json.loads((BASE/'symbolic_audit.json').read_text()) if (BASE/'symbolic_audit.json').exists() else {}
    passed=p.returncode==0 and terminated is None and ex.get('error') is None and a.get('status')=='UNIVERSAL_RR_RELEASE_AUGMENTATION_SYMBOLIC_AUDIT_PASS' and used<cap
    r={'status':'PASS' if passed else 'FAILED_OR_UNKNOWN_STOP','prior_uniform_CPU_charge':PRIOR,
       'child_CPU':max(used,ex.get('whole_process_CPU_seconds',0)),'allocated_CPU_cap':cap,
       'peak_working_set_bytes_observed':peak,'RAM_cap_bytes':32*1024**3,
       'returncode':p.returncode,'termination':terminated,'error':ex.get('error'),
       'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
       'completed_checks_replayed':0,'M3_status':'OPEN'}
    write('run_result.json',r);print(json.dumps(r,indent=2),flush=True)
    assert passed

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('controller_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
