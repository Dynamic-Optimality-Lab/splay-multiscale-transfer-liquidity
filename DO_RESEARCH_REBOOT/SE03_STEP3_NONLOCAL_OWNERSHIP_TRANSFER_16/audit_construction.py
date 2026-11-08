"""Bounded PRODUCER construction on already source-audited C15 records.
This is not an independent audit and does not replay a single splay.
"""
import hashlib, json, time
from pathlib import Path
from adaptive_transfer import extend
B = Path(__file__).resolve().parent
OLD = B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f: json.dump(x,f,indent=2)
def unpack(xs): return {tuple(x['demand']):tuple(x['unit']) for x in xs}
def pack(m): return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def inventory(rows):
    D={(t['occurrence'],k) for t in rows for k in range(1,t['qF']+1)}
    U={(t['occurrence'],j,b) for t in rows for j in range(1,t['a']+1) for b in (0,1)}
    return D,U
def own_map(rows, macros):
    by_t={t['occurrence']:t for t in rows};h0={}
    for m in macros:
        us=[(t,j,b) for t in m['occurrences'] for j in range(1,by_t[t]['a']+1) for b in (0,1)]
        ds=[(t,k) for t in m['occurrences'] for k in range(1,by_t[t]['qF']+1)]
        h0.update(zip(ds,us))
    return h0
def construct(label, source_file, index, rows, macros, h, full, a):
    D,U=inventory(rows)
    assert set(full)==D and len(set(full.values()))==len(full)
    assert set(full.values())<=U and all(full[d]==u for d,u in h.items())
    initial_image=set(h.values())
    recipe={d:u for d,u in full.items() if d not in h}
    assert len(set(recipe.values()))==len(recipe) and not set(recipe.values())&initial_image
    per_macro=[]
    support={t['target'] for t in rows if t['genuine_F']}
    by_t={t['occurrence']:t for t in rows}
    zero_holes=[]
    for m in macros:
        us=[(t,j,b) for t in m['occurrences'] for j in range(1,by_t[t]['a']+1) for b in (0,1)]
        beta,z,H,Q=len(m['branch']),m['z'],m['H'],m['Q']
        expected=min(2*H,beta+z)
        actual=initial_image&set(us)
        assert actual==set(us[:expected])
        if 2*H-Q==0:
            hole=max(beta+z-2*H,0)
            assert hole==int(z==1 and len(m['unary'])==0)
            if hole:
                assert 4*H+1<=len(support)
                zero_holes.append({'macro':m['macro'],'H':H,'Q':Q,'beta':beta,'z':z,
                    'target':m['target'],'required_distinct_marks':4*H+1})
        per_macro.append({'macro':m['macro'],'physical_units':len(us),'comparison_prefix':expected})
    def supplier(d,image):
        if d not in recipe: return None
        u=recipe[d]
        assert u not in image
        return u, {'kind':'INHERITED_EXPLICIT_FAMILY_RESET_PAIR',
            'source_file':source_file,'report':index,'demand':d,'unit':u,
            'scope':'only this source family; not a universal reset theorem'}
    result=extend(D,U,a,h,supplier)
    assert not result['blocked'] and set(result['allocation'])==D
    return {'label':label,'source_file':source_file,'source_sha256':sha(OLD/source_file),
        'report':index,'D_count':len(D),'U_count':len(U),'initial_unpaid':len(D-set(a)),
        'initial_holes':len(D-set(h)),'initial_old_a':pack(a),
        'complete_allocation':pack(result['allocation']), 'paths':result['paths'],
        'lazy_escapes':result['escapes'],'visited_distinct_demands':result['visited_distinct_demands'],
        'comparison_image_prefix_rows':per_macro,'raw_zero_holes':zero_holes,
        'all_old_values_fixed':True,'status':'PRODUCER_CONSTRUCTED_INDEPENDENT_AUDIT_PENDING'}
