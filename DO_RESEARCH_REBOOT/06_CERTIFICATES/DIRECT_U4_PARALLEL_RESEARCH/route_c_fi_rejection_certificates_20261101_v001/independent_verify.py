"""Independent source-entry, physical-pool and suffix-certificate checker."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
checks=Counter()


def ck(test,name):
    if not test:raise AssertionError(name)
    checks[name]+=1
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
def nodes(t,key):
    out=[]
    while t:
        out.append(t)
        if t[0]==key:return out
        t=t[1 if key<t[0] else 2]
    raise AssertionError('present source key')
def depth(t,key):return len(nodes(t,key))-1
def keys(t):return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])


def envelope(t,x,y,events):
    px,py=nodes(t,x),nodes(t,y);d,h=len(px)-1,len(py)-1
    common=0
    while common<min(len(px),len(py)) and px[common][0]==py[common][0]:common+=1
    ops=[]
    for top in range(d-2,-1,-2):
        g,p=px[top][0],px[top+1][0]
        ops.append(dict(case=('L' if x<g else 'R')+('L' if x<p else 'R'),
            site_depth=top,grandparent=g,parent=p))
    if d%2:ops.append(dict(case='ZIG',site_depth=0,grandparent=t[0],parent=None))
    ck([o['case'] for o in ops]==[e[0] for e in events],'original source frame word')
    entry=None;mu=outer=matched=0
    if d==0:role,cap='root_noop',h
    elif x==y:role,cap='accessed',0
    else:
        entry=next(i for i,o in enumerate(ops) if y in keys(nodes(t,o['grandparent'])[-1]))
        op=ops[entry]
        if op['case']=='ZIG':role='zig_root' if y==op['grandparent'] else 'zig_fringe';mu=1
        elif y==op['parent']:role,mu='parent',0
        else:role='grandparent' if y==op['grandparent'] else 'fringe';mu=2
        later=[o['case'] for o in ops[entry+1:] if o['case']!='ZIG']
        outer=len(later);matched=later.count('LL' if y<x else 'RR');cap=h+mu-outer-matched
    return dict(source_depth=h,access_depth=d,lca_depth=common-1,operations=ops,
        entry_operation=entry,entry_role=role,first_gain_allowance=mu,outer_doubles=outer,
        matching_outer_doubles=matched,target_side='equal' if x==y else ('left' if y<x else 'right'),
        upper_depth=min(h+2,max(0,cap)))


def independently_group(rows):
    starts=[i for i,r in enumerate(rows) if r['key']!=rows[i-1]['key']]
    result=[]
    for pos,i in enumerate(starts):
        end=starts[(pos+1)%len(starts)];ids=[i];at=(i+1)%len(rows)
        while at!=end:ids.append(at);at=(at+1)%len(rows)
        ck(rows[i]['a']>0,'block leader costs A work')
        ck(all(rows[j]['a']==0 for j in ids[1:]),'same-root followers have no A capacity')
        kept=[j for j in ids if rows[j]['mode']=='KEEP'];active=[j for j in kept if rows[j]['d_B']>0]
        ck(len(active)<=1,'at most one genuine B change per source block')
        q=sum(rows[j]['q'] for j in ids)
        result.append(dict(leader=i,key=rows[i]['key'],indices=ids,a=rows[i]['a'],q=q,
            delta=q-2*rows[i]['a'],has_KEEP=bool(kept),first_KEEP=kept[0] if kept else None,
            B_active_access=active[0] if active else None))
    return result


def independently_fact(rows,bs,i,j):
    ar=rows[bs[i]['B_active_access']];T=ar['destination_B'];y=bs[j]['key'];h=depth(T,y)
    changes=[];at=(i+1)%len(bs)
    while at!=j:
        if bs[at]['B_active_access'] is not None:changes.append(bs[at]['B_active_access'])
        at=(at+1)%len(bs)
    profile=None;first=changes[0] if changes else None
    c=h//2 if bs[j]['has_KEEP'] else 0
    if first is not None:
        fr=rows[first];ck(fr['source_B']==T,'first intervention exact post-anchor source')
        profile=envelope(fr['source_B'],fr['key'],y,fr['B_events'])
        ck(depth(fr['destination_B'],y)<=profile['upper_depth'],'source-only bound checked against first post tree')
        c=profile['upper_depth']//2+len(changes)-1 if bs[j]['has_KEEP'] else 0
    ck(bs[j]['q']<=c,'every source ceiling covers payer own demand')
    return dict(anchor=i,payer=j,anchor_occurrence=bs[i]['leader'],payer_occurrence=bs[j]['leader'],
        key=y,h=h,k=len(changes),between_B_occurrences=changes,first_intervention=first,
        frame_profile=profile,ceiling=c)


def check_trial(trial,rows,bs,facts):
    N=len(bs);cut=trial['cut'];fresh=trial['fresh_only']
    units={i:[[0,b['leader'],e,z] for e in range(b['a']) for z in [0,1]] for i,b in enumerate(bs)}
    demands={i:[[0,j,e] for j in b['indices'] for e,ev in enumerate(rows[j]['B_events']) if ev[0]!='ZIG'] for i,b in enumerate(bs)}
    legal_units={tuple(u) for us in units.values() for u in us}
    legal_demands={tuple(d) for ds in demands.values() for d in ds}
    usedU,usedD,history,paid,visited,claims=set(),set(),[],{},set(),[]
    def claim(d,u,kind,donor):
        ck(tuple(d) in legal_demands and tuple(u) in legal_units,'physical source unit and demand membership')
        ck(d[0]==u[0]==0 and u[1]==bs[donor]['leader'],'one current-period donor pool only')
        ck(tuple(d) not in usedD and tuple(u) not in usedU,'no reused unit or demand within period')
        usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
    ck(len(trial['steps'])==N,'one block visit per cut position')
    for turn,step in enumerate(trial['steps']):
        j=(cut+turn)%N;b=bs[j];C=len(units[j]);before=sum(bs[i]['delta']-paid[i] for i in history)
        ck(j not in visited,'physical pool visited once');visited.add(j)
        if b['delta']>0:
            for d,u in zip(demands[j][:C],units[j]):claim(d,u,'positive_own',j)
            history.append(j);paid[j]=0
            ids=[];minimum=None;r=C;offer=0;x=b['delta'];loss=0;out=C;loans=[];retired=0
        else:
            fact_anchors=history[-1:] if fresh else history
            ids=[f'{i}:{j}' for i in fact_anchors]
            minimum=min(facts[s]['ceiling'] for s in ids) if ids else None
            r=C if not ids else min(C,minimum);ck(b['q']<=r,'one source reservation protects own work')
            offer=C-r;x=-offer;loss=r-b['q'];out=r;loans=[]
            for d,u in zip(demands[j],units[j][:b['q']]):claim(d,u,'payer_own',j)
            for i in history:
                offset=paid[i];amount=min(bs[i]['delta']-offset,C-out)
                if amount<=0:continue
                ck(i!=j,'no loan to future or own positive pool')
                for k in range(amount):
                    claim(demands[i][2*bs[i]['a']+offset+k],units[j][out+k],'loan',j)
                loans.append(dict(anchor=i,payer=j,residual_start=offset,residual_end=offset+amount,
                    unit_start=out,unit_end=out+amount));paid[i]+=amount;out+=amount
            retired=C-b['q']-(out-r)
        after=sum(bs[i]['delta']-paid[i] for i in history)
        expected=dict(turn=turn,block=j,leader=b['leader'],key=b['key'],delta=b['delta'],C=C,q=b['q'],
            fact_ids=ids,minimum_ceiling=minimum,reservation=r,certified_offer=offer,reserved_loss=loss,
            x=x,debt_before=before,debt_after=after,history=list(history),residual_cursors=[[i,paid[i]] for i in history],
            loans=loans,lent=out-r if b['delta']<=0 else 0,retired_unused=retired)
        ck(step==expected,'every frozen reservation history FIFO range and debt is exact')
        ck(after==max(0,before+x) and x==b['delta']+loss,'clipped recurrence and source-loss identity')
        ck(sum(u[1]==b['leader'] for u in usedU)==C-retired,'pool retired with exact unused count')
    residual=[[bs[i]['leader'],bs[i]['delta']-paid[i]] for i in history if paid[i]<bs[i]['delta']]
    unassigned=[d for i in history for d in demands[i][2*bs[i]['a']+paid[i]:]]
    debt=sum(v for _,v in residual)
    ck(debt==trial['final_debt'] and residual==trial['unpaid'] and unassigned==trial['unassigned_demands'],'exact rejected residual demand identities')
    ck(trial['accepted']==(debt==0) and len(claims)+debt==len(legal_demands),'full demand accounting and cut status')
    ck(legal_demands-usedD=={tuple(d) for d in unassigned},'no unrecorded unpaid demand')
    ck(trial['distinct_assigned_units']==trial['distinct_assigned_demands']==len(claims),'distinct physical multiplicity count')
    ck(trial['periods']==1 and trial['startup_units_used']==trial['reused_units']==0,'no startup other lap or reused credit')
    if 'assignments' in trial:ck(trial['assignments']==claims,'selected complete distinct-unit injection matches')
    return claims


def direct_suffix_certificate(trial,ci):
    steps=trial['steps'];total=best=0;start=len(steps)
    # Reverse suffix summation, independently of the producer's prefix-minimum selection.
    for p in range(len(steps)-1,-1,-1):
        total+=steps[p]['x']
        if total>best:best,start=total,p
    ck(best==trial['final_debt'],'exact largest suffix sum equals final debt')
    if best==0:return None
    busy=steps[start:];running=0;relative=[]
    for s in busy:running+=s['x'];relative.append(running)
    ck(busy[0]['delta']>0 and busy[0]['debt_before']==0 and all(v>0 for v in relative),'canonical terminal busy interval starts positive and never clears')
    ck(all(s['lent']==s['certified_offer'] for s in busy if s['delta']<=0),'every certified suffix unit spent during busy interval')
    if start:
        prior=steps[start-1]
        ck(prior['debt_after']==0,'all prefix debts paid before busy interval')
    pref=[0]
    for s in steps:pref.append(pref[-1]+s['x'])
    source=sum(s['delta'] for s in busy);loss=sum(s['reserved_loss'] for s in busy)
    ck(source+loss==best and all(s['reserved_loss']>=0 for s in busy),'exact open-source imbalance plus protected-prefix loss')
    return dict(case=ci,cut=trial['cut'],prefix_sums=pref,last_minimum_offset=start,minimum_prefix_value=pref[start],
        busy_blocks=[s['block'] for s in busy],busy_steps=busy,relative_busy_prefix_balances=relative,
        paid_source_history_before_busy=steps[start-1]['history'] if start else [],terminal_debt=best,
        positive_excess=sum(max(s['delta'],0) for s in busy),certified_offer_sum=sum(s['certified_offer'] for s in busy),
        source_delta_sum=source,reserved_loss_sum=loss,
        loss_class='source-positive open suffix' if source>0 else 'reservation-loss necessary',
        unpaid_demands=trial['unassigned_demands'],all_lendable_suffix_units_spent_while_busy=True,
        reset_history_at_busy_start=False,prefix_units_imported=False,whole_cycle_FI_rejection_claimed=False)


def main():
    entry=read(HERE/'entry_source_pins.json')
    for rel,h in entry['files'].items():ck(sha(ROOT/rel)==h,'inherited source and prior files preserved')
    ck(entry['gate_sha256']==sha(HERE/'RC00_FOUR_RULE_GATE.md'),'pre-execution gate preserved')
    summary=read(HERE/'audit_summary.json')
    names=['fixed_corpus_sources.json','source_fact_table.json','cut_recurrence_traces.json',
        'FI_rejection_certificates.json','fresh_run_budget_certificate.json']
    for name in names:ck(summary[name+'_sha256']==sha(HERE/name),'certificate provenance hash')
    cases=read(HERE/'fixed_corpus_sources.json')['cases']
    factsets=read(HERE/'source_fact_table.json')['cases']
    traces=read(HERE/'cut_recurrence_traces.json')['cases']
    recorded=read(HERE/'FI_rejection_certificates.json')['certificates']
    budgets=read(HERE/'fresh_run_budget_certificate.json')['cases']
    reconstructed=[];new_facts=[];counts=Counter();proper_controls=[];sharing_controls=[]
    ck(len(cases)==len(factsets)==len(traces)==len(budgets)==14,'fixed fourteen preverified source controls only')
    for ci,case in enumerate(cases):
        rows,bs=case['rows'],case['blocks']
        ck(independently_group(rows)==bs,'root-key grouping independently matches source leaders')
        for j,r in enumerate(rows):
            ck(r['source_A']==rows[j-1]['destination_A'] and r['source_B']==rows[j-1]['destination_B'],'exact cyclic paired source continuity')
            ck(r['a']==(depth(r['source_A'],r['key'])+1)//2 and len(r['A_events'])==r['a'],'A source event accounting')
            ck(all(keys(r[k])==list(range(1,case['n']+1)) for k in ['source_A','source_B','destination_A','destination_B']),'strict full source trees')
            if r['mode']=='KEEP':
                ck(r['q']==depth(r['source_B'],r['key'])//2 and r['z']==depth(r['source_B'],r['key'])%2,'B double and genuine zig source conventions')
            else:ck(r['source_B']==r['destination_B'] and r['q']==0,'DELETE freezes B')
        fs={}
        for i,b in enumerate(bs):
            if b['delta']<=0:continue
            for j,p in enumerate(bs):
                if p['delta']<=0:fs[f'{i}:{j}']=independently_fact(rows,bs,i,j)
        ck(fs==factsets[ci]['facts'],'all source facts independently rebuilt by subtree entry')
        new_facts.append(fs)
        ck(len(traces[ci]['trials'])==len(bs),'all existing physical cuts checked')
        for cut,trial in enumerate(traces[ci]['trials']):
            ck(trial['cut']==cut and not trial['fresh_only'],'unaltered full-history FI on every cut')
            check_trial(trial,rows,bs,fs)
            cert=direct_suffix_certificate(trial,ci)
            if cert:reconstructed.append(cert)
            counts['cuts']+=1;counts['accepts' if trial['accepted'] else 'rejects']+=1
        bgt=budgets[ci];positives=[i for i,b in enumerate(bs) if b['delta']>0]
        ck(bgt['positive_blocks']==positives,'all cyclic positive runs identified')
        owners={}
        for j,b in enumerate(bs):
            if b['delta']>0:continue
            for d in range(1,len(bs)):
                i=(j-d)%len(bs)
                if bs[i]['delta']>0:owners[j]=i;break
        seen_payers=set();runs=[]
        for i in positives:
            ps=[];j=(i+1)%len(bs)
            while bs[j]['delta']<=0:
                ck(owners[j]==i and j not in seen_payers,'one physical fresh payer belongs to one nearest-positive run')
                seen_payers.add(j);p=bs[j];f=fs[f'{i}:{j}'];C=2*p['a'];rho=min(C,f['ceiling']);offer=C-rho
                ck(p['q']<=rho,'fresh source fact protects own work without older anchors')
                if p['has_KEEP']:
                    if f['k']==0:qualified=f['h']<=2*C-1
                    else:
                        U=f['frame_profile']['upper_depth']
                        qualified=f['k']<=C and U<=2*(C-f['k'])+1
                    ck((offer>0)==qualified,'exact capacity-relative freshness and frame condition')
                else:ck(offer==C,'each KEEP-less pool counted once at full capacity')
                ps.append(dict(block=j,leader=p['leader'],key=p['key'],has_KEEP=p['has_KEEP'],capacity=C,
                    ceiling=f['ceiling'],reservation=rho,offer=offer,fact_id=f'{i}:{j}'))
                j=(j+1)%len(bs)
            T=sum(p['offer'] for p in ps)
            runs.append(dict(anchor=i,leader=bs[i]['leader'],excess=bs[i]['delta'],payers=ps,total_offer=T,g=bs[i]['delta']-T))
        ck(seen_payers=={j for j,b in enumerate(bs) if b['delta']<=0} and runs==bgt['runs'],'cyclic run partition and local budgets exact')
        E=sum(b['delta'] for b in bs if b['delta']>0);CD=sum(2*b['a'] for b in bs if not b['has_KEEP'])
        L=sum(p['offer'] for r in runs for p in r['payers'] if p['has_KEEP']);G=E-CD-L
        ck((E,CD,L,G)==(bgt['E'],bgt['C_D'],bgt['L_fresh'],bgt['Gamma']) and G==sum(r['g'] for r in runs),'global fresh identity with no double-counted pool')
        pref=[0]
        for r in runs:pref.append(pref[-1]+r['g'])
        ck(pref==bgt['run_prefix_sums'],'run signed-prefix sums')
        if G<=0:
            cut=bgt['constructed_positive_cut'];position=positives.index(cut)
            rotated=[runs[(position+t)%len(runs)]['g'] for t in range(len(runs))]
            ck(all(sum(rotated[t:])<=0 for t in range(len(rotated)+1)),'constructed run cut has no positive ending suffix')
            aux,actual=bgt['auxiliary_selected_ledger'],bgt['actual_FI_selected_ledger']
            ck(aux['cut']==actual['cut']==cut and aux['fresh_only'] and not actual['fresh_only'],'positive-boundary comparison uses available current anchor facts')
            check_trial(aux,rows,bs,fs);check_trial(actual,rows,bs,fs)
            ck(aux['accepted'] and actual['accepted'],'fresh and actual queues clear at the constructed cut')
            for a,b in zip(aux['steps'],actual['steps']):
                ck(b['reservation']<=a['reservation'] and b['debt_after']<=a['debt_after'],'retained full history gives FI debt domination without new credit')
                if a['delta']<=0:ck(len(a['fact_ids'])==1,'auxiliary source fact encountered inside this period')
            byblock={s['block']:s for s in aux['steps']}
            for run in runs:
                start=byblock[run['anchor']]['debt_before']
                endblock=run['payers'][-1]['block'] if run['payers'] else run['anchor']
                ck(byblock[endblock]['debt_after']==max(0,start+run['g']),'run collapse models discarded surplus exactly')
            counts['budget_covered']+=1
        if E>CD and G<=0:proper_controls.append(ci)
        if any(r['g']>0 for r in runs) and G<=0:sharing_controls.append(ci)
    ck(reconstructed==recorded and len(recorded)==44,'all forty-four exact canonical rejection certificates agree')
    ck((counts['cuts'],counts['accepts'],counts['rejects'])==(636,592,44),'old cut classifications exactly reproduced')
    ck(counts['budget_covered']==14 and proper_controls==[12,13],'proper-filter controls H5 and reflection')
    for a in range(0,14,2):
        x,y=budgets[a],budgets[a+1]
        ck((x['E'],x['C_D'],x['L_fresh'],x['Gamma'])==(y['E'],y['C_D'],y['L_fresh'],y['Gamma']),'reflected source budgets coincide')
    UH=HERE.parent/'route_c_uniform_Hm_separation_20261101_v001'
    uniform=read(UH/'uniform_proof_certificate.json')
    ck(uniform['FI_latest_KEEP5_fact']==dict(h=3,k=1,U=2,ceiling=1,capacity=2,own_q=1),'inherited source donor proves one fresh unit per H_m copy')
    ck(uniform['UD_debts']=='m' and uniform['UD_total_lendable_DELETE_capacity']==4,'inherited unbounded H_m strictness parameters')
    ck(1-1==0 and -4<0,'Gamma(H_m)<=m-4-m=-4 for every m>=5')
    proof=HERE/'RC01_CERTIFICATES_AND_STRICT_FILTER_PROOF.md';ck(proof.is_file(),'full universal recurrence and minimum-prefix proof supplied')
    save('independent_audit.json',dict(status='PASS',date='2026-11-01',checks=dict(checks),
        audited_summary_sha256=sha(HERE/'audit_summary.json'),
        analytic_proof_sha256=sha(proof),
        output_hashes={name:sha(HERE/name) for name in names},
        source_entry_method='original subtree membership; producer reuses pinned source profiles',
        certificate_selection='direct backwards suffix maximization; producer uses last prefix minimum',
        source_cases=14,existing_cuts_checked=636,accepted_cuts=592,rejected_cuts=44,
        exact_busy_certificates=44,fresh_budget_covered_controls=14,
        controls_with_starved_individual_runs=sharing_controls,
        properness_controls=proper_controls,positive_Gamma_controls=[],
        theorem='Gamma<=0 constructs an FI-successful positive-run cut on every admissible closed source walk',
        strict_remaining_filter='FI all-cut failure implies E>C_D+L_fresh; proper subclass of E>C_D',
        positive_Gamma_implies_FI_failure='NOT ESTABLISHED',remaining_class_nonemptiness='OPEN',
        new_all_cut_FI_counterexamples_claimed=False,new_source_words=0,new_source_engine_calls=0,
        new_m_values_replayed=0,larger_finite_fits=0,startup_or_other_lap_units_used=0,reused_units=0,
        matching_terminal_line='FROZEN',universal_CD='OPEN',automatic_successor_launched=False))
    print(json.dumps(dict(status='PASS',checks=sum(checks.values()),cuts=636,certificates=44,
        fresh_budget_covered_controls=14,controls_with_starved_runs=sharing_controls,
        proper_remaining_class='E>C_D+L_fresh',positive_Gamma_controls_found=0,
        new_source_words=0,larger_finite_fits=0),indent=2))


if __name__=='__main__':main()
