"""Exact symbolic conservation of maximum core 8's right pair in low rotations."""
import sys,json,time,hashlib,itertools
from pathlib import Path
from collections import Counter
sys.path.insert(0,'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG
from PC_B_CONTROLLER import BState,b_single_rot,crank
OUT=Path('DO_RESEARCH_REBOOT/M3_PHI01/primitive_certificate.json')

def main():
    assert not OUT.exists()
    d=DAG();b=BState(d,'S')
    x=d.var_int('x',5);p=d.var_int('p',5);g=d.var_int('g',5)
    sx=d.var_bool('sx');sp=d.var_bool('sp');pr=d.var_bool('pr')
    out=b_single_rot(d,b,x,p,g,sp,sx,pr)
    base=list(d.nodes);tab=dict(d.tab);rows=[];roles=Counter();start=time.process_time()
    # All possibly present real nodes when gap 9 is absent; core 8 has maximum rank.
    nodes=list(range(18))
    for xx,pp in itertools.permutations(nodes,2):
        for gg in [19]+[a for a in nodes if a not in (xx,pp)]:
            if gg!=19 and ((crank(xx)<crank(gg))!=(crank(pp)<crank(gg))):continue
            assert time.process_time()-start<120,'UNKNOWN: certificate cap'
            pins={'x':xx,'p':pp,'g':gg,'sx':crank(xx)>crank(pp),
                  'sp':gg!=19 and crank(pp)>crank(gg),'pr':gg==19}
            left=d.simplify(out.kr[8],pins);right=d.simplify(out.rr[8],pins)
            passed=left==b.kr[8] and right==b.rr[8]
            assert passed,(pins,d.nodes[left],d.nodes[right])
            role='X' if xx==8 else 'P' if pp==8 else 'GP' if gg==8 else 'OFF'
            roles[role]+=1
            rows.append({'pins':pins,'role_of_8':role,'kr_reflexive':True,'rr_reflexive':True,
                         'pins_sha256':hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest()})
            d.nodes=list(base);d.tab=dict(tab)
    result={'status':'COMPLETE','cases':len(rows),'roles':dict(roles),
            'unfixed_source_fields':'ALL','production_DAG_nodes':len(base),
            'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
