"""Independent physical source and iterative join countercertificates."""
import json,time,sys,pickle,hashlib,importlib.util
from pathlib import Path
from audit_verify37 import fr,node,renumber
from closed_word_composition_independent_v2 import audit_word
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def count(t):return 0 if not node(t) else 1+count(t[1])+count(t[2])
def merge(L,R,p,rule):
    stack=[]
    while node(L) and node(R):
        choose=True if rule=='predecessor' else abs(L[0]-p)<=abs(R[0]-p) if rule=='nearest_root' else count(L)<=count(R)
        if choose:stack.append(('L',L));L=L[2]
        else:stack.append(('R',R));R=R[1]
    v=L if node(L) else R
    for side,t in reversed(stack):v=(t[0],t[1],v) if side=='L' else (t[0],v,t[2])
    return v
def project(t,p,rule):
    if not node(t):return t
    L,R=project(t[1],p,rule),project(t[2],p,rule)
    return merge(L,R,p,rule) if t[0]==p else (t[0],L,R)
def main():
    global queries
    native=json.loads((B/'native10_source_actions.json').read_text());N=len(native['trees']);idx={fr(t):i for i,t in enumerate(native['trees'])};mir=native['mirror'];raw=(B/'native10_B_modal_factored_debt.pkl').read_bytes();receipt=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==receipt['input_sha256']['native10_B_modal_factored_debt.pkl'];O=pickle.loads(raw);del raw;D=lambda a,b:O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    G=json.loads((B/'four_hull_source_basis_independent_audit.json').read_text());assert G['status'].startswith('PASS')
    sp=importlib.util.spec_from_file_location('independent_second_gap_join33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=int(sys.argv[2]) or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_CAP')
        queries+=1
    I.tick=tick;proofs=[];files=[]
    for name in ('nearest_root','predecessor'):
        file='second_gap_'+name+'_closed_source.json';files.append(file);z=json.loads((B/file).read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in z['input_sha256'].items());e=z['candidate'];p=e['private_key'];proof=audit_word(z,native,G['source_kernel'],I,tick)
        for rule in (('predecessor','smaller_side') if name=='predecessor' else ('nearest_root',)):
            sa=idx[renumber(project(fr(e['source_A']),p,rule))];ta=idx[renumber(project(fr(e['actual_A_target']),p,rule))];ds,dt=D(sa,e['source_B_core_index']),D(ta,e['B_target_core_index']);assert (sa,ta)==(e['old_source_A_index'],e['old_projected_target_index']) and (ds,dt,e['H'],e['Q'],e['price'])==(1,0,1,2,0);proofs.append({'rule':rule,'old_projected_indices':[sa,ta],'debt':[ds,dt],'signed_margin':-1,'closed_source':file,'source_verification':proof})
    assert time.process_time()-START<CAP-1
    files+=['closed_word_composition_independent_v2.py','native10_modal_oracle_independent_audit.json','native10_source_independent_audit.json','four_hull_source_basis_independent_audit.json','second_gap_join_candidates_continuation.json']
    out('second_gap_join_independent_audit.json',{'status':'PASS_SOURCE_EXACT_THREE_SECOND_GAP_JOIN_REFUTATIONS','private_key':5,'anchor_physical_keys':list(range(2,21,2)),'three_distinct_candidate_rules':proofs,'source_queries':queries,'source_engine_calls':queries,'verification_method':'independent iterative zipper join and mutable non-hull splays; all other original operations composed from accepted complete source bases','not_an_arbitrary_geometry_rule_refutation':True,'not_a_CD_counterexample':True,'frozen_owners_unchanged':True,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}});print(json.dumps({'status':'PASS_THREE_SECOND_GAP_JOIN_REFUTATIONS','source_queries':queries,'rules':len(proofs)}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify53_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
