"""Producer completion of actual full/erased recency closure and interval
identities for NEW witnesses. No source replay or independent audit.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def read(n):return json.loads((B/n).read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def update(rec,x):
    if x in rec:rec.remove(x)
    rec.insert(0,x)
def recent(word,erased=None,initial=None):
    r=[] if initial is None else list(initial)
    for mode,x in word:
        if mode=='K' and x!=erased:update(r,x)
    return r
def main():
    sources=read('rr7_owner_certificates.json')['reports']
    marked=read('marked_owner_certificates.json')['reports']
    sources+= [r for r in marked if r['qualifying_marked_first_frontiers']]
    outputs=[]
    for r in sources:
        T=len(r['word']);use=max(r['u'],1);delta=(use-r['u'])*T;base=r['base']+delta
        prefix=r['reaching_prefix']+r['word']*use
        full=recent(prefix);erased=recent(prefix,r['erased'])
        assert len(full)==7 and len(erased)==6
        full_after=recent(r['word']*r['L'],initial=full)
        erased_after=recent(r['word']*r['L'],r['erased'],erased)
        assert full_after==full and erased_after==erased
        transform=lambda x:[x[0]+delta,*x[1:]]
        maps={}
        for name in ('f6','locked_common','prior','leaf_comparison','natural_h0'):
            maps[name]=[{'demand':transform(z['demand']),'unit':transform(z['unit'])} for z in r[name]]
        rows=[dict(t,occurrence=t['occurrence']+delta) for t in r['rows']]
        assert all(base<t['occurrence']<=base+len(rows) for t in rows)
        outputs.append({'erased':r['erased'],'mirrored':r['mirrored'],'original_u':r['u'],'selected_u':use,
            'L':r['L'],'coordinate_shift':delta,'actual_interval':[base+1,base+len(rows)],
            'common_initial':r['common_initial'],'actual_reaching_prefix':prefix,
            'initial_A':r['initial_A'],'initial_BF':r['initial_BF'],'initial_BE':r['initial_BE_at_recurrence'],
            'rows':rows,'maps':maps,'initial_full_recent':full,'final_full_recent':full_after,
            'initial_erased_recent':erased,'final_erased_recent':erased_after,
            'all_existing_map_values_transported_together':True,
            'old_instance_files_unchanged':True,
            'RR7_qualifiers':r['qualifying_RR7_collisions'],
            'marked_qualifiers':r.get('qualifying_marked_first_frontiers',[]),
            'qualifier_ids_use_original_coordinates_add_shift':delta})
    low=[]
    for H in range(1,5):
        for m in range(0,min(4,2*H)+1):
            lo=2*H-m+1;hi=min(6,2*H)
            if lo<=hi:low.append({'H':H,'m':m,'g_min':lo,'g_max':hi,'tail':2*H-m,
                'source_realizability':'NOT_ASSERTED_BY_NUMERICAL_BOUNDS'})
    assert sum(x['g_max']-x['g_min']+1 for x in low)==26
    out('fully_aligned_countercertificates.json',{'status':'PRODUCER_SOURCE_AND_RECENCY_CLOSURE_AUDIT_PENDING','cases':outputs,
        'note':'marked u0 source is explicitly transported to the NEXT actual closed copy to ensure actual full/erased recency lists close; every map endpoint moves together, no cross-copy loan'})
    out('low_creator_capacity_profiles.json',{'status':'EXACT_BOUND_PARTITION_NOT_FINITE_SOURCE_PROOF',
        'r':7,'bound_g':'g<=min(r-1,2H)','bound_m':'m<=min(2H,floor((r+1)/2))',
        'H_at_most':4,'overfull_rows':low,'numerical_triples':26,
        'counter_realizes_one_low_profile':'overfull_source_result.json: H1,m2,g>=1,tail0',
        'higher_r':'use symbolic threshold ceil((r-1+floor((r+1)/2))/2); no all-r finite cutoff asserted'})
    print(json.dumps({'status':'ALIGNED_RECENCY_AND_BOUND_PROFILE_PRODUCER_PASS',
        'cases':[{'erased':r['erased'],'mirror':r['mirrored'],'actual_interval':r['actual_interval'],'shift':r['coordinate_shift']} for r in outputs],
        'low_profile_rows':len(low),'low_numerical_triples':26}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_alignment_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
