"""Complete the SAME root-return mechanism's exact conservation diagnostic.

No new source search or witness. Uses the frozen FE01 source H, checks every
increment against the already two-engine-verified PG physical transitions,
and exposes the absent A/B coupling without treating an identity as a proof.
"""
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PG=HERE.parent/'route_c_pf_positive_gap_closure_20261101_v001'
FE=HERE.parent/'route_c_fe01_first_entry_20261101_v001'
checks=Counter()


def ck(v,label):
    if not v:raise AssertionError(label)
    checks[label]+=1
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def path(t,y):
    p=[]
    while t is not None:
        p.append(t)
        if t[0]==y:return p
        t=t[1 if y<t[0] else 2]
    raise AssertionError('present key')
def depth(t,y):return len(path(t,y))-1


spec=importlib.util.spec_from_file_location('frozen_exact_H',FE/'source_first_entry.py')
inherited=importlib.util.module_from_spec(spec);spec.loader.exec_module(inherited)


def analyze(rows,side):
    N=len(rows);support={r['key'] for r in rows};occ=defaultdict(list)
    for j,r in enumerate(rows):occ[r['key']].append(j)
    results={}
    for y,indices in occ.items():
        for at,j in enumerate(indices):
            prev=indices[at-1];L=(j-prev)%N or N;departure=(prev+1)%N
            source=rows[departure]['source_'+side]
            epsilon=inherited.profile(source,rows[departure]['key'],y)['H']
            ck(epsilon==depth(rows[departure]['destination_'+side],y) and epsilon in [1,2],
               'exact departure epsilon from source H agrees with verified physical output')
            eta=1-epsilon//2;terms=[]
            for offset in range(2,L):
                t=(prev+offset)%N;r=rows[t];T=r['source_'+side]
                before=depth(T,y);after_source=inherited.profile(T,r['key'],y)['H']
                after_actual=depth(r['destination_'+side],y)
                ck(after_source==after_actual,'every exact return increment agrees with verified original transition')
                delta=after_source-before;loss=2-delta
                ck(loss>=0,'source +2 displacement yields nonnegative gain deficit')
                terms.append(dict(block=t,key=y,before_depth=before,source_H=after_source,
                                  actual_shift=delta,gain_deficit=loss))
            K=sum(t['gain_deficit'] for t in terms)
            actual_depth=depth(rows[j]['source_'+side],y)
            ck(actual_depth==epsilon+2*(L-2)-K,'exact source telescoping return-depth reconstruction')
            beta=(K+1)//2 if epsilon==2 else K//2
            ck(beta>=0 and actual_depth//2==L-1-eta-beta,'exact parity-correct return-double loss identity')
            results[j]=dict(block=j,key=y,previous_same_block=prev,L=L,epsilon=epsilon,eta=eta,
                intermediate_terms=terms,K=K,beta=beta,pre_access_depth=actual_depth,
                double_count=actual_depth//2,zig=actual_depth%2)
    ordered=[results[j] for j in range(N)];M=(len(support)-1)*N
    q=sum(r['double_count'] for r in ordered);z=sum(r['zig'] for r in ordered)
    E=sum(r['eta'] for r in ordered);K=sum(r['K'] for r in ordered);B=sum(r['beta'] for r in ordered)
    ck(q==M-E-B,'exact summed source-return identity')
    all_terms=[(t['block'],t['key']) for r in ordered for t in r['intermediate_terms']]
    expected={(t,y) for t,r in enumerate(rows) for y in support
              if y not in [r['key'],rows[t-1]['key']]}
    ck(len(all_terms)==len(set(all_terms)) and set(all_terms)==expected,
       'each intermediate tracked-key source occurrence counted exactly once')
    ck(K==2*N*(len(support)-1)-2*q-z-E,'column closure reduces deficit sum to the same exact identity')
    return dict(side=side,rows=ordered,M=M,double_count=q,zigs=z,sum_eta=E,sum_K=K,sum_beta=B,
                return_loss=E+B,StepEv_total=q+z)


def main():
    audit=read(HERE/'independent_audit.json');pg=read(PG/'closed_source_certificate.json')
    cert=read(HERE/'root_return_certificate.json')
    ck(audit['status']=='PASS' and audit['root_return_certificate_sha256']==sha(HERE/'root_return_certificate.json'),
       'new root audit passed on the exact fixed source certificate')
    ck(cert['original_PG_sha256']==sha(PG/'closed_source_certificate.json'),'physical transition provenance unchanged')
    out={}
    for orientation,rows in [('ordinary',pg['ordinary_rows']),('reflected',pg['reflected_rows'])]:
        A=analyze(rows,'A');B=analyze(rows,'B');M=A['M']
        R_A=A['return_loss']-A['zigs'];R_B=B['return_loss']
        ck(A['StepEv_total']==25 and B['double_count']==22,'exact A/B source-cost translations')
        ck(M-R_A==25 and M-R_B==22,'paired return-loss cost identities')
        ck(2*R_A-R_B-M==22-50==-28,'paired conservation diagnostic is exactly source signed cost')
        out[orientation]=dict(A=A,B=B,R_A=R_A,R_B=R_B,Q_minus_2A=2*R_A-R_B-M)
    save('exact_return_loss_diagnostic.json',dict(status='PASS',checks=dict(checks),total_checks=sum(checks.values()),
        source_PG_sha256=sha(PG/'closed_source_certificate.json'),root_audit_sha256=sha(HERE/'independent_audit.json'),
        original_transitions_already_verified_by_both_engines=True,new_source_engine_calls=0,
        data=out,scope='exact source accounting diagnostic; no joint A/B inequality proved',
        identity_not_counted_as_rigidity_advancement=True,FE02_rigidity='OPEN',FE02_CD='OPEN',
        no_new_witnesses_sizes_or_repetitions=True))
    print(json.dumps(dict(status='PASS',diagnostic_checks=sum(checks.values()),
        ordinary_R_A=out['ordinary']['R_A'],ordinary_R_B=out['ordinary']['R_B'],
        source_margin=-28,joint_source_inequality='NOT PROVED'),indent=2))


if __name__=='__main__':main()