def main():
    reports=[];families={}
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        source=read(OLD/name);families[name]=source
        for i,f in enumerate(source['reports']):
            h=unpack(f['leaf_partial_h']);full=unpack(f['family_full_h'])
            a=unpack(f['owners']['prior']) if f['owners'] else own_map(f['rows'],f['macros'])
            reports.append(construct(name+':'+str(i),name,i,f['rows'],f['macros'],h,full,a))
    image=read(OLD/'owner_image_source_audit.json')
    template=families['zero_run_source_certificates.json']['reports'][0]
    full=unpack(template['family_full_h']);candidate=None
    for i,f in enumerate(image['reports']):
        assert f['L']==1 and len(f['rows'])==len(template['rows'])
        h=unpack(f['leaf_comparison_h']);a=unpack(f['prior'])
        reports.append(construct('actual_erasure_'+str(f['erased']),'owner_image_source_audit.json',i,
            f['rows'],template['macros'],h,full,a))
        if f['erased']==13:
            blocks=[{'root':x['demand'],'frontier':x['unit']} for x in f['partial_forward_blocks']]
            assert len(blocks)==2
            deep=template['deep_packets'];assert len(deep)==1
            m=template['macros'][deep[0]['macro_indices'][0]]
            us=[(t['occurrence'],j,b) for t in f['rows'] if t['occurrence'] in m['occurrences'] for j in range(1,t['a']+1) for b in (0,1)]
            spare=sorted(set(us)-set(h.values()))
            assert m['H']==1 and len(spare)==1
            candidate={'status':'PRODUCER_DERIVED_RESTRICTED_CANDIDATE_OBSTRUCTION_AUDIT_PENDING',
                'source_file':'owner_image_source_audit.json','source_sha256':sha(OLD/'owner_image_source_audit.json'),
                'report':i,'erased':13,'source_word':image['source_word'],'initial_A_BF':image['initial_A_BF'],
                'initial_BE':f['rows'][0]['before'][2], 'rows':f['rows'],
                'f6':f['f6'],'old_a':f['prior'],'leaf_h':f['leaf_comparison_h'],
                'blocked_components':blocks,'allowed_deep_only_tail':spare,
                'minimum_fresh_image_edges_for_all_initial_blocked_components':2,
                'candidate_free_image_count':f['candidate_free_image_count'],
                'scope':'monotone extension of h at undefined frontiers using ONLY the originating deep macro tail; not all rematching or U16'}
    assert candidate is not None
    out('adaptive_family_certificates.json',{'status':'PRODUCER_ONLY_NOT_INDEPENDENTLY_AUDITED',
        'source_engine_calls':0,'old_source_histories_reused':8,'old_actual_owner_variants_reused':7,
        'new_source_histories':0,'reports':reports})
    out('deep_tail_candidate_obstruction.json',candidate)
    out('construction_summary.json',{'status':'PASS_PRODUCER_CONSTRUCTION_ONLY','reports':len(reports),
        'total_lazy_escape_edges':sum(len(x['lazy_escapes']) for x in reports),
        'summary':[{'label':x['label'],'unpaid':x['initial_unpaid'],'holes':x['initial_holes'],
            'escapes':len(x['lazy_escapes']),'max_path':max([len(p['steps']) for p in x['paths']],default=0)} for x in reports],
        'new_universal_source_existence_theorem':False,'independent_audit':'PENDING_SEPARATE_CAP'})
    print(json.dumps({'status':'PRODUCER_ONLY','records':len(reports),'source_engine_calls':0,
        'one_deep_tail_candidate':candidate['blocked_components'],'available_tail':candidate['allowed_deep_only_tail']}),flush=True)
if __name__=='__main__':
    error=None
    try: main()
    except BaseException as ex: error={'type':type(ex).__name__,'message':str(ex)};raise
    finally: out('audit_construction_exit.json',{'whole_process_CPU_seconds':time.process_time(),
        'error':error,'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
