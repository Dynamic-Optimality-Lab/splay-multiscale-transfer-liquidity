"""Independent low primitive semantics and complete interface-name audit."""
import sys,json,time,itertools
from pathlib import Path
P='DO_RESEARCH_REBOOT/06_CERTIFICATES/'
sys.path[:0]=[P+'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',P+'DIRECT_CDK5N_11F_STRICT_CLOSURE',
             P+'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE',P+'DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS']
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BState,b_single_rot,crank
from STRICT_LOW_COMPILER import StateVars7
from STRICT_HIGH_COMPILER import FiberVars7
from CW_PRODUCT_COMPILER import state_suffixes7,fiber_suffixes
from S03_RELATION_SCOPE_COMPILER import project_edge
BASE=Path('DO_RESEARCH_REBOOT/M3_COMB_AUD01')
FIELDS=('kl','rl','kr','rr','lo','hi')

def main():
    output=BASE/'primitive_interface_audit.json';assert not output.exists();start=time.process_time()
    d=DAG();b=BState(d,'S');x=d.var_int('x',5);p=d.var_int('p',5);g=d.var_int('g',5)
    sx=d.var_bool('sx');sp=d.var_bool('sp');pr=d.var_bool('pr')
    out=b_single_rot(d,b,x,p,g,sp,sx,pr);nodes=list(d.nodes);tab=dict(d.tab);core_cases=0
    for xx,pp in itertools.permutations(range(9),2):
        for gg in [19]+[a for a in range(9) if a not in (xx,pp)]:
            if gg!=19 and (xx<gg)!=(pp<gg):continue
            side=xx>pp;root=gg==19;pins={'x':xx,'p':pp,'g':gg,'sx':side,'sp':not root and pp>gg,'pr':root}
            expected={f:list(getattr(b,f)) for f in FIELDS};mid='l' if side else 'r';pfield='kr' if side else 'kl';prfield='rr' if side else 'rl'
            expected[pfield][pp]=getattr(b,'k'+mid)[xx];expected[prfield][pp]=getattr(b,'r'+mid)[xx]
            xf='kl' if side else 'kr';xr='rl' if side else 'rr';expected[xf][xx]=d.const_int(0,2);expected[xr][xx]=d.const_int(pp,5)
            if not root:
                gf='kr' if pp>gg else 'kl';gr='rr' if pp>gg else 'rl';expected[gf][gg]=d.const_int(0,2);expected[gr][gg]=d.const_int(xx,5)
            for f in FIELDS:
                for actual,wanted in zip(getattr(out,f),expected[f]):assert d.simplify(actual,pins)==wanted,(xx,pp,gg,f)
            assert d.simplify(out.root,pins)==(d.const_int(xx,5) if root else b.root)
            core_cases+=1;d.nodes=list(nodes);d.tab=dict(tab)
    assert core_cases==408
    max_cases=0
    for xx,pp in itertools.permutations(range(18),2):
        for gg in [19]+[a for a in range(18) if a not in (xx,pp)]:
            if gg!=19 and (crank(xx)<crank(gg))!=(crank(pp)<crank(gg)):continue
            pins={'x':xx,'p':pp,'g':gg,'sx':crank(xx)>crank(pp),'sp':gg!=19 and crank(pp)>crank(gg),'pr':gg==19}
            assert d.simplify(out.kr[8],pins)==b.kr[8] and d.simplify(out.rr[8],pins)==b.rr[8]
            max_cases+=1;d.nodes=list(nodes);d.tab=dict(tab)
    assert max_cases==3570
    q=DAG();s=StateVars7(q,'QO');t=StateVars7(q,'QO2');m=FiberVars7(q,'QM')
    def name(n):return q.nodes[n][3][1]
    def bn(b):return [b.root]+[n for f in FIELDS for n in getattr(b,f)]
    def on(o):return {name(n) for n in [o.mu]+o.sig+o.ak+o.aS+o.aI+bn(o.b)}
    def mn(o):return {name(n) for n in [o.mu,o.v]+o.sig+bn(o.b)}
    source,destination,mid=on(s),on(t),mn(m)
    assert source==set(state_suffixes7('QO')) and destination==set(state_suffixes7('QO2'))
    assert mid==set(fiber_suffixes('QM')) and len(source)==len(destination)==147 and len(mid)==127
    # Reconstruct scope patterns over ALL actual coordinates, then check lexical free vars.
    private=q.var_int('audit_private_witness',5)
    atom=q.AND(*[q.EQ(q.vars[n],q.vars[n]) for n in source|destination|mid],q.EQ(private,private))
    # EQ(v,v) simplifies immediately; use an unconstrained independent comparison instead.
    atom=q.AND(*[q.LT(q.vars[n],q.const_int(31,5)) if q.nodes[q.vars[n]][1]!=BOOL else q.vars[n]
                 for n in source|destination|mid],q.LT(private,q.const_int(31,5)))
    from functools import lru_cache
    @lru_cache(None)
    def free(n):
        k,typ,args,extra=q.nodes[n]
        if k=='var':return frozenset([extra[1]])
        names=frozenset().union(*(free(a) for a in args))
        return names-frozenset(extra) if k=='exists' else names
    scope=[]
    for label,body,keep,wanted in [
        ('OO',atom,('QO',),source|destination),
        ('OM',q.EXISTS(tuple(sorted(destination)),atom),('QO','QM'),source|mid),
        ('MO',q.EXISTS(tuple(sorted(source)),atom),('QM','QO2'),destination|mid)]:
        projected,_=project_edge(q,body,keep);actual=set(free(projected));assert actual==wanted,(label,actual^wanted)
        scope.append({'sort':label,'lexical_free_coordinate_count':len(actual),'private_witness_free':False})
    result={'status':'PASS_INDEPENDENT_PRIMITIVES_AND_INTERFACE_SCOPE',
            'core_rotation_cases_all115_fields':core_cases,'maximum_pair_identities':max_cases,
            'ordinary_coordinate_count':147,'midpoint_coordinate_count':127,
            'raw_interval_coordinates_in_interface':True,'alpha_unused_fields_in_interface':True,
            'scope_pattern_checks':scope,'scope_kind':'actual interface fields with source-equivalent existential patterns',
            'full_Product_instantiation':'not required; low/high roots audited separately',
            'production_rotation_DAG_nodes':len(nodes),'cpu_seconds':round(time.process_time()-start,3)}
    assert result['cpu_seconds']<120
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
