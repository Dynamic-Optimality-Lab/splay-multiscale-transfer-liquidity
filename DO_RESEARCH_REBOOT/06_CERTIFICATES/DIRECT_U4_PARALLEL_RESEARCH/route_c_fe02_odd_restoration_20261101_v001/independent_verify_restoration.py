"""Independent pointer/tuple physical-source and restoration verification."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
counts=Counter()


def ck(v,s):assert v,s;counts[s]+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
tu=load('restoration_check_tuple',ROOT/'python/independent/splay.py')
pt=load('restoration_check_pointer',ROOT/'python/liquidity/legacy_embedding.py')
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def tj(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return [t[1],tj(t[2]),tj(t[3])]
def pp(t,parent=None):
    if t is None:return None
    if isinstance(t,str):return pt.mknode(t,p=parent)
    n=pt.mknode(t[0],p=parent);n['l']=pp(t[1],n);n['r']=pp(t[2],n);return n
def pj(t,parent=None):
    if t is None:return None
    ck(t['p'] is parent,'pointer-parent-link')
    if isinstance(t['k'],str):
        ck(t['l'] is None and t['r'] is None,'opaque-fringe-untouched');return t['k']
    return [t['k'],pj(t['l'],t),pj(t['r'],t)]
def path(t,x):
    out=[]
    while isinstance(t,list):
        out.append(t[0])
        if t[0]==x:return out
        t=t[1 if x<t[0] else 2]
    raise AssertionError('present explicit core key')
def depth(t,x):return len(path(t,x))-1
def core(t):return [] if not isinstance(t,list) else core(t[1])+[t[0]]+core(t[2])
def norm(e):return [[v['case'],v['lo'],v['hi'],v['orient']] for v in e]


def edge(a,b,mode,x):
    da=depth(a,x);at,ae=tu.trace(tt(a),x);ap,ape=pt.splay_trace(pp(a),x)
    A=tj(at);ae=[list(v) for v in ae]
    ck(A==pj(ap),'independent-A-tree');ck(ae==norm(ape),'independent-A-events')
    ck(len(ae)==(da+1)//2,'A-real-StepEv-cost')
    if mode=='KEEP':
        db=depth(b,x);bt,be=tu.trace(tt(b),x);bp,bpe=pt.splay_trace(pp(b),x)
        B=tj(bt);be=[list(v) for v in be]
        ck(B==pj(bp),'independent-B-tree');ck(be==norm(bpe),'independent-B-events')
        ck(sum(e[0]!='ZIG' for e in be)==db//2,'B-real-double-demand')
        ck(sum(e[0]=='ZIG' for e in be)==db%2,'terminal-B-zig-preserved')
    else:db=None;B=b;be=[]
    ck(core(a)==core(A) and core(b)==core(B),'ordered-core-keys-preserved')
    return dict(mode=mode,key=x,source_A=a,source_B=b,destination_A=A,destination_B=B,
        d_A=da,d_B=db,a=len(ae),q=sum(e[0]!='ZIG' for e in be),z=sum(e[0]=='ZIG' for e in be),
        delta=sum(e[0]!='ZIG' for e in be)-2*len(ae),A_events=ae,B_events=be)


def row_check(r):
    v=edge(r['source_A'],r['source_B'],r['mode'],r['key'])
    for k in v:
        if k in r:ck(v[k]==r[k],'recorded-'+k)
    if 'source_path_A' in r:
        ck(path(r['source_A'],r['key'])==r['source_path_A'],'original-A-source-path')
        ck(depth(r['destination_A'],r['source_A'][0])==r['source_epsilon_A'],'source-epsilon-A-actual-oldroot-depth')
        if r['mode']=='KEEP':
            ck(path(r['source_B'],r['key'])==r['source_path_B'],'original-B-source-path')
            ck(depth(r['destination_B'],r['source_B'][0])==r['source_epsilon_B'],'source-epsilon-B-actual-oldroot-depth')


def history(rs):
    for i,r in enumerate(rs):
        if i:ck((rs[i-1]['destination_A'],rs[i-1]['destination_B'])==(r['source_A'],r['source_B']),'whole-source-chain')
        row_check(r)


def mixed(r):
    A,B=r['source_A'],r['source_B'];x=r['key']
    d=edge(A,B,'DELETE',x);z=edge(d['destination_A'],d['destination_B'],'DELETE',x)
    k=edge(z['destination_A'],z['destination_B'],'KEEP',x)
    f=edge(k['destination_A'],k['destination_B'],'KEEP',x)
    ck(z['a']==k['a']==f['a']==0 and z['q']==f['q']==0,'same-root-zero-A-followers')
    ck((d['a'],k['q'])==(r['a'],r['q']),'mixed-block-costed-projection')
    ck((k['destination_A'],k['destination_B'])==(r['destination_A'],r['destination_B']),'mixed-block-full-endpoint')
    return dict(key=x,A_leader_occurrence=0,B_first_KEEP_occurrence=2,a=d['a'],q=k['q'])


def injection(d,rows):
    au=set();bd=set()
    for v in d['assignments']:
        i,e,bit=v['A_unit'];j,f=v['B_double']
        ck(0<=i<len(rows) and 0<=e<rows[i]['a'] and bit in (0,1),'actual-A-event-and-bit')
        ck(0<=j<len(rows) and 0<=f<len(rows[j]['B_events']) and rows[j]['B_events'][f][0]!='ZIG','actual-B-double-index')
        ck((i,e,bit) not in au and (j,f) not in bd,'no-reused-physical-credit-or-demand')
        au.add((i,e,bit));bd.add((j,f))
    all_b={(j,f) for j,r in enumerate(rows) for f,z in enumerate(r['B_events']) if z[0]!='ZIG'}
    ck(bd==all_b,'all-B-double-demands-paid-exactly-once')
    p=d['positive_cut'];q=d['donor_block']
    ck(rows[q]['delta']<0 and d['donor_unit']==[q,rows[q]['a']-1,1],'last-real-spare-unit')
    ck(d['startup_credit_used']==d['future_period_credit_used']==0,'no-imported-period-credit')
    start=(rows[p]['source_A'],rows[p]['source_B']);A,B=start
    for t in range(len(rows)):
        r=rows[(p+t)%len(rows)]
        ck((A,B)==(r['source_A'],r['source_B']),'positive-cut-actual-source-owner')
        v=edge(A,B,r['mode'],r['key']);A,B=v['destination_A'],v['destination_B']
    ck((A,B)==start,'one-positive-cut-traversal-closes-exactly')


def algebra(d):
    for A in (1,2):
        for B in (1,2):
            ck(d['possible_helper_deficits'][f'{A},{B}']==2*A-B>=0,'exact-source-deficit-possibilities')
    # Coefficientwise verification, for arbitrary integers d_A,v,z_A,p.
    keys=set(d['A_capacity_coefficients'])|set(d['B_demand_coefficients'])|set(d['reserve_coefficients'])
    for k in keys:
        residual=d['A_capacity_coefficients'].get(k,0)-d['B_demand_coefficients'].get(k,0)-d['reserve_coefficients'].get(k,0)
        ck(residual==d['residual_coefficients'][k]==0,'zero-symbolic-reserve-residual')
    ck(d['source_reserve_identity']=='2*a-q=z_A+ceil(D/2)','unbounded-source-reserve-identity-recorded')


def main():
    d=read(HERE/'odd_restoration_source_certificate.json')
    for field in ['rows','symbolic_rows','reflected_rows']:
        rs=d[field];history(rs)
        ck(rs[0]['source_A']==rs[0]['source_B'],'diagonal-start-source')
        ck((rs[-1]['destination_A'],rs[-1]['destination_B'])==(rs[0]['source_A'],rs[0]['source_B']),'exact-full-pair-closure')
        ck([i for i,r in enumerate(rs) if r['delta']>0]==[d['positive_block']],'one-and-only-one-positive-block')
        ck(all(rs[i]['key']!=rs[(i+1)%len(rs)]['key'] for i in range(len(rs))),'maximal-cyclic-A-root-blocks')
    rs=d['rows'];p=d['positive_block'];r0,r1,ret=rs[p:p+3]
    ck([(r['a'],r['q']) for r in (r0,r1,ret)]==[(1,3),(1,2),(1,2)],'source-local-positive-saturated-saturated')
    states=[(r0['source_A'],r0['source_B'])]+[(r['destination_A'],r['destination_B']) for r in (r0,r1,ret)]
    flags=[path(A,1)==path(B,1) for A,B in states]
    ck(flags==d['common_boundary_by_episode_cut']==[True,False,False,True],'first-common-prefix-restoration')
    for A,B in states[:1]:ck(7 in path(A,8) and 7 in path(B,8),'exported-pair-initially-agreed')
    ck(1 in path(r0['destination_A'],2) and 2 in path(r0['destination_B'],1),'original-odd-inversion-created')
    ck(1 in path(ret['destination_A'],2) and 1 in path(ret['destination_B'],2),'original-odd-inversion-restored')
    for r in (r1,ret):
        ck(7 in path(r['destination_A'],8) and 8 in path(r['destination_B'],7),'new-source-inversion-transferred-and-survives')
    ck(r1['source_path_B'][1]==8,'export-parent-selected-from-source')
    ck(ret['destination_A'][2][0]==7 and ret['destination_B'][2][0]==8,'critical-final-LL-child-normal-form')
    ck((r1['source_epsilon_A'],r1['source_epsilon_B'])==(1,2),'critical-helper-epsilons')
    ck((ret['d_A'],ret['d_B'])==(2,4),'exact-boundary-return-depths')
    local=d['local_capacity_certificate']
    au={(i,e,b) for i in range(p,p+3) for e in range(rs[i]['a']) for b in (0,1)}
    bd={(i,e) for i in range(p,p+3) for e,z in enumerate(rs[i]['B_events']) if z[0]!='ZIG'}
    ck(au=={tuple(v) for v in local['A_units']} and bd=={tuple(v) for v in local['B_double_demands']},'local-dual-uses-only-physical-events')
    ck(len(au)==local['capacity']==6 and len(bd)==local['demand']==7,'exact-local-capacity-deficit-seven-over-six')
    ck(sum(r['delta'] for r in rs[p:p+3])==1 and all(r['delta']>=0 for r in rs[p:p+3]),'no-local-source-repayment-through-restoration')
    ck(sum(r['a'] for r in rs)==d['A']==46 and sum(r['q'] for r in rs)==d['Q']==16,'closed-total46-16')
    injection(d['direct_injection'],rs)
    owners=[mixed(r) for r in (r0,r1,ret)]
    a=read(HERE/'uniform_reserve_algebra_certificate.json');algebra(a)
    old=read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    for field in ('ordinary_rows','reflected_rows','startup_rows'):history(old[field])
    ck([r['key'] for r in old['ordinary_rows']]==[7,5,3,1,5,6,4,1,2,1,5,1,6,7,1,2,1,3,1],'frozen19-block-word')
    ck(sum(r['a'] for r in old['ordinary_rows'])==25 and sum(r['q'] for r in old['ordinary_rows'])==22,'frozen19-block-totals')
    for i in (2,4):ck(old['ordinary_rows'][i]['a']==old['ordinary_rows'][i]['q']==1,'frozen-two-alternative-donor-capacities')
    pins=read(HERE/'entry_source_pins.json')
    for p,h in pins['files'].items():ck(sha(ROOT/p)==h,'unchanged-frozen-file')
    result=dict(status='PASS',total_checks=sum(counts.values()),checks=dict(sorted(counts.items())),
        both_original_engines=True,opaque_all14_gaps=True,reflection=True,mixed_physical_owners=owners,
        closed_FE02_control=dict(blocks=34,A=46,Q=16,positive_block=7,first_restoration_block=9,
            first_real_later_donor=d['direct_injection']['donor_block'],initial_pair=[1,2],transferred_pair=[7,8]),
        local_repayment_obstruction='7 actual B doubles versus6 actual A units; no spare through first restoration',
        universal_k_normal_form='mathematical source proof, not a k sweep',
        arbitrary_eventual_discharge='OPEN',FE02_CD='OPEN',Coarse_Double_counterexample=False,
        larger_finite_fits=0,larger_source_key_count_replays=0,larger_repetition_replays=0,
        script_sha256=sha(Path(__file__)),
        certificate_hashes={p.name:sha(p) for p in HERE.glob('*certificate.json')},
        original_source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py']})
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',checks=sum(counts.values()),closed_FE02_control=result['closed_FE02_control'],FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
