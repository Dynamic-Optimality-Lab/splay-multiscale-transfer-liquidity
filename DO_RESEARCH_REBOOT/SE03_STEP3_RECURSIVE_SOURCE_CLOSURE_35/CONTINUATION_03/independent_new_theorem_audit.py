"""Separate symbolic/certificate implementation; no source engines or fresh splays."""
import hashlib,itertools,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    cert=read(F/'new_symbolic_certificate.json');dep=read(F/'dependency_manifest.json')
    for row in dep['inherited']:assert sha(Path(row['path']))==row['sha256']
    assert dep['controller_sha256']==sha(B/'run_phase_1440.py')=='f630e39f4fac093f3ab62cf6458dacbda7d17ac4e8e83be83c215a212e1cb40f'
    # All positive path degree compositions, independently of producer's (q,b,d) loop.
    found={}
    def compositions(total,length,prefix=()):
        if length==0:
            if total==0:yield prefix
            return
        for val in range(1,total-length+2):
            yield from compositions(total-val,length-1,prefix+(val,))
    for total in range(1,7):
        for q in range(1,total+1):
            for ds in compositions(total,q):
                b=sum(v>=3 for v in ds)
                for d in range(7-total):
                    kappa=min(2,d+q)-min(2,d)
                    assert b<=2 and kappa<=2 and 4-b-kappa>=0
                    if b+kappa>2:found.setdefault((q,b,d,kappa),set()).add(tuple(sorted(ds)))
    expected={(z['q'],z['b'],z['d'],z['kappa']):set(map(tuple,z['degree_multisets'])) for z in cert['r7_exceptions']}
    assert found==expected
    assert {key:len(vals) for key,vals in found.items()}=={(2,1,0,2):5,(2,2,0,2):1,(3,1,0,2):3,(4,1,0,2):1}
    # Independently derive root-local frames using immutable algebraic rotations.
    # These are free-term identities, not access calls on a concrete BST.
    def L(t):
        k,a,(j,b,c)=t
        return (j,(k,a,b),c)
    def R(t):
        k,(j,a,b),c=t
        return (j,a,(k,b,c))
    def tup(t):return tuple(map(tup,t)) if isinstance(t,list) else t
    def flat(t):return [t] if isinstance(t,str) else flat(t[1])+[t[0]]+flat(t[2])
    for name,frames in cert['OR35_frames'].items():
        before,after=map(tup,frames)
        if name=='LL':actual=R(R(before))
        elif name=='RR':actual=L(L(before))
        elif name=='LR':actual=R((before[0],L(before[1]),before[2]))
        elif name=='RL':actual=L((before[0],before[1],R(before[2])))
        elif name=='L':actual=R(before)
        else:actual=L(before)
        assert actual==after and flat(before)==flat(after)
    guard=(F/'H1_CONTEXT_BARRIER_GUARD.md').read_text()
    assert 'cannot cross a nonempty inactive' in guard
    assert 'parent in the fixed entry P0' in guard
    # New reservation composition: reverse component walks, not producer forward walks.
    hist=B/'SOURCE_JOINT_REPAIR_03'
    src=read(hist/'actual_monotone_return_source.json');own=read(hist/'actual_auxiliary_owner_extension.json')
    def mp(xs):return {tuple(z['demand']):tuple(z['unit']) for z in xs}
    reg=read(F/'claim_reservation_composition.json')
    for path,h in reg['input_sha256'].items():assert sha(P/path)==h
    h=mp(src['funding']['full_h']);prior=mp(own['old_canonical_effective_a0']);now=mp(own['full_allocation'])
    bound=mp(reg['claim_bound_reservations']);locked=prior|bound
    assert all(locked[d]==u for d,u in prior.items()) and len(set(locked.values()))==len(locked)
    reverse_h={u:d for d,u in h.items()};answer=dict(locked);unused=set(h.values())-set(locked.values())
    for endpoint in sorted(unused):
        u=endpoint;seen=set()
        while u in reverse_h:
            assert u not in seen;seen.add(u);d=reverse_h[u]
            if d not in locked:
                assert d not in answer;answer[d]=endpoint;break
            u=locked[d]
    assert answer==now and len(answer)==36 and len(set(answer.values()))==36
    assert reg['current_frozen_input_rolled_back'] is False
    # Status discipline: compare interface verification with actual universal targets.
    docs=['SOURCE_SPEC.md','DEGREE_LAYER_CHANNEL_THEOREM.md','SEVEN_KEY_EXCEPTION_CLASSIFICATION.md',
      'ONE_EVENT_RUN_CONFINEMENT.md','H1_CONTEXT_BARRIER_GUARD.md',
      'CLAIM_BOUND_RESERVATION_COMPATIBILITY.md','CREDIT_BRIDGE_ATTACK.md']
    report={'status':'PASS_WITH_EXACT_SCOPE','source_queries':0,'source_engine_calls':0,
      'mechanical_checks':['complete integer path-degree partition at r7',
        'independently reconstructed six free-term root-local frames',
        'guarded contraction requirements retained',
        'reverse-component verification of new claim-reservation composition',
        'current complete36 map unchanged','original dependency/controller hashes'],
      'mathematical_derivations_reviewed':['threshold status alternation and distinct actual birth bits',
        'degree-layer identity/path budget','seven-key nonexception Type B working10',
        'H1 unique positive target and first-use anonymous pointer argument',
        'source lift with nonempty context barrier','claim-bound full-owner reservation theorem'],
      'not_machine_formalized':['universal induction/geometry of the source theorems',
        'exhaustiveness of all legitimate additional Gamma reservation types',
        'source compensation on exceptional H1 runs'],
      'trust':'distinct static code, same research agent; not external peer review or proof-assistant verification',
      'UCF35':'OPEN','SI34':'REFUTED_IMMUTABLE','source_simple_credit_closed':False,
      'all_Gamma_compatibility_closed':False,
      'input_sha256':{n:sha(F/n) for n in docs+['new_symbolic_certificate.json','claim_reservation_composition.json']}}
    with (F/'independent_new_theorem_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print('NEW_SYMBOLIC_THEOREM_INTERFACES_PASS; EXCEPTIONAL_REPAYMENT_AND_EXTRA_GAMMA_OPEN',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify92_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
