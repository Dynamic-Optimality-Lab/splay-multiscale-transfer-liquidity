"""Independent original pointer/tuple verification of source lift/classification.

No producer import, source graph search, parameter fit or source-size sweep.
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


def ck(x,t):assert x,t;counts[t]+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
tu=load('lift_check_original_tuple',ROOT/'python/independent/splay.py')
pt=load('lift_check_original_pointer',ROOT/'python/liquidity/legacy_embedding.py')
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
        ck(t['l'] is None and t['r'] is None,'opaque-fringe-unsearched');return t['k']
    return [t['k'],pj(t['l'],t),pj(t['r'],t)]
def path(t,x):
    ns=[];ds=[]
    while isinstance(t,list):
        ns.append(t)
        if t[0]==x:return ns,ds
        side=1 if x<t[0] else 2;ds.append('L' if side==1 else 'R');t=t[side]
    raise AssertionError('present core key')
def protected(a,b):
    out=set();stack=[(a,b)]
    while stack:
        x,y=stack.pop()
        if isinstance(x,str) and x==y:out.add(x)
        elif isinstance(x,list) and isinstance(y,list) and x[0]==y[0]:
            out.add(x[0]);stack.extend([(x[1],y[1]),(x[2],y[2])])
    return out
def norm(ev):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in ev]


def splay(t,x):
    u,e=tu.trace(tt(t),x);p,pe=pt.splay_trace(pp(t),x);ans=tj(u)
    ck(ans==pj(p),'independent-full-splay-destination')
    ev=[list(z) for z in e];ck(ev==norm(pe),'independent-original-events')
    return ans,ev


def row(r):
    a,ae=splay(r['source_A'],r['key']);dA=len(path(r['source_A'],r['key'])[1])
    ck(a==r['destination_A'] and ae==r['A_events'],'recorded-original-A')
    ck(len(ae)==r['a']==(dA+1)//2,'original-A-StepEv-cost')
    if r['mode']=='KEEP':
        b,be=splay(r['source_B'],r['key']);dB=len(path(r['source_B'],r['key'])[1])
        ck(b==r['destination_B'] and be==r['B_events'],'recorded-original-B')
        ck(sum(e[0]!='ZIG' for e in be)==r['q']==dB//2,'original-B-double-demand')
        ck(sum(e[0]=='ZIG' for e in be)==dB%2,'terminal-zig-not-double')
    else:ck(r['destination_B']==r['source_B'] and r['q']==0,'DELETE-keeps-B-frozen')


def independent_lift(source,x,u,record):
    side=1 if x<source[0] else 2
    R,_=splay(source[side],x)
    if side==1:base=[x,R[1],[source[0],R[2],source[2]]]
    else:base=[x,[source[0],source[1],R[1]],R[2]]
    ck(base==record['base_lift'],'single-boundary-base-zig-formula')
    p=source[side][0]
    first=None if u==0 else (1 if x<p else 2)
    flag=u%2==1 and first==side
    ck(flag==record['comparison_correction'],'source-parity-straight-criterion')
    ck(record['original_internal_depth']==u and record['original_child_root']==p,'source-child-depth-and-key')
    q=pp(base)
    if flag:
        if side==1:pt._rot_right(q['r'])
        else:pt._rot_left(q['l'])
    result=pj(q);full,_=splay(source,x)
    ck(result==record['result']==full,'corrected-lift-is-original-source-splay')
    return flag,p


def classify(r,v):
    A,B,x=r['source_A'],r['source_B'],r['key']
    na,da=path(A,x);nb,db=path(B,x);h=0
    while na[h][0]==nb[h][0] and na[h][0]!=x:h+=1
    kind='common_target' if na[h][0]==nb[h][0]==x else 'disagreement_interval'
    ua,ub=len(da)-h,len(db)-h
    ck((kind,h,ua,ub)==(v['kind'],v['external_depth'],v['internal_depth_A'],v['internal_depth_B']),'independent-first-disagreement-interval')
    ck(da[:h]==db[:h]==v['external_directions'],'common-external-source-word')
    asym=[]
    for z in v['levels']:
        j=z['external_source_index'];g=na[j][0]
        ck(g==nb[j][0]==z['external_key'],'named-shared-external-key')
        names=[]
        for ns,ds,field,ev in ((na,da,'A',r['A_events']),(nb,db,'B',r['B_events'])):
            flag,p=independent_lift(ns[j],x,len(ds)-j-1,z[field])
            sig=(g,p,1 if x<g else 2) if flag else None;names.append(sig)
            idx=z[field]['source_double_event_index']
            if flag:
                actual=(len(ds)-j-2)//2
                ck(idx==actual and ev[idx][0]==('LL' if x<g else 'RR'),'comparison-correction-real-source-double-provenance')
                ck(ev[idx][1]==min(g,p,x) and ev[idx][2]==max(g,p,x),'source-event-original-triple')
            else:ck(idx is None,'no-invented-event-for-base-zig')
        ck((names[0]!=names[1])==z['asymmetric_named_correction'],'asymmetric-named-correction')
        if names[0]!=names[1]:asym.append((j,g))
    if kind=='common_target' or h==0:safe=True
    elif ua%2==ub%2==0:safe=True
    elif ua%2==ub%2==1:
        safe=(da[h]!=da[h-1] and db[h]!=db[h-1])
    else:
        odddirs=da if ua%2 else db
        safe=odddirs[h]!=odddirs[h-1] and all(da[j]!=da[j+1] for j in range(h-1))
    before=protected(A,B);after=protected(r['destination_A'],r['destination_B'])
    ck(safe==v['predicted_retention']==v['correction_congruence']==(not asym),'complete-source-parity-retention-classification')
    ck(safe==(before<=after)==v['actual_retention'],'classification-iff-all-old-common-keys-retained')
    ck(before==set(v['old_common']) and after==set(v['new_common']),'common-protected-keys-and-opaque-subtrees')
    if asym:
        witness=min(asym)[1]
        ck(witness==v['source_witness'] and witness in before-after,'outermost-asymmetric-old-ancestor-evicted')
    elif kind=='disagreement_interval':
        ck(x not in before and before<after and x in after,'new-refinement-class-adds-accessed-key')
    else:ck(r['q']-2*r['a']<0,'common-target-forces-negative-nontrivial-block')
    ck(v['recurrence_output_A']==r['destination_A'] and v['recurrence_output_B']==r['destination_B'],'whole-prefix-recurrence-output')


def physical_injection(c):
    rs=c['rows'];d=c['direct_injection'];us=set();ds=set()
    for a in d['assignments']:
        i,e,b=a['A_unit'];j,f=a['B_double']
        ck(0<=e<rs[i]['a'] and b in(0,1),'actual-A-unit-and-bit')
        ck(rs[j]['B_events'][f][0]!='ZIG','actual-B-double-physical-index')
        ck((i,e,b) not in us and (j,f) not in ds,'no-reused-A-unit-or-B-demand')
        us.add((i,e,b));ds.add((j,f))
    ck(len(ds)==c['Q'],'all-actual-B-demands-paid-once')
    ck(d['startup_credit_used']==d['future_period_credit_used']==0,'no-imported-period-credit')


def mixed(r):
    A,B,x=r['source_A'],r['source_B'],r['key']
    a,ae=splay(A,x);b,be=splay(B,x)
    # Subsequent same-key A accesses have no event; B waits until KEEP.
    a2,a2e=splay(a,x);b2,b2e=splay(b,x)
    ck(not a2e and not b2e,'zero-followers-idempotent-source')
    ck(a==r['destination_A'] and b==r['destination_B'],'mixed-complete-boundary-projection')
    ck(len(ae)==r['a'] and sum(z[0]!='ZIG' for z in be)==r['q'],'mixed-original-event-counts')
    return dict(key=x,A_DELETE_leader_occurrence=0,B_first_KEEP_occurrence=2,a=r['a'],q=r['q'])


def main():
    d=read(HERE/'boundary_lift_source_certificate.json');ck(d['status']=='PASS' and not d['discrepancies'],'producer-fixed-corpus-no-discrepancies')
    for name,p in d['primitive_lifts'].items():
        independent_lift(p['source'],p['key'],len(path(p['source'],p['key'])[1])-1,p['lift'])
        ck(p['full']==p['lift']['result'],'all-six-primitive-source-identities')
    parity=Counter();total=0
    for corpus,records in d['corpora'].items():
        for z in records:
            r,v=z['row'],z['analysis'];row(r);classify(r,v);total+=1
            parity[','.join(map(str,v['parity_pair']))]+=1
    ck(total==d['total_fixed_rows']==179 and dict(parity)==d['source_parity_counts'],'fixed-corpus-size-and-all-four-parities')
    ad=read(BASE/'route_c_fe02_approach_discharge_20261101_v001/closed_discharge_certificate.json')
    source_safe_controls=[]
    for name,c in ad['cases'].items():
        for r in c['rows']:
            if r['mode']=='DELETE':row(r)
        nonneg=[v for v in d['corpora']['AD_'+name] if v['row']['q']-2*v['row']['a']>=0]
        ck(all(v['analysis']['predicted_retention'] for v in nonneg),'actual-FE02-refinement-class-nonvacuity')
        ck(c['rows'][0]['source_A']==c['rows'][-1]['destination_A'] and c['rows'][0]['source_B']==c['rows'][-1]['destination_B'],'old-actual-control-full-closure')
        physical_injection(c);source_safe_controls.append(dict(name=name,nonnegative_parities=[v['analysis']['parity_pair'] for v in nonneg]))
    shortcut=read(HERE/'composition_shortcut_obstruction_certificate.json')
    ore=read(BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json')
    rs=[ore['rows'][i] for i in ore['episode_indices']]
    ck(rs[0]['source_A']==rs[-1]['destination_A'],'actual-A-source-return')
    ck([v[0] for r in rs for v in r['A_events']]==['ZIG','ZIG','LL'],'one-unpaired-physical-same-side-source-double')
    final=rs[-1];local,_=splay(final['source_A'][1],1)
    base=[1,local[1],[11,local[2],final['source_A'][2]]]
    ck(base==shortcut['base_lift'] and base!=shortcut['original_A_source'],'base-part-alone-not-neutral-on-A-return')
    q=pp(base);pt._rot_right(q['r']);repaired=pj(q)
    ck(repaired==shortcut['corrected_result']==shortcut['original_A_source'],'single-formal-correction-closes-A-source')
    owners=[mixed(r) for r in rs]
    w=read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    ck(sum(r['a'] for r in w['ordinary_rows'])==25 and sum(r['q'] for r in w['ordinary_rows'])==22,'frozen-W25-22')
    for i in(2,4):ck(w['ordinary_rows'][i]['a']==w['ordinary_rows'][i]['q']==1,'frozen-alternative-donor-capacities')
    pins=read(HERE/'entry_source_pins.json')
    for name,h in pins['files'].items():ck(sha(ROOT/name)==h,'frozen-file-hash')
    result=dict(status='PASS',total_checks=sum(counts.values()),checks=dict(sorted(counts.items())),
        fixed_source_rows=179,primitive_identities=6,source_parities=dict(parity),
        both_original_engines=True,full_prefix_recurrence_verified=True,
        source_safe_FE02_controls=source_safe_controls,mixed_physical_owners=owners,
        independent_per_tree_correction_cancellation='REFUTED—EXACT; coupled global composition remains open',
        step1_source_classification='PROVED by source identity and induction; finite audit is verification only',
        step2_global_composition='OPEN; proof gate not passed',step3_physical_injection='verified on new source-safe domain',
        FE02_CD='OPEN',Coarse_Double_counterexample=False,larger_finite_fits=0,
        larger_source_key_count_replays=0,coefficient_or_source_graph_search=False,
        script_sha256=sha(Path(__file__)),
        certificate_hashes={p.name:sha(p) for p in HERE.glob('*certificate.json')},
        original_source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py']})
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',checks=sum(counts.values()),fixed_rows=179,parities=dict(parity),source_safe_FE02_controls=source_safe_controls,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
