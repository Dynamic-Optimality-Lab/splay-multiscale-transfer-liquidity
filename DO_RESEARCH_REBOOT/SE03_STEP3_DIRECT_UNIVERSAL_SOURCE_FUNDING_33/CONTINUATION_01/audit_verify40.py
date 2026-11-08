"""Independent actual-source replay and three-edge nonlinear formula refutation."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
from audit_verify37 import delete,renumber,fr,node
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    basis=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,basis['trees']));idx={t:i for i,t in enumerate(T)};N=len(T);mir=basis['mirror'];export=json.loads((B/'native10_credit_certificate.json').read_text());level=dict(export['nonzero_debt']);debt=lambda a,b:level.get(min(a*N+b,mir[a]*N+mir[b]),0)
    sp=importlib.util.spec_from_file_location('independent_debt_set_closed_edges33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_SOURCE_CAP')
        queries+=1
    I.tick=tick;records=[]
    def update(c,k):return (k,)+tuple(v for v in c if v!=k)
    for name in ('root_aware_contraction_first_closed_source.json','root_aware_contraction_second_closed_source.json'):
        z=json.loads((B/name).read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in z['input_sha256'].items());e=z['candidate'];private=e['private_key'];ps=sorted({idx[renumber(v)] for v in delete(fr(e['source_A']),private)});pt=sorted({idx[renumber(v)] for v in delete(fr(e['actual_A_target']),private)});src=sorted({debt(a,e['source_B_core_index']) for a in ps});dst=sorted({debt(a,e['B_target_core_index']) for a in pt});sm=sum(1<<v for v in src);tm=sum(1<<v for v in dst);assert (sm,tm)==(e['source_value_mask'],e['target_value_mask']);sm+=16*(e['source_A'][0]//2-1);tm+=16*(e['actual_A_target'][0]//2-1);srcall=sorted(debt(a,e['source_B_core_index']) for a in ps);dstall=sorted(debt(a,e['B_target_core_index']) for a in pt)
        initial=fr(z['initial_common_A_B_BE']);keys=sorted([2,private]+list(range(4,21,2)));ranks={v:i+1 for i,v in enumerate(keys)}
        def shape(tree):
            def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,ranks[v.key]-1),walk(v.right,hi))
            return walk(tree.root,11)
        A,F,E=I.Tree(initial),I.Tree(initial),I.Tree(initial);word=z['word'];n=len(word);cf=();ce=();period={r['absolute_t']:r for r in z['period_rows']};begin=end=None;AA=QQ=EE=0;packet=False;genuine=set()
        for copy in range(z['source_prefix_copies']+z['period_copies']):
            for j,(mode,key) in enumerate(word):
                row=z['A_word_source_rows'][j];assert shape(A)==fr(row['before']);pa,ea=A.access(key);assert len(ea)==(len(pa)+1)//2==row['H'] and shape(A)==fr(row['after']);f0,e0=shape(F),shape(E);cf0,ce0=cf,ce;q=qe=0;absolute=copy*n+j+1
                if absolute==z['period'][0]:begin=(fr(row['before']),f0,e0,cf0,ce0)
                if mode=='K':
                    k=key//2;fr0=F.root.key;pf,ef=F.access(key);q=len(pf)//2
                    if fr0!=key:cf=update(cf,k)
                    if k!=10:
                        er0=E.root.key;pe,ee=E.access(key);qe=len(pe)//2
                        if er0!=key:ce=update(ce,k)
                if absolute in period:
                    r=period[absolute];assert (r['word_index'],r['kind'],r['key'],r['H'],r['QF'],r['QE'])==(j,mode,key,len(ea),q,qe);assert (tuple(r['chartF_before']),tuple(r['chartF_after']),tuple(r['chartE_before']),tuple(r['chartE_after']))==(cf0,cf,ce0,ce);assert renumber(delete(f0,private)[0])==T[r['BF_before']] and renumber(delete(shape(F),private)[0])==T[r['BF_after']];assert renumber(delete(e0,private)[0])==T[r['BE_before']] and renumber(delete(shape(E),private)[0])==T[r['BE_after']];AA+=len(ea);QQ+=q;EE+=qe
                    if mode=='K' and f0[0]!=key:genuine.add(key)
                if absolute==z['packet_absolute_t']:
                    assert (key,len(ea),q)==(e['target_actual_key'],e['H'],e['Q']);packet=True
                if absolute==z['period'][1]:end=(shape(A),shape(F),shape(E),cf,ce)
            assert shape(A)==shape(F)==initial
        assert packet and begin==end and len(genuine)==10 and (AA,QQ,EE)==(z['A_period'],z['QF_period'],z['QE_period'])
        records.append({'witness_file':name,'source_value_set':src,'target_value_set':dst,'source_value_multiset':srcall,'target_value_multiset':dstall,'source_mask':sm,'target_mask':tm,'price':e['price'],'private_key':private,'physical_keys':keys,'period':z['period'],'packet_t':z['packet_absolute_t'],'costs':[AA,QQ,EE],'CD_margin':2*AA-QQ,'all_source_closures_verified':True,'genuine_KEEP_keys':sorted(genuine)})
    oldreceipt=json.loads((B/'interior_max_contraction_independent_audit.json').read_text());oldsource=json.loads((B/'interior_max_contraction_closed_source.json').read_text());assert oldreceipt['status']=='PASS_SOURCE_EXACT_MAX_CONTRACTION_POTENTIAL_REFUTATION' and oldreceipt['input_sha256']['interior_max_contraction_closed_source.json']==hashlib.sha256((B/'interior_max_contraction_closed_source.json').read_bytes()).hexdigest();c=oldsource['candidate'];assert set(c['all_source_projection_debts'])=={0,2} and set(c['all_target_projection_debts'])=={0} and c['price']==1 and c['private_key']==3
    assert [(r['source_mask'],r['target_mask'],r['price']) for r in records]==[(4,58,-1),(58,37,1)];assert all(r['private_key']==3 and r['physical_keys']==records[0]['physical_keys'] for r in records)
    # Exact elimination. No upper bound or monotonicity on either unknown is used.
    # -1+u-2>=0; +1+v-u>=0; +1+0-v>=0.
    assert (-1)+1+1+0-2==-1
    deps=('root_aware_contraction_first_closed_source.json','root_aware_contraction_second_closed_source.json','interior_max_contraction_closed_source.json','interior_max_contraction_independent_audit.json','native10_credit_certificate.json','root_aware_contraction_debt_set_candidate.json')
    result={'status':'PASS_ANY_ROOT_AWARE_SINGLETON_COMPATIBLE_CONTRACTION_DEBT_SET_FORMULA_REFUTATION','exact_scalar_obstruction':['F(root4,{1,3})>=3','F(root3,{0,2})>=F(root4,{1,3})-1>=2','F(root3,{0,2})<=1'],'contradiction':'2<=F(root3,{0,2})<=1','sum_of_three_signed_margins':-1,'width_bound_used_in_extracted_proof':False,'all_real_nonlinear_functions_of_value_set_refuted':True,'singleton_compatibility_required':{'F({2})':2,'F({0})':0},'same_fixed_private_inventory_signature':{'ten_genuine_anchors':[2,4,6,8,10,12,14,16,18,20],'one_A_only_private_key':3,'B_private_gap':'between first and second genuine anchors'},'root_aware_same_private_signature':True,'multiset_intermediate_profiles_also_match':records[0]['target_value_multiset']==records[1]['source_value_multiset'] and records[1]['target_value_multiset']==sorted(c['all_source_projection_debts']),'full_B_shape_or_full_chart_dependent_functions':'not refuted unless they also identify these source profiles','actual_source_edges':records,'accepted_third_control_reused_without_replay':oldreceipt['input_sha256'],'not_one_actual_source_path_or_negative_cycle':True,'no_Coarse_Double_counterexample':True,'source_queries':queries,'source_engine_calls':queries,'principal_U33':'OPEN','external_or_formal_proof_assistant_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}}
    out('root_aware_contraction_debt_set_independent_audit.json',result);print(json.dumps({'status':result['status'],'source_queries':queries,'scalar_contradiction':result['contradiction'],'new_source_periods':[r['period'] for r in records],'CD_margins':[r['CD_margin'] for r in records],'width_bound_used':False}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify40_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
