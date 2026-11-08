"""Bounded PRODUCER derivation of a closed-source concatenation family.
Reuses stored rotations/owners; never an independent replay/audit.
"""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def unpack(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def shift(z,n):return (z[0]+n,*z[1:])
def main():
    old=read('rr7_source_candidate.json');ov=read('overfull_source_result.json')
    case=next(z for z in read('fully_aligned_countercertificates.json')['cases'] if not z['mirrored'])
    paid=next(z for z in read('fully_aligned_source_repairs.json')['cases'] if not z['mirrored'])
    b=case['actual_interval'][0]-1
    hA={shift(d,-b):shift(u,-b) for d,u in unpack(paid['independent_source_comparison']).items()}
    hB=unpack(read('overfull_nonlocal_bundle_repayment.json')['relative_comparison'])
    blocks=[]
    for label,word,rows,h,base in (('A80',old['word'],case['rows'],hA,b),('B82',ov['word'],ov['rows'],hB,0)):
        T=len(word);D={(i,k) for i,t in enumerate(rows,1) for k in range(1,t['qF']+1)}
        U={(i,j,bit) for i,t in enumerate(rows,1) for j in range(1,t['a']+1) for bit in (0,1)}
        assert [(z['mode'],z['target']) for z in rows]==[tuple(z) for z in word]
        assert set(h)==D and set(h.values())<=U and len(set(h.values()))==len(D)==60
        initial=rows[0]['before'][:2];final=rows[-1]['after'][:2]
        assert initial==final
        blocks.append({'label':label,'length':T,'word':word,'initial_A_BF':initial,'final_A_BF':final,
          'physical_comparison':pack(h),'A':sum(t['a'] for t in rows),'QF':sum(t['qF'] for t in rows),
          'costs':[{'occurrence':i,'a':t['a'],'qF':t['qF']} for i,t in enumerate(rows,1)],
          'KEEP_word':[x for mode,x in word if mode=='K'],
          'evidence':'C18 producer source rows/complete comparison; independent audit pending'})
    assert blocks[0]['initial_A_BF']==blocks[1]['initial_A_BF']
    assert blocks[0]['KEEP_word']==blocks[1]['KEEP_word']
    assert case['selected_u']==2 and case['L']==1 and case['erased']==13
    out('closed_block_family.json',{'status':'RESTRICTED_SOURCE_FAMILY_DERIVATION_AUDIT_PENDING',
      'source_support':[1,3,5,7,9,11,13],'source_core':13,
      'reaching_prefix':old['reaching_prefix'],'recurrence_preparation':['A80','A80'],
      'erasure':13,'erased_block_recurrence_u':2,'L':1,
      'common_A_BF_boundary':blocks[0]['initial_A_BF'],'blocks':blocks,
      'arbitrary_word_rule':'Any NONEMPTY finite word in {A80,B82}; offset each complete physical comparison by its actual cumulative operation length',
      'same_KEEP_word_implies_same_erased_block_transition':True,
      'source_engine_calls':0,'universal_LOW_theorem_proved':False})
    # Source-exact failures of candidate SHARED-FIRST-RESET capacities.
    # Source words are assembled from a closed block; no new rotations run.
    for n in (2,3):
        word=ov['word']*n
        ds=[(11+82*i,2) for i in range(n)]
        unit_pair=[(8,1,0),(8,1,1)]
        repaired=[(d,(8+82*i,1,1)) for i,d in enumerate(ds)]
        assert len({u for d,u in repaired})==n
        out('shared_first_reset_'+str(n)+'.json',{
          'status':'RESTRICTED_CANDIDATE_FAILURE_NOT_MAIN_LOW_REFUTATION',
          'source_word':word,'initial_A_BF':blocks[1]['initial_A_BF'],
          'actual_reaching_prefix':old['reaching_prefix']+old['word']*2,
          'absolute_base':len(old['reaching_prefix'])+2*80,
          'relative_demands':ds,'restricted_candidate_inventory':unit_pair,
          'all_pairs_fundable_from_restricted_pair':True,
          'complete_collection_fundable_from_restricted_pair':n<=2,
          'naive_repeated_single_bit_donor':(8,1,1),
          'actual_distinct_source_repair':repaired,'A':116*n,'QF':60*n,
          'closure_reason':'induction over the exact same closed source block; no cross-copy loan',
          'erased_owner_map':'not computed for this new word; accepted I6 source domain supplies a same-interval license if needed',
          'independent_source_replay':False,'source_engine_calls':0})
    out('joint_producer_summary.json',{'status':'PRODUCER_PASS_NOT_AUDIT','blocks':2,
      'block_costs':[(z['label'],z['length'],z['A'],z['QF']) for z in blocks],
      'new_assembled_source_words':2,'new_source_engine_calls':0,
      'complete_family':'arbitrary finite mixed concatenation; entire comparison injected, prior-map exchange by inherited theorem',
      'universal_joint_LOW':'OPEN','same_erased_KEEP_transition':True})
    print(json.dumps({'status':'RESTRICTED_JOINT_SOURCE_FAMILY_PASS','block_costs':[(z['label'],z['A'],z['QF']) for z in blocks],
      'new_assembled_source_words':2,'source_engine_calls':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_joint_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
      'source_engine_calls':0,'new_assembled_source_words':2 if error is None else 0,
      'new_finite_tests':0,'old_semantic_rows_replayed':0})
