"""Source-period transport of a paired-closed witness to a warm chart seam."""
import json,time,copy,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    old=json.loads((B/'geodesic_source_countercertificate.json').read_text());assert old['u']==0 and old['L']==1 and old['rows'][0]['before']==old['rows'][-1]['after'];z=copy.deepcopy(old);n=len(z['word']);z['u']=1;z['reaching_prefix']=z['word'];z['period']=[v+n for v in z['period']];z['natural_window']=[v+n for v in z['natural_window']]
    for r in z['rows']:r['occurrence']+=n
    z['source_queries']=0;z['inherited_source_engine_calls']=old['source_queries'];z['transport']='repeat the exact original triple-closed word once before the certified period; actual occurrence bijection t->t+length(W), no new or borrowed donor';z['source_sha256']=hashlib.sha256((B/'geodesic_source_countercertificate.json').read_bytes()).hexdigest();out('geodesic_source_chart_aligned.json',z);print(json.dumps({'status':'CHART_SEAM_WARMED_BY_ORIGINAL_SOURCE_PERIOD','period':z['period'],'prefix_length':n,'source_queries':0,'pending_independent_replay':True}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof30_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
