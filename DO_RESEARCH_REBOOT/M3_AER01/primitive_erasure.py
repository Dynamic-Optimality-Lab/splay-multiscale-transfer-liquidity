"""Original single_rot erasure identity for every invalid 8-bit reference."""
import sys,json,time,itertools
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M2_SEP01','DO_RESEARCH_REBOOT/M3_PHI01']
from experiment import D as d,V
from PC_ROTATION_INTERPRETER import AState,single_rot
OUT=Path('DO_RESEARCH_REBOOT/M3_AER01/primitive_erasure.json')
def state(side,gside,rootflag,block,ref):
    s=AState.__new__(AState);s.d=d;s.root=V(1 if rootflag else 2)
    for f in ('kl','kr'):setattr(s,f,[V(2) for _ in range(127)])
    for f in ('rl','rr'):setattr(s,f,[V(255) for _ in range(127)])
    def put(i,right,k,r):getattr(s,'kr' if right else 'kl')[i]=V(k);getattr(s,'rr' if right else 'rl')[i]=V(r)
    put(1,side,0,0)
    if not rootflag:put(2,gside,0,1)
    # Off-path side blocks: x's two children and p's other child.
    loc=((0,False),(0,True),(1,not side))[block];put(*loc,0,ref)
    return s
def erase(s):
    n=AState.__new__(AState);n.d=d;n.root=s.root
    for f in ('kl','rl','kr','rr'):setattr(n,f,list(getattr(s,f)))
    for i in range(127):
        for k,r in (('kl','rl'),('kr','rr')):
            if getattr(n,k)[i].v==0 and getattr(n,r)[i].v>=127:getattr(n,k)[i]=V(2);getattr(n,r)[i]=V(255)
    return n
def raw(s):return (s.root.v,*(tuple(v.v for v in getattr(s,f)) for f in ('kl','rl','kr','rr')))
def main():
    assert not OUT.exists();start=time.process_time();cases=0
    for side,gside,rootflag,block,ref in itertools.product((False,True),(False,True),(False,True),range(3),range(127,256)):
        s=state(side,gside,rootflag,block,ref);args=(V(0),V(1),V(127 if rootflag else 2),V(gside),V(side),V(rootflag))
        assert raw(erase(single_rot(d,s,*args)))==raw(single_rot(d,erase(s),*args))
        cases+=1
        assert time.process_time()-start<120
    result={'status':'FINITE_EXACT_VERIFIED','invalid_ref_values':129,'cases':cases,'fields_per_case':509,
      'both_orientations':True,'both_root_flags':True,'all_three_side_blocks':True,'cpu_seconds':round(time.process_time()-start,3)}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
