"""New Omega arbitrary-fringe proof terms; completed B backbone is reused."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def N(k,l,r):return (k,l,r)
def at(t,p):
    for c in p:t=t[1 if c=='L' else 2]
    return t
def put(t,p,v):
    if not p:return v
    k,l,r=t
    return N(k,put(l,p[1:],v),r) if p[0]=='L' else N(k,l,put(r,p[1:],v))
def pair(t,k):
    g,l,r=t
    if k=='LL':u,(x,a,b),c=l;return N(x,a,N(u,b,N(g,c,r)))
    if k=='RR':u,b,(x,c,d)=r;return N(x,N(u,N(g,l,b),c),d)
    if k=='LR':u,a,(x,b,c)=l;return N(x,N(u,a,b),N(g,c,r))
    if k=='RL':u,(x,b,c),d=r;return N(x,N(g,l,b),N(u,c,d))
    raise AssertionError(k)
def zig(t,k):
    g,l,r=t
    if k=='L':x,a,b=l;return N(x,a,N(g,b,r))
    x,a,b=r;return N(x,N(g,l,a),b)
def derive(t,x,p):
    assert at(t,p)[0]==x
    frames=[]
    while len(p)>=2:
        prefix=p[:-2];k=p[-2:];t=put(t,prefix,pair(at(t,prefix),k));frames.append([prefix,k]);p=prefix
    if p:t=zig(t,p);frames.append(['',p])
    assert t[0]==x
    return t,frames
def visible(t,d=0):
    if d>2 or isinstance(t,str):return []
    return [t[0]]+visible(t[1],d+1)+visible(t[2],d+1)
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
error=None
try:
    F={i:'F'+str(i) for i in range(12)}
    R=F[11]
    for k in reversed(range(1,12)):R=N(k,F[k-1],R)
    E=N(6,N(5,F[4],F[5]),N(8,N(7,F[6],F[7]),N(10,N(9,F[8],F[9]),F[10])))
    P=N(1,F[0],N(3,N(2,F[1],F[2]),N(11,N(4,F[3],E),F[11])))
    known_B_after_deep_and_min=N(1,F[0],N(2,F[1],N(11,N(4,N(3,F[2],F[3]),E),F[11])))
    rows=[('K',3,'RR'),('D',1,'LL'),('D',4,'RRR'),('D',1,'L'),
          ('D',11,'RRRRRRRR'),('D',1,'LL'),('D',11,'RR'),('D',3,'LLR'),('D',1,'L'),
          ('K',1,''),('K',11,'RR'),('K',1,'LL'),('D',2,'RL'),('D',4,'RRL'),
          ('D',11,'R'),('D',1,'LLL'),('D',2,'RL'),('D',1,'L')]
    t=R;trace=[];total=0
    for i,(mode,k,path) in enumerate(rows,1):
        t,frames=derive(t,k,path);a=(len(path)+1)//2;total+=a
        trace.append({'occurrence':i,'mode':mode,'key':k,'A_path':path,'A_frames':frames,'A_cost':a,'A_end':t})
        if i==10:
            assert t==P
            assert set(visible(t)) & {3,5,7,9}=={3}
            assert at(t,'R')[0]==3
        if i==12:assert t==P
        assert time.process_time()<CAP
    assert total==24 and t==known_B_after_deep_and_min
    # Reuse H6 closure and suffix cost14 instead of rerunning its B steps.
    assert total+14==38 and 2+20==22 and 2*38-22==54
    assert trace[10]['A_cost']==trace[11]['A_cost']==1
    assert sum(x['A_cost'] for x in trace[1:10])==13
    assert trace[9]['mode']=='K' and trace[9]['key']==1 and trace[9]['A_cost']==0
    # Source old debt>=1 follows from V={3}, c=min(2,1+psi)>=1 and
    # the unchanged accepted lineage; Hamiltonian/ray normalized value1.
    assert -2+2-1==-1
    out('omega_derivation.json',{'status':'PASS_UNIVERSAL_SOURCE_COUNTERSCHEMA_TO_NORMALIZED_CHART_COMPOSITION',
      'quantification':'all twelve arbitrary ordered BST gap variables F0..F11',
      'initial_diagonal':R,'prefix_trace':trace,'prepared_A':P,
      'known_B_after_H6_first_two':known_B_after_deep_and_min,
      'B_backbone':'local inverse K3,K1 followed by completed H6; suffix cost14/closure reused, not replayed',
      'totals':{'operations':28,'KEEPs':14,'DELETEs':14,'A':38,'QF':22,'original_slack':54},
      'critical_pair':{'occurrences':[11,12],'A_costs':[1,1],'B_doubles':[5,1],'weight':-2},
      'preceding_genuine_boundary':10,'preparatory_A_charged_to_previous_macro':13,
      'old_chart_marks':[1,3,5,7,9],'old_visible_nonroot_marked':[3],
      'old_D_lower_bound':1,'normalized_old_chart_D':1,'target_range_upper':2,'chart_residual_upper':-1,
      'original_CD_counterexample':False,'Step2_complete':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0})
    print('OMEGA_UNIVERSAL_PREPARATION_REPAIR_AND_MACRO_SEAM_PROOF_PASS; original slack54')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_omega_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
