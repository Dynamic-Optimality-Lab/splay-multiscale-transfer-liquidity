"""Complete private-capacity peeling on each saved source graph.
Also checks the new cyclic B-birth intersection lemma on accepted states.
No splay calls; this is not an infinite-source proof.
"""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;C=P/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    z=json.loads((C/'pooled_source_results.json').read_text());result=[]
    for case in z['cases']:
        mm=case['macros'];NN=[{tuple(u) for u in m['N']} for m in mm];active=set(range(len(mm)));steps=[]
        while active:
            counts=collections.Counter(u for i in active for u in NN[i]);eligible=[]
            for i in active:
                priv=sorted(u for u in NN[i] if counts[u]==1)
                if len(priv)>=mm[i]['Q']:eligible.append((i,priv))
            if not eligible:break
            i,priv=min(eligible);steps.append(dict(index=i,end=mm[i]['end'],Q=mm[i]['Q'],private_count=len(priv),selected=priv[:mm[i]['Q']]));active.remove(i)
        union=set().union(*(NN[i] for i in active)) if active else set();deficit=sum(mm[i]['Q'] for i in active)-len(union)
        # For each pair, old marked B ancestors with no genuine refresh on
        # the forward and reverse cyclic arcs each number at most ONE.
        E=len(mm);viol=[];pairrecords=[];birth_bound=0
        for i in range(E):
            gi={x['g'] for x in mm[i]['retirement_proof']}
            for j in range(i+1,E):
                gj={x['g'] for x in mm[j]['retirement_proof']};common=gi&gj
                forward_targets={mm[k]['target'] for k in range(i+1,j)}
                reverse_targets={mm[k]['target'] for k in list(range(j+1,E))+list(range(i))}
                f=common-forward_targets;r=common-reverse_targets
                assert not f&r and len(f)<=1 and len(r)<=1
                # Shared first-retirement operation/pivot identities are
                # actual rotation-ticket identities by OR34, without replay.
                ti={(x['g'],x['all_retiring_operations'][0]) for x in mm[i]['retirement_proof']};tj={(x['g'],x['all_retiring_operations'][0]) for x in mm[j]['retirement_proof']};shared=ti&tj
                assert {g for g,t in shared}<=f|r and len(shared)<=2
                birth_bound=max(birth_bound,len(shared))
                if shared:pairrecords.append(dict(indices=[i,j],forward_unrefreshed=sorted(f),reverse_unrefreshed=sorted(r),shared_first_tickets=sorted(shared)))
        rec=dict(source=case['name'],removed=len(steps),total_macros=len(mm),steps=steps,irreducible_indices=sorted(active),irreducible_deficit=deficit,raw_pool_counterexample=deficit>0,peeling_counterexample=bool(active),cyclic_pair_collision_bound_observed=birth_bound,pair_records=pairrecords)
        if active:
            assert deficit<=0 # Raw source cover already certified in C34.
            rec['irreducible_macros']=[mm[i] for i in sorted(active)];rec['union_units']=sorted(union)
        result.append(rec);print(json.dumps({k:v for k,v in rec.items() if k in ('source','removed','total_macros','irreducible_indices','irreducible_deficit','peeling_counterexample','cyclic_pair_collision_bound_observed')}),flush=True)
    with (F/'peeling_core_and_birth_intersections.json').open('x',encoding='utf-8') as f:json.dump(dict(status='SAVED_SOURCE_PEELING_CORE_AND_NEW_BIRTH_BOUND_CONTROL',input_sha256={'C34/pooled_source_results.json':sha(C/'pooled_source_results.json')},cases=result,source_queries=0,source_engine_calls=0,universal_peeling='ACTIVE',SI34='ACTIVE'),f,indent=2)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof171_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
