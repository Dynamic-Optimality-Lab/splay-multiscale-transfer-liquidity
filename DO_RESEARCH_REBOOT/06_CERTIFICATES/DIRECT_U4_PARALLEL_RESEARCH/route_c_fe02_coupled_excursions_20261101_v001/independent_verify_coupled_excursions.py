"""Independent original-source verification of coupled anchor composition."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
counts=Counter()


def ck(v,t):assert v,t;counts[t]+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
tu=load('coupled_check_tuple',ROOT/'python/independent/splay.py')
pt=load('coupled_check_pointer',ROOT/'python/liquidity/legacy_embedding.py')
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
        ck(t['l'] is None and t['r'] is None,'opaque-subtree-unsearched');return t['k']
    return [t['k'],pj(t['l'],t),pj(t['r'],t)]
def path(t,x):
    out=[]
    while isinstance(t,list):
        out.append(t[0])
        if t[0]==x:return out
        t=t[1 if x<t[0] else 2]
    raise AssertionError('present core key')
def at(t,x):
    while isinstance(t,list):
        if t[0]==x:return t
        t=t[1 if x<t[0] else 2]
    raise AssertionError('present core key')
def norm(e):return [[v['case'],v['lo'],v['hi'],v['orient']] for v in e]


def edge(A,B,mode,x):
    ta,ae=tu.trace(tt(A),x);pa,ape=pt.splay_trace(pp(A),x)
    a=tj(ta);ae=[list(z) for z in ae]
    ck(a==pj(pa),'independent-A-whole-destination');ck(ae==norm(ape),'independent-A-events')
    ck(len(ae)==(len(path(A,x)))//2,'actual-A-StepEv-edge-depth')
    if mode=='KEEP':
        tb,be=tu.trace(tt(B),x);pb,bpe=pt.splay_trace(pp(B),x);b=tj(tb);be=[list(z) for z in be]
        ck(b==pj(pb),'independent-B-whole-destination');ck(be==norm(bpe),'independent-B-events')
        ck(sum(z[0]!='ZIG' for z in be)==(len(path(B,x))-1)//2,'actual-B-double-edge-depth')
        ck(sum(z[0]=='ZIG' for z in be)==(len(path(B,x))-1)%2,'terminal-B-zig-retained')
    else:b=B;be=[]
    return dict(source_A=A,source_B=B,destination_A=a,destination_B=b,mode=mode,key=x,
        a=len(ae),q=sum(z[0]!='ZIG' for z in be),A_events=ae,B_events=be,
        delta=sum(z[0]!='ZIG' for z in be)-2*len(ae))


def row(r):
    v=edge(r['source_A'],r['source_B'],r['mode'],r['key'])
    for k in v:
        if k in r:ck(v[k]==r[k],'recorded-'+k)


def history(rs):
    for i,r in enumerate(rs):
        if i:ck((rs[i-1]['destination_A'],rs[i-1]['destination_B'])==(r['source_A'],r['source_B']),'full-source-history-chain')
        row(r)


def parse(rs,g):
    hits=[i for i,r in enumerate(rs) if r['key']==g];out=[];N=len(rs)
    for k,i in enumerate(hits):
        j=hits[(k+1)%len(hits)];length=(j-i)%N or N
        ids=[(i+t)%N for t in range(1,length+1)]
        roots=[rs[t]['key'] for t in ids[:-1]]
        right=bool(roots) and all(g<x for x in roots)
        left=bool(roots) and all(g>x for x in roots)
        ordered=(right and all(a<b for a,b in zip(roots,roots[1:]))) or (left and all(a>b for a,b in zip(roots,roots[1:])))
        out.append(dict(start=i,end=j,ids=ids,roots=roots,side='R' if right else 'L' if left else None,ordered=ordered))
    return out


def phase_audit(rs,g,stored=None):
    ps=parse(rs,g);critical=[]
    if stored is not None:ck(len(ps)==len(stored),'anchor-phase-count')
    for n,p in enumerate(ps):
        A,B=rs[p['start']]['destination_A'],rs[p['start']]['destination_B']
        if stored is not None:
            z=stored[n]
            ck((p['start'],p['end'],p['ids'],p['roots'],p['side'],p['ordered'])==(z['start_after_block'],z['return_block'],z['indices'],z['internal_keys'],z['one_side'],z['ordered']),'independent-cyclic-excursion-partition')
        if p['side']:
            opp=1 if p['side']=='R' else 2
            for name,T in [('A',A),('B',B)]:
                initial=at(T,g)[opp]
                for i in p['ids']:
                    ck(at(rs[i]['source_'+name],g)[opp]==initial and at(rs[i]['destination_'+name],g)[opp]==initial,'entire-opposite-subtree-isolation')
        if p['ordered'] and A[0]==B[0]==g and all(rs[i]['mode']=='KEEP' for i in p['ids']):
            epsA=[];epsB=[]
            for i in p['ids'][:-1]:
                r=rs[i]
                epsA.append(len(path(r['destination_A'],r['source_A'][0]))-1)
                epsB.append(len(path(r['destination_B'],r['source_B'][0]))-1)
            ret=rs[p['end']];da=sum(epsA);db=sum(epsB);D=sum(2*a-b for a,b in zip(epsA,epsB))
            ck((da,db)==(ret['d_A'],ret['d_B']),'exact-ordered-return-depth-sums')
            spare=(da%2)+(D+1)//2
            ck(spare==2*ret['a']-ret['q']>=0,'actual-return-spare-source-identity')
            if stored is not None:
                f=stored[n]['ordered_source_formula']
                ck(f['epsilon_A']==epsA and f['epsilon_B']==epsB and f['source_reserve']==spare,'source-formula-recorded')
            if spare==0:
                ck(all(a==1 and b==2 for a,b in zip(epsA,epsB)) and (len(epsA)-1)%2==1,'critical-phase-all-one-two-and-parity')
                side=2 if p['side']=='R' else 1
                child0=B[side][0];child1=ret['destination_B'][side][0];first=p['roots'][0]
                ck((child0<first<child1) if side==2 else (child0>first>child1),'strict-outward-B-child-drift')
                ck(ret['destination_B'][3-side]==B[3-side],'opposite-B-child-subtree-fixed-at-critical-return')
                critical.append(dict(anchor=g,start=p['start'],end=p['end'],side=p['side'],before=child0,first=first,after=child1))
    return ps,critical


def injection(rs,d):
    aa=set();bb=set()
    for a in d['assignments']:
        i,e,b=a['A_unit'];j,f=a['B_double']
        ck(0<=e<rs[i]['a'] and b in(0,1),'actual-physical-A-event-bit')
        ck(0<=f<len(rs[j]['B_events']) and rs[j]['B_events'][f][0]!='ZIG','actual-physical-B-double')
        ck((i,e,b) not in aa and (j,f) not in bb,'no-unit-or-demand-reuse')
        aa.add((i,e,b));bb.add((j,f))
    ck(len(bb)==sum(r['q'] for r in rs),'all-B-demands-paid-once')
    j=d['donor_block'];p=d['positive_cut']
    ck(rs[j]['delta']<0 and d['donor_unit']==[j,rs[j]['a']-1,1],'last-unit-source-certified-spare')
    ck(d['startup_credit_used']==d['future_period_credit_used']==0,'no-imported-credit')
    start=(rs[p]['source_A'],rs[p]['source_B']);A,B=start
    for k in range(len(rs)):
        r=rs[(p+k)%len(rs)];ck((A,B)==(r['source_A'],r['source_B']),'single-positive-cut-source-order')
        A,B=r['destination_A'],r['destination_B']
    ck((A,B)==start,'single-period-positive-cut-full-closure')


def mixed(r):
    A,B,x=r['source_A'],r['source_B'],r['key']
    d=edge(A,B,'DELETE',x);z=edge(d['destination_A'],B,'DELETE',x)
    k=edge(z['destination_A'],B,'KEEP',x)
    ck((d['a'],k['q'])==(r['a'],r['q']),'mixed-A-leader-B-first-KEEP-costs')
    ck(z['a']==k['a']==0,'mixed-zero-A-followers')
    ck((k['destination_A'],k['destination_B'])==(r['destination_A'],r['destination_B']),'mixed-block-complete-boundary-projection')
    return dict(key=x,A_leader_occurrence=0,B_first_KEEP_occurrence=2,a=d['a'],q=k['q'])


def main():
    d=read(HERE/'coupled_excursion_control_certificate.json')
    ck(d['status']=='VERIFIED_FE02_ORDERED_EXCURSION_CONTROL','fixed-control-proposal-succeeded')
    for field,anchor,phasefield in [('rows',1,'excursions'),('symbolic_rows',1,'symbolic_excursions'),('reflected_rows',13,'reflected_excursions')]:
        rs=d[field];history(rs)
        ck(rs[0]['source_A']==rs[0]['source_B'],'exact-diagonal-reachability')
        ck((rs[-1]['destination_A'],rs[-1]['destination_B'])==(rs[0]['source_A'],rs[0]['source_B']),'complete-pair-control-closure')
        positives=[i for i,r in enumerate(rs) if r['delta']>0]
        ck(positives==d['positive_blocks']==[8] and (rs[8]['a'],rs[8]['q'])==(1,3),'one-positive-original-FE02-instance')
        ck(all(rs[i]['key']!=rs[(i+1)%len(rs)]['key'] for i in range(len(rs))),'maximal-cyclic-blocks-equal-occurrences')
        phases,critical=phase_audit(rs,anchor,d[phasefield])
        ck(len(phases)==17 and all(p['ordered'] for p in phases),'all-seventeen-source-excursions-ordered')
    ck(sum(r['a'] for r in d['rows'])==d['A']==45 and sum(r['q'] for r in d['rows'])==d['Q']==22,'control-source45-22')
    injection(d['rows'],d['direct_injection'])
    coverage=read(HERE/'anchor_coverage_certificate.json')
    old=read(BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json')
    history(old['rows']);history(old['reflected_rows'])
    failures={};crit=[];qualifying=[]
    for g in range(1,14):
        ps,cs=phase_audit(old['rows'],g,coverage['anchors'][str(g)]['all_excursions']);crit+=cs
        mirrored,mircrit=phase_audit(old['reflected_rows'],14-g);crit+=mircrit
        good=all(p['ordered'] for p in ps)
        ck(good==coverage['anchors'][str(g)]['qualifies'],'all-fixed-anchors-independent-coverage')
        if good:qualifying.append(g)
        else:failures[str(g)]=next(p for p in ps if not p['ordered'])
    ck(qualifying==coverage['qualifying_anchors']==[],'actual-FE02-no-qualifying-anchor-coverage-obstruction')
    ck(any(p['side']=='R' for p in crit) and any(p['side']=='L' for p in crit),'critical-source-drift-both-orientations')
    mixed_owners=[mixed(r) for r in d['rows'][8:11]]
    pg=read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    for field in ['ordinary_rows','reflected_rows','startup_rows']:history(pg[field])
    ck(sum(r['a'] for r in pg['ordinary_rows'])==25 and sum(r['q'] for r in pg['ordinary_rows'])==22,'frozen19-block25-22-regression')
    for j in(2,4):ck(pg['ordinary_rows'][j]['a']==pg['ordinary_rows'][j]['q']==1,'frozen-alternative-donor-capacities')
    pins=read(HERE/'entry_source_pins.json')
    for p,h in pins['files'].items():ck(sha(ROOT/p)==h,'frozen-inherited-file-hash')
    result=dict(status='PASS',total_checks=sum(counts.values()),checks=dict(sorted(counts.items())),
        both_original_engines=True,source_control=dict(blocks=35,excursions=17,A=45,Q=22,positive_block=8,
            donor_block=d['direct_injection']['donor_block']),opaque_all14_gaps=True,reflection=True,
        coupled_critical_drift_contexts=crit,mixed_physical_owners=mixed_owners,
        fixed_OR34_anchor_failures=failures,unqualified_FE02_anchor_coverage='REFUTED—EXACT',
        saturated_counterexample_specific_coverage='OPEN',
        all_size_coupled_theorem='written source side-isolation plus ordered phase drift and endpoint argument, not finite audit extrapolation',
        FE02_CD='OPEN',Coarse_Double_counterexample=False,larger_finite_fits=0,
        larger_source_key_count_replays=0,source_graph_or_coefficient_search=False,
        script_sha256=sha(Path(__file__)),
        certificate_hashes={p.name:sha(p) for p in HERE.glob('*certificate.json')},
        original_source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py']})
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',checks=sum(counts.values()),source_control=result['source_control'],critical_drift_contexts=len(crit),qualifying_OR34_anchors=qualifying,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
