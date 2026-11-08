"""Independent all-color source grammar for both end gaps together."""
import json,time,sys,itertools,hashlib,collections
from pathlib import Path
from audit_verify36 import calc
from audit_verify49 import build,nodes,assert_relation,flip
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def node(t):return isinstance(t,tuple)
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'mixed_both_end_gaps_source_normal_forms.json').read_text());assert not Z['unresolved'];direct={(r['path'],tuple(r['colors'])):r for r in Z['direct_schemas']};helpers={(r['path'],tuple(r['colors'])):r for r in Z['helper_schemas']};seen=set();hseen=set();counts=collections.Counter()
    for d in range(1,5):
        for bits in itertools.product('LR',repeat=d):
            word=''.join(bits);bare,x=build(word)
            for C in itertools.product(range(7),repeat=d+1):
                if any(C[i]>C[i+1] for i in range(d)) or C.count(1)>1 or C.count(5)>1 or 2 not in C or 4 not in C:continue
                colors=tuple('LmFMJzH'[i] for i in C);one=C.index(1) if 1 in C else C.count(0)-.25;last=C.index(5) if 5 in C else len(C)-C.count(6)-.75;f=max(i for i,c in enumerate(C) if c==2);j=C.index(4)
                def payload(v):
                    if node(v):return v[0],payload(v[1]),payload(v[2])
                    k=int(v[1:])
                    if 1 not in C and k==C.count(0):return one,'E','E'
                    if 5 not in C and k==len(C)-C.count(6):return last,'E','E'
                    return 'X'+str(k) if f<k<=j else 'E'
                def project(v):
                    if not node(v):return v
                    k,L,R=v;L=project(L);R=project(R)
                    if k in (one,last):return k,L,R
                    c=C[k]
                    if c==0:assert L=='E';return R
                    if c==6:assert R=='E';return L
                    if c==2:assert nodes(L)<={one};return (one,'E',R) if one in nodes(L) else R
                    if c==4:assert nodes(R)<={last};return (last,L,'E') if last in nodes(R) else L
                    return k,L,R
                old=lambda k:C[k] in (1,3,5);t=payload(bare);actual,h=calc(t,x);s,p=project(t),project(actual);key=word,colors
                if old(bare[0]) and old(x):
                    row=direct[key];seen.add(key);native,h0=calc(s,x);assert h0<=h;label=row['label']
                    if label.startswith('REFLECTED_'):assert_relation(label[len('REFLECTED_'):],flip(s),flip(p),-x,-last)
                    else:assert_relation(label,s,p,x,one)
                    counts[label]+=1
                elif d<=2 and old(bare[0])!=old(x):
                    row=helpers[key];hseen.add(key);target=x if old(x) else p[0];native,h0=calc(s,target);assert native==p and h0<=h==1 and target==row['old_target']
                else:continue
                assert (t,actual,s,p)==tuple(fr(row[k]) for k in ('source','actual_after','projected_source','projected_after'));assert h==row['actual_H'] and h0==row['old_H']
    assert seen==set(direct) and hseen==set(helpers) and len(seen)==54 and len(hseen)==8 and dict(counts)==Z['class_counts'];assert time.process_time()-START<CAP-1
    deps=('BOTH_END_GAPS_SOURCE_CREDIT_THEOREM.md','mixed_both_end_gaps_source_normal_forms.json','mixed_exterior_first_gap_independent_audit.json','first_gap_private_population_independent_audit.json','exterior_private_population_independent_audit.json','first_gap_new_H2_coefficients_independent_audit.json','private_max_pullback_independent_audit.json','native10_complete_independent_audit.json')
    for n in deps[2:]:assert json.loads((B/n).read_text())['status'].startswith('PASS')
    out('both_end_gaps_independent_audit.json',{'status':'PASS_COMPLETE_SIMULTANEOUS_BOTH_END_GAPS_AND_EXTERIOR_SOURCE_CREDIT','direct_new_schemas':54,'helper_new_schemas':8,'class_counts':dict(counts),'method':'independent all-color-product order filtering and zipper rotation identities with arbitrary ordered free payloads','all_finite_private_populations_and_source_lengths':True,'same_word_all_four_active_bands':True,'width':3,'working_bank':9,'source_queries':0,'source_engine_calls':0,'owner_composition':'original C14 E1/E3 licenses remain required','larger_B_or_all_r_claim':False,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}});print(json.dumps({'status':'PASS_BOTH_END_GAPS_AND_EXTERIOR_UNIFORM_SOURCE_CREDIT','new_direct':54,'new_helpers':8,'bank':9,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify52_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
