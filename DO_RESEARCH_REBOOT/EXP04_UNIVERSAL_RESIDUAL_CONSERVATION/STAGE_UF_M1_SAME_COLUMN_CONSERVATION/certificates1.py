from base1 import *
from physical1 import Edges
from fractions import Fraction
import gc

if __name__=='__main__':
    meter=Meter('candidate_certificates');sources=load(ROOT/'NEW_SOURCE_CATALOG.json');out=[]
    for i in range(5):
        s=sources[i];n=s['n'];m=s['m'];a=load(ROOT/f'NEW_AUDIT_{i:02}.json');phys=load(ROOT/f'NEW_PHYS_{i:02}.json')
        b=Edges(s['initial_B']);gain_volume=0
        for e in phys['events']:
            if e['actor']!='B':continue
            v=e['promoted'];old=b.m[v];b.step(e);gain_volume+=(b.m[v]&~old).bit_count()
            assert v==e['target'] and e['case']=='ZIG'
        A=s['analytic_A'];F=n*(m+n-1)
        assert a['flux_totals']['A_signed_flux']==gain_volume==F
        fns={'linear':lambda z:z,'indicator':lambda z:int(z>0),'integer_log':lambda z:z.bit_length()}
        fs={}
        for name,f in fns.items():
            analytic=m*(f(n-1)+f(1))+2*sum(f(j) for j in range(1,n))
            recorded=sum(f(z['created_atoms']) for z in a['primitive_flux'] if z['id'][0]=='A')
            assert analytic==recorded
            fs[name]={'original_A_flux':analytic,'flux_over_A':str(Fraction(analytic,A))}
        out.append({'source':s['name'],'n':n,'m':m,'A':A,'Q_B':0,'original_R6':0,'actual_R_C':0,
            'full_original_S':phys['original_S'],'A_signed_volume_flux':F,'B_target_marked_gain_volume':gain_volume,
            'B_non_target_gain_events':0,'exact_flux_over_A':str(Fraction(F,A)),
            'candidate_function_checks':fs,'scope':'Refutes constant A-volume-flux price and target-gain volume price, not an unpaid C bound.'})
        del a,phys,b;gc.collect()
    chainrows=[]
    for i in (6,7,8,9,10,11):
        s=sources[i];phys=load(ROOT/f'NEW_PHYS_{i:02}.json');a=load(ROOT/f'NEW_AUDIT_{i:02}.json')
        k=s['k'];g=2 if s['family']=='private_hanger_lift_of_C05_chain' else 1
        ds={tuple(v['parent']):v for v in phys['doubles']}
        chain=next(v for v in a['maximal_C_chains'] if v['head']==[1,1])
        assert chain['C_count']==k-1 and chain['g']==g
        Ag=chain['A_component_keys_mask'];volume=[]
        for h in range(1,k+1):
            z=ds[h,1];before=(z['F']&~Ag).bit_count();after=(z['J']&~Ag).bit_count()
            assert (before,after)==(2*(k-h+1),2*(k-h))
            volume.append({'original_parent':[h,1],'g':g,'target':z['target'],
                'column_mismatch_before':before,'column_mismatch_after':after,
                'column_indicator_drop':int(before>0)-int(after>0),'actual_gap_weight':0})
        assert sum(z['column_indicator_drop'] for z in volume[1:])==1
        chainrows.append({'source':s['name'],'k':k,'physical_population':len(s['initial_B']['children']),
            'critical_C_chain_edges':k-1,'A_component':chain['A_component_shape'],'critical_column_rows':volume,
            'C_consumers_with_zero_own_column_indicator_drop':k-2,'actual_R_C':0,
            'scope':'Refutes all-physical-C per-column unit-debit templates; actual original overflow remains periodic-paid.'})
        del phys,a;gc.collect()
    write('TEMPLATE_FAILURE_CERTIFICATES.json',{'volume_price_obstructions':out,'long_chain_indicator_obstructions':chainrows,
        'universal_claim':'Exact physical formulas are proved in M1_POTENTIAL_TEMPLATE_OBSTRUCTION.md; finite checks are controls.'})
    meter.ok=True;print('PASS exact source-uniform template counterfamily formulas and complete witnesses',flush=True)
