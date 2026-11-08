"""Cumulative resumable Bellman closure on exact certified cache products.
No original source access function is imported or evaluated.
"""
import array,collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1]);BATCH=int(sys.argv[3]);PHASE=sys.argv[4]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    model=read(F/'complete_product_model_k0.json')
    g={'B_trees':model['B_trees'],'B_edges':model['B_edges'],'native_to_physical':model['A_keys']}
    native={'destination':model['A_destination'],'H':model['A_H'],'trees':model['A_trees']}
    AD,H=native['destination'],native['H'];N=len(AD)
    if BATCH==1:
        # Work on the larger genuinely seven-key SCC; the16-cycle component
        # has the inherited all-A MR source theorem and is not replayed here.
        comp=list(range(len(g['B_trees'])));Nb=len(comp);bi={b:i for i,b in enumerate(comp)}
        edges=[(e['source'],e['target'],e['key'],e['q'],i) for i,e in enumerate(g['B_edges']) if e['source'] in bi and e['target'] in bi]
        adj=[[] for _ in comp];phys_to_native={v:i for i,v in enumerate(g['native_to_physical'])}
        for bs,bt,key,q,ei in edges:adj[bi[bs]].append((phys_to_native[key],q,bi[bt],ei))
        total=N*Nb;assert total+N+len(g['B_trees'])<2000000
        state={'component':comp,'Nb':Nb,'adj':adj,'level':array.array('i',[0])*total,
          'parent':array.array('i',[-1])*total,'action':array.array('h',[0])*total,
          'inside':bytearray(total),'queue':collections.deque(), 'nonzero':0,'updates':0,
          'edge_examinations':0,'processed':0,'seeded':False,'seed_index':0,'max_level':0,
          'input_sha256':sha(F/'complete_product_model_k0.json'),'negative_cycle':None}
    else:
        with (F/('complete_k0_search_%02d.pkl'%(BATCH-1))).open('rb') as f:state=pickle.load(f)
        assert state['input_sha256']==sha(F/'complete_product_model_k0.json')
    Nb=state['Nb'];adj=state['adj'];levels=state['level'];parent=state['parent'];action=state['action']
    inside=state['inside'];queue=state['queue'];comp=state['component'];last_updated=None
    def relax(t,value,s,act):
        nonlocal last_updated
        if value<=levels[t]:return
        if levels[t]==0:state['nonzero']+=1
        levels[t]=value;parent[t]=s;action[t]=act;state['updates']+=1;last_updated=t
        state['max_level']=max(state['max_level'],value)
        if not inside[t]:inside[t]=1;queue.append(t)
    if not state['seeded']:
        for ai in range(state['seed_index'],N):
            ha=H[ai];dest=AD[ai]
            for bs,outs in enumerate(adj):
                for x,q,bt,ei in outs:
                    if 2*ha[x]<q:
                        relax(dest[x]*Nb+bt,q-2*ha[x],ai*Nb+bs,ei+1)
            state['seed_index']=ai+1
            if ai%128==0 and time.process_time()-START>CAP-4:break
        state['seeded']=state['seed_index']==N
    def cycle_check(v):
        trail=[];position={}
        while v>=0 and v not in position and len(trail)<200000:
            position[v]=len(trail);trail.append(v);v=parent[v]
        if v<0 or v not in position:return
        cyc=list(reversed(trail[position[v]:]));steps=[];weight=0
        for t in cyc:
            s=parent[t];a,b=divmod(s,Nb);at,bt=divmod(t,Nb);act=action[t]
            if act<0:
                x=-act-1;w=2*H[a][x];assert AD[a][x]==at and b==bt
                steps.append({'source':s,'target':t,'kind':'DELETE','native_key':x+1,'A_H':H[a][x],'q':0,'weight':w})
            else:
                e=g['B_edges'][act-1];x=g['native_to_physical'].index(e['key']);w=2*H[a][x]-e['q']
                assert AD[a][x]==at and e['source']==comp[b] and e['target']==comp[bt]
                steps.append({'source':s,'target':t,'kind':'KEEP','native_key':x+1,'B_edge':act-1,'A_H':H[a][x],'q':e['q'],'weight':w})
            weight+=w
        if weight<0:state['negative_cycle']={'steps':steps,'weight':weight,'source_exact_bridge':'CP35','status':'CANDIDATE_REQUIRES_INDEPENDENT_CYCLE_AND_SUPPORT_AUDIT'}
    while state['seeded'] and queue and state['negative_cycle'] is None and time.process_time()-START<CAP-4:
        code=queue.popleft();inside[code]=0;ai,bs=divmod(code,Nb);d=levels[code];dest=AD[ai];ha=H[ai]
        for x in range(len(H[0])):
            state['edge_examinations']+=1;value=d-2*ha[x]
            if value>0:relax(dest[x]*Nb+bs,value,code,-x-1)
        for x,q,bt,ei in adj[bs]:
            state['edge_examinations']+=1;value=d-2*ha[x]+q
            if value>0:relax(dest[x]*Nb+bt,value,code,ei+1)
        state['processed']+=1
        if state['updates']//50000>state.get('cycle_check_bucket',0):
            state['cycle_check_bucket']=state['updates']//50000
            if last_updated is not None:cycle_check(last_updated)
    # Full invariant examination is the independent verifier's job, not a
    # new native source simulation or a false universal theorem promotion.
    with (F/('complete_k0_search_%02d.pkl'%BATCH)).open('xb') as f:pickle.dump(state,f,pickle.HIGHEST_PROTOCOL)
    status='NEGATIVE_CACHED_SOURCE_CYCLE_CANDIDATE' if state['negative_cycle'] else 'COMPLETE_RESTRICTED_PRODUCT_CREDIT' if state['seeded'] and not queue else 'CACHED_PRODUCT_CHECKPOINT'
    report={'status':status,'batch':BATCH,'mathematical_product_states':N*Nb,'B_vertices':Nb,'native_A_shapes':N,
      'nonzero_levels':state['nonzero'],'maximum_level':state['max_level'],'pending':len(queue),'seeded':state['seeded'],
      'seed_index':state['seed_index'],'processed':state['processed'],'relaxations':state['updates'],
      'cached_product_edge_examinations':state['edge_examinations'],
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN_PENDING_PROOF_OR_COUNTERCERTIFICATE',
      'no_generalized_finite_pass_claim':True}
    if state['negative_cycle'] is not None:out('negative_complete_k0_cycle_candidate.json',state['negative_cycle'])
    out('complete_k0_search_%02d.json'%BATCH,report);print(json.dumps(report),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/('audit_'+PHASE+'_exit.json')).open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
