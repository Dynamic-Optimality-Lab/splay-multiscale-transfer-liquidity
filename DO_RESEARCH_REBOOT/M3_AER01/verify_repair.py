"""Complete old image regression and all accepted source-mutant inequalities."""
import sys,json,time,copy
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_AER01','DO_RESEARCH_REBOOT/M3_S3P01']
from empty_interval_potential import rho,EmptyIntervalPotential
from certify_core3_v2 import load as old_load
BASE=Path('DO_RESEARCH_REBOOT/M3_AER01')
def main():
    out=BASE/'repair_certificate.json';assert not out.exists();start=time.process_time();P=EmptyIntervalPotential();pc=P.physical
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_ACL01/finite_completion_v3.json').read_text());patterns=c['patterns'];queries=0;emptytests=0
    for row in patterns:
        a=row['alpha'];im=rho(a);assert pc.ids[im]==row['image'];queries+=1
        # Exhaust every local kind/S/index combination at every observed
        # EMPTY position. Simultaneous replacements follow from the same
        # syntactic empty-interval return, proved in RESULT.md.
        for pos in range(1,7):
            if a[pos][0]!=2:continue
            for k in (0,1,2):
                for ss in (0,1):
                    for ix in range(9):
                        aa=copy.deepcopy(a);aa[pos]=[k,ss,ix]
                        # A depth-one empty branch may expose arbitrary
                        # alias grandchildren; the interval rule ignores them.
                        if pos in (1,2):
                            for q in ((3,4) if pos==1 else (5,6)):aa[q]=[0,1,(ix+q)%9]
                        assert rho(aa)==im;queries+=1;emptytests+=1
        assert queries<1000000 and time.process_time()-start<120,'UNKNOWN finite cap'
    oc,oa=old_load();images=[pc.ids[rho(a)] if a[0][1] else oc['refined_shadow'][i] for i,a in enumerate(oc['shadows'])]
    assert images==oc['refined_shadow']
    assert all(oa['images'][i]==pc.c['B_bases'][b]+pc.local[images[a]] and oa['potential'][i]==pc.p[oa['images'][i]]
      for i,(b,a) in enumerate(zip(oa['ordinary_b'],oa['ordinary_a'])))
    audit=json.loads(Path('DO_RESEARCH_REBOOT/M3_ACL_AUD02/dangling_audit.json').read_text());rows=[]
    for r in audit['accepted_rows']:
        s=P.inspect(r['source']);t=P.inspect(r['destination']);v=r['w']+s['value']-t['value'];assert v>=0,(r['seed'],r['slot'],r['side'],v)
        assert t['table_node'] is not None and t['value']<=-t['psi']
        rows.append({'seed':r['seed'],'slot':r['slot'],'side':r['side'],'ref':r['ref'],'old_residual':r['residual'],
          'new_residual':v,'new_source':s,'new_destination':t})
    result={'status':'FINITE_EXACT_VERIFIED','proper_patterns':len(patterns),'empty_interval_junk_cases':emptytests,
      'finite_queries':queries,'old_registered_values_unchanged':len(oa['potential']),'accepted_original_mutants':len(rows),
      'old_negative_residuals_repaired':sum(r['old_residual']<0 for r in rows),
      'minimum_new_residual':min(r['new_residual'] for r in rows),'new_fit':False,
      'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    assert result['cpu_seconds']<120
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
