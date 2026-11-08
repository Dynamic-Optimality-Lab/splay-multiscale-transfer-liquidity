"""Recurse after a non-falsifying first family: force a precise zero-edge
leaf-law failure, then repair the smaller branch frontier on this family.
"""
import json,time
import audit_discovery as V
from leaf_channels import build,augment_partial
p=V.p;B=V.B;P=V.P
def counter_word(r):
    n=2*r-1;g=2*(r-6)+1;x=g+2;old=list(range(g,n+1,2))
    prefix=[('K',y) for y in range(3,g+1,2)]
    middle=[('K',n),('D',g),('D',x),('D',g),('K',g)]
    middle += [('K',y) for y in old[1:]+old[-2::-1]]
    suffix=[('K',y) for y in range(g-2,0,-2)]
    return prefix+middle+suffix+[('D',y) for y in range(n,0,-1)]
def main():
    reports=[]
    for r in (7,8):
        n=2*r-1;M=set(range(1,n+1,2));one=V.gamma_word(r)+counter_word(r)
        for mirrored in (False,True):
            def mirror(t):return t if isinstance(t,str) else (n+1-t[0],mirror(t[2]),mirror(t[1]))
            initial=mirror(p.vine(n)) if mirrored else p.vine(n)
            word=[(m,n+1-x if mirrored else x) for m,x in one];z=n-2 if mirrored else 3
            E=initial;seen={};steps=0
            while E not in seen:
                assert steps<50;seen[E]=steps;steps+=1
                for m,x in word:
                    if m=='K' and x!=z:E=p.trace(E,x)[0]
            u=seen[E];L=steps-u;E0=E
            rows,end=p.replay(initial,word*L,erased=z,erased_start=E0);assert end==(initial,initial,E0)
            assert {t['target'] for t in rows if t['genuine_F']}==M
            assert all(p.labels(p.core(t['before'][1],M))==set(range(1,n+1)) for t in rows)
            v=build(rows,M);bad=[e for e in v['macros'] if e['signed_leaf_residual']<0]
            assert any((e['H'],e['Q'],len(e['branch']),e['z'])==(1,2,2,1) for e in bad)
            full=dict(v['h']);repairs=[];block=len(word)
            for copy in range(L):
                reset_start=(copy+1)*block-n+1;reset_end=(copy+1)*block
                supplier=next(e for e in v['macros'] if reset_start in e['occurrences'])
                assert not supplier['branch'] and supplier['z']==0
                spare=[(t['occurrence'],j,b) for t in rows[reset_start-1:reset_end] for j in range(1,t['a']+1) for b in (0,1)]
                rr=sorted(d for d in v['R'] if copy*block<d[0]<=(copy+1)*block)
                assert len(rr)<=4 and len(spare)>=2*(n-1)
                assert not set(spare)&set(v['h'].values())
                full.update(zip(rr,spare));repairs.append({'block_copy':copy,'reset_occurrences':list(range(reset_start,reset_end+1)),
                    'supplier_macro':supplier['macro'],'branch_frontier':rr,'actual_pairs':list(zip(rr,spare))})
            assert set(full)==v['D'] and len(set(full.values()))==len(full) and set(full.values())<=v['U']
            owner=None
            if r==7:
                aux=[]
                for t in rows:
                    m='D' if t['mode']=='K' and t['target']==z else t['mode'];a,b=t['before'],t['after']
                    aux.append(dict(t,mode=m,genuine_F=m=='K' and a[2][0]!=t['target'],qF=t['qE'],qE=0,
                        before=(a[0],a[2],a[2]),after=(b[0],b[2],b[2])))
                fE=V.allocate(aux)['f'];C=v['D']&set(fE);l={d:fE[d] for d in C}
                prior=V.X.exchange(v['D'],v['U'],l,v['h0']);a=prior['allocation']
                partial=augment_partial(v['D'],v['U'],a,v['h']);finished=augment_partial(v['D'],v['U'],a,full)
                assert not finished['blocked_frontier'] and all(finished['allocation'][d]==u for d,u in a.items())
                Rnat=v['D']-set(v['h0']);alpha={d:d if d in Rnat else prior['blocked'][d]['owner'] for d in v['D']-set(a)}
                deepR={tuple(d) for e in v['deep'] for d in e['natural_excess']}
                owner={'actual_f6_from_sealed_CD6':True,'auxiliary_rows':aux,'fE':V.pack(fE),'common':C,'prior':V.pack(a),
                    'leaf_only_frontiers':V.pack(partial['blocked_frontier']),'leaf_only_paths':partial['paths'],
                    'deep_anchored_blocked':[d for d in partial['blocked_frontier'] if alpha[d] in deepR],
                    'family_full_after_exchange':V.pack(finished['allocation']),'family_full_paths':finished['paths'],'all_old_values_fixed':True}
            reports.append({'r':r,'mirrored':mirrored,'initial_A_BF':initial,'initial_BE':E0,'erased':z,'word':word*L,'base_word':word,
                'actual_reaching_prefix_copies':u,'L':L,'rows':rows,'A':sum(t['a'] for t in rows),
                'QF':sum(t['qF'] for t in rows),'QE':sum(t['qE'] for t in rows),'maximal_full_core':n,
                'leaf_partial_h':V.pack(v['h']),'branch_frontier':v['R'],'channels':v['channels'],'macros':v['macros'],
                'deep_packets':v['deep'],'leaf_D_counterexamples':bad,'family_repairs':repairs,'family_full_h':V.pack(full),'owners':owner})
            print(json.dumps({'r':r,'mirror':mirrored,'length':len(rows),'deep':len(v['deep']),'bad_leaf_rows':len(bad),'branch_slots':len(v['R']),
                'leaf_owner_blocks':len(owner['leaf_only_frontiers']) if owner else None}),flush=True)
    V.out('leaf_source_certificates2.json',V.ser({'status':'SOURCE_EXACT_UNIFORM_LEMMA_AUDITS_AND_RESTRICTED_FAMILY_FUNDING','reports':reports,
        'scope':'complete uniform proofs separate; these are exact deterministic source witnesses, not finite support induction',
        'main_U_DEEP_GROUP':'OPEN_AFTER_LOCKS_AND_GENERAL_BRANCH_FRONTIER','new_source_engine_calls':V.calls}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:V.out('audit_discovery2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':V.calls,'new_finite_tests':4})
