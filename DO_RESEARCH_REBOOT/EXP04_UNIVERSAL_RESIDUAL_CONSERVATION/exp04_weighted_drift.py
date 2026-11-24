from exp04_weighted_potential import *


if __name__=='__main__':
    meter=Meter('EXP04_cycle10_weighted_drift_v002');out=[]
    archived=json.loads((PREV/'EXP03_SOURCE_WITNESSES.json').read_text())
    byname={s['name']:s for s in archived['inherited_sources']+archived['new_sources']}
    for n in (65,129,257,513):
        a=Tree(vine(range(1,n+1)));b=Tree(vine(range(1,n+1)))
        for x in range(2,n+1):Replay.plain_splay(a,x)
        before=b.state();p0=product_potential(a,b);Replay.plain_splay(b,n);p1=product_potential(a,b);ratio=p1/p0
        m=(n-1)//2;exponent=2*m*(m+1)-1
        assert ratio<=Fraction(1,2**exponent)
        # Explicit post-splay geometry: even right spine under max, odd leaves.
        assert b.root==n and b.ch[n]==[2,None]
        for j in range(1,m+1):assert b.ch[2*j]==[2*j-1,2*j+2 if j<m else None]
        p=(n-1).bit_length()-3;witness=byname[f'mixed_p{p}_Gcopies2']
        out.append({'n':n,'first_B_operation':n,'actual_A_root':n,'B_before':before,'B_after':b.state(),
            'exact_product_ratio_hex':[hex(ratio.numerator),hex(ratio.denominator)],
            'certified_first_B_potential_drop_at_least':exponent,'omitted_hit_family_A':4*n-1,
            'archived_complete_witness':witness,'archived_measured_A':witness['A'],
            'archived_signed_A_lower_bound':exponent-4*witness['A'],
            'parametric_omitted_hit_signed_A_lower_bound':exponent-4*(4*n-1),
            'qualification':'The original weighted Access Lemma1 gives Delta_B Phi<=4 since target weight>=1 and total weight<=2. Genuine KEEP count K_B<=A; B root repeats change no potential.'})
        print(n,'first B drop >=',exponent,'A(source)=',4*n-1,flush=True)
    write('EXP04_WEIGHTED_SIGNED_DRIFT_REFUTATION.json',{'sources':out,
        'conclusion':'No absolute bound on signed A drift/A for this candidate potential; not a counterexample to Q_B/A.',
        'proof':'Before first B access to n=2m+1, A is left vine, B right vine. P_before>=4^(n(n-1)/2). After B splays n, odd keys are leaves and even spine contributions give P_after<=(4/3)4^(m^2). Hence log2(P_before/P_after)>=2m(m+1)-1. Other genuine B accesses increase Phi by at most4 each (weighted Access Lemma1), with K_B<=A. Full paired closure gives total signed A drift >=2m(m+1)-1-4A =Omega(n^2), while A=4n-1.'})
    meter.success=True
