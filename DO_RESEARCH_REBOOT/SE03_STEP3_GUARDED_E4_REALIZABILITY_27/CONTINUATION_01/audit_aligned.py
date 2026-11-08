"""Final actual-period source and frozen-owner receipt; original cut realized."""
import collections,json,sys,time
import audit_construct as C
B=C.B;P=C.P;p=C.p;L=C.L;M=C.M;V=C.V
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(x):return tuple(fr(y) for y in x) if isinstance(x,list) else x
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def pending_peak(f):
    events=[]
    for d,u in f.items():events.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    live=set();peak=0
    for key,d in sorted(events):
        if d in live:live.remove(d)
        else:live.add(d);peak=max(peak,len(live))
    assert not live;return peak
def main():
    cand=json.loads((B/'construction_candidate.json').read_text());old=json.loads((B/'owner_receipt.json').read_text())
    body=[tuple(x) for x in cand['period']];T=len(body);cut=old['six_key_source_packet_receipts'][0]['occurrences'][0]-1
    assert cut==141
    prefix=[tuple(x) for x in cand['original_reaching_prefix']]+body*2+body[:cut]
    _,initial=C.replay(V,V,V,prefix);word=body[cut:]+body[:cut];rows,end=C.replay(*initial,word)
    assert end==initial;base=len(prefix)
    for r in rows:r['occurrence']+=base
    def tau(t):return base+(t-cut if t>cut else T+t-cut)
    tags={k:tau(t) for k,t in cand['tags'].items()}
    by={r['occurrence']:r for r in rows};aux=[]
    for r in rows:
        mode='D' if r['mode']=='K' and r['target']==11 else r['mode'];bb,aa=r['before'],r['after']
        aux.append(dict(r,mode=mode,genuine_F=mode=='K' and bb[2][0]!=r['target'],qF=r['qE'],qE=0,
            before=(bb[0],bb[2],bb[2]),after=(aa[0],aa[2],aa[2])))
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
    from cd6_allocator import allocate
    from branch_funding import build
    small=allocate(aux);f6=small['f'];local=[dict(r,occurrence=i+1) for i,r in enumerate(aux)]
    raw=build(local);assert raw['full_cut_before_packet']==0
    def back(t):return base+t[0],*t[1:]
    transported={(tau(z['demand'][0]),*z['demand'][1:]):(tau(z['unit'][0]),*z['unit'][1:]) for z in old['f6']}
    assert transported==f6
    full=L.build(rows,M);D,U=full['D'],full['U'];lock={d:u for d,u in f6.items() if d in D}
    X=C.mod('exchange27aligned',P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
    nat=X.exchange(D,U,lock,full['h0']);a=nat['allocation'];stages=[]
    def stage(name,h):
        nonlocal a
        prior=dict(a);v=L.augment_partial(D,U,a,h);a=v['allocation'];assert all(a[d]==u for d,u in prior.items())
        stages.append({'name':name,'comparison':pack(h),'prior':pack(prior),'additions':pack(v['additions']),
            'after':pack(a),'blocked':[(d,f) for d,f in sorted(v['blocked_frontier'].items())],'paths':v['paths']})
    v,profile,creator,transport=C.selection(rows)
    hc=dict(full['h'])
    for q in creator:hc[tuple(q['demand'])]=tuple(q['unit'])
    ht=dict(hc)
    for z in transport:ht[tuple(z['origin'])]=ht.pop(tuple(z['birth']))
    hp=dict(ht);birthgroups=collections.defaultdict(list);mm=L.macros(rows);own=[]
    for z in transport:birthgroups[z['birth_macro']].append(tuple(z['birth']))
    for i,dd in sorted(birthgroups.items()):
        free=[u for u in mm[i]['units'] if u not in hp.values()]
        for d,u in zip(sorted(dd),free):hp[d]=u;own.append({'demand':d,'unit':u})
    for name,h in (('leaf_channels',full['h']),('protected_creators',hc),('T19_independent_comparison',ht),('first_own_tail',hp)):stage(name,h)
    jm=next(m for m in mm if tags['j'] in m['occurrences']);jd=jm['units'][2]
    assert jd not in hp.values()
    hj=dict(hp);missing_births=[tuple(z['birth']) for z in transport if z['birth'][0]==tags['e'] and tuple(z['birth']) not in hj]
    assert len(missing_births)==1;hj[missing_births[0]]=jd;stage('C22_protected_j_ordinal3',hj)
    # One source-exact extra high-gap bit, independent of total cardinality.
    gap=next(m for m in mm if tags['gap1'] in m['occurrences']);gd=gap['units'][8]
    assert gap['H']>=8 and gd not in f6.values() and gd not in full['h0'].values() and gd not in hj.values()
    assert gd not in a.values()
    unpaid=sorted(D-set(a));assert len(unpaid)==1
    a_before_extra=dict(a);a[unpaid[0]]=gd;assert set(a)==D and len(set(a.values()))==len(D)
    assert all(a[d]==u for d,u in a_before_extra.items())
    uv=(tags['v'],1,1);ed=(tags['e'],4);assert f6[ed]==uv and a[ed]==uv
    assert all(a[d]==u for d,u in lock.items())
    # Original nonidentity flip: skip only this proof-comparison block.
    shadow=by[tags['h']]['after'][0];shadow,sp,se=C.tr(shadow,7)
    assert shadow==by[tags['e']]['after'][0] and len(se)==2
    flip={'original_A_events':sum(by[tags[k]]['a'] for k in ('g','s','t','v','p')),
        'full_B_doubles':sum(by[tags[k]]['qF'] for k in ('g','s','t','v','p')),
        'shadow_e_path':sp,'shadow_e_events':se,'original_e_path':by[tags['e']]['A_path'],
        'rejoin_exact':True,'repair_units':[(tags['p'],1,0),(tags['p'],1,1)],'corrected_R_balance':0}
    receipts=[]
    for q in raw['packet_receipt']:
        receipts.append(dict(q,occurrences=[base+t for t in q['occurrences']],
            selected_spares=[back(u) for u in q['selected_spares']],fixed_own_units=[back(u) for u in q['fixed_own_units']],
            new_pairs=[(back(d),back(u)) for d,u in q['new_pairs']],carry=[back(u) for u in q['carry']]))
    peaks={'raw_h6_working':raw['working_units'],'f6_endpoint_buffer':pending_peak(f6),'full_frozen_endpoint_buffer':pending_peak(a)}
    assert max(peaks.values())<=25
    out('aligned_source_and_owners.json',{'status':'EXACT_SOURCE_AND_FULL_OWNER_RECEIPT_PENDING_DISTINCT_IMPLEMENTATION_AUDIT',
        'original_common_tree':V,'reaching_prefix':prefix,'period':word,'initial':initial,'rows':rows,'tags':tags,
        'actual_interval':[base+1,base+T],'body_cut_after':cut,'body_length':T,'six_key_core':small['core'],
        'f6_mode':'accepted canonical raw; no applicable original Step1 five-key/core9 instance',
        'original_Step1_domains':old['original_Step1_domains'],'f6':pack(f6),'h6_natural':pack(small['h0']),
        'h6_packet_receipts':receipts,'h6_max_debt':raw['max_debt_on_period'],'h6_cut_packet':0,
        'full_h0':pack(full['h0']),'leaf_comparison':pack(full['h']),'common_locked':pack(lock),'natural_prior':pack(nat['allocation']),
        'creator_claims':profile['claims'],'creator_pairs':creator,'selected_transports':transport,
        'selected_at_e':[z for z in transport if z['birth'][0]==tags['e']],
        'own_tail_pairs':own,'policy_stages':stages,'j_donor':jd,'j_paid_comparison_hole':missing_births[0],
        'source_gap_donor':gd,'gap_macro_H':gap['H'],'extra_payment':{'demand':unpaid[0],'unit':gd},
        'final_full_allocation':pack(a),'all_frozen_successes_preserved':True,'uv':uv,'uv_full_owner':ed,
        'flip':flip,'Bank25':25,'working_peaks':peaks,
        'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),
        'independent_audit':False})
    print(json.dumps({'status':'ALIGNED_COMPLETE_SOURCE_AND_OWNER_RECEIPT','actual_interval':[base+1,base+T],
        'tags':tags,'peaks':peaks,'selected_at_e':[z for z in transport if z['birth'][0]==tags['e']],
        'uv':uv,'owner':ed,'extra_payment':{'demand':unpaid[0],'unit':gd}}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_aligned_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries})
