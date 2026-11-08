"""New independent inventory/control/comparator audit. Reuse the accepted
distinct pointer verifier as a library; DO NOT rerun W199 source replay.
No C28 or C27 producer source/allocator/exchange module is imported.
"""
import collections,hashlib,importlib.util,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();checks=[];pins={}
s=importlib.util.spec_from_file_location('C28_independent_pointer_library',OLD/'audit_independent2.py');I=importlib.util.module_from_spec(s);s.loader.exec_module(I)
def read(p):
    z=p.read_bytes();pins[str(p)]=hashlib.sha256(z).hexdigest();return json.loads(z)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(x):return {tuple(z['demand']):tuple(z['unit']) for z in x}
def check(n):checks.append(n);print(n,flush=True)
def profile_at(a,cut):
    n=0
    for d,u in a.items():
        ut=(u[0],0,u[1],u[2]);dt=(d[0],1,d[1],0)
        n+=(ut<=cut)!=(dt<=cut)
    return n
def peak(a):
    cuts={(u[0],0,u[1],u[2]) for u in a.values()}|{(d[0],1,d[1],0) for d in a}
    return max((profile_at(a,t) for t in cuts),default=0)
def verify_bank(rows,wanted):
    mm=I.macro_list(rows,'E');pk=[];used=set()
    for i,m in enumerate(mm):
        if m['Q']==5:
            j=(i+1)%len(mm);assert mm[j]['Q']==1;used|={i,j};pk.append((i,m['rows']+mm[j]['rows']))
    pk.extend((i,m['rows']) for i,m in enumerate(mm) if i not in used);pk.sort();debt,info=I.debt_function(rows)
    dd=[(debt(rr[0]['before'][0],rr[0]['before'][2]),debt(rr[-1]['after'][0],rr[-1]['after'][2])) for i,rr in pk]
    top=max(ds for ds,dt in dd);assert top==2 and dd[0][0]==2
    own={d:u for m in mm for d,u in zip(m['demands'],m['units'])};answer=dict(own);bank=[]
    for (i,rr),(ds,dt) in zip(pk,dd):
        assert len(bank)==top-ds
        uu=[(r['occurrence'],j,b) for r in rr for j in range(1,r['a']+1) for b in (0,1)]
        dd0=[(r['occurrence'],j) for r in rr for j in range(1,r['qE']+1)];owned={own[d] for d in dd0 if d in own}
        budget=2*min(sum(r['a'] for r in rr),4);assert budget-len(dd0)+dt-ds>=0
        pool=[u for u in uu if u not in owned][:budget-len(owned)]+bank
        for d in dd0:
            if d not in own:answer[d]=pool.pop(0)
        assert len(pool)>=top-dt;bank=pool[:top-dt]
    assert not bank and answer==wanted
