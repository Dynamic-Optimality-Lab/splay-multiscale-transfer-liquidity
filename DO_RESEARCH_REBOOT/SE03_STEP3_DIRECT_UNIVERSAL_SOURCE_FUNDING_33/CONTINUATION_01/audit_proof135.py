"""Uniform framed source identities and an ordinary comparison beyond contractions."""
import json,time,sys
from pathlib import Path
from audit_verify35 import splay,node
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    # G<j<p<R, with no other anchor between G and j or j and p.
    G,j,p,R=1,2,2.5,4;E='E';X='X';A0=(G,E,(j,E,(p,E,(R,X,E))));T0=(G,E,(j,E,(R,X,E)))
    A,a1=splay(A0,R);A,a2=splay(A,G);S=A;assert (a1,a2)==(2,1) and S==(G,E,(R,(p,(j,E,E),X),E))
    C,c1=splay(T0,R);C,c2=splay(C,G);assert (c1,c2)==(1,1);CS=C;assert CS==(G,E,(j,E,(R,X,E)))
    A,a3=splay(S,p);A,a4=splay(A,R);T=A;assert (a3,a4)==(1,1) and T==(R,(p,(G,E,(j,E,E)),X),E)
    C,c3=splay(CS,j);C,c4=splay(C,R);CT=C;assert (c3,c4)==(1,1) and CT==(R,(j,(G,E,E),X),E)
    U,u=splay(T,G);V,v=splay(U,R);assert (u,v)==(1,1) and V==T;CU,cu=splay(CT,G);CV,cv=splay(CU,R);assert (cu,cv)==(1,1) and CV==CT
    HP,hp=splay(U,p);HR,hr=splay(HP,R);assert (hp,hr)==(1,1) and HR==T;CP,cp=splay(CU,j);CR,cr=splay(CP,R);assert cp==cr==1 and CR==CT
    z={'status':'UNIFORM_FRAMED_RETURN_AND_PROXY_SOURCE_IDENTITIES','initial_unary_A':A0,'old_initial':T0,'marked_creator_word':[R,G],'actual_creator_costs':[a1,a2],'comparison_creator_costs':[c1,c2],'framed_source':S,'framed_comparison':CS,'private_activation_actual_word':[p,R],'private_activation_comparison_word':[j,R],'actual_costs':[a3,a4],'comparison_costs':[c3,c4],'unprotected_destination':T,'normalized_comparison_destination':CT,'actual_return_intermediate':U,'comparison_return_intermediate':CU,'actual_return_word':[G,R],'comparison_return_word':[G,R],'return_costs':[u,v],'both_return_exactly':True,'repeated_private_proxy_from_return_intermediate':True,'arbitrary_finite_repetition':'the two exact actual/comparison state pairs T/CT and U/CU close under G,R and under Dp,R with proxy Dj,R; induction, not sampled repetition','scope':'any ordered G<j<p<R with all other anchors strictly between p,R in arbitrary rigid term X; arbitrary independent V-free gap populations by ordinary source substitution','B_operations_changed':False,'unprotected_destination_reason':'left side of p has old G root and nonempty right j; R tag forbidden since p is on left spine of R','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('framed_return_proxy_source_identities.json',z);print(json.dumps({'status':z['status'],'actual_creator_costs':z['actual_creator_costs'],'comparison_creator_costs':z['comparison_creator_costs'],'return_exact':True,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof135_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
