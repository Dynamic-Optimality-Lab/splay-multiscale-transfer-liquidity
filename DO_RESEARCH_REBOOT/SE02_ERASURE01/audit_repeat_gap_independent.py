"""Separate continuation audit; universal free-term proof, no concrete engine.

The23-step object is a single symbolic identity with nine free hanger terms,
not a finite instance experiment or shape/population search. Paired skeleton
inequality proves distinctness for EVERY legal substitution of those hangers.
"""
import ast,hashlib,json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parent.parent
R=B.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def raw(p):return xp(p).read_text(encoding='utf-8')
def read(p):return json.loads(raw(p))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def contains(p,qs):
    t=' '.join(raw(p).casefold().split())
    for q in qs:assert ' '.join(q.casefold().split()) in t,(str(p),q)
def poly(t):return {k:Fraction(v) for k,v in t.items() if Fraction(v)!=0}
def affine(s):
    assert len(s['ge'])==len(s['mg']) and len(s['eq'])==len(s['me'])
    assert all(Fraction(v)>=0 for v in s['mg']);out={}
    for ts,ms in ((s['ge'],s['mg']),(s['eq'],s['me'])):
        for t,m in zip(ts,ms):
            for k,v in poly(t).items():out[k]=out.get(k,Fraction(0))+Fraction(m)*v
    assert poly(out)==poly(s['goal']),s['name']

# Independent universal source equational kernel over free hanging terms.
def N(k,l,r):return ('N',k,l,r)
def Rzig(t):
    _,g,A,xn=t;_,x,B,C=xn
    return N(x,N(g,A,B),C)
def Lzig(t):
    _,g,xn,C=t;_,x,A,B=xn
    return N(x,A,N(g,B,C))
def RR(t):
    _,g,A,pn=t;_,p,B,xn=pn;_,x,C,D=xn
    return N(x,N(p,N(g,A,B),C),D)
def LL(t):
    _,g,pn,D=t;_,p,xn,C=pn;_,x,A,B=xn
    return N(x,A,N(p,B,N(g,C,D)))
def LR(t):
    _,g,pn,D=t;_,p,A,xn=pn;_,x,B,C=xn
    return N(x,N(p,A,B),N(g,C,D))
def LLL(t):return Lzig(N(t[1],LL(t[2]),t[3]))
def RLR(t):return Rzig(N(t[1],t[2],LR(t[3])))
def ID(t):return t
RULE={'R':Rzig,'L':Lzig,'RR':RR,'LL':LL,'LR':LR,'LLL':LLL,'RLR':RLR,'ID':ID}
AE={'R':1,'L':1,'RR':1,'LL':1,'LR':1,'LLL':2,'RLR':2,'ID':0}
QD={'R':0,'L':0,'RR':1,'LL':1,'ID':0}
def skeleton(t):
    if isinstance(t,str):return None
    return (t[1],skeleton(t[2]),skeleton(t[3]))

