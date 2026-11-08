"""One A-only root query isolating the saved FIX geometry at9 activation.
Original paired B/source facts are unchanged; no new return path is asserted.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=int(sys.argv[2])
sp=importlib.util.spec_from_file_location('FR31_fix_control_source',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
def path(t,x):
    if C.queries>=CAP:raise TimeoutError('remaining query cap')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    old=json.loads((P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json').read_text());z=next(v for v in old['rows'] if v['occurrence']==120)
    t,pa,ev=C.tr(fr(z['after'][0]),9);assert pa=='LRRL' and len(ev)==2
    out('FIX_9_activation_control.json',{'status':'SAVED_FIX_A_GEOMETRY_CONTROL','before_A':z['after'][0],'target':9,'A_path':pa,'A_events':ev,'after_A':t,
        'A_cost':2,'matching_counter_PREFIX_cost':1,'B_geometry_same_as_PREFIX_activation':True,'full_B_Q':3,'sigma_E_if_this_immediate_activation':2,
        'scope':'the saved FIX state immediately after first upper11, ONE proposed activation; not all FIX continuations','source_queries':1})
    print(json.dumps({'status':'FIX_ACTIVATION_GEOMETRY','A_path':pa,'A_cost':2,'PREFIX_cost':1}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
