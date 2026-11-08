"""PRODUCER source-rule construction on immutable old source records.
No new history, splay replay, independent audit or global graph search.
"""
import importlib.util,json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
C15=B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
C16=B.parent/'SE03_STEP3_NONLOCAL_OWNERSHIP_TRANSFER_16'
spec=importlib.util.spec_from_file_location('C16_adaptive_transfer',C16/'adaptive_transfer.py')
A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def inventories(rows):
    D={(t['occurrence'],k) for t in rows for k in range(1,t['qF']+1)}
    U={(t['occurrence'],j,b) for t in rows for j in range(1,t['a']+1) for b in (0,1)}
    return D,U
def own(rows,macros):
    by={t['occurrence']:t for t in rows};h={}
    for m in macros:
        ds=[(t,k) for t in m['occurrences'] for k in range(1,by[t]['qF']+1)]
        us=[(t,j,b) for t in m['occurrences'] for j in range(1,by[t]['a']+1) for b in (0,1)]
        h.update(zip(ds,us))
    return h
def fixed_paths(D,a,h):
    inv={u:d for d,u in a.items()};records=[]
    for p in sorted(D-set(a)):
        d=p;seen=set();steps=[]
        while d in h:
            assert d not in seen;seen.add(d);u=h[d];owner=inv.get(u)
            steps.append({'demand':d,'unit':u,'owner':owner})
            if owner is None:break
            d=owner
        records.append({'root':p,'steps':steps,'frontier':d if d not in h else None,
            'terminal':steps[-1]['unit'] if steps and steps[-1]['owner'] is None else None})
    return records
def make(name,index,f,owners=None):
    rows=f['rows'];h=unpack(f['leaf_partial_h']);D,U=inventories(rows);by={t['occurrence']:t for t in rows}
    r=f['r'];block=len(f['base_word']);full=dict(h);bands=[]
    for copy in range(f['L']):
        relative_end=5*r+5 if name=='zero_run_source_certificates.json' else 5*r+3
        end=copy*block+relative_end
        m=next(m for m in f['macros'] if m['occurrences'][-1]==end)
        assert m['Q']==1
        us=[(t,j,b) for t in m['occurrences'] for j in range(1,by[t]['a']+1) for b in (0,1)]
        tail=us[2:]
        holes=sorted(tuple(d) for d in f['branch_frontier'] if copy*block<d[0]<=(copy+1)*block)
        assert len(tail)>=len(holes) and not set(tail)&set(h.values())
        pairs=list(zip(holes,tail));full.update(pairs)
        bands.append({'block_copy':copy,'supplier_macro':m['macro'],'supplier_end':end,
            'supplier_occurrences':m['occurrences'],'H':m['H'],'Q':m['Q'],
            'branch_count':len(m['branch']),'z':m['z'],'actual_units':us,
            'protected_tail':tail,'frontiers':holes,'source_ordinal_pairs':pairs})
    assert set(full)==D and len(set(full.values()))==len(full) and set(full.values())<=U
    if owners is None:
        a=unpack(f['owners']['prior']) if f['owners'] else own(rows,f['macros'])
    else:a=unpack(owners['prior'])
    extras={d:u for d,u in full.items() if d not in h}
    def supplier(d,image):
        if d not in extras:return None
        return extras[d],{'kind':'ACTUAL_Q1_PREPARATION_TAIL','source_file':name,
            'report':index,'unit':extras[d],'demand':d,
            'license':'restricted preparation-tail source theorem; not universal source cover'}
    result=A.extend(D,U,a,h,supplier)
    assert not result['blocked'] and set(result['allocation'])==D
    return {'source_file':name,'source_sha256':sha(C15/name),'report':index,
        'r':r,'mirrored':f['mirrored'],'erased':f['erased'] if owners is None else owners['erased'],
        'prior_kind':'actual_certified_f6_partial' if f['owners'] or owners is not None else 'natural_partial_only_no_f7_claim',
        'D_count':len(D),'U_count':len(U),'bands':bands,'comparison':pack(full),
        'old_a':pack(a),'allocation':pack(result['allocation']),'paths':result['paths'],
        'lazy_escapes':result['escapes'],'initial_component_paths':fixed_paths(D,a,h),
        'all_old_values_fixed':True,'new_source_history':False,'status':'PRODUCER_PROOF_DERIVATION_AUDIT_PENDING'}
def main():
    reports=[];templates={}
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        data=read(C15/name);templates[name]=data['reports']
        for i,f in enumerate(data['reports']):reports.append(make(name,i,f))
    own_data=read(C15/'owner_image_source_audit.json')
    template=templates['zero_run_source_certificates.json'][0]
    for f in own_data['reports']:
        assert f['L']==1
        # SAME actual A/full-B record; only the inherited BE/owner map differs.
        reports.append(make('zero_run_source_certificates.json',0,template,owners=f))
    two=next(x for x in reports[8:] if x['erased']==13)
    original=read(C16/'deep_tail_candidate_obstruction.json')
    a=unpack(two['old_a']);h=unpack(template['leaf_partial_h'])
    blocked=[p for p in two['initial_component_paths'] if p['frontier'] is not None]
    assert {tuple(p['root']) for p in blocked}=={(15,3),(15,5)}
    assert {tuple(p['frontier']) for p in blocked}=={(42,2),(41,2)}
    lookup={tuple(p['root']):p for p in two['paths']}
    witness={'status':'PRODUCER_SOURCE_DERIVATION_AUDIT_PENDING','source_path':'C16/deep_tail_candidate_obstruction.json',
        'source_sha256':sha(C16/'deep_tail_candidate_obstruction.json'),
        'old_source':original,'supplier_band':two['bands'][0],
        'old_blocked_components':blocked,
        'preparation_repairs':[lookup[(15,3)],lookup[(15,5)]],
        'complete_comparison':two['comparison'],'allocation':two['allocation'],
        'coupling':'one candidate originating-deep tail shared by two separate blocked paths; no intrinsic source-saturation follows',
        'final_reset_used_for_new_escape':False}
    out('preparation_supply_certificates.json',{'status':'PRODUCER_ONLY_NOT_SEALED',
        'new_source_histories':0,'source_engine_calls':0,'reused_histories':8,'reused_owner_variants':7,'reports':reports})
    out('two_component_preparation_repair.json',witness)
    summary={'status':'PASS_PRODUCER_CONSTRUCTION_ONLY','source_engine_calls':0,
        'reports':[{'source':x['source_file'],'r':x['r'],'mirror':x['mirrored'],'erased':x['erased'],
            'supplier_H_Q':[[b['H'],b['Q']] for b in x['bands']],
            'frontier_pairs':[b['source_ordinal_pairs'] for b in x['bands']],
            'old_unpaid':len(x['paths']),'lazy_escape_count':len(x['lazy_escapes'])} for x in reports],
        'main_U17_ESCAPE':'OPEN_NO_UNIVERSAL_PREPARATION_COVER_PROOF'}
    out('preparation_summary.json',summary)
    print(json.dumps({'status':summary['status'],'reports':len(reports),
        'two_component_paths':witness['preparation_repairs'],
        'source_pairs':two['bands'][0]['source_ordinal_pairs'],'new_source_engine_calls':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_preparation_exit.json',{'whole_process_CPU_seconds':time.process_time(),
        'error':error,'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
