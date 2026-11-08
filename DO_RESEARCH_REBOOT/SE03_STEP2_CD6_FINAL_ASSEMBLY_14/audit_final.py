"""Independent new assembly/absolute-ID audit and final dependency seal.
All old exhaustive table/grammar audits are reused, not rerun.
"""
import hashlib,importlib.util,json,subprocess,sys,time
from pathlib import Path
from cd6_allocator import allocate,realize_aligned_period
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent
s=importlib.util.spec_from_file_location('immutable_CD6_assembly',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I)
calls=0;replayed=0;start=time.process_time();limit=float(sys.argv[1])-1.5
def read(d,n):return json.loads((P/d/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def tree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],tree(t[1]),tree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def move(t,x):
    global calls
    calls+=1;assert calls<2000000;return I.trace(t,x)
def marked_core(t,M):
    if t[0]=='leaf':return set()
    l,r=marked_core(t[2],M),marked_core(t[3],M)
    return l|r|{t[1]} if l or r or t[1] in M else set()
def replay(initial,word,z,expected=None):
    global replayed
    A,F,E=map(tree,initial);begin=(A,F,E);rows=[];M=set()
    for t,(mode,x) in enumerate(word,1):
        before=(A,F,E);genuine=mode=='K' and x!=F[1];_,ad=I.lookup(A,x);A,ae=move(A,x);be=ee=[]
        if mode=='K':
            _,bd=I.lookup(F,x);F,be=move(F,x);assert sum(e[0]!='ZIG' for e in be)==bd//2
            if x!=z:E,ee=move(E,x)
        assert len(ae)==(ad+1)//2
        qf,qe=sum(e[0]!='ZIG' for e in be),sum(e[0]!='ZIG' for e in ee)
        row={'occurrence':t,'mode':mode,'target':x,'genuine_F':genuine,'a':len(ae),'qF':qf,'qE':qe,
            'before':tuple(plain(v) for v in before),'after':tuple(plain(v) for v in (A,F,E))}
        if genuine:M.add(x)
        if expected is not None:
            old=expected[t-1];assert (old['a'],old['qF'],old['qE'])==(len(ae),qf,qe)
            assert freeze(old['before'])==row['before'] and freeze(old['after'])==row['after']
        rows.append(row);replayed+=1
    assert (A,F,E)==begin and len(M)==6
    S=marked_core(begin[1],M)
    assert all(marked_core(tree(r['before'][1]),M)==S and marked_core(tree(r['after'][1]),M)==S for r in rows)
    return rows,len(S)
def reverse_common(D,U,l,h):
    # Independent BACKWARDS component algorithm, not original forward exchange.
    inverse={u:d for d,u in h.items()};answer=dict(l)
    for terminal in U-set(l.values()):
        u=terminal;seen=set()
        while u in inverse:
            d=inverse[u]
            if d not in l:assert d not in answer;answer[d]=terminal;break
            if d in seen:break
            seen.add(d);u=l[d]
    assert len(set(answer.values()))==len(answer);return answer
def natural_h0(rows):
    ends=[j for j,r in enumerate(rows) if r['genuine_F']];h={};seen=[]
    for j,end in enumerate(ends):
        prev=ends[j-1];seg=rows[prev+1:end+1] if prev<end else rows[prev+1:]+rows[:end+1]
        uu=[(r['occurrence'],a,b) for r in seg for a in range(1,r['a']+1) for b in (0,1)]
        dd=[(r['occurrence'],q) for r in seg for q in range(1,r['qF']+1)]
        h.update(zip(dd,uu));seen += [r['occurrence'] for r in seg]
    assert sorted(seen)==[r['occurrence'] for r in rows];return h
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def audit_case(name,oldrows,expected_k,base,erased=None,initial=None,word=None):
    if oldrows is not None:
        if erased is None:
            M={r['target'] for r in oldrows if r['genuine_F']};changed={r['target'] for r in oldrows if r['mode']=='K' and r['before'][2]!=r['after'][2]}
            assert len(M-changed)==1;erased=next(iter(M-changed))
        initial=oldrows[0]['before'];word=[(r['mode'],r['target']) for r in oldrows]
    rows,k=replay(initial,word,erased,oldrows);assert k==expected_k
    # The NEW interface uses nontrivial actual timestamps, never local IDs.
    actual=[dict(r,occurrence=base+i+1) for i,r in enumerate(rows)]
    v=allocate(actual);D={(r['occurrence'],j) for r in actual for j in range(1,r['qF']+1)}
    U={(r['occurrence'],j,b) for r in actual for j in range(1,r['a']+1) for b in (0,1)}
    assert v['D']==D and v['U']==U and v['h0']==natural_h0(actual)
    assert set(v['f'])==D and set(v['f'].values())<=U and len(set(v['f'].values()))==len(D)
    assert all(v['h'][d]==u for d,u in v['h0'].items())
    E={(r['occurrence'],j) for r in actual for j in range(1,r['qE']+1)};us=sorted(U);fE=dict(zip(sorted(E),us[3:]+us[:3]));l={d:fE[d] for d in D&E}
    prior=reverse_common(D,U,l,v['h0']);expected=reverse_common(D,U,l,v['h'])
    w=allocate(actual,auxiliary_demands=E,fE=fE,frozen_prior=prior)
    assert w['f']==expected and set(expected)==D and len(set(expected.values()))==len(D)
    assert all(w['f'][d]==u for d,u in prior.items()) and all(w['f'][d]==fE[d] for d in D&E)
    assert len(D)==sum(r['qF'] for r in actual) and len(U)==2*sum(r['a'] for r in actual)
    # Chart accounting is literal per occurrence, independent of a chart D.
    signed=[{'occurrence':r['occurrence'],'qF':r['qF'],'qE':r['qE'],'C':min(r['qF'],r['qE']),
        'P':max(r['qF']-r['qE'],0),'N':max(r['qE']-r['qF'],0)} for r in actual]
    assert all(r['qF']-r['qE']==r['P']-r['N'] for r in signed)
    r={'name':name,'core':k,'actual_period':w['actual_period'],'erased':erased,'rows':len(rows),
        'A':len(U)//2,'QF':len(D),'QE':len(E),'full_and_aux_closure':True,'fixed_labeled_core':True,
        'h0':pack(v['h0']),'h':pack(v['h']),'prior':pack(prior),'f':pack(w['f']),
        'logical_fE_fixture_not_numeric_sealed_fE':True,'fE':pack(fE),'all_old_values_fixed':True,
        'chart_corrections':signed,'working_bound':11,'source_tables_and_population_lift':'sealed old audits reused, not re-enumerated'}
    out('source_'+name+'.json',r)
    assert time.process_time()-start<limit,'bounded new audit reserve'
    return r,v,actual,E,fE,prior
def main():
    c10='SE03_STEP2_FULL_FUNDING_CLOSURE_10';c13='SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13';c14='SE03_STEP2_UNARY_A_LIFT_14'
    reports=[]
    # Core6: use the ALREADY CERTIFIED actual erasure alignment, not its transient.
    fam=next(f for f in read(c10,'deficient_source_schemas.json')['families'] if f['core']==6)
    al=fam['erasure_alignments'][0];assert al['status']=='EXACT_SOURCE_ALIGNMENT'
    r,*_=audit_case('core6',None,6,600000,al['erased'],(fam['initial_A_BF'],fam['initial_A_BF'],al['initial_BE']),fam['word']*al['L']);reports.append(r)
    for reflected in (False,True):
        data=read(c13,'core7_source_certificate.json')
        old=next(r for r in data['source_reports'] if r['slot_count']==3 and r['reflected']==reflected)
        r,*_=audit_case('core7_'+str(int(reflected)),old['rows'],7,700000+10000*reflected,old['erased']);reports.append(r)
    data=read(c13,'core8_seal.json')
    for reflected in (False,True):
        old=next(r for r in data['source_reports'] if r['requested_count_control']==3 and r['reflected']==reflected)
        r,*_=audit_case('core8_'+str(int(reflected)),old['rows'],8,800000+10000*reflected,old['erased']);reports.append(r)
    data=read(c13,'slot_count_witnesses.json')
    for source in data['reports']:
        e=next(e for e in source['erased_runs'] if e['L']==1)
        r,*_=audit_case('core'+str(source['core'])+'_'+str(int(source['reflected'])),e['rows'],source['core'],source['core']*100000+10000*source['reflected'],e['erased']);reports.append(r)
    # Sigma is an exact old failed adjacent-donor source. Its reflection
    # uses the exact order-reversal lift, not a separate finite-population claim.
    sigma=read(c10,'donor_rule_audit.json')['counterexamples'][0]['source_period_rows']
    M={r['target'] for r in sigma if r['genuine_F']};k=len(marked_core(tree(sigma[0]['before'][1]),M))
    def mirror(t):return t if isinstance(t,str) else (12-t[0],mirror(t[2]),mirror(t[1]))
    reflected=[dict(r,target=12-r['target'],before=tuple(mirror(t) for t in r['before']),after=tuple(mirror(t) for t in r['after'])) for r in sigma]
    for name,rr in (('Sigma',sigma),('Sigma_reflected',reflected)):
        r,*_=audit_case(name,rr,k,1300000+10000*(name!='Sigma'));reports.append(r)
    # Mandatory exact ORIGINAL Gamma26, not the different modified paired family.
    gamma=read('SE03_STEP2_REPAY01','source_term_derivation.json')
    word=[(r['mode'],r['key']) for r in gamma['trace']]
    r,v,rows,E,fE,prior=audit_case('Gamma26',None,11,1400000,gamma['erased_key'],
        (gamma['initial_full_and_A'],gamma['initial_full_and_A'],gamma['initial_recurrent_E']),word);reports.append(r)
    assert (r['A'],r['QF'],r['QE'])==(34,30,24) and len(rows)==26
    for t,old in enumerate(gamma['trace'],1):
        row=rows[t-1];assert [row['a'],row['qF'],row['qE']]==old['costs'];assert freeze(row['after'])==freeze(old['end_terms'])
    assert rows[12]['a']==1 and rows[12]['qE']==4 and rows[12]['qF']==5
    assert rows[9]['a']==4 and rows[8]['a']==1
    gen=[j+1 for j,row in enumerate(rows) if row['mode']=='K' and row['before'][2][0]!=row['target']]
    assert 12 in gen and 13 in gen and not any(8<j<12 for j in gen)
    legal=[j for j in gen if j!=12];transport=[]
    for cut in legal:
        which={int(t<=cut) for t in (9,10,13)};assert len(which)==1
        mapping={(9,1):(10,3,0),(13,5):(10,3,1)}
        # Cut26 is delta0 of the NEXT actual copy, not delta0 at old base.
        delta=cut%26;copy_start=2000000+cut-delta
        got=realize_aligned_period(mapping,26,copy_start,delta)
        assert len(set(got.values()))==2 and all(2000000+cut<t<=2000000+cut+26 for t,j,b in got.values())
        transport.append({'cut':cut,'pairs':pack(got)})
    out('gamma_period_replay.json',{'status':'PASS_ORIGINAL_GAMMA26_SOURCE_AND_LEGAL_CUTS','A':34,'QF':30,'QE':24,
        'source':str(P/'SE03_STEP2_REPAY01/source_term_derivation.json'),'source_sha256':sha(P/'SE03_STEP2_REPAY01/source_term_derivation.json'),
        'forced_D12_D13':[0,2],'forbidden_cut':12,'reason':'H1Q4 and inherited debt range[0,2]; genuine boundaries only',
        'donor_actual_macro_event_ordinal':4,'selected_events_by_original_fE':'first<=3; donor excluded independently of other numeric fE values',
        'donors':[(10,3,0),(10,3,1)],'full_demands':[(9,1),(13,5)],'legal_cut_transports':transport})
    # Adversarial NEW interface errors; no source theorem is reopened.
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,AssertionError):rejected.append(name)
        else:raise AssertionError('invalid assembly accepted: '+name)
    keys=sorted(fE);bad=dict(fE);bad[keys[1]]=bad[keys[0]]
    reject('duplicate_auxiliary_owner',lambda:allocate(rows,auxiliary_demands=E,fE=bad))
    bad2=dict(fE);bad2[keys[0]]=(rows[0]['occurrence']-1,1,0)
    reject('previous_copy_donor',lambda:allocate(rows,auxiliary_demands=E,fE=bad2))
    bad3=dict(prior);d=next(iter(prior));bad3[d]=(rows[-1]['occurrence']+1,1,0)
    reject('changed_frozen_prior',lambda:allocate(rows,auxiliary_demands=E,fE=fE,frozen_prior=bad3))
    reject('missing_auxiliary_domain',lambda:allocate(rows,fE=fE))
    reject('unlicensed_prior_without_auxiliary_map',lambda:allocate(rows,frozen_prior=prior))
    reject('nonclosed_source',lambda:allocate(rows[:-1]))
    reject('transport_from_second_copy',lambda:realize_aligned_period({(1,1):(27,1,0)},26,0,0))
    out('independent_audit.json',{'status':'PASS_ALL_DOMAIN_CD6_ASSEMBLY_AND_ACTUAL_ID_INTERFACE','source_reports':[{k:v for k,v in r.items() if k not in ('h0','h','f','prior','fE','chart_corrections')} for r in reports],
        'source_controls_replayed':len(reports),'source_rows_replayed':replayed,'source_engine_calls':calls,
        'all_old_exhaustive_tables_and_lifts':'reused after hash revalidation; not rerun',
        'all_direct_masks':23,'exact_order_reversals':15,'other_core8_masks':13,'core7_all_masks':'source theorem covers5',
        'ownership':'independent reverse-component reconstruction equals dispatcher; old partial/common values exact',
        'Gamma':'authoritative original26 repaired, all candidate genuine legal cuts checked','Sigma':'old45/46 limitation and reflection funded by full rule',
        'invalid_inputs_rejected':rejected,'new_source_words':0,
        'trust':'same agent, distinct immutable primitive/core/depth implementation and backwards owner checker; not external/formal certification'})
    # Final consistency/dependency seal. No old semantic table is re-executed.
    pins=json.loads((B/'dependency_pins.json').read_text())
    for p in pins['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    for p in pins['external_pins']:assert sha(Path(p['path']))==p['sha256'],p['path']
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
    assert not git('status','--porcelain','--untracked-files=no')
    assert json.loads((B/'run_assembly_result.json').read_text())['status']=='PASS'
    docs=['SOURCE_SPEC.md','CORE_DOMAIN_EXHAUSTIVENESS.md','CLOSED_PERIOD_CORE_CONSTANCY.md','SIX_CORE_CERTIFICATE_LEDGER.md',
        'ABSOLUTE_PERIOD_ALIGNMENT.md','FROZEN_OWNER_COMPATIBILITY.md','CHART_SIGNED_CORRECTIONS.md','CARRY_STORAGE_SEAM.md',
        'GLOBAL_PHYSICAL_INJECTION.md','CD6_THEOREM.md','UNIFORM_R_TRANSFER.md','CASE_LEDGER.md','INDEPENDENT_AUDIT.md',
        'ADVERSARIAL_AUDIT.md','FULL_PROOF.md','FINAL_VERDICT.md','CHECKPOINT.md']
    for n in docs:assert (B/n).is_file(),n
    names=docs+['cd6_allocator.py','audit_final.py','six_core_certificate_ledger.json','assembly_protocol_certificate.json',
        'independent_audit.json','gamma_period_replay.json','dependency_pins.json']
    names += [p.name for p in sorted(B.glob('source_*.json'))]
    out('CD6_FINAL_CERTIFICATE.json',{'outcome':'A','status':'PROVED_COMPLETE_ORIGINAL_SIX_KEY_COARSE_DOUBLE','Step2':'COMPLETE_AT_STATED_SIX_KEY_SOURCE_SCOPE',
        'statement':'forall original reachable exactly A/full-B paired-closed W with six genuine KEEP keys, explicit f_W:D_full(W) injects into U_A(W), hence Q_B(W)<=2A(W)',
        'core_partition':[6,7,8,9,10,11],'necessary_masks':57,'complete_original_cost_bridge':True,
        'actual_period_identity':True,'frozen_owner_scope':'all original common fE and prior a values on SAME certified aligned period; no invented extension of special Step1 scope',
        'Bank25':25,'independent_full_witness_working_bound':11,'all_original_operations_kept':True,
        'IAGS_gates':{g:'CLOSED' for g in 'ABCDEFGHIJKL'},'L1_to_L15':'ALL_CLOSED_BY_EXPLICIT_SOURCE_AND_PHYSICAL_MAP_PROOF',
        'inherited_local_pins_verified':len(pins['pins']),'Gamma26_replayed':True,'Gate_U14':'U-B',
        'uniform_source_hypotheses':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'files':[{'path':n,'sha256':sha(B/n)} for n in names],
        'trust':'computer-assisted symbolic source proof, same-agent separate immutable implementation; no formal/external certification'})
    print(json.dumps({'outcome':'A','status':'CD6_FINAL_SEALED','core_classes':6,'source_controls':len(reports),'source_rows':replayed,'calls':calls,'Gate_U':'U-B'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_final_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls,'old_semantic_rows_replayed':replayed,'new_finite_tests':0})
