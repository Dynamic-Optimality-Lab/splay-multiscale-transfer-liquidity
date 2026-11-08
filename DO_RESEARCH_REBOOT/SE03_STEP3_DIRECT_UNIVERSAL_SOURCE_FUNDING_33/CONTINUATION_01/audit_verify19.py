"""Independent actual source/owner composition from accepted I6 through10.
Only the new B6/B7/B8 executions are replayed; accepted A/B10/B9 reused.
"""
import json,pickle,time,sys,hashlib,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def rd(p):return json.loads(p.read_text())
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def mp(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    z=rd(B/'native10_normalized_owner_chain.json');old=rd(B/'native10_width2_source_countercertificate.json');old_audit=rd(B/'native10_width3_lower_independent_audit.json');assert hashlib.sha256((B/'native10_width2_source_countercertificate.json').read_bytes()).hexdigest()==old_audit['input_sha256']['native10_width2_source_countercertificate.json']
    cert=rd(B/'native10_credit_certificate.json');audit=rd(B/'native10_complete_independent_audit.json');assert audit['status']=='PASS_COMPLETE_NATIVE10_SOURCE_CREDIT_CERTIFICATE' and cert['checked_input_pickle_sha256']==audit['input_sha256']
    with (B/'native10_debt_03.pkl').open('rb') as f:pinned=pickle.load(f)
    levels=dict(cert['nonzero_debt']);assert levels==pinned['level'] and not pinned['queue'];del pinned
    src=rd(B/'native10_source_actions.json');idx={fr(t):i for i,t in enumerate(src['trees'])};N=len(idx);mirror=src['mirror']
    def debt(st):
        a,b=(idx[fr(t)] for t in st[:2]);return levels.get(min(a*N+b,mirror[a]*N+mirror[b]),0)
    sp=importlib.util.spec_from_file_location('independent_new_nested_streams33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_COMPOSITION_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def dump(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,dump(v.left,lo,v.key-1),dump(v.right,v.key+1,hi))
        return dump(tree.root,1,10)
    allrows={6:z['six_key_rows']};allrows.update({s['support']:s['rows'] for s in z['stages']});T=fr(z['initial_diagonal']);word=z['word'];period=z['period'];actual={}
    for r in (6,7,8):
        tree=I.Tree(T);rec={};before_period=None
        for t,(mode,x) in enumerate(z['prefix']+word,1):
            if t==period[0]:before_period=shape(tree)
            before=shape(tree);path='';ev=[]
            if mode=='K' and x<=r:path,ev=tree.access(x)
            if period[0]<=t<=period[1]:rec[t]=(before,shape(tree),path,len(path)//2)
        assert shape(tree)==before_period;actual[r]=rec
    for r,rows in allrows.items():
        assert fr(rows[0]['before'])==fr(rows[-1]['after'])
        for i,row in enumerate(rows):
            original=old['rows'][i];assert row['occurrence']==original['occurrence'] and row['a']==original['a'] and fr(row['before'][0])==fr(original['before'][0]) and fr(row['after'][0])==fr(original['after'][0])
            mode='K' if original['mode']=='K' and original['target']<=r else 'D';assert row['mode']==mode and row['original_mode']==original['mode']
            if r<=8:before,after,path,q=actual[r][row['occurrence']]
            else:j=1 if r==10 else 2;before=fr(original['before'][j]);after=fr(original['after'][j]);path=original['BF_path' if r==10 else 'BE_path'];q=original['qF' if r==10 else 'qE']
            assert fr(row['before'][1])==before and fr(row['after'][1])==after and row['qF']==q and row['BF_path']==path
            assert row['genuine_F']==(mode=='K' and before[0]!=row['target'])
        assert {v['target'] for v in rows if v['genuine_F']}==set(range(1,r+1))
    def natural(rows):
        ends=[i for i,r in enumerate(rows) if r['genuine_F']];mm=[]
        for j,end in enumerate(ends):
            p=ends[j-1];seg=rows[p+1:end+1] if p<end else rows[p+1:]+rows[:end+1];D=[(r['occurrence'],k) for r in seg for k in range(1,r['qF']+1)];U=[(r['occurrence'],j,b) for r in seg for j in range(1,r['a']+1) for b in (0,1)];mm.append((seg,D,U))
        return mm
    base={d:u for s,D,U in natural(allrows[6]) for d,u in zip(D,U)};assert base==mp(z['canonical_f6']);prev=base;records=[]
    for stage in z['stages']:
        r=stage['support'];mm=natural(stage['rows']);D={d for s,dd,U in mm for d in dd};U={u for s,dd,uu in mm for u in uu};h0={d:u for s,dd,uu in mm for d,u in zip(dd,uu)};h=mp(stage['raw_h']);a=mp(stage['old_effective_a']);final=mp(stage['full_f'])
        assert h0==mp(stage['h0']) and mp(stage['input_fE'])==prev and len(U)==106
        for mapping,domain in ((h,D),(final,D),(prev,set(prev))):assert set(mapping)==domain and len(set(mapping.values()))==len(mapping) and set(mapping.values())<=U
        assert all(h[d]==u for d,u in h0.items());bank=[];paid={};released=set();selected_all=set();peak=0
        for record in stage['raw_source_receipt']:
            i=record['macro_index'];seg,dd,uu=mm[i];ds=debt(seg[0]['before']);dt=debt(seg[-1]['after']);H=len(uu)//2;c=min(H,3);K=stage['max_debt'];assert (ds,dt,c)==(record['D_source'],record['D_target'],record['c']) and len(bank)==K-ds
            selected=uu[:2*c];fixed={d:h0[d] for d in dd if d in h0};assert set(fixed.values())<=set(selected) and 2*c-len(dd)+dt-ds==record['margin']>=0;peak=max(peak,len(bank)+len(selected));pool=[u for u in selected if u not in fixed.values()]+bank;paid.update(fixed)
            for d in dd:
                if d not in fixed:paid[d]=pool.pop(0)
            keep=K-dt;assert len(pool)>=keep;released.update(pool[keep:]);bank=pool[:keep];assert bank==list(map(tuple,record['carry']));selected_all.update(selected)
        assert not bank and paid==h and peak==stage['working_peak']<=9 and set(h.values())|released==selected_all and not set(h.values())&released
        common=D&prev.keys();locked={d:prev[d] for d in common};inverse={u:d for d,u in locked.items()}
        def exchange(source):
            ans=dict(locked);paths={}
            for root in sorted(source.keys()-locked.keys()):
                d=root;seen=set();path=[]
                while d in source:
                    assert d not in seen;seen.add(d);u=source[d];path.append((d,u))
                    if u not in inverse:ans[root]=u;paths[root]=path;break
                    d=inverse[u]
            return ans,paths
        oldmap,op=exchange(h0);newmap,np=exchange(h);assert oldmap==a and newmap==final and all(np[d]==p for d,p in op.items()) and all(final[d]==u for d,u in a.items()) and all(final[d]==prev[d] for d in common)
        assert set(map(tuple,stage['E_only_retired']))==prev.keys()-D and len(stage['new_additions'])==len(D-a.keys());records.append({'support':r,'demands':len(D),'common':len(common),'retired_E_only':len(prev.keys()-D),'old_effective_owners_preserved':len(a),'new_owners':len(D-a.keys()),'working_peak':peak});prev=final
    result={'status':'PASS_ACTUAL_NORMALIZED_SOURCE_COMPOSITION_6_TO_10','actual_period':period,'A_events':53,'physical_A_units':106,'full_demands':27,'canonical_I6_input':'native core6 own-map, no unprovided five-key/core9 source reservation','stage_records':records,'all_old_success_paths_and_values_preserved':True,'source_closure_all_five_B_executions':True,'source_backbone_bound':10,'new_source_queries':queries,'counterexample_to_CD':False,'uniform_support_transfer_claimed':False,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_normalized_owner_chain.json','native10_credit_certificate.json','NATIVE_TEN_SOURCE_THEOREM.md')}}
    out('native10_normalized_composition_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify19_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
