from base5 import *
from new_audit5 import audit

if __name__=='__main__':
    m=Meter('left_fringe_original_audits');out=[]
    for i,s in enumerate(load(ROOT/'FRINGE_SOURCE_CATALOG.json')):
        row=audit(s,i,'FRINGE');out.append(row);write('FRINGE_RESULTS.json',out)
        print('PASS left-fringe',i,'starparents',len(row['critical']['R_star_parents']),'F_E_negative',len(row['critical']['sigma_F_E_negative_gaps']),
            'repeated_old',len(row['critical']['canonical_repeated_sigma_edges']),'noH_allquota',row['no_H_diagnostic']['all_selected'],flush=True);gc.collect()
    m.info['fresh_complete_sources']=len(out);m.ok=True
