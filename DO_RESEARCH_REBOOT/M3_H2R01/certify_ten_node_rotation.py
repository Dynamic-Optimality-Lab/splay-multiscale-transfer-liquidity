"""Source-original primitive identity on the ten-node core plus gap-0 kernel."""
import sys,json,time,itertools,hashlib
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BState,b_single_rot,crank
OUT=Path('DO_RESEARCH_REBOOT/M3_H2R01/ten_node_rotation_certificate.json')
FIELDS=('kl','rl','kr','rr','lo','hi');NODES=tuple(range(10))
def reflexive(d,n):
    k,t,a,z=d.nodes[n]
    if k=='const' and t==BOOL:return bool(z)
    if k=='eq':return a[0]==a[1]
    if k=='and':return reflexive(d,a[0]) and reflexive(d,a[1])
    return False
def main():
    assert not OUT.exists();start=time.process_time();d=DAG();b=BState(d,'S')
    x=d.var_int('x',5);p=d.var_int('p',5);g=d.var_int('g',5)
    sx=d.var_bool('sx');sp=d.var_bool('sp');pr=d.var_bool('pr')
    out=b_single_rot(d,b,x,p,g,sp,sx,pr);base=list(d.nodes);tab=dict(d.tab);rows=[]
    for xx,pp in itertools.permutations(NODES,2):
        for gg in (19,)+tuple(i for i in NODES if i not in (xx,pp)):
            if gg!=19 and ((crank(xx)<crank(gg))!=(crank(pp)<crank(gg))):continue
            assert time.process_time()-start<120,'UNKNOWN: ten-node primitive cap'
            side=crank(xx)>crank(pp);gp_side=gg!=19 and crank(pp)>crank(gg)
            pins={'x':xx,'p':pp,'g':gg,'sx':side,'sp':gp_side,'pr':gg==19}
            expected={f:list(getattr(b,f)) for f in FIELDS};zk=d.const_int(0,2)
            if side:
                expected['kr'][pp]=b.kl[xx];expected['rr'][pp]=b.rl[xx]
                expected['kl'][xx]=zk;expected['rl'][xx]=d.const_int(pp,5)
            else:
                expected['kl'][pp]=b.kr[xx];expected['rl'][pp]=b.rr[xx]
                expected['kr'][xx]=zk;expected['rr'][xx]=d.const_int(pp,5)
            if gg!=19:
                k,r=('kr','rr') if gp_side else ('kl','rl')
                expected[k][gg]=zk;expected[r][gg]=d.const_int(xx,5)
            root=d.const_int(xx,5) if gg==19 else b.root
            eq=[d.EQ(out.root,root)]
            eq.extend(d.EQ(u,v) for f in FIELDS for u,v in zip(getattr(out,f),expected[f]))
            reduced=d.simplify(d.AND(*eq),pins);assert reflexive(d,reduced),pins
            rows.append({'pins':pins,'all_115_fields_reflexive':True,
                         'pins_sha256':hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest()})
            d.nodes=list(base);d.tab=dict(tab)
    assert len(rows)==570
    result={'status':'COMPLETE','cases':len(rows),'fields_per_case':115,
            'production_DAG_nodes':len(base),'source_fields_unfixed':True,
            'node_order_by_crank':[9,0,1,2,3,4,5,6,7,8],
            'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
