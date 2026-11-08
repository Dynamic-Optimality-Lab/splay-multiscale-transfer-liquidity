"""Bounded, append-only controller for each new proof phase."""
import ctypes,json,subprocess,sys,time
from ctypes import wintypes
from pathlib import Path
BASE=Path(__file__).resolve().parent
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def cpu(p):
    c,e,k,u=(wintypes.FILETIME() for _ in range(4))
    assert ctypes.windll.kernel32.GetProcessTimes(wintypes.HANDLE(int(p._handle)),ctypes.byref(c),ctypes.byref(e),ctypes.byref(k),ctypes.byref(u))
    return ((k.dwHighDateTime<<32)+k.dwLowDateTime+(u.dwHighDateTime<<32)+u.dwLowDateTime)/1e7
class Memory(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
def memory(p):
    o=Memory();o.cb=ctypes.sizeof(o)
    assert ctypes.windll.psapi.GetProcessMemoryInfo(wintypes.HANDLE(int(p._handle)),ctypes.byref(o),o.cb)
    return o.PeakWorkingSetSize
def main():
    phase=sys.argv[1];prior=2329.34375
    for q in BASE.glob('run_*_result.json'):
        d=json.loads(q.read_text());prior+=d['child_CPU']
        prior+=json.loads((BASE/('controller_'+d['phase']+'_exit.json')).read_text())['whole_process_CPU_seconds']
    phase_cap=float(sys.argv[2]) if len(sys.argv)>2 else 300
    cap=min(phase_cap,7200-prior-time.process_time()-5);assert cap>0
    used=peak=0;reason=None
    with (BASE/('log_'+phase+'.txt')).open('x',encoding='utf-8') as f:
        p=subprocess.Popen([sys.executable,'-B',str(BASE/('audit_'+phase+'.py')),str(cap)],stdout=f,stderr=subprocess.STDOUT)
        started=time.monotonic()
        try:
            while p.poll() is None:
                used=cpu(p);peak=max(peak,memory(p))
                if used>=cap or peak>32*1024**3 or time.monotonic()-started>=12*3600:
                    reason='CAP';p.kill();break
                time.sleep(.02)
            p.wait();used=cpu(p)
        finally:
            if p.poll() is None:p.kill();p.wait();used=cpu(p)
    exit_path=BASE/('audit_'+phase+'_exit.json')
    ex=json.loads(exit_path.read_text()) if exit_path.exists() else {}
    result={'phase':phase,'status':'PASS' if p.returncode==0 and reason is None and not ex.get('error') and used<cap else 'FAILED_OR_UNKNOWN',
      'prior_uniform_CPU_charge':prior,'child_CPU':max(used,ex.get('whole_process_CPU_seconds',0)),
      'allocated_CPU_cap':cap,'returncode':p.returncode,'termination':reason,'error':ex.get('error'),
      'peak_working_set_bytes_observed':peak,'new_finite_tests':0,'completed_checks_replayed':0}
    write('run_'+phase+'_result.json',result);print(json.dumps(result,indent=2),flush=True)
    assert result['status']=='PASS'
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('controller_'+sys.argv[1]+'_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
