"""Symbolic rigid-subtree feature identities and learned loop-counter induction."""
import sympy as sp
import z3
from kernel import dump

N=sp.Symbol('N',integer=True,positive=True)
H=('opaque',4,N-1)  # Every original key4..N-1 retained, arbitrary full BST.
V=('vine',0,N)
V1=('shifted_vine',1,N)


def node(k,l=None,r=None):return ('node',k,l,r)


def left_root(t):
    if t==V:return V1
    _,k,l,r=t;assert r and r[0]=='node';_,p,h,rr=r;return node(p,node(k,l,h),rr)


def compare(a,b):
    if a==b:return 0
    if a==N:return 1
    if b==N:return -1
    return -1 if a<b else 1


def top(t,r):
    if t==V:return set(range(r))
    if t==V1:
        return {1} if r==1 else {0,1,2} if r==2 else {0,1,2,3}
    answer=set();stack=[(t,0)]
    while stack:
        s,d=stack.pop()
        if s is None or d>=r:continue
        assert s[0]=='node','A queried frontier entered an opaque subtree: obligation OPEN.'
        _,k,l,rr=s;answer.add(k);stack.extend(((l,d+1),(rr,d+1)))
    return answer


def closure(t,keys):
    if t==V:return (N if N in keys else max(keys))+1
    if t==V1:
        hi=N if N in keys else max(1,max(keys));lo=0 if 0 in keys else 1
        return hi-lo+1
    ancestors=set()
    for key in keys:
        at=t
        while True:
            assert at and at[0]=='node','An ancestor query entered an opaque subtree: obligation OPEN.'
            _,k,l,r=at;ancestors.add(k);order=compare(key,k)
            if order==0:break
            at=l if order<0 else r
    return sp.Integer(len(ancestors))


def root(t):return 0 if t==V else 1 if t==V1 else t[1]


def features(A,B):
    out=[]
    for r in (1,2,3):
        aa,bb=top(A,r),top(B,r);out.extend([closure(B,aa)-len(aa),closure(A,bb)-len(bb)])
    return out+[v*int(root(A)==root(B)) for v in out]


def symbolic_frontier_rows():
    L=node(2,None,node(3,None,H));fan=node(1,node(0),node(N,L))
    stem2=node(0,None,node(1,None,node(N,L)))
    stem3=node(0,None,node(1,None,node(2,None,node(N,node(3,None,H)))))
    reverse3=stem2;reverse2=node(0,None,node(N,node(1,None,L)))
    states=[('root_inverse',fan,V),('stem3_delete',stem3,V),('stem3_keep',stem3,V),
            ('stem2_delete',stem2,V),('stem2_keep',stem2,V),('reverse_guard3',V,reverse3),('reverse_guard2',V,reverse2)]
    out=[]
    for name,A,B in states:
        before=features(A,B);A2=left_root(A);B2=left_root(B) if name.endswith('keep') else B
        after=features(A2,B2);d=[sp.expand(v-u) for u,v in zip(before,after)]
        slopes=[int(v.coeff(N)) for v in d];intercepts=[int(v.subs(N,0)) for v in d]
        out.append({'template':name,'before':list(map(str,before)),'after':list(map(str,after)),
                    'delta':list(map(str,d)),'slopes':slopes,'intercepts':intercepts,
                    'arbitrary_rigid_hanger':'H contains all keys4..N-1; no frontier or query enters H.',
                    'vine_closure_rule':'All ancestors of a finite marked set in a right vine form the prefix ending at its largest key; shifted root1 has the corresponding interval plus0 when queried.'})
    return out


def learn_and_verify_counters():
    # variables remaining depth,doubles,zigs,cost,initial depth. Nullspace of
    # transition increments AND the common-diagonal initialization constraint.
    updates=sp.Matrix([[-2,1,0,1,0],[-1,0,1,1,0],[1,0,0,0,1]])
    basis=updates.nullspace();assert len(basis)==2
    d,b,z,c,D=z3.Ints('remaining doubles zigs units initial')
    def invariant(d,b,z,c,D):return z3.And(d>=0,b>=0,z>=0,z<=1,c>=0,D>=0,D==d+2*b+z,c==b+z,z3.Implies(z==1,d==0))
    inv=invariant(d,b,z,c,D);checks={}
    conditions={
      'initialization':z3.Implies(D>=0,invariant(D,0,0,0,D)),
      'all_LL_RR_LR_RL_double_steps':z3.Implies(z3.And(inv,d>=2),invariant(d-2,b+1,z,c+1,D)),
      'terminal_zig':z3.Implies(z3.And(inv,d==1),invariant(0,b,z+1,c+1,D)),
      'A_cost_at_exit':z3.Implies(z3.And(inv,d==0),c==(D+1)/2),
      'B_double_cost_at_exit':z3.Implies(z3.And(inv,d==0),b==D/2)}
    for name,formula in conditions.items():
        solver=z3.Solver();solver.add(z3.Not(formula));result=solver.check();checks[name]=str(result);assert result==z3.unsat
    return {'status':'SYMBOLIC_COUNTER_INDUCTION_VERIFIED','learned_nullspace_basis':[[str(x) for x in v] for v in basis],
            'variables':['remaining_depth','doubles','zigs','units','initial_depth'],'invariants':['initial=remaining+2*doubles+zigs','units=doubles+zigs','zigs in{0,1}; zig implies remaining0'],
            'Z3_checks':checks,'scope':'Exact counter-transition abstraction of the original splay loop. Physical rotation and target-depth semantics must also be checked; this is not a potential-credit or Universal CD proof.'}


def run(out):
    from parametric import expected,KINDS
    rows=symbolic_frontier_rows()
    for row in rows:
        assert all([a*n+b for a,b in zip(row['slopes'],row['intercepts'])]==expected(n,row['template']) for n in (8,16,32,128))
    dump(out/'SYMBOLIC_FRONTIER_IDENTITIES.json',{'status':'SYMBOLIC_RIGID_SUBTREE_IDENTITIES','parameter':'Every N>=8; actual reaching family uses even N','rows':rows,'scope':'Physical state feature identities, not inferred from numerical interpolation. Full-source reachability/closure has a separate parametric spine proof.'})
    dump(out/'LOOP_INDUCTION_CERTIFICATE.json',learn_and_verify_counters())
    print({'symbolic_frontier_templates':len(rows),'counter_induction':'VERIFIED'})


if __name__=='__main__':
    import sys
    from pathlib import Path
    run(Path(sys.argv[1]))
