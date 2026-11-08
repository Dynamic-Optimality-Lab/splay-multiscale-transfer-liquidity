"""Alternate color enumeration and independent zipper mixed-source audit."""
import json,time,sys,itertools,hashlib,collections
from pathlib import Path
from audit_verify36 import calc
from audit_verify49 import build,nodes,assert_relation
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def node(t):return isinstance(t,tuple)
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'mixed_exterior_first_gap_source_normal_forms.json').read_text());assert not Z['unresolved']
    direct={(r['path'],tuple(r['colors'])):r for r in Z['direct_schemas']};helpers={(r['path'],tuple(r['colors'])):r for r in Z['helper_schemas']};seen=set();hseen=set();counts=collections.Counter()
    for d in range(1,5):
        for bits in itertools.product('LR',repeat=d):
            word=''.join(bits);bare,x=build(word)
            for C in itertools.product(range(5),repeat=d+1):
                if any(C[i]>C[i+1] for i in range(d)) or C.count(1)>1 or 2 not in C:continue
                colors=tuple('LmFMH'[i] for i in C);one=C.index(1) if 1 in C else C.count(0)-.5;lastF=max(i for i,v in enumerate(C) if v==2);firstH=C.index(4) if 4 in C else d+1
                def payload(v):
                    if node(v):return v[0],payload(v[1]),payload(v[2])
                    j=int(v[1:])
                    if 1 not in C and j==C.count(0):return one,'E','E'
                    return 'X'+str(j) if lastF<j<=firstH else 'E'
                def project(v):
                    if not node(v):return v
                    k,L,R=v;L=project(L);R=project(R)
                    if k==one:return k,L,R
                    color=C[k]
                    if color==0:assert L=='E';return R
                    if color==4:assert R=='E';return L
                    if color==2:
                        assert nodes(L)<={one}
                        return (one,'E',R) if one in nodes(L) else R
                    return k,L,R
                root=bare[0];isold=lambda k:C[k] in (1,3);t=payload(bare);actual,h=calc(t,x);s,p=project(t),project(actual);key=word,colors
                if isold(root) and isold(x):
                    row=direct[key];seen.add(key);native,h0=calc(s,x);assert h0<=h;assert_relation(row['label'],s,p,x,one);counts[row['label']]+=1
                elif d<=2 and isold(root)!=isold(x):
                    row=helpers[key];hseen.add(key);target=x if isold(x) else p[0];native,h0=calc(s,target);assert native==p and h0<=h==1 and target==row['old_target']
                else:continue
                assert (t,actual,s,p)==tuple(fr(row[k]) for k in ('source','actual_after','projected_source','projected_after'));assert h==row['actual_H'] and h0==row['old_H']
    assert seen==set(direct) and hseen==set(helpers) and len(seen)==79 and len(hseen)==25 and dict(counts)==Z['class_counts']
    deps=('MIXED_EXTERIOR_FIRST_GAP_SOURCE_THEOREM.md','mixed_exterior_first_gap_source_normal_forms.json','first_gap_private_population_independent_audit.json','exterior_private_population_independent_audit.json','first_gap_new_H2_coefficients_independent_audit.json','private_max_pullback_independent_audit.json','native10_complete_independent_audit.json')
    for n in deps[2:]:assert json.loads((B/n).read_text())['status'].startswith('PASS')
    assert time.process_time()-START<CAP-1
    out('mixed_exterior_first_gap_independent_audit.json',{'status':'PASS_COMPLETE_SIMULTANEOUS_EXTERIOR_FIRST_GAP_SOURCE_CREDIT','direct_schemas':len(seen),'helper_schemas':len(hseen),'class_counts':dict(counts),'method':'independent unrestricted color-product enumeration filtered by necessary source order; zipper source calculus; complete free ordered terms, not private-population samples','uniform_private_population_and_source_length':True,'reflection':'last gap with both exterior sides, separately from first gap','width':3,'c':'min(actual whole H,3)','working_bank':9,'no_new_coefficients_or_owner_changes':True,'owner_composition':'original C14 E1/E3 licenses still required','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}})
    print(json.dumps({'status':'PASS_MIXED_FIRST_GAP_EXTERIOR_UNIFORM_THEOREM','direct':79,'helpers':25,'bank':9,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify51_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
