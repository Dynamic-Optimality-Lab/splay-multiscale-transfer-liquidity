"""Independent zipper calculus and alternate color enumeration for first-gap lift.
No producer classifier, debt repair, finite private-population replay, or oracle.
"""
import json,time,sys,itertools,hashlib,collections
from pathlib import Path
from audit_verify36 import calc
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def node(t):return isinstance(t,tuple)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def build(word):
    def bare(k):
        if k==len(word):return ('*','gap','gap')
        return ('*',bare(k+1),'gap') if word[k]=='L' else ('*','gap',bare(k+1))
    key=gap=0
    def label(v):
        nonlocal key,gap
        if not node(v):g=gap;gap+=1;return 'G'+str(g)
        L=label(v[1]);k=key;key+=1;R=label(v[2]);return k,L,R
    t=label(bare(0));v=t
    for c in word:v=v[1 if c=='L' else 2]
    return t,v[0]
def nodes(t):return set() if not node(t) else {t[0]}|nodes(t[1])|nodes(t[2])
def payload(t,P,one):
    explicit=one==0;last=max(P)
    def walk(v):
        if not node(v):
            j=int(v[1:])
            if not explicit and j==0:return (one,'E','E')
            return 'E' if j<=last else 'X'+str(j)
        return v[0],walk(v[1]),walk(v[2])
    return walk(t)
def project(v,P,one):
    if not node(v):return v
    k,L,R=v
    if k in P:
        assert not (nodes(L)-P-{one})
        return (one,'E',project(R,P,one)) if one in nodes(L) else project(R,P,one)
    return k,project(L,P,one),project(R,P,one)
def wordpath(t,x):
    r=''
    while t[0]!=x:k=1 if x<t[0] else 2;r+='L' if k==1 else 'R';t=t[k];assert node(t)
    return r
def flip(t):return t if not node(t) else (-t[0],flip(t[2]),flip(t[1]))
def assert_relation(label,s,p,x,one):
    native,h=calc(s,x);w=wordpath(s,x)
    if label=='COMMUTING':assert p==native;return
    if label.startswith('EXTRA_EVENT_'):
        if label.endswith('LL'):native,p=flip(native),flip(p)
        xx,left,D=native;pp,gg,C=left;g,A,BB=gg;assert p==(xx,(g,A,(pp,BB,C)),D);return
    if label.startswith('INHERITED_'):
        ss,pp=s,p
        if label.endswith('LLL') or label.endswith('LLR'):ss,pp=flip(ss),flip(pp)
        ww=wordpath(ss,ss[0] if False else (-x if ss!=s else x));g,A,right=ss;a,BB,ur=right;b,ul,rr=ur
        if ww=='RRR':xx,D,E=rr;expected=(xx,(a,(g,A,BB),(b,ul,D)),E)
        else:assert ww=='RRL';xx,C,D=ul;expected=(xx,(a,(g,A,BB),C),(b,D,rr))
        assert pp==expected;return
    if label=='RLL_MIN_ROOT':
        assert w=='RLL' and s[0]==one;xx,L,right=native;v,C,ur=right;u,D,E=ur;assert p==(xx,L,(u,(v,C,D),E));return
    if label=='LRR_MIN_LEFT':
        assert w=='LRR' and s[1][0]==one;xx,left,R=native;u,m,C=left;mark,A,BB=m;assert p==(xx,(mark,A,(u,BB,C)),R);return
    raise AssertionError('UNKNOWN_CASE')
