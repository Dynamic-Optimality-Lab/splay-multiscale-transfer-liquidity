"""Two actual closed-source comb fixtures: zero helper and paid helper.
No old certificate/owner is edited. Source counterclaims concern intrinsic
signed expressions, independently of optional nested owner normalization.
"""
import collections,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C29_source_producer',OLD/'audit_construct.py')
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l=None,r=None):return (k,l,r)
def fill(t,count=None):
    if count is None:count=[0]
    if t is None:z='F'+str(count[0]);count[0]+=1;return z
    return t[0],fill(t[1],count),fill(t[2],count)
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def profile(a):
    events=[]
    for d,u in a.items():events.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    live=set();peak=0
    for t,d in sorted(events):
        if d in live:live.remove(d)
        else:live.add(d);peak=max(peak,len(live))
    assert not live;return peak
T=fill(N(3,N(2,N(1)),N(6,N(4,None,N(5)),N(7,None,N(10,N(8,None,N(9)),N(11,None,N(12,None,N(13))))))))
def body(strong):
    word=[('D',x) for x in range(13,0,-1)]
    word += [('D',x) for x in (12,1,11,1,13,1,12,1,11,13,1,7,1,13,1,13,7)]
    tags={'preparation':len(word)+1};word.append(('K',7));root=7
    if strong:word.append(('D',1))
    tags['helper']=len(word)+1;word.append(('K',13));tags['comb']=len(word)+1;word.append(('K',1));root=1
    def padded(k):
        nonlocal root
        z=13 if root!=13 else 1
        word.extend([('D',z),('D',root)]*2);word.append(('K',k));root=k
    for k in (3,7,3,13,3,7,3):padded(k)
    for k in (9,7,13,7):padded(k)
    for k in (11,7,11):padded(k)
    for k in (5,3,7,3):padded(k)
    padded(3)
    return word,tags
def auxiliary(rows):
    ans=[]
    for r in rows:
        mode='D' if r['mode']=='K' and r['target']==11 else r['mode'];bb,aa=r['before'],r['after']
        ans.append(dict(r,mode=mode,genuine_F=mode=='K' and bb[2][0]!=r['target'],qF=r['qE'],qE=0,
            before=(bb[0],bb[2],bb[2]),after=(aa[0],aa[2],aa[2])))
    return ans
