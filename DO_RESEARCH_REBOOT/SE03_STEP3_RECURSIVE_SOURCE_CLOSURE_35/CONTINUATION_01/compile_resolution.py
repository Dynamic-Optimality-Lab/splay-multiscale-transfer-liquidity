"""Charged symbolic certificate assembly; no original source primitive."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def leaf(x):return [x,None,None]
def U(x=1):return None if x>13 else [x,None if x==1 else leaf(x-1),U(x+2)]
def main():
    for audit in ('independent_critical_source_audit.json','independent_symbolic_source_audit.json'):
        a=read(F/audit)
        for p,h in a['input_sha256'].items():assert sha(F/p)==h
    base=read(C/'proof_boxes.json');updates={'ROOT35':'REFUTED','PEEL35':'REFUTED','COMP35':'REFUTED','REAL35':'PROVED','MULTI35':'REFUTED'}
    for node in base['boxes']:
        if node['id'] in updates:
            node['prior_status']=node['status'];node['status']=updates[node['id']];node['verification_status']='source construction and independent critical/symbolic audits in CONTINUATION_01';node['resolution_artifact']='CONTINUATION_01/SI34_SOURCE_REFUTATION.md';node['blocker']=None
    base.update(version=2,root_status='REFUTED',blocker_type=None,not_A_or_E=False,not_terminal_A_L=True,terminal_outcome='E-SI34',source_countercut=True,full_architecture_refuted=False,higher_Gate_U='OPEN')
    base['boxes'].append(dict(id='REPAIR35',parent='U35',target='three explicit predecessor/consumer source blocks fund critical deficits with working3',source_scope='this source only; independent comparison; no arbitrary a0-free claim',inherited_results=['original natural h0 and source block semantics'],required_children=[],dual_falsification_objective='a donor collision or invalid actual bit/cost in the stated blocks',reduction_justification='three disjoint original operation inventories',status='PROVED',verification_status='independent symbolic source audit and critical A replay',parent_bridge='shows credits outside PR can legally help this source; not a universal grouping theorem',artifact='CONTINUATION_01/SOURCE_REPAIR_AND_PARENT_STATUS.md',edge_type='restricted-valid-replacement-interface'))
    out('proof_boxes_v2.json',base)
    Fword=[1,3,1,5,1,7,1,9,1,11,1,13];Rword=[1,11,1,9,1,7,1,5,1,3,1]
    initialA=[15,[14,U(),None],None]
    lowStart=[1,None,[14,U(3),None]]
    T=read(F/'new_A_primitive_rows.json')['initial']
    def drop_g(t):
        if t is None:return None
        if t[0]==15:return None
        return [t[0],drop_g(t[1]),drop_g(t[2])]
    source=dict(kind='EXACT_SYMBOLIC_CONSTRUCTIVE_SOURCE',physical_keys=list(range(1,16)),genuine_full_keys=list(range(1,16,2)),erased_key=3,initial_A=initialA,initial_full_B={'kind':'right_vine','keys':[1,15]},desired_A_before_forward=T,gamma_low=dict(definition='shortest lexicographic ordinary-splay word over1..14',input_low_tree=lowStart,output_low_tree=drop_g(T),actual_use='all letters are original DELETEs in15-key tree with rigid leaf15'),gamma_wrap=dict(definition='shortest lexicographic ordinary-splay word over1..15',input_tree_expression='Splay(Rword,Splay(Fword,T))',output_tree=initialA),word=[dict(kind='KEEP',key=15),dict(kind='DELETE',key=1),dict(kind='DELETE_WORD',word='gamma_low'),dict(kind='KEEP_WORD',word=Fword),dict(kind='KEEP_WORD',word=Rword),dict(kind='DELETE_WORD',word='gamma_wrap')],reaching_prefix='DELETE shortest-lex Gamma_1..15(right_vine_1..15, initial_A)',closed_period='first repeated BE/tree and recent-chart boundary state after warmup: actual copies u..u+L-1',source_word_fully_expanded_numerically=False,all_original_costs_retained=True)
    demands=[];pools={};source_slots=[]
    for i,target in ((2,5),(4,9),(6,13)):
        t=f'b+ell+{2+2*i}';cc='b+2';own=[[t,1,b] for b in (0,1)];common=[[cc,1,b] for b in (0,1)]
        demands.extend([[t,k] for k in (1,2,3)]);pools[str(target)]=common+own
        source_slots.append(dict(target=target,absolute_occurrence=t,H=1,Q=3,old_B_marked_ancestors=[1,target-2,15],all_retiring_operations=[cc,t],natural_macro_operations=[t]))
    cert=dict(status='E_SI34_SOURCE_COUNTERCERTIFICATE',source=source,absolute_parameter_definitions=dict(b='actual offset before initial KEEP15 in a selected copy inside the aligned original period',ell='actual length of gamma_low'),selected_macros=source_slots,actual_B_demands=demands,exact_neighborhoods=pools,total_demand=9,distinct_units=8,sigma=3,overlap=4,local_unused=0,deficit=1,connected=True,each_private_capacity=2,all_selected_own_excess=True,no_DELETE_only_return_loop=True,source_CD_margin_lower_bound_per_word=4,physical_owner_maps_modified=False,original_architecture_refuted=False,full_source_numerically_replayed=False,critical_source_replayed_by_distinct_implementations=True,source_proof_artifacts={n:sha(F/n) for n in ('SYMBOLIC_B_CLOSURE.md','SOURCE_CONSTRUCTION.md','EXACT_NEGATIVE_CUT.md','SI34_SOURCE_REFUTATION.md')},audit_receipts={n:sha(F/n) for n in ('independent_critical_source_audit.json','independent_symbolic_source_audit.json')})
    out('SI34_source_countercertificate.json',cert)
    assert len(demands)==9 and not (F/'FULL_PROOF.md').exists()
    print('SI34_SOURCE_REFUTATION_COMPILED_WITH_PRESERVED_HIGHER_GAPS',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof173_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
