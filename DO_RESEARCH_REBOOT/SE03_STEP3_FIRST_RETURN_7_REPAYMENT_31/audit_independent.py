"""Distinct mutable implementation of the revised legal PREFIX first return.
Only30 new actual accesses; all old reaching-prefix facts reused unchanged.
Closed completion is proved by an explicit inverse/reset/periodization schema,
not falsely represented as a replay of the enormous closed period.
"""
import importlib.util,json,sys,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2]);CAP=float(sys.argv[1]);START=time.process_time()
sp=importlib.util.spec_from_file_location('FR31_mutable_source',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
def tick():
    if I.queries>=QCAP or time.process_time()-START>=CAP-1:raise TimeoutError('FR31 inherited audit/query cap')
    I.queries+=1
I.tick=tick
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def stats(z):
    x=z['target'];pa,ch=I.marked(z['before'][1],I.M);_,nc=I.marked(z['after'][1],I.M);anc=[];a=pa[x]
    while a is not None:anc.append(a);a=pa[a]
    E=lambda cc:sum(max(len(v)-2,0) for v in cc.values());beta=sum(len(ch[v])>=2 for v in anc);k3=sum(len(ch[v])>=3 for v in anc);leaf=int(not ch[x]);c=min(z['a'],3)
    assert len(anc)==z['qF']
    return {'occurrence':z['occurrence'],'target':x,'H':z['a'],'QF':z['qF'],'QE':z['qE'],'beta':beta,'z':leaf,'k3':k3,
        'rho':2*c-beta-leaf,'E_before':E(ch),'E_after':E(nc),'sigma_E':2*c-z['qF']+E(nc)-E(ch),
        'A_path':z['A_path'],'BF_path':z['BF_path'],'marked_before':ch,'marked_after':nc}
def inverse_word(a):
    if not a:return []
    result=[a[0]]
    for x in inverse_word(a[1:]):result.extend((x,a[0]))
    return result
def main():
    oldpath=P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json';old=json.loads(oldpath.read_text());initial=I.fr(next(z for z in old['rows'] if z['occurrence']==116)['before'])
    word=[('D',x) for x in (11,7,9,11,7,13)]+[('K',x) for x in (13,7,11,5,11,9,5,7,11)]
    rows,end=I.execute(initial,word,116)
    out('prefix_candidate_rows.json',{'status':'EXACT_NEW_MUTABLE_ROWS_BEFORE_ASSERTIONS','start_after115':initial,'word':word,'rows':rows,'end':end,'queries':I.queries})
    assert I.queries==30
    ledger=[stats(z) for z in rows if z['occurrence']>=123]
    assert [z['target'] for z in ledger]==[7,11,5,11,9,5,7,11]
    assert [z['H'] for z in ledger]==[1]*8
    assert [z['QF'] for z in ledger]==[2,2,3,1,3,1,2,2]
    assert [z['sigma_E'] for z in ledger]==[0,-1,0,0,0,0,0,1]
    assert [z['A_path'] for z in ledger[:3]]==['L','RL','LL']
    assert all(I.core(z['before'][1],I.M)==set(range(1,14)) and I.core(z['after'][1],I.M)==set(range(1,14)) for z in rows)
    assert all(ev['kind']=='DOUBLE' and ev['case'] in ('LL','RR') and ev['G'] in I.M and ev['P'] not in I.M for z in rows for ev in z['BF_events'])
    assert sum(z['sigma_E'] for z in ledger[1:7])==-1 and sum(z['sigma_E'] for z in ledger[1:])==0
    assert ledger[1]['E_before']==1 and ledger[6]['E_after']==0 and ledger[7]['E_after']==1
    # The six prep DELETEs belong to the previous natural macro, before
    # the KEEP13 synchronization; j itself contains only the one KEEP7.
    assert rows[6]['target']==13 and rows[6]['mode']=='K' and rows[6]['a']==0
    assert all(z['mode']=='K' for z in rows[7:])
    prefix_rows=[I.fr_row(z) for z in old['rows'][:30]]+rows;Pword=[tuple(z) for z in old['period'][:30]]+word
    inv=[];receipts=[]
    for z in reversed(prefix_rows):
        if z['mode']!='K':continue
        pa=I.parent_map(z['before'][1]);x=z['target'];path=[];v=x
        while pa[v] is not None:path.append(pa[v]);v=pa[v]
        # Physical BF path already checked: root-first G at even depths.
        t=z['before'][1];anc=[]
        for i,ch in enumerate(z['BF_path']):
            if i%2==0:anc.append(t[0])
            t=t[1 if ch=='L' else 2]
        assert len(anc)==z['qF'];targets=inverse_word(anc);assert len(targets)==2**len(anc)-1
        inv.extend(('K',x) for x in targets);receipts.append({'prefix_occurrence':z['occurrence']-85,'root_first_ancestors':anc,'q':len(anc),'targets':targets})
    reset=[('D',x) for x in range(13,0,-1)]+[('D',3)];W=Pword+inv+reset
    assert len(Pword)==45 and len(inv)==38 and len(W)==97
    assert max(z['q'] for z in receipts)==3 and sum(z['q']==3 for z in receipts)==2
    assert sum(z['q'] for z in receipts)==25
    # Fully literal local physical matching. This is a separate comparer,
    # not an assertion that its donors are free under supplied normalized a.
    sub=[z for z in rows if 124<=z['occurrence']<=129];h0={};D=set();U=set()
    for z in sub:
        units=[(z['occurrence'],j,b) for j in range(1,z['a']+1) for b in (0,1)];dd=[(z['occurrence'],k) for k in range(1,z['qF']+1)];h0.update(zip(dd,units));D.update(dd);U.update(units)
    H=dict(h0);H[(125,3)]=(126,1,1);H[(127,3)]=(128,1,1)
    assert set(H)==D and len(H)==len(set(H.values()))==12 and set(H.values())==U
    assert sum(z['a'] for z in sub)==6 and sum(z['qF'] for z in sub)==12
    certificate={'status':'EXACT_PREFIX_FIRST_RETURN_REFUTATION_WITH_SYMBOLIC_FULL_CLOSED_COMPLETION',
        'scope':'FR31-PREFIX per explicit user clarification; FR31-FIX separate and OPEN',
        'accepted_source_dependency':str(oldpath),'accepted_source_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),
        'original_diagonal_tree':old['original_diagonal_tree'],'known_reaching_prefix_N':old['reaching_prefix'],
        'known_synchronized_A0':old['initial'][0],'known_erased_seed_E0':old['initial'][2],
        'cached_original_first30_rows':old['rows'][:30],'start_after115':initial,'new_word':word,'new_rows':rows,'ledger':ledger,
        'j':123,'helper':124,'comb':125,'first_upper':126,'activate9':127,'bridge5':128,'first_return7':129,'next_recovery11':130,
        'low_phase':[],'Sigma_low':0,'D_entry':1,'R_return':0,'Sigma_helper_through_first_return':-1,'Sigma_through_next11':0,
        'local_native_h0':[{'demand':d,'unit':u} for d,u in sorted(h0.items())],
        'local_full_comparison':[{'demand':d,'unit':u} for d,u in sorted(H.items())],
        'first_return_actual_A':6,'first_return_full_Q':12,'first_return_original_price':0,
        'P_word':Pword,'inverse_word':inv,'inverse_receipts':receipts,'last_A_reset':reset,'closed_block_W':W,
        'W_length':97,'prefix_genuine_KEEPs':len(receipts),'inverse_genuine_KEEPs':len(inv),'full_W_Q':76,'CD_safe_margin_lower_bound':32,
        'symbolic_closed_history':{'C':'Catalan(13)=742900','M':'factorial(742900)',
            'reaching_word':'N followed by W^C','period_word':'W^M',
            'initial_A':'known_synchronized_A0','initial_BF':'original_diagonal_tree',
            'initial_BE':'F_E^C(known_erased_seed_E0)','F_E':'exact ordinary bottom-up execution of W with KEEP11 erased',
            'first_counter_helper_absolute':85+97*742900+39,'first_counter_upper_absolute':85+97*742900+41,
            'first_counter_return_absolute':85+97*742900+44,
            'closure_certificate':'root-first SS inverse identity, ordered A reset, finite deterministic13-anchor BST orbit period divides C!',
            'all_other_erasure_periods':'same finite-state bound aligns any fixed further KEEP-subsequence erasure; original legal cut still requires its actual receipt'},
        'verification_scope':'new local source replay only; old source facts reused; full97-word and enormous period closure proved symbolically, NOT replayed',
        'source_queries':I.queries,'historical_owners_changed':False,'Coarse_Double_counterexample':False}
    out('prefix_first_return_countercertificate.json',certificate)
    out('independent_audit.json',{'status':'PASS_DISTINCT_MUTABLE_LOCAL_SOURCE_WITH_EXPLICIT_SYMBOLIC_COMPLETION',
        'source_queries':I.queries,'trust':'distinct implementation operated by SAME research agent; not external peer review/formal proof assistant',
        'new_actual_operations':len(word),'new_A_BF_BE_queries':30,'all_BF_SS_core13_verified':True,
        'first_return_sigma_E':-1,'upper_return_contribution':0,'entry_debt':1,'later_recovery_sigma_total':0,
        'independent_local_physical_demand_units':12,'full_closed_history_replayed':False,
        'completion':'written root-first inverse/reset/finite-orbit proof schema; separate arithmetic audit required',
        'FR31_PREFIX_refuted':True,'FR31_FIX_refuted':False,
        'input_sha256':{str(oldpath):hashlib.sha256(oldpath.read_bytes()).hexdigest()}})
    print(json.dumps({'status':'FR31_PREFIX_COUNTER_CHECKED','queries':I.queries,'first_return_sigma':-1,'next11_total':0,'W_length':97,
        'full_period_closure':'symbolic, not replayed'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
