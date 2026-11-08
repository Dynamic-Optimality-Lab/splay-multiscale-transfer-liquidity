"""Audit all three FULL-B/value-set source edges, conserving original query cap."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
from audit_verify37 import fr,delete,renumber
from closed_word_composition_independent import audit_word
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    basis=json.loads((B/'native10_source_actions.json').read_text());N=len(basis['trees']);idx={fr(t):i for i,t in enumerate(basis['trees'])};mir=basis['mirror'];export=json.loads((B/'native10_credit_certificate.json').read_text());L=dict(export['nonzero_debt']);debt=lambda a,b:L.get(min(a*N+b,mir[a]*N+mir[b]),0);G=json.loads((B/'four_hull_source_basis_independent_audit.json').read_text());assert G['status']=='PASS_COMPLETE_G4_PRIMITIVES_AND_ROOTED_HULL_TERM_LIFT'
    sp=importlib.util.spec_from_file_location('independent_B_sensitive_set_source33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_WORD_CAP')
        queries+=1
    I.tick=tick;rows=[];names=[]
    for j in range(3):
        name='B_sensitive_set_edge_'+str(j)+'_closed_source.json';names.append(name);z=json.loads((B/name).read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in z['input_sha256'].items());e=z['candidate'];p=e['private_key'];src=sorted(debt(idx[renumber(a)],e['source_B_core_index']) for a in delete(fr(e['source_A']),p));dst=sorted(debt(idx[renumber(a)],e['B_target_core_index']) for a in delete(fr(e['actual_A_target']),p));proof=audit_word(z,basis,G['source_kernel'],I,tick);proof.update(source_B=e['source_B_core_index'],target_B=e['B_target_core_index'],source_value_set=sorted(set(src)),target_value_set=sorted(set(dst)),source_value_multiset=src,target_value_multiset=dst,price=e['price']);rows.append(proof)
    assert [(r['source_B'],r['target_B']) for r in rows]==[(3277,6496),(6496,8680),(8680,1620)];assert [(r['source_value_set'],r['target_value_set'],r['price']) for r in rows]==[([2],[0,2],0),([0,2],[1,2],0),([1,2],[0],1)];assert 0+0+1+0-2==-1
    assert rows[0]['target_value_multiset']==rows[1]['source_value_multiset'] and rows[1]['target_value_multiset']!=rows[2]['source_value_multiset']
    names+=['native10_credit_certificate.json','native10_source_independent_audit.json','four_hull_source_basis_independent_audit.json','B_sensitive_source_only_obstruction.json','B_sensitive_full_multiset_chain_candidate.json','closed_word_composition_independent.py']
    out('B_sensitive_debt_value_set_independent_audit.json',{'status':'PASS_SOURCE_EXACT_ANY_FULL_B_SENSITIVE_DEBT_VALUE_SET_RULE_REFUTATION','scope':'ANY real F(actual B, SET of old D10 contraction values), nonnegative, F(B,{d})=d; fixed same one-private-gap1 signature','scalar_chain':['F(6496,{0,2})>=2','F(8680,{1,2})>=F(6496,{0,2})','F(8680,{1,2})<=1'],'contradiction':'2<=F(8680,{1,2})<=1','width_or_optional_HIGH_envelopes_used':False,'full_multiset_rules':'NOT REFUTED: intermediate[1,2] differs from[1,1,2] at B8680','actual_source_edges':rows,'source_queries':queries,'source_engine_calls':queries,'verification_method':'fresh mutable A for non-hull accesses plus independently checked complete G4/ten-anchor identities for EVERY remaining original operation; exact common-source composition and physical periods; not all operations reported as new engine replays','no_physical_bits_assigned_or_frozen_owners_changed':True,'not_an_actual_full_A_state_path_or_CD_counterexample':True,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}});print(json.dumps({'status':'PASS_FULL_B_VALUE_SET_FAMILY_REFUTED','fresh_source_queries':queries,'period_CD_margins':[r['CD_margin'] for r in rows],'full_multiset_family':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify46_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
