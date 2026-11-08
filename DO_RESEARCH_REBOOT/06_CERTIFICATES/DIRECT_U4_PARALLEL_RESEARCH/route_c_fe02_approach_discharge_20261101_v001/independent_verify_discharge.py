"""Read-only certificates; independent original pointer and tuple replays.

No producer import, new-size sweep, recurrence horizon or old output writer.
Opaque nodes represent entire unsearched subtrees, not sample fringes.
"""
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
counts=Counter()


def check(v,tag):
    assert v,tag
    counts[tag]+=1


def load(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


tu=load('audit_original_tuple',ROOT/'python/independent/splay.py')
pt=load('audit_original_pointer',ROOT/'python/liquidity/legacy_embedding.py')


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
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
    check(t['p'] is parent,'pointer-parent-links')
    if isinstance(t['k'],str):
        check(t['l'] is None and t['r'] is None,'opaque-subtree-untouched')
        return t['k']
    return [t['k'],pj(t['l'],t),pj(t['r'],t)]
def dep(t,x):
    d=0
    while t is not None and not isinstance(t,str):
        if t[0]==x:return d
        t=t[1 if x<t[0] else 2];d+=1
    raise AssertionError('key present')
def core(t):
    return [] if t is None or isinstance(t,str) else core(t[1])+[t[0]]+core(t[2])
def norm(ev):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in ev]


