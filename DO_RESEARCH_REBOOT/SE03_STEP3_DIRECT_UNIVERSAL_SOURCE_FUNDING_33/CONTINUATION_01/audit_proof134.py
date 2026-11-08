"""Activation from general protected sources; expose only required virtual fringes."""
import json,time,sys,itertools
from pathlib import Path
from audit_proof114 import trees,visit,bind
from audit_proof130 import spines
from saturated_fringe_source_tools import allowed_tags
from audit_verify35 import splay,path,node
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
class Invalid(Exception):pass
class Need(Exception):
    def __init__(self,key,side):self.key=key;self.side=side
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def replace(t,bindings):
    if not node(t):return replace(bindings[t],bindings) if t in bindings else t
    return t[0],replace(t[1],bindings),replace(t[2],bindings)
def oldkeys(t,P):return [] if not node(t) else oldkeys(t[1],P)+([] if t[0] in P else [t[0]])+oldkeys(t[2],P)
def phi(t,P,tags,LS,RS,refine=False,used=None):
    if not node(t):return t
    k,L,R=t;L=phi(L,P,tags,LS,RS,refine,used);R=phi(R,P,tags,LS,RS,refine,used)
    if k not in P:return k,L,R
    if L=='E':return R
    if R=='E':return L
    side=tags[k]
    if used is not None:used.add(k)
    if side=='L':
        if k in RS:raise Invalid()
        if not node(L):
            if refine:raise Need(L,'L')
            raise Invalid()
        if L[2]!='E':raise Invalid()
        return L[0],L[1],R
    if k in LS:raise Invalid()
    if not node(R):
        if refine:raise Need(R,'R')
        raise Invalid()
    if R[1]!='E':raise Invalid()
    return R[0],L,R[2]
def main():
    rows=[];seen=set();bad=None;complete=True;templates=0
    for m in range(2,6):
        for ti,t in enumerate(trees(0,m)):
            g=t[0]
            for y in range(m):
                if y==g or len(path(t,y))>2:continue
                middle,h=splay(t,y)
                for x in range(m):
                    if x==y or len(path(middle,x))>2 or visit(t,y)|visit(middle,x)!=set(range(m)):continue
                    templates+=1
                    for mask in range(1,1<<m):
                        P={k for k in range(m) if mask>>k&1}
                        if g in P or x in P or y not in P:continue
                        for flags in range(1<<(m+1)):
                            base=bind(t,flags)
                            for bits in itertools.product('LR',repeat=len(P)):
                                tags=dict(zip(sorted(P),bits));stack=[({}, {'X'+str(j):(j-1,j) for j in range(m+1)})]
                                while stack:
                                    if time.process_time()-START>CAP-8:complete=False;break
                                    bindings,bounds=stack.pop();actual=replace(base,bindings);allowed=allowed_tags(actual,P,bounds)
                                    if any(tags[k] not in allowed[k] for k in P):continue
                                    LS,RS=spines(actual);used=set()
                                    try:s=phi(actual,P,tags,LS,RS,True,used)
                                    except Invalid:continue
                                    except Need as need:
                                        assert need.key not in bindings and len(bindings)<=len(P);lo,hi=bounds[need.key];j=(lo+hi)/2;name='Y'+str(len(bindings))+'_'+need.key
                                        for nonempty in (False,True):
                                            b2=bindings.copy();b2[need.key]=(j,name if nonempty else 'E','E') if need.side=='L' else (j,'E',name if nonempty else 'E');bb=bounds.copy();bb[name]=(lo,j) if need.side=='L' else (j,hi);stack.append((b2,bb))
                                        continue
                                    key=(actual,y,x,mask,tuple((k,tags[k]) for k in sorted(used)))
                                    if key in seen:continue
                                    seen.add(key);mid,h1=splay(actual,y);after,h2=splay(mid,x);assert h1==h2==1;LS2,RS2=spines(after);after_allowed=allowed_tags(after,P,bounds);witness=None;any_tags=False
                                    for dstbits in itertools.product('LR',repeat=len(P)):
                                        dtags=dict(zip(sorted(P),dstbits))
                                        if any(dtags[k] not in after_allowed[k] for k in P):continue
                                        try:p=phi(after,P,dtags,LS2,RS2)
                                        except Invalid:continue
                                        any_tags=True
                                        for z in oldkeys(actual,P):
                                            old,c1=splay(s,z);old,c2=splay(old,x)
                                            if c1+c2<=2 and old==p:witness={'destination_tags':dtags,'comparison_DELETE_proxy':z,'old_event_costs':[c1,c2],'comparison_after':p};break
                                        if witness:break
                                    row={'m':m,'tree_index':ti,'private_mask':mask,'leaf_mask':flags,'actual_source_after_virtual_fringe_exposure':actual,'original_active_skeleton':base,'source_tags':tags,'used_source_tags':sorted(used),'virtual_bindings':bindings,'variable_bounds':bounds,'helper':y,'terminal':x,'actual_after':after,'old_source':s,'witness':witness,'some_destination_protected_tags_exist':any_tags};rows.append(row)
                                    if witness is None:bad=row;break
                                if not complete or bad:break
                            if not complete or bad:break
                        if not complete or bad:break
                    if not complete or bad:break
                if not complete or bad:break
            if not complete or bad:break
        if not complete or bad:break
    z={'status':'PROTECTED_SOURCE_ACTIVATION_LOCAL_CONDITION_HAS_EXCEPTION' if bad else 'PROTECTED_SOURCE_ACTIVATION_SYMBOLIC_DERIVATION_COMPLETE' if complete else 'PROTECTED_SOURCE_ACTIVATION_SYMBOLIC_DISCOVERY_PARTIAL','enumeration_complete':complete and bad is None,'source_templates_visited':templates,'source_schemas':len(rows),'schemas':rows,'exception':bad,'exception_scope':'tag-valid free source predicate; source creator-protocol reachability and arbitrary unseen comparison proxy not asserted','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('saturated_source_activation_analysis.json',z);print(json.dumps({k:v for k,v in z.items() if k not in ('schemas','exception')}));print(json.dumps({'exception':bad}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof134_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
