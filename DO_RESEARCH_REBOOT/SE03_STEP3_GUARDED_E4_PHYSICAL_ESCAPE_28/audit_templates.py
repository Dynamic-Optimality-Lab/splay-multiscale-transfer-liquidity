"""Exact local templates for an arbitrary-multiplicity source theorem.
No source simulation: use the checked complete four-copy receipt to
identify the base/induction boundary maps, then prove replication in prose.
"""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def rel(m,start,end):
    sub={d:u for d,u in m.items() if start<=d[0]<=end}
    assert all(start<=u[0]<=end for u in sub.values())
    return {(d[0]-start+1,*d[1:]):(u[0]-start+1,*u[1:]) for d,u in sub.items()}
def main():
    c=json.loads((B/'catchment_forcing_countercertificate.json').read_text());old=json.loads((OLD/'aligned_source_and_owners.json').read_text())
    assert len(c['period'])==459;V=c['period'][:65];state=c['initial']
    for i in range(4):
        assert c['period'][65*i:65*(i+1)]==V
        assert c['rows'][65*i]['before']==state and c['rows'][65*(i+1)-1]['after']==state
    assert c['period'][260:]==old['period'] and c['rows'][260]['before']==state and c['rows'][-1]['after']==state
    maps={'f6':mp(c['f6']),'natural':mp(c['policy_stages'][0]['prior'])}
    for z in c['policy_stages']:
        maps[z['name']+'_comparison']=mp(z['comparison']);maps[z['name']+'_effective']=mp(z['after'])
    base={name:rel(m,573,637) for name,m in maps.items()};assert len(base['leaf_effective'])==14
    for name,m in maps.items():
        for i in range(4):assert rel(m,573+65*i,637+65*i)==base[name]
    oldpartial=mp(old['policy_stages'][-1]['after']);newpartial=mp(c['prior_before_extra'])
    assert rel(newpartial,833,1031)=={(d[0]-572,*d[1:]):(u[0]-572,*u[1:]) for d,u in oldpartial.items()}
    assert len(newpartial)==14*4+57
    assert c['extra_payments']==[{'demand':[921,3],'unit':[577,1,0]}]
    assert (5,1,0) not in set(base['leaf_effective'].values())
    assert all(z['birth'][0]>=833 and z['origin'][0]>=833 for z in c['selected_transports'])
    assert all(z['demand'][0]>=833 and z['unit'][0]>=833 for z in c['creator_pairs'])
    rows=c['rows'];table=[]
    for r in rows[:65]:
        if r['mode']=='K':table.append({'local_occurrence':r['occurrence']-572,'target':r['target'],'a':r['a'],'qF':r['qF'],'qE':r['qE']})
    out('uniform_insertion_templates.json',{'status':'EXACT_BASE_AND_INDUCTION_TEMPLATES_NOT_FINITE_M_EXTRAPOLATION',
        'source_word_V':V,'triple_boundary':state,'V_length':65,'V_A':sum(r['a'] for r in rows[:65]),
        'V_QF':sum(r['qF'] for r in rows[:65]),'V_QE':sum(r['qE'] for r in rows[:65]),'V_KEEP_table':table,
        'V_local_policy_templates':{name:pack(m) for name,m in base.items()},
        'V_complete_frozen_local_map':pack(base['leaf_effective']),'V_first_macro_ninth_unit_local':[5,1,0],
        'W_original_partial_template_57':old['policy_stages'][-1]['after'],
        'uniform_late_payment':{'demand_formula':'(661+65*m,3)','unit':[577,1,0],'m_domain':'integer m>=1'},
        'uniform_counts':{'operations':'199+65*m','A':'261+67*m','QF':'58+14*m','QE':'27+6*m',
            'outside_native_deficits':'m+1','deep_Q6_count':1,'effective_complete_demands':'58+14*m'},
        'induction_interfaces':['V exact whole A/BF/BE return at the same boundary',
            'six-key debt at boundary is maximum2, hence canonical bank empty',
            'V B-leaf changes only1/3/5, each leaf at its boundary: no leaf channel crosses V boundary',
            'V has no branch frontier, hence creates no new protected-creator/T19 selection',
            'common/natural and later owner paths stay inside the block-diagonal source/comparison components',
            'single actual first-V bit carried until sole W root; no other cyclic-copy bit borrowed'],
        'private_population_lift':'arbitrary ordered BST substitution at the14 external gaps of the fixed13-anchor source; no arbitrary anonymous A-ancestor lifting claimed',
        'not_complete_U28':True,'same_agent_external_audit':False})
    print(json.dumps({'status':'UNIFORM_TEMPLATE_IDENTITIES_PASS','V_A':sum(r['a'] for r in rows[:65]),
        'V_QF':sum(r['qF'] for r in rows[:65]),'all_block_maps_local_and_repeat':True,'one_future_W_root':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_templates_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
