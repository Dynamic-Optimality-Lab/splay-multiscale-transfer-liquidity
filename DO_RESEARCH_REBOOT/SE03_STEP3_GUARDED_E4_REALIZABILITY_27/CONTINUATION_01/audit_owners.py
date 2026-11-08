"""Producer actual accepted h6 receipt and immutable full policy stages."""
import collections,importlib.util,json,sys,time
import audit_construct as C
B=C.B;P=C.P;p=C.p;L=C.L;M=C.M;calls0=C.calls
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(x):return tuple(fr(z) for z in x) if isinstance(x,list) else x
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def main():
    data=json.loads((B/'construction_candidate.json').read_text());rows=[dict(r,before=fr(r['before']),after=fr(r['after'])) for r in data['rows']]
    aux=[]
    for r in rows:
        mode='D' if r['mode']=='K' and r['target']==11 else r['mode'];bb,aa=r['before'],r['after']
        aux.append(dict(r,mode=mode,genuine_F=mode=='K' and bb[2][0]!=r['target'],qF=r['qE'],qE=0,
            before=(bb[0],bb[2],bb[2]),after=(aa[0],aa[2],aa[2])))
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
    from cd6_allocator import allocate
    from branch_funding import build
    small=allocate(aux);backend=build(aux);f6=small['f'];assert f6==backend['h']
    tags=data['tags'];uv=(tags['v'],1,1);ed=(tags['e'],4)
    assert f6[ed]==uv
    bank_v=next(r for r in backend['packet_receipt'] if tags['v'] in r['occurrences'])
    bank_p=next(r for r in backend['packet_receipt'] if tags['p'] in r['occurrences'])
    bank_e=next(r for r in backend['packet_receipt'] if tags['e'] in r['occurrences'])
    assert bank_p['carry'][1]==uv and (ed,uv) in bank_e['new_pairs']
    # Discover actual domains of the older special Step1 allocator, without
    # assuming its five-key/core9 theorem covers smaller cores.
    f5_domains=[]
    for z in sorted(M-{11}):
        e=fr(data['original_common_tree'])
        for mode,x in data['original_reaching_prefix']:
            if mode=='K' and x not in (11,z):e=C.tr(e,x)[0]
        history=[];seen={}
        while e not in seen and len(history)<30:
            seen[e]=len(history);history.append(e)
            for mode,x in data['period']:
                if mode=='K' and x not in (11,z):e=C.tr(e,x)[0]
        assert e in seen
        f5_domains.append({'additional_erasure':z,'u':seen[e],'L':len(history)-seen[e],
            'core':len(p.labels(p.core(e,M-{11,z}))),
            'inherited_special_Step1_scope':len(p.labels(p.core(e,M-{11,z})))==9})
    full=L.build(rows,M);D,U=full['D'],full['U'];locked={d:u for d,u in f6.items() if d in D}
    X=C.mod('exchange27owner',P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
    natural=X.exchange(D,U,locked,full['h0']);a=natural['allocation'];stages=[]
    def stage(name,h):
        nonlocal a
        old=dict(a);v=L.augment_partial(D,U,a,h);a=v['allocation'];assert all(a[d]==u for d,u in old.items())
        stages.append({'name':name,'comparison':pack(h),'prior':pack(old),'additions':pack(v['additions']),
            'after':pack(a),'blocked':[(d,f) for d,f in sorted(v['blocked_frontier'].items())],'paths':v['paths']})
    stage('leaf_channels',full['h'])
    hc=dict(full['h'])
    for q in data['creator_pairs']:hc[tuple(q['demand'])]=tuple(q['unit'])
    stage('protected_creators',hc)
    ht=dict(hc)
    for z in data['selected_transports']:
        birth=tuple(z['birth']);origin=tuple(z['origin']);assert birth in ht and origin not in ht
        ht[origin]=ht.pop(birth)
    stage('T19_independent_transposed_comparison',ht)
    hp=dict(ht);own_pairs=[];mm=L.macros(rows);by_birth=collections.defaultdict(list)
    for z in data['selected_transports']:by_birth[z['birth_macro']].append(tuple(z['birth']))
    for mi,demands in sorted(by_birth.items()):
        free=[u for u in mm[mi]['units'] if u not in hp.values()]
        for d,u in zip(sorted(demands),free):hp[d]=u;own_pairs.append({'demand':d,'unit':u})
    stage('first_own_tail_after_preserved_creators',hp)
    assert a[ed]==uv and all(a[d]==u for d,u in locked.items())
    ce=int((tags['e'],1,1) in {tuple(q['unit']) for q in data['creator_pairs']})
    out('owner_receipt.json',{'status':'PRODUCER_ACTUAL_CANONICAL_OWNER_RECEIPT_PENDING_INDEPENDENT_CHECK',
        'f6_mode':'canonical raw; no older fixed f5 supplied on this new source',
        'original_Step1_domains':f5_domains,'special_Step1_not_extended':True,'six_key_core':small['core'],
        'six_key_marks':sorted(small['marks']),'six_key_fixed_core':sorted(small['fixed_full_core']),
        'f6':pack(f6),'raw_h6':pack(small['h']),'h6_natural':pack(small['h0']),
        'six_key_source_packet_receipts':backend['packet_receipt'],'six_key_cut_packet':backend['full_cut_before_packet'],
        'six_key_max_debt':backend['max_debt_on_period'],'six_key_working_units':backend['working_units'],
        'bank_v':bank_v,'bank_p':bank_p,'bank_e':bank_e,'uv':uv,'raw_e4':ed,
        'full_natural':pack(full['h0']),'common_locked':pack(locked),'natural_prior':pack(natural['allocation']),
        'policy_stages':stages,'final_partial_a':pack(a),'remaining_full_unpaid':sorted(D-set(a)),
        'actual_full_uv_owner':next(d for d,u in a.items() if u==uv),'e_creator_spent_second_bit':ce,
        'own_tail_pairs':own_pairs,'source_engine_calls':C.calls,'source_queries':C.queries,
        'all_old_successes_preserved':True,'Bank25':25})
    print(json.dumps({'status':'ACTUAL_OWNER_RECEIPT_BUILT','core':small['core'],'uv':uv,'owner':next(d for d,u in a.items() if u==uv),
        'bank_lengths':[len(bank_v['carry']),len(bank_p['carry']),len(bank_e['carry'])],
        'f5_domains':f5_domains,'full_unpaid':len(D-set(a)),'c_e':ce}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_owners_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries,'backend_rows_supplied':199})
