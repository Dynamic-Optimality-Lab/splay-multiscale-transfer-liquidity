"""Exact FI suffix certificates and fresh-run budgets on pinned old controls.

No new source word, n, m, source engine or finite fit. Source-frame profiles
are inherited from the old independently checked FI/CA source certificates.
"""
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=HERE.parent/'route_c_uniform_Hm_separation_20261101_v001'
FI=HERE.parent/'route_c_first_intervention_ceiling_20261031_v001'
CA=HERE.parent/'route_c_102_cut_protocol_audit_20261101_v001'
NI=HERE.parent/'route_c_nowhere_immediate_residual_20261101_v001'
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def depth(t,key):
    d=0
    while t[0]!=key:
        t=t[1 if key<t[0] else 2];d+=1
    return d


def blocks(rows):
    leaders=[i for i,r in enumerate(rows) if r['a']>0]
    result=[]
    for number,i in enumerate(leaders):
        end=leaders[(number+1)%len(leaders)]
        ids=[i];j=(i+1)%len(rows)
        while j!=end:
            ids.append(j);j=(j+1)%len(rows)
        key=rows[i]['key']
        assert all(rows[k]['a']==0 and rows[k]['key']==key for k in ids[1:])
        kept=[k for k in ids if rows[k]['mode']=='KEEP']
        active=[k for k in kept if rows[k]['d_B']>0]
        assert len(active)<=1
        q=sum(rows[k]['q'] for k in ids)
        result.append(dict(leader=i,key=key,indices=ids,a=rows[i]['a'],q=q,
            delta=q-2*rows[i]['a'],has_KEEP=bool(kept),first_KEEP=kept[0] if kept else None,
            B_active_access=active[0] if active else None))
    return result


def source_facts(rows,bs,profiles):
    result={};N=len(bs)
    for i,b in enumerate(bs):
        if b['delta']<=0: continue
        at=b['B_active_access'];assert at is not None
        post=rows[at]['destination_B']
        for j,payer in enumerate(bs):
            if payer['delta']>0: continue
            dist=(j-i)%N;assert dist>0
            between=[bs[(i+t)%N]['B_active_access'] for t in range(1,dist)
                if bs[(i+t)%N]['B_active_access'] is not None]
            y=payer['key'];h=depth(post,y);k=len(between)
            profile=None;first=between[0] if between else None
            c=h//2 if payer['has_KEEP'] else 0
            if first is not None:
                assert rows[first]['source_B']==post
                profile=profiles[(first,y)]
                assert profile['source_depth']==h
                assert depth(rows[first]['destination_B'],y)<=profile['upper_depth']
                c=profile['upper_depth']//2+k-1 if payer['has_KEEP'] else 0
            assert payer['q']<=c
            result[f'{i}:{j}']=dict(anchor=i,payer=j,anchor_occurrence=b['leader'],
                payer_occurrence=payer['leader'],key=y,h=h,k=k,between_B_occurrences=between,
                first_intervention=first,frame_profile=profile,ceiling=c)
    return result


