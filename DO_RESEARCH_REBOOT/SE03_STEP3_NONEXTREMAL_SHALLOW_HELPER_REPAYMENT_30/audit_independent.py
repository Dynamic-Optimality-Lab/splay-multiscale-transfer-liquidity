"""Distinct mutable-source verification of the new critical source and its
forward comparison. No C30 producer/replay/allocator/packet code imported.
Old primitives are the previously distinct implementation, not the producer.
"""
import importlib.util,json,sys,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();checks=[];pins={}
sp=importlib.util.spec_from_file_location('C30_mutable_independent',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
def tick():
    if I.queries>=QCAP or time.process_time()-START>=CAP-1:raise TimeoutError('independent inherited cap')
    I.queries+=1
I.tick=tick
def read(n):
    p=B/n;raw=p.read_bytes();pins[n]=hashlib.sha256(raw).hexdigest();return json.loads(raw)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def ok(s):checks.append(s);print(s,flush=True)
def profile(m):return I.buffer_peak(m)
def exact_profiles(mm):
    ans=[]
    for m in mm:
        x=m['rows'][-1]['target'];pa,ch=I.marked(m['rows'][0]['before'][1],I.M);_,nc=I.marked(m['rows'][-1]['after'][1],I.M);a=[];v=pa[x]
        while v is not None:a.append(v);v=pa[v]
        assert len(a)==m['Q'];beta=sum(len(ch[v])>=2 for v in a);k3=sum(len(ch[v])>=3 for v in a);d=len(ch[x]);z=int(d==0);c=min(m['H'],3)
        E=lambda cc:sum(max(len(v)-2,0) for v in cc.values());L=lambda cc:sum(not v for v in cc.values())
        assert L(nc)-L(ch)==m['Q']-beta-z
        sigma=2*c-m['Q']+E(nc)-E(ch);expected=2*c-k3 if d>=2 else 2*c-1-k3 if d==1 else 2*c-min(m['Q'],2)-k3
        assert sigma==expected
        ans.append({'H':m['H'],'Q':m['Q'],'beta':beta,'z':z,'k3':k3,'rho':2*c-beta-z,'sigma_E':sigma,'E_before':E(ch),'E_after':E(nc)})
    return ans
def main():
    r=read('nonextremal_source_countercertificate.json');g=read('source_signed_and_seed_analysis.json');p=read('forward_recovery_and_period_receipt.json');T=I.fr(r['original_diagonal_tree'])
    prefix,S=I.execute((T,T,T),r['reaching_prefix'],1,r['prefix_rows']);assert S==I.fr(r['initial'])
    lo,hi=r['actual_interval'];rows,end=I.execute(S,r['period'],lo,r['rows']);assert end==S==I.fr(r['end'])
    assert len(rows)==len(prefix)==85 and (lo,hi)==(86,170)
    assert {z['target'] for z in rows if z['mode']=='K'}==I.M
    assert all(I.core(z['before'][1],I.M)==set(range(1,14)) for z in rows)
    erased_cores={len(I.core(z['before'][2],I.E)) for z in rows};assert len(erased_cores)==1
    assert all(ev['case'] in ('LL','RR') and ev['G'] in I.M and ev['P'] not in I.M for z in rows for ev in z['BF_events'])
    assert (sum(z['a'] for z in rows),sum(z['qF'] for z in rows),sum(z['qE'] for z in rows))==(109,66,42)
    ok('Actual diagonal prefix and85-operation A/BF/BE source rebuilt; every state, rotation, cost, support and exact triple closure matches')
    mm=I.macro_list(rows);al=exact_profiles(mm);tag=r['tags'];ci=next(i for i,m in enumerate(mm) if tag['comb'] in m['occurrences']);pi=ci-1;ji=ci-2
    assert [(z['H'],z['Q'],z['beta'],z['z'],z['sigma_E']) for z in al[ji:ci+1]]==[(1,2,2,0,0),(1,2,1,1,-1),(1,3,3,1,0)]
    assert sum(z['sigma_E'] for z in al[ji:ci+1])==-1
    assert [z['rho'] for z in al]==[z['rho'] for z in r['macro_ledger']]
    assert [z['sigma_E'] for z in al]==[z['sigma_E'] for z in r['macro_ledger']]
    by={z['occurrence']:z for z in rows};assert [by[tag[k]]['A_path'] for k in ('j','helper','comb')]==['L','RL','LL']
    assert by[117]['before'][0][0]==13 and [by[tag[k]]['target'] for k in ('j','helper','comb')]==[7,11,5]
    ok('Nonextremal critical Qj2 source verified: all three H1, helper sigma-1 and triple sigma-1; extremal source hypothesis explicitly absent')
    h0={d:u for m in mm for d,u in zip(m['demands'],m['units'])};D={d for m in mm for d in m['demands']};U={u for m in mm for u in m['units']}
    assert D-set(h0)=={(119,3)};H=dict(h0);H[(119,3)]=(120,1,1)
    assert H==I.mp(p['full_H_forward']) and len(set(H.values()))==len(H)==66 and set(H.values())<=U
    assert h0[(120,1)]==(120,1,0) and (120,1,1) not in h0.values()
    pp=p['signed_packets'];assert sorted(i for group in pp for i in group)==list(range(len(mm)))
    assert all(sum(al[i]['sigma_E'] for i in group)>=0 for group in pp)
    recover=next(group for group in pp if ci in group);assert recover==[pi,ci,ci+1,ci+2]
    assert [mm[i]['Q'] for i in recover]==[2,3,1,2] and all(mm[i]['H']==1 for i in recover)
    assert sum(al[i]['sigma_E'] for i in recover)==0
    ok('Actual forward recovery includes the -1 helper debit; complete signed source partition and physical q1 spare rebuilt, with every natural owner unchanged')
    debts=[(al[z[0]]['E_before'],al[z[-1]]['E_after']) for z in pp];K=max(x for x,y in debts);cut=next(i for i,(x,y) in enumerate(debts) if x==K)
    bank=[];hx=dict(h0);working=0
    for step in range(len(pp)):
        k=(cut+step)%len(pp);ids=pp[k];ds,dt=debts[k];assert len(bank)==K-ds
        uu=[u for i in ids for u in mm[i]['units'][:2*min(mm[i]['H'],3)]];dd=[d for i in ids for d in mm[i]['demands']];own={h0[d] for d in dd if d in h0}
        pool=[u for u in uu if u not in own]+bank;working=max(working,len(pool)+len(own))
        for d in dd:
            if d not in h0:hx[d]=pool.pop(0)
        assert len(pool)>=K-dt;bank=pool[:K-dt]
    assert not bank and hx==H and (K,working)==(p['raw_E_max'],p['raw_working'])==(2,9)
    # Rotate verified state rows, not re-execute semantic source calls.
    c=p['aligned_cut_ops'];rot=rows[c:]+rows[:c];assert rot[0]['before']==rot[-1]['after']==I.fr(p['aligned_initial'])
    assert [(z['mode'],z['target']) for z in rot]==[tuple(v) for v in p['aligned_word']]
    assert all(rot[i]['after']==rot[(i+1)%len(rot)]['before'] for i in range(len(rot)))
    last=rows[c-1]['occurrence'];tau=lambda t:t+85 if t<=last else t
    HU={tuple([tau(d[0]),*d[1:]]):tuple([tau(u[0]),*u[1:]]) for d,u in H.items()}
    assert HU==I.mp(p['full_H_aligned']) and profile(HU)==3
    a,b=p['aligned_source_interval'];assert (a,b)==(157,241)
    assert all(a<=d[0]<=b and a<=u[0]<=b for d,u in HU.items())
    cuts=[]
    for c in range(85):
        start=a+c;tt=lambda t:t+85 if t<start else t
        hh={tuple([tt(d[0]),*d[1:]]):tuple([tt(u[0]),*u[1:]]) for d,u in HU.items()};cuts.append(profile(hh))
    assert cuts==p['all85_single_word_cut_profiles'] and max(cuts)<=6
    ok('Raw max-E working9 and actual-source rotation/absolute IDs independently verified; aligned endpoint profile3, all cyclic cut templates within6')
    assert len([z for z in al if z['sigma_E']<0])==4 and sum(z['sigma_E'] for z in al)==60
    assert sum(z['sigma_E'] for z in al if z['sigma_E']<0)==-4
    # Existing sources are control DATA, never rerun. Their negative helper
    # balances remain literal; no new theorem predicts they are nonnegative.
    old=P/'SE03_STEP3_MARKED_COMB_SIGNED_REPAYMENT_29/signed_comb_and_control_ledgers.json';raw=old.read_bytes();pins[old.relative_to(P).as_posix()]=hashlib.sha256(raw).hexdigest();control=json.loads(raw)
    weak=control['reports'][0];assert any(z['sigma_E']==-1 for z in weak['macro_ledger'])
    assert [(z['source'],len(z['negative_sigma_E'])) for z in control['controls']]==[('W199',4),('W459',8)]
    ok('Old C29 -1 and C28 W199/W459 controls reused without replay or changed owners; new N helper-only sum-4 and full signed sum60 kept separate')
    def legal(m):return set(m)==D and len(set(m.values()))==len(m) and set(m.values())<=U and all(m[d]==u for d,u in h0.items())
    bad=dict(H);bad[(119,3)]=(120,1,0);assert not legal(bad)
    bad=dict(H);bad[(119,3)]=(35,1,1);assert not legal(bad)
    bad=dict(H);bad[(120,1)]=(120,1,1);assert not legal(bad)
    assert I.queries==344 and I.queries<=QCAP
    out('independent_audit.json',{'status':'PASS_DISTINCT_IMPLEMENTATION_EXACT_SOURCE_AND_FORWARD_TEMPLATE',
        'trust':'distinct implementation operated by SAME research agent; no external peer review or formal proof assistant',
        'checks':checks,'source_queries':I.queries,'input_sha256':pins,'original_period':[lo,hi],'aligned_period':[a,b],
        'A':109,'QF':66,'QE':42,'aux_core':next(iter(erased_cores)),'critical_triple_sigma_E':-1,'forward_packet_sigma_E':0,
        'raw_working':working,'aligned_H_profile':3,'all_m_all_cut_profile_bound_by_written_induction':6,
        'helper_only_sum_per_word':-4,'full_sigma_E_per_word':60,
        'normalized_owner_interface':'conditional theorem: actual supplied normalized a, original path eligibility/transport, B_a<=9; no unsupplied f5/raw replacement claimed',
        'uniformity':'written deterministic returning-word, opaque-gap and cut symmetric-difference proofs, not finite sampling of m/populations',
        'principal_NH30_closed':False,'Coarse_Double_counterexample':False,'Gate_U_unconditional':False})
    print(json.dumps({'status':'C30_INDEPENDENT_PASS','source_queries':I.queries,'checks':len(checks),'aux_core':next(iter(erased_cores))}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
