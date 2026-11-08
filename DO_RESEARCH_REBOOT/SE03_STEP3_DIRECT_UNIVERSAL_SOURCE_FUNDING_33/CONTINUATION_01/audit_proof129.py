"""Eight arbitrary-term protected-fringe source identities."""
import json,time,sys
from pathlib import Path
from audit_verify35 import splay,node
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def project(t,p,tag):
    if not node(t):return t
    k,L,R=t;L=project(L,p,tag);R=project(R,p,tag)
    if k!=p:return k,L,R
    if tag=='L':j,A,E=L;assert E=='E';return j,A,R
    if tag=='R':j,E,D=R;assert E=='E';return j,L,D
    assert L=='E' or R=='E';return R if L=='E' else L
def main():
    inputs=[('RR_birth',(2,'A',(5,'E',(8,'B','C'))),8,5,None,'L'),('LL_birth',(8,(5,(2,'A','B'),'E'),'C'),2,5,None,'R'),('RL_unary',(2,'A',(8,(5,'B','C'),'E')),5,8,None,None),('LR_unary',(8,(2,'E',(5,'A','B')),'C'),5,2,None,None),('L_retire',(8,(5,(2,'A','E'),'R'),'C'),2,5,'L',None),('L_survive',(8,(5,(2,'A','E'),(6,'B','C')),'D'),6,5,'L','L'),('R_retire',(2,'A',(5,'L',(8,'E','D'))),8,5,'R',None),('R_survive',(2,'A',(5,(4,'B','C'),(8,'E','D'))),4,5,'R','R')];rows=[]
    for name,t,x,p,before,after in inputs:
        actual,H=splay(t,x);s=project(t,p,before);end=project(actual,p,after);old,h=splay(s,x);assert old==end and H==h==1;rows.append({'case':name,'source':t,'target':x,'private':p,'source_tag':before,'destination_tag_if_branch_remains':after,'actual_after':actual,'old_source':s,'old_after':old,'actual_H':H,'old_H':h})
    out('protected_fringe_H1_local_forms.json',{'status':'COMPLETE_EIGHT_PROTECTED_FRINGE_H1_SOURCE_IDENTITIES','schemas':rows,'population_scope':'arbitrary ordered free terms, V-free E; branch tags removed when the remaining side becomes V-free','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'});print(json.dumps({'status':'PASS_EIGHT_SOURCE_IDENTITIES','schemas':8,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof129_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
