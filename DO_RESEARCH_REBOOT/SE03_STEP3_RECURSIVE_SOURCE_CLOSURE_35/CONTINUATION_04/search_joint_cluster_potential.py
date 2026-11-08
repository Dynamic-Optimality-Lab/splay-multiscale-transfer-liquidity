"""Exact alternative certificates for a uniform joint-geometry formula class."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
import collections,functools,hashlib,json,pickle,sys,time
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
NAMES=['A_LCA_on_B_marked','A_LCA_on_B_unmarked','B_LCA_on_A_marked','B_LCA_on_A_branchers',
 'all_cluster_intersection','marked_marked_cluster_intersection','marked_unmarked_cluster_intersection',
 'brancher_marked_cluster_intersection','brancher_unmarked_cluster_intersection',
 'A_marked_depth_sum','B_marked_depth_sum','A_anonymous_brancher_count','A_marked_leaf_count','B_marked_leaf_count']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def main():
    a=json.loads((F/'branch_H1_r7.json').read_text());b=json.loads((F/'maximal_B_grammar.json').read_text())
    with (F/'real_leaf_profile_packets.pkl').open('rb') as f:pm=pickle.load(f)
    intervals=[((1<<j)-1)^((1<<i)-1) for i in range(7) for j in range(i+1,8)];ii={v:i for i,v in enumerate(intervals)}
    def metadata(t,isA):
        clusters=[];marked=[];leaves=0
        def visit(u,d):
            nonlocal leaves
            if not isinstance(u,tuple):return 0
            k=u[0];rank=k//1000-1 if isA and k%1000==0 else ((k-1)//2 if not isA and k%2 else -1)
            l,r=visit(u[1],d+1),visit(u[2],d+1);s=l|r|(1<<rank if rank>=0 else 0)
            assert s in ii
            clusters.append((s,d,rank>=0));marked.append(rank>=0)
            if rank>=0 and not l and not r:leaves+=1
            return s
        visit(t,0);m=np.zeros(28,dtype=np.int16);u=m.copy();dep=m.copy()
        for s,d,ism in clusters:(m if ism else u)[ii[s]]+=1
        for s,j in ii.items():dep[j]=max(d for ss,d,ism in clusters if ss&s==s)
        singles=[ii[1<<i] for i in range(7)]
        return m,u,dep,int(dep[singles].sum()),len(clusters)-7,leaves
    AM=[];AU=[];AD=[];AS=[];AC=[];AL=[]
    for t in a['A_branch_trees']:
        m,u,d,s,c,l=metadata(tup(t),True);AM.append(m);AU.append(u);AD.append(d);AS.append(s);AC.append(c);AL.append(l)
    BM=[];BU=[];BD=[];BS=[];BC=[];BL=[]
    for t in b['trees']:
        m,u,d,s,c,l=metadata(tup(t),False);BM.append(m);BU.append(u);BD.append(d);BS.append(s);BC.append(c);BL.append(l)
    AM,AU,AD,BM,BU,BD=map(lambda v:np.array(v,dtype=np.int16),(AM,AU,AD,BM,BU,BD));AT=(AM+AU>0).astype(np.int16)
    @functools.lru_cache(maxsize=4)
    def values(j):
        return np.array([AD@BM[j],AD@BU[j],AM@BD[j],AU@BD[j],AT@(BM[j]+BU[j]>0).astype(np.int16),
          AM@BM[j],AM@BU[j],AU@BM[j],AU@BU[j],AS,np.full(5947,BS[j]),AC,AL,np.full(5947,BL[j])],dtype=np.int16).T
    differences=[];weights=[];refs=[]
    # Deterministic spread over the complete B grammar and every source group.
    # These are necessary inequalities, not a finite passing proof.
    selected=range(0,len(pm['packets']),7)
    for pid in selected:
        p=pm['packets'][pid];fs,ft=values(p['source']),values(p['target'])
        for h,key in p['low']:
            rows=pm['groups'][key]
            if not rows:continue
            inds=sorted(set(np.linspace(0,len(rows)-1,min(10,len(rows)),dtype=int).tolist()))
            for j in inds:
                s,t,w=rows[j];differences.append((ft[t]-fs[s]).tolist());weights.append(2*h-p['Q']);refs.append((pid,h,key,j,s,t))
        if time.process_time()-START>CAP-8:break
    delta=np.array(differences,dtype=np.int16);ww=np.array(weights,dtype=np.int16)
    # Direct alternative: lambda>=0, sum lambda=1, sum lambda DeltaF=0.
    # Minimize the weighted source price. At most d+2 basic entries suffice.
    Aeq=np.vstack((delta.T,np.ones(len(delta),dtype=np.int16)));beq=np.array([0]*len(NAMES)+[1])
    res=linprog(ww.astype(float),A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs',options={'time_limit':max(.25,CAP-(time.process_time()-START)-3),'threads':1})
    cert=None
    if res.success and res.fun < -1e-8:
        support=np.flatnonzero(res.x>1e-8).tolist();matrix=[[Fraction(int(Aeq[i,j])) for j in support]+[Fraction(int(beq[i]))] for i in range(len(beq))]
        pivots=[];r=0
        for c in range(len(support)):
            pivot=next((i for i in range(r,len(matrix)) if matrix[i][c]),None)
            if pivot is None:continue
            matrix[r],matrix[pivot]=matrix[pivot],matrix[r];den=matrix[r][c];matrix[r]=[v/den for v in matrix[r]]
            for i in range(len(matrix)):
                if i!=r and matrix[i][c]:
                    q=matrix[i][c];matrix[i]=[v-q*w for v,w in zip(matrix[i],matrix[r])]
            pivots.append(c);r+=1
        assert len(pivots)==len(support)
        lam=[Fraction(0)]*len(support)
        for i,c in enumerate(pivots):lam[c]=matrix[i][-1]
        assert all(v>=0 for v in lam) and sum(lam)==1
        assert all(sum(v*int(delta[j,k]) for v,j in zip(lam,support))==0 for k in range(len(NAMES)))
        price=sum(v*int(ww[j]) for v,j in zip(lam,support));assert price<0
        cert={'weighted_price':str(price),'rows':[{'reference':refs[j],'lambda':str(v),'weight':int(ww[j]),'delta':delta[j].tolist()} for v,j in zip(lam,support) if v]}
    report={'status':'JOINT_GEOMETRY_LINEAR_CLASS_REFUTED' if cert else 'NO_REFUTATION_DERIVED','features':NAMES,
      'inequalities':len(delta),'last_packet_examined':pid,'LP_status':str(res.message),'LP_objective':None if not res.success else float(res.fun),
      'exact_rational_certificate':cert,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'not_a_source_cycle':True,'not_a_Coarse_Double_refutation':True,
      'input_sha256':{p:sha(F/p) for p in ('real_leaf_profile_packets.pkl','branch_H1_r7.json','maximal_B_grammar.json','JOINT_CLUSTER_POTENTIAL_BOX.md')}}
    with (F/'joint_cluster_linear_result.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('exact_rational_certificate','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof226_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
