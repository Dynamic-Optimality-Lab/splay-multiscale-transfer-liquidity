from epoch_payment import *
from exp01_diagnostics import incidence


if __name__=='__main__':
    meter=Meter('epoch_controls');out=[]
    # Reconstruct original residuals before any new payment.
    private=json.loads((C2/'PRIVATE_ANCESTOR_SOURCES.json').read_text())[0]
    archived=json.loads((PARENT/'EXP04_SOURCE_WITNESSES.json').read_text())
    srcs=archived['inherited_sources']+archived['new_sources']
    mixed=next(s for s in srcs if s['name']=='mixed_p5_Gcopies2')
    exp1=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    old=json.loads((exp1/'EXP01_SOURCE_WITNESSES.json').read_text())['sources']
    controls=[private,mixed]+[next(s for s in old if s['name']==n) for n in ('DW_5_1_at31','DW_6_1_at31')]
    for s in controls:
        r=Replay(s);star,_,_=original_residual(r)
        events=star
        if s['name'].startswith('DW'):
            # Broader original R6 controls retain their original rho and consuming parent IDs.
            events=[{'rho':p['rho'],'consumer':p['rho'][0],'original_parent':p['parent'],'type':'R6'}
                    for p in r.pairs if p['class']=='R6']
        z=from_replay(r,events)
        row={'source':s['name'],'population':len(r.keys),'A':r.A,'Q_B':r.Q,
            'original_R_star':star,'demand_scope':'original_R6' if s['name'].startswith('DW') else 'original_R_star',
            'epoch_payment':z,'independent_original_operations':r.independent_checks,
            'trace_hash':digest(r.events)}
        if s['name'].startswith('DW'):
            row['original_root_entry_R6_incidence']=incidence(r,{'R6'})
        if s['name']=='mixed_p5_Gcopies2':
            row['collision_parents_785_793']=[p for p in z['packets'] if [785,2] in p['remaining_original_parents'] or tuple(p['selected_first_parent'])==(785,2)]
        out.append(row);write('EPOCH_CONTROL_RESULTS.json',out)
        print(s['name'],'scope',len(events),'first',len(z['selected_original_gaps']),
              'new',len(z['strictly_new_relative_to_own_path']),'repeat',len(z['repeat_original_gaps']),
              'max epoch parents',z['maximum_unrestricted_parent_uses_per_A_epoch'],flush=True)
        del r
    meter.success=True;meter.details['independently_replayed_controls']=len(out)
