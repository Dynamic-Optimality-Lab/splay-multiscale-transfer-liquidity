"""Exact root-lift source recurrence and bounded inherited-control audit."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
s=importlib.util.spec_from_file_location('boundary_lift_original_tuple',ROOT/'python/independent/splay.py')
tu=importlib.util.module_from_spec(s);s.loader.exec_module(tu)


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,d):
    with (HERE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def N(k,l=None,r=None):return [k,l,r]
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
def path(t,x):
    nodes=[];dirs=[]
    while isinstance(t,list):
        nodes.append(t)
        if t[0]==x:return nodes,dirs
        d='L' if x<t[0] else 'R';dirs.append(d);t=t[1 if d=='L' else 2]
    raise AssertionError('present explicit key')
def common(a,b):
    if isinstance(a,str) and a==b:return {a}
    if isinstance(a,list) and isinstance(b,list) and a[0]==b[0]:
        return {a[0]}|common(a[1],b[1])|common(a[2],b[2])
    return set()
def serial(v):return sorted(v,key=lambda z:(isinstance(z,str),str(z)))


def boundary(a,b,x):
    h=0
    while isinstance(a,list) and isinstance(b,list) and a[0]==b[0]:
        if a[0]==x:return dict(kind='common_target',h=h,body_A=a,body_B=b)
        side=1 if x<a[0] else 2;a,b=a[side],b[side];h+=1
    return dict(kind='disagreement_interval',h=h,body_A=a,body_B=b)


def lift(source_g,R,x,u):
    g=source_g[0];t='L' if x<g else 'R'
    p=source_g[1 if t=='L' else 2]
    inner=None if u==0 else ('L' if x<p[0] else 'R')
    correction=u%2==1 and t==inner
    if t=='L':
        base=N(x,R[1],N(g,R[2],source_g[2]));ans=base
        if correction:
            q=base[2];pivot=q[1];assert pivot[0]==p[0]
            ans=N(x,base[1],N(pivot[0],pivot[1],N(g,pivot[2],q[2])))
    else:
        base=N(x,N(g,source_g[1],R[1]),R[2]);ans=base
        if correction:
            q=base[1];pivot=q[2];assert pivot[0]==p[0]
            ans=N(x,N(pivot[0],N(g,q[1],pivot[1]),pivot[2]),base[2])
    return ans,dict(outer_direction=t,original_internal_depth=u,internal_parity=u%2,
        original_child_root=p[0],first_inner_direction=inner,comparison_correction=correction,
        base_lift=base,result=ans)


def analyze(a,b,x,eventsA=None,eventsB=None):
    q=boundary(a,b,x);h=q['h'];na,da=path(a,x);nb,db=path(b,x)
    uA=len(da)-h;uB=len(db)-h
    RA,_=splay(q['body_A'],x);RB,_=splay(q['body_B'],x)
    levels=[]
    for j in range(h-1,-1,-1):
        RA,la=lift(na[j],RA,x,len(da)-j-1)
        RB,lb=lift(nb[j],RB,x,len(db)-j-1)
        ca=(na[j][0],la['original_child_root'],la['outer_direction']) if la['comparison_correction'] else None
        cb=(nb[j][0],lb['original_child_root'],lb['outer_direction']) if lb['comparison_correction'] else None
        for v,ev,depth in ((la,eventsA,len(da)),(lb,eventsB,len(db))):
            v['source_double_event_index']=None
            if v['comparison_correction']:
                idx=(depth-j-2)//2;v['source_double_event_index']=idx
                if ev is not None:assert ev[idx][0]==v['outer_direction']*2
        levels.append(dict(external_source_index=j,external_key=na[j][0],A=la,B=lb,
            asymmetric_named_correction=ca!=cb))
    fullA,ae=splay(a,x);fullB,be=splay(b,x)
    before=common(a,b);after=common(fullA,fullB)
    asymmetric=[v for v in levels if v['asymmetric_named_correction']]
    if q['kind']=='common_target' or h==0:pred=True
    elif uA%2==uB%2==0:pred=True
    elif uA%2==uB%2==1:
        pred=not levels[0]['A']['comparison_correction'] and not levels[0]['B']['comparison_correction']
    else:
        odd=levels[0]['A'] if uA%2 else levels[0]['B']
        pred=not odd['comparison_correction'] and all(da[j]!=da[j+1] for j in range(h-1))
    witness=min(asymmetric,key=lambda z:z['external_source_index'])['external_key'] if asymmetric else None
    return dict(kind=q['kind'],external_depth=h,external_directions=da[:h],internal_depth_A=uA,
        internal_depth_B=uB,parity_pair=[uA%2,uB%2],levels=levels,
        predicted_retention=pred,correction_congruence=not asymmetric,
        actual_retention=before<=after,old_common=serial(before),new_common=serial(after),
        evicted=serial(before-after),source_witness=witness,
        witness_actually_evicted=witness in before-after if witness is not None else None,
        recurrence_exact=(RA==fullA and RB==fullB),recurrence_output_A=RA,recurrence_output_B=RB,
        actual_A_events=ae,actual_B_events=be)


def primitives():
    A,B,C,D='A','B','C','D'
    src={
        'LL':(N(3,N(2,N(1,A,B),C),D),1),
        'RR':(N(1,A,N(2,B,N(3,C,D))),3),
        'LR':(N(3,N(1,A,N(2,B,C)),D),2),
        'RL':(N(1,A,N(3,N(2,B,C),D)),2),
        'ZIG_L':(N(2,N(1,A,B),C),1),
        'ZIG_R':(N(1,A,N(2,B,C)),2)}
    out={}
    for case,(t,x) in src.items():
        nodes,ds=path(t,x);body=t[1 if ds[0]=='L' else 2]
        R,_=splay(body,x);v,info=lift(t,R,x,len(ds)-1);full,ev=splay(t,x)
        assert v==full
        assert info['comparison_correction']==(case in ['LL','RR'])
        out[case]=dict(source=t,key=x,local_splay=R,lift=info,full=full,events=ev)
    return out


def main():
    pg=BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json'
    ad=BASE/'route_c_fe02_approach_discharge_20261101_v001/closed_discharge_certificate.json'
    ui=BASE/'route_c_fe02_unequal_interval_escape_20261101_v001/odd_boundary_obstruction_certificate.json'
    ore=BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json'
    p,a,u,o=read(pg),read(ad),read(ui),read(ore)
    corpora={f'W_{k}':p[k] for k in ['ordinary_rows','reflected_rows','startup_rows']}
    corpora.update({f'AD_{k}':v['rows'] for k,v in a['cases'].items()})
    corpora.update({f'OR_{k}':o[k] for k in ['rows','reflected_rows','symbolic_rows']})
    corpora['UI_closed']=u['physical_closed_rows']
    corpora['UI_symbolic_edge']=[u['saturated_row']]
    out={};errors=[];safe_nonneg=unsafe_nonneg=0;parities={}
    for name,rs in corpora.items():
        selected=[]
        for r in rs:
            if r['mode']!='KEEP' or r['a']==0:continue
            v=analyze(r['source_A'],r['source_B'],r['key'],r['A_events'],r['B_events'])
            if not v['recurrence_exact'] or v['predicted_retention']!=v['actual_retention'] or v['correction_congruence']!=v['predicted_retention'] or (v['source_witness'] is not None and not v['witness_actually_evicted']):
                errors.append(dict(corpus=name,occurrence=r['occurrence'],analysis=v,row=r))
            par=','.join(map(str,v['parity_pair']));parities[par]=parities.get(par,0)+1
            if r.get('delta',r['q']-2*r['a'])>=0:
                if v['predicted_retention']:safe_nonneg+=1
                else:unsafe_nonneg+=1
            selected.append(dict(row=r,analysis=v))
        out[name]=selected
    result=dict(status='PASS' if not errors else 'EXACT_SCOPED_DISCREPANCY',
        gate_sha256=sha(HERE/'BL00_FOUR_RULE_GATE.md'),primitive_lifts=primitives(),corpora=out,
        discrepancies=errors,total_fixed_rows=sum(len(v) for v in out.values()),
        source_parity_counts=parities,safe_nonnegative=safe_nonneg,unsafe_nonnegative=unsafe_nonneg,
        source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [pg,ad,ui,ore]},
        all_size_proof='root-lift identity, induction, and source parity classification; not a finite h sweep',
        comparison_rotations_are_not_extra_physical_units=True,larger_finite_fits=0,FE02_CD='OPEN')
    save('boundary_lift_source_certificate.json',result)
    print(json.dumps({k:result[k] for k in ['status','total_fixed_rows','source_parity_counts','safe_nonnegative','unsafe_nonnegative','FE02_CD']},indent=2))


if __name__=='__main__':main()
