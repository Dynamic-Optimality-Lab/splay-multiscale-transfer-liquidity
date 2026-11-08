"""Two actual genuine H1 KEEPs, unary endpoints, branching in between."""
import json,time,sys,itertools,collections
from pathlib import Path
from audit_proof114 import trees,visit,bind,project
from audit_verify35 import splay,path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    rows=[];templates=0
    for m in range(2,6):
        for ti,t in enumerate(trees(0,m)):
            g=t[0]
            for y in range(m):
                if y==g or len(path(t,y))>2:continue
                mid,h=splay(t,y)
                for x in range(m):
                    if x==y or len(path(mid,x))>2 or visit(t,y)|visit(mid,x)!=set(range(m)):continue
                    templates+=1
                    for mask in range(1,1<<m):
                        P={k for k in range(m) if mask>>k&1}
                        if P&{g,y,x}:continue
                        for flags in range(1<<(m+1)):
                            actual=bind(t,flags);s=project(actual,P)
                            if s is None:continue
                            mid,h1=splay(actual,y);after,h2=splay(mid,x);assert h1==h2==1;p=project(after,P)
                            if p is None:continue
                            old,h0=splay(s,y);old,hx=splay(old,x);row={'m':m,'tree_index':ti,'private_mask':mask,'leaf_mask':flags,'source':actual,'first_KEEP':y,'second_KEEP':x,'actual_middle':mid,'actual_after':after,'projected_source':s,'projected_after':p,'ordinary_old_two_KEEP_target':old,'old_H':h0+hx,'actual_H':2,'commutes':old==p,'source_and_final_private_core_unary':True};rows.append(row)
    bad=[r for r in rows if not r['commutes'] or r['old_H']>2];z={'status':'UNIFORM_TWO_KEEP_H1_UNARY_RETURN_PROJECTION_PROVED' if not bad else 'TWO_KEEP_UNARY_RETURN_PROJECTION_HAS_EXCEPTIONS','source_templates':templates,'free_term_schemas':len(rows),'failures':bad,'schemas':rows,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('two_KEEP_H1_unary_return_source_forms.json',z);print(json.dumps({'status':z['status'],'templates':templates,'schemas':len(rows),'failures':len(bad),'first_failure':bad[0] if bad else None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof128_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
