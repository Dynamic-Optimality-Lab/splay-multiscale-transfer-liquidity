"""Two precise cross-boundary reset checks,26 A-only source calls.
All remaining original block operations reuse their accepted identical states.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=min(26,int(sys.argv[2]))
sp=importlib.util.spec_from_file_location('C30_reset_cross_source',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
def path(t,x):
    if C.queries>=QCAP:raise TimeoutError('cross-boundary query cap')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    old=json.loads((P/'SE03_STEP3_MARKED_COMB_SIGNED_REPAYMENT_29/comb_source_fixtures.json').read_text());new=json.loads((B/'nonextremal_source_countercertificate.json').read_text());p=json.loads((B/'forward_recovery_and_period_receipt.json').read_text())
    W=old['reports'][0];SW=fr(W['initial']);SU=fr(p['aligned_initial']);assert SW[1:]==SU[1:] and SW[0][0]==SU[0][0]==3
    assert W['period'][:13]==[['D',x] for x in range(13,0,-1)]==p['aligned_word'][:13]
    wbase=sum(r['a'] for r in W['rows'][:13]);ubase=sum(r['a'] for r in new['rows'][p['aligned_cut_ops']:p['aligned_cut_ops']+13])
    expected=fr(W['rows'][12]['after'][0]);assert expected==fr(new['rows'][p['aligned_cut_ops']+12]['after'][0])
    reports=[]
    for name,start,cost in [('W_to_U',SW,wbase),('U_to_W',SU,ubase)]:
        a=start[0];rr=[]
        for i,x in enumerate(range(13,0,-1),1):
            before=a;a,pa,ev=C.tr(a,x);rr.append({'occurrence':i,'mode':'D','target':x,'before_A':before,'after_A':a,'A_path':pa,'A_events':ev,'a':len(ev)})
        assert a==expected and sum(z['a'] for z in rr)==cost
        assert rr[0]['a']>=1
        reports.append({'name':name,'initial':start,'rows':rr,'reset_A_cost':cost,'after_A':a,'B_and_BE_frozen':True})
    out('mixed_reset_bridge_receipt.json',{'status':'EXACT_TWO_RESET_BRIDGES_PENDING_DISTINCT_AUDIT','reports':reports,'W_boundary':SW,'U_boundary':SU,
        'reset_cost_W':wbase,'reset_cost_U':ubase,'word_types':['W0','W1','U'],'queries':C.queries,
        'cyclic_total_A_formula':'158*n0+159*n1+109*nU, because each cross-reset correction R(previous endpoint)-R(destination endpoint) telescopes',
        'source_only_scope':'full mixed source and independent signed/comparison license; actual supplied normalized owners still require the stated profile/eligibility hypotheses'})
    print(json.dumps({'status':'MIXED_RESET_BRIDGES','queries':C.queries,'reset_cost_W':wbase,'reset_cost_U':ubase}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source6_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
