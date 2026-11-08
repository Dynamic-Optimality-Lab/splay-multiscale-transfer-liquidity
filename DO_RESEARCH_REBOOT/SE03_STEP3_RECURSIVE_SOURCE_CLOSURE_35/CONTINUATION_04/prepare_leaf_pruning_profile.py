"""Formal source projections and unchanged six-key debt coefficients."""
import functools,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
C14=P/'SE03_STEP2_UNARY_A_LIFT_14'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(t):return (t[0],freeze(t[1]),freeze(t[2])) if isinstance(t,list) else t
def bare(t):return None if t is None or isinstance(t,str) else (t[0],bare(t[1]),bare(t[2]))
def main():
    a=json.loads((F/'branch_H1_r7.json').read_text());bb=json.loads((F/'active_a10_model.json').read_text())
    old=json.loads((C14/'branch_core11_mask0.json').read_text());oldA=json.loads((C14/'branch_grammar2.json').read_text())
    aa=[freeze(t) for t in a['A_branch_trees']]
    oldtrees=oldA['states']
    assert oldtrees is not None
    at=[freeze(t) for t in oldtrees];ai={t:i for i,t in enumerate(at)};assert len(ai)==974
    roots=[t[0]//1000-1 for t in at];classes=[[i for i,g in enumerate(roots) if g==j] for j in range(6)]
    local={x:k for cl in classes for k,x in enumerate(cl)}
    # D6 ordering independently recoverable from the immutable C14 checker.
    b6=[bare(t) for t in old['BF_trees']];bi={t:i for i,t in enumerate(b6)}
    sizes=[len(classes[(t[0]-1)//2]) for t in b6];offset=np.cumsum([0]+sizes[:-1]).tolist()
    assert sum(sizes)==len(old['debt'])
    aproj=[]
    for e in range(7):
        ms=[1000*(j+1) for j in range(7) if j!=e];mapping={v:1000*(i+1) for i,v in enumerate(ms)}
        def reduce(t):
            if t is None:return None
            v,l,r=t[0],reduce(t[1]),reduce(t[2])
            if v in mapping:return (mapping[v],l,r)
            if l is None:return r
            if r is None:return l
            return (1000*sum(x<v for x in ms)+500,l,r)
        aproj.append([ai[reduce(t)] if a['A_roots'][j]!=e else -1 for j,t in enumerate(aa)])
    btrees=[bare(t) for t in json.loads((F/'maximal_B_grammar.json').read_text())['trees']];leaves=[];proj=[]
    for t in btrees:
        ls=[]
        def visit(u,p=None):
            if u is None:return
            if u[0]%2 and u[1] is None and u[2] is None and p is not None:ls.append((u[0],p[0]))
            visit(u[1],u);visit(u[2],u)
        visit(t);ls.sort();res=[]
        for e,p in ls:
            assert p%2==0
            def prune(u):
                if u is None:return None
                if u[0]==p:
                    c=u[1] if u[2] is not None and u[2][0]==e else u[2]
                    assert (u[1] is not None and u[1][0]==e) or (u[2] is not None and u[2][0]==e)
                    return c
                return (u[0],prune(u[1]),prune(u[2]))
            kept=[v for v in range(1,14) if v not in (e,p)];rank={v:i+1 for i,v in enumerate(kept)}
            def ren(u):return None if u is None else (rank[u[0]],ren(u[1]),ren(u[2]))
            pr=ren(prune(t));res.append(bi[pr])
        assert ls;leaves.append([(e-1)//2 for e,p in ls]);proj.append(res)
    z={'A_projection':np.array(aproj,dtype=np.int16),'A6_local':np.array([local[i] for i in range(974)],dtype=np.int16),
       'old_debt':np.array(old['debt'],dtype=np.int8),'old_offsets':np.array(offset,dtype=np.int32),
       'B_leaves':leaves,'B_projection':proj,'A_roots':a['A_roots'],'B_roots':bb['B_roots'],'B_edges':bb['B_edges'],
       'H1_rows':a['H1_rows'],'H2_rows':json.loads((F/'branch_H2_r7.json').read_text())['H2_rows'],
       'input_sha256':{str(p):sha(p) for p in [C14/'branch_core11_mask0.json',C14/'branch_grammar2.json',
         F/'branch_H1_r7.json',F/'branch_H2_r7.json',F/'active_a10_model.json',F/'LEAF_PRUNING_RECURSION_BOX.md',
         P/'SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md']}}
    with (F/'leaf_profile_inputs.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={'status':'COMPLETE_ANALYTICAL_PROJECTIONS','A7_count':len(aa),'A6_count':len(at),'B7_count':len(btrees),
      'B6_necessary_count':len(b6),'D6_max':max(old['debt']),'source_queries':0,'source_engine_calls':0,
      'projections_are_actual_erased_B':False,'JR35':'OPEN','input_sha256':z['input_sha256']}
    with (F/'leaf_profile_inputs.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof222_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
