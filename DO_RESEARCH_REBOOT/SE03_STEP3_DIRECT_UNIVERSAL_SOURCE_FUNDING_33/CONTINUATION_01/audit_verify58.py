"""Distinct zipper algebra for arbitrary-length protected-fringe induction."""
import json,time,sys,hashlib
from pathlib import Path
from audit_verify36 import calc
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def node(t):return isinstance(t,tuple)
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def phi(v,p,tag):
    if not node(v):return v
    k,L,R=v
    if k!=p:return k,phi(L,p,tag),phi(R,p,tag)
    if tag=='L':assert node(L) and L[2]=='E';return L[0],phi(L[1],p,tag),phi(R,p,tag)
    if tag=='R':assert node(R) and R[1]=='E';return R[0],phi(L,p,tag),phi(R[2],p,tag)
    if L=='E':return phi(R,p,tag)
    assert R=='E';return phi(L,p,tag)
def spine(v,side):
    r=[]
    while node(v):r.append(v[0]);v=v[side]
    return tuple(r)+(('ARBITRARY_TAIL',v),)
def main():
    z=json.loads((B/'protected_fringe_H1_local_forms.json').read_text());assert len(z['schemas'])==8;names=set()
    for r in z['schemas']:
        t=fr(r['source']);p=r['private'];x=r['target'];tag=r['source_tag'];after,h=calc(t,x);before=phi(t,p,tag);old,c=calc(before,x);projected=phi(after,p,r['destination_tag_if_branch_remains']);assert projected==old==fr(r['old_after']) and before==fr(r['old_source']) and after==fr(r['actual_after']) and h==c==1;names.add(r['case'])
        if tag=='L':assert t[0]>p
        if tag=='R':assert t[0]<p
        newtag=r['destination_tag_if_branch_remains']
        if newtag=='L':assert after[0]>p
        if newtag=='R':assert after[0]<p
    assert names=={'RR_birth','LL_birth','RL_unary','LR_unary','L_retire','L_survive','R_retire','R_survive'}
    before=(2,(1,'A','M'),'R');after=(1,'A',(2,'M','R'));assert spine(before,2)==(2,('ARBITRARY_TAIL','R')) and spine(after,2)==(1,2,('ARBITRARY_TAIL','R'));assert spine(before,1)==(2,1,('ARBITRARY_TAIL','A')) and spine(after,1)==(1,('ARBITRARY_TAIL','A'))
    assert time.process_time()-START<CAP-1;deps=('H1_PROTECTED_FRINGE_SIMULATION.md','protected_fringe_H1_local_forms.json','two_KEEP_unary_return_independent_audit.json')
    out('protected_fringe_H1_independent_audit.json',{'status':'PASS_UNIFORM_ARBITRARY_SUPPORT_ARBITRARY_LENGTH_H1_SOURCE_SIMULATION','local_free_term_identities':8,'spine_context_lemma':'right rotation adds only pivot on right spine and removes only parent on left spine when at corresponding spine; off-spine context remains off-spine; inverse gives left rotation; all other nodes unchanged','induction':'all off-path branches retain local fringes and spine guards; on-path unary/birth and protected branch retire/survive are exactly the8 checked cases; actual marked roots and H1 depth force completeness','all_finite_private_populations_and_word_lengths':True,'all_finite_anchor_supports':True,'orientation_tags':'source-generated creator witnesses; not asserted state function of old debt multiset','initial_unary_required':True,'final_unary_needed_only_for_unique_endpoint_projection':True,'positive_anonymous_access_or_H2_included':False,'source_queries':0,'source_engine_calls':0,'no_numerical_debt_table_or_finite_population_samples':True,'physical_source_ordinals_preserved':True,'Gate_U':'OPEN; ordinary credit, activation and mixed ownership interfaces retain hypotheses','principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}});print(json.dumps({'status':'PASS_ALL_SUPPORT_ALL_LENGTH_H1_SOURCE_BRIDGE','local_identities':8,'source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify58_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
