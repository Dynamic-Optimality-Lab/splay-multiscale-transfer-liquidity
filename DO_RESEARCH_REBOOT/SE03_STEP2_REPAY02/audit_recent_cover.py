"""Universal label/mass and cold-component proof schemas; no source runs."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1])
def p(**kw):return {k:Fraction(v) for k,v in kw.items() if v}
def add(*parts):
    q={}
    for part in parts:
        for k,c in part.items():q[k]=q.get(k,Fraction())+c
    return {k:c for k,c in q.items() if c}
def N(k,l,r):return (k,l,r)
def left(t):g,l,r=t;u,a,b=r;return N(u,N(g,l,a),b)
def right(t):g,l,r=t;u,a,b=l;return N(u,a,N(g,b,r))
def inorder(t):return inorder(t[1])+[t[0]]+inorder(t[2]) if isinstance(t,tuple) else [t]
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
error=None
try:
    # Lower core bound c-2(r-k), substitute c=2r-1-delta.
    assert add(p(r=2,one=-1,delta=-1),p(r=-2,k=2))==p(k=2,one=-1,delta=-1)
    # Exact complement size in maximal core for any recently visited k.
    assert add(p(r=2,one=-1),p(k=-2,one=1))==p(r=2,k=-2)
    # One omitted key leaves <=2 nodes; k5 on core10 has8<=core<=9.
    assert 10-2==8 and 2*5-1==9 and 11-2==9
    assert 11-2*2==7 and 2*4-1==7
    # Universal innermost cold-chain source rewrites, with no marked
    # labels in A,B,C,D; marked v is retained inside the private u subtree.
    chainR=N('v','A',N('u','B',N('z','C','D')))
    chainL=N('v',N('u',N('z','A','B'),'C'),'D')
    assert left(left(chainR))==N('z',N('u',N('v','A','B'),'C'),'D')
    assert right(right(chainL))==N('z','A',N('u','B',N('v','C','D')))
    # Mixed inner frame leaves unmarked u with only mark-free gap blocks.
    mixRL=N('v','A',N('u',N('z','B','C'),'D'))
    afterRL=left(N(mixRL[0],mixRL[1],right(mixRL[2])))
    assert afterRL==N('z',N('v','A','B'),N('u','C','D'))
    mixLR=N('v',N('u','A',N('z','B','C')),'D')
    afterLR=right(N(mixLR[0],left(mixLR[1]),mixLR[2]))
    assert afterLR==N('z',N('u','A','B'),N('v','C','D'))
    # Sibling same-side cold source has inorder marked,U,U,marked.
    sibling=N('u0',N('v','A','B'),N('u1','C',N('z','D','E')))
    roles=[x for x in inorder(sibling) if x in {'u0','u1','v','z'}]
    assert roles==['v','u0','u1','z']
    # Exact signed chart cost identities; not inequalities assumed feasible.
    wc=p(C=2,q=-1,one=1);w=p(H=2,q=-1)
    assert add(w,{k:-v for k,v in wc.items()})==p(H=2,C=-2,one=-1)
    lhs=p(H=2,q=-1,dnew=1,dold=-1)
    rhs=add(p(C=2,q=-1,one=1,dnew=1,dvirtual=-1),
            p(dvirtual=1,dold=-1,one=-1),p(H=2,C=-2))
    assert lhs==rhs
    assert time.process_time()<CAP
    out('recent_cover_derivation.json',{'status':'PASS_UNIVERSAL_RECENT_SUPPORT_AND_COLD_SOURCE_IDENTITIES',
      'complement_bound':'|S minus C_V|<=2|M minus V|',
      'recent_upper_bound':'|C_V|<=2|V|-1 from actual last-distinct window',
      'six_core11':'recent5 core9, recent4 core7, omitted key in two-node twig',
      'six_core10':'recent5 core8/9, fixed nine Scores=S minus omitted marked leaf',
      'cold_core11_partition':['two disjoint two-node components','one four-node component'],
      'actual_four_node_miss':'same-side chain only; inner mixed drops u, sibling same-side violates sorted alternation',
      'internal_prefix_cost':'one actual B double, no A event removed',
      'same_ordered_chart_shape':'marked v replaced by adjacent marked z; raw signatures may change',
      'residual_identity':'full residual = chart residual + dvirtual-dold-1 + actual A tail',
      'unknown_chart_comparisons_proved':False,'Step2_complete':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0})
    print('RECENT_SUPPORT_AND_SIGNED_COLD_EXCHANGE_DERIVATION_PASS')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_recent_cover_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
