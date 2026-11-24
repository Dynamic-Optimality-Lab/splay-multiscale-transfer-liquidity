"""Independent original-tree, graph, potential, cycle, frontier and dual verification.

No current producer/kernel/teacher/learner/parametric/symbolic imports. Immutable
tree primitives are imported read-only from the older sealed verifier.
"""
import gzip
import importlib.util
import itertools
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;START=time.process_time()
spec=importlib.util.spec_from_file_location('gso_independent_immutable',ROOT/'DO_RESEARCH_REBOOT/COVER_FLOW_AUDIT_20261121_V001/verify.py')
IMM=importlib.util.module_from_spec(spec);sys.modules[spec.name]=IMM;spec.loader.exec_module(IMM)


def read(p):
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8')) as f:return json.load(f)


def write(p,x):p.write_text(json.dumps(x,indent=2),encoding='utf-8')


def tree(s):
    values={None:None};ch={int(k):v for k,v in s['children'].items()};stack=[(s['root'],False)]
    while stack:
        k,done=stack.pop()
        if done:
            l,r=ch[k];values[k]=IMM.node(k,values[l],values[r])
        else:stack.append((k,True));stack.extend((c,False) for c in ch[k] if c is not None)
    return values[s['root']]


def state(t):
    out={};stack=[t]
    while stack:
        v=stack.pop();out[str(v.k)]=[v.l.k if v.l else None,v.r.k if v.r else None];stack.extend(x for x in (v.l,v.r) if x)
    return {'root':t.k,'children':out}


def encode(t,n):
    s=state(t);return tuple([s['root']]+[x or 0 for k in range(1,n+1) for x in s['children'][str(k)]])


