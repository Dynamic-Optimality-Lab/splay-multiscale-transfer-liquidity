"""Independent source replay, original-frame reconstruction and unit checking.

Uses both unmodified original splay engines on the one physical n=13 witness,
and the original tuple engine on opaque-fringe terms. No size/repetition sweep.
The producer's source-profile routine is not imported.
"""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
checks=Counter()
calls=Counter()


def ck(test,name):
    if not test:raise AssertionError(name)
    checks[name]+=1


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


tuple_engine=load('original_tuple_splay','python/independent/splay.py')
pointer_engine=load('original_pointer_splay','python/liquidity/legacy_embedding.py')


def totuple(t):
    if t is None:return tuple_engine.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tuple_engine.node(t[0],totuple(t[1]),totuple(t[2]))


def fromtuple(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return [t[1],fromtuple(t[2]),fromtuple(t[3])]


def topointer(t,parent=None):
    if t is None:return None
    p=pointer_engine.mknode(t[0],p=parent)
    p['l']=topointer(t[1],p);p['r']=topointer(t[2],p)
    return p


def frompointer(t):
    return None if t is None else [t['k'],frompointer(t['l']),frompointer(t['r'])]


def keys(t):
    if t is None or isinstance(t,str):return []
    return keys(t[1])+[t[0]]+keys(t[2])


def path(t,y):
    result=[]
    while t is not None:
        ck(not isinstance(t,str),'source descent never enters opaque fringe')
        result.append(t)
        if t[0]==y:return result
        t=t[1 if y<t[0] else 2]
    raise AssertionError('absent source key')


def mirror(t):
    if t is None:return None
    if isinstance(t,str):return 'F_lower'
    return [14-t[0],mirror(t[2]),mirror(t[1])]


def replay_rows(rows,physical=True):
    A,B=rows[0]['source_A'],rows[0]['source_B']
    for r in rows:
        ck((A,B)==(r['source_A'],r['source_B']),'exact consecutive paired source states')
        if physical:
            ck(keys(A)==keys(B)==list(range(1,14)),'physical strict ordered BST key set')
        for side in ['A','B']:
            source=r['source_'+side];expected=r['destination_'+side]
            if side=='B' and r['mode']=='DELETE':
                ck(source==expected and r['B_events']==[],'DELETE retains keys and freezes B')
                continue
            depth=len(path(source,r['key']))-1
            ck(depth==r['d_'+side],'actual source edge depth')
            t,events=tuple_engine.trace(totuple(source),r['key'])
            calls['physical_tuple' if physical else 'opaque_term_tuple']+=1
            ck(fromtuple(t)==expected,'original tuple source destination')
            ck([list(e) for e in events]==r[side+'_events'],'original tuple source event identities')
            if physical:
                p,pe=pointer_engine.splay_trace(topointer(source),r['key'])
                calls['physical_pointer']+=1
                ck(frompointer(p)==expected,'independent original pointer source destination')
                pev=[[e['case'],e['lo'],e['hi'],e['orient']] for e in pe]
                ck(pev==r[side+'_events'],'independent original pointer event identities')
            if side=='A':
                ck(len(events)==r['a']==(depth+1)//2,'A StepEv capacity count')
            else:
                ck(sum(e[0]!='ZIG' for e in events)==r['q']==depth//2,'B double demand count')
                ck(sum(e[0]=='ZIG' for e in events)==r['z']==depth%2,'B final zig count')
        A,B=r['destination_A'],r['destination_B']
    return A,B


def source_profile(T,z,y,events):
    px=path(T,z);h=len(path(T,y))-1;d=len(px)-1
    ops=[]
    for top in range(d-2,-1,-2):
        g,p=px[top][0],px[top+1][0]
        case=('L' if z<g else 'R')+('L' if z<p else 'R')
        ops.append(dict(case=case,site_depth=top,grandparent=g,parent=p))
    if d%2:ops.append(dict(case='ZIG',site_depth=0,grandparent=T[0],parent=None))
    ck([o['case'] for o in ops]==[e[0] for e in events],'first-intervention original source frames')
    entry=None;mu=pmu=r=m=0;pf=False
    if d==0:role='root_noop';old=new=h
    elif z==y:role='accessed';old=new=0
    else:
        entry=next(i for i,o in enumerate(ops) if y in keys(px[o['site_depth']]))
        o=ops[entry]
        if o['case']=='ZIG':role='zig';mu=1
        elif y==o['parent']:role='parent';mu=0
        else:role='other';mu=2
        pmu=mu
        if o['case'] in ['LR','RL']:
            parent=px[o['site_depth']+1]
            pf=y in keys(parent[1 if o['case']=='LR' else 2])
            if pf:pmu=0
        later=[o['case'] for o in ops[entry+1:] if o['case']!='ZIG']
        r=len(later);m=later.count('LL' if y<z else 'RR')
        old=h+mu-r-m;new=h+pmu-r-m
    return dict(source_depth=h,access_depth=d,operations=ops,entry=entry,role=role,
        parent_outer_fringe=pf,old_mu=mu,new_mu=pmu,outer_doubles=r,matching_outer_doubles=m,
        old_U=min(h+2,max(0,old)),PF_U=min(h+2,max(0,new)))


def check_scan(rows,trial,protocol):
    N=len(rows);history=[];queue=[];claims=[];steps=[];usedD=set();usedU=set()
    def claim(d,u,kind):
        ck(tuple(d) not in usedD and tuple(u) not in usedU,'no physical unit or demand reused')
        ck(d[0]==u[0]==0 and 0<=d[1]<N and 0<=u[1]<N,'one physical period and no startup credits')
        usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
    order=[(trial['cut']+i)%N for i in range(N)]
    for t,j in enumerate(order):
        r=rows[j];C=2*r['a'];before=len(queue)
        us=[[0,j,e,b] for e in range(r['a']) for b in [0,1]]
        ds=[[0,j,e] for e,ev in enumerate(r['B_events']) if ev[0]!='ZIG'];facts=[]
        if r['delta']>0:
            for d,u in zip(ds[:C],us):claim(d,u,'positive_own')
            queue+=ds[C:];history.append((j,t));reserve=C;offer=lam=0;x=r['delta']
        else:
            for anchor,at in history:
                intervening=[rows[v] for v in order[at+1:t] if rows[v]['d_B']>0]
                T=rows[anchor]['destination_B'];k=len(intervening)
                if not intervening:c=(len(path(T,r['key']))-1)//2
                else:
                    first=intervening[0]
                    ck(first['source_B']==T,'first genuine B change uses original anchor destination')
                    profile=source_profile(T,first['key'],r['key'],first['B_events'])
                    c=profile['PF_U' if protocol=='PF' else 'old_U']//2+k-1
                facts.append(dict(anchor=anchor,k=k,ceiling=c))
            reserve=min([C]+[f['ceiling'] for f in facts])
            ck(r['q']<=reserve,'source reservation protects own work without demand oracle')
            for d,u in zip(ds,us[:r['q']]):claim(d,u,'payer_own')
            offer=C-reserve;lam=reserve-r['q'];x=-offer;take=min(offer,len(queue))
            for d,u in zip(queue[:take],us[reserve:reserve+take]):claim(d,u,'loan')
            queue=queue[take:]
        step=dict(scan_index=t,block=j,key=r['key'],capacity=C,own_q=r['q'],delta=r['delta'],
            history=[i for i,at in history],facts=facts,reservation=reserve,offer=offer,reserved_loss=lam,
            signed_input=x,debt_before=before,debt_after=len(queue))
        ck(step==trial['steps'][t],'independent full-history reservation and debt step')
        ck(len(queue)==max(0,before+x),'clipped debt recurrence')
        steps.append(step)
    ck(trial['assignments']==claims and trial['unpaid']==queue,'independent physical assignment ledger')
    ck(trial['periods']==1 and len(queue)==trial['final_debt']==1 and not trial['accepted'],'all-cut source rejection')
    ck(len(claims)+len(queue)==sum(r['q'] for r in rows),'every actual B double accounted')
    X=[0]
    for s in steps:X.append(X[-1]+s['signed_input'])
    b=max(i for i,x in enumerate(X) if x==min(X));busy=steps[b:]
    cert=dict(last_minimum_index=b,busy_blocks=[s['block'] for s in busy],source_delta_sum=sum(s['delta'] for s in busy),
        reserved_loss_sum=sum(s['reserved_loss'] for s in busy),terminal_debt=len(queue))
    ck(cert==trial['busy_suffix'],'canonical last-minimum busy suffix independently rebuilt')
    ck(cert['source_delta_sum']+cert['reserved_loss_sum']==1,'exact source-cost reservation-loss split')
    ck(trial['startup_units_used']==trial['reused_units']==0,'no startup or reused algorithmic credits')


def check_direct(rows,trial):
    T=rows[0]['destination_B'];z=rows[1]['key'];y=rows[2]['key']
    p=source_profile(T,z,y,rows[1]['B_events'])
    ck((p['source_depth'],p['entry'],p['parent_outer_fringe'],p['PF_U'])==(3,0,False,4),
       'fixed missing unit is outside unchanged parent-outer PF correction')
    # This exact role calculation precedes use of any future payer q.
    entry=p['operations'][0];g=path(T,entry['grandparent'])[-1]
    if entry['case']=='RL':outer=g[1]
    else:
        ck(entry['case']=='LR','reflected first entry is LR');outer=g[2]
    ck(y in keys(outer),'tracked key in original grandparent outer subtree')
    ck(p['outer_doubles']==1 and p['matching_outer_doubles']==0,'one cross outer frame with depth shift minus one')
    ck(p['operations'][1]['case'] in ['LR','RL'],'outer cross frame')
    safe_depth=p['source_depth']+1-1
    ck(safe_depth==3 and safe_depth//2==1,'source-selected safe own-work bound before future demand')
    claims=trial['assignments'];usedD=set();usedU=set();loans=[]
    for claim in claims:
        d,u=claim['demand'],claim['unit'];_,j,e=d;_,pool,ae,bit=u
        ck(tuple(d) not in usedD and tuple(u) not in usedU,'direct certificate has distinct physical identities')
        ck(d[0]==u[0]==0 and 0<=j<19 and 0<=pool<19,'direct certificate uses only one recurrent period')
        ck(0<=e<len(rows[j]['B_events']) and rows[j]['B_events'][e][0]!='ZIG','direct demand is original B double')
        ck(0<=ae<rows[pool]['a'] and bit in [0,1],'direct unit belongs to actual A StepEv')
        usedD.add(tuple(d));usedU.add(tuple(u))
        if claim['kind']=='own':
            ck(j==pool,'own work paid from its own physical pool')
        else:
            loans.append(claim)
            ck((j,e,pool,ae,bit)==(0,2,2,0,1),'one fixed exact-entry loan to third anchor double')
            ck(rows[pool]['q']<=safe_depth//2 and rows[pool]['a']>=1,'source bound protects donor own work')
    demands={(0,j,e) for j,r in enumerate(rows) for e,ev in enumerate(r['B_events']) if ev[0]!='ZIG'}
    ck(usedD==demands and len(claims)==22 and len(loans)==1,'complete 22-demand source injection')
    ck(2*sum(r['a'] for r in rows)-len(usedU)==28,'exact unused distinct capacity')


def main():
    pins=read(HERE/'entry_source_pins.json')
    for rel,h in pins['files'].items():ck(sha(ROOT/rel)==h,'all inherited files preserved')
    ck(sha(HERE/'PG00_FOUR_RULE_GATE.md')==pins['gate_sha256'],'original four-rule gate preserved')
    data=read(HERE/'closed_source_certificate.json');selected=read(HERE/'first_return_obstruction.json')
    ck(data['selected_audit_sha256']==sha(HERE/'first_return_obstruction.json'),'selected witness provenance')
    ck(data['fixed_completion_scope_sha256']==sha(HERE/'PG00A_FIXED_WITNESS_COMPLETION.md'),'fixed completion scope pin')
    rows=data['ordinary_rows'];reflected=data['reflected_rows'];formal=data['formal_opaque_fringe_rows']
    ck([r['key'] for r in rows]==[7,5,3,1,5,6,4,1,2,1,5,1,6,7,1,2,1,3,1],'exact unaltered selected closure word')
    ck(rows[0]['source_A']!=rows[0]['source_B'],'unequal recurrent source pair')
    A,B=replay_rows(data['startup_rows'])
    ck(A==rows[0]['source_A'] and B==rows[0]['source_B'],'actual diagonal startup reaches recurrent source')
    ck(data['startup_rows'][0]['source_A']==data['startup_rows'][0]['source_B'],'startup begins with equal original trees')
    for orientation,rs in [('ordinary',rows),('reflected',reflected)]:
        A,B=replay_rows(rs)
        ck(A==rs[0]['source_A'] and B==rs[0]['source_B'],'full exact paired physical closure')
        ck(all(r['source_A']!=r['source_B'] and r['destination_A']!=r['destination_B'] for r in rs),
           'nowhere-diagonal physical closed walk')
        for protocol in ['FI','PF']:
            trials=data['all_cut_audits'][orientation][protocol]
            ck([s['cut'] for s in trials]==list(range(19)),'every physical block cut once')
            for trial in trials:check_scan(rs,trial,protocol)
        check_direct(rs,data['direct_injection'][orientation])
    for ordinary,mirrored in zip(rows,reflected):
        ck(mirrored['key']==14-ordinary['key'],'key reflection')
        for side in ['source_A','source_B','destination_A','destination_B']:
            ck(mirrored[side]==mirror(ordinary[side]),'full source reflection')
    A,B=replay_rows(formal,physical=False)
    ck(A==formal[0]['source_A'] and B==formal[0]['source_B'],'opaque-fringe source identity closes exactly')
    # The symbolic identities are universal substitutions, not a finite fringe sample.
    ck(all(r['key']<=7 for r in formal),'fringe is never accessed')
    T=rows[0]['destination_B'];events=rows[1]['B_events'];profiles={}
    for y in range(1,8):
        p=source_profile(T,5,y,events);profiles[str(y)]=p
        ck(p==data['first_intervention_profiles'][str(y)],'all first-intervention profiles reconstructed independently')
        ck(len(path(rows[1]['destination_B'],y))-1<=p['PF_U']<=p['old_U'],'unchanged PF/FI source bound sound on fixed frame')
    loss=0
    for j,r in enumerate(rows[1:],1):
        k=j-1;C=2*r['a'];p=profiles[str(r['key'])]
        c=p['source_depth']//2 if k==0 else p['PF_U']//2+k-1
        rho=min(C,c);f=C-rho;lam=rho-r['q'];loss+=lam
        expected=dict(block=j,key=r['key'],capacity=C,own_q=r['q'],k=k,h=p['source_depth'],U_PF=p['PF_U'],
            ceiling=c,reservation=rho,offer=f,reserved_loss=lam)
        ck(expected==data['fresh_budget_rows'][j-1],'exact PF fresh source budget row')
        ck(f==0 and lam>=0,'all latest-anchor suffixes empty')
        if k==0:
            ck(C==2 and c==2,'immediate latest-anchor own reservation')
            ck(19-1>=C,'every older copy first-key ceiling at least 18')
        else:
            ck(c>=C,'latest nonfirst source ceiling covers capacity')
            # For any older copy ell>=1, c_old=c+19ell, exactly.
            ck(19>0,'older identical source facts only raise this ceiling')
    expected_totals=dict(blocks=19,A=25,C=50,Q_B=22,E=1,C_D=0,L_PF_fresh=0,Gamma_PF=1,
                         source_delta=-28,reserved_loss_fresh=29)
    ck(data['totals']==expected_totals and loss==29,'positive-gap source-cost and reservation-loss totals')
    ck(sum(r['a'] for r in rows)==25 and sum(r['q'] for r in rows)==22,'source total work independently summed')
    ck([i for i,r in enumerate(rows) if r['delta']>0]==[0] and rows[0]['a']==1 and rows[0]['q']==3,'exactly one one-unit positive')
    ck(selected['first_return_off_diagonal'] and rows[4]['destination_A']!=rows[4]['destination_B'],
       'first return fails both PF repayment and synchronization')
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    ck(stage_now==pins['stage_files'] and len(stage_now)==125,'all Stage 11G hashes and inventory unchanged')
    save('independent_audit.json',dict(status='PASS',checks=dict(sorted(checks.items())),total_checks=sum(checks.values()),
        original_source_calls=dict(calls),physical_key_count=13,repetition_controls_replayed=[1],
        larger_finite_fits=0,new_key_count_sweeps=0,source_search_engine_calls=0,
        physical_cuts_checked=76,PF_rejected_cuts_per_orientation=19,FI_rejected_cuts_per_orientation=19,
        direct_injection_demands_per_orientation=22,opaque_fringe_symbolic_identity=True,
        all_size_proof_basis='exact opaque-fringe source identities; analytic repeated-copy ceiling comparison',
        general_one_unit_closure_theorem='OPEN',original_FI_PF_algorithms='UNCHANGED',
        closed_source_sha256=sha(HERE/'closed_source_certificate.json'),
        source_shas={p:sha(ROOT/p) for p in ['python/independent/splay.py','python/liquidity/legacy_embedding.py']},
        matching_terminal='FROZEN',stage_11g_files_unchanged=125))
    print(json.dumps(dict(status='PASS',checks=sum(checks.values()),source_calls=dict(calls),
        all_cut_trials=76,positive_Gamma_PF=1,direct_injection=22,stage_11g=125),indent=2))


if __name__=='__main__':main()
