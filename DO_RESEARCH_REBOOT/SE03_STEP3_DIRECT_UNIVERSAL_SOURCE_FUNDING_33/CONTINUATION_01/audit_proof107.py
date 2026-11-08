"""Uniform first-gap H1 private-helper comparison identities, all populations."""
import json,time,itertools
from pathlib import Path
from audit_verify35 import formal_path,splay,node
from audit_proof106 import leaves,replace_leaves,pred
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def term(word,P,one,explicit):
    t,x=formal_path(word);k=len(P);m={}
    for j,v in enumerate(leaves(t)):
        if not explicit and j==0:m[v]=(one,'E','E')
        elif j<=(k if explicit else k-1):m[v]='E'
        else:m[v]='X'+str(j)
    return replace_leaves(t,m),x
def main():
    rows=[]
    for depth in (1,2):
        for letters in itertools.product('LR',repeat=depth):
            word=''.join(letters);bare,target=formal_path(word)
            for explicit in (True,False):
                one=0 if explicit else -1
                for count in range(1,depth+1):
                    P=set(range(1,count+1)) if explicit else set(range(count))
                    if bare[0] in P or target not in P:continue
                    t,y=term(word,P,one,explicit);after,h=splay(t,y);before_old=pred(t,P,one);after_old=pred(after,P,one);comparison,h0=splay(before_old,one);assert h==1 and h0<=1 and after_old==comparison
                    rows.append({'kind':'marked_root_private_helper','path':word,'private':sorted(P),'one':one,'target':y,'actual_source':t,'actual_after':after,'projected_source':before_old,'projected_after':after_old,'old_comparison_target':one,'actual_H':h,'old_H':h0})
            # A private root followed by a genuine old marked target.
            for explicit in (True,False):
                one=0 if explicit else -1
                for count in range(1,depth+1):
                    P=set(range(1,count+1)) if explicit else set(range(count))
                    if bare[0] not in P or target in P or (explicit and target!=one):continue
                    t,x=term(word,P,one,explicit);after,h=splay(t,x);before_old=pred(t,P,one);after_old=pred(after,P,one);comparison,h0=splay(before_old,x);assert h==1 and h0<=1 and after_old==comparison
                    rows.append({'kind':'private_root_marked_target','path':word,'private':sorted(P),'one':one,'target':x,'actual_source':t,'actual_after':after,'projected_source':before_old,'projected_after':after_old,'old_comparison_target':x,'actual_H':h,'old_H':h0})
    result={'status':'COMPLETE_FIRST_GAP_H1_PRIVATE_HELPER_TERM_IDENTITIES','schemas':rows,'counts':{kind:sum(r['kind']==kind for r in rows) for kind in ('marked_root_private_helper','private_root_marked_target')},'uniform_source_scope':'any finite first-gap private population; source positive events H1, arbitrary ordered free payloads; no finite population test','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('first_gap_private_helper_normal_forms.json',result);print(json.dumps({k:v for k,v in result.items() if k!='schemas'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof107_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
