from base4 import *
from adapterc import adapter
from gate1 import signature
import exp04_core,exp04_monotone

if __name__=='__main__':
    meter=Meter('PC1_original_paid_windows');out=[]
    for stem in ('NEW','PROTECTED'):
        ss=load(C3/f'{stem}_SOURCE_CATALOG.json');rows=load(C3/f'{stem}_RESULTS.json')
        for i,s in enumerate(ss):
            p=load(C3/f'{stem}_PHYS_{i:02}.json');b=load(C3/f'{stem}_BIRTH_{i:02}.json')
            f=load(C3/f'{stem}_FOREST_{i:02}.json');an=load(C3/f'{stem}_M1_AUDIT_{i:02}.json')
            r=adapter(s,p,b);eps,ps=exp04_core.psi_episodes(r)
            star=rows[i]['original_R_star'];z=exp04_monotone.monotone_analysis(r,star,eps)
            assert {digest(e['rho']) for e in z['paid']}=={digest(e['rho']) for e in star}
            sig=signature(p,b,f,an);ds={tuple(d['parent']):d for d in p['doubles']};U={ast.literal_eval(v):u for v,u in b['U'].items()}
            critical=[];support={}
            for e in z['paid']:
                if e['original_parent'][0]!=2:continue
                sysz=next(q for q in z['systems'] if q['comparison_orientation']==e['orientation'] and q['strategy']==e['strategy'])
                wi,t,j=e['shadow_double'];w=sysz['windows'][wi];key=(e['strategy'],e['orientation'],wi)
                support[str(key)]=w
                v=tuple(e['original_parent']);assert v in sig
                creator=tuple(U[v]['creator'])
                critical.append({'gap':e,'original_R6':next(a for a in b['original_R6'] if a['rho']==e['rho']),
                    'consumer_double':ds[v],'consumer_U':U[v],'creator_double':ds[creator],'creator_U':U[creator],
                    'pre_A_path':p['boundaries'][1]['A_path'],'prehybrid_parent_rank':sorted({tuple(q['original_parent']) for q in star if q['consumer']==2}).index(v)+1,
                    'actual_D_rank':None,'supporting_window':str(key)})
            record={'source':s['name'],'source_sha256':digest(s),'stem':stem,'index':i,
                'critical':critical,'supporting_windows':support,'episodes':eps,'Psi_after_operations':ps,
                'frozen_all_gap_assignments':z['paid'],'all_R_star_paid':True,
                'physical_source_file':str(C3/f'{stem}_PHYS_{i:02}.json'),'physical_source_sha256':hfile(C3/f'{stem}_PHYS_{i:02}.json')}
            out.append(record);write('PC1_PAID_WINDOW_CERTIFICATES.json',out)
            for key,w in support.items():print('PC1',stem,i,key,'targets',w['targets'][:12],'ell',w['ell'],'domain',w['domain_size'],'firstretained',w['retained'][:3],'last',w['retained'][-1],flush=True)
            del p,b,f,an,r,z;gc.collect()
    meter.info['complete_inherited_sources']=len(out);meter.ok=True
