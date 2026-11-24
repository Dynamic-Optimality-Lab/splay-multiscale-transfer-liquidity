from campaign4 import *
from fast_physics import FullTree,physical_replay,skeleton_cost,decode,path_hull
from independent_path_audit import check as check_physical

def spine(st):
    out=set()
    for side in (0,1):
        k=st['root']
        while k is not None:out.add(k);k=st['children'][str(k)][side]
    return sorted(out)

def cheap_walk(n):
    initial=vine(range(1,n+1))
    # All A requests move along the root's immediate next physical neighbor.
    # B sees a nontrivial sparse subsequence; restoration stays measured.
    word=ops('D',range(2,n+1))+ops('K',range(n,0,-1))
    word+=ops('K',range(2,n+1))+ops('K',range(n-1,0,-1))
    return {'name':f'C04_rootwalk_n{n}','family':'one-StepEv A geometry control',
        'initial_A':initial,'initial_B':initial,'diagonal_initial':initial,'reaching_prefix':[],
        'operations':word,'parametric_domain':'all integers n>=2; all helpers and exact restoration included'}

def check_spine(s):
    f=physical_replay(s,collect_A=True);E=spine(s['initial_A']);rank={k:i for i,k in enumerate(E)}
    assert all(z['a']<=1 for z in f['rows'])
    # Independently computed raw S; these controls visit every key genuinely.
    bt=FullTree(s['initial_B']);marks=set()
    for tag,x in s['operations']:
        if tag=='K':
            if bt.root!=x:marks.add(x)
            bt.splay(x,bt,'A')
    S=path_hull(Tree(s['initial_B']),marks)
    rho={e:sum(k<=e for k in S) for e in E}
    d=max((rho[v]-rho[u] for u,v in zip(E,E[1:])),default=0)
    previous=s['initial_A']['root'];variation=0;metric=0
    for z in f['rows']:
        st=decode(z['A_code'],len(s['initial_A']['children']))
        assert spine(st)==E and z['x'] in rank
        jump=abs(rank[z['x']]-rank[previous]);assert jump<=2*z['a']
        metric+=abs(rho[z['x']]-rho[previous]).bit_length();variation+=jump
        previous=z['x']
    xs=[x for tag,x in s['operations'] if tag=='K']
    sr={x:i for i,x in enumerate(sorted(S))}
    L=sum(abs(sr[x]-sr[xs[i-1]]).bit_length() for i,x in enumerate(xs))
    m=sum(x!=xs[i-1] for i,x in enumerate(xs))
    assert L<=metric<=max(1,(2*d).bit_length())*f['A']
    assert m+L<=3*f['A'] and S<=set(E)
    return {'source':s['name'],'A':f['A'],'Q_B':f['Q_B'],'original_S_size':len(S),
        'fixed_A_extreme_spine_size':len(E),'maximum_A_StepEv_per_access':1,
        'maximum_S_rank_gap_on_E':d,'cyclic_A_root_E_variation':variation,
        'actual_A_root_log_metric_variation':metric,'raw_m':m,'raw_L':L,
        'old_raw_periodic_certificate':m+L,'theorem_bound':3*f['A'],
        'every_A_boundary_spine_and_root_jump_checked':True,'original_Pi_classified':False}

def return_checks(s):
    f=physical_replay(s);rows=f['rows'];N=len(rows);positions=defaultdict(list)
    positions[f['initial_B_code']].append(0)
    for i,z in enumerate(rows,1):positions[z['B_code']].append(i)
    pairs=[]
    for state,ps in positions.items():
        # Exact consecutive returns plus the whole source; no exhaustive claim.
        pairs.extend((a,b) for a,b in zip(ps,ps[1:]) if a<b)
    pairs.append((0,N));out=[]
    for lo,hi in sorted(set(pairs)):
        xs=[z['x'] for z in rows[lo:hi] if z['tag']=='K']
        if not xs:continue
        code=f['initial_B_code'] if lo==0 else rows[lo-1]['B_code']
        st=decode(code,len(s['initial_B']['children']));J=path_hull(Tree(st),set(xs))
        z=periodic_cost(xs,J);rank={x:i for i,x in enumerate(sorted(J))}
        linear=[]
        for x in xs:
            if not linear or linear[-1]!=x:linear.append(x)
        D=len(J)+len(linear)+sum(abs(rank[v]-rank[u]).bit_length() for u,v in zip(linear,linear[1:]))
        assert z['B_cyclic']<=D
        tree=FullTree(st);other=FullTree(st);Q=0
        expected=sum(x['q'] for x in rows[lo:hi])
        for r in range(1,4):
            for x in xs:Q+=tree.splay(x,other,'A')[1]
            assert tree.code==code and Q==r*expected
        out.append({'interval_after':lo,'through':hi,'complete_B_closed':True,'A':sum(x['a'] for x in rows[lo:hi]),
            'N':len(J),'D_raw':D,'c_cyclic':z['B_cyclic'],'Q_B':expected,
            'three_exact_repetitions_preserve_cost_and_full_state':True})
    return out

if __name__=='__main__':
    meter=Meter('structural_checks')
    s=cheap_walk(1025);f=physical_replay(s);s.update(A=f['A'],Q_B=f['Q_B'])
    write('SPINE_SOURCE.json',s)
    proof=check_spine(s);proof['independent_physical']=check_physical(s)
    old=json.loads((REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY/EXP01_SOURCE_WITNESSES.json').read_text())
    # The old archive is a list; preserve only references and exact replay evidence.
    if isinstance(old,dict):old=old.get('sources',old.get('new_sources',[]))
    selected=[x for x in old if x['name'].startswith('DH_')][:2]
    historical=[check_spine(x) for x in selected]
    small=cheap_walk(9)
    returns=return_checks(small)
    write('STRUCTURAL_CHECKS.json',{'new_large_spine_control':proof,'historical_DH_controls':historical,
        'closed_return_comparison_checks':returns,
        'proofs_are_analytic_not_inferred_from_tests':True})
    print('PASS one-StepEv A transport and exact B-return cancellation checks',flush=True)
    meter.success=True
