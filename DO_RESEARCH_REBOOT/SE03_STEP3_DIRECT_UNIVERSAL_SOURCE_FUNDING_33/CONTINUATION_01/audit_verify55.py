"""Independent insertion-permutation grammar and zipper proof of unary lifting."""
import json,time,sys,itertools,hashlib,collections
from pathlib import Path
from audit_verify36 import calc
from audit_verify49 import assert_relation
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def node(t):return isinstance(t,tuple)
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def insert(t,k):
    if t is None:return k,None,None
    return (t[0],insert(t[1],k),t[2]) if k<t[0] else (t[0],t[1],insert(t[2],k))
def label_gaps(t):
    j=0
    def walk(v):
        nonlocal j
        if v is None:g='G'+str(j);j+=1;return g
        return v[0],walk(v[1]),walk(v[2])
    return walk(t)
def skeleton(t):
    j=0
    def walk(v):
        nonlocal j
        if not node(v):g='G'+str(j);j+=1;return g
        return v[0],walk(v[1]),walk(v[2])
    return walk(t)
def route(t,x):
    r=[]
    while True:
        r.append(t[0])
        if t[0]==x:return r
        t=t[1 if x<t[0] else 2];assert node(t)
def main():
    Z=json.loads((B/'unary_boundary_LOW_source_normal_forms.json').read_text());assert Z['enumeration_complete'] and not Z['unresolved'];rows={}
    for r in Z['schemas']:
        key=(skeleton(fr(r['source'])),r['helper'],r['target'],r['private_mask'],r['leaf_mask']);assert key not in rows;rows[key]=r
    seen=set();counts=collections.Counter();templates=0
    for m in range(2,6):
        shapes=set()
        for perm in itertools.permutations(range(m)):
            t=None
            for k in perm:t=insert(t,k)
            shapes.add(label_gaps(t))
        assert len(shapes)=={2:2,3:5,4:14,5:42}[m]
        for t in shapes:
            g=t[0]
            for x in range(m):
                if x==g:continue
                choices=[]
                r=route(t,x)
                if len(r)-1<=4 and set(r)==set(range(m)):choices.append(None)
                for y in range(m):
                    if y==g or len(route(t,y))>3:continue
                    mid,h1=calc(t,y)
                    if x==y or len(route(mid,x))>3:continue
                    if set(route(t,y))|set(route(mid,x))==set(range(m)):choices.append(y)
                for y in choices:
                    templates+=1
                    for oldmask in range(1<<m):
                        if not oldmask>>g&1 or not oldmask>>x&1 or oldmask==(1<<m)-1:continue
                        P=((1<<m)-1)^oldmask
                        def project(v):
                            if not node(v):return v
                            L,R=project(v[1]),project(v[2])
                            if L is None or R is None:return None
                            if P>>v[0]&1:
                                if L=='E':return R
                                if R=='E':return L
                                return None
                            return v[0],L,R
                        for flags in range(1<<(m+1)):
                            def bind(v):
                                if not node(v):i=int(v[1:]);return 'X'+str(i) if flags>>i&1 else 'E'
                                return v[0],bind(v[1]),bind(v[2])
                            source=bind(t);s=project(source)
                            if s is None:continue
                            if y is None:after,H=calc(source,x)
                            else:mid,h1=calc(source,y);after,h2=calc(mid,x);assert h1==h2==1;H=2
                            p=project(after)
                            if p is None:continue
                            key=(t,y,x,P,flags);r=rows[key];seen.add(key);assert (source,after,s,p)==tuple(fr(r[k]) for k in ('source','actual_after','projected_source','projected_after'));assert H==r['actual_H'];kind=r['class'];counts[kind]+=1
                            if kind=='COMPARISON_WORD':
                                a,h0=calc(s,r['comparison']['helper']);a,hx=calc(a,x);assert a==p and h0+hx==r['old_H']<=H
                            else:
                                native,h0=calc(s,x);assert h0==r['old_H']<=H
                                if kind=='GENERIC_RLL':assert_relation('RLL_MIN_ROOT',s,p,x,s[0])
                                elif kind=='GENERIC_LRR':assert_relation('LRR_MIN_LEFT',s,p,x,s[1][0])
                                else:assert_relation(kind,s,p,x,-100)
    assert seen==set(rows) and len(rows)==2992 and templates==60 and dict(counts)==Z['class_counts'];assert time.process_time()-START<CAP-1
    deps=('UNARY_BOUNDARY_SOURCE_CREDIT_THEOREM.md','unary_boundary_LOW_source_normal_forms.json','general_RLL_LRR_coefficients_independent_audit.json','first_gap_new_H2_coefficients_independent_audit.json','private_max_pullback_independent_audit.json','native10_complete_independent_audit.json')
    for n in deps[2:]:assert json.loads((B/n).read_text())['status'].startswith('PASS')
    out('unary_boundary_independent_audit.json',{'status':'PASS_COMPLETE_ARBITRARY_GAP_UNARY_BOUNDARY_SOURCE_CREDIT','source_templates':templates,'free_term_schemas':len(rows),'class_counts':dict(counts),'method':'all insertion permutations generate all ordered skeletons (preorder is an insertion witness), independent old/private complement coloring and zipper source identities','uniform_private_population_all_gaps_and_source_length':True,'intermediate_anonymous_branching_allowed':True,'boundary_anonymous_branching_allowed':False,'ten_anchor_coefficient_scope':True,'geometry_general_n':'conditional on corresponding ordinary/reassociation/HIGH laws, not proved coefficients for all n','width':3,'working_bank':9,'original_owner_composition_conditional':True,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}});print(json.dumps({'status':'PASS_UNARY_BOUNDARY_UNIFORM_SOURCE_CREDIT','templates':60,'schemas':2992,'bank':9,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify55_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
