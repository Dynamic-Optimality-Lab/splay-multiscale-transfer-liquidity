"""Packetized degree-excess comparison, complete degree-count audit data,
and explicit nested-domain discovery. No new source search."""
import importlib.util,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C29_algebra_source',OLD/'audit_construct.py')
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(z) for z in t) if isinstance(t,list) else t
def mp(z):return {tuple(x['demand']):tuple(x['unit']) for x in z}
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def peak(a):
    ev=[]
    for d,u in a.items():ev.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    live=set();ans=0
    for t,d in sorted(ev):
        if d in live:live.remove(d)
        else:live.add(d);ans=max(ans,len(live))
    assert not live;return ans
def main():
    data=json.loads((B/'comb_source_fixtures.json').read_text());ledger=json.loads((B/'signed_comb_and_control_ledgers.json').read_text());proofs=[]
    for r,l in zip(data['reports'],ledger['reports']):
        rows=[dict(z,before=fr(z['before']),after=fr(z['after'])) for z in r['rows']];mm=C.L.macros(rows);tag=r['tags'][0];al=l['macro_ledger']
        ci=next(i for i,m in enumerate(mm) if tag['comb'] in m['occurrences']);ii=[ci-1,ci] if mm[ci-1]['H']>=2 else [ci-2,ci-1,ci]
        pp=[]
        for i,m in enumerate(mm):
            if i==ii[0]:pp.append(ii)
            elif i not in ii:pp.append([i])
        debts=[(al[g[0]]['before']['E'],al[g[-1]]['after']['E']) for g in pp];K=max(ds for ds,dt in debts);cut=next(i for i,(ds,dt) in enumerate(debts) if ds==K)
        h={d:u for m in mm for d,u in zip(m['demands'],m['units'])};bank=[];records=[];working=0
        for s in range(len(pp)):
            j=(cut+s)%len(pp);g=pp[j];ds,dt=debts[j];assert len(bank)==K-ds
            chosen=[u for i in g for u in mm[i]['units'][:2*min(mm[i]['H'],3)]];dd=[d for i in g for d in mm[i]['demands']];own={h[d] for d in dd if d in h};missing=[d for d in dd if d not in h]
            sigma=len(chosen)-len(dd)+dt-ds;assert sigma>=0 and own<=set(chosen)
            spare=[u for u in chosen if u not in own];pool=spare+bank;working=max(working,len(pool)+len(own));pairs=[]
            for d in missing:u=pool.pop(0);h[d]=u;pairs.append((d,u))
            assert len(pool)>=K-dt;bank=pool[:K-dt];records.append({'packet':j,'macros':g,'before':ds,'after':dt,'sigma_E':sigma,'chosen':chosen,'pairs':pairs,'carry':bank[:]})
        assert not bank and len(set(h.values()))==len(h) and peak(h)<=25
        # Current full source owner map is immutable. Exercise the new full
        # comparer against ONLY the archived33-entry prefix, never replace it.
        prior=mp(r['effective_prefix']);inverse={u:d for d,u in prior.items()};answer=dict(prior);paths=[]
        for root in sorted(set(h)-set(prior)):
            d=root;steps=[];seen=set()
            while True:
                assert d not in seen;seen.add(d);u=h[d];steps.append((d,u))
                if u not in inverse:break
                d=inverse[u]
            answer[root]=u;paths.append({'root':root,'steps':steps,'terminal':u})
        assert peak(answer)<=25 and all(answer[d]==u for d,u in prior.items())
        proofs.append({'source_id':r['source_id'],'packet_indices':pp,'canonical_processing_packet':cut,'E_max':K,
            'full_comparison_H_E':pack(h),'receipts':records,'working':working,'actual_I_profile':peak(h),
            'historical_prefix_extension':pack(answer),'owner_paths':paths,'extended_profile':peak(answer),'current_full_a_not_replaced':True})
    # Necessary degree profiles are an exact finite count classification at
    # fixed7 marks, NOT a finite bound on original BST populations.
    negatives=set();count=0
    def paths(q,budget):
        if q==0:
            yield ();return
        for off in range(budget+1):
            for z in paths(q-1,budget-off):yield (off+1,)+z
    for q in range(1,7):
        for d in range(7-q):
            for degrees in paths(q,6-q-d):
                beta=sum(v>=2 for v in degrees);b2=sum(v==2 for v in degrees);k3=sum(v>=3 for v in degrees);z=int(d==0);eps=int(d+q>=2)-int(d>=2)
                de=max(d+q-2,0)-max(d-2,0)-k3
                assert de==(q-beta-z)+b2-eps
                sigma=2-q+de;count+=1
                if sigma<0:
                    assert d==0 and q>=2 and k3>=1;negatives.add((q,beta,b2,k3,sigma))
                assert 4-q+de>=0
    # Discover rather than silently assert the old special five-key domains.
    shared=data['reports'][0];nested=[]
    for x in sorted(C.M-{11}):
        t=fr(shared['original_diagonal_tree'])
        for mode,k in shared['reaching_prefix']:
            if mode=='K' and k not in (11,x):t=C.tr(t,k)[0]
        start=t;seen={};seq=[]
        while t not in seen and len(seq)<10:
            seen[t]=len(seq);seq.append(t)
            for mode,k in shared['period']:
                if mode=='K' and k not in (11,x):t=C.tr(t,k)[0]
        assert t in seen;core=len(C.p.labels(C.p.core(t,C.M-{11,x})))
        nested.append({'extra_erased':x,'u':seen[t],'L':len(seq)-seen[t],'recurrent_core':core,
            'old_special_core9_candidate':core==9,'current_interval_already_closed':start==t,
            'existing_fixed_f5_supplied':False})
    out('packetized_excess_and_nested_domains.json',{'status':'PRODUCER_SIGNED_PACKETS_AND_DEBT_TRANSFER_LEDGER','reports':proofs,
        'universal_degree_profile_count':count,'necessary_negative_E_profiles':sorted(negatives),
        'H_ge2_nonnegative_proved_by_inequalities':True,'all_count_profiles_realizable_asserted':False,
        'nested_five_domains':nested,'owner_scope':'NEW raw-canonical fixtures, no older fixed five-key map supplied; all older-normalized cases remain separate',
        'full_MC29_proved':False})
    print(json.dumps({'status':'PACKETIZED_E_SIGNED_COMPARISONS','queries':C.queries,
        'reports':[{'id':z['source_id'],'cut':z['canonical_processing_packet'],'working':z['working'],'actual_I_peak':z['actual_I_profile'],'owner_extension_peak':z['extended_profile']} for z in proofs],
        'degree_profiles':count,'nested_core9':[z['extra_erased'] for z in nested if z['old_special_core9_candidate']]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_algebra_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
