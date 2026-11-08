"""One fixed original-source C->B0 connector, not a CD inequality search."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('connector_original_tuple',ROOT/'python/independent/splay.py')
tu=importlib.util.module_from_spec(spec);spec.loader.exec_module(tu)
N=13;BOUND=742900;LEAF=tu.LEAF


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tt(t):return LEAF if t is None else tu.node(t[0],tt(t[1]),tt(t[2]))
def encode(t):
    out=0;stack=[t]
    while stack:
        s=stack.pop()
        if s[0]=='leaf':out<<=1
        else:out=(out<<1)|1;stack.append(s[3]);stack.append(s[2])
    return out
def decode(code):
    pos=2*N;key=0
    def go():
        nonlocal pos,key
        bit=(code>>pos)&1;pos-=1
        if not bit:return LEAF
        l=go();key+=1;k=key;r=go();return tu.node(k,l,r)
    t=go();assert pos==-1 and key==N;return t
def doubles(t):
    _,x,l,r=t;out=[]
    if r[0]!='leaf' and r[3][0]!='leaf':
        _,p,B,g=r;_,kg,C,D=g
        out.append(tu.node(kg,tu.node(p,tu.node(x,l,B),C),D))
    if l[0]!='leaf' and l[2][0]!='leaf':
        _,p,g,C=l;_,kg,A,B=g
        out.append(tu.node(kg,A,tu.node(p,B,tu.node(x,C,r))))
    if l[0]!='leaf' and r[0]!='leaf':
        _,p,A,B=l;_,g,C,D=r
        out.append(tu.node(g,tu.node(p,A,tu.node(x,B,C)),D))
        out.append(tu.node(p,A,tu.node(g,tu.node(x,B,C),D)))
    return out
def preimages(post):
    x=post[1];initial=doubles(post)
    _,_,l,r=post
    if r[0]!='leaf':
        _,p,B,C=r;initial.append(tu.node(p,tu.node(x,l,B),C))
    if l[0]!='leaf':
        _,p,A,B=l;initial.append(tu.node(p,A,tu.node(x,B,r)))
    seen=set();stack=initial
    while stack:
        t=stack.pop();code=encode(t)
        if code in seen:continue
        seen.add(code)
        actual,_=tu.trace(t,x);assert actual==post,'inverse must be an actual source edge'
        yield code
        cur,frames=tu._descend(t,x,[])
        for inner in doubles(cur):stack.append(tu._plug(frames,inner))


def main():
    d=json.loads((HERE/'source_discharge_certificate.json').read_text())
    start,target=encode(tt(d['C'])),encode(tt(d['B0']))
    f={start:None};b={target:None};ff=[start];bf=[target];meet=None;levels=0;inverse_checks=0
    while ff and bf and meet is None:
        levels+=1
        if len(ff)<=len(bf):
            new=[]
            for code in ff:
                tree=decode(code)
                for x in range(1,N+1):
                    out,_=tu.trace(tree,x);dest=encode(out)
                    if dest not in f:f[dest]=(code,x);new.append(dest)
                    if dest in b:meet=dest;break
                if meet is not None:break
            ff=new
        else:
            new=[]
            for code in bf:
                tree=decode(code);x=tree[1]
                for pred in preimages(tree):
                    inverse_checks+=1
                    if pred not in b:b[pred]=(code,x);new.append(pred)
                    if pred in f:meet=pred;break
                if meet is not None:break
            bf=new
        assert len(f)<=BOUND and len(b)<=BOUND
        print(json.dumps(dict(levels=levels,forward_states=len(f),backward_states=len(b),found=meet is not None)),flush=True)
    word=None
    if meet is not None:
        left=[];at=meet
        while f[at] is not None:
            at,x=f[at];left.append(x)
        word=left[::-1];at=meet
        while b[at] is not None:
            at,x=b[at];word.append(x)
        tree=decode(start)
        for x in word:tree,_=tu.trace(tree,x)
        assert encode(tree)==target
    result=dict(status='FIXED_CONNECTOR_FOUND' if word is not None else 'FIXED_TARGET_NOT_REACHED',
        source_certificate_sha256=sha(HERE/'source_discharge_certificate.json'),
        scope_sha256=sha(HERE/'AD00A_FIXED_CONNECTOR_SCOPE.md'),source_keys=N,state_bound=BOUND,
        forward_states=len(f),backward_states=len(b),levels=levels,inverse_edges_source_checked=inverse_checks,
        connector=word,complete_source_replay_verified=word is not None,
        no_general_FE02_claim=True,no_larger_key_count_fit=True)
    with (HERE/'fixed_connector_certificate.json').open('x',encoding='utf-8') as out:json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
