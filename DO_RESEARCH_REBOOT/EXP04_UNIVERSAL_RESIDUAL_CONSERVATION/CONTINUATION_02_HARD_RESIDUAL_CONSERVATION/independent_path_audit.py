from fast_physics import *
from types import SimpleNamespace
sys.path.insert(0,str(REPO/'python'))
from independent import splay as ind


def checked_access(tree,immutable,x,other,actor):
    before=immutable;nodes=[];cur=before
    while cur[0]=='node':
        nodes.append(cur)
        if cur[1]==x:break
        cur=cur[2] if x<cur[1] else cur[3]
    path=[z[1] for z in nodes];assert path==tree.path(x)
    pathset=set(path);oldfringes=[]
    for z in nodes:
        for child in z[2:]:
            if child[0]=='node' and child[1] not in pathset:oldfringes.append(id(child))
    tree.touched=set();steps,q,G,details=tree.splay(x,other,actor)
    after,ev=ind.trace(before,x)
    assert tree.touched<=pathset and tree.root==after[1]==x
    assert steps==len(ev) and [e[0] for e in ev]==[d[0] for d in details]
    assert q==sum(e[0]!='ZIG' for e in ev)
    visited=set();newfringes=[];stack=[(after,0)]
    while stack:
        z,parent=stack.pop();_,k,l,rr=z;assert k in pathset and k not in visited;visited.add(k)
        assert tree.p[k]==parent
        assert tree.l[k]==(l[1] if l[0]=='node' else 0)
        assert tree.r[k]==(rr[1] if rr[0]=='node' else 0)
        for child in (l,rr):
            if child[0]!='node':continue
            assert tree.p[child[1]]==k
            if child[1] in pathset:stack.append((child,k))
            else:newfringes.append(id(child))
    assert visited==pathset and Counter(newfringes)==Counter(oldfringes)
    # Every modified child field was checked, every off-path field stayed
    # unchanged, and every immutable off-path component is the same object.
    # With initial full equality, this proves COMPLETE post-state equality.
    return after,steps,q,G,len(pathset),len(oldfringes)


def check(s):
    a=FullTree(s['initial_A']);b=FullTree(s['initial_B']);view=SimpleNamespace(ind=ind)
    aa=Replay.as_tuple(view,Tree(s['initial_A']));bb=aa if s['initial_A']==s['initial_B'] else Replay.as_tuple(view,Tree(s['initial_B']))
    A=Q=stepcount=pathnodes=fringes=0
    for t,(tag,x) in enumerate(s['operations'],1):
        aa,steps,_,_,p,f=checked_access(a,aa,x,b,'A');A+=steps;stepcount+=steps;pathnodes+=p;fringes+=f
        if tag=='K':
            bb,steps,q,_,p,f=checked_access(b,bb,x,a,'B');Q+=q;stepcount+=steps;pathnodes+=p;fringes+=f
    assert A==s['A'] and Q==s['Q_B']
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    return {'source':s['name'],'population':a.n,'original_operations':len(s['operations']),
        'A':A,'Q_B':Q,'independent_StepEv_cases':stepcount,'checked_path_nodes':pathnodes,
        'unchanged_complete_fringe_identity_checks':fringes,
        'all_complete_intermediate_states_equal_by_exact_edge_and_fringe_induction':True,
        'probabilistic_hash_equality_used':False,'paired_closure':True}


if __name__=='__main__':
    meter=Meter('independent_path_and_fringe_audit');out=[]
    sources=json.loads((ROOT/'DILATED_SOURCES.json').read_text())+[json.loads((ROOT/'ADAPTIVE_LIFT_SOURCE.json').read_text())]
    for s in sources:
        z=check(s);out.append(z);write('INDEPENDENT_PATH_AND_FRINGE_RESULTS.json',out)
        print('PASS',s['name'],z['population'],z['original_operations'],'exact complete-state inductions',flush=True)
    meter.success=True;meter.details['sources']=len(out)
