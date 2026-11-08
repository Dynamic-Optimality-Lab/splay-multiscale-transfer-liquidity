"""Falsify, do not assume, the candidate post-owner leaf-image capacity.
All seven actual erased six-key owners of one exact r7 source are tested.
"""
import json,time
import audit_discovery as V
from leaf_channels import build,augment_partial
p=V.p;B=V.B
def main():
    source=json.loads((B/'zero_run_source_certificates.json').read_text())['reports'][0]
    template=source['rows'][:len(source['base_word'])];word=source['base_word'];R=V.freeze(source['initial_A_BF']);M=set(range(1,14,2));reports=[]
    for erased in sorted(M):
        E=R;seen={};u=0
        while E not in seen:
            assert u<50;seen[E]=u;u+=1
            for mode,x in word:
                if mode=='K' and x!=erased:E=p.trace(E,x)[0]
        start=seen[E];L=u-start;E0=E;rows=[]
        for copy in range(L):
            for old in template:
                before=(V.freeze(old['before'][0]),V.freeze(old['before'][1]),E);ev=[]
                if old['mode']=='K' and old['target']!=erased:E,_,ev=p.trace(E,old['target'])
                rows.append(dict(old,occurrence=copy*len(word)+old['occurrence'],qE=sum(e['kind']=='DOUBLE' for e in ev),
                    before=before,after=(V.freeze(old['after'][0]),V.freeze(old['after'][1]),E)))
        assert E==E0;v=build(rows,M);aux=[]
        for t in rows:
            mode='D' if t['mode']=='K' and t['target']==erased else t['mode'];a,b=t['before'],t['after']
            aux.append(dict(t,mode=mode,genuine_F=mode=='K' and a[2][0]!=t['target'],qF=t['qE'],qE=0,
                before=(a[0],a[2],a[2]),after=(b[0],b[2],b[2])))
        small=V.allocate(aux);fE=small['f'];l={d:fE[d] for d in v['D']&set(fE)}
        prior=V.X.exchange(v['D'],v['U'],l,v['h0']);a=prior['allocation'];Pmissing=sorted(v['D']-set(a));free=sorted(set(v['h'].values())-set(a.values()))
        ext=augment_partial(v['D'],v['U'],a,v['h']);enough=len(free)>=len(Pmissing)
        candidate={**a,**dict(zip(Pmissing,free))} if enough else None
        if candidate:assert set(candidate)==v['D'] and len(set(candidate.values()))==len(candidate)
        reports.append({'erased':erased,'u':start,'L':L,'actual_auxiliary_core':small['core'],'rows':rows,
            'f6':V.pack(fE),'prior':V.pack(a),'leaf_comparison_h':V.pack(v['h']),'partial_forward_blocks':V.pack(ext['blocked_frontier']),
            'old_unpaid':len(Pmissing),'candidate_free_image_units':free,'candidate_free_image_count':len(free),
            'candidate_capacity_passes_this_source':enough,'candidate_completed_map':V.pack(candidate) if candidate else None,
            'not_universal':'no source theorem proves this image capacity for arbitrary r/W/owners'})
        print(json.dumps({'erased':erased,'core6':small['core'],'unpaid':len(Pmissing),'forward_blocks':len(ext['blocked_frontier']),
            'free_image':len(free),'image_capacity_passes':enough}),flush=True)
    V.out('owner_image_source_audit.json',V.ser({'status':'EXACT_SOURCE_IMAGE_FALSIFICATION_AUDIT_NOT_UNIVERSAL_PROOF','source_word':word,
        'initial_A_BF':R,'reports':reports,'source_engine_calls':V.calls}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:V.out('audit_owner_images_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':V.calls,'new_finite_tests':7})
