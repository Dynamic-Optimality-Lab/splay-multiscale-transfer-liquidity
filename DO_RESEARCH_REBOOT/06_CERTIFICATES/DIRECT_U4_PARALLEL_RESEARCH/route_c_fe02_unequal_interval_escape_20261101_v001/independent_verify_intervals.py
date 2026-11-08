"""Original pointer/tuple replays and independent source-frontier checks.

Imports no producer. Only the predeclared fixed corpus is verified.
"""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
counts=Counter()


def ck(x,tag):assert x,tag;counts[tag]+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def load(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
tu=load('interval_check_tuple',ROOT/'python/independent/splay.py')
pt=load('interval_check_pointer',ROOT/'python/liquidity/legacy_embedding.py')
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def tj(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return [t[1],tj(t[2]),tj(t[3])]
def pp(t,p=None):
    if t is None:return None
    if isinstance(t,str):return pt.mknode(t,p=p)
    n=pt.mknode(t[0],p=p);n['l']=pp(t[1],n);n['r']=pp(t[2],n);return n
def pj(t,p=None):
    if t is None:return None
    ck(t['p'] is p,'pointer-parent-link')
    if isinstance(t['k'],str):
        ck(t['l'] is None and t['r'] is None,'opaque-subtree-untouched');return t['k']
    return [t['k'],pj(t['l'],t),pj(t['r'],t)]
def depth(t,k):
    d=0
    while isinstance(t,list):
        if t[0]==k:return d
        t=t[1 if k<t[0] else 2];d+=1
    raise AssertionError('explicit present key')
def keys(t):return [] if not isinstance(t,list) else keys(t[1])+[t[0]]+keys(t[2])
def events(e):return [[v['case'],v['lo'],v['hi'],v['orient']] for v in e]


def pair_scan(a,b,path=()):
    # Independently identify common-prefix keys and mismatch intervals by
    # path coordinates, not by the producer's interval bounds/recursion.
    stack=[(a,b,path)];common=[];opaque=[];holes=[]
    while stack:
        x,y,p=stack.pop()
        if x is None and y is None:continue
        if isinstance(x,str) and x==y:opaque.append(x);continue
        if isinstance(x,list) and isinstance(y,list) and x[0]==y[0]:
            common.append(x[0]);stack.extend([(x[2],y[2],p+(2,)),(x[1],y[1],p+(1,))])
        else:holes.append((p,x,y))
    return dict(keys=set(common),opaque=Counter(opaque),holes=holes)


def locate(a,b,x):
    u,v=a,b;h=0
    while isinstance(u,list) and isinstance(v,list) and u[0]==v[0]:
        if u[0]==x:return dict(kind='common_core')
        side=1 if x<u[0] else 2;u,v=u[side],v[side];h+=1
    ua,ub=depth(u,x),depth(v,x)
    return dict(kind='disagreement_interval',external_depth=h,internal_depth_A=ua,
        internal_depth_B=ub,even_even=ua%2==ub%2==0)


def check_expr(a,b,e):
    v=pair_scan(a,b)
    ck(e['constant']==len(v['keys']),'common-core-count')
    ck(e['opaque_size_coefficients']==dict(v['opaque']),'formal-opaque-mass-coefficients')


def edge(a,b,mode,x):
    da=depth(a,x);at,ae=tu.trace(tt(a),x);ap,aep=pt.splay_trace(pp(a),x)
    A=tj(at);pa=pj(ap);ae=[list(v) for v in ae]
    ck(A==pa,'independent-A-destination');ck(ae==events(aep),'independent-A-events')
    ck(len(ae)==(da+1)//2,'A-StepEv-edge-depth')
    if mode=='KEEP':
        db=depth(b,x);bt,be=tu.trace(tt(b),x);bp,bep=pt.splay_trace(pp(b),x)
        B=tj(bt);pb=pj(bp);be=[list(v) for v in be]
        ck(B==pb,'independent-B-destination');ck(be==events(bep),'independent-B-events')
        ck(sum(v[0]!='ZIG' for v in be)==db//2,'B-double-edge-depth')
        ck(sum(v[0]=='ZIG' for v in be)==db%2,'B-terminal-zig-retained')
    else:db=None;B=b;be=[]
    ck(keys(A)==keys(a) and keys(B)==keys(b),'ordered-core-preserved')
    return dict(source_A=a,source_B=b,destination_A=A,destination_B=B,mode=mode,key=x,
        d_A=da,d_B=db,a=len(ae),q=sum(v[0]!='ZIG' for v in be),z=sum(v[0]=='ZIG' for v in be),
        delta=sum(v[0]!='ZIG' for v in be)-2*len(ae),A_events=ae,B_events=be)


def row_check(r):
    v=edge(r['source_A'],r['source_B'],r['mode'],r['key'])
    for k in v:
        if k in r:ck(v[k]==r[k],'recorded-'+k)


def history(rows):
    for i,r in enumerate(rows):
        if i:ck((rows[i-1]['destination_A'],rows[i-1]['destination_B'])==(r['source_A'],r['source_B']),'complete-source-chain')
        row_check(r)


def mixed(a,b,x):
    # Preserve original ownership: leader DELETE, zero-cost DELETE,
    # first KEEP for B work, then an idempotent same-key KEEP.
    d=edge(a,b,'DELETE',x);f=edge(d['destination_A'],d['destination_B'],'DELETE',x)
    k=edge(f['destination_A'],f['destination_B'],'KEEP',x)
    z=edge(k['destination_A'],k['destination_B'],'KEEP',x);v=edge(a,b,'KEEP',x)
    ck(f['a']==k['a']==z['a']==0 and f['q']==z['q']==0,'zero-A-followers')
    ck((d['a'],k['q'])==(v['a'],v['q']),'costed-mixed-projection')
    ck((k['destination_A'],k['destination_B'])==(v['destination_A'],v['destination_B']),'mixed-full-endpoint')
    return dict(key=x,A_leader_occurrence=0,B_first_KEEP_occurrence=2,a=d['a'],q=k['q'])


def reflected(t):
    if not isinstance(t,list):return t
    return [6-t[0],reflected(t[2]),reflected(t[1])]


def main():
    primitive=read(HERE/'primitive_context_certificate.json')
    for case,v in primitive['contexts'].items():
        r=v['row'];row_check(r);c=locate(r['source_A'],r['source_B'],r['key'])
        ck(c['even_even'],'primitive-even-even-source-entry')
        for k in c:ck(c[k]==v['classification'][k],'primitive-source-classification')
        before,after=pair_scan(r['source_A'],r['source_B']),pair_scan(r['destination_A'],r['destination_B'])
        ck(before['keys']<after['keys'],'old-core-retained-plus-accessed-key')
        ck(r['key'] in after['keys']-before['keys'],'accessed-key-newly-agreed')
        check_expr(r['source_A'],r['source_B'],v['before']);check_expr(r['destination_A'],r['destination_B'],v['after'])
    fixed=read(HERE/'existing_control_interval_certificate.json');even=odd=common=0
    for name,rows in fixed['corpora'].items():
        for v in rows:
            r=v['row'];row_check(r);c=locate(r['source_A'],r['source_B'],r['key'])
            for k in c:ck(c[k]==v['classification'][k],'independent-canonical-hole-entry')
            check_expr(r['source_A'],r['source_B'],v['before']);check_expr(r['destination_A'],r['destination_B'],v['after'])
            pre,post=pair_scan(r['source_A'],r['source_B']),pair_scan(r['destination_A'],r['destination_B'])
            if c['kind']=='common_core':
                common+=1;ck(r['delta']<0,'common-core-target-forces-negative-block')
            elif c['even_even']:
                even+=1;ck(pre['keys']<post['keys'],'even-even-all-old-common-keys-retained')
            else:odd+=1
            if r['delta']>=0:ck(c['kind']=='disagreement_interval','nonnegative-block-enters-unequal-interval')
    obstruction=read(HERE/'odd_boundary_obstruction_certificate.json')
    for k in ['symbolic_startup_rows','physical_closed_rows','symbolic_closed_rows']:history(obstruction[k])
    r=obstruction['saturated_row'];row_check(r)
    check_expr(r['source_A'],r['source_B'],obstruction['before'])
    check_expr(r['destination_A'],r['destination_B'],obstruction['after'])
    c=locate(r['source_A'],r['source_B'],r['key'])
    ck((c['external_depth'],c['internal_depth_A'],c['internal_depth_B'])==(1,0,3),'odd-boundary-source-depths')
    ck((r['a'],r['q'],r['delta'])==(1,2,0),'saturated-zero-spare-capacity')
    for name in ('physical_closed_rows','symbolic_closed_rows'):
        rs=obstruction[name];ck(rs[0]['source_A']==rs[0]['source_B'],'obstruction-diagonal-reachability')
        ck((rs[-1]['destination_A'],rs[-1]['destination_B'])==(rs[0]['source_A'],rs[0]['source_B']),'obstruction-full-pair-closure')
    sym=obstruction['symbolic_closed_rows'];never={r['key'] for r in sym}
    ck(never=={1,2,3,4,5},'no-interior-fringe-key-accessed')
    states=[(sym[0]['source_A'],sym[0]['source_B'])]+[(r['destination_A'],r['destination_B']) for r in sym]
    l_agreement=[int(pair_scan(a,b)['opaque'].get('L',0)) for a,b in states]
    ck(l_agreement[0]==l_agreement[-1]==1 and l_agreement[4]==1 and l_agreement[5]==0,'unaccessed-L-evicted-and-restored')
    reflection=[]
    for r in sym:
        v=edge(reflected(r['source_A']),reflected(r['source_B']),r['mode'],6-r['key'])
        ck(v['destination_A']==reflected(r['destination_A']) and v['destination_B']==reflected(r['destination_B']),'reflected-full-source-identity')
        ck((v['a'],v['q'])==(r['a'],r['q']),'reflected-source-costs')
        reflection.append(dict(mode=v['mode'],key=v['key'],a=v['a'],q=v['q']))
    failed=read(HERE/'fixed_composition_failure_certificate.json');history(failed['rows'])
    positives=[[i,r['key'],r['a'],r['q']] for i,r in enumerate(failed['rows']) if r['delta']>0]
    ck(positives==failed['actual_positive_rows']==[[16,7,1,3],[29,7,1,3]],'membership-proposal-rejected-for-two-positives')
    ck(not failed['FE02_membership_claimed'] and failed['no_alternative_connector_searched'],'failure-scope-not-promoted')
    rows=failed['rows'];ck(rows[-1]['destination_A']==rows[-1]['destination_B']==rows[0]['source_A'],'failed-target-still-exactly-closed')
    # The old base13 control meets the proved source-even FE02 criterion.
    ad=read(BASE/'route_c_fe02_approach_discharge_20261101_v001/closed_discharge_certificate.json')['cases']['base']
    for r in ad['rows']:
        if r['delta']>=0:
            c=locate(r['source_A'],r['source_B'],r['key']);ck(c.get('even_even',False),'actual-FE02-source-even-nonvacuity')
    # Check its existing actual one-period injection, without changing it.
    assigned=ad['direct_injection']['assignments'];u=set();d=set()
    for v in assigned:
        i,e,bit=v['A_unit'];j,z=v['B_double']
        ck(e<ad['rows'][i]['a'] and bit in (0,1),'actual-A-unit')
        ck(ad['rows'][j]['B_events'][z][0]!='ZIG','actual-B-double')
        ck((i,e,bit) not in u and (j,z) not in d,'no-credit-or-demand-reuse')
        u.add((i,e,bit));d.add((j,z))
    ck(len(d)==ad['Q']==16,'source-even-physical-injection-complete')
    mixed_owners=[mixed(r['source_A'],r['source_B'],r['key'])]
    source_ee=primitive['contexts']['LR']['row']
    mixed_owners.append(mixed(source_ee['source_A'],source_ee['source_B'],source_ee['key']))
    # Full frozen19-block regression and tuple/pointer first-entry events.
    w=read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    for k in ['ordinary_rows','reflected_rows','startup_rows']:history(w[k])
    ck(sum(r['a'] for r in w['ordinary_rows'])==25 and sum(r['q'] for r in w['ordinary_rows'])==22,'frozen-W25-22-regression')
    for j in (2,4):ck(w['ordinary_rows'][j]['a']==w['ordinary_rows'][j]['q']==1,'frozen-alternative-physical-donors')
    pins=read(HERE/'entry_source_pins.json')
    for name,h in pins['files'].items():ck(sha(ROOT/name)==h,'all-frozen-file-hashes')
    result=dict(status='PASS',total_checks=sum(counts.values()),checks=dict(sorted(counts.items())),
        primitive_contexts=6,existing_fixed_rows=sum(len(v) for v in fixed['corpora'].values()),
        existing_source_cases=dict(even_even=even,odd_boundary=odd,common_core_target=common),
        symbolic_L_agreement_by_boundary=l_agreement,unaccessed_payload_recovery_verified=True,
        reflected_symbolic_obstruction=reflection,mixed_physical_owners=mixed_owners,
        failed_composition_positive_indices=[16,29],failed_composition_FE02_membership=False,
        even_even_FE02_class_nonvacuity='old base13 control',distinct_physical_units_verified=True,
        arbitrary_FE02_eventual_discharge='OPEN',FE02_CD='OPEN',
        Coarse_Double_counterexample=False,larger_finite_fits=0,
        larger_source_key_count_replays=0,source_sizes='existing5-core and13-core; opaque primitive cores<=5',
        certificate_hashes={p.name:sha(p) for p in HERE.glob('*certificate.json')},
        original_source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py']},
        script_sha256=sha(Path(__file__)))
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',checks=sum(counts.values()),source_cases=result['existing_source_cases'],
        lost_and_recovered_unaccessed_L=True,failed_membership_correctly_rejected=True,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
