"""Fixed exact source reset certificate and inherited one-sided LCA audit."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
s=importlib.util.spec_from_file_location('turn_reset_original_tuple',ROOT/'python/independent/splay.py')
tu=importlib.util.module_from_spec(s);s.loader.exec_module(tu)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,d):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def N(k,l=None,r=None):return [k,l,r]
def vine(keys):
    t=None
    for x in reversed(list(keys)):t=N(x,None,t)
    return t
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
def depth(t,x):return len(path(t,x)[1])
def keys(t):return [] if not isinstance(t,list) else keys(t[1])+[t[0]]+keys(t[2])
def reflect(t,n):
    return None if t is None else N(n+1-t[0],reflect(t[2],n),reflect(t[1],n))
def opaque(t,n,prefix):
    gap=0
    def go(t):
        nonlocal gap
        if t is None:
            tag=prefix+str(gap);gap+=1;return tag
        return N(t[0],go(t[1]),go(t[2]))
    v=go(t);assert gap==n+1;return v
def execute(A,B,word):
    out=[]
    for i,(mode,x) in enumerate(word):
        da=depth(A,x);aa,ae=splay(A,x)
        if mode=='KEEP':db=depth(B,x);bb,be=splay(B,x)
        else:db=None;bb=B;be=[]
        q=sum(e[0]!='ZIG' for e in be)
        out.append(dict(occurrence=i,mode=mode,key=x,source_A=A,source_B=B,destination_A=aa,
            destination_B=bb,d_A=da,d_B=db,a=len(ae),q=q,z=sum(e[0]=='ZIG' for e in be),
            delta=q-2*len(ae),A_events=ae,B_events=be))
        A,B=aa,bb
    return out


def update(T,g,x,side,active=True):
    h=depth(T,g)
    if not active:return dict(applied=False,h=h,j=0,e=0,predicted_h=h,actual_h=h)
    spine='L' if side=='R' else 'R';ng,dg=path(T,g);nx,dx=path(T,x)
    assert all(d==spine for d in dg)
    j=0
    while j<len(dx) and dx[j]==spine:j+=1
    on_spine=j==len(dx)
    if on_spine:e=0
    else:
        local=len(dx)-j
        e=1 if local%2 else (2 if dx[j]==dx[j+1] else 1)
    predicted=h-j+e;result,_=splay(T,x);actual=depth(result,g)
    assert predicted==actual
    return dict(applied=True,h=h,j=j,e=e,predicted_h=predicted,actual_h=actual,
        source_anchor_path=[n[0] for n in ng],source_target_path=[n[0] for n in nx],
        source_LCA_key=nx[j][0],target_on_anchor_spine=on_spine,
        residual_anchor_depth=h-j,near_anchor=j>=h-1)


def phase_audit(rows,g):
    M=len(rows);hits=[i for i,r in enumerate(rows) if r['key']==g];out=[]
    for n,i in enumerate(hits):
        j=hits[(n+1)%len(hits)];length=(j-i)%M or M
        ids=[(i+t)%M for t in range(1,length+1)];internal=ids[:-1]
        if not internal:continue
        roots=[rows[k]['key'] for k in internal]
        side='R' if all(x>g for x in roots) else 'L' if all(x<g for x in roots) else None
        startA,startB=rows[i]['destination_A'],rows[i]['destination_B']
        if side is None or startA[0]!=g or startB[0]!=g:continue
        updates=[]
        for k in internal:
            r=rows[k];a=update(r['source_A'],g,r['key'],side)
            b=update(r['source_B'],g,r['key'],side,r['mode']=='KEEP')
            before=2*a['h']-b['h'];after=2*a['actual_h']-b['actual_h']
            assert after==before-2*a['j']+b['j']+2*a['e']-b['e']
            updates.append(dict(block=k,A=a,B=b,D_before=before,D_after=after,row=r))
        ret=rows[j];hA=depth(ret['source_A'],g);hB=depth(ret['source_B'],g)
        entry=dict(anchor=g,start_after=i,return_block=j,indices=ids,internal_keys=roots,side=side,
            updates=updates,return_row=ret,return_depth_A=hA,return_depth_B=hB)
        if ret['mode']=='KEEP':
            D=2*hA-hB;reserve=(hA%2)+(D+1)//2
            assert reserve==2*ret['a']-ret['q']
            final=updates[-1]
            qualified=final['B']['applied'] and final['B']['predicted_h']<=3
            if qualified:assert ret['q']<=1 and ret['delta']<=-1
            entry.update(D_return=D,exact_signed_reserve=reserve,qualifying_final_reset=qualified,
                near_anchor_final_branch=final['B']['applied'] and final['B'].get('near_anchor',False))
        out.append(entry)
    return out


def main():
    U=N(6,None,N(7,None,N(8)))
    inner=N(3,None,N(4,None,N(5,None,N(9,U))))
    low=N(2,None,N(10,inner))
    B=N(1,None,N(11,low,vine(range(12,17))))
    A=N(1,None,N(16,N(10,N(9,N(8,vine(range(2,8)))),vine(range(11,16)))))
    assert keys(A)==keys(B)==list(range(1,17))
    word=[('KEEP',x) for x in [16,10,9,8,1]]
    rs=execute(A,B,word)
    assert [(r['a'],r['q']) for r in rs]==[(1,3),(1,2),(1,2),(1,2),(1,2)]
    assert B[2][0]==11 and rs[-1]['destination_B'][2][0]==5
    trajectories=[]
    for r in rs[:-1]:
        aa=update(r['source_A'],1,r['key'],'R');bb=update(r['source_B'],1,r['key'],'R')
        trajectories.append(dict(row=r,A=aa,B=bb,D_before=2*aa['h']-bb['h'],D_after=2*aa['actual_h']-bb['actual_h']))
    assert [v['B']['actual_h'] for v in trajectories]==[2,2,3,4]
    assert [v['D_after'] for v in trajectories]==[0,0,-1,-2]
    symbolic=execute(opaque(A,16,'A_F'),opaque(B,16,'B_F'),word)
    reflected=execute(reflect(A,16),reflect(B,16),[('KEEP',17-x) for _,x in word])
    assert [(r['a'],r['q']) for r in symbolic]==[(r['a'],r['q']) for r in reflected]==[(r['a'],r['q']) for r in rs]
    units=[[i,e,b] for i,r in enumerate(rs) for e in range(r['a']) for b in(0,1)]
    demands=[[i,e] for i,r in enumerate(rs) for e,z in enumerate(r['B_events']) if z[0]!='ZIG']
    assert len(units)==10 and len(demands)==11
    counter=dict(status='EXACT_VALID_SOURCE_INWARD_RESET_WITHOUT_SPARE',gate_sha256=sha(HERE/'TR00_FOUR_RULE_GATE.md'),
        source_A=A,source_B=B,word=word,rows=rs,symbolic_rows=symbolic,reflected_rows=reflected,
        anchor=1,initial_B_child=11,final_B_child=5,strict_approaching_internal_roots=[16,10,9,8],
        source_trajectories=trajectories,A_steps=5,B_double_demands=11,positive_blocks=[0],
        local_physical_units=units,local_B_demands=demands,actual_capacity=10,actual_demand=11,
        no_negative_block=True,return_reserve=0,D_before_return=-2,
        new_exact_symbolic_core_keys=16,opaque_gap_pairs=17,arbitrary_unequal_gap_interiors=True,
        diagonal_reachability='NOT ESTABLISHED; no connector search performed',
        exact_paired_closed_provenance='NOT ESTABLISHED; this episode itself is not closed',
        refuted_scope='unrestricted per-excursion child nondecrease or reset-payment for arbitrary valid paired source trees',
        reachable_closed_FE02_refutation=False,FE02_CD='OPEN',Coarse_Double_counterexample=False,
        numerical_or_size_fit=False)
    save('inward_reset_source_certificate.json',counter)
    ppg=BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json'
    por=BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json'
    pce=BASE/'route_c_fe02_coupled_excursions_20261101_v001/coupled_excursion_control_certificate.json'
    pg,ore,ce=read(ppg),read(por),read(pce)
    corpora={f'W_{k}':pg[k] for k in ['ordinary_rows','reflected_rows']}
    corpora.update({f'OR_{k}':ore[k] for k in ['rows','reflected_rows']})
    corpora.update({f'CE_{k}':ce[k] for k in ['rows','reflected_rows','symbolic_rows']})
    audits={}
    for name,rows in corpora.items():
        g=13 if 'reflected' in name else 1
        audits[name]=phase_audit(rows,g)
    total=sum(len(v['updates']) for ps in audits.values() for v in ps)
    qualifying=[dict(corpus=name,anchor=p['anchor'],return_block=p['return_block'],
        internal_keys=p['internal_keys'],return_type=[p['return_row']['a'],p['return_row']['q']],
        last_helper=p['updates'][-1]['block']) for name,ps in audits.items() for p in ps if p.get('qualifying_final_reset')]
    save('closed_source_LCA_audit_certificate.json',dict(status='PASS',corpora=audits,
        source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [ppg,por,pce]},
        source_updates=total,qualifying_return_contexts=qualifying,
        no_closed_source_writers_rerun=True,larger_finite_fits=0,FE02_CD='OPEN'))
    print(json.dumps(dict(counter_status=counter['status'],core_keys=16,source_B_child=[11,5],
        local_units=10,local_demands=11,reachability='NOT ESTABLISHED',closed_provenance='NOT ESTABLISHED',
        fixed_old_source_updates=total,qualifying_returns=len(qualifying),FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