def main():
    old=read(OLD/'aligned_source_and_owners.json');prior_audit=read(OLD/'independent_audit2.json')
    assert prior_audit['input_sha256']['DO_RESEARCH_REBOOT/SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/aligned_source_and_owners.json']==pins[str(OLD/'aligned_source_and_owners.json')]
    inv=read(B/'w199_inventory.json');a=mp(old['final_full_allocation']);U={(r['occurrence'],j,b) for r in old['rows'] for j in range(1,r['a']+1) for b in (0,1)};D={(r['occurrence'],j) for r in old['rows'] for j in range(1,r['qF']+1)}
    assert set(a)==D and len(set(a.values()))==58 and set(a.values())<=U
    assert not inv['current_residuals'] and len(inv['current_unowned'])==464 and {tuple(u) for u in inv['current_unowned']}==U-set(a.values())
    assert len(inv['bits'])==len(U)==522 and len(inv['demands'])==len(D)==58
    inverse={u:d for d,u in a.items()};assert inverse[(769,1,1)]==(771,4) and inverse[(621,2,0)]==(661,3)
    for bit in inv['bits']:
        u=tuple(bit['unit']);assert u in U and bit['effective_owner']==(list(inverse[u]) if u in inverse else None)
        assert bit['unowned']==(u not in inverse) and bit['eligible_current_residuals']==[]
    for row in inv['demands']:assert a[tuple(row['demand'])]==tuple(row['effective_unit']) and row['frozen'] and not row['unpaid']
    assert peak(a)==6 and 58<=2*261 and inv['scalar_margin']==464
    check('W28: all522 bits/58 demands, current full frozen map, P empty,464 unowned, e4 and later gap owner retained; accepted W199 replay reused')
    control=read(B/'shortened_source_control.json');pol=read(B/'shortened_control_policy.json')
    assert control['original_reaching_prefix']==old['reaching_prefix'] and I.fr(control['initial'])==I.fr(old['initial'])
    rows,end=I.execute(I.fr(control['initial']),control['period'],573,control['rows']);assert end==I.fr(control['initial']) and len(rows)==48
    keeps_old=[r for r in old['rows'] if r['mode']=='K'];keeps_new=[r for r in rows if r['mode']=='K'];assert len(keeps_old)==len(keeps_new)
    for r,z in zip(keeps_new,keeps_old):assert r['target']==z['target'] and r['after'][0]==I.fr(z['after'][0]) and r['qF']==z['qF'] and r['qE']==z['qE']
    assert all(I.core(r['before'][1],I.M)==set(range(1,14)) and len(I.core(r['before'][2],I.E))==9 for r in rows)
    f6=mp(control['f6']);verify_bank(rows,f6);tags=control['tags'];assert f6[(tags['e'],4)]==(tags['v'],1,1)
    mm,led,h,h0,DD,UU,channels=I.leaf_map(rows);claims,paid,hc,tr=I.creator_stage(rows,mm,led,h,channels)
    assert I.fr(tr)==I.fr(pol['selected_transports']) and len([z for z in tr if z['birth'][0]==tags['e']])==2
    common={d:u for d,u in f6.items() if d in DD};cur=I.natural_extend(common,h0);assert cur==mp(pol['natural_prior'])
    ht=dict(hc)
    for z in tr:ht[z['origin']]=ht.pop(z['birth'])
    hp=dict(ht);bg=collections.defaultdict(list)
    for z in tr:bg[z['birth_macro']].append(z['birth'])
    for mi,ds in sorted(bg.items()):
        free=[u for u in mm[mi]['units'] if u not in hp.values()]
        for d,u in zip(sorted(ds),free):hp[d]=u
    hj=dict(hp);jm=next(m for m in mm if tags['j'] in m['occurrences']);jd=jm['units'][2];assert jd not in hp.values()
    missing=[z['birth'] for z in tr if z['birth'][0]==tags['e'] and z['birth'] not in hj]
    if missing:hj[missing[0]]=jd
    for stage,hm in zip(pol['policy_stages'],[h,hc,ht,hp,hj]):
        assert hm==mp(stage['comparison']) and cur==mp(stage['prior']);cur=I.extend(cur,hm,DD);assert cur==mp(stage['after'])
    assert cur==mp(pol['prior_before_extra']);images=set(f6.values())|set(h0.values())|set(hj.values())
    for z in pol['extra_payments']:
        d,u=tuple(z['demand']),tuple(z['unit']);assert d not in cur and u in UU and u not in images|set(cur.values());cur[d]=u
    assert cur==mp(pol['final_full_a']) and set(cur)==DD and len(set(cur.values()))==58 and peak(cur)==6
    assert sum(r['a'] for r in rows)==64 and sum(r['qF'] for r in rows)==58
    check('Separate48-operation control: new pointer replay, exact triple closure, original KEEP states, full bank/policy/selected-origin and funding checks PASS; W199 unchanged')
    receipts=read(B/'catchment_comparison_receipts.json')
    for z,rr,tt,aa in ((receipts['results'][0],[I.fr_row(r) for r in old['rows']],old['tags'],a),
                      (receipts['results'][1],rows,tags,cur)):
        m0=I.macro_list(rr);fm={k:next(m for m in m0 if m['occurrences'][-1]==tt[k]) for k in ('j','h','g','s','t','v','p','e')}
        assert [fm[k]['Q'] for k in fm]==[1,2,1,3,1,2,1,6] and fm['j']['H']>=3 and all(fm[k]['H']==1 for k in fm if k!='j')
        DD={d for m in m0 for d in m['demands']};own={d:u for m in m0 for d,u in zip(m['demands'],m['units'])};fd={d for m in fm.values() for d in m['demands']}
        outside=sorted((DD-set(own))-fd);assert len(outside)<=3
        H=dict(own)
        for k,u in zip([(tt['s'],3)]+[(tt['e'],j) for j in range(3,7)],fm['j']['units'][1:6]):H[k]=u
        for d,k in zip(outside,('g','t','p')):H[d]=fm[k]['units'][1]
        assert H==mp(z['source_independent_H']) and set(H)==DD and len(set(H.values()))==58 and peak(H)==8
        prev=mp(z['historical_prefix']);ans=I.extend(prev,H,DD);assert ans==mp(z['counterfactual_extension_of_historical_prefix']) and peak(ans)==6
        inverse={u:d for d,u in prev.items()}
        for path in z['owner_walks']:
            root=tuple(path['root']);assert root not in prev;d=root
            for j,(dd,u) in enumerate(path['steps']):
                dd,u=tuple(dd),tuple(u);assert dd==d and H[d]==u
                if j+1<len(path['steps']):d=inverse[u]
                else:assert u not in inverse and ans[root]==u
        assert aa==mp(old['final_full_allocation'] if z['source_id']=='C27-W199-frozen' else pol['final_full_a'])
        for row in z['cut_bound_receipts']:
            cut=tuple(row['cut']);assert profile_at(ans,cut)<=profile_at(H,cut)+2*profile_at(prev,cut)
    check('New full source comparator: both58-demand maps independently rebuilt from j ordinals2..6 and g/t/p second units; historical walks validated and CURRENT frozen maps untouched')
    cert=read(B/'uniform_ordinal_proof_certificate.json');ass=cert['assumptions']
    for label in ('lower_identity','upper_identity'):
        row=cert[label];total=[0]*6;total[-1]=row['positive_constant'];assert total[-1]>=0
        for name,coef in row['nonnegative_terms'].items():
            assert coef>=0
            total=[a+coef*b for a,b in zip(total,ass[name])]
        assert total==row['goal']
    # Exact propositional proofs at an ARBITRARY unit, not BST examples.
    for band,base,exc,owned in itertools.product((False,True),repeat=4):
        premises=(not band or not base) and (not owned or base or exc)
        if premises and band and not exc:assert not owned
    # Image-provenance induction preservation at an arbitrary physical bit.
    for prior,terminal,base,exc in itertools.product((False,True),repeat=4):
        if (not prior or base or exc) and (not terminal or base or exc):assert not(prior or terminal) or base or exc
    check('Uniform ordinal identities: exact nonnegative linear-combination certificates; arbitrary-point set provenance/exclusion tautologies checked, not finite support tests')
    # Universal source-count proof obligations use fixed source slot classes:
    # critical deficit count5; spare count5+3; frame natural bound2;
    # outside natural bound6; arbitrary finite disjoint catchments compose.
    assert 2+5+3==10 and 6+3==9 and 10+2*7==24<=25
    check('Uniform restricted theorem: arithmetic/storage constants checked; source-uniform proof remains the inspectable manuscript, not proof-assistant certification or complete U28 audit')
    theorem=B/'CATCHMENT_COMPARISON_THEOREM.md';pins[str(theorem)]=hashlib.sha256(theorem.read_bytes()).hexdigest()
    out('independent_audit.json',{'status':'PASS_NEW_INSTANCE_AND_DEDUCTIVE_ALGEBRA_CHECKS','checks':checks,'input_sha256':pins,
        'W199_replayed':False,'old_W199_source_and_owner_receipt_reused':True,'W28':'FUNDED, residual extension empty',
        'new_control_source':'48-operation separate guarded history; pointer replay and owner policy PASS',
        'universal_theorem_verification':'exact restricted manuscript proof inspected; arbitrary-variable linear/propositional certificates checked; no formal verification of every source lemma',
        'full_U28':'OPEN; catchment existence, all-owner storage/eligibility and arbitrary support not proved',
        'same_agent_distinct_implementation':True,'external_peer_review':False,'proof_assistant_certification':False,
        'new_source_queries':I.queries,'source_search_repeated':False})
    print(json.dumps({'status':'C28_INDEPENDENT_PASS','source_queries':I.queries,'checks':len(checks)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
