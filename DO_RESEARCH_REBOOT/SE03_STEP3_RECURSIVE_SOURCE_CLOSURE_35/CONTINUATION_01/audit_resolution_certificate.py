"""Independent certificate/status/source-scope integration check.
No source engine imports or fresh original accesses.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def keys(t,lo=float('-inf'),hi=float('inf')):
    if t is None:return []
    k,l,r=t;assert lo<k<hi;return keys(l,lo,k)+[k]+keys(r,k,hi)
def main():
    z=read(F/'SI34_source_countercertificate.json');src=z['source'];reg=read(F/'proof_boxes_v2.json')
    for n,h in z['source_proof_artifacts'].items():assert sha(F/n)==h
    for n,h in z['audit_receipts'].items():assert sha(F/n)==h
    for aud in ('independent_critical_source_audit.json','independent_symbolic_source_audit.json'):
        for n,h in read(F/aud)['input_sha256'].items():assert sha(F/n)==h
    assert keys(src['initial_A'])==keys(src['desired_A_before_forward'])==list(range(1,16))
    assert keys(src['gamma_low']['input_low_tree'])==keys(src['gamma_low']['output_low_tree'])==list(range(1,15))
    word=src['word'];assert word[0]==dict(kind='KEEP',key=15) and word[1]==dict(kind='DELETE',key=1)
    keep=[15]+word[3]['word']+word[4]['word'];assert len(keep)==24 and set(keep)==set(range(1,16,2)) and all(a!=b for a,b in zip(keep,keep[1:]))
    assert keep[-1]!=keep[0] and src['erased_key']==3
    assert not src['source_word_fully_expanded_numerically'] and z['all_selected_own_excess'] and z['no_DELETE_only_return_loop']
    D={tuple(d) for d in z['actual_B_demands']};NN={t:{tuple(u) for u in us} for t,us in z['exact_neighborhoods'].items()};U=set().union(*NN.values())
    assert len(D)==9 and len(U)==8 and len(D)-len(U)==z['deficit']==1
    assert sum(len(s)-3 for s in NN.values())==z['sigma']==3 and sum(map(len,NN.values()))-len(U)==z['overlap']==4
    assert all(len(s-set().union(*(v for k,v in NN.items() if k!=t)))==2 for t,s in NN.items())
    # Demand and bit IDs are exact source-coordinate expressions; no
    # numeric Gamma length or erased period is silently substituted.
    assert {d[0] for d in D}=={'b+ell+6','b+ell+10','b+ell+14'} and {d[1] for d in D}=={1,2,3}
    nodes={n['id']:n for n in reg['boxes']};assert all(nodes[i]['status']=='REFUTED' for i in ('ROOT35','PEEL35','COMP35','MULTI35'))
    assert nodes['REAL35']['status']=='PROVED' and nodes['U35']['status']=='BLOCKED' and not reg['full_architecture_refuted']
    assert nodes['REPAIR35']['status']=='PROVED' and 'this source only' in nodes['REPAIR35']['source_scope']
    old=read(C/'campaign_manifest.json')
    for n,h in old['artifacts'].items():assert sha(C/n)==h
    for phase in ('core44','verify87','verify88','proof173'):assert read(B/f'run_{phase}_result.json')['status']=='PASS'
    result=dict(status='PASS_SOURCE_COUNTERCERTIFICATE_AND_NEGATIVE_RECONSTRUCTION',input_sha256={n:sha(F/n) for n in ('SI34_source_countercertificate.json','proof_boxes_v2.json','SI34_SOURCE_REFUTATION.md','SCOPE_AUDIT.md')},mathematical_outcome='E-SI34',full_original_source_proof='symbolic construction with canonical finite transforms and proved B recurrence',full_numerical_replay=False,root_law_refuted=True,Coarse_Double_counterexample=False,all_route_architecture_counterexample=False,old_owner_and_certificate_hashes_preserved=True,source_queries=0,source_engine_calls=0,verification_type='same-agent distinct implementation/static audit; not external/formal verification')
    with (F/'independent_resolution_certificate_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(result['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify89_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
