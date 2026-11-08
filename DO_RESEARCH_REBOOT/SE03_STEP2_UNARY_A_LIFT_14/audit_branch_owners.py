"""New physical algorithm audit on PINNED already-replayed source periods.
No old tree/cost checks are rerun. Independent set accounting checks every
new receipt, natural owner, absolute unit and complete licensed exchange.
"""
import hashlib,json,time
from pathlib import Path
from branch_funding import build,with_owners,freeze
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def check(rows,v):
    actualU={(r['occurrence'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
    actualD={(r['occurrence'],j) for r in rows for j in range(1,r['qF']+1)}
    assert v['U']==actualU and v['D']==actualD
    assert set(v['h'])==actualD and len(set(v['h'].values()))==len(actualD) and set(v['h'].values())<=actualU
    assert all(v['h'][d]==u for d,u in v['h0'].items())
    seen=[];assigned=set(v['h0'].values());carry=set();peak=0
    for pp in v['packet_receipt']:
        seen+=pp['occurrences'];before=v['max_debt_on_period']-pp['D_before'];after=v['max_debt_on_period']-pp['D_after']
        assert len(carry)==before and pp['w']+pp['D_after']-pp['D_before']>=0
        spare=set(map(tuple,pp['selected_spares']));assert not spare&assigned and not spare&carry
        assert all(u[0] in pp['occurrences'] for u in spare)
        pool=carry|spare;new=set()
        for d,u in pp['new_pairs']:
            assert tuple(u) in pool-new;assert tuple(d) not in v['h0'];new.add(tuple(u));assert v['h'][tuple(d)]==tuple(u)
        carry=set(map(tuple,pp['carry']));assert len(carry)==after and carry<=pool-new
        assert not carry&assigned;assigned|=new
        assert len(spare)+len(pp['fixed_own_units'])==2*min(pp['H'],4)
        peak=max(peak,before+2*min(pp['H'],4));assert peak<=11
    assert not carry and sorted(seen)==sorted(r['occurrence'] for r in rows)
    E={(r['occurrence'],j) for r in rows for j in range(1,r['qE']+1)};units=sorted(actualU);fixtures=[]
    for shift in (0,1,3):
        fE=dict(zip(sorted(E),units[shift:]+units[:shift]));o=with_owners(v,E,fE)
        assert all(o['extension']['allocation'][d]==u for d,u in o['prior']['allocation'].items())
        assert all(o['extension']['allocation'][d]==fE[d] for d in actualD&E)
        fixtures.append({'logical_fixture_only':True,'shift':shift,'old_paid_values':len(o['prior']['allocation']),
            'new_residuals':len(o['extension']['additions']),'paths':o['extension']['paths'],'all_old_values_fixed':True})
    n=len(rows)
    for delta in range(n):
        tau=lambda t:t if t>delta else t+n
        donors={(tau(u[0]),u[1],u[2]) for u in v['h'].values()};demands={(tau(d[0]),d[1]) for d in v['h']}
        assert len(donors)==len(demands)==len(actualD) and all(delta<t<=delta+n for t,j,b in donors)
    return fixtures
def main():
    assert json.loads((B/'branch_all_independent_audit.json').read_text())['status'].startswith('PASS_ALL_38')
    sources=json.loads((OLD/'slot_count_witnesses.json').read_text());reports=[]
    for source in sources['reports']:
        # All six erasures were ALREADY source-replayed and pinned. The full
        # A/BF algorithm is erasure-independent; reuse it, audit each fE interface.
        for e in source['erased_runs']:
            if e['L']!=1:continue
            rows=e['rows'];v=build(rows);fixtures=check(rows,v)
            reports.append({'core':source['core'],'reflected':source['reflected'],'erased':e['erased'],
                'old_source_replay_reused':True,'rows':len(rows),'natural_excess_slots':len(v['R']),
                'all_old_natural_values_fixed':True,'working_units':v['working_units'],'h':pack(v['h']),
                'packet_receipt':v['packet_receipt'],'owner_fixtures':fixtures,'legal_cut_transports':len(rows)})
    unary=json.loads((B/'unary_source_receipt.json').read_text());v=build(unary['rows']);check(unary['rows'],v)
    out('branch_physical_owner_audit.json',{'status':'PASS_ACTUAL_PHYSICAL_FUNDING_AND_FROZEN_OWNER_INTERFACE','reports':reports,
        'reused_old_closed_periods':len(reports),'nonvacuous_anonymous_source_reused':True,'unary_full_rule_h':pack(v['h']),
        'all_existing_allocations_preserved':True,'working_bound':11,'Bank25':25,
        'numeric_fE_status':'only logical owner fixtures exercised; theorem is parametric for every supplied original certified fE',
        'source_engine_calls':0,'old_semantic_rows_replayed':0})
    print(json.dumps({'status':'PASS_ALL_NEW_OWNER_RECEIPTS','old_periods_reused':len(reports),'nonvacuous_unary':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_branch_owners_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'old_semantic_rows_replayed':0})
