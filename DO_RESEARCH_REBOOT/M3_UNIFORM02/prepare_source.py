"""Versioned one-root adapter; preserve old failed attempt without replay."""
from pathlib import Path
BASE=Path(__file__).resolve().parent
old=(BASE.parent/'M3_UNIFORM01/original_lift.py').read_text()
text=old.replace('INDEPENDENT_DIRECT_COUNTEREXAMPLE_AUDIT_PASS','INDEPENDENT_PROMOTION_ENDPOINT_AUDIT_PASS').replace('D1','D_run').replace('J1','J_run').replace('one_step','sign_run')
needle="    source=Path(read(OUT/'construction.json')['source_folder']);"
text=text.replace(needle,"    old_failure=read(BASE.parent/'M3_UNIFORM01/case_000/obstruction.json')\n    assert (r['source_B'],r['source_A'],r['destination_B'],r['destination_A'])!=(old_failure['source_B'],old_failure['source_A'],old_failure['destination_B'],old_failure['destination_A']),'Old failed source completion must not be retried'\n"+needle)
needle="    marks={x};marks.update(k for k in range(9) if len(marks)<5);mu=sum(1<<k for k in marks)"
text=text.replace(needle,"    marks={x};marks.update(k for k in range(9) if len(marks)<5);mu=341 if (341>>x)&1 else sum(1<<k for k in marks)")
needle="    assert dag.ev_ground(L['root'],env),'First expansion is not an accepted ORIGINAL root'"
text=text.replace(needle,"    root=bool(dag.ev_ground(L['root'],env))\n    write(OUT/'original_attempt.json',{'root':root,'environment':env,'source':raw['source'],'destination':raw['destination'],'mu':mu,'sigma':sig,'stored_row':r['option'],'new_original_root_evaluations':1})\n    if not root:\n        write(OUT/'original_control.json',{'status':'FIRST_NEW_COMPLETION_ROOT_FALSE_UNLIFTED','original_root':False,'new_original_root_evaluations':1,'old_rejected_completion_repeated':False,'original_counterexample_to_J_run':False,'original_negative_cycle_certified':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP});return")
assert text!=old and text.count('root=bool(dag.ev_ground')==1
compile(text,str(BASE/'original_lift.py'),'exec')
with (BASE/'original_lift.py').open('x',encoding='utf-8') as f:f.write(text)
print('Prepared one new-row source adapter; old phase unchanged.')