def graph_tree(raw):
    return tree({'root':raw[0],'children':{str(k):[raw[2*k-1] or None,raw[2*k] or None] for k in range(1,(len(raw)+1)//2)}})


def insert(t,k):
    if t is None:return IMM.node(k)
    return IMM.node(t.k,insert(t.l,k),t.r) if k<t.k else IMM.node(t.k,t.l,insert(t.r,k))


def describe(t):
    depth={};parent={t.k:None};stack=[(t,0)]
    while stack:
        v,d=stack.pop();depth[v.k]=d
        for c in (v.l,v.r):
            if c:parent[c.k]=v.k;stack.append((c,d+1))
    return depth,parent


def features(A,B):
    da,pa=describe(A);db,pb=describe(B);out=[]
    for r in (1,2,3):
        for depth,parent in ((da,pb),(db,pa)):
            marked={k for k,d in depth.items() if d<r};ancestors=set()
            for k in marked:
                while k is not None and k not in ancestors:ancestors.add(k);k=parent[k]
            out.append(len(ancestors)-len(marked))
    return out+[x*int(A.k==B.k) for x in out]


def splay(t,x,actor=None,op=None,records=None):
    def emit(step,bit,typ,child,parent,demoted):
        if records is not None:records.append({'id':[actor,op,step,bit],'type':typ,'promoted':child.k,'demoted':parent.k,'old_child_span':[child.lo,child.hi],'new_demoted_span':[demoted.lo,demoted.hi]})
    return IMM.rebuild(t,x,emit,lambda *args:None)


def verify_graph(path):
    g=read(path);n=g['support'];trees=[graph_tree(t) for t in g['trees']]
    enumerated=set()
    for perm in itertools.permutations(range(1,n+1)):
        t=None
        for k in perm:t=insert(t,k)
        enumerated.add(encode(t,n))
    assert enumerated==set(map(tuple,g['trees']))
    lookup={tuple(t):i for i,t in enumerate(g['trees'])};trans=[]
    for t in trees:
        row=[]
        for x in range(1,n+1):result,d=splay(t,x);row.append([lookup[encode(result,n)],d])
        trans.append(row)
    assert trans==g['tree_transitions']
    pairs=g['pairs'];index={tuple(p):i for i,p in enumerate(pairs)};assert len(index)==len(pairs);T=len(trees)
    for i in range(T):assert pairs[i]==[i,i] and g['parents'][i] is None
    for i in range(T,len(pairs)):
        p,mode,x=g['parents'][i];assert p<i;aa,bb=pairs[p]
        expected=[trans[aa][x-1][0],trans[bb][x-1][0] if mode=='K' else bb];assert pairs[i]==expected
    edge=0
    for i,(aa,bb) in enumerate(pairs):
        assert g['features'][i]==features(trees[aa],trees[bb])
        for x in range(1,n+1):
            a,da=trans[aa][x-1];b,db=trans[bb][x-1]
            for mode,v,q in [('D',bb,0),('K',b,db//2)]:
                assert g['edges'][edge]==[i,index[(a,v)],(da+1)//2,q,mode,x];edge+=1
    assert edge==len(g['edges'])
    rr=[e[0] for e in g['edges']];cc=[e[1] for e in g['edges']]
    matrix=coo_matrix(([1]*len(rr),(rr,cc)),shape=(len(pairs),len(pairs))).tocsr()
    count,comp=connected_components(matrix,directed=True,connection='strong')
    assert g['recurrent_edges']==[i for i,e in enumerate(g['edges']) if comp[e[0]]==comp[e[1]]]
    certificates=read(path.parent/f'certificates_{n}.json.gz');checks=0
    trials=list(certificates['trials'].values())
    best=certificates['optimum'];assert best['status']=='FINITE_EXACT_OPTIMUM';trials.append(best['upper_certificate'])
    for cert in trials:
        C=Fraction(cert['C'])
        if cert['status']=='FINITE_EXACT_POTENTIAL':
            p=cert['potential_numerators'];den=cert['potential_denominator'];assert den==C.denominator and len(p)==len(pairs)
            assert all(den*q+p[v]-p[u]<=C.numerator*a for u,v,a,q,_,_ in g['edges'])
        else:
            ids=cert['cycle'];assert ids
            assert all(g['edges'][ids[j]][1]==g['edges'][ids[(j+1)%len(ids)]][0] for j in range(len(ids)))
            aa=sum(g['edges'][j][2] for j in ids);qq=sum(g['edges'][j][3] for j in ids);assert qq>C*aa
        checks+=1
    ids=best['attaining_cycle']
    if ids:
        assert all(g['edges'][ids[j]][1]==g['edges'][ids[(j+1)%len(ids)]][0] for j in range(len(ids)))
        aa=sum(g['edges'][j][2] for j in ids);qq=sum(g['edges'][j][3] for j in ids);assert aa>0 and Fraction(qq,aa)==Fraction(best['C'])
    print('verified graph',n,len(pairs),len(g['edges']),best['C'],flush=True)
    return {'support':n,'BST_universe':len(trees),'reachable_pairs':len(pairs),'all_original_edges':len(g['edges']),'recurrent_edges':len(g['recurrent_edges']),'exact_C':best['C'],'certificates':checks,'independent_feature_definition':'literal B/A ancestor union of the marked depth frontier'}


def verify_source(path):
    w=read(path);s=w['source'];initial={a:tree(s['initial_'+a]) for a in ('A','B')};keys=set(map(int,s['initial_A']['children']))
    assert keys==set(map(int,s['initial_B']['children']))
    diagonal=s.get('diagonal')
    if diagonal is None:assert s['initial_A']==s['initial_B'] and not s.get('prefix');diagonal=s['initial_A']
    reach={a:tree(diagonal) for a in ('A','B')}
    for mode,x in s.get('prefix',[]):
        for actor in ('A','B') if mode=='K' else ('A',):reach[actor],_=splay(reach[actor],x)
    assert all(state(reach[a])==s['initial_'+a] for a in ('A','B'))
    selected={row['id'][1]:row for row in w.get('rows',[])};trees=initial.copy();A=Q=rot=0
    genuine=set();previous=initial['B'].k
    for mode,x in s['operations']:
        if mode=='K':
            if x!=previous:genuine.add(x)
            previous=x
    _,parentB=describe(initial['B']);S=set()
    for x in genuine:
        while x is not None:S.add(x);x=parentB[x]
    for op,(mode,x) in enumerate(s['operations'],1):
        row=selected.get(op);bits=[]
        if row is not None:before=features(trees['A'],trees['B'])
        trees['A'],da=splay(trees['A'],x,'A',op,bits if row is not None else None);db=0
        if mode=='K':
            if trees['B'].k!=x:
                cur=trees['B'];pathkeys=[]
                while True:
                    pathkeys.append(cur.k)
                    if cur.k==x:break
                    cur=cur.l if x<cur.k else cur.r
                assert set(pathkeys)<=S
            trees['B'],db=splay(trees['B'],x,'B',op,bits if row is not None else None)
        aa=(da+1)//2;qq=db//2;A+=aa;Q+=qq;rot+=da+db
        if row is not None:
            after=features(trees['A'],trees['B']);assert row['before']==before and row['after']==after
            assert row['delta']==[v-u for u,v in zip(before,after)] and (row['a'],row['q'])==(aa,qq)
            assert row['bits']==bits and (row['mode'],row['target'])==(mode,x)
    assert all(state(trees[a])==s['initial_'+a] for a in ('A','B'))
    for key,value in [('A',A),('Q_B',Q),('period_rotations',rot)]:
        if key in w:assert w[key]==value
    if s.get('expected_A') is not None:assert A==s['expected_A']
    if s.get('expected_Q') is not None:assert Q==s['expected_Q']
    return {'file':path.name,'source_name':s['name'],'physical_keys':len(keys),'original_carrier_S':len(S),'operations':len(s['operations']),'period_rotations':rot,'A':A,'Q_B':Q,'selected_rows':len(selected),'full_pair_closure':True,'prefix_checked':True,'all_selected_original_bits':True}


def verify_dual(out):
    d=read(out/'PARAMETRIC_DUAL_CERTIFICATE.json');s=read(out/'SYMBOLIC_FRONTIER_IDENTITIES.json')
    assert d['affine_slopes']==[r['slopes'] for r in s['rows']] and d['affine_intercepts']==[r['intercepts'] for r in s['rows']]
    weights=list(map(Fraction,d['equality_multipliers']));a=d['terminal_q_slope'];M=d['affine_slopes']
    assert all(sum(w*row[i] for w,row in zip(weights,M))==a[i] for i in range(12))
    combined=a[:]
    for term in d['nonnegative_dual_rows']:
        w=Fraction(term['weight']);assert w>=0;row=M[d['source_templates'].index(term['template'])]
        combined=[v+w*term['equality_orientation']*z for v,z in zip(combined,row)]
    assert combined==[0]*12 and Fraction(d['combined_rhs'])==-1
    def rank(rows):
        x=[list(map(Fraction,r)) for r in rows];at=0
        for col in range(12):
            pivot=next((j for j in range(at,len(x)) if x[j][col]),None)
            if pivot is None:continue
            x[at],x[pivot]=x[pivot],x[at];v=x[at][col];x[at]=[z/v for z in x[at]]
            for j in range(at+1,len(x)):
                v=x[j][col]
                if v:x[j]=[a-v*b for a,b in zip(x[j],x[at])]
            at+=1
            if at==len(x):break
        return at
    core=d['optimized_universal_obstruction_core'];assert core['size']==5
    subset=[M[i] for i in core['template_indices']];ww=list(map(Fraction,core['multipliers']))
    assert all(sum(w*r[i] for w,r in zip(ww,subset))==a[i] for i in range(12))
    for k in range(5):
        for ids in itertools.combinations(range(7),k):
            sub=[M[i] for i in ids];assert rank(sub+[a])>rank(sub)
    return {'exact_dual_arithmetic':True,'nonnegative_inequality_weights':True,'contradiction':'0<=-1','minimum_recorded_template_core':5,'scope':'Universal row provenance is the separate symbolic state identity and explicit original-source spine proof, not finite interpolation. Core minimality is only among the seven recorded template rows.'}


def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='run_001');parser.add_argument('--no-write',action='store_true');args=parser.parse_args();out=HERE/args.output
    assert args.no_write or not (HERE/'FINAL_MANIFEST.json').exists()
    graphs=[verify_graph(p) for p in sorted(out.glob('graph_*.json.gz'))]
    sources=[]
    for p in sorted([*out.glob('*.json.gz'),*out.glob('*.json')]):
        raw=read(p)
        if isinstance(raw,dict) and 'source' in raw and 'initial_A' in raw['source']:
            sources.append(verify_source(p));assert time.process_time()-START<=360
    dual=verify_dual(out)
    result={'passed':True,'graphs':graphs,'sources':sources,'source_witness_files':len(sources),'distinct_source_names':len({r['source_name'] for r in sources}),'all_graph_edges':sum(r['all_original_edges'] for r in graphs),'source_original_operations':sum(r['operations'] for r in sources),'source_period_rotations':sum(r['period_rotations'] for r in sources),'selected_source_rows':sum(r['selected_rows'] for r in sources),'exact_dual':dual,'cpu_seconds':time.process_time()-START,'independence':'Immutable full tree rotations, insertion-permutation BST enumeration, literal marked-frontier ancestor closure and independent SCC implementation. Imports no current engine producer. Same-agent code independence, not peer review or a formal BST-source proof.'}
    if not args.no_write:write(out/'INDEPENDENT_VERIFICATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('graphs','sources')}))


if __name__=='__main__':main()
