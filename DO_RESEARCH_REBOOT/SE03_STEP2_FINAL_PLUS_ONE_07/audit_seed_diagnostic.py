"""Diagnose representation differences; never convert a failed audit to PASS."""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('campaign07_checker',B/'audit_independent.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
a=d.a
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    p=json.loads((B/'terminal_seeds.json').read_text());report=[]
    for ci,c in enumerate(p['terminal_cases']):
        word=(c['oldroot'],c['plus_target'],c['cold_q4']);fs,sz=a.frames(word,range(1,12),0,12)
        E={d.canonical(t) for t,z in fs}
        P={d.canonical(a.Aread(v['A'])) for v in p['groups'] if ci in v['cases']}
        if len(E)!=len(P):
            missing=[t for t in E if not any(d.includes(u,t) for u in P)]
            extra=[t for t in P if not any(d.includes(u,t) for u in E)]
            report.append({'case':ci,'word':word,'producer_terms':len(P),'forward_terms':len(E),
                'forward_terms_uncovered_by_producer':len(missing),'producer_terms_uncovered_by_forward':len(extra),
                'first_missing':a.Aw(missing[0]) if missing else None,'first_extra':a.Aw(extra[0]) if extra else None})
            if len(report)>=8:break
    out('seed_diagnostic.json',{'status':'DIAGNOSTIC_ONLY','differences':report,'source_engine_calls':a.calls,'new_finite_tests':0})
    print(json.dumps(report),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seed_diagnostic_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':a.calls,'new_finite_tests':0})
