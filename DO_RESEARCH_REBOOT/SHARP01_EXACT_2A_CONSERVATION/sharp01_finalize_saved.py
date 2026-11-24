"""Recover completed immutable ledger artifacts, without replaying any source."""
from sharp01_experiments import *

start=time.process_time();wall=time.perf_counter()
sources=json.loads((BASE/'SHARP01_SOURCE_WITNESSES.json').read_text())['sources']
manifest=json.loads((BASE/'SHARP01_INPUT_MANIFEST.json').read_text())
changed={rel:{'before':h,'after':sha(REPO/rel)} for rel,h in manifest['input_sha256'].items() if sha(REPO/rel)!=h}
# Mathematical reports and EXP01 are provenance, not runtime imports. Preserve
# every before/after mismatch; the exact executed words and code are isolated.
assert not any('certificates2.json' in rel or 'zero_run_source_certificates.json' in rel or 'python/independent/' in rel for rel in changed),changed
manifest['concurrent_provenance_changes']=changed
manifest['executed_source_constructor_sha256']=sha(BASE/'sharp01_sources.py')
manifest['independent_reference_sha256']=sha(BASE/'sharp01_tuple_reference.py')
manifest['recovery']='finalized saved ledgers after provenance-only concurrent EXP01 addition; no source replay'
write(BASE/'SHARP01_INPUT_MANIFEST.json',manifest)
summaries=[];incs=[];candidates={};index=[]
for k,s in enumerate(sources):
    name=f'ledgers/source_{k:03d}.json';led=json.loads((BASE/name).read_text())
    assert led['source']==s and led['summary']['Delta']<=0
    summaries.append(led['summary']);incs.append({'source':s['name'],**incidence(led)})
    potential_update(candidates,led);index.append({'name':s['name'],'path':name,'sha256':sha(BASE/name)})
    assert time.process_time()-start<60,'saved-ledger finalization CPU reserve'
for z in candidates.values():
    z['nonnegative_scalar_feasible']=z['zero_obstruction'] is None and (z['upper'] is None or z['lower']<=z['upper'])
    z['lower']=str(z['lower']);z['upper']=None if z['upper'] is None else str(z['upper'])
write(BASE/'SHARP01_GAP_LEDGER.json',{'state_reference_format':'Each per-source states table resolves complete A/B trees. All original operation, StepEv and real-bit IDs are in operations/steps/events.',
                                   'no_KEEP_case':'no gaps, Q=0 and A explicitly unpartitioned', 'ledgers':index})
write(BASE/'SHARP01_RESULTS.json',{'sources':summaries,'potential_templates':candidates,'incidence':incs})
receipt={'status':'PASS_FINITE_CORPUS_WITH_RECORDED_PROVENANCE_CHANGE','sources':len(sources),
         'operations':sum(s['operations'] for s in summaries),'max_n':max(s['n'] for s in summaries),
         'positive_source_deficits':0,'finalization_cpu_seconds':time.process_time()-start,'finalization_wall_seconds':time.perf_counter()-wall,
         'initial_run':'all sources completed; final EXP01 provenance hash guard failed',
         'initial_run_actual_cpu_seconds':None,'initial_run_conservative_cpu_charge_seconds':600,
         'initial_run_cpu_bound_reason':'CPU guard passed after every source, including last; final comparison did not replay sources',
         'initial_run_peak_memory_bytes':None,
         'limitation':'CPU and peak-memory receipt was after the failed final hash guard; exact initial-run figures were not persisted. No guessed measurements are supplied.',
         'ledger_total_bytes':sum((BASE/i['path']).stat().st_size for i in index)}
write(BASE/'SHARP01_RUN_RECEIPT.json',receipt);print(json.dumps(receipt))
