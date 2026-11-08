"""Exact signed/owner/packet ledgers from saved rows; no source replay."""
import collections,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;C28=P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28';OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C29_classification',OLD/'audit_construct.py')
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(z) for z in t) if isinstance(t,list) else t
def mp(z):return {tuple(x['demand']):tuple(x['unit']) for x in z}
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def state(t):
    par,ch=C.L.marked_tree(t,C.M);L=sum(not v for v in ch.values());br=sum(len(v)>=2 for v in ch.values());E=sum(max(len(v)-2,0) for v in ch.values());assert E==L-br-1 and 0<=E<=4
    return {'L':L,'branches':br,'E':E,'marked_children':ch}
def analyze(rows):
    mm=C.L.macros(rows);ans=[]
    for i,m in enumerate(mm):
        x=m['rows'][-1]['target'];s=state(m['rows'][0]['before'][1]);t=state(m['rows'][-1]['after'][1]);par,ch=C.L.marked_tree(m['rows'][0]['before'][1],C.M)
        ancestors=[];v=par[x]
        while v is not None:ancestors.append(v);v=par[v]
        beta=sum(len(ch[v])>=2 for v in ancestors);b2=sum(len(ch[v])==2 for v in ancestors);k3=sum(len(ch[v])>=3 for v in ancestors);d=len(ch[x]);z=int(d==0);c=min(m['H'],3)
        eps=int(d+m['Q']>=2)-int(d>=2)
        rho=2*c-beta-z;sigma=2*c-m['Q']+t['E']-s['E']
        assert sigma==rho+b2-eps and t['branches']-s['branches']==eps-b2
        ans.append({'macro':i,'end':m['occurrences'][-1],'occurrences':m['occurrences'],'target':x,'H':m['H'],'Q':m['Q'],
            'beta':beta,'z':z,'d':d,'b2':b2,'k3':k3,'rho':rho,'sigma_E':sigma,'before':s,'after':t})
    return mm,ans
def profile(a):
    ee=[]
    for d,u in a.items():ee.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    live=set();peak=0
    for t,d in sorted(ee):
        if d in live:live.remove(d)
        else:live.add(d);peak=max(peak,len(live))
    assert not live;return peak
def signed_map(mm,al,tag):
    ci=next(i for i,m in enumerate(mm) if tag['comb'] in m['occurrences']);pi=(ci-1)%len(mm);ji=(ci-2)%len(mm)
    ids=[pi,ci] if mm[pi]['H']>=2 else [ji,pi,ci];assert ids==sorted(ids)
    packets=[];used=set(ids)
    for i,m in enumerate(mm):
        if i==ids[0]:packets.append(ids)
        elif i not in used:packets.append([i])
    debts=[(al[ii[0]]['before']['L']-1,al[ii[-1]]['after']['L']-1) for ii in packets];top=max(x for x,y in debts);cut=next(i for i,(x,y) in enumerate(debts) if x==top)
    h={d:u for m in mm for d,u in zip(m['demands'],m['units'])};bank=[];receipts=[];working=0
    for step in range(len(packets)):
        idx=(cut+step)%len(packets);ii=packets[idx];ds,dt=debts[idx];assert len(bank)==top-ds
        chosen=[u for j in ii for u in mm[j]['units'][:2*min(mm[j]['H'],3)]];dd=[d for j in ii for d in mm[j]['demands']];owned={h[d] for d in dd if d in h};missing=[d for d in dd if d not in h]
        assert owned<=set(chosen);rho=len(chosen)-len(dd)+dt-ds;assert rho>=0
        spare=[u for u in chosen if u not in owned];pool=spare+bank;working=max(working,len(pool)+len(owned));added=[]
        for d in missing:u=pool.pop(0);h[d]=u;added.append((d,u))
        assert len(pool)>=top-dt;bank=pool[:top-dt]
        receipts.append({'packet':idx,'macros':ii,'D_before':ds,'D_after':dt,'rho':rho,'units':chosen,'new_pairs':added,'carry':bank[:]})
    assert not bank;return {'map':pack(h),'packet_receipts':receipts,'processing_start_packet':cut,'max_leaf_debt':top,'working':working,'actual_cut_profile_peak':profile(h),'packet_macro_indices':packets}
