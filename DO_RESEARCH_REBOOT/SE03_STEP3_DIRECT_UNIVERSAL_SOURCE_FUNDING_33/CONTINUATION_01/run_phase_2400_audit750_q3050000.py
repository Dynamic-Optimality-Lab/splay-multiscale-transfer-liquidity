"""Cumulative capped controller; derived from unchanged C19 controller."""
import ctypes,json,subprocess,sys,time
from ctypes import wintypes
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def cpu(p):
    c,e,k,u=(wintypes.FILETIME() for _ in range(4))
    assert ctypes.windll.kernel32.GetProcessTimes(wintypes.HANDLE(int(p._handle)),ctypes.byref(c),ctypes.byref(e),ctypes.byref(k),ctypes.byref(u))
    return ((k.dwHighDateTime<<32)+k.dwLowDateTime+(u.dwHighDateTime<<32)+u.dwLowDateTime)/1e7
class Memory(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
def memory(p):
    m=Memory();m.cb=ctypes.sizeof(m)
    assert ctypes.windll.psapi.GetProcessMemoryInfo(wintypes.HANDLE(int(p._handle)),ctypes.byref(m),m.cb)
    return m.PeakWorkingSetSize
def main():
    phase,group=sys.argv[1:3];entry=json.loads((B/'entry_authorized2400_audit750_q3050000.json').read_text())
    total=entry['prior_uniform_CPU'];used_group=entry['inherited_group_CPU'][group]
    for ph in B.glob('run_*_result.json'):
        r=json.loads(ph.read_text());c=json.loads((B/('controller_'+r['phase']+'_exit.json')).read_text())
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge
        if r['group']==group:used_group+=charge
    qremaining=entry['remaining_conservative_queries']-sum(json.loads(p.read_text()).get('source_queries',0) for p in B.glob('run_*_result.json'))
    qcap=min(qremaining,entry['phase_query_caps'].get(phase.rstrip('0123456789'),0));assert qcap>=0
    cap=min(entry['group_caps'][group]-used_group-time.process_time()-1,
            7200-total-time.process_time()-6,entry['phase_caps'].get(phase,20))
    assert cap>0
    peak=used=0;reason=None
    with (B/('log_'+phase+'.txt')).open('x',encoding='utf-8') as log:
        p=subprocess.Popen([sys.executable,'-B',str(B/('audit_'+phase+'.py')),str(cap),str(qcap)],stdout=log,stderr=subprocess.STDOUT)
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
    ep=B/('audit_'+phase+'_exit.json');ex=json.loads(ep.read_text()) if ep.exists() else {}
    r={'phase':phase,'group':group,'status':'PASS' if p.returncode==0 and reason is None and not ex.get('error') and used<cap and ex.get('source_queries',0)<=qcap else 'FAILED_OR_UNKNOWN',
       'prior_uniform_CPU_charge':total,'prior_group_CPU_charge':used_group,'allocated_child_cap':cap,'allocated_query_cap':qcap,
       'child_CPU':max(used,ex.get('whole_process_CPU_seconds',0)),
       'peak_working_set_bytes_observed':peak,'returncode':p.returncode,'termination':reason,'error':ex.get('error'),
       'source_engine_calls':ex.get('source_engine_calls',0),'source_queries':ex.get('source_queries',0)}
    out('run_'+phase+'_result.json',r);print(json.dumps(r),flush=True);assert r['status']=='PASS'
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('controller_'+sys.argv[1]+'_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

