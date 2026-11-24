from base4 import *
from sources4 import make
from deform_audit4 import audit

if __name__=='__main__':
    m=Meter('shared_disruption');ss=[make(16,'half'),make(32,'half'),make(64,'half'),make(32,repeats=8)]
    write('SHARED_SOURCE_CATALOG.json',ss);out=[]
    for i,s in enumerate(ss):
        row=audit(s,i,stem='SHARED');out.append(row);write('SHARED_RESULTS.json',out)
        c=row['critical'];print('PASS SHARED',i,'N',c['physical_N_h'],'a',c['A_gap'],'Rstarparents',len(c['R_star_parents']),
            'starOutsideF',len(c['R_star_gaps_outside_F']),'E',row['assigned_counts']['E_old'],'S',len(row['actual_S_UU']),flush=True);gc.collect()
    m.info['fresh_complete_sources']=len(out);m.ok=True