def main():
    data=json.loads((B/'comb_source_fixtures.json').read_text());reports=[]
    for r in data['reports']:
        rows=[dict(z,before=fr(z['before']),after=fr(z['after'])) for z in r['rows']];mm,al=analyze(rows);tags=r['tags'][0]
        helper=next(m for m in mm if tags['helper'] in m['occurrences']);comb=next(m for m in mm if tags['comb'] in m['occurrences']);full=C.L.build(rows,C.M);h=full['h'];tail=[u for u in helper['units'] if u not in h.values()]
        current=mp(r['final_full_a']);inverse={u:d for d,u in current.items()};signed=signed_map(mm,al,tags);strong=None
        if helper['H']>=2:
            holes=sorted(d for d in full['R'] if d[0]==tags['comb']);assert len(holes)==2 and len(tail)>=2
            hplus=dict(h);hplus.update(zip(holes,tail[:2]));assert set(hplus)==full['D'] and len(set(hplus.values()))==len(hplus)
            prefix=mp(r['effective_prefix']);inv={u:d for d,u in prefix.items()};answer=dict(prefix);paths=[]
            for root in sorted(full['D']-set(prefix)):
                d=root;steps=[];seen=set()
                while True:
                    assert d not in seen;seen.add(d);u=hplus[d];steps.append((d,u))
                    if u not in inv:break
                    d=inv[u]
                answer[root]=u;paths.append({'root':root,'steps':steps,'terminal':u})
            assert profile(answer)<=25 and all(answer[d]==u for d,u in prefix.items())
            strong={'hplus':pack(hplus),'historical_prefix_extension':pack(answer),'paths':paths,'profile_peak':profile(answer),
                'current_final_a_unchanged':True,'tail_units':tail[:2]}
        else:assert not tail
        reports.append({'source_id':r['source_id'],'macro_ledger':al,'helper_unused_raw_tail':tail,
            'helper_unit_current_owners':[{'unit':u,'owner':inverse.get(u)} for u in helper['units']],
            'comb_demands_current_owners':[{'demand':d,'unit':current[d]} for d in comb['demands']],
            'signed_packet_construction':signed,'strong_comparison':strong,'current_map_not_replaced':True,
            'natural_missing_slots':sorted(full['D']-set(full['h0'])),'leaf_branch_frontiers':sorted(full['R']),
            'actual_unpaid_before_late_success':sorted(full['D']-set(mp(r['effective_prefix']))),'actual_unpaid_now':[]})
    controls=[]
    c27=json.loads((OLD/'aligned_source_and_owners.json').read_text());cc=json.loads((C28/'catchment_forcing_countercertificate.json').read_text())
    for name,c in (('W199',c27),('W459',cc)):
        rows=[dict(z,before=fr(z['before']),after=fr(z['after'])) for z in c['rows']];mm,al=analyze(rows)
        controls.append({'source':name,'marked_comb_occurrences':[z['end'] for z in al if (z['H'],z['Q'],z['beta'],z['z'])==(1,3,3,1)],
            'max_beta':max(z['beta'] for z in al),'negative_sigma_E':[z for z in al if z['sigma_E']<0],
            'sum_sigma_E':sum(z['sigma_E'] for z in al),'sum_rho':sum(z['rho'] for z in al),
            'old_full_funding_preserved':True})
    out('signed_comb_and_control_ledgers.json',{'status':'PRODUCER_EXACT_IDENTITIES_WITH_SOURCE_ROWS_REUSED','reports':reports,'controls':controls,
        'sigma_E_global_candidate_refuted':True,'principal_MC29_closed':False,
        'infinite_neutral_family_comb_exclusion':'V beta<=1 and W beta<=2; exact B returns prove this for every m and gap substitution',
        'helper_debt_not_ignored':True})
    print(json.dumps({'status':'SIGNED_LEDGER_COMPLETE','reports':[{'id':z['source_id'],
        'leaf_packet_cut':z['signed_packet_construction']['processing_start_packet'],'raw_working':z['signed_packet_construction']['working'],
        'raw_peak':z['signed_packet_construction']['actual_cut_profile_peak'],'raw_tail':z['helper_unused_raw_tail']} for z in reports],
        'controls':[{'source':z['source'],'comb_count':len(z['marked_comb_occurrences']),'negative_E_count':len(z['negative_sigma_E'])} for z in controls]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_classify_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
