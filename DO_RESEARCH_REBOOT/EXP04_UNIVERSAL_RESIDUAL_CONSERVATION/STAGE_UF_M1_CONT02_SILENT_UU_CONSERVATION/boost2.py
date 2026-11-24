from base2 import *
from coercion import coerce,advance
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze
from birthc import reconstruct
from native2 import adapter
from fast_physics import physical_replay,skeleton_cost
from independent import splay as ind
import gc,ast

def make(base,baseA,baseRaw,T=1):
    s=copy.deepcopy(base);m=s['critical_g'];low=s['low_guard'];high=s['high_guard'];M=s['max_core']
    def trim(st):return {'root':st['root'],'children':{j:[None if x in (low,high) else x for x in cs]
        for j,cs in st['children'].items() if int(j) not in (low,high)}}
    acore=trim(s['initial_A']);inner=list(range(m+1,M))
    ch={str(j):[None,None] for j in range(m,M+1)}
    ch[str(m)][1]=M;ch[str(M)][0]=inner[0]
    for a,b in zip(inner,inner[1:]):ch[str(a)][1]=b
    canon={'root':m,'children':ch}
    pre,st0=coerce(acore,canon);back,st1=coerce(canon,acore)
    h0={'root':2,'children':{'1':[None,None],'2':[1,3],'3':[None,4],'4':[None,None]}}
    h1={'root':1,'children':{'1':[None,4],'2':[None,3],'3':[None,None],'4':[2,None]}}
    w0,_=coerce(h0,h1);w1,_=coerce(h1,h0);lift={1:low,2:m,3:M,4:high}
    before=pre+[lift[x] for x in w0];after=[lift[x] for x in w1]+back
    mid,ca=advance(s['initial_A'],before)
    assert mid['root']==low and mid['children'][str(low)][1]==high
    assert mid['children'][str(high)][0]==m
    z,c=advance(mid,[high,low]);assert z==mid and c==2
    z,cb=advance(mid,after);assert z==s['initial_A']
    z,c=advance(s['initial_B'],[high,low]);assert z==s['initial_B'] and c==2
    b=(high-low).bit_length();bridge=ca+cb
    if T is None:
        assert b>9;T=(10*(baseA+bridge)-baseRaw)//(2*(b-9))+1
    initial_len=len(s['operations']);loop_start=initial_len+len(before)+1
    s['operations']+= [['D',x] for x in before]+[['K',x] for _ in range(T) for x in (high,low)]+[['D',x] for x in after]
    s.update(name=f'M1C2_guarded_padded_with_extreme_identity_T{T}',family='padded_chain_plus_paired_rootzig_replication',
        base_source_sha256=digest(base),replication=T,rootzig_loop_start=loop_start,
        rootzig_before_D=before,rootzig_after_D=after,rootzig_bridge_A=bridge,
        expected_A=baseA+bridge+2*T,expected_Q_B=None,
        expected_raw_periodic_cost=baseRaw+2*T*(1+b),base_operations=initial_len,
        source_legal_complete_closure_argument='Original paired-closed source followed by exact A-only bridge, paired full-state two-zig identities, and exact A-only reverse bridge.')
    return s

