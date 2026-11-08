"""Producer derivation of collective zero-hole/leaf-birth transposition.
Uses existing source rows; no source replay and no independent audit.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def main():
    s=importlib.util.spec_from_file_location('C19_reused_channels',P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py')
    L=importlib.util.module_from_spec(s);s.loader.exec_module(L)
    old=P/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
    family=read(B/'closed_block_family.json');reports=[]
    for label,rows in (('A80',read(old/'rr7_source_candidate.json')['rows']),('B82',read(old/'overfull_source_result.json')['rows'])):
        M={z['target'] for z in rows if z['genuine_F']};v=L.build(rows,M)
        zero=[m for m in v['macros'] if (m['H'],m['Q'],len(m['branch']),m['z'])==(1,2,2,1)]
        alt=dict(v['h']);pairs=[];transported=set()
        for m in zero:
            assert len(m['branch_unpaid'])==1
            d=tuple(m['branch_unpaid'][0]);rho=tuple(m['reserve'])
            c=next(c for c in v['channels'] if tuple(c['unit'])==rho)
            birth=tuple(c['demand']);assert birth in alt and alt[birth]==rho and d not in alt
            del alt[birth];alt[d]=rho;transported.add(birth)
            pairs.append({'zero_macro':m['macro'],'zero_frontier':d,'marked_key':m['target'],
              'reserved_unit':rho,'unary_birth_demand':birth,'birth_macro':c['birth_macro'],
              'wraps_given_seam':c['wraps_given_seam']})
        assert len(transported)==len(zero) and set(alt.values())==set(v['h'].values())
        assert len(set(alt.values()))==len(alt)
        grouped=[]
        for m in v['macros']:
            demands=sorted(d for d in transported if d[0] in m['occurrences'])
            if not demands:continue
            units={(t,j,b) for t in m['occurrences'] for j in range(1,rows[t-1]['a']+1) for b in (0,1)}
            tail=sorted(units-set(alt.values()))
            grouped.append({'birth_macro':m['macro'],'H':m['H'],'Q':m['Q'],
              'transported_demands':demands,'available_own_tail':tail,
              'local_tail_shortfall':max(0,len(demands)-len(tail))})
        full={tuple(z['demand']):tuple(z['unit']) for z in next(z for z in family['blocks'] if z['label']==label)['physical_comparison']}
        complete=dict(full)
        for z in pairs:
            d=tuple(z['zero_frontier']);birth=tuple(z['unary_birth_demand']);rho=tuple(z['reserved_unit'])
            assert full[birth]==rho
            complete[d]=rho;complete[birth]=full[d]
        assert set(complete)==v['D'] and len(set(complete.values()))==len(complete)
        reports.append({'source':label,'transpositions':pairs,'alternative_partial_comparison':pack(alt),
          'remaining_holes':sorted(v['D']-set(alt)),'transported_birth_groups':grouped,
          'complete_alternative_comparison':pack(complete),
          'comparison_image_unchanged':True,'old_effective_owners_touched':False,
          'local_birth_tail_rule_refuted_on_this_source':any(z['local_tail_shortfall'] for z in grouped)})
    out('zero_leaf_transposition.json',{'status':'SOURCE_DERIVATION_AUDIT_PENDING','reports':reports,
      'universal_statement':'Every deduplicated H1 zero-hole set injects into distinct actual same-key unary leaf-birth demands; comparison recoloring preserves its entire physical image',
      'not_new_usable_credit':True,'source_engine_calls':0})
    print(json.dumps({'status':'ZERO_LEAF_COLLECTIVE_TRANSPOSITION_PASS',
      'profiles':[{'source':z['source'],'zero_count':len(z['transpositions']),
       'local_tail_shortfalls':[g['local_tail_shortfall'] for g in z['transported_birth_groups']]} for z in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_transport_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
      'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
