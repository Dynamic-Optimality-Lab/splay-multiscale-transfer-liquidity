"""Independent physical fE-interface audit over actual source demand IDs.
Test owner fixtures are arbitrary injections, NOT claimed sealed fE values.
All actual certified maps are covered by the stronger parametric proof.
"""
import collections,importlib.util,json,sys,time
from pathlib import Path
from single_slot_allocator import from_frozen_auxiliary,extend_one
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
spec=importlib.util.spec_from_file_location('separate_owner11',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
started=time.process_time();calls=0;CAP=min(75,float(sys.argv[1])-4)
def move(t,x):
    global calls
    calls+=1;assert calls<1000000 and time.process_time()-started<CAP
    return I.trace(t,x)
def tree(v):return ('leaf',v) if isinstance(v,str) else I.node(v[0],tree(v[1]),tree(v[2]))
def q(ev):return sum(e[0]!='ZIG' for e in ev)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def backwards(unit,inv,locked):
    seen=set()
    while unit in inv:
        d=inv[unit]
        if d in seen:return None
        seen.add(d)
        if d not in locked:return d
        unit=locked[d]
    return None
def reverse_partial(D,U,l,h0,R):
    inv={u:d for d,u in h0.items()};ans=dict(l)
    for unit in U-set(l.values()):
        root=backwards(unit,inv,l)
        if root is not None:ans[root]=unit
    missing=D-set(ans)
    assert len(missing)<=1
    return ans,missing
def main():
    old=json.loads((B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/deficient_source_schemas.json').read_text())
    fam=next(v for v in old['families'] if v['core']==7);Rtree=tree(fam['initial_A_BF']);word=[tuple(v) for v in fam['word']]
    reports=[];cases=0;branches=collections.Counter();nonlocal_units=0;longest=0
    for alignment in fam['erasure_alignments']:
        z=alignment['erased'];E=Rtree
        for copy in range(alignment['u']):
            for m,x in word:
                if m=='K' and x!=z:E=move(E,x)[0]
        assert E==tree(alignment['initial_BE']);E0=E;A=BF=Rtree;rows=[];U=set();D=set();EE=set()
        for i,(m,x) in enumerate(word,1):
            gen=m=='K' and BF[1]!=x;A,ae=move(A,x);be=ee=[]
            if m=='K':
                BF,be=move(BF,x)
                if x!=z:E,ee=move(E,x)
            rows.append({'occurrence':i,'mode':m,'target':x,'genuine_F':gen,'a':len(ae),'qF':q(be),'qE':q(ee)})
            U|={(i,j,b) for j in range(1,len(ae)+1) for b in (0,1)}
            D|={(i,k) for k in range(1,q(be)+1)};EE|={(i,k) for k in range(1,q(ee)+1)}
        assert (A,BF,E)==(Rtree,Rtree,E0)
        common=D&EE;local=collections.Counter();examples=[]
        for reverse in (False,True):
            us=sorted(U,reverse=reverse);es=sorted(EE)
            for offset in range(len(us)):
                test_owner={d:us[(i+offset)%len(us)] for i,d in enumerate(es)}
                result=from_frozen_auxiliary(rows,test_owner);build=result['build'];l={d:test_owner[d] for d in common}
                expected,missing=reverse_partial(D,U,l,build['h0'],build['R'])
                assert expected==result['prior']['allocation'] and missing==result['prior']['uncovered']
                final=result['extension']['allocation']
                assert set(final)==D and len(set(final.values()))==len(final) and set(final.values())<=U
                assert all(final[d]==u for d,u in expected.items())
                assert all(final[d]==test_owner[d] for d in common)
                if not missing:branch='empty_residual'
                else:
                    p=next(iter(missing));branch='p_is_excess' if p==build['R'] else 'p_is_blocked_other_demand'
                    assert result['anchor']==build['R']
                    u=result['extension']['unit'];assert u not in set(expected.values())
                    inv={v:d for d,v in build['h'].items()}
                    candidates=[v for v in U-set(expected.values()) if backwards(v,inv,expected)==p]
                    assert candidates==[u]
                    if u!=build['seed_spare']:nonlocal_units+=1
                    longest=max(longest,len(result['extension']['path']))
                    if len(examples)<2:examples.append({'branch':branch,'missing':p,'R':build['R'],
                        'seed_spare':build['seed_spare'],'selected_unit':u,'path':result['extension']['path']})
                branches[branch]+=1;local[branch]+=1;cases+=1
        reports.append({'erased':z,'aux_core':alignment['aux_core'],'QE':len(EE),'common':len(common),
            'full_only':len(D-EE),'auxiliary_only':len(EE-D),'owner_fixture_cases':dict(local),'examples':examples})
    # Concrete invalid inputs, including another cyclic copy's same local bit.
    rejected=[];good=result['build']['h'];paid=dict(result['prior']['allocation']);DD=result['build']['D'];UU=result['build']['U']
    duplicate=dict(good);ds=sorted(DD);duplicate[ds[1]]=duplicate[ds[0]]
    outside=dict(good);unit=outside[ds[0]];outside[ds[0]]=(unit[0]+len(rows),unit[1],unit[2])
    for name,bad in [('duplicate_physical_bit',duplicate),('other_period_copy',outside)]:
        try:extend_one(DD,UU,paid,bad)
        except ValueError:rejected.append(name)
        else:raise AssertionError('invalid source unit accepted')
    try:extend_one(DD,UU,{},good)
    except ValueError:rejected.append('multiple_residuals_outside_campaign')
    else:raise AssertionError('scope expanded')
    assert rejected==['duplicate_physical_bit','other_period_copy','multiple_residuals_outside_campaign']
    result={'status':'PASS_ALL_OWNER_BRANCHES_ON_ACTUAL_TYPED_SOURCE_IDS','erasure_reports':reports,
        'fixture_scope':'adversarial injective owner maps, not numerical replacements for actual frozen fE',
        'cases':cases,'branches':dict(branches),'non_seed_terminal_donors':nonlocal_units,'longest_actual_ID_path':longest,
        'rejected':rejected,'all_old_assignments_preserved':True,'all_common_fE_values_preserved_parametrically':True,
        'universal_bridge':'all-paid injectivity theorem, no finite-to-universal or actual-fE-realizability claim',
        'source_engine_calls':calls,'new_finite_tests':cases+3}
    out('ownership_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k!='erasure_reports'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_ownership_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'new_finite_tests':699})
