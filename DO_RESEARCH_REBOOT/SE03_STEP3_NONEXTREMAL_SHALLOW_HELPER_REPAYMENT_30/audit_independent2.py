"""Distinct check of the new first-return source-exclusion control only.
Completed85-operation source audit is reused, not rerun.
"""
import importlib.util,json,sys,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2]);START=time.process_time();CAP=float(sys.argv[1])
sp=importlib.util.spec_from_file_location('C30_exclusion_mutable',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
def tick():
    if I.queries>=QCAP or time.process_time()-START>=CAP-1:raise TimeoutError('inherited cap')
    I.queries+=1
I.tick=tick
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    r=json.loads((B/'nonextremal_source_countercertificate.json').read_text());p=json.loads((B/'first_root_return_source_exclusion.json').read_text());s=I.fr(next(z for z in r['rows'] if z['occurrence']==119)['after'])
    rows,end=I.execute(s,[('K',7)],120,[p['candidate_transition']]);before=I.core(s[1],I.M);after=I.core(end[1],I.M)
    assert after<before and sorted(before-after)==p['lost_labels']
    # Six additional original search-path queries, charged conservatively.
    ans=[]
    for x in sorted(I.M-{5}):
        tick();tree=I.Tree(s[1]);n=tree.nodes[x];rev=[]
        while n.parent:rev.append('L' if n.parent.left is n else 'R');n=n.parent
        path=''.join(reversed(rev));ss=len(path)%2==0 and all(path[i:i+2] in ('LL','RR') for i in range(0,len(path),2));ans.append({'target':x,'path':path,'SS_necessary_condition':ss})
    assert ans==p['all_other_marked_paths'] and [z['target'] for z in ans if z['SS_necessary_condition']]==[1,3,11,13]
    assert I.queries==9
    out('independent_source_exclusion_audit.json',{'status':'PASS_DISTINCT_NEW_SOURCE_EXCLUSION','source_queries':I.queries,
        'method':'new mutable actual transition plus conservatively charged path queries; old complete source receipt reused',
        'lost_core_labels':sorted(before-after),'B_path':rows[0]['BF_path'],'full_core_after':len(after),
        'consequence':'the immediate KEEP7 falsifier cannot be in a closed full-core13 source; first-return repayment remains OPEN',
        'trust':'same research agent, distinct implementation; not external peer review or formal proof assistant',
        'input_hashes':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('nonextremal_source_countercertificate.json','first_root_return_source_exclusion.json')}})
    print(json.dumps({'status':'EXCLUSION_INDEPENDENT_PASS','source_queries':I.queries,'core_loss':sorted(before-after)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
