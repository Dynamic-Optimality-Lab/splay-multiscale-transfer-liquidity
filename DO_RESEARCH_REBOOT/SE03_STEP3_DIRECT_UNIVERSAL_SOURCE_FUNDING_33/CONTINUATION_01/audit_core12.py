"""New source comparison executions only. Original A/B10/B9 replay reused.
Build actual normalized owner chain from accepted canonical I6 through10.
"""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
from native10_source_allocator import Allocator
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def main():
    global queries
    old=json.loads((B/'native10_width2_source_countercertificate.json').read_text());assert old['u']==old['L']==1;T=fr(old['initial_diagonal']);word=old['word'];period=old['rows'];n=len(word);sp=importlib.util.spec_from_file_location('new_comparison6_8_native10_33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('SOURCE_CAP')
        queries+=1;return p0(t,x)
    S.path=path;hist={}
    for r in (6,7,8):
        tree=T;before_period=None;rec=[]
        for copy in range(2):
            if copy==1:before_period=tree
            for local,(mode,x) in enumerate(word,1):
                t=copy*n+local;before=tree;pa='';ev=[]
                if mode=='K' and x<=r:tree,pa,ev=S.trace(tree,x)
                if copy==1:rec.append({'occurrence':t,'before':before,'after':tree,'path':pa,'events':ev,'q':len(pa)//2})
        assert tree==before_period;hist[r]=rec
    staged={}
    for r in range(6,11):
        rows=[]
        for i,oldrow in enumerate(period):
            A,F,E=map(fr,oldrow['before']);At,Ft,Et=map(fr,oldrow['after'])
            if r<=8:b=hist[r][i]['before'];bt=hist[r][i]['after'];pa=hist[r][i]['path'];ev=hist[r][i]['events'];q=hist[r][i]['q']
            else:b,bt,pa,ev,q=(F,Ft,oldrow['BF_path'],oldrow['BF_events'],oldrow['qF']) if r==10 else (E,Et,oldrow['BE_path'],oldrow['BE_events'],oldrow['qE'])
            mode='K' if oldrow['mode']=='K' and oldrow['target']<=r else 'D';rows.append(dict(oldrow,mode=mode,original_mode=oldrow['mode'],genuine_F=mode=='K' and b[0]!=oldrow['target'],before=(A,b,b),after=(At,bt,bt),BF_path=pa,BF_events=ev,qF=q,qE=q))
        assert rows[0]['before']==rows[-1]['after'] and {v['target'] for v in rows if v['genuine_F']}==set(range(1,r+1));staged[r]=rows
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'));import cd6_allocator as C
    from source_funding import own_map,with_owners
    base=C.allocate(staged[6]);assert base['core']==6 and base['f']==base['h0'];prev=base['f'];previousD=base['D'];engine=Allocator();stages=[]
    for r in range(7,11):
        v=own_map(staged[r]);raw=engine.build(staged[r],v['macros'],v['h0']);v['h']=raw['h'];owner=with_owners(v,previousD,prev);final=owner['extension']['allocation'];a=owner['prior']['allocation'];assert all(final[d]==u for d,u in a.items()) and all(final[d]==prev[d] for d in owner['common'])
        stages.append({'support':r,'rows':staged[r],'demands':sorted(v['D']),'h0':pack(v['h0']),'raw_h':pack(raw['h']),'input_fE':pack(prev),'common':sorted(owner['common']),'E_only_retired':sorted(previousD-v['D']),'old_effective_a':pack(a),'full_f':pack(final),'new_additions':pack(owner['extension']['additions']),'raw_source_receipt':raw['receipt'],'max_debt':raw['max_debt'],'working_peak':raw['working_peak'],'cut_before_macro':raw['cut_before_macro'],'all_old_successes_unchanged':True,'licensed_paths':owner['licensed']['paths']});prev=final;previousD=v['D']
    result={'status':'COMPLETE_ACTUAL_NORMALIZED_SOURCE_CHAIN_6_TO_10','initial_diagonal':T,'word':word,'prefix':old['reaching_prefix'],'period':old['period'],'source_A_events':old['A'],'source_A_units':2*old['A'],'six_key_rows':staged[6],'canonical_f6':pack(base['f']),'base_core':6,'no_five_key_core9_domain':'all nested retained ancestor cores are inside keys1..6','stages':stages,'full_support':10,'full_demands':len(prev),'original_source_rows_reused':'native10_width2_source_countercertificate.json, A/B10/B9; new B6/B7/B8 executions only','old_source_audit_sha256':hashlib.sha256((B/'native10_width3_lower_independent_audit.json').read_bytes()).hexdigest(),'native10_credit_sha256':hashlib.sha256((B/'native10_credit_certificate.json').read_bytes()).hexdigest(),'new_source_queries':queries,'principal_U33':'OPEN'}
    out('native10_normalized_owner_chain.json',result);print(json.dumps({'status':result['status'],'base_core':6,'source_queries':queries,'stages':[{'r':s['support'],'D':len(s['demands']),'old_a':len(s['old_effective_a']),'new':len(s['new_additions']),'working':s['working_peak']} for s in stages]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core12_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
