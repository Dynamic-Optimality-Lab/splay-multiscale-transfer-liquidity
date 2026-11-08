"""Fixed source parity exposure and complete synchronization identities."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]


def load(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
tu=load('discharge_original_tuple',ROOT/'python/independent/splay.py')
def N(k,l=None,r=None):return [k,l,r]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,v):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2);f.write('\n')
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return N(t[1],jt(t[2]),jt(t[3]))
def splay(t,x):
    a,e=tu.trace(tt(t),x);return jt(a),[list(v) for v in e]
def keys(t):return [] if t is None or isinstance(t,str) else keys(t[1])+[t[0]]+keys(t[2])
def depth(t,x):
    d=0
    while t is not None and not isinstance(t,str):
        if t[0]==x:return d
        t=t[1 if x<t[0] else 2];d+=1
    raise AssertionError('present core key')
def inflate(t):
    gap=0
    def go(t):
        nonlocal gap
        if t is None:
            tag='F'+str(gap);gap+=1;return tag
        return N(t[0],go(t[1]),go(t[2]))
    ans=go(t);assert gap==14;return ans
def execute(A,B,word):
    rows=[]
    for j,(mode,x) in enumerate(word):
        da=depth(A,x);na,ae=splay(A,x)
        if mode=='KEEP':db=depth(B,x);nb,be=splay(B,x)
        else:db=None;nb=B;be=[]
        a=len(ae);q=sum(e[0]!='ZIG' for e in be)
        rows.append(dict(occurrence=j,mode=mode,key=x,source_A=A,source_B=B,destination_A=na,destination_B=nb,
            d_A=da,d_B=db,a=a,q=q,z=sum(e[0]=='ZIG' for e in be),delta=q-2*a,A_events=ae,B_events=be))
        A,B=na,nb
    return rows


def main():
    U=N(4,N(3,N(2)),N(6,N(5)))
    R=N(11,N(9,None,N(10)),N(12))
    A0=N(13,N(1,None,N(8,N(7,U),R)))
    V=N(4,None,N(5,None,N(6,None,N(7))))
    B0=N(13,N(1,None,N(11,N(3,N(2),N(8,V,N(9,None,N(10)))),N(12))))
    C=N(7,N(1,None,U),N(8,None,N(13,R)))
    assert keys(A0)==keys(B0)==keys(C)==list(range(1,14))
    startup=execute(B0,B0,[('DELETE',x) for x in [8,7,1,13]])
    assert (startup[-1]['destination_A'],startup[-1]['destination_B'])==(A0,B0)
    span=execute(A0,B0,[('KEEP',8),('KEEP',7)])
    assert [(r['a'],r['q']) for r in span]==[(1,2),(1,3)]
    assert span[-1]['destination_A']==span[-1]['destination_B']==C
    def exposure(A,B):
        da,db=depth(A,7),depth(B,7)
        return dict(d_A=da,d_B=db,G=db-2*da,z_A=da%2,z_B=db%2,E=db//2-2*((da+1)//2))
    before=exposure(A0,B0);after=exposure(span[0]['destination_A'],span[0]['destination_B'])
    assert before==dict(d_A=3,d_B=8,G=2,z_A=1,z_B=0,E=0)
    assert after==dict(d_A=2,d_B=6,G=2,z_A=0,z_B=0,E=1)
    symbolic_startup=execute(inflate(B0),inflate(B0),[('DELETE',x) for x in [8,7,1,13]])
    assert symbolic_startup[-1]['destination_A']==inflate(A0)
    symbolic_span=execute(inflate(A0),inflate(B0),[('KEEP',8),('KEEP',7)])
    assert symbolic_span[-1]['destination_A']==symbolic_span[-1]['destination_B']==inflate(C)
    proposed=[13,1,11,3,8,7,6,5,4,2,1,13]
    tail=execute(C,C,[('KEEP',x) for x in proposed])
    proposed_return=tail[-1]['destination_A']==B0
    save('source_discharge_certificate.json',dict(A0=A0,B0=B0,C=C,startup_rows=startup,source_span_rows=span,
        before_exposure=before,after_exposure=after,symbolic_startup_rows=symbolic_startup,
        symbolic_span_rows=symbolic_span,ordered_gap_variables=14,
        helper_saturated=True,upcoming_unique_positive_type=[1,3],complete_synchronization=True,
        proposed_connector=proposed,proposed_connector_rows=tail,proposed_connector_success=proposed_return,
        actual_closed_embedding_status='VERIFIED' if proposed_return else 'NOT YET ESTABLISHED',
        scope='one exact all-size source scaffold; not a universal classification of exposures',
        FE02_CD='OPEN',larger_finite_fits=0,larger_repetition_replays=0))
    print(json.dumps(dict(status='SOURCE_IDENTITIES_VERIFIED',before=before,after=after,
        helper=[1,2],positive=[1,3],complete_synchronization=True,diagonal_startup=[8,7,1,13],
        all_ordered_gap_fringe_identity=True,proposed_connector_success=proposed_return),indent=2))


if __name__=='__main__':main()
