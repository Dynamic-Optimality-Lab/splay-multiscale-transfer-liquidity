"""Complete independent native10 primitive audit; reuse accepted LOW rows,
lift other HIGH rows with largest off-path leaf, replay only512 NEW cases."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    z=json.loads((B/'native10_source_actions.json').read_text());low=json.loads((B/'ten_anchor_LOW_source_schemas.json').read_text());old=json.loads((B/'nine_label_native_action_cache.json').read_text());assert json.loads((B/'ten_anchor_schema_independent_audit.json').read_text())['status']=='PASS_COMPLETE_TEN_ANCHOR_LOW_SCHEMA_LIFT'
    assert hashlib.sha256((B/'ten_anchor_LOW_source_schemas.json').read_bytes()).hexdigest()==z['reused_LOW_sha256'] and hashlib.sha256((B/'nine_label_native_action_cache.json').read_bytes()).hexdigest()==z['native9_source_sha256']
    T=list(map(fr,z['trees']));OT=list(map(fr,old['trees']));idx={t:i for i,t in enumerate(T)};oi={t:i for i,t in enumerate(OT)};assert T==list(map(fr,low['trees'])) and len(T)==16796
    sp=importlib.util.spec_from_file_location('distinct_native10_new_cases33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_SOURCE_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def go(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,go(v.left,lo,v.key-1),go(v.right,v.key+1,hi))
        return go(tree.root,1,10)
    fresh={(s,x):(t,q) for s,x,t,q in z['fresh_source_rows']};lifts=0
    for i,t in enumerate(T):
        depth={};leaves=[]
        def walk(v,d):
            if isinstance(v,str):return
            k,l,r=v;depth[k]=d
            if isinstance(l,str) and isinstance(r,str):leaves.append(k)
            walk(l,d+1);walk(r,d+1)
        walk(t,0)
        for x in range(1,11):
            h=(depth[x]+1)//2;q=depth[x]//2;assert z['H'][i][x-1]==h and z['Q'][i][x-1]==q
            if h<=2:assert z['destination'][i][x-1]==low['LOW_destination'][i][x-1];continue
            choices=[v for v in leaves if v!=x]
            if not choices:
                assert (i,x) in fresh;tree=I.Tree(t);path,ev=tree.access(x);dst=idx[shape(tree)];assert (dst,sum(e['kind']=='DOUBLE' for e in ev))==fresh[i,x] and dst==z['destination'][i][x-1];continue
            leaf=max(choices);keep=[v for v in range(1,11) if v!=leaf];rank={v:j+1 for j,v in enumerate(keep)}
            def smaller(v,upper=9):
                if isinstance(v,str) or v[0]==leaf:return 'F'+str(upper)
                k,l,r=v;k=rank[k];return k,smaller(l,k-1),smaller(r,upper)
            s=oi[smaller(t)];rx=rank[x];assert old['Q'][s][rx-1]==q and old['H'][s][rx-1]==h
            payload={}
            for gap in range(10):
                a=keep[gap-1] if gap else 0;b=keep[gap] if gap<9 else 11;payload['F'+str(gap)]=(leaf,'F'+str(leaf-1),'F'+str(leaf)) if a<leaf<b else 'F'+str(a)
            def bigger(v):return payload[v] if isinstance(v,str) else (keep[v[0]-1],bigger(v[1]),bigger(v[2]))
            assert idx[bigger(OT[old['destination'][s][rx-1]])]==z['destination'][i][x-1];lifts+=1
    assert queries==len(fresh)==512 and lifts==43168
    result={'status':'PASS_COMPLETE_NATIVE10_SOURCE_ACTIONS','shapes':16796,'all_primitive_actions':167960,'accepted_LOW_rows_reused':107484,'accepted_identities_reused':16796,'HIGH_free_gap_instances':lifts,'NEW_Hamiltonian_cases_replayed':512,'new_source_queries':queries,'external_or_formal_verification':False,'input_sha256':hashlib.sha256((B/'native10_source_actions.json').read_bytes()).hexdigest(),'principal_U33':'OPEN'}
    out('native10_source_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify15_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
