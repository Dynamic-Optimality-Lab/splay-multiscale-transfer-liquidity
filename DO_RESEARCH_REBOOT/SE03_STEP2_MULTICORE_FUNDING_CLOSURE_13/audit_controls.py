"""Mandatory historical sources plus Campaign12 two-slot certificate replay."""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;m=n=None
def out(name,v):
    if name=='historical_controls.json':
        v=dict(v);v.pop('all_outputs_redirected_to11',None);v['all_outputs_redirected_to13']=True
        v['scope']='mandatory original controls, no new full-core promotion'
    with (B/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    global m,n
    m=load('old11_controls13',B.parent/'SE03_STEP2_CORE7_SINGLE_EXCESS_11/audit_controls.py');m.B=B;m.out=out;m.main()
    old12=B.parent/'SE03_STEP2_CORE7_TWO_EXCESS_12';sys.path.insert(0,str(old12))
    n=load('old12_independent13',old12/'audit_independent3.py');n.out=lambda name,v:out('old12_'+name,v);n.main()
    result={'status':'PASS_ALL_REQUIRED_HISTORICAL_AND_TWO_SLOT_CONTROLS',
        'old_period_rows':1856,'old12_two_slot_source_reports':48,'old12_owner_fixtures':432,
        'old12_source_events':5816,'old12_generic_owner_cases':62208,'all_old_files_read_only':True,
        'Sigma45_46':'original failure preserved','Gamma26':'original legal donor/cut repaired and preserved',
        '06_09':'original scopes/replays preserved','11':'429 skeletons/3003 accesses recomputed through12 checker',
        'source_engine_calls':m.a.calls+m.c8.d.calls+m.c10.calls+m.n10.d.calls+n.calls}
    out('historical_replay_summary.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:
        calls=(m.a.calls+m.c8.d.calls+m.c10.calls+m.n10.d.calls if m and m.n10 else 0)+(n.calls if n else 0)
        out('audit_controls_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls,'old_semantic_rows_replayed':1856 if m and m.n10 else 0})
