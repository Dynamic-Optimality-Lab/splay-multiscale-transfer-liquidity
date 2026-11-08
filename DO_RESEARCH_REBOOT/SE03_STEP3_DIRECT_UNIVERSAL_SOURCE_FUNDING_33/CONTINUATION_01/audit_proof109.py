"""Simultaneous end-gap source equations, with arbitrary exterior populations."""
import json,time,sys,itertools,collections
from pathlib import Path
from audit_verify35 import formal_path,splay,node
from audit_proof106 import leaves,replace_leaves,classify
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def reflect(t):return t if not node(t) else (-t[0],reflect(t[2]),reflect(t[1]))
def grammar(word,C):
    bare,x=formal_path(word);one=C.index('m') if 'm' in C else C.count('L')-.25
    last=C.index('z') if 'z' in C else len(C)-C.count('H')-.75
    f=max(i for i,c in enumerate(C) if c=='F');j=C.index('J');m={}
    for k,v in enumerate(leaves(bare)):
        if 'm' not in C and k==C.count('L'):m[v]=(one,'E','E')
        elif 'z' not in C and k==len(C)-C.count('H'):m[v]=(last,'E','E')
        elif f<k<=j:m[v]='X'+str(k)
        else:m[v]='E'
    return replace_leaves(bare,m),x,one,last,{i:c for i,c in enumerate(C)}
def project(t,C,one,last):
    if not node(t):return t
    k,L,R=t;L=project(L,C,one,last);R=project(R,C,one,last);color=C.get(k,'m' if k==one else 'z')
    if color=='L':assert L=='E';return R
    if color=='H':assert R=='E';return L
    if color=='F':
        if L=='E':return R
        assert L==(one,'E','E');return one,'E',R
    if color=='J':
        if R=='E':return L
        assert R==(last,'E','E');return last,L,'E'
    return k,L,R
def main():
    direct=[];helpers=[]
    for d in range(1,5):
        for bits in itertools.product('LR',repeat=d):
            word=''.join(bits)
            for nums in itertools.combinations_with_replacement(range(7),d+1):
                colors=tuple('LmFMJzH'[i] for i in nums)
                if colors.count('m')>1 or colors.count('z')>1 or 'F' not in colors or 'J' not in colors:continue
                t,x,one,last,C=grammar(word,colors);root=t[0];marked=lambda k:C[k] in ('m','M','z');after,h=splay(t,x);s,p=project(t,C,one,last),project(after,C,one,last)
                row={'path':word,'colors':colors,'minimum_anchor':one,'maximum_anchor':last,'target':x,'source':t,'actual_after':after,'projected_source':s,'projected_after':p,'actual_H':h}
                if marked(root) and marked(x):
                    label,oldword,h0=classify(s,p,x,h,one)
                    if label.startswith('UNCLASSIFIED'):
                        reflected,ww,hh=classify(reflect(s),reflect(p),-x,h,-last)
                        if not reflected.startswith('UNCLASSIFIED'):label='REFLECTED_'+reflected
                    row.update(kind='direct',label=label,old_path=oldword,old_H=h0);direct.append(row)
                elif d<=2 and marked(root)!=marked(x):
                    target=x if marked(x) else p[0];comparison,h0=splay(s,target);row.update(kind='helper',old_target=target,old_H=h0,commutes=p==comparison);helpers.append(row)
    bad=[r for r in direct if r['label'].startswith('UNCLASSIFIED') or r['old_H']>r['actual_H']]+[r for r in helpers if not r['commutes'] or r['old_H']>1]
    assert time.process_time()-START<CAP-1
    z={'status':'COMPLETE_MIXED_BOTH_END_GAPS_SOURCE_GRAMMAR' if not bad else 'MIXED_BOTH_END_GAPS_OPEN','direct_schemas':direct,'helper_schemas':helpers,'class_counts':dict(collections.Counter(r['label'] for r in direct)),'unresolved':bad,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('mixed_both_end_gaps_source_normal_forms.json',z);print(json.dumps({'status':z['status'],'direct':len(direct),'helpers':len(helpers),'classes':z['class_counts'],'unresolved':len(bad)}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof109_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
