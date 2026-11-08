"""One inherited deep episode: exact terminal source profile, no fitting."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
OLD=BASE/'route_c_fe02_turn_reset_20261101_v001'
spec=importlib.util.spec_from_file_location('deep_profile_original_tuple',ROOT/'python/independent/splay.py')
tu=importlib.util.module_from_spec(spec);spec.loader.exec_module(tu)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,d):
    with (HERE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return [t[1],jt(t[2]),jt(t[3])]
def path(t,x):
    out=[]
    while isinstance(t,list):
        out.append(t[0])
        if t[0]==x:return out
        t=t[1 if x<t[0] else 2]
    raise AssertionError('present core key')
def edge(A,B,x,mode='KEEP'):
    aa,ae=tu.trace(tt(A),x);ae=[list(v) for v in ae]
    if mode=='KEEP':bb,be=tu.trace(tt(B),x);be=[list(v) for v in be];db=len(path(B,x))-1;bb=jt(bb)
    else:bb=B;be=[];db=None
    a,q=len(ae),sum(v[0]!='ZIG' for v in be)
    return dict(mode=mode,key=x,source_A=A,source_B=B,destination_A=jt(aa),destination_B=bb,
        d_A=len(path(A,x))-1,d_B=db,A_events=ae,B_events=be,a=a,q=q,delta=q-2*a)
def gaps(t,d=0):
    if isinstance(t,str):return {t:d}
    if t is None:return {}
    return gaps(t[1],d+1)|gaps(t[2],d+1)
def body(ascending):
    t=None
    if ascending:
        for k in range(13,7,-1):t=[k,None,t]
    else:
        for k in range(8,14):t=[k,t,None]
    return t
def expand(t,letter):
    if t is None:return None
    if isinstance(t,str):return body(letter=='A') if t==letter+'_F1' else None
    return [7*t[0],expand(t[1],letter),expand(t[2],letter)]
def reflect(t):return None if t is None else [119-t[0],reflect(t[2]),reflect(t[1])]
def run(A,B,word):
    rs=[]
    for i,x in enumerate(word):
        r=edge(A,B,x);r['occurrence']=i;rs.append(r);A,B=r['destination_A'],r['destination_B']
    return rs
def inject(rs,donor):
    out=[]
    for i,r in enumerate(rs):
        units=[[i,e,b] for e in range(r['a']) for b in (0,1)]
        demands=[[i,e] for e,v in enumerate(r['B_events']) if v[0]!='ZIG']
        for j,b in enumerate(demands):
            u=units[j] if j<len(units) else [donor,rs[donor]['a']-1,1]
            out.append(dict(A_unit=u,B_double=b))
    assert len({tuple(v['A_unit']) for v in out})==len(out)
    return dict(assignments=out,donor_block=donor,donor_A_unit=[donor,rs[donor]['a']-1,1],
        positive_B_double=[0,2],capacity=2*sum(r['a'] for r in rs),demands=sum(r['q'] for r in rs),
        closed_source_provenance='NOT ESTABLISHED; injection of actual prefix events, not a new closed witness')


def main():
    old=read(OLD/'inward_reset_source_certificate.json')
    last=old['rows'][-1];A,B=last['destination_A'],last['destination_B']
    core=[edge(A,B,x) for x in range(2,17)]
    sa,sb=old['symbolic_rows'][-1]['destination_A'],old['symbolic_rows'][-1]['destination_B']
    ga,gb=gaps(sa),gaps(sb)
    table=[]
    for i in range(17):
        alpha,beta=ga['A_F'+str(i)],gb['B_F'+str(i)]
        base=[2*((alpha+u+1)//2)-(beta+u)//2 for u in (0,1)]
        table.append(dict(gap=i,alpha=alpha,beta=beta,reserve_u0=base[0],reserve_u1=base[1],
            matched_interior_min_reserve=min(base),recurrence='r(u+2)=r(u)+1',
            unequal_saturation_B_depth='u_B=4*ceil((alpha+u_A)/2)+z_B-beta, z_B in {0,1}'))
    good=all(r['delta']<0 for r in core) and all(r['matched_interior_min_reserve']>=1 for r in table)
    save('terminal_depth_profile_certificate.json',dict(status='PASS' if good else 'FIXED_PREDICTION_FAILED',
        source_certificate_sha256=sha(OLD/'inward_reset_source_certificate.json'),endpoint_A=A,endpoint_B=B,
        symbolic_endpoint_A=sa,symbolic_endpoint_B=sb,core_next_rows=core,gap_table=table,
        all_nonroot_core_queries_negative=all(r['delta']<0 for r in core),
        all_matched_gap_queries_negative=all(r['matched_interior_min_reserve']>=1 for r in table),
        core_size=16,formal_gap_pairs=17,full_FE02_CD='OPEN',larger_finite_fits=0))
    if not good:
        print('Fixed terminal prediction failed; preserved certificate; no alternate template.');return
    injections={str(r['key']):inject(old['rows']+[r],5) for r in core}
    save('core_repayment_injection_certificate.json',dict(status='PASS',injections=injections,
        physical_units='actual original prefix and next-query events; no duplicate unit or invented comparison credit'))
    AA,BB=expand(old['symbolic_rows'][0]['source_A'],'A'),expand(old['symbolic_rows'][0]['source_B'],'B')
    word=[112,70,63,56,7,8]
    rs=run(AA,BB,word);rr=run(reflect(AA),reflect(BB),[119-x for x in word])
    predicted=[(1,3),(1,2),(1,2),(1,2),(1,2),(2,4)]
    match=[(r['a'],r['q']) for r in rs]==[(r['a'],r['q']) for r in rr]==predicted
    save('unequal_gap_escape_certificate.json',dict(status='PASS' if match else 'FIXED_PREDICTION_FAILED',
        gap=1,core_labels='k -> 7*k',gap_labels=list(range(8,14)),core_keys=16,explicit_fringe_keys=6,
        total_explicit_keys=22,template_fixed_in='DC00A_FIXED_UNEQUAL_GAP_TEMPLATE.md',
        A_gap_shape='right vine',B_gap_shape='left vine',same_gap_key_set=True,
        queried_fringe_key=8,u_A=0,u_B=5,alpha=table[1]['alpha'],beta=table[1]['beta'],
        source_A=AA,source_B=BB,word=word,rows=rs,reflected_rows=rr,
        actual_capacity=2*sum(r['a'] for r in rs),actual_demand=sum(r['q'] for r in rs),
        no_negative_block=all(r['delta']>=0 for r in rs),positive_blocks=[i for i,r in enumerate(rs) if r['delta']>0],
        paired_closed=False,diagonal_reachability='NOT ESTABLISHED',
        reachable_closed_FE02_refutation=False,full_FE02_CD='OPEN',Coarse_Double_counterexample=False,
        size_or_coefficient_fit=False,source_graph_or_connector_search=False))
    print(json.dumps(dict(terminal_profile='PASS',negative_core_targets=len(core),positive_gap_minima=len(table),
        unequal_gap_escape='PASS' if match else 'FIXED_PREDICTION_FAILED',
        new_explicit_total_keys=22,capacity=2*sum(r['a'] for r in rs),demand=sum(r['q'] for r in rs),
        full_FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
