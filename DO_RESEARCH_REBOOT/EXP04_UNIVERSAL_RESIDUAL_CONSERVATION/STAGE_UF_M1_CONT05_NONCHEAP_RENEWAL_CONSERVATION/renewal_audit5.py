from base5 import *
from new_audit5 import audit

if __name__=='__main__':
    m=Meter('renewal_packet_original_audits');out=[]
    for i,s in enumerate(load(ROOT/'RENEW_SOURCE_CATALOG.json')):
        row=audit(s,i,'RENEW');out.append(row);write('RENEW_RESULTS.json',out)
        print('PASS renewal',i,'N',row['critical']['N_h'],'starparents',len(row['critical']['R_star_parents']),
            'F_E_negative',len(row['critical']['sigma_F_E_negative_gaps']),'oldedges',len(row['critical']['canonical_repeated_sigma_edges']),
            'noH_allquota',row['no_H_diagnostic']['all_selected'],flush=True);gc.collect()
    m.info['fresh_complete_sources']=len(out);m.ok=True