def edge(A,B,mode,x):
    at,ae=tu.trace(tt(A),x);ap,aep=pt.splay_trace(pp(A),x)
    ad=tj(at);pa=pj(ap);ae=[list(e) for e in ae]
    check(ad==pa,'independent-A-tree')
    check(ae==norm(aep),'independent-A-events')
    da=dep(A,x)
    check(len(ae)==(da+1)//2,'A-edge-depth-cost')
    if mode=='KEEP':
        bt,be=tu.trace(tt(B),x);bp,bep=pt.splay_trace(pp(B),x)
        bd=tj(bt);pb=pj(bp);be=[list(e) for e in be];db=dep(B,x)
        check(bd==pb,'independent-B-tree')
        check(be==norm(bep),'independent-B-events')
        check(sum(e[0]!='ZIG' for e in be)==db//2,'B-double-edge-depth-cost')
        check(sum(e[0]=='ZIG' for e in be)==db%2,'terminal-zig-kept')
    else:bd=B;be=[];db=None
    check(core(ad)==core(A) and core(bd)==core(B),'ordered-core-preserved')
    return dict(source_A=A,source_B=B,destination_A=ad,destination_B=bd,mode=mode,key=x,
        d_A=da,d_B=db,a=len(ae),q=sum(e[0]!='ZIG' for e in be),
        z=sum(e[0]=='ZIG' for e in be),delta=sum(e[0]!='ZIG' for e in be)-2*len(ae),
        A_events=ae,B_events=be)


def rows_audit(rows):
    for j,r in enumerate(rows):
        if j:
            check(rows[j-1]['destination_A']==r['source_A'] and rows[j-1]['destination_B']==r['source_B'],'history-source-chain')
        v=edge(r['source_A'],r['source_B'],r['mode'],r['key'])
        for k in v:
            if k in r:check(v[k]==r[k],'recorded-'+k)


def gaps(t,d=0):
    if isinstance(t,str):return {t:d}
    if t is None:return {}
    return {**gaps(t[1],d+1),**gaps(t[2],d+1)}


def parity_proof():
    cases=[]
    # Delta G = 2t + Delta zB. Delta E = t - Delta zA.
    # Nonincreasing G bounds t ABOVE, exposure bounds it BELOW;
    # the entire integer interval is examined, with no depth bound.
    for a0,a1,b0,b1 in itertools.product((0,1),repeat=4):
        za,zb=a1-a0,b1-b0
        upper=(-zb)//2;lower=1+za
        for t in range(lower,upper+1):
            case=dict(z_A_before=a0,z_A_after=a1,z_B_before=b0,z_B_after=b1,
                delta_G=2*t+zb,delta_E=t-za)
            check(a0==1 and a1==0 and t==0 and zb in (-1,0),'complete-parity-classification')
            check(case['delta_E']==1,'exposure-increment-exactly-one')
            cases.append(case)
    check(len(cases)==3,'three-exposure-parity-configurations')
    return cases


def mixed_audit(A,B,x):
    # One block: actual A leader DELETE, zero-cost DELETE follower,
    # first KEEP carries all B work, subsequent KEEP is a genuine no-op.
    d=edge(A,B,'DELETE',x)
    f=edge(d['destination_A'],d['destination_B'],'DELETE',x)
    k=edge(f['destination_A'],f['destination_B'],'KEEP',x)
    z=edge(k['destination_A'],k['destination_B'],'KEEP',x)
    c=edge(A,B,'KEEP',x)
    check(f['a']==k['a']==z['a']==0 and f['q']==z['q']==0,'mixed-zero-followers')
    check((d['a'],k['q'])==(c['a'],c['q']),'mixed-costed-projection')
    check(k['destination_A']==c['destination_A'] and k['destination_B']==c['destination_B'],'mixed-endpoint-projection')
    return dict(key=x,A_leader_occurrence=0,B_first_KEEP_occurrence=2,a=d['a'],q=k['q'],
        A_events=d['A_events'],B_events=k['B_events'],same_costed_endpoint=True)


def injection_audit(rows,d):
    us=set();ds=set()
    for a in d['assignments']:
        i,e,bit=a['A_unit'];j,f=a['B_double']
        check(0<=i<len(rows) and 0<=e<len(rows[i]['A_events']) and bit in (0,1),'actual-physical-A-unit')
        check(0<=j<len(rows) and 0<=f<len(rows[j]['B_events']) and rows[j]['B_events'][f][0]!='ZIG','actual-physical-B-demand')
        u=(i,e,bit);v=(j,f)
        check(u not in us and v not in ds,'no-reused-unit-or-demand')
        us.add(u);ds.add(v)
    all_ds={(j,f) for j,r in enumerate(rows) for f,event in enumerate(r['B_events']) if event[0]!='ZIG'}
    check(ds==all_ds,'every-B-double-paid-once')
    p=d['positive_block'];n=d['donor_block']
    check(rows[p]['delta']==1 and rows[n]['delta']<0,'positive-and-donor-source-cost')
    check(d['donor_unit']==[n,rows[n]['a']-1,1],'last-unit-rule')
    check(rows[n]['q']<=2*rows[n]['a']-1,'last-unit-source-available')
    order=d['cut_order'];check(order==[(p+j)%len(rows) for j in range(len(rows))],'one-period-cut-order')
    A,B=rows[p]['source_A'],rows[p]['source_B'];start=(A,B)
    for j in order:
        r=rows[j];check((A,B)==(r['source_A'],r['source_B']),'positive-cut-real-source')
        v=edge(A,B,r['mode'],r['key']);A,B=v['destination_A'],v['destination_B']
    check((A,B)==start,'positive-cut-full-pair-closure')
    check(d['startup_credit_used']==d['future_period_credit_used']==0,'no-imported-credit')


def main():
    source=read(HERE/'source_discharge_certificate.json')
    overlap=read(HERE/'overlap_discharge_certificate.json')
    closed=read(HERE/'closed_discharge_certificate.json')
    for name in ('startup_rows','source_span_rows','symbolic_startup_rows','symbolic_span_rows','proposed_connector_rows'):
        rows_audit(source[name])
    check(not source['proposed_connector_success'],'failed-initial-proposal-retained')
    for name in ('before_exposure','after_exposure'):
        r=source[name];check(2*r['E']==r['G']-r['z_B']-2*r['z_A'],'parity-identity')
    check(source['before_exposure']['G']==source['after_exposure']['G']==2,'source-exposure-with-unchanged-G')
    check((source['before_exposure']['E'],source['after_exposure']['E'])==(0,1),'source-parity-exposure')
    parity=parity_proof();mixed=[]
    for u,v in overlap['cases'].items():
        for name in ('startup_rows','exposure_rows','symbolic_startup_rows','symbolic_span_rows','same_connector_rows'):
            rows_audit(v[name])
        A,B=v['postpositive_A'],v['postpositive_B']
        nonnegative=[]
        for row in v['core_successors']:
            r=edge(A,B,'KEEP',row['key'])
            for k in ('d_A','d_B','a','q','delta'):check(r[k]==row[k],'complete-core-successor-table')
            check((r['destination_A']==r['destination_B'])==row['synchronizes'],'core-successor-sync-flag')
            if r['delta']>=0:nonnegative.append(row['key'])
        check(nonnegative==([] if u=='4' else [2]),'only-declared-saturated-successor')
        if u=='4':
            l=A[1];p=l[1];rot=[A[0],[p[0],p[1],[l[0],p[2],l[2]]],A[2]]
            check(rot==B,'full-one-internal-rotation-identity')
        sy=v['symbolic_span_rows'][-2]
        ga,gb=gaps(sy['destination_A']),gaps(sy['destination_B'])
        check(len(ga)==len(gb)==14,'all-ordered-gap-fringes')
        for row in v['fringe_successors']:
            a0,b0=ga[row['gap']],gb[row['gap']]
            check((a0,b0)==(row['A_root_depth'],row['B_root_depth']),'source-fringe-root-depth')
            for z in row['parity_cases']:
                p=z['parity'];ac=(a0+p+1)//2;qc=(b0+p)//2
                check(ac==z['A_StepEv_constant'] and qc==z['B_double_constant'],'exact-fringe-parity-coefficients')
                check(qc-2*ac==z['delta_constant']<=-1 and z['delta_v_coefficient']==-1,'all-depth-fringe-deficit')
        mixed.append(dict(overlap=u,rows=[mixed_audit(A,B,x) for x in ([4] if u=='4' else [2,4])]))
    for name,c in closed['cases'].items():
        for field in ('rows','symbolic_rows','reflected_rows'):rows_audit(c[field])
        for field in ('rows','symbolic_rows','reflected_rows'):
            rs=c[field]
            check(rs[0]['source_A']==rs[0]['source_B'],'diagonal-reachability-of-closed-control')
            check((rs[-1]['destination_A'],rs[-1]['destination_B'])==(rs[0]['source_A'],rs[0]['source_B']),'closed-complete-pair-not-just-root')
            check([i for i,r in enumerate(rs) if r['delta']>0]==c['positive_blocks'],'exactly-one-positive-block')
            check(all(rs[i]['key']!=rs[(i+1)%len(rs)]['key'] for i in range(len(rs))),'cyclic-maximal-block-boundaries')
        check(sum(r['a'] for r in c['rows'])==c['A'] and sum(r['q'] for r in c['rows'])==c['Q'],'closed-control-total')
        injection_audit(c['rows'],c['direct_injection'])
    old=read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    for field in ('ordinary_rows','reflected_rows','startup_rows','formal_opaque_fringe_rows'):rows_audit(old[field])
    w=old['ordinary_rows'];check(sum(r['a'] for r in w)==25 and sum(r['q'] for r in w)==22,'frozen-19-block-costs')
    donors={}
    for j in (2,4):
        check(w[j]['a']==w[j]['q']==1,'frozen-alternative-donor-source-capacity')
        donors[str(j)]=dict(A_unit=[j,0,1],B_double=[0,2],A_event=w[j]['A_events'][0],
            distinct_alternative_not_cumulative=True)
    pins=read(HERE/'entry_source_pins.json')
    for path,digest in pins['files'].items():check(sha(ROOT/path)==digest,'frozen-inherited-file')
    result=dict(status='PASS',total_checks=sum(counts.values()),checks=dict(sorted(counts.items())),
        parity_cases=parity,mixed_physical_owner_checks=mixed,old_19_block_donors=donors,
        new_closed_controls={k:dict(blocks=len(v['rows']),A=v['A'],Q=v['Q'],donor=v['direct_injection']['donor_block']) for k,v in closed['cases'].items()},
        both_original_engines=True,opaque_fringe_replay_both_engines=True,
        unrestricted_FE02_CD='OPEN',universal_Coarse_Double='OPEN',
        larger_finite_fits=0,larger_key_count_replays=0,new_size_sweep=False,
        actual_CD_counterexample_claimed=False,FE01_PG02_unchanged=True,
        script_sha256=sha(Path(__file__)),source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py']},
        certificate_hashes={n:sha(HERE/n) for n in ['source_discharge_certificate.json','overlap_discharge_certificate.json','closed_discharge_certificate.json','fixed_connector_certificate.json','overlap_connector_certificate.json']})
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',total_checks=sum(counts.values()),closed_controls=result['new_closed_controls'],FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
