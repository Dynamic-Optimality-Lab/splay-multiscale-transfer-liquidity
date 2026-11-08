"""Complete the separate48-operation control's actual frozen policy,
then record a uniformly quantified ordinal/cut proof certificate.
No new source splay is executed; verified/generated rows are reused.
"""
import collections,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C28_control_policy',OLD/'audit_construct.py')
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(x):return tuple(fr(z) for z in x) if isinstance(x,list) else x
def mp(x):return {tuple(z['demand']):tuple(z['unit']) for z in x}
def pack(x):return [{'demand':d,'unit':u} for d,u in sorted(x.items())]
def profile(a):
    ee=[]
    for d,u in a.items():ee.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    active=set();peak=0;rr=[]
    for t,d in sorted(ee):
        if d in active:active.remove(d)
        else:active.add(d)
        peak=max(peak,len(active));rr.append({'point':t,'records':len(active)})
    assert not active;return peak,rr
def main():
    c=json.loads((B/'shortened_source_control.json').read_text());rows=[dict(r,before=fr(r['before']),after=fr(r['after'])) for r in c['rows']]
    full=C.L.build(rows,C.M);D,U=full['D'],full['U'];f6=mp(c['f6']);common={d:u for d,u in f6.items() if d in D}
    X=load('C28_control_exchange',P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py');a=X.exchange(D,U,common,full['h0'])['allocation'];natural=dict(a);stages=[]
    def stage(n,h):
        nonlocal a
        old=dict(a);z=C.L.augment_partial(D,U,a,h);a=z['allocation'];assert all(a[d]==u for d,u in old.items())
        stages.append({'name':n,'comparison':pack(h),'prior':pack(old),'after':pack(a),'additions':pack(z['additions'])})
    v,pp,cp,tr=C.selection(rows);ate=[z for z in tr if z['birth'][0]==c['tags']['e']];assert len(ate)==2
    hc=dict(full['h'])
    for z in cp:hc[tuple(z['demand'])]=tuple(z['unit'])
    ht=dict(hc)
    for z in tr:ht[tuple(z['origin'])]=ht.pop(tuple(z['birth']))
    hp=dict(ht);groups=collections.defaultdict(list);mm=C.L.macros(rows)
    for z in tr:groups[z['birth_macro']].append(tuple(z['birth']))
    for i,ds in sorted(groups.items()):
        free=[u for u in mm[i]['units'] if u not in hp.values()]
        for d,u in zip(sorted(ds),free):hp[d]=u
    for name,h in (('leaf',full['h']),('creator',hc),('T19',ht),('own_tail',hp)):stage(name,h)
    jm=next(m for m in mm if c['tags']['j'] in m['occurrences']);jd=jm['units'][2];assert jd not in hp.values();hj=dict(hp)
    missing=[tuple(z['birth']) for z in ate if tuple(z['birth']) not in hj]
    if missing:hj[missing[0]]=jd;stage('j_ordinal3',hj)
    before=dict(a);remaining=sorted(D-set(a));images=set(f6.values())|set(full['h0'].values())|set(hj.values());seeds=[]
    for m in mm:
        if any(r['mode']!='D' for r in m['rows'][:-1]):continue
        for u in m['units'][8:]:
            if u not in images and u not in set(a.values()):seeds.append(u)
    assert len(seeds)>=len(remaining);new=[]
    for d,u in zip(remaining,seeds):a[d]=u;new.append({'demand':d,'unit':u})
    assert set(a)==D and len(set(a.values()))==len(D) and all(a[d]==u for d,u in before.items())
    peak,trace=profile(a);assert peak<=25
    out('shortened_control_policy.json',{'status':'SEPARATE_SOURCE_COMPLETE_POLICY_PENDING_DISTINCT_AUDIT','source_id':c['source_id'],
        'f6':c['f6'],'common':pack(common),'natural_prior':pack(natural),'full_h0':pack(full['h0']),
        'creator_pairs':cp,'selected_transports':tr,'selected_at_e':ate,'policy_stages':stages,
        'prior_before_extra':pack(before),'extra_payments':new,'final_full_a':pack(a),'full_endpoint_peak':peak,'cut_profile':trace,
        'source_queries':0,'old_source_mutated':False,'qF':sum(r['qF'] for r in rows),'A':sum(r['a'] for r in rows),
        'old_5_core9_absence_inherited':'identical cyclic KEEP sequence and same erased B states; DELETE changes only A'})
    # A certificate for universal linear identities, not finite tests of H.
    out('uniform_ordinal_proof_certificate.json',{'status':'UNIFORM_MANUSCRIPT_LEMMA_ALGEBRA_CERTIFICATE',
        'variables':['L','c','g','k','j'],
        'assumptions':{'k_nonnegative':[0,0,0,1,0,0],'j_nonnegative':[0,0,0,0,1,0],
            'j_below_k':[0,0,0,1,-1,-1],'band_capacity':[1,-1,-1,-1,0,0]},
        'unit_ordinal':[0,1,0,0,1,1],
        'lower_identity':{'goal':[0,0,0,0,1,1],'nonnegative_terms':{'j_nonnegative':1},'positive_constant':1},
        'upper_identity':{'goal':[1,-1,-1,0,-1,-1],'nonnegative_terms':{'band_capacity':1,'j_below_k':1},'positive_constant':0},
        'source_premises':['original actual clean full macro D*KEEP, terminal full-nonroot KEEP',
            'six-key high-core raw selector and its original natural owners; each packet budget<=8',
            'no selected T19 arrival in this supplier macro; creator payments are LAST g units',
            'all later effective insertions have complete comparison/exception provenance',
            'static source/block eligibility for the proposed immediate-next-macro demand',
            'baseline cut-record profile plus new interval load<=25'],
        'does_not_assert':['a supplier exists for every guarded recovery','exception load is universally small',
            'generic prefixes remain<=8 for arbitrary support','Bank25 follows from Hall']})
    print(json.dumps({'status':'48_SOURCE_POLICY_COMPLETE','prior_remaining':remaining,'extra':new,'peak':peak,
        'uniform_source_forcing':'NOT_ASSUMED','source_engine_calls':C.calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_control_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
