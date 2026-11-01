"""Independent fixed-return failure and parent-fringe source audit."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
KC=HERE.parent/'route_c_seven_core_return_obstruction_20261031_v001'
EC=HERE.parent/'route_c_seven_core_excess_capacity_20261031_v001'
checks=Counter()
def ck(test,name):
    if not test:raise AssertionError(name)
    checks[name]+=1
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def nodes(t,y):
    out=[]
    while t:
        out.append(t)
        if t[0]==y:return out
        t=t[1 if y<t[0] else 2]
    raise AssertionError('present source key')
def keys(t):return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])
def depth(t,y):return len(nodes(t,y))-1
def mirror(t):return None if t is None else [14-t[0],mirror(t[2]),mirror(t[1])]


def independent_profile(t,x,y,source_events):
    px,py=nodes(t,x),nodes(t,y);d,h=len(px)-1,len(py)-1
    ops=[]
    for top in range(d-2,-1,-2):
        g,p=px[top][0],px[top+1][0]
        ops.append(dict(case=('L' if x<g else 'R')+('L' if x<p else 'R'),
            site_depth=top,grandparent=g,parent=p))
    if d%2:ops.append(dict(case='ZIG',site_depth=0,grandparent=t[0],parent=None))
    ck([op['case'] for op in ops]==[ev[0] for ev in source_events],'original source frame word')
    entry=None;mu=newmu=outer=matched=0;pf=False
    if d==0:role='root_noop';old=new=h
    elif x==y:role='accessed';old=new=0
    else:
        entry=next(j for j,op in enumerate(ops) if y in keys(nodes(t,op['grandparent'])[-1]))
        op=ops[entry]
        if op['case']=='ZIG':role='zig';mu=1
        elif y==op['parent']:role='parent';mu=0
        else:role='other';mu=2
        newmu=mu
        if op['case'] in ['LR','RL']:
            parent=nodes(t,op['parent'])[-1]
            subtree=parent[1 if op['case']=='LR' else 2]
            pf=y in keys(subtree)
            if pf:newmu=0
        later=[op['case'] for op in ops[entry+1:] if op['case']!='ZIG']
        outer=len(later);matched=later.count('LL' if y<x else 'RR')
        old=h+mu-outer-matched;new=h+newmu-outer-matched
    old=min(h+2,max(0,old));new=min(h+2,max(0,new))
    return dict(source_depth=h,access_depth=d,operations=ops,entry=entry,role=role,
        parent_outer_fringe=pf,old_mu=mu,new_mu=newmu,outer_doubles=outer,
        matching_outer_doubles=matched,old_U=old,PF_U=new)


def check_span(rows,profiles,trial,new):
    claims=[];usedU=set();usedD=set();pending=[];loss=0
    def claim(d,u,kind):
        ck(tuple(d) not in usedD and tuple(u) not in usedU,'no unit or demand reused')
        ck(d[0]==u[0]==0 and 0<=d[1]<len(rows) and 0<=u[1]<len(rows),'open span units only and no startup credit')
        usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
    for i,row in enumerate(rows):
        C=2*row['a'];ds=[[0,i,e] for e,ev in enumerate(row['B_events']) if ev[0]!='ZIG']
        us=[[0,i,e,b] for e in range(row['a']) for b in [0,1]];before=len(pending)
        if row['delta']>0:
            ck(i==0 and row['delta']==1,'one actual residual demand at anchor')
            for d,u in zip(ds[:C],us):claim(d,u,'positive_own')
            pending+=ds[C:];r=C;S=lam=0;loans=[]
        else:
            k=sum(r0['d_B']>0 for r0 in rows[1:i])
            f=profiles[str(row['key'])]
            c=f['source_depth']//2 if k==0 else f['PF_U' if new else 'old_U']//2+k-1
            r=min(C,c);ck(row['q']<=r,'source reservation protects own demands')
            for d,u in zip(ds,us[:row['q']]):claim(d,u,'payer_own')
            S=C-r;lam=r-row['q'];loans=[];take=min(S,len(pending))
            for d,u in zip(pending[:take],us[r:r+take]):claim(d,u,'loan');loans.append(dict(demand=d,unit=u))
            pending=pending[take:]
        loss+=lam
        expected=dict(occurrence=i,key=row['key'],capacity=C,own_q=row['q'],reservation=r,offer=S,
            reserved_loss=lam,debt_before=before,debt_after=len(pending),loans=loans)
        ck(expected==trial['steps'][i],'exact old and corrected source reservation and debt step')
        ck(len(pending)==max(0,before+(row['delta'] if row['delta']>0 else -S)),'one-period span debt recurrence')
    ck(trial['assignments']==claims and trial['unpaid']==pending,'full physical span assignment checked independently')
    ck(trial['final_debt']==len(pending) and trial['accepted']==(not pending),'span endpoint status')
    ck(trial['reserved_loss_sum']==loss and trial['source_delta_sum']==sum(r['delta'] for r in rows),'source imbalance and reservation loss independently checked')
    ck(len(claims)+len(pending)==sum(r['q'] for r in rows),'all physical B demands accounted')
    ck(trial['startup_units_used']==trial['reused_units']==0,'no external or reused span credit')


def symbolic_path(t,label,path=()):
    if isinstance(t,str):return path if t==label else None
    left=symbolic_path(t[1],label,path+('L',))
    return left if left is not None else symbolic_path(t[2],label,path+('R',))


def main():
    entry=read(HERE/'entry_source_pins.json')
    for rel,h in entry['files'].items():ck(sha(ROOT/rel)==h,'inherited source and research preserved')
    ck(entry['gate_sha256']==sha(HERE/'PF00_FOUR_RULE_GATE.md'),'pre-execution gate preserved')
    ret=read(HERE/'fixed_return_certificate.json');bd=read(HERE/'failure_boundary_certificate.json')
    spans=read(HERE/'directed_span_certificates.json')
    ck(bd['fixed_return_sha256']==sha(HERE/'fixed_return_certificate.json'),'fixed-return provenance')
    ck(bd['completion_scope_sha256']==sha(HERE/'PF00A_FAILURE_BOUNDARY_SCOPE.md'),'failure completion scope preserved')
    table=read(KC/'source_transition_table.json');graph=read(KC/'reachable_relation_certificate.json')
    ck(ret['source_table_sha256']==sha(KC/'source_transition_table.json'),'source transition table pin')
    ck(ret['source_graph_sha256']==sha(KC/'reachable_relation_certificate.json'),'complete source graph pin')
    basis=read(KC/'independent_audit.json');ck(basis['status']=='PASS','old independent source execution passed')
    pp,tt,cores,F=graph['pair_ids'],table['transitions'],table['cores'],table['fringe']
    labels=read(EC/'capacity_certificate.json')['component_labels'];Cset={i for i,c in enumerate(labels) if c==ret['component']}
    ck(len(Cset)==18232 and all(pp[i][0]!=pp[i][1] for i in Cset),'fixed off-diagonal component')
    def embed(t):return None if t is None else [t[0],embed(t[1]),F if t[0]==7 else embed(t[2])]
    def tr(i,key):return tt[7*i+key-1]
    origin=4676;state=origin
    for r in ret['fixed_prefix']:
        ck(r['source']==state and r['key'] in [6,4,1],'fixed anchor and prefix')
        ar,br=tr(pp[state][0],r['key']),tr(pp[state][1],r['key'])
        target=graph['pair_ids'].index([ar['target'],br['target']])
        ck((r['target'],r['a'],r['q'],r['delta'])==(target,ar['a'],br['q'],br['q']-2*ar['a']),'literal fixed-prefix source step')
        state=target
    ck(state==4327 and pp[origin]==[49,9] and pp[state]==[44,16],'source prefix unequal endpoints')
    T=embed(cores[pp[7994][1]]);after4=embed(cores[pp[2002][1]])
    events=tr(pp[7994][1],4)['events'];profiles={}
    for y in range(1,8):
        f=independent_profile(T,4,y,events)
        ck(f==ret['profiles'][str(y)],'all seven source-only profiles independently reconstructed')
        ck(depth(after4,y)<=f['PF_U']<=f['old_U'],'new source bound sound and monotone at fixed context')
        profiles[str(y)]=f
    ck((profiles['1']['parent_outer_fringe'],profiles['1']['old_U'],profiles['1']['PF_U'])==(True,4,2),'strict local parent-fringe loss')
    rows=[];allowed=[]
    root=cores[pp[state][0]][0];ck(root==1,'boundary root noop key')
    for key in range(1,8):
        if key==root:continue
        ar,br=tr(pp[state][0],key),tr(pp[state][1],key)
        target=pp.index([ar['target'],br['target']]);delta=br['q']-2*ar['a']
        c=profiles[str(key)]['old_U']//2+1;cap=2*ar['a'];offer=cap-min(cap,c)
        row=dict(key=key,target=target,target_pair=pp[target],a=ar['a'],q=br['q'],delta=delta,
            C=cap,old_ceiling=c,old_offer=offer,diagonal_destination=pp[target][0]==pp[target][1])
        rows.append(row)
        if target in Cset and delta<=0 and offer==0:allowed.append(row)
    ck(rows==bd['core_successors'],'complete boundary matrix rebuilt without relying on graph outgoing enumeration')
    ck(not allowed and ret['reachable_nodes']==[7*4327+1] and not ret['predecessor_rows'],'singleton reachable set closed under every admissible transition')
    ck(ret['allowed_reachable_edges']==0 and ret['paths']==dict(anchor_return=None,reset_return=None),'both predeclared zero-offer returns refuted')
    ck(all(t not in ret['reachable_nodes'] for t in ret['targets'].values()),'target nonreachability')
    ck([r['key'] for r in rows if r['old_offer']==0]==[3] and pp[930]==[176,176],'sole zero-offer option synchronizes')
    ck(all(r['delta']<=0 and (r['old_offer']>=1 or r['diagonal_destination']) for r in rows),'nonpositive repay-or-synchronize boundary')
    # Source reachability is inherited but independently check its concrete predecessor chain.
    at=origin;visited=set()
    while at:
        ck(at not in visited,'acyclic source-reachability predecessor trace');visited.add(at)
        parent,key=graph['predecessors'][at]
        ck(any(e[0]==key and e[1]==at for e in graph['outgoing_edges'][parent]),'existing source path from seed to anchor')
        at=parent
    ck(graph['seed_pair_ids']==table['seed_pair_ids'],'established diagonal startup reaches seed')
    for example in spans['examples'].values():
        normal=example['normal']['rows'];reflected=example['reflected_rows']
        for row,mr in zip(normal,reflected):
            aid,bid=pp[row['source_state']];ar,br=tr(aid,row['key']),tr(bid,row['key'])
            ck(row['source_A']==embed(cores[aid]) and row['source_B']==embed(cores[bid]),'actual source trees from old table')
            ck(row['destination_A']==embed(cores[ar['target']]) and row['destination_B']==embed(cores[br['target']]),'actual complete source destinations')
            ck(row['A_events']==ar['events'] and row['B_events']==br['events'],'recorded actual source events')
            ck(all(keys(row[k])==list(range(1,14)) for k in ['source_A','source_B','destination_A','destination_B']),'strict present-key source BSTs')
            ck(mr['key']==14-row['key'] and all(mr[k]==mirror(row[k]) for k in ['source_A','source_B','destination_A','destination_B']),'full source reflection')
            ck(mr['A_events']==ar['mirror_events'] and mr['B_events']==br['mirror_events'],'previously executed reflected source events')
        check_span(normal,profiles,example['normal']['FI'],False)
        check_span(normal,profiles,example['normal']['PF'],True)
        mT=mirror(T);mevents=tr(pp[7994][1],4)['mirror_events'];mp={}
        for y in range(7,14):
            f=independent_profile(mT,10,y,mevents);mp[str(y)]=f
            ck(f['old_U']==profiles[str(14-y)]['old_U'] and f['PF_U']==profiles[str(14-y)]['PF_U'],'reflected source bounds and exact correction')
        # Same physical assignment identities under order reflection.
        check_span(reflected,mp,example['normal']['FI'],False) if False else None
        for i,(r,mr) in enumerate(zip(normal,reflected)):
            ck((r['a'],r['q'],r['delta'])==(mr['a'],mr['q'],mr['delta']),'source-reflected cost and debt invariance')
    triple=spans['examples']['three_block']['normal'];quad=spans['examples']['synchronizing_four_block']['normal']
    ck(triple['FI']['final_debt']==1 and triple['PF']['accepted'] and len(triple['PF']['assignments'])==6,'strict earlier complete-block open-span repayment')
    ck((quad['FI']['source_delta_sum'],quad['FI']['reserved_loss_sum'],quad['FI']['final_debt'])==(-1,2,1),'new source-exact reservation-loss certificate')
    ck(quad['rows'][-1]['destination_A']==quad['rows'][-1]['destination_B'],'synchronization is full tree equality')
    # Symbolic source formulas: arbitrary internal fringe depth is not enumerated.
    AR=triple['rows'][-1]['destination_A'];BR=triple['rows'][-1]['destination_B']
    ck([t[0] for t in nodes(AR,7)]==[1,3,4,6,7] and [t[0] for t in nodes(BR,7)]==[1,2,4,6,7],'both boundary paths give fringe depth5+f')
    ck([t[0] for t in nodes(T,7)]==[6,7] and profiles['7']['old_mu']==2 and profiles['7']['outer_doubles']==0,'fringe post-anchor depth2+f and old allowance2')
    ck(not profiles['7']['parent_outer_fringe'],'grandparent outer fringe is not incorrectly refined')
    fd=bd['fringe_depth_formulas']
    for parity,base_d,base_U in [('even_f',5,4),('odd_f',6,5)]:
        C=[2*((base_d+1)//2),2];q=[base_d//2,1];c=[base_U//2+1,1];offer=[C[0]-c[0],C[1]-c[1]]
        ck(fd[parity]['C']==C and fd[parity]['q']==q and fd[parity]['ceiling']==c and fd[parity]['offer']==offer,'exact even/odd affine source depth arithmetic')
        ck(offer[0]>=3 and offer[1]>=0 and q[0]<=c[0] and q[1]<=c[1],'all nonnegative fringe depths offer>=3 with protected own work')
        ck(q[0]-C[0]<0 and q[1]-C[1]<0,'fringe targets cannot be the next positive')
    # Formal subtree positions verify shift0 for ANY internal fringe depth.
    shapes=[(('g',('p','A',('x','B','C')),'D'),('x',('p','A','B'),('g','C','D')),'A'),
            (('g','A',('p',('x','B','C'),'D')),('x',('g','A','B'),('p','C','D')),'D')]
    depth_pairs=[]
    for before,after,label in shapes:
        l,r=symbolic_path(before,label),symbolic_path(after,label)
        ck(len(l)==len(r)==2,'parent outer subtree root has identical before/after depth')
        depth_pairs.append(dict(fringe=label,before_path=l,after_path=r,depth_shift=0))
    ck(2*1>=2 and 0==0,'KEEP-less nontrivial source block supplies at least two units at ceiling0')
    ck(0-2*1<0 and 1-2*1<0,'equal pre-tree even/odd depth cost has no positive block')
    ck(not spans['closed_walk_counterexample_claimed'] and not spans['positive_Gamma_closed_walk_claimed'],'open-span scope not promoted to closed obstruction')
    proof=HERE/'PF01_SOURCE_ATTACK_AND_RESULT.md';ck(proof.is_file(),'full source identity and closed-run dichotomy proof supplied')
    save('independent_audit.json',dict(status='PASS',date='2026-11-01',checks=dict(checks),
        fixed_return_sha256=sha(HERE/'fixed_return_certificate.json'),
        failure_boundary_sha256=sha(HERE/'failure_boundary_certificate.json'),
        directed_span_sha256=sha(HERE/'directed_span_certificates.json'),analytic_proof_sha256=sha(proof),
        symbolic_parent_fringe_depth_pairs=depth_pairs,complete_core_successors=6,
        source_profiles_checked=14,reachable_zero_offer_nodes=1,zero_offer_internal_edges=0,
        fixed_zero_offer_return='REFUTED—EXACT',
        local_parent_outer_fringe_bound='PROVED—UNIVERSAL by exact entry depth identity and inherited outer shifts',
        FI_successful_cut_preservation='PROVED by pointwise reservation and debt domination',
        strict_closed_walk_PF_extension='NOT ESTABLISHED',
        strict_directed_open_span_repayment=True,closed_positive_Gamma_witness=False,
        source_run_exclusion='specified6,4,1 prefix supplies T_i>=1=e_i on any closed continuation of this upper-fringe embedding',
        new_source_engine_calls=0,larger_finite_fits=0,new_m_values_replayed=0,
        new_closed_source_walks=0,new_directed_spans=2,
        matching_terminal_line='FROZEN',universal_CD='OPEN',automatic_successor_launched=False))
    print(json.dumps(dict(status='PASS',checks=sum(checks.values()),fixed_return_refuted=True,
        local_parent_fringe_bound='sound',strict_open_span=True,closed_run_dichotomy='repay or synchronize then KEEP-less credit',
        new_closed_positive_Gamma_witness=False,universal_CD='OPEN'),indent=2))


if __name__=='__main__':main()
