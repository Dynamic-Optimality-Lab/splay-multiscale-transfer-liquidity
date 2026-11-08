"""H1 retirement free identities; H2 no-simulation and full source closure."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
from audit_verify36 import calc,mirror
from audit_verify37 import fr,node,renumber
from closed_word_composition_independent_v2 import audit_word
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def retire(t,p):
    if not node(t):return t
    if t[0]==p:
        assert not node(t[1]) or not node(t[2])
        return retire(t[2] if t[1]=='E' else t[1],p)
    return t[0],retire(t[1],p),retire(t[2],p)
def main():
    global queries
    # Two exhaustive H1 orientations and literal reflected equations.
    h1=[]
    for orientation in ('LL','LR'):
        g=6;p,x=(3,2) if orientation=='LL' else (2,3)
        source=(g,(p,(x,'A','E'),'C'),'D') if orientation=='LL' else (g,(p,'A',(x,'E','C')),'D')
        expected=(x,'A',(g,'C','D'));old=(g,(x,'A','C'),'D');after,h=calc(source,x);shadow,c=calc(old,x)
        assert h==c==1 and retire(after,p)==shadow==expected
        rafter,rh=calc(mirror(source,20),20-x);rold,rc=calc(mirror(old,20),20-x);assert rafter==mirror(after,20) and rold==mirror(expected,20) and rh==rc==1
        h1.append({'orientation':orientation,'source':source,'comparison_source':old,'projected_target':expected,'costs':[h,c],'reflected_identity':True})
    g,c,v,p,x=10,8,4,3,2;source=(g,(c,(p,(x,'A','E'),(v,'E','W')),'E'),'R');actual,h=calc(source,x);star=(x,'A',(g,(c,(v,'E','W'),'E'),'R'));assert h==2 and retire(actual,p)==star
    left=(g,(c,(x,'A',(v,'E','W')),'E'),'R');right=(g,(c,(v,(x,'A','E'),'W'),'E'),'R')
    leftdest,lh=calc(left,x);rightdest,rh=calc(right,x);assert (lh,rh)==(1,2) and leftdest!=star and rightdest!=star
    t,a=calc(left,c);t,b=calc(t,x);assert a==b==1 and t==leftdest
    for z0 in (c,v):
        t,a=calc(right,z0);t,b=calc(t,x);assert a==b==1 and t==(x,'A',(v,'E',(c,'W',(g,'E','R')))) and t!=star
    ra,rrh=calc(mirror(source,20),20-x);assert rrh==2 and ra==mirror(actual,20)
    native=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,native['trees']));idx={t:i for i,t in enumerate(T)};G=json.loads((B/'four_hull_source_basis_independent_audit.json').read_text());z=json.loads((B/'retirement_preimage_closed_source.json').read_text());e=z['candidate'];certificate=json.loads((B/'retirement_two_event_comparison_certificate.json').read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==hh for n,hh in z['input_sha256'].items())
    # Independent direct construction of BOTH joins; the inner children
    # are empty, so there are exactly two, not a bounded join selection.
    def sourcejoin(t,side):
        if not node(t):return t
        if t[0]==5:
            L,R=t[1:];assert not node(L[2]) and not node(R[1])
            return (L[0],L[1],R) if side=='L' else (R[0],L,R[2])
        return t[0],sourcejoin(t[1],side),sourcejoin(t[2],side)
    sa=[idx[renumber(sourcejoin(fr(e['source_A']),side))] for side in ('L','R')];assert sorted(sa)==sorted(e['source_contraction_indices'])==[8860,8902]
    target=idx[renumber(retire(fr(e['actual_A_target']),5))];assert target==e['target_contraction_index']==5549
    comparisons=[]
    for aa in e['source_contraction_indices']:
        for helper in [None]+list(range(1,11)):
            t=T[aa];hc=0
            if helper is not None:t,hh=calc(t,helper);hc+=hh
            t,hh=calc(t,2);hc+=hh;dest=idx[t];comparisons.append({'old_source':aa,'optional_DELETE_proxy':helper,'terminal_KEEP':2,'ordinary_H':hc,'old_destination':dest,'matches_target':dest==target});assert not(hc<=2 and dest==target)
    assert comparisons==certificate['all_comparisons']
    sp=importlib.util.spec_from_file_location('independent_retirement_source72',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=int(sys.argv[2]) or time.process_time()-START>CAP-2:raise TimeoutError('RETIREMENT_SOURCE_AUDIT_CAP')
        queries+=1
    I.tick=tick;word=audit_word(z,native,G['source_kernel'],I,tick);assert word['period']==[102,202] and word['packet_t']==139 and word['costs']==[118,18,18]
    files=('ONE_BRANCH_RETIREMENT_BOUNDARY.md','RETIREMENT_NO_TWO_EVENT_SIMULATION.md','retirement_preimage_closed_source.json','retirement_two_event_comparison_certificate.json','audit_verify72.py','closed_word_composition_independent_v2.py','native10_source_independent_audit.json','four_hull_source_basis_independent_audit.json')
    receipt={'status':'PASS_UNIFORM_H1_RETIREMENT_AND_SOURCE_EXACT_H2_NONSIMULATION','uniform_H1_source_preimage_cases':h1,'H1_exhaustiveness':'private branch must be middle of the length-two marked-root/marked-target path; two orientations and their reflections','H1_lower_envelope_corollary':'inherits a verified ordinary signed source law at its actual domain; not a signed law for arbitrary new J','uniform_H2_counterfamily':'written free-term equations and <=2 positive-event word classification; source gap is comparison geometry','exact_control_old_source_indices':sa,'exact_control_unique_target':target,'all_22_ordinary_comparisons_independently_checked':True,'original_source_verification':word,'not_a_CD_counterexample':True,'not_all_comparison_architectures_refuted':True,'frozen_owners_unchanged':True,'source_queries':queries,'source_engine_calls':queries,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}}
    assert time.process_time()-START<CAP-1
    out('retirement_boundary_independent_audit.json',receipt);print(json.dumps({'status':receipt['status'],'source_queries':queries,'period':word['period'],'ordinary_comparisons':22,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify72_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