def scan(rows,bs,facts,cut,fresh_only=False,assignments=False):
    N=len(bs);history=[];cursor={};steps=[];claims=[]
    units={i:[[0,b['leader'],e,bit] for e in range(b['a']) for bit in [0,1]] for i,b in enumerate(bs)}
    demands={i:[[0,t,e] for t in b['indices'] for e,ev in enumerate(rows[t]['B_events']) if ev[0]!='ZIG'] for i,b in enumerate(bs)}
    for turn in range(N):
        j=(cut+turn)%N;b=bs[j];C=2*b['a']
        before=sum(bs[i]['delta']-cursor[i] for i in history)
        if b['delta']>0:
            for d,u in zip(demands[j][:C],units[j]):claims.append(dict(demand=d,unit=u,kind='positive_own'))
            history.append(j);cursor[j]=0
            ids=[];minimum=None;r=C;S=0;loans=[];out=C;x=b['delta'];loss=0
        else:
            anchors=history[-1:] if fresh_only else history
            ids=[f'{i}:{j}' for i in anchors]
            minimum=min(facts[s]['ceiling'] for s in ids) if ids else None
            r=min(C,minimum) if ids else C;assert b['q']<=r
            S=C-r;x=-S;loss=r-b['q'];out=r;loans=[]
            for d,u in zip(demands[j],units[j][:r]):claims.append(dict(demand=d,unit=u,kind='payer_own'))
            for i in history:
                owed=bs[i]['delta']-cursor[i];take=min(owed,C-out)
                if take<=0:continue
                start=cursor[i]
                for d,u in zip(demands[i][2*bs[i]['a']+start:2*bs[i]['a']+start+take],units[j][out:out+take]):
                    claims.append(dict(demand=d,unit=u,kind='loan'))
                loans.append(dict(anchor=i,payer=j,residual_start=start,residual_end=start+take,
                    unit_start=out,unit_end=out+take))
                cursor[i]+=take;out+=take
        after=sum(bs[i]['delta']-cursor[i] for i in history)
        assert after==max(0,before+x) and x==b['delta']+loss
        steps.append(dict(turn=turn,block=j,leader=b['leader'],key=b['key'],delta=b['delta'],C=C,q=b['q'],
            fact_ids=ids,minimum_ceiling=minimum,reservation=r,certified_offer=S,reserved_loss=loss,
            x=x,debt_before=before,debt_after=after,history=list(history),
            residual_cursors=[[i,cursor[i]] for i in history],loans=loans,
            lent=out-r if b['delta']<=0 else 0,retired_unused=C-b['q']-(out-r) if b['delta']<=0 else 0))
    debt=sum(bs[i]['delta']-cursor[i] for i in history)
    unpaid=[[bs[i]['leader'],bs[i]['delta']-cursor[i]] for i in history if bs[i]['delta']>cursor[i]]
    assert len(claims)==len({tuple(a['demand']) for a in claims})==len({tuple(a['unit']) for a in claims})
    assert len(claims)+debt==sum(b['q'] for b in bs)
    out=dict(cut=cut,accepted=debt==0,final_debt=debt,unpaid=unpaid,steps=steps,
        distinct_assigned_units=len(claims),distinct_assigned_demands=len(claims),
        unassigned_demands=[d for i in history for d in demands[i][2*bs[i]['a']+cursor[i]:]],
        periods=1,startup_units_used=0,reused_units=0,fresh_only=fresh_only)
    if assignments:out['assignments']=claims
    return out


def rejection_certificate(trial,case):
    steps=trial['steps'];prefix=[0]
    for s in steps:prefix.append(prefix[-1]+s['x'])
    minimum=min(prefix);debt=prefix[-1]-minimum
    assert debt==trial['final_debt']
    last=max(i for i,v in enumerate(prefix) if v==minimum)
    if debt==0:
        assert last==len(steps)
        return None
    assert last<len(steps)
    busy=steps[last:]
    assert busy[0]['delta']>0 and busy[0]['debt_before']==0
    balances=[v-minimum for v in prefix[last+1:]]
    assert all(v>0 for v in balances)
    assert all(s['lent']==s['certified_offer'] for s in busy if s['delta']<=0)
    source=sum(s['delta'] for s in busy);loss=sum(s['reserved_loss'] for s in busy)
    assert source+loss==debt
    return dict(case=case,cut=trial['cut'],prefix_sums=prefix,last_minimum_offset=last,
        minimum_prefix_value=minimum,busy_blocks=[s['block'] for s in busy],
        busy_steps=busy,relative_busy_prefix_balances=balances,
        paid_source_history_before_busy=steps[last-1]['history'] if last else [],
        terminal_debt=debt,positive_excess=sum(max(s['delta'],0) for s in busy),
        certified_offer_sum=sum(s['certified_offer'] for s in busy),
        source_delta_sum=source,reserved_loss_sum=loss,
        loss_class='source-positive open suffix' if source>0 else 'reservation-loss necessary',
        unpaid_demands=trial['unassigned_demands'],all_lendable_suffix_units_spent_while_busy=True,
        reset_history_at_busy_start=False,prefix_units_imported=False,
        whole_cycle_FI_rejection_claimed=False)


