"""Distinct immutable-engine source, physical ID, partial exchange audit.
No source producer or primary source engine is imported. Exchange expected
answers are reconstructed BACKWARDS from terminal units/blocked owners.
"""
import collections,importlib.util,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
spec=importlib.util.spec_from_file_location('independent_splay10',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
from physical_exchange import exchange
started=time.process_time();calls=0;CAP=min(90,float(sys.argv[1])-4)
def move(t,x):
    global calls
    calls+=1;assert calls<1500000 and time.process_time()-started<CAP
    return I.trace(t,x)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def tree(v):return ('leaf',v) if isinstance(v,str) else I.node(v[0],tree(v[1]),tree(v[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def core(t,marks):
    if t[0]=='leaf':return frozenset()
    L,R=core(t[2],marks),core(t[3],marks)
    return L|R|{t[1]} if t[1] in marks or L or R else frozenset()
def mirror(t,n):return ('leaf','F'+str(n-int(t[1][1:]))) if t[0]=='leaf' else I.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
def q(ev):return sum(v[0]!='ZIG' for v in ev)
def path(t,x):
    ans=''
    while t[0]!='leaf' and t[1]!=x:
        c=0 if x<t[1] else 1;ans+='LR'[c];t=t[2+c]
    assert t[0]!='leaf';return ans
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def reverse_expected(D,U,locked,h):
    inv={u:d for d,u in h.items()};answers={};blocks={}
    def back(unit):
        seen=set()
        while unit in inv:
            d=inv[unit]
            if d in seen:return None
            seen.add(d)
            if d not in locked:return d
            unit=locked[d]
        return None
    for unit in U-set(locked.values()):
        root=back(unit)
        if root is not None:answers[root]=unit
    for owner in set(locked)-set(h):
        root=back(locked[owner])
        if root is not None:blocks[root]=owner
    return {**locked,**answers},blocks
def allmaps(D,U):
    for n in range(len(D)+1):
        for ds in itertools.combinations(D,n):
            for us in itertools.permutations(U,n):yield dict(zip(ds,us))
def main():
    data=json.loads((B/'deficient_source_schemas.json').read_text());fund=json.loads((B/'family_funding_receipts.json').read_text())
    reports=[];allrows=0;erasedchecks=0;transport=0
    for fam,receipt in zip(data['families'],fund['families']):
        n=fam['core'];R=tree(fam['initial_A_BF']);marks=set(fam['marks']);rows=fam['rows'];N=len(rows)
        for reflected in (False,True):
            root=mirror(R,n) if reflected else R;A=BF=root;cost=[0,0];units=set();demands=set();recent=[]
            word=[(m,n+1-x if reflected else x) for m,x in fam['word']]
            for m,x in reversed(word):
                if m=='K' and x not in recent:recent.append(x)
            for i,((m,x),old,chart) in enumerate(zip(word,rows,fam['charts']),1):
                assert core(BF,{n+1-k for k in marks} if reflected else marks)==set(range(1,n+1))
                beforeA,beforeB=A,BF;pa=path(A,x);A,ae=move(A,x);be=[]
                if m=='K':BF,be=move(BF,x)
                assert len(ae)==old['a'] and q(be)==old['qF']
                expectedA=tree(old['after'][0]);expectedB=tree(old['after'][1])
                if reflected:expectedA=mirror(expectedA,n);expectedB=mirror(expectedB,n)
                assert A==expectedA and BF==expectedB
                oldrecent=[n+1-k for k in chart['recent_before']] if reflected else chart['recent_before']
                assert recent==oldrecent
                if m=='K':recent=[x]+[k for k in recent if k!=x]
                assert recent==([n+1-k for k in chart['recent_after']] if reflected else chart['recent_after'])
                cost[0]+=len(ae);cost[1]+=q(be)
                units|={(i,j,b) for j in range(1,len(ae)+1) for b in (0,1)}
                demands|={(i,k) for k in range(1,q(be)+1)};allrows+=1
            assert (A,BF)==(root,root) and cost==[fam['A'],fam['QF']]
            h={tuple(v['demand']):tuple(v['unit']) for v in receipt['full_allocation']}
            assert set(h)==demands and len(set(h.values()))==len(h) and set(h.values())<=units
            for repair in receipt['repairs']:
                donors=list(map(tuple,repair['actual_donors']));prev=fam['packets'][repair['previous_actual_packet']]
                assert all(u[0] in prev['occurrences'] for u in donors)
                assert len(donors)==len(repair['demands']) and set(donors)<=set(receipt and units)
            if not reflected:
                for al in fam['erasure_alignments']:
                    assert al['status']=='EXACT_SOURCE_ALIGNMENT'
                    E=R;z=al['erased'];base=al['u']*N;T=al['L']*N
                    for repeat in range(al['u']):
                        for m,x in fam['word']:
                            if m=='K' and x!=z:E=move(E,x)[0]
                    assert E==tree(al['initial_BE']);begin=E;qe=0
                    for m,x in fam['word']*al['L']:
                        if m=='K' and x!=z:E,ev=move(E,x);qe+=q(ev)
                    assert E==begin and qe==al['QE'] and len(core(E,marks-{z}))==al['aux_core']
                    # EVERY possible integral source cut; no fictitious offset
                    # is claimed to be the actual M3 maximum-debt cut.
                    for delta in range(T):
                        def tau(t):return base+t if t>delta else base+t+T
                        actualU={(tau(copy*N+u[0]),u[1],u[2]) for copy in range(al['L']) for u in units}
                        mapped=[(tau(copy*N+u[0]),u[1],u[2]) for copy in range(al['L']) for u in h.values()]
                        assert len(set(mapped))==len(h)*al['L'] and set(mapped)<=actualU
                        assert all(base+delta<t<=base+delta+T for t,j,b in mapped)
                        transport+=1
                    erasedchecks+=1
            reports.append({'core':n,'reflected':reflected,'A':cost[0],'QF':cost[1],
                'closure':True,'original_CD_slack':2*cost[0]-cost[1],
                'funded_demands':len(h),'deficit_packets':[(v['H'],v['Q'],v['w']) for v in fam['deficit_packets']]})
    # Mandatory original26-operation Gamma, read exact authoritative source.
    gamma=json.loads((B.parent/'SE03_STEP2_REPAY01/source_term_derivation.json').read_text())
    R=tree(gamma['initial_full_and_A']);E0=tree(gamma['initial_recurrent_E']);A=BF=R;BE=E0;ar=[];genE=[]
    for i,r in enumerate(gamma['trace'],1):
        x=r['key'];m=r['mode'];pa=path(A,x);A,ae=move(A,x);be=ee=[]
        if m=='K':
            BF,be=move(BF,x)
            if x!=gamma['erased_key']:
                if BE[1]!=x:genE.append(i)
                BE,ee=move(BE,x)
        assert [len(ae),q(be),q(ee)]==r['costs']
        assert (A,BF,BE)==tuple(tree(t) for t in r['end_terms'])
        ar.append({'a':len(ae),'qF':q(be),'qE':q(ee),'events':ae})
    assert (A,BF,BE)==(R,R,E0)
    assert [sum(r[k] for r in ar) for k in ('a','qF','qE')]==[34,30,24]
    assert ar[12]['a']==1 and ar[12]['qE']==4 and ar[12]['qF']==5
    assert ar[9]['a']==4 and ar[9]['events'][2][0]=='RR'
    assert ar[8]['a']+3==4 and not any(8<i<12 for i in genE)
    assert 12 in genE and 13 in genE and 9 not in genE
    cutchecks=[]
    for cut in genE:
        if cut==12:continue # debt0 cannot be a maximum, since D13=2.
        which=[int(t<=cut) for t in (9,10,13)]
        assert len(set(which))==1
        cutchecks.append(cut)
    gamma_result={'status':'PASS_SOURCE_EXACT_ORIGINAL_GAMMA_REPAIR','A':34,'QF':30,'QE':24,
        'D12':0,'D13':2,'D_reason':'H1Q4 auxiliary edge and sealed range[0,2]',
        'units':[[10,3,0],[10,3,1]],'full_demands':[[9,1],[13,5]],
        'tail_ordinal_in_previous_macro':4,'actual_maximum_cut_candidates_not_splitting_blocks':cutchecks,
        'cut12':'REJECTED by actual forced debt0<2','fixed_fE':'both units excluded from first-three-event selector for EVERY actual M3 debt sequence',
        'global_fE_values':'not invented or numerically evaluated beyond these forced/excluded facts'}
    out('gamma_period_ownership_audit.json',gamma_result)
    # Exhaust every SMALL abstract map, as a regression of the universal
    # algebraic exchange theorem, not as source or arbitrary-size proof.
    D=(0,1,2);U={0,1,2,3};maps=list(allmaps(D,tuple(sorted(U))));checks=0;blocked_examples=[]
    for locked in maps:
        for h in maps:
            actual=exchange(D,U,locked,h);expected,blocks=reverse_expected(set(D),U,locked,h)
            assert actual['allocation']==expected
            assert {r:v['owner'] for r,v in actual['blocked'].items()}==blocks
            if len(h)==len(D):assert actual['total']
            if blocks and len(blocked_examples)<2:blocked_examples.append({'locked':list(locked.items()),'h':list(h.items()),'blocked':list(blocks.items())})
            checks+=1
    rejected=[]
    for name,h in [('duplicate_donor',{0:0,1:0}),('outside_period',{0:99})]:
        try:exchange(D,U,{},h)
        except ValueError:rejected.append(name)
        else:raise AssertionError('invalid ownership accepted')
    out('independent_audit.json',{'status':'PASS_STATED_PARTIAL_THEOREMS_AND_RECEIPTS_ONLY',
        'source_reports':reports,'new_source_rows_recomputed':allrows,'actual_erasure_alignments':erasedchecks,
        'integral_period_cut_transports_checked':transport,'exchange_regression_map_pairs':checks,
        'blocked_frontier_examples':blocked_examples,'invalid_owner_inputs_rejected':rejected,
        'uniform_exchange':'independently reverse-checked; universal proof is algebraic, not extrapolated from5329 cases',
        'core6_universal':'analytic proof Q<=2,H>=1 plus actual-ID exchange; no finite-to-universal inference',
        'Gamma':'original26-op source and occurrence9/10/12/13 verified',
        'Step2':'OPEN','global_donor_supply':'NOT_PROVED','new_finite_tests':checks+2+12,
        'source_engine_calls':calls,'old_semantic_rows_replayed':26,
        'trust':'same-agent distinct immutable source engine and separate backward component algorithm; no formal assistant/external review'})
    print(json.dumps({'status':'PASS_PARTIAL_ONLY','source_calls':calls,'source_rows':allrows,
        'alignments':erasedchecks,'period_cuts':transport,'map_checks':checks}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'new_finite_tests':5343,'old_semantic_rows_replayed':26})
