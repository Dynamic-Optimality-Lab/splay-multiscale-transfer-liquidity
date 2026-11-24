from campaign3b import *
from inherited_epoch_audit import A_pivots


def test(s,demands):
    A,pivots=A_pivots(s);steps=defaultdict(list)
    for entries in pivots.values():
        for h,bit in entries:
            if bit[3]==0:steps[h].append(bit[:3])
    for h in steps:steps[h].sort()
    keeps=[h for h,(tag,x) in enumerate(s['operations'],1) if tag=='K'];T=len(s['operations'])
    packets=defaultdict(lambda:defaultdict(list))
    for e in demands:packets[e['consumer']][tuple(e['original_parent'])].append(e)
    allocations=[];loads=Counter();overflow=[];whole_packets=[];gap_budgets={}
    for k,h in enumerate(keeps):
        prev=keeps[k-1];length=(h-prev)%T or T
        ts=[(prev+j-1)%T+1 for j in range(1,length+1)]
        actual=[eid for t in ts for eid in steps[t]];gap_budgets[h]=actual
        parents=sorted(packets[h]);a=len(actual)
        assert all(len(packets[h][p])<=3 for p in parents)
        if len(parents)<=a:whole_packets.extend(e for p in parents for e in packets[h][p])
        for j,p in enumerate(parents):
            if j>=2*a:overflow.extend(packets[h][p]);continue
            resource=actual[j//2];ds=packets[h][p];loads[resource]+=len(ds)
            allocations.append({'original_parent':p,'actual_A_StepEv':resource,'original_gaps':[e['rho'] for e in ds]})
    assert sum(len(z) for z in gap_budgets.values())==A
    assert max(loads.values(),default=0)<=6
    assert sum(len(z['original_gaps']) for z in allocations)+len(overflow)==len(demands)
    assert len(whole_packets)<=3*A
    return {'source':s['name'],'original_gap_count':len(demands),'A':A,
        'selected_parent_allocations':allocations,'literal_overflow':overflow,
        'maximum_actual_A_StepEv_gap_load':max(loads.values(),default=0),
        'whole_width_le_A_packet_gap_count':len(whole_packets),
        'width_by_KEEP':[{'h':h,'distinct_original_parents':len(packets[h]),'actual_A_gap_steps':len(gap_budgets[h])}
                         for h in sorted(packets) if packets[h]],
        'actual_gap_steps_partition_verified':True}


if __name__=='__main__':
    meter=Meter('packet_payments')
    s=json.loads((ROOT/'DILATED_PACKET_SOURCES.json').read_text())[-1]
    row=json.loads((ROOT/'DILATED_PACKET_RESULTS.json').read_text())[-1]
    C=row['ordered_accounting']['C_after_frozen_and_prefix'];out=test(s,C)
    assert len(out['selected_parent_allocations'])==2 and not out['literal_overflow']
    assert {tuple(z['actual_A_StepEv']) for z in out['selected_parent_allocations']}=={('A',646,1),('A',653,1)}
    cert=json.loads((ROOT/'COUNTEREXAMPLE_CERTIFICATE.json').read_text())
    assert all(p['old_g']==154 for p in cert['original_parent_certificates'])
    out['whole_column_154_payment']={'actual_A_gap_StepEv':[z['actual_A_StepEv'] for z in out['selected_parent_allocations']],
        'all_original_C_gaps_paid':len(C),'global_proved_budget':'3A for the whole fixed-key column, not per epoch',
        'maximum_load_in_this_source':max(len(z['original_gaps']) for z in out['selected_parent_allocations'])}
    write('COUNTEREXAMPLE_PACKET_PAYMENT.json',out)
    large=next(s for s in json.loads((C3/'SCALING_SOURCES.json').read_text()) if s['p']==6)
    old=next(z for z in json.loads((C3/'SCALING_RESULTS.json').read_text()) if z['source']==large['name'])
    wider=test(large,old['original_R_star'])
    assert any(z['distinct_original_parents']>z['actual_A_gap_steps'] for z in wider['width_by_KEEP'])
    wider['refuted_statement']='Every packet of original R_star parents has width<=A(G_h).'
    wider['stronger_quota_fit_statement_width_le_2A']='NOT REFUTED by this control; the original failed expectation confused total gaps with same-KEEP parent width.'
    wider['scope']='Original R_star pool only; existing old hybrid pays this source. No post-hybrid overflow escape claimed.'
    write('WIDTH_FIT_COUNTERCONTROL.json',wider)
    print('PASS real A-StepEv column and quota donors; width<=A_gap refuted; width<=2A_gap not refuted here',flush=True)
    meter.success=True
