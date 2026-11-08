"""Independent endpoint-driven complete saturated H2 retirement check.
Does not use the producer's two target rows; enumerates every actual
fringe target at depth3/4 and tests actual retirement with a zipper kernel.
"""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
from audit_verify36 import calc,mirror
from audit_verify37 import renumber
from interior_projection_source_tools import fr,isnode,scale,known
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def rotation(t,left):
    k,A,Bb=t
    if left:q,C,D=Bb;return q,(k,A,C),D
    q,C,D=A;return q,C,(k,D,Bb)
def fringe(t,p,j,side):
    if not isnode(t):return t
    if t[0]==p:
        f=t[1 if side=='L' else 2];assert f[0]==j and f[2 if side=='L' else 1]=='E'
        return (j,f[1],fringe(t[2],p,j,side)) if side=='L' else (j,fringe(t[1],p,j,side),f[2])
    return t[0],fringe(t[1],p,j,side),fringe(t[2],p,j,side)
def main():
    # Complete p-involved primitive cases when p is the least path key.
    p,j,g=3,2,6
    primitive=[((p,(j,'A','E'),(g,'B','C')),True),((g,(p,(j,'A','E'),'B'),'C'),False)]
    for t,left in primitive:
        assert fringe(rotation(t,left),p,j,'L')==rotation(fringe(t,p,j,'L'),left)
        mt=mirror(t,20);assert fringe(rotation(mt,not left),20-p,20-j,'R')==rotation(fringe(mt,20-p,20-j,'R'),not left)
    Z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,Z['trees']));N=len(T);idx={t:i for i,t in enumerate(T)};mir=Z['mirror'];raw=(B/'native10_debt_03.pkl').read_bytes();oldpin=json.loads((B/'native10_complete_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==oldpin['input_sha256'];saved=pickle.loads(raw);L=saved['level'];assert not saved['queue'] and len(L)==1769616;del raw,saved
    cache=collections.OrderedDict();cacheframes=0;formal_checks=0;retired_forms=0
    def at(t,key):
        d=0
        while t[0]!=key:t=t[1 if key<t[0] else 2];d+=1
        return t,d
    def drop(t,p):
        if not isnode(t):return t
        if t[0]==p:
            assert not isnode(t[1]) or not isnode(t[2])
            return t[1] if isnode(t[1]) else t[2]
        return t[0],drop(t[1],p),drop(t[2],p)
    def forms(a):
        nonlocal cacheframes,formal_checks,retired_forms
        if a in cache:cache.move_to_end(a);return cache[a]
        original=scale(T[a]);answer=[]
        for side,child,opposite in (('L',1,2),('R',2,1)):
            parents=[original];v=original[child];path=[child]
            while isnode(v) and len(path)<=3:
                if isnode(v[opposite]):
                    j=v[0]//2;p=2*j+(1 if side=='L' else -1);branch=(p,(2*j,v[1],'E'),v[2]) if side=='L' else (p,v[1],(2*j,'E',v[2]));As=branch
                    for parent,direction in reversed(list(zip(parents,path))):As=(parent[0],As,parent[2]) if direction==1 else (parent[0],parent[1],As)
                    assert idx[renumber(fringe(As,p,2*j,side))]==a
                    for x in range(1,11):
                        if not ((2*x<p) if side=='L' else (2*x>p)):continue
                        _,depth=at(As,2*x)
                        if depth not in (3,4):continue
                        after,h=calc(As,2*x);formal_checks+=1;assert h==2
                        pp,_=at(after,p)
                        if isnode(pp[1]) and isnode(pp[2]):continue
                        target=idx[renumber(drop(after,p))];answer.append((x,target,p,j,side,len(path)));retired_forms+=1
                parents.append(v);v=v[child];path=path+[child]
        cache[a]=answer;cacheframes+=len(answer)
        if len(cache)>1024:_,old=cache.popitem(last=False);cacheframes-=len(old)
        assert len(L)+3*N+cacheframes+len(cache)<1850000
        return answer
    qmax=[max(r) for r in Z['Q']];automatic=checked=records=0;worst=100
    for code,d in L.items():
        records+=1;a,b=divmod(code,N)
        if d<=4-qmax[b]:automatic+=1;continue
        for x,target,p,j,side,depth in forms(a):
            q=Z['Q'][b][x-1];price=4-q
            if d<=price:continue
            bt=Z['destination'][b][x-1];dt=L.get(min(target*N+bt,mir[target]*N+mir[bt]),0);margin=price+dt-d;assert margin>=0;worst=min(worst,margin);checked+=1
        if records%16384==0 and time.process_time()-START>CAP-2:raise TimeoutError('SATURATED_H2_COMPLETE_AUDIT_CAP')
    producer=json.loads((B/'saturated_H2_retirement_work_01.json').read_text());assert producer['complete'] and producer['counter'] is None and records==producer['cursor']==1769616 and automatic==producer['automatic_positive_records']==1734298 and checked==producer['explicit_retirement_couplings']==1182
    files=('SATURATED_NONFRINGE_SPLAY.md','SATURATED_DIRECT_H2_RETIREMENT.md','saturated_H2_retirement_work_01.json','audit_verify73.py','native10_complete_independent_audit.json','native10_source_independent_audit.json')
    result={'status':'PASS_FIXED_TEN_DIRECT_H2_SATURATED_RETIREMENT_SIGNED_THEOREM','old_nonzero_source_coefficients_checked':records,'implicit_zero_source_cases':'automatic since Q<=4, actual H2 and Dtarget>=0','joint_reflection_coverage':'both L/R forms checked on every canonical source; accepted D10 and source mirror symmetry reused','automatic_positive_records':automatic,'nontrivial_signed_retirement_couplings':checked,'minimum_nontrivial_margin':worst,'independent_formal_actual_source_accesses':formal_checks,'retirement_forms_generated':retired_forms,'target_enumeration':'every old fringe target at actual depth3/4; endpoint retirement tested after the actual zipper splay, not producer target rows','nonfringe_uniform_theorem':'four generic primitive equations plus written path/rotation induction; arbitrary support and depth, one active private fringe','numerical_signed_scope':'fixed ten-anchor full B, one active saturated anonymous path branch that retires; arbitrary consistently projected inactive terms','not_all_LOW_coverage':True,'not_all_r_signed_funding':True,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}}
    assert time.process_time()-START<CAP-1
    out('saturated_direct_H2_retirement_independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify73_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