if __name__=='__main__':
    meter=Meter('rootzig_replication_attack')
    base=load(ROOT/'RUN_B_SOURCE_CATALOG.json')[4];row=load(ROOT/'RUN_B_RESULTS.json')[4]
    short=make(base,row['A'],row['raw_periodic_cost'],1);long=make(base,row['A'],row['raw_periodic_cost'],None)
    write('BOOST_SOURCE_CATALOG.json',[short,long]);pref=prefix_check(short)
    r,pool=replay(short);ff=scan_forest(r);fc=audit_forest(r,ff)
    p={'source':short['name'],'source_sha256':digest(short),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
       'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],
       'boundaries':r.boundaries,'state_pool':pool}
    f={'source':short['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
    w={'vertices':[{'parent':v,'type':d['type'],'w':0} for v,d in sorted(ff.items())],
       'R_overflow':0,'zero_reason':'Positive original raw periodic certificate on short source.'}
    assert r.A==short['expected_A'];an=analyze(short,p,f,w);birth=reconstruct(short,p,f,an,weights=w)
    native=adapter(short,p,birth)
    U={ast.literal_eval(k):v for k,v in birth['U'].items()};critical=[]
    for j,h in enumerate(short['critical_operations']):
        if j<2:continue
        v=(h,short['L']+1);u=(short['critical_operations'][j-1],short['L']+1)
        assert v in U and u in U and U[v]['creator']==u and not U[u]['exposed']
        assert ff[v]['type']=='C' and tuple(ff[v]['predecessor'])==u
        assert any(tuple(z['parent'])==v for z in birth['original_R6']);critical.append(v)
    assert len(critical)==short['k']-2
    start=short['rootzig_loop_start'];lrows=p['boundaries'][start-1:start+1]
    lo=lrows[0]['start_time'];hi=lrows[-1]['end_time'];template=p['events'][lo:hi]
    assert len(template)==4 and all(e['case']=='ZIG' for e in template)
    assert lrows[0]['pre_A_state']==lrows[-1]['post_A_state'] and lrows[0]['pre_B_state']==lrows[-1]['post_B_state']
    for label,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',birth)):
        write('BOOST_SHORT_'+label+'.json',z)
    short_summary={'source':short['name'],'source_sha256':digest(short),'prefix':pref,'A':r.A,'Q_B':r.Q,
        'operations':len(short['operations']),'primitives':r.T,'original_U':len(U),'original_R6':len(birth['original_R6']),
        'preserved_late_silent_UU_R6_parents':critical,'native_U_and_all_original_pairs_agree':True,
        'original_R_star':None,'scope':'Original R_star NOT_CLASSIFIED; independent/native U/cohort/R6 complete.'}
    expansion={'short_source_sha256':digest(short),'long_source_sha256':digest(long),'template_original_operations':[start,start+1],
        'template_primitive_slice_zero_based':[lo,hi],'template_events':template,'copies_in_long':long['replication'],
        'event_rule':'Keep prefix events times<=lo; for copy c=0..T-1 repeat template with time+=4c and original operation id[1]+=2c; suffix events time+=4(T-1), operation id[1]+=2(T-1). All other event fields unchanged.',
        'boundary_rule':'Repeat the two template rows, shifting t by2c and all primitive times by4c. Suffix t shifts2(T-1), primitive times4(T-1). State-pool IDs unchanged.',
        'B_double_rule':'No B doubles occur at or after the added loop. All B double original IDs and event times unchanged.',
        'full_state_template_identity_verified':True,'only_real_A_bits':True,
        'internal_SET_Pi_U_cohort_invariance':'New copies change only two boundary labels at extreme roots; internal original F/J labels and their B creation/loss/inside-hit chronology unchanged. No original U producer added or removed relative to short.',
        'scan_invariance':'Both extrema are in initial I and S with at least two intervening ranks; repeated opposite-extreme blocks make no long consecutive-rank scan. The original short-source boundary blocks are preserved.'}
    write('BOOST_EVENT_EXPANSION.json',expansion)
    del r,pool,p,f,w,an,birth,native,ff,U;gc.collect()
    fast=physical_replay(long)
    assert fast['A']==long['expected_A'] and fast['Q_B']==row['Q_B']
    S=set(range(1,long['high_guard']+1));xs=[x for tag,x in long['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(S))}
    raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
    assert raw==long['expected_raw_periodic_cost']>10*fast['A']
    norms=[skeleton_cost(fast,variant=v) for v in ('G','H')]
    assert all(z['eligible_periodic'] for z in norms)
    ls=long['rootzig_loop_start'];le=ls+2*long['replication']
    assert all(not any(ls<=h<le for h in z['retained_original_operations']) for z in norms)
    states={};codes=[];rr=[]
    for z in fast['rows']:
        code=z['B_code']
        if code not in states:states[code]=len(codes);codes.append(format(code,'x'))
        rr.append({**{k:v for k,v in z.items() if k!='B_code'},'B_state':states[code]})
    write('BOOST_LONG_FAST_STATES.json',{'n':long['high_guard'],'code_format':'M0 full labelled child-pointer integer code, hex',
        'states':codes,'rows':rr,'full_A_B_return_verified':True,'every_operation_full_tree_incremental_replay':True,
        'independent_immutable_scope':'Complete short source plus exact two-zig event/state replication lemma; not a second full tuple reconstruction for every long-loop copy.'})
    long_summary={'source':long['name'],'source_sha256':digest(long),'replication':long['replication'],'A':fast['A'],
        'Q_B':fast['Q_B'],'operations':len(long['operations']),'raw_periodic_cost':raw,
        'raw_periodic_eligible':False,'G_H_periodic_certificates':norms,
        'U_R6_scope':'Exact insertion/replication law from fully independently/native-checked short source; no full long native Pi/R_star rerun claimed.',
        'inherited_late_silent_UU_R6_parents':critical,'actual_S_UU':0,
        'zero_reason':'Positive original guarded and hard-guarded periodic certificates; cheap D quota applies unchanged.'}
    write('BOOST_RESULTS.json',{'short':short_summary,'long':long_summary})
    meter.info.update(fresh_complete_sources=2,long_operations=len(long['operations']));meter.ok=True
    print('PASS boost short/long',len(short['operations']),len(long['operations']),'copies',long['replication'],
        'raw',raw,'10A',10*fast['A'],'G/H',[z['B_cyclic'] for z in norms],flush=True)
