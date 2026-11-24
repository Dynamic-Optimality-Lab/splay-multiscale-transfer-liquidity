from base7 import *
from catalog7 import complete_controls,known_inputs,accounting
from workload7 import merged_replay

if __name__=='__main__':
    unsealed();m=Meter('two_sided_merge_falsification')
    refs={z['source']['name']:z for z in complete_controls()};known={e['source']['name']:accounting(e) for e in known_inputs()}
    original=load(C6/'ONE_SIDED_SHADOW_RESULTS.json');out=[];first=None;allbad=[]
    for z in original:
        e=refs[z['source']];assert digest(e['source'])==z['source_sha256'];p=load(e['physical']);ds={tuple(d['parent']):d for d in p['doubles']};rows=p['boundaries'];N=len(rows);tests=[]
        acc=known.get(z['source']);eligible={tuple(t['original_parent']) for t in acc['C_old']} if acc is not None else None
        for old in z.get('tested_stored_PF_intervals',z.get('tested_canonical_original_C_old_intervals',[])):
            u,v=tuple(old['earlier']),tuple(old['later']);g=old['old_g']
            hits=old['left_original_inside_hits']+old['right_original_inside_hits'];hits.sort(key=lambda hx:(hx[0]-u[0]-1)%N)
            test=merged_replay(p,rows,ds,u,v,g,hits)
            result={'earlier':u,'later':v,'old_g':g,'left_hits':old['left_original_inside_hits'],'right_hits':old['right_original_inside_hits'],
                'earlier_original_C_old':None if eligible is None else u in eligible,'later_original_C_old':None if eligible is None else v in eligible,
                'full_component_merge_failed':bool(test['full_g_component_failure']),'old_g_coverage_failed':not test['all_original_old_g_matched'],
                'merged_inside_shadow':test}
            tests.append(result)
            if result['full_component_merge_failed']:
                allbad.append({'source':z['source'],'earlier':u,'later':v,'old_g':g,'both_C_old':None if eligible is None else u in eligible and v in eligible})
                if first is None:first={'source':e['source'],'source_sha256':digest(e['source']),'physical':e['physical'],'physical_sha256':hfile(e['physical']),
                    'failed_candidate':'Broader physical no-promotion/reset-free MERGE0 full-component lemma. Canonical C_old scope is reported separately.','test':result}
        out.append({'source':z['source'],'source_sha256':digest(e['source']),'tests':tests})
        write('MERGE_PROBE_RESULTS.json',out);gc.collect()
    write('MERGE_PROBE_SUMMARY.json',{'sources':len(out),'intervals':sum(len(z['tests']) for z in out),'component_failures':allbad,
        'old_g_coverage_failures':sum(t['old_g_coverage_failed'] for z in out for t in z['tests']),
        'full_C_old_candidate_refuted':any(z['both_C_old'] is True for z in allbad)})
    if first is not None:write('FIRST_PHYSICAL_MERGE_OBSTRUCTION.json',first)
    m.info.update(sources=len(out),component_failures=len(allbad));m.ok=True
    print('PASS exact merge falsification sweep;',len(allbad),'component failures;',sum(t['old_g_coverage_failed'] for z in out for t in z['tests']),'coverage failures',flush=True)
