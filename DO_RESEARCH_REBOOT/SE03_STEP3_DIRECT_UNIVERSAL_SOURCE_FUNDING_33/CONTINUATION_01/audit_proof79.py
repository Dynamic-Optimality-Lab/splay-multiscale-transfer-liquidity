"""A sharp anonymous-unary-ancestor test of the surviving k=3 factorization.
Full B has ten genuine marks and one rigid private key11 in gap10. New A
sources put that SAME private key as a unary ancestor on the actual H1 path.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    native=json.loads((B/'native10_source_actions.json').read_text());T=native['trees'];D=np.array(native['destination']);Q=np.array(native['Q']);roots=np.array([t[0] for t in T]);old=np.load(B/'root_clipped3_deficit_profile_graph.npz');protos=[];records=[];sources=[];targets=[];prices=[];powers=6**np.arange(10,dtype=np.int64)
    def fill(lo,hi,kind):
        if lo>hi:return 'F'+str(hi)
        v=lo if kind==0 else hi if kind==1 else (lo+hi)//2;return (v,fill(lo,v-1,kind),fill(v+1,hi,kind))
    def marked_cost(t):
        depth={}
        def visit(t,d):
            if isinstance(t,str):return
            k,l,r=t;depth[k]=d;visit(l,d+1);visit(r,d+1)
        visit(t,0);assert set(depth)==set(range(1,12));return np.array([(depth[i]+1)//2 for i in range(1,11)],dtype=np.int16)
    for g in range(1,10):
        bb=np.flatnonzero(roots==g)
        for x in range(g+1,11):
            for style in range(3):
                A=fill(1,g-1,style);BB=fill(g+1,x-1,style);C=fill(x+1,10,style);before=(g,A,(11,(x,BB,C),'F11'));after=(x,(g,A,BB),(11,C,'F11'));hs=marked_cost(before);ht=marked_cost(after);assert hs[x-1]==1 and ht[x-1]==0;pid=len(protos);protos.append({'root':g,'target':x,'style':style,'A_before':before,'A_after':after,'actual_A_path':'RL','actual_A_events':1,'actual_private_key':11,'private_is_unary_ancestor_at_source':True});b2=D[bb,x-1];ps=np.maximum(Q[bb]-2*hs,-3);pt=np.maximum(Q[b2]-2*ht,-3);sources.append(((ps+3)@powers)*10+g-1);targets.append(((pt+3)@powers)*10+x-1);prices.append(2-Q[bb,x-1]);records.extend((pid,int(b)) for b in bb)
    snew=np.concatenate(sources);tnew=np.concatenate(targets);wnew=np.concatenate(prices);sold=old['keys'][old['src'],0];told=old['keys'][old['dst'],0];s=np.concatenate((sold,snew));t=np.concatenate((told,tnew));w=np.concatenate((old['w'],wnew));handles=np.concatenate((old['source_records'][:,0],-np.arange(1,len(records)+1,dtype=np.int64)));E=len(w);sort=np.lexsort((np.arange(E),w,t,s));ss=s[sort];tt=t[sort];first=np.ones(E,dtype=np.bool_);first[1:]=(ss[1:]!=ss[:-1])|(tt[1:]!=tt[:-1]);chosen=sort[first];keys=np.unique(np.concatenate((s[chosen],t[chosen])));src=np.searchsorted(keys,s[chosen]);dst=np.searchsorted(keys,t[chosen]);N=len(keys);EE=len(chosen);assert N<2000000 and EE<5000000 and N+EE<4000000;order=np.argsort(src,kind='stable');offset=np.concatenate(([0],np.cumsum(np.bincount(src,minlength=N))));np.savez_compressed(B/'unary_ancestor_gap10_graph.npz',keys=keys[:,None],src=src,dst=dst,w=w[chosen],order=order,offset=offset,source_records=handles[chosen,None]);np.savez_compressed(B/'unary_ancestor_gap10_records.npz',records=np.array(records,dtype=np.int32));out('unary_ancestor_gap10_prototypes.json',protos)
    with (B/'unary_ancestor_gap10_work_00.pkl').open('xb') as f:pickle.dump({'level':np.zeros(N,dtype=np.int64),'parent':np.full(N,-1,dtype=np.int32),'queue':list(range(N)),'pending':np.ones(N,dtype=np.bool_),'head':0,'checks':0,'updates':0},f)
    result={'status':'UNARY_ANONYMOUS_ANCESTOR_SOURCE_EXTENSION_BUILT','physical_keys':11,'genuine_KEEP_keys':list(range(1,11)),'private_key':11,'B_private_key_placement':'rigid mark-free gap10 leaf in the FULL physical B tree','new_A_placement':'same private11 is unary right child of marked root g, actual accessed marked x is its left child; actual path RL, one genuine bottom-up double','local_H':1,'all_original_operations_and_keys_retained':True,'old_source_edges_lifted':'same private11 in an A/B rigid gap; all marked costs and profile inputs unchanged by source-term substitution','new_source_packets':len(records),'new_A_prototypes':len(protos),'nodes':N,'edges':EE,'source_handle':'nonnegative=old original source edge, negative=-(new row+1)','new_source_queries':0,'source_realization':'closed ten-mark B cycle with rigid private gap, and uniform arbitrary-A realization corollary; explicit new words required for any promoted counterexample','principal_U33':'OPEN'};out('unary_ancestor_gap10_source_spec.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof79_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