def fresh_budgets(rows,bs,facts):
    positives=[i for i,b in enumerate(bs) if b['delta']>0]
    assert positives
    runs=[];N=len(bs)
    for position,i in enumerate(positives):
        end=positives[(position+1)%len(positives)];j=(i+1)%N;payers=[]
        while j!=end:
            b=bs[j];f=facts[f'{i}:{j}'];C=2*b['a'];r=min(C,f['ceiling']);offer=C-r
            if b['has_KEEP']:
                if f['k']==0:
                    assert (offer>0)==(f['h']<=2*C-1)
                else:
                    U=f['frame_profile']['upper_depth']
                    assert (offer>0)==(f['k']<=C and U<=2*(C-f['k'])+1)
            else:assert offer==C
            payers.append(dict(block=j,leader=b['leader'],key=b['key'],has_KEEP=b['has_KEEP'],
                capacity=C,ceiling=f['ceiling'],reservation=r,offer=offer,fact_id=f'{i}:{j}'))
            j=(j+1)%N
        T=sum(p['offer'] for p in payers)
        runs.append(dict(anchor=i,leader=bs[i]['leader'],excess=bs[i]['delta'],payers=payers,
            total_offer=T,g=bs[i]['delta']-T))
    E=sum(b['delta'] for b in bs if b['delta']>0)
    CD=sum(2*b['a'] for b in bs if not b['has_KEEP'])
    L=sum(p['offer'] for r in runs for p in r['payers'] if p['has_KEEP'])
    Gamma=E-CD-L;assert Gamma==sum(r['g'] for r in runs)
    pref=[0]
    for r in runs:pref.append(pref[-1]+r['g'])
    minimum_index=min(range(len(pref)),key=lambda t:pref[t])
    cut=positives[minimum_index%len(positives)] if Gamma<=0 else None
    return dict(positive_blocks=positives,runs=runs,E=E,C_D=CD,L_fresh=L,Gamma=Gamma,
        run_prefix_sums=pref,minimum_prefix_index=minimum_index,constructed_positive_cut=cut)


