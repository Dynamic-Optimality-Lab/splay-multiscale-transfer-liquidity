"""Check the finite symbolic templates used by the returning-word induction.
Saved source rows are reused. No additional source search or replay.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('family_helpers',B/'audit_classify.py')
F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)

def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)

def main():
    data=json.loads((B/'comb_source_fixtures.json').read_text());reports=[]
    a,b=data['reports'];assert a['initial']==b['initial'] and a['reaching_prefix']==b['reaching_prefix']
    assert a['period']==a['body'] and b['period']==b['body']
    assert [z for z in a['body'] if z[0]=='K']==[z for z in b['body'] if z[0]=='K']
    off=b['tags'][0]['helper']-b['actual_interval'][0]-1
    assert b['body'][off]==['D',1] and b['body'][:off]+b['body'][off+1:]==a['body']
    for r in data['reports']:
        rows=[dict(z,before=F.fr(z['before']),after=F.fr(z['after'])) for z in r['rows']]
        mm,al=F.analyze(rows);tag=r['tags'][0];ci=next(i for i,m in enumerate(mm) if tag['comb'] in m['occurrences']);ids=[ci-2,ci-1,ci]
        pp=[ids if i==ids[0] else [i] for i in range(len(mm)) if i not in ids[1:]]
        debt=[(al[g[0]]['before']['L']-1,al[g[-1]]['after']['L']-1) for g in pp];K=max(s for s,t in debt)
        assert K==debt[0][0]==3
        h={d:u for m in mm for d,u in zip(m['demands'],m['units'])};bank=[];receipts=[];working=0
        for k,(g,(ds,dt)) in enumerate(zip(pp,debt)):
            assert len(bank)==K-ds
            units=[u for i in g for u in mm[i]['units'][:2*min(mm[i]['H'],3)]];dd=[d for i in g for d in mm[i]['demands']]
            own={h[d] for d in dd if d in h};missing=[d for d in dd if d not in h];spare=[u for u in units if u not in own]
            rho=len(units)-len(dd)+dt-ds;assert rho>=0
            pool=spare+bank;working=max(working,len(pool)+len(own));added=[]
            for d in missing:u=pool.pop(0);h[d]=u;added.append((d,u))
            assert len(pool)>=K-dt;bank=pool[:K-dt]
            receipts.append({'packet':k,'macros':g,'rho':rho,'D_before':ds,'D_after':dt,'selected_units':units,'new_pairs':added,'carry':bank[:]})
        assert not bank and h==F.mp(r['full_independent_H']) and working<=12
        assert set(h)=={d for m in mm for d in m['demands']} and len(set(h.values()))==len(h)
        assert r['initial']==r['rows'][-1]['after'] and r['a_peak']==5
        triple=[al[i] for i in ids];assert sum(z['rho'] for z in triple)==(3 if r['source_id'].startswith('C29-weak') else 5)
        assert all(z['H']>=4 for i,z in enumerate(al) if i not in ids)
        prefix=F.mp(r['effective_prefix']);final=F.mp(r['final_full_a']);assert len(prefix)==33 and len(final)==34 and all(final[d]==u for d,u in prefix.items())
        assert len(r['paths'])==1 and len(r['paths'][0]['steps'])==2 and tuple(r['paths'][0]['terminal'])==mm[ids[0]]['units'][1]
        assert all(r['actual_interval'][0]<=u[0]<=r['actual_interval'][1] for u in final.values())
        reports.append({'source_id':r['source_id'],'triple_macro_indices':ids,'triple_rho':sum(z['rho'] for z in triple),'receipts':receipts,
                        'leaf_maximum_at_boundary':K,'working_peak':working,'full_a_peak':F.profile(final),'comparison_peak':F.profile(h),
                        'A':r['A'],'QF':r['QF'],'QE':r['QE'],'operations':len(r['period']),'full_comparison_H':F.pack(h)})
    assert [(z['operations'],z['A'],z['QF'],z['QE']) for z in reports]==[(128,158,34,30),(129,159,34,30)]
    out('mixed_family_templates.json',{'status':'EXACT_TEMPLATES_FOR_RETURNING_WORD_INDUCTION','reports':reports,
        'arbitrary_multiplicity_proof':'MIXED_COMB_FAMILY_THEOREM.md; identical whole-tree boundary, empty boundary bank and local owner templates',
        'raw_canonical_receipt_only':True,'older_fixed_five_key_receipt_supplied':False,'principal_MC29_closed':False})
    print(json.dumps({'status':'FAMILY_TEMPLATES_PASS','source_queries':0,'reports':[{k:z[k] for k in ('source_id','triple_rho','working_peak','full_a_peak')} for z in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_family_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
