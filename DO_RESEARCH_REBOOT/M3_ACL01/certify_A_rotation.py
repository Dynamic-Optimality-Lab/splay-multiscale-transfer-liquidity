"""Original A.single_rot parametric identity with all 509 state fields free."""
import sys,json,time,itertools
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG,BOOL
from PC_ROTATION_INTERPRETER import AState,single_rot
from PC_STRUCTURAL_WITNESS import NSLOT,NULL_REF
OUT=Path('DO_RESEARCH_REBOOT/M3_ACL01/A_rotation_certificate.json')
def reflexive(d,n):
    k,t,a,z=d.nodes[n]
    if k=='const' and t==BOOL:return bool(z)
    if k=='eq':return a[0]==a[1]
    if k=='and':return reflexive(d,a[0]) and reflexive(d,a[1])
    return False
def main():
    assert not OUT.exists();start=time.process_time();d=DAG();s=AState.__new__(AState);s.d=d
    s.root=d.var_int('Sroot',7)
    for f in ('kl','rl','kr','rr'):setattr(s,f,[d.var_int(f'S{f}{i}',8) for i in range(NSLOT)])
    x=d.var_int('x',7);p=d.var_int('p',7);g=d.var_int('g',7)
    sx=d.var_bool('sx');sp=d.var_bool('sp');pr=d.var_bool('pr')
    out=single_rot(d,s,x,p,g,sp,sx,pr);base=list(d.nodes);tab=dict(d.tab);rows=[]
    for side,gside,rootflag in itertools.product((False,True),repeat=3):
        pins={'x':0,'p':1,'g':NULL_REF if rootflag else 2,'sx':side,'sp':gside,'pr':rootflag}
        expect={f:list(getattr(s,f)) for f in ('kl','rl','kr','rr')}
        if side:
            expect['kr'][1]=s.kl[0];expect['rr'][1]=s.rl[0];expect['kl'][0]=d.const_int(0,2);expect['rl'][0]=d.const_int(1,7)
        else:
            expect['kl'][1]=s.kr[0];expect['rl'][1]=s.rr[0];expect['kr'][0]=d.const_int(0,2);expect['rr'][0]=d.const_int(1,7)
        if not rootflag:
            k,r=('kr','rr') if gside else ('kl','rl');expect[k][2]=d.const_int(0,2);expect[r][2]=d.const_int(0,7)
        eroot=d.const_int(0,7) if rootflag else s.root
        eq=[d.EQ(out.root,eroot)]+[d.EQ(a,b) for f in expect for a,b in zip(getattr(out,f),expect[f])]
        assert reflexive(d,d.simplify(d.AND(*eq),pins)),pins
        rows.append({'pins':pins,'all_509_fields_reflexive':True});d.nodes=list(base);d.tab=dict(tab)
        assert time.process_time()-start<120
    result={'status':'FINITE_EXACT_VERIFIED','cases':len(rows),'fields_per_case':509,
      'production_DAG_nodes':len(base),'source_state_fields_unfixed':True,
      'representative_indices':[0,1,2],'arbitrary_indices':'requires the source index-renaming lemma in report',
      'rows':rows,'cpu_seconds':round(time.process_time()-start,3)}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
