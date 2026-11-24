"""Independent immutable primitive replay of all saved COMPLETE witnesses.

Does not import the producer or trust its interval, potential, Psi, neutral,
source-closure or original cyclic-run fields. Same-agent code independence.
"""
import bisect
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.setrecursionlimit(30000)
HERE=Path(__file__).resolve().parent


def vine(n):
    t=None
    for x in range(n,0,-1):
        t=(x,None,t)
    return t


def labels(t):
    result=set()
    def visit(v):
        if v is None:return None
        k,l,r=v
        lrange=visit(l);rrange=visit(r)
        lo=lrange[0] if lrange else k
        hi=rrange[1] if rrange else k
        result.add((lo,hi))
        return lo,hi
    visit(t)
    return result


def path(t,x):
    found=[]
    while t is not None:
        found.append(t)
        if t[0]==x:return found
        t=t[1] if x<t[0] else t[2]
    raise AssertionError('missing target')


def rotate(t,parent,direction):
    frames=[];cur=t
    while cur[0]!=parent:
        k,l,r=cur
        if parent<k:frames.append(('L',k,r));cur=l
        else:frames.append(('R',k,l));cur=r
    k,l,r=cur
    if direction=='LEFT':
        pk,h,rr=r;sub=(pk,(k,l,h),rr)
    else:
        pk,ll,h=l;sub=(pk,ll,(k,h,r))
    for side,k,sibling in reversed(frames):
        sub=(k,sub,sibling) if side=='L' else (k,sibling,sub)
    return sub


def potential(A,B,layer):
    return -sum((hi-lo+1==15) if layer=='15' else (hi-lo+1>=3 and ((hi-lo+1)&(hi-lo+2))==0)
                for lo,hi in B-A)


def verify(file):
    w=json.loads(file.read_text());s=w['source'];p,q,n=s['p'],s['q'],s['N'];assert n==(1<<(p+1))*(q+1)+1
    assert s['prefix']==[]
    kept={n+1-(1<<j) for j in range(p+1)}
    expected=[['prep','D',x] for x in range(2,n+1)]+[['descent','K' if x in kept else 'D',x] for x in range(n,0,-1)]+[['forward','K',x] for x in range(1,n+1)]+[['reverse','K',x] for x in range(n-1,0,-1)]
    assert s['word']==expected and len(expected)==4*n-2
    trees={'A':vine(n),'B':vine(n)};sets={k:labels(t) for k,t in trees.items()};initial=trees['A']
    events=w['real_rotations'];cursor=0;demands=[];bs=defaultdict(list);ls=defaultdict(list);Asteps=Q=Z=0;producer_starts={}
    for op,(_,mode,target) in enumerate(expected,1):
        for actor in ['A','B'] if mode=='K' else ['A']:
            trace=path(trees[actor],target);depth=len(trace)-1
            if actor=='A':Asteps+=(depth+1)//2
            else:Q+=depth//2;Z+=depth%2;producer_starts[op]=cursor
            step=0
            while len(trace)>1:
                step+=1
                if len(trace)==2:
                    typ='ZIG';promoted=[target];frame=None
                else:
                    x,pr,g=trace[-1],trace[-2],trace[-3]
                    typ=('L' if g[1] is pr else 'R')+('L' if pr[1] is x else 'R')
                    promoted=[pr[0],target] if typ[0]==typ[1] else [target,target]
                    frame=(min(labels(g),key=lambda z:z[0])[0],max(labels(g),key=lambda z:z[1])[1])
                    # The whole frame is the unique largest physical subtree interval.
                    frame=max(labels(g),key=lambda z:z[1]-z[0])
                deltas=[]
                for bit,x in enumerate(promoted):
                    e=events[cursor];assert e['id']==[actor,op,step,bit] and e['type']==typ and e['promoted']==x and e['target']==target
                    xtrace=path(trees[actor],x);parent=xtrace[-2]
                    # Compare both pointer directions without dereferencing an empty left child.
                    direction='RIGHT' if parent[1] is not None and parent[1][0]==x else 'LEFT'
                    assert direction==e['direction'] and parent[0]==e['demoted']
                    pre={layer:potential(sets['A'],sets['B'],layer) for layer in ['M','15']}
                    psi_before=len(sets['B']-sets['A']);old=sets[actor]
                    trees[actor]=rotate(trees[actor],parent[0],direction);sets[actor]=labels(trees[actor]);new=sets[actor]
                    removed=old-new;created=new-old
                    assert len(removed)==len(created)==1
                    assert list(next(iter(removed)))==e['removed'] and list(next(iter(created)))==e['created']
                    dpsi=len(sets['B']-sets['A'])-psi_before
                    assert dpsi==e['psi_delta'];deltas.append(dpsi)
                    for layer in ['M','15']:
                        post=potential(sets['A'],sets['B'],layer)
                        assert pre[layer]==e['phi_before'][layer] and post==e['phi_after'][layer] and post-pre[layer]==e['phi_delta'][layer]
                        if actor=='A':assert post-pre[layer]<=1
                    if actor=='A':assert all(lo==1 or hi==n for lo,hi in sets['A'])
                    else:
                        bs[next(iter(created))].append(cursor);ls[next(iter(removed))].append(cursor)
                    cursor+=1
                if actor=='B' and frame:
                    neutral=deltas==[0,0];inside=frame[0]>1 and frame[1]<n
                    demands.append({'id':[op,step],'frame':list(frame),'neutral':neutral,'interior':inside,'U_int':neutral and inside})
                trace=path(trees[actor],target)
    assert cursor==len(events) and trees['A']==trees['B']==initial and Asteps==4*(n-1)
    got={tuple(x['id']):x for x in demands};saved={tuple(x['id']):x for x in w['all_B_double_records']};assert got.keys()==saved.keys()
    for identifier,d in got.items():
        x=saved[identifier]
        assert all(x[k]==v for k,v in d.items())
        if not d['U_int']:continue
        lab=tuple(d['frame']);start=producer_starts[identifier[0]]
        b=bs[lab];loss=ls[lab];j=bisect.bisect_left(b,start)-1;gamma=b[j] if j>=0 else b[-1]-len(events)
        prior=[z for z in loss if z<gamma%len(events)];kap=(prior[-1] if prior else loss[-1]-len(events))+(gamma//len(events))*len(events)
        assert kap<gamma<start
        assert events[gamma%len(events)]['id']==x['Gamma'] and events[kap%len(events)]['id']==x['kappa']
        assert gamma//len(events)==x['Gamma_lap'] and kap//len(events)==x['kappa_lap']
    if p==3:assert Q==28*q+25 and Z==28*q+27 and sum(d['U_int'] for d in demands)==10*q+5
    return {'file':file.name,'p':p,'q':q,'N':n,'operations':len(expected),'real_rotations':cursor,'A':Asteps,'Q_B':Q,'Z_B':Z,
            'U_int':sum(d['U_int'] for d in demands),'all_original_cyclic_records_verified':True,'exact_full_pair_closure':True}


def main():
    start=time.process_time();results=[verify(f) for f in sorted(HERE.glob('*_complete_witness.json'))]
    out={'passed':True,'witnesses':results,'cpu_seconds':time.process_time()-start,
         'verification_level':'Independent immutable primitive implementation; same agent, not a proof assistant or external reviewer.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'INDEPENDENT_EVENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
