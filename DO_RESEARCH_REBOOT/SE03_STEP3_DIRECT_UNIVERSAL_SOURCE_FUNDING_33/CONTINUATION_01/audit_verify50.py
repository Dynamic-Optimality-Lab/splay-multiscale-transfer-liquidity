"""Audit all three FULL-B/value-set source edges, conserving original query cap."""
import json,time,sys,hashlib,importlib.util,pickle
from pathlib import Path
from audit_verify37 import fr,delete,renumber
from closed_word_composition_independent import audit_word
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    basis=json.loads((B/'native10_source_actions.json').read_text());N=len(basis['trees']);idx={fr(t):i for i,t in enumerate(basis['trees'])};mir=basis['mirror'];oracle=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes());pin=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256((B/'native10_B_modal_factored_debt.pkl').read_bytes()).hexdigest()==pin['input_sha256']['native10_B_modal_factored_debt.pkl'];debt=lambda a,b:oracle['base'][b]+oracle['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0);G=json.loads((B/'four_hull_source_basis_independent_audit.json').read_text());assert G['status']=='PASS_COMPLETE_G4_PRIMITIVES_AND_ROOTED_HULL_TERM_LIFT'
    sp=importlib.util.spec_from_file_location('independent_B_sensitive_set_source33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_WORD_CAP')
        queries+=1
    I.tick=tick;rows=[];names=[]
    for j in range(3):
        name='B_full_spectrum_edge_'+str(j)+'_closed_source.json';names.append(name);z=json.loads((B/name).read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in z['input_sha256'].items());e=z['candidate'];p=e['private_key'];src=sorted(debt(idx[renumber(a)],e['source_B_core_index']) for a in delete(fr(e['source_A']),p));dst=sorted(debt(idx[renumber(a)],e['B_target_core_index']) for a in delete(fr(e['actual_A_target']),p));proof=audit_word(z,basis,G['source_kernel'],I,tick);proof.update(source_B=e['source_B_core_index'],target_B=e['B_target_core_index'],source_value_set=sorted(set(src)),target_value_set=sorted(set(dst)),source_value_multiset=src,target_value_multiset=dst,price=e['price']);rows.append(proof)
    assert [(r['source_B'],r['target_B']) for r in rows]==[(618,6736),(6736,8777),(8777,1902)]
    assert [(r['source_value_multiset'],r['target_value_multiset'],r['price']) for r in rows]==[([1],[0,1],0),([0,1],[0,1],0),([0,1],[0],0)]
    assert all(rows[i]['target_B']==rows[i+1]['source_B'] and rows[i]['target_value_multiset']==rows[i+1]['source_value_multiset'] for i in (0,1))
    names+=['native10_modal_oracle_independent_audit.json','native10_source_independent_audit.json','four_hull_source_basis_independent_audit.json','B_full_spectrum_result_02.json','closed_word_composition_independent.py']
    out('B_full_spectrum_formula_independent_audit.json',{'status':'PASS_SOURCE_EXACT_FULL_B_AND_FULL_MULTISET_FORMULA_REFUTATION','scope':'ANY real F(actual B, full multiset of D10 over distinct contractions), fixed old debt on singleton contraction, same gap1 private inventory','scalar_chain':['u=F(6736,[0,1])>=1','v=F(8777,[0,1])>=u','v<=0'],'contradiction':'1<=v<=0','width_nonnegativity_or_HIGH_envelopes_used':False,'actual_source_edges':rows,'source_queries':queries,'source_engine_calls':queries,'verification_method':'fresh mutable non-hull A accesses plus previously independently checked complete G4/ten-anchor identities composed through EVERY remaining original operation and exact common-source closure','not_an_actual_full_A_state_path_or_CD_counterexample':True,'no_physical_bits_assigned_or_frozen_owners_changed':True,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}})
    print(json.dumps({'status':'PASS_FULL_B_FULL_MULTISET_FAMILY_REFUTED','fresh_source_queries':queries,'period_CD_margins':[r['CD_margin'] for r in rows]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify50_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
