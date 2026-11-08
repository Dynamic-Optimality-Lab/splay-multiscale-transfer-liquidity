"""Independent closed-source refutation of three actual-B-guided projections."""
import collections,hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
from audit_verify37 import fr,node,renumber
from closed_word_composition_independent_v2 import audit_word
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);queries=0

def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)

def keys(t):return set() if not node(t) else keys(t[1])|{t[0]}|keys(t[2])

def project(tree,private,Btree,rule):
    queue=collections.deque([(Btree,0)]);levels={};order=[]
    while queue:
        v,d=queue.popleft()
        if not node(v):continue
        levels[2*v[0]]=d;order.append(2*v[0]);queue.extend(((v[1],d+1),(v[2],d+1)))
    def join(left,right):
        frames=[]
        while node(left) and node(right):
            if rule=='B_minimum_subtree_depth':
                kl,kr=keys(left),keys(right);combined=kl|kr
                assert max(combined)-min(combined)==2*(len(combined)-1)
                nearest=next(k for k in order if k in combined)
                assert len([k for k in combined if levels[k]==levels[nearest]])==1
                choose=nearest in kl
            else:
                dl,dr=levels[left[0]],levels[right[0]]
                choose=dl<dr or dl==dr and rule=='B_root_depth_left_tie'
            if choose:frames.append(('L',left));left=left[2]
            else:frames.append(('R',right));right=right[1]
        result=left if node(left) else right
        for side,v in reversed(frames):result=(v[0],v[1],result) if side=='L' else (v[0],result,v[2])
        return result
    def walk(v):
        if not node(v):return v
        L,R=walk(v[1]),walk(v[2])
        return join(L,R) if v[0]==private else (v[0],L,R)
    return walk(tree)

def main():
    global queries
    native=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,native['trees']));N=len(T);idx={t:i for i,t in enumerate(T)};mir=native['mirror']
    raw=(B/'native10_B_modal_factored_debt.pkl').read_bytes();prior=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['input_sha256']['native10_B_modal_factored_debt.pkl'];O=pickle.loads(raw);del raw
    def D(a,b):return O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    G=json.loads((B/'four_hull_source_basis_independent_audit.json').read_text());assert G['status'].startswith('PASS')
    sp=importlib.util.spec_from_file_location('independent_B_guided_sources65',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=int(sys.argv[2]) or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_RESOURCE_CAP')
        queries+=1
    I.tick=tick;proofs=[];files=[]
    family=json.loads((B/'B_guided_contraction_candidates.json').read_text())
    for name,rules in (('B_guided_root_left_closed_source.json',('B_root_depth_left_tie','B_minimum_subtree_depth')),('B_guided_root_right_closed_source.json',('B_root_depth_right_tie',))):
        files.append(name);z=json.loads((B/name).read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in z['input_sha256'].items())
        e=z['candidate'];source=audit_word(z,native,G['source_kernel'],I,tick)
        for rule in rules:
            sa=idx[renumber(project(fr(e['source_A']),5,T[e['source_B_core_index']],rule))];ta=idx[renumber(project(fr(e['actual_A_target']),5,T[e['B_target_core_index']],rule))]
            candidate=family['failures'][rule];assert (sa,ta)==(candidate['old_source_A_index'],candidate['old_projected_target_index'])
            ds,dt=D(sa,e['source_B_core_index']),D(ta,e['B_target_core_index'])
            assert (e['H'],e['Q'],e['price'],ds,dt)==(1,1,1,2,0)
            assert e['price']+dt-ds==-1
            proofs.append({'rule':rule,'source_word':name,'old_projected_indices':[sa,ta],'debt_values':[ds,dt],'original_packet_H_Q_price':[1,1,1],'signed_margin':-1,'source_verification':source})
    assert len(proofs)==3 and time.process_time()-START<CAP-1
    files+=['B_guided_contraction_candidates.json','audit_verify65.py','closed_word_composition_independent_v2.py','native10_source_independent_audit.json','native10_modal_oracle_independent_audit.json','four_hull_source_basis_independent_audit.json']
    out('B_guided_contraction_independent_audit.json',{'status':'PASS_SOURCE_EXACT_THREE_B_GUIDED_PROJECTION_REFUTATIONS','refuted_rules':proofs,'method':'independent breadth-first B order, iterative zipper join, mutable non-hull accesses; accepted complete source bases for every remaining original operation','not_all_B_sensitive_debts_refuted':True,'not_a_CD_counterexample':True,'frozen_owners_unchanged':True,'principal_U33':'OPEN','source_queries':queries,'source_engine_calls':queries,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}})
    print(json.dumps({'status':'PASS_THREE_SOURCE_EXACT_B_GUIDED_JOIN_REFUTATIONS','source_queries':queries,'rules':3,'principal_U33':'OPEN'}))

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify65_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