def main():
    inherited=read(OLD/'entry_source_pins.json');pins=dict(inherited['files'])
    for rel,h in pins.items():assert sha(ROOT/rel)==h,rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==inherited['stage_files'] and len(stage)==125
    assert (git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no'))==(inherited['head'],inherited['branch'],'')
    save('entry_source_pins.json',dict(date='2026-11-01',files=pins,stage_files=stage,
        head=inherited['head'],branch=inherited['branch'],tracked_status='',gate_sha256=sha(HERE/'RC00_FOUR_RULE_GATE.md')))
    for name,h in read(OLD/'delivery_manifest.json')['files'].items():assert sha(OLD/name)==h
    assert read(FI/'independent_audit.json')['status']==read(CA/'independent_audit.json')['status']=='PASS'
    old=read(FI/'first_intervention_certificate.json');profiles={}
    for r in old['local_envelope_matrix']:profiles[(r['witness'],r['occurrence'],r['tracked_key'])]=r['profile']
    ca_facts=read(CA/'source_fact_table.json');ca_trials=read(CA/'cut_ledgers.json')['trials']
    ni=read(NI/'full_source_replays.json');corpus=[]
    for wi,w in enumerate(old['witnesses']):
        rows=[dict(r,mode={'K':'KEEP','D':'DELETE'}[r['mode']]) for r in w['full_replay']]
        pp={(occ,y):v for (idx,occ,y),v in profiles.items() if idx==wi}
        corpus.append(dict(name=w['name'],n=w['n'],rows=rows,prior_blocks=w['blocks'],profiles=pp,
            expected=w['cut_trials'],expected_kind='old_FI_compact',source='old FI witness'+str(wi)))
    for orient,field in [('normal','cycle'),('reflected','mirrored_cycle')]:
        pp={}
        for f in ca_facts[orient].values():
            if f['first_intervention'] is not None:
                key=(f['first_intervention'],f['tracked_key'])
                if key in pp:assert pp[key]==f['frame_profile']
                pp[key]=f['frame_profile']
        corpus.append(dict(name='H5_'+orient,n=13,rows=ni[field],prior_blocks=None,profiles=pp,
            expected=ca_trials[orient]['FI'],expected_kind='CA_full',source='NI H5 '+orient))
    facts_out=[];traces=[];certs=[];budget_out=[];source_inputs=[]
    for ci,item in enumerate(corpus):
        rows=item['rows'];bs=blocks(rows)
        if item['prior_blocks'] is not None:assert bs==item['prior_blocks']
        assert len(bs)==len(rows)
        for i,row in enumerate(rows):
            assert row['source_A']==rows[i-1]['destination_A'] and row['source_B']==rows[i-1]['destination_B']
        fs=source_facts(rows,bs,item['profiles'])
        facts_out.append(dict(case=ci,name=item['name'],facts=fs))
        source_inputs.append(dict(case=ci,name=item['name'],n=item['n'],source=item['source'],rows=rows,blocks=bs))
        case_trials=[]
        for cut in range(len(bs)):
            trial=scan(rows,bs,fs,cut);prior=item['expected'][cut]
            assert trial['accepted']==prior['accepted']
            if item['expected_kind']=='old_FI_compact':
                assert trial['final_debt']==prior['unpaid_excess'] and trial['unpaid']==prior['unpaid']
                transfers=[[bs[s['block']]['leader'],bs[l['anchor']]['leader'],l['residual_start'],l['residual_end'],l['unit_start'],l['unit_end']]
                    for s in trial['steps'] for l in s['loans']]
                assert transfers==prior['transfers']
            else:
                assert trial['final_debt']==prior['final_debt']
                for a,b in zip(trial['steps'],prior['steps']):
                    assert a['reservation']==b['reservation'] and a['debt_after']==b['debt_after']
            cert=rejection_certificate(trial,ci)
            if cert is not None:certs.append(cert)
            case_trials.append(trial)
        traces.append(dict(case=ci,name=item['name'],trials=case_trials))
        budgets=fresh_budgets(rows,bs,fs)
        if budgets['Gamma']<=0:
            cut=budgets['constructed_positive_cut']
            aux=scan(rows,bs,fs,cut,fresh_only=True,assignments=True)
            actual=scan(rows,bs,fs,cut,assignments=True)
            assert aux['accepted'] and actual['accepted']
            for a,b in zip(aux['steps'],actual['steps']):
                assert b['reservation']<=a['reservation'] and b['debt_after']<=a['debt_after']
            # The whole current run anchor is encountered before every payer.
            for step in aux['steps']:
                if step['delta']<=0:assert len(step['fact_ids'])==1
            budgets.update(auxiliary_selected_ledger=aux,actual_FI_selected_ledger=actual)
        budget_out.append(dict(case=ci,name=item['name'],**budgets))
    assert len(corpus)==14 and sum(len(t['trials']) for t in traces)==636 and len(certs)==44
    save('fixed_corpus_sources.json',dict(source_FI_certificate_sha256=sha(FI/'first_intervention_certificate.json'),
        source_NI_replays_sha256=sha(NI/'full_source_replays.json'),cases=source_inputs,
        all_contexts_previously_verified=True,new_source_words=0,new_source_engine_calls=0))
    save('source_fact_table.json',dict(cases=facts_out,profiles_from_pinned_existing_certificates=True,
        actual_payer_q_substituted_for_reservation=False))
    save('cut_recurrence_traces.json',dict(cases=traces,all_periods_one=True,all_startup_units_zero=True))
    save('FI_rejection_certificates.json',dict(status='EXACT certificates, not all-cut counterexamples',
        certificates=certs,certificate_count=len(certs),all_keep_original_full_cut_history=True))
    save('fresh_run_budget_certificate.json',dict(cases=budget_out,
        theorem='Gamma<=0 implies a constructed positive-run cut is FI-successful',
        necessary_remaining_class='E>C_D+L_fresh',positive_Gamma_sufficient_for_FI_rejection=False,
        universal_Gamma_nonpositivity_claimed=False,remaining_class_nonempty_claimed=False))
    summary=dict(status='EXACT_CERTIFICATES_AND_STRICT_SOURCE_FILTER',date='2026-11-01',
        gate_sha256=sha(HERE/'RC00_FOUR_RULE_GATE.md'),
        corpus_cases=14,existing_cuts_checked=636,accepted_existing_cuts=592,rejected_existing_cuts=44,
        certificate_loss_classes=dict(Counter(c['loss_class'] for c in certs)),
        fresh_budget_outcomes=[dict(case=b['case'],name=b['name'],E=b['E'],C_D=b['C_D'],
            L_fresh=b['L_fresh'],Gamma=b['Gamma'],constructed_cut=b['constructed_positive_cut']) for b in budget_out],
        fresh_budget_covered_cases=sum(b['Gamma']<=0 for b in budget_out),
        positive_Gamma_control_cases=[b['case'] for b in budget_out if b['Gamma']>0],
        universal_proof='clipped debt identity, stationary run recurrence, minimum-prefix cut and FI domination',
        strictness_witness='all H_m,m>=5: E=m>C_D=4 and L_fresh>=m, hence Gamma<=-4',
        obstruction_class='O_fresh={reachable closed source walks:E>C_D+L_fresh}',
        all_cut_FI_rejecting_new_witnesses=0,new_source_words=0,new_source_engine_calls=0,
        new_m_values_replayed=0,larger_finite_fits=0,
        matching_terminal_line='FROZEN',universal_CD='OPEN',automatic_successor_launched=False)
    for name in ['fixed_corpus_sources.json','source_fact_table.json','cut_recurrence_traces.json',
                 'FI_rejection_certificates.json','fresh_run_budget_certificate.json']:
        summary[name+'_sha256']=sha(HERE/name)
    save('audit_summary.json',summary)
    print(json.dumps(dict(status=summary['status'],cuts=636,rejection_certificates=44,
        certificate_loss_classes=summary['certificate_loss_classes'],
        fresh_budget_outcomes=summary['fresh_budget_outcomes'],preserved_files=len(pins)),indent=2))


if __name__=='__main__':main()
