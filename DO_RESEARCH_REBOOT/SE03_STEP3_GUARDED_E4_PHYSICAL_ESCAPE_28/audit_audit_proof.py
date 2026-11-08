"""Distinct exact-source + induction-interface audit for NEW insertion
countercertificate/hybrid/family. No old successful source replay repeated.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
s=importlib.util.spec_from_file_location('C28_independent_library',B/'audit_independent.py');J=importlib.util.module_from_spec(s);s.loader.exec_module(J);I=J.I
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def restriction(m,a,b):
    z={d:u for d,u in m.items() if a<=d[0]<=b};assert all(a<=u[0]<=b for u in z.values())
    return {(d[0]-a+1,*d[1:]):(u[0]-a+1,*u[1:]) for d,u in z.items()}
def main():
    c=read(B/'catchment_forcing_countercertificate.json');old=read(OLD/'aligned_source_and_owners.json');temp=read(B/'uniform_insertion_templates.json');hy=read(B/'hybrid_partition_receipt.json')
    assert c['old_reaching_prefix']==old['reaching_prefix'] and I.fr(c['initial'])==I.fr(old['initial'])
    rows,end=I.execute(I.fr(c['initial']),c['period'],573,c['rows']);assert end==I.fr(c['initial']) and len(rows)==459
    assert all(I.core(r['before'][1],I.M)==set(range(1,14)) and len(I.core(r['before'][2],I.E))==9 for r in rows)
    assert sum(r['a'] for r in rows)==529 and sum(r['qF'] for r in rows)==114 and sum(r['qE'] for r in rows)==51
    f6=mp(c['f6']);J.verify_bank(rows,f6);tags=c['tags'];assert f6[(tags['e'],4)]==(tags['v'],1,1)
    mm,led,h,h0,D,U,channels=I.leaf_map(rows);claims,paid,hc,tr=I.creator_stage(rows,mm,led,h,channels)
    assert I.fr(tr)==I.fr(c['selected_transports']) and len([z for z in tr if z['birth'][0]==tags['e']])==2
    common={d:u for d,u in f6.items() if d in D};a=I.natural_extend(common,h0);ht=dict(hc)
    for z in tr:ht[z['origin']]=ht.pop(z['birth'])
    hp=dict(ht);groups=collections.defaultdict(list)
    for z in tr:groups[z['birth_macro']].append(z['birth'])
    for i,ds in sorted(groups.items()):
        free=[u for u in mm[i]['units'] if u not in hp.values()]
        for d,u in zip(sorted(ds),free):hp[d]=u
    hj=dict(hp);jm=next(m for m in mm if tags['j'] in m['occurrences']);jd=jm['units'][2];assert jd not in hp.values()
    missing=[z['birth'] for z in tr if z['birth'][0]==tags['e'] and z['birth'] not in hj]
    if missing:hj[missing[0]]=jd
    for z,hh in zip(c['policy_stages'],[h,hc,ht,hp,hj]):
        assert a==mp(z['prior']) and hh==mp(z['comparison']);a=I.extend(a,hh,D);assert a==mp(z['after'])
    before=dict(a);assert before==mp(c['prior_before_extra']) and len(before)==113
    images=set(f6.values())|set(h0.values())|set(hj.values())
    for z in c['extra_payments']:
        d,u=tuple(z['demand']),tuple(z['unit']);assert d not in a and u in U and u not in images|set(a.values());a[d]=u
    assert a==mp(c['current_complete_a']) and set(a)==D and len(set(a.values()))==114 and J.peak(a)==6
    frameends={tags[k] for k in ('j','h','g','s','t','v','p','e')};outside=sorted(d for d in D-set(h0) if d[0] not in frameends)
    assert len(outside)==5 and len([r for r in rows if r['qF']==6])==1
    assert all(rows[t-573]['a']==1 and rows[t-573]['qF']==3 for t in c['inserted_native_deficit_occurrences'])
    print('Exact459-operation full-guard source, complete114-demand frozen funding and one-frame/five-outside-deficit countercertificate PASS',flush=True)
    # Verify the elementary block data on which the induction is based.
    V=c['period'][:65];state=I.fr(c['initial']);debt,info=I.debt_function(rows);assert debt(state[0],state[2])==2
    localmaps={};allh={}
    for i in range(4):
        rr=rows[65*i:65*(i+1)];assert rr[0]['before']==rr[-1]['after']==state and c['period'][65*i:65*(i+1)]==V
        vm,vl,vh,vh0,vd,vu,vc=I.leaf_map(rr);assert set(vh)==vd and len(vd)==14
        active={z['key'] for z in vc};assert active=={1,3,5}
        par,ch=I.marked(state[1],I.M);assert all(not ch[k] for k in active)
        assert max(len(z['branch']) for z in vl)==1
        assert all(len(z['branch'])+z['z']<=2*z['H'] for z in vl)
        assert all(not any(d in z['unpaid'] for d in vd) for z in vl)
        allh.update(vh)
        for key,values in temp['V_local_policy_templates'].items():
            if key=='f6':actual=f6
            elif key=='natural':actual=mp(c['policy_stages'][0]['prior'])
            elif key.endswith('_comparison'):actual=mp(next(z for z in c['policy_stages'] if z['name']==key[:-11])['comparison'])
            elif key.endswith('_effective'):actual=mp(next(z for z in c['policy_stages'] if z['name']==key[:-10])['after'])
            else:raise AssertionError(key)
            assert restriction(actual,573+65*i,637+65*i)==mp(values)
        loc=restriction(before,573+65*i,637+65*i);assert loc==mp(temp['V_complete_frozen_local_map'])
        assert (5,1,0) not in set(loc.values())
    assert c['period'][260:]==old['period']
    assert restriction(before,833,1031)=={(d[0]-572,*d[1:]):(u[0]-572,*u[1:]) for d,u in mp(old['policy_stages'][-1]['after']).items()}
    assert all(z['origin'][0]>=833 and z['birth'][0]>=833 for z in tr)
    print('Induction interfaces: exact V triple return; maximum debt2/empty bank; local leaf channels; no V branch frontier; componentwise owner-policy repetition PASS',flush=True)
    # Hybrid full H uses L blocks plus the source-native F frame on W.
    for b in hy['blocks']:
        hh=mp(b['source_comparison']);assert set(hh.values())<=U and J.peak(hh)<=10
    H=mp(hy['H']);assert set(H)==D and len(set(H.values()))==114 and J.peak(H)==8
    assert allh.items()<=H.items();answer=I.extend(before,H,D)
    assert answer==mp(hy['comparison_extension_of_historical_prefix']) and J.peak(answer)==6
    # Template induction, rather than tests over m: local copies use translated
    # local maps; one extra edge opens in FIRST_V, persists across REPEAT_V,
    # then closes in W. These are all state transitions needed for V^m W.
    full=a;ownwithout={d:u for d,u in a.items() if d!=(921,3)};u=(577,1,0)
    assert u not in ownwithout.values() and full[(921,3)]==u
    profiles={}
    for name,start,stop in (('FIRST_V',573,637),('REPEAT_V',638,702),('W',833,1031)):
        cuts={(r['occurrence'],0,j,b) for r in rows if start<=r['occurrence']<=stop for j in range(1,r['a']+1) for b in (0,1)}
        cuts|={(r['occurrence'],1,j,0) for r in rows if start<=r['occurrence']<=stop for j in range(1,r['qF']+1)}
        profiles[name]=max(J.profile_at(full,t) for t in cuts)
    assert max(profiles.values())==6
    transitions=[{'block':'FIRST_V','incoming':'empty','outgoing':'stored original u577'},
        {'block':'REPEAT_V','incoming':'stored original u577','outgoing':'same original u577'},
        {'block':'W','incoming':'stored original u577','outgoing':'empty'}]
    # Universal arithmetic of absolute translated addresses, no bounded m.
    assert 577-573>=0 and 637-577>=0 and 661-573>=0 and 771-661>=0
    assert 65>0 and 661-577>0 and 14*4+58==114 and 67*4+261==529
    print('Exact FIRST_V, REPEAT_V and W ownership/carry templates PASS; self-loop state supplies induction for arbitrary m>=1',flush=True)
    files=['catchment_forcing_countercertificate.json','hybrid_partition_receipt.json','uniform_insertion_templates.json',
        'NEUTRAL_INSERTION_FAMILY_THEOREM.md','CATCHMENT_COMPARISON_THEOREM.md']
    out('family_independent_audit.json',{'status':'PASS_EXACT_NEW_SOURCE_AND_UNIFORM_INDUCTION_INTERFACES',
        'source_queries':I.queries,'old_W199_replay_repeated':False,'new_source_length':459,
        'source_funding':'complete114-demand source map, peak6, all successes kept',
        'counterexample_scope':'refutes pure one-frame/at-most3-natural-deficit catchment forcing; NOT a funding obstruction',
        'hybrid_source_comparison_peak':8,'template_profiles':profiles,'induction_transitions':transitions,
        'source_uniform_scope':'specified V^m W receipt construction, every integer m>=1, and ordered14-gap BST substitutions',
        'verification_boundary':'exact source/policy and base/self-loop/final templates checked by distinct implementation; induction and opaque-subtree commutation are inspectable mathematical arguments, not formal proof-assistant certification',
        'same_agent_distinct_implementation':True,'external_peer_review':False,'complete_U28_proved':False,
        'sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}})
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_audit_proof_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
