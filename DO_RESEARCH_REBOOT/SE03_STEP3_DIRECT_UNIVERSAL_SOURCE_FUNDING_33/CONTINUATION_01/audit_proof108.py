"""Source-uniform mixed exterior and first-gap path grammar, not population samples."""
import json,time,sys,itertools,collections
from pathlib import Path
from audit_verify35 import formal_path,splay,node
from audit_proof106 import leaves,replace_leaves,classify
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def grammar(word,colors):
    bare,x=formal_path(word);one=colors.index('m') if 'm' in colors else colors.count('L')-.5
    lastF=max(i for i,c in enumerate(colors) if c=='F');firstH=colors.index('H') if 'H' in colors else len(colors)
    m={}
    for j,v in enumerate(leaves(bare)):
        if 'm' not in colors and j==colors.count('L'):m[v]=(one,'E','E')
        elif lastF<j<=firstH:m[v]='X'+str(j)
        else:m[v]='E'
    return replace_leaves(bare,m),x,one,{i:c for i,c in enumerate(colors)}
def project(t,C,one):
    if not node(t):return t
    k,L,R=t;L=project(L,C,one);R=project(R,C,one);color=C.get(k,'m')
    if color=='L':assert L=='E';return R
    if color=='H':assert R=='E';return L
    if color=='F':
        if L=='E':return R
        assert L==(one,'E','E');return one,'E',R
    return k,L,R
def main():
    direct=[];helpers=[]
    for d in range(1,5):
        for letters in itertools.product('LR',repeat=d):
            word=''.join(letters)
            for nums in itertools.combinations_with_replacement(range(5),d+1):
                colors=tuple('LmFMH'[i] for i in nums)
                if colors.count('m')>1 or 'F' not in colors:continue
                t,x,one,C=grammar(word,colors);root=t[0];marked=lambda k:C[k] in ('m','M')
                after,h=splay(t,x);s,p=project(t,C,one),project(after,C,one)
                row={'path':word,'colors':colors,'minimum_anchor':one,'target':x,'source':t,'actual_after':after,'projected_source':s,'projected_after':p,'actual_H':h}
                if marked(root) and marked(x):
                    label,oldword,h0=classify(s,p,x,h,one);assert h0<=h;row.update(kind='direct',label=label,old_path=oldword,old_H=h0);direct.append(row)
                elif d<=2 and marked(root) and not marked(x):
                    oldtarget=p[0];comparison,h0=splay(s,oldtarget);row.update(kind='marked_root_private_helper',old_target=oldtarget,old_H=h0,commutes=p==comparison);helpers.append(row)
                elif d<=2 and not marked(root) and marked(x):
                    comparison,h0=splay(s,x);row.update(kind='private_root_marked_target',old_target=x,old_H=h0,commutes=p==comparison);helpers.append(row)
    bad=[r for r in direct if r['label'].startswith('UNCLASSIFIED')]+[r for r in helpers if not r['commutes'] or r['old_H']>1]
    assert time.process_time()-START<CAP-1
    z={'status':'COMPLETE_MIXED_EXTERIOR_FIRST_GAP_SOURCE_GRAMMAR' if not bad else 'MIXED_EXTERIOR_FIRST_GAP_OPEN','direct_schemas':direct,'helper_schemas':helpers,'class_counts':dict(collections.Counter(r['label'] for r in direct)),'unresolved':bad,'population_scope':'arbitrary finite; every length<=4 direct path operand exposed, remaining anchor-free/anchor1/arbitrary higher-anchor payloads are free terms','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'}
    out('mixed_exterior_first_gap_source_normal_forms.json',z);print(json.dumps({'status':z['status'],'direct':len(direct),'helpers':len(helpers),'classes':z['class_counts'],'unresolved':len(bad)}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof108_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