def main():
    assert C.p.labels(C.p.core(T,C.M))==set(range(1,14))
    weak,tags0=body(False);strong,tags1=body(True)
    _,first=C.replay(T,T,T,weak);assert first[1]==T
    # A's initial reset and fixed preparation make its end identical on
    # every repetition. BE is recurrent under the exact KEEP subsequence.
    ee=T;seen={};states=[]
    while ee not in seen and len(states)<12:
        seen[ee]=len(states);states.append(ee)
        for mode,x in weak:
            if mode=='K' and x!=11:ee=C.tr(ee,x)[0]
    assert ee in seen;u=seen[ee];ell=len(states)-u;warm=max(1,u)
    prefix=weak*warm;_,initial=C.replay(T,T,T,prefix)
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
    import cd6_allocator as A
    from source_funding import own_map
    from branch_funding import build as high
    reports=[]
    for name,bb,tags in (('weak_zero_helper',weak,tags0),('strong_paid_helper',strong,tags1)):
        period=bb*ell;rr,end=C.replay(*initial,period);assert end==initial
        localaux=auxiliary(rr);sm=A.allocate(localaux);k=sm['core'];cut=0
        if k>=9:backend=high(localaux);cut=backend['packet_receipt'][0]['occurrences'][0]-1
        elif k==8:
            backend=A.core8(localaux,A.cert8());cut=backend['macros'][backend['full_cut_before_macro']]['occurrences'][0]-1
        else:backend={'full_cut_before_macro':0,'working_units':4,'source_scope':'certified direct/core7 source rule'}
        actualprefix=prefix+period[:cut];_,start=C.replay(T,T,T,actualprefix);word=period[cut:]+period[:cut];rows,end=C.replay(*start,word);assert end==start;base=len(actualprefix);Tlen=len(period)
        for r in rows:r['occurrence']+=base
        def tau(t):return base+(t-cut if t>cut else Tlen+t-cut)
        ta=[{key:tau(t+i*len(bb)) for key,t in tags.items()} for i in range(ell)]
        aux=auxiliary(rows);sm=A.allocate(aux);f6=sm['f'];full=C.L.build(rows,C.M);mm=C.L.macros(rows);D,U=full['D'],full['U'];H=dict(full['h0'])
        combs=[]
        for t in ta:
            m=next(m for m in full['macros'] if t['comb'] in m['occurrences']);hp=next(m for m in full['macros'] if t['helper'] in m['occurrences'])
            assert (m['H'],m['Q'],len(m['branch']),m['z'])==(1,3,3,1)
            assert (hp['H'],hp['Q'],len(hp['branch']),hp['z'])==((2 if name.startswith('strong') else 1),2,1,1)
            prep=next(m for m in mm if t['preparation'] in m['occurrences']);missing=(t['comb'],3);assert missing not in H
            H[missing]=prep['units'][1]
            firstrow=next(r for r in rows if r['occurrence']==hp['occurrences'][0]);lastrow=next(r for r in rows if r['occurrence']==hp['occurrences'][-1])
            par,children=C.L.marked_tree(firstrow['before'][1],C.M);_,newch=C.L.marked_tree(lastrow['after'][1],C.M)
            bp=sum(len(v)>=2 for v in children.values());bt=sum(len(v)>=2 for v in newch.values())
            combs.append({'tags':t,'comb_profile':m,'helper_profile':hp,'original_comb_price':-1,'leaf_comb_change':-1,
                'comb_rho':-2,'helper_rho':2*min(hp['H'],3)-2,'pair_rho':2*min(hp['H'],3)-4,
                'shifted_branch_potential_helper_residual':2*min(hp['H'],3)-hp['Q']+(len(hp['leaf_after'])-bt-1)-(len(hp['leaf_before'])-bp-1)})
        assert set(H)==D and len(set(H.values()))==len(D) and all(H[d]==u for d,u in full['h0'].items())
        X=load('C29_owner_exchange',P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py');common={d:u for d,u in f6.items() if d in D}
        nat=X.exchange(D,U,common,full['h0']);a=nat['allocation'];old=dict(a);z=C.L.augment_partial(D,U,a,full['h']);a=z['allocation'];assert all(a[d]==u for d,u in old.items())
        prior=dict(a);inv={u:d for d,u in a.items()};paths=[]
        for root in sorted(D-set(a)):
            d=root;steps=[];visited=set()
            while True:
                assert d not in visited;visited.add(d);u0=H[d];steps.append((d,u0))
                if u0 not in inv:break
                d=inv[u0]
            a[root]=u0;paths.append({'root':root,'steps':steps,'terminal':u0})
        assert set(a)==D and len(set(a.values()))==len(a) and all(a[d]==u for d,u in prior.items()) and profile(a)<=25
        assert all(C.p.labels(C.p.core(r['before'][1],C.M))==set(range(1,14)) for r in rows)
        reports.append({'source_id':'C29-'+name,'original_diagonal_tree':T,'body':bb,'reaching_prefix':actualprefix,
            'period':word,'initial':start,'rows':rows,'actual_interval':[base+1,base+len(word)],'tags':ta,
            'erased_key':11,'BE_recurrence':{'u':u,'L':ell},'aux_core':k,'aux_cut':cut,
            'f6_mode':'accepted canonical raw; no pre-existing nested five-key map supplied on this NEW source',
            'f6':pack(f6),'common_locked':pack(common),'natural_prior':pack(nat['allocation']),
            'leaf_comparison':pack(full['h']),'effective_prefix':pack(prior),'full_independent_H':pack(H),
            'final_full_a':pack(a),'paths':paths,'H_peak':profile(H),'a_peak':profile(a),
            'comb_receipts':combs,'signed_period_rho':sum(2*min(m['H'],3)-len(m['branch'])-m['z'] for m in full['macros']),
            'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),
            'historical_maps_modified':False,'counterclaim':('immediate predecessor always pays rho-comb; D0=L-B-1 is globally valid' if name.startswith('weak') else None)})
        assert C.queries<3100
    out('comb_source_fixtures.json',{'status':'PRODUCER_EXACT_COMB_SOURCE_AND_SIGNED_COUNTERCERTIFICATES_PENDING_INDEPENDENT_AUDIT',
        'reports':reports,'claims_not_refuted':['Coarse-Double','Universal CD','Dynamic Optimality','all possible signed repayment mechanisms'],
        'source_queries':C.queries})
    print(json.dumps({'status':'COMB_FIXTURES_CONSTRUCTED','queries':C.queries,
        'reports':[{'id':r['source_id'],'length':len(r['period']),'aux_core':r['aux_core'],'cut':r['aux_cut'],
            'pair_rho':[z['pair_rho'] for z in r['comb_receipts']],'D0_helper':[z['shifted_branch_potential_helper_residual'] for z in r['comb_receipts']],
            'A':r['A'],'QF':r['QF'],'a_peak':r['a_peak']} for r in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
