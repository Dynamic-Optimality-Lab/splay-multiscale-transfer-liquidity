"""Resume ONLY the failed Gamma boundary metadata and remaining final checks.
The completed fourteen independent source/owner receipts are reused.
"""
import importlib.util,json,textwrap,time
from pathlib import Path
B=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('completed_CD6_audit_prefix',B/'audit_final.py')
V=importlib.util.module_from_spec(s);s.loader.exec_module(V)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def read(n):return json.loads((B/n).read_text())
def unpack(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def main():
    fail=read('run_final_result.json')
    assert fail['status']=='FAILED_OR_UNKNOWN' and fail['error']['type']=='AssertionError'
    log=(B/'log_final.txt').read_text()
    assert 'assert 12 in gen and 13 in gen and not any(8<j<12 for j in gen)' in log
    reports=[json.loads(p.read_text()) for p in sorted(B.glob('source_*.json'))]
    assert len(reports)==14 and {r['core'] for r in reports}==set(range(6,12))
    receipt_hashes=[]
    for r in reports:
        f,h,h0,prior,fE=map(unpack,(r['f'],r['h'],r['h0'],r['prior'],r['fE']))
        D={(z['occurrence'],j) for z in r['chart_corrections'] for j in range(1,z['qF']+1)}
        E={(z['occurrence'],j) for z in r['chart_corrections'] for j in range(1,z['qE']+1)}
        assert set(f)==set(h)==D and len(set(f.values()))==len(set(h.values()))==len(D)==r['QF']
        assert len(E)==r['QE'] and set(fE)==E and len(set(fE.values()))==len(E)
        assert all(h[d]==u for d,u in h0.items()) and all(f[d]==u for d,u in prior.items())
        assert all(f[d]==fE[d] for d in D&E)
        assert r['full_and_aux_closure'] and r['fixed_labeled_core'] and r['all_old_values_fixed'] and r['working_bound']==11
        a,b=r['actual_period'];assert all(a<=u[0]<=b and u[1]>=1 and u[2] in(0,1) for u in f.values())
        p=B/('source_'+r['name']+'.json');receipt_hashes.append({'path':p.name,'sha256':V.sha(p)})
    out('source_receipt_recovery.json',{'status':'PASS_REUSE_ALL_COMPLETED_INDEPENDENT_SOURCE_AND_OWNER_CHECKS',
        'receipts':receipt_hashes,'old_rows_replayed_once':3328,'old_immutable_calls_once':4850,
        'failed_assertion_scope':'auxiliary boundary metadata after all fourteen receipts, not source replay/funding/owner checks',
        'new_semantic_rows_replayed':0,'new_source_engine_calls':0})
    gamma=V.read('SE03_STEP2_REPAY01','source_term_derivation.json');g=next(r for r in reports if r['name']=='Gamma26')
    previous=(gamma['initial_full_and_A'],gamma['initial_full_and_A'],gamma['initial_recurrent_E']);rows=[];gen=[]
    base=g['actual_period'][0]-1
    for t,r in enumerate(gamma['trace'],1):
        x,mode=r['key'],r['mode'];after=tuple(r['end_terms']);a,qf,qe=r['costs']
        if mode=='K' and x!=gamma['erased_key'] and previous[2][0]!=x:gen.append(t)
        rows.append({'occurrence':base+t,'mode':mode,'target':x,'genuine_F':mode=='K' and previous[1][0]!=x,
            'a':a,'qF':qf,'qE':qe,'before':previous,'after':after})
        previous=after
    assert sum(r['a'] for r in rows)==34 and sum(r['qF'] for r in rows)==30 and sum(r['qE'] for r in rows)==24
    assert 12 in gen and 13 in gen and not any(8<j<12 for j in gen),gen
    assert rows[12]['a']==1 and rows[12]['qE']==4 and rows[12]['qF']==5 and rows[9]['a']==4 and rows[8]['a']==1
    legal=[j for j in gen if j!=12];transport=[]
    for cut in legal:
        assert len({int(t<=cut) for t in (9,10,13)})==1
        delta=cut%26;copy_start=2000000+cut-delta
        got=V.realize_aligned_period({(9,1):(10,3,0),(13,5):(10,3,1)},26,copy_start,delta)
        assert len(set(got.values()))==2 and all(2000000+cut<t<=2000000+cut+26 for t,j,b in got.values())
        transport.append({'cut':cut,'pairs':V.pack(got)})
    out('gamma_period_replay.json',{'status':'PASS_ORIGINAL_GAMMA26_SOURCE_AND_LEGAL_CUTS','A':34,'QF':30,'QE':24,
        'immutable_replay_reused':'source_Gamma26.json, completed before initial metadata assertion',
        'source':str(V.P/'SE03_STEP2_REPAY01/source_term_derivation.json'),'source_sha256':V.sha(V.P/'SE03_STEP2_REPAY01/source_term_derivation.json'),
        'auxiliary_genuine_boundaries':gen,'erased_KEEP_excluded':gamma['erased_key'],
        'forced_D12_D13':[0,2],'forbidden_cut':12,'reason':'H1Q4 and inherited range[0,2]; genuine auxiliary boundaries only',
        'donor_actual_macro_event_ordinal':4,'selected_events_by_original_fE':'first<=3; donor excluded without guessing other fE values',
        'donors':[(10,3,0),(10,3,1)],'full_demands':[(9,1),(13,5)],'legal_cut_transports':transport})
    # Reuse the UNEXECUTED remaining old audit suffix exactly, with its
    # load-bearing implementation checks. Add the continuation's provenance
    # files to the final seal. Nothing in the completed source prefix is run.
    source=(B/'audit_final.py').read_text()
    tail=source.split('    # Adversarial NEW interface errors; no source theorem is reopened.\n',1)[1].split("\nif __name__=='__main__':",1)[0]
    tail=textwrap.dedent(tail)
    old="names=docs+['cd6_allocator.py','audit_final.py','six_core_certificate_ledger.json'"
    new="names=docs+['cd6_allocator.py','audit_final.py','audit_resume.py','AUDIT_CONTINUATION.md','source_receipt_recovery.json','six_core_certificate_ledger.json'"
    assert old in tail;tail=tail.replace(old,new)
    V.calls=4850;V.replayed=3328
    namespace={'reports':reports,'rows':rows,'E':{tuple(z['demand']) for z in g['fE']},'fE':unpack(g['fE']),'prior':unpack(g['prior'])}
    exec(compile(tail,str(B/'audit_final.py')+':UNEXECUTED_REMAINING_SUFFIX','exec'),V.__dict__,namespace)
    assert read('CD6_FINAL_CERTIFICATE.json')['status']=='PROVED_COMPLETE_ORIGINAL_SIX_KEY_COARSE_DOUBLE'
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_resume_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'old_semantic_rows_replayed':0,'reused_previously_replayed_rows':3328,'new_finite_tests':0})