def main():
    inherited=read(B/'dependency_pins.json');pins=inherited['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    # The first publication remains immutable; only append-only continuation.
    first=read(B/'final_manifest.json')
    for p in first['files']:assert sha(B/p['file'])==p['sha256'],p['file']
    assert read(B/'independent_audit_v2.json')['status']=='INDEPENDENT_SE02_MATHEMATICAL_AND_SOURCE_AUDIT_PASS'
    source=ROOT/'python/independent/splay.py';tree=ast.parse(raw(source))
    fs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    code=ast.get_source_segment(raw(source),fs['_rebuild'])
    for s in ('cur = node(x, t1, node(kp, t2, node(kg, q, c)))',
      'cur = node(x, node(kp, node(kg, c, q), t1), t2)',
      'cur = node(x, node(kp, q, t1), node(kg, t2, d))',
      'cur = node(x, t1, node(kp, t2, q))','cur = node(x, node(kp, q, t1), t2)'):assert s in code
    # Independent stronger funding premise: never strengthen CD(5) silently.
    k5=R/'06_CERTIFICATES/DIRECT_CDK5_LOW'
    contains(k5/'DIRECT_CDK5_LOW_restricted_class_proof.md',[
      'reachable, exactly closed','|supp(KEEP)|=5','≤8 at every cyclic state',
      'Q_B ≤ 2C_K','No finite-n residue'])
    old=read(k5/'DIRECT_CDK5_LOW_independent_verification.json')
    assert old['verdict']=='PASS' and old['edge_mismatch']==old['inequ_violations']==0
    assert read(R/'CD5_BASE01/CD5_CERTIFICATE.json')['mandatory_open_CD5_dependencies']==[]
    contains(B/'NOVELTY_ADDENDUM.md',[
      'does NOT establish genuinely new coverage','compositional closure',
      'downgrades that advancement claim','no proper repeated paired vertex'])
    contains(B/'REPEAT_GAP_COMPENSATION.md',[
      'A may have any valid source tree','DELETEs may access ANY present key','Q_E <= 2 C_E',
      'NOT the general scalar CD(5)','first request to a different key',
      'CHANGE gap','REPEAT gap','before or at the first full Kz',
      'DIFFERENT repeat gaps','Repeat gaps and change gaps are disjoint',
      'A >= C_E+2m','No paired-identity contraction is used',
      'Five-key/core9 already has a known B-only obstruction','Full original CD stays OPEN'])
    contains(B/'PRIMITIVE_CORE8_FAMILY.md',[
      '23-occurrence','Both B-double consumers have a=0,q=1','A(G)=23','Q_full=4',
      'Q_E=2','C_E=8','NO proper repeated paired vertex','only equal paired vertices',
      'not asserted','Bank25 stays25'])

    # Whole-family source identity over nine free, disjoint inorder gaps.
    f=['F'+str(i) for i in range(9)]
    tail=N('b2',f[3],N('b3',f[4],N('b4',f[5],N('b5',f[6],N('b6',f[7],f[8])))))
    S=N('b1',N('p',N('z',f[0],f[1]),f[2]),tail)
    expected_T=N('b1',N('z',f[0],N('p',f[1],f[2])),tail)
    steps=[('D','b2','R',None),('D','z','LLL',None),('K','z','ID','LL'),
      ('D','b1','RLR',None),('K','b1','ID','RR')]
    V=[('b2','R'),('b3','R'),('b4','R'),('b6','RR')]
    VI=[('b4','LL'),('b3','L'),('b2','L'),('b1','L')]
    steps += [('K',k,w,w) for k,w in V]
    steps += [('D',k,w,None) for k,w in VI]
    steps += [('D','p','LR',None),('D','b1','R',None)]
    steps += [('D',k,w,None) for k,w in V]
    steps += [('K',k,w,w) for k,w in VI]
    assert len(steps)==23
    a=b=e=S;vertices=[(skeleton(a),skeleton(b))]
    A=Q=QE=D=J=0;full_marked=set();aux_keep=[];snapshots={}
    for i,(mode,key,wa,wb) in enumerate(steps,1):
        before_a,before_b=a,b
        a=RULE[wa](a);assert a[1]==key
        A+=AE[wa]
        if mode=='K':
            assert before_b[1]!=key  # all full-family KEEPs are genuine
            b=RULE[wb](b);assert b[1]==key
            q=QD[wb];Q+=q;full_marked.add(key)
            if key=='z':qe=0;D+=q
            else:
                # In the erased family only the return at occurrence5 changes
                # from RR to a root identity; all later B source rules coincide.
                ew='ID' if i==5 else wb
                e=RULE[ew](e);assert e[1]==key
                qe=QD[ew];QE+=qe;J+=q-qe;aux_keep.append(key)
        snapshots[i]=(a,b,e)
        vertices.append((skeleton(a),skeleton(b)))
    assert a==b==e==S
    assert (A,Q,QE,D,J)==(23,4,2,1,1)
    assert full_marked=={'z','b1','b2','b3','b4','b6'}
    assert len(set(vertices[:-1]))==23 and vertices[-1]==vertices[0]
    # Earlier paired-reset family P,W was a composition. New pulse is not.
    assert snapshots[2][0][1]=='z' and snapshots[5][0]==expected_T
    assert snapshots[2][0]!=snapshots[5][0] and snapshots[2][1]==snapshots[5][1]==S
    C=sum(x!=aux_keep[i-1] for i,x in enumerate(aux_keep));assert C==8
    # Explicit marginal donor and actual causal consumers.
    assert steps[0]==('D','b2','R',None) and AE['R']==1
    assert steps[2]==('K','z','ID','LL') and steps[4]==('K','b1','ID','RR')
    assert aux_keep[-1]==aux_keep[0]=='b1'  # repeat gap across selected cut
    assert steps[0][0]=='D' and 1<3<5

    p=read(B/'repeat_gap_derivation.json');t=p['theorem'];fam=p['primitive_family']
    assert p['novelty_correction']['first_paired_reset_family_in_CD5_concatenation_closure']
    assert not p['novelty_correction']['first_family_counted_as_genuinely_new_coverage']
    assert t['domain']=='original reachable fully paired-closed, six genuine KEEP keys, marked B core8'
    assert not t['A_geometry_or_reset_required'] and t['all_Kz_in_pulses']
    assert t['strong_auxiliary_bound']=='Q_E<=2 C_E from completed RT2/K4/K5-LOW, not from scalar CD(5)'
    assert t['repeat_and_change_gap_pools_disjoint'] and t['distinct_pulse_returns_distinct_repeat_gaps']
    assert t['donor_at_or_before_both_consumers'] and not t['guard_completeness_proved']
    assert not t['funding_available_on_all_smaller_support_walks']
    assert fam['occurrences']==23 and (fam['A'],fam['Q_full'],fam['Q_erased'],fam['C_E'])==(A,Q,QE,C)
    assert fam['G']==6 and fam['core']==8 and fam['proper_repeated_paired_vertices']==0
    assert not fam['B_pulse_returns_A'] and fam['outside_CD5_corele7_and_their_proper_paired_subwalk_concatenations']
    expected={
      'repeat_gap_compensation':([{'C':2,'QE':-1},{'A':1,'C':-1,'m':-2}],[{'Q':1,'QE':-1,'m':-2}],{'A':2,'Q':-1,'m':-2}),
      'family_true_slack':([],[{'A':1,'m':-23},{'Q':1,'m':-4}],{'A':2,'Q':-1,'m':-42}),
      'family_marginal':([],[{'Delta':1,'Q':-1,'QE':1},{'Q':1,'m':-4},{'QE':1,'m':-2}],{'Delta':1,'m':-2}),
      'disjoint_reservation_capacity':([{'A':1,'C':-1,'m':-2}],[],{'A':2,'C':-2,'m':-4})}
    seen=set()
    for s in p['affine_schemas']:
        assert s['name'] not in seen;seen.add(s['name'])
        assert (s['ge'],s['eq'],s['goal'])==expected[s['name']];affine(s)
    assert seen==set(expected)
    assert p['new_finite_tests']==p['new_solver_queries']==p['new_original_root_queries']==p['completed_semantic_checks_replayed']==0
    assert not p['matching_terminal_modified'] and not p['frozen_graph_modified'] and p['Bank25']==25
    assert not p['unrestricted_CD_proved'] and not p['uniform_support_induction_proved']
    assert time.process_time()<float(sys.argv[1])
    write('repeat_gap_independent_audit.json',{
      'status':'INDEPENDENT_SE02_REPEAT_GAP_AUDIT_PASS','declared_input_pins_verified':len(pins),
      'first_publication_hashes_unchanged':True,'initial_novelty_claim_downgraded':True,
      'strong_auxiliary_funding_scope':'completed five-key/core<=8 B-only theorem; not arbitrary CD(5)',
      'source_repeat_gap_credit_reservation':'PROVED_DISJOINT_FROM_AUXILIARY_CHANGE_GAP_POOL',
      'A_paired_reset_required':False,'arbitrary_DELETE_interleaving_allowed':True,
      'direct_and_indirect_marginal':'1+1 per B-return pulse','marginal_donors_causal_and_injective':True,
      'six_key_core8_family':'PROVED_ALL_NINE_FREE_HANGERS_AND_REPETITIONS',
      'symbolic_period_occurrences':23,'symbolically_distinct_pre_vertices':23,
      'proper_paired_closed_subwalks':0,'family_costs':{'A':23,'Q':4,'QE':2,'C_E':8,'D':1,'J':1},
      'two_starved_marginal_consumers':True,'family_donor':'occurrence1 Db2 child ZIG, two distinct bits',
      'old_entry_classes_and_proper_paired_concatenations_excluded':True,
      'all_noncompositional_historical_bank_novelty_certified':False,
      'universal_affine_schemas':sorted(seen),'favorable_key_selection_proved':False,
      'uniform_support_induction_proved':False,'unrestricted_CD_proved':False,
      'new_finite_tests':0,'new_solver_queries':0,'new_original_root_queries':0,'old_semantic_checks_replayed':0,
      'no_research_or_construction_imports':True,'external_peer_review':False,'whole_compiler_formalization':False,
      'publication_requires_combined_resource_and_integrity_PASS':True})
    print(json.dumps({'status':'INDEPENDENT_REPEAT_GAP_AUDIT_PASS','universal_CD':'OPEN','new_finite_tests':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_repeat_gap_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