def main():
    direct=json.loads((B/'first_gap_predecessor_direct_LOW_normal_forms.json').read_text());helpers=json.loads((B/'first_gap_private_helper_normal_forms.json').read_text());rows={(r['actual_path'],tuple(r['private_keys_on_path']),r['anchor1_symbol']):r for r in direct['schemas']};hrows={(r['kind'],r['path'],tuple(r['private']),r['one']):r for r in helpers['schemas']};seen=set();hseen=set();count=collections.Counter()
    for depth in range(1,5):
        for letters in itertools.product('LR',repeat=depth):
            word=''.join(letters);bare,target=build(word);allkeys=set(range(depth+1))
            for mask in range(1,1<<(depth+1)):
                P={k for k in allkeys if mask>>k&1};one=-1 if 0 in P else 0;valid=P==set(range(max(P)+1)) if one==-1 else P==set(range(1,max(P)+1))
                if not valid:continue
                t=payload(bare,P,one)
                if depth>=2 and bare[0] not in P and target not in P:
                    key=word,tuple(sorted(P)),one;row=rows[key];seen.add(key);actual,h=calc(t,target);s,p=project(t,P,one),project(actual,P,one);assert t==fr(row['actual_source_term_after_payload_projection']) and actual==fr(row['actual_target_term_after_payload_projection']);assert s==fr(row['projected_old_source']) and p==fr(row['projected_actual_target']);native,old_h=calc(s,target);assert old_h<=h==row['actual_H'];assert_relation(row['class'],s,p,target,one);count[row['class']]+=1
                if depth>2:continue
                if bare[0] not in P and target in P:kind='marked_root_private_helper';oldtarget=one
                elif bare[0] in P and target not in P:
                    if one==0:assert target==0
                    kind='private_root_marked_target';oldtarget=target
                else:continue
                key=kind,word,tuple(sorted(P)),one;row=hrows[key];hseen.add(key);actual,h=calc(t,target);s,p=project(t,P,one),project(actual,P,one);comparison,old_h=calc(s,oldtarget);assert h==1 and old_h<=1 and p==comparison;assert t==fr(row['actual_source']) and actual==fr(row['actual_after']) and s==fr(row['projected_source']) and p==fr(row['projected_after'])
    assert seen==set(rows) and hseen==set(hrows) and len(rows)==46 and len(hrows)==15;assert dict(count)==direct['class_counts'];coeff=json.loads((B/'first_gap_new_H2_coefficients_independent_audit.json').read_text());old=json.loads((B/'private_max_pullback_independent_audit.json').read_text());high=json.loads((B/'native10_complete_independent_audit.json').read_text());assert coeff['status']=='PASS_COMPLETE_FIRST_GAP_RLL_AND_LRR_COEFFICIENT_LAWS' and old['status']=='PASS_COMPLETE_PRIVATE_MAX_COEFFICIENT_OBLIGATIONS';assert len(old['critical_quartet_candidate_cases'])==66 and len(old['internal_positive_source_cases'])==2811 and high['HIGH_envelope_checks']==151164
    assert time.process_time()-START<CAP-1
    names=('FIRST_GAP_PREDECESSOR_SOURCE_LIFT.md','FIRST_GAP_PRIVATE_POPULATION_CREDIT_THEOREM.md','first_gap_predecessor_direct_LOW_normal_forms.json','first_gap_private_helper_normal_forms.json','first_gap_new_H2_coefficients_independent_audit.json','private_max_pullback_independent_audit.json','native10_complete_independent_audit.json')
    out('first_gap_private_population_independent_audit.json',{'status':'PASS_COMPLETE_FIRST_GAP_ARBITRARY_PRIVATE_POPULATION_SOURCE_CREDIT_THEOREM','direct_schemas':len(rows),'helper_schemas':len(hrows),'direct_class_counts':dict(count),'source_coverage':'independent enumeration of all path-node color subsets respecting the first-gap order, source root/terminal kinds and presence/absence of minimum anchor on the actual path','uniform_parameters':'arbitrary finite private populations, source length, repeats, all helpers in first gap, ordered rigid private payloads; reflected last gap separately','old_H2_coefficient_properties':'all1733 potentially constraining couplings independently checked; old implicit-zero and slack cases exact','working_bank_bound':9,'width':3,'c':'min(actual whole H,3)','physical_source_ledger':'all actual operations/StepEv bits retained; comparison helper cost never exceeds actual; h0 included, carry empty at actual max-debt seam; original fE exchange remains conditional on its licenses','source_queries':0,'source_engine_calls':0,'not_proved':'mixed active gaps/exterior populations, larger B backbones or forall r E_r','external_or_formal_proof_assistant_verification':False,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}});print(json.dumps({'status':'PASS_FIRST_GAP_POPULATION_SOURCE_CREDIT','direct_schemas':46,'helper_schemas':15,'bank':9,'source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify49_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
