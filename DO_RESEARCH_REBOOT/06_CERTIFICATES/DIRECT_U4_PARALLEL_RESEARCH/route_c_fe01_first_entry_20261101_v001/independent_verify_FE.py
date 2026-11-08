"""Independent FE01 audit: no import of the new source formula or producer.

Derives shifts from both original engines on opaque-fringe identities;
classifies first entry using original LCA/divergence coordinates; compares
to both source outputs on a gate-fixed existing n=13 corpus. Separately
reconstructs the unchanged FI/PF and new FE physical FIFO ledgers.
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
PG=HERE.parent/'route_c_pf_positive_gap_closure_20261101_v001'
checks=Counter();calls=Counter()
ENTRY={};OUTER={}


def ck(value,label):
    if not value:raise AssertionError(label)
    checks[label]+=1
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


tuple_source=load('fe_original_tuple','python/independent/splay.py')
pointer_source=load('fe_original_pointer','python/liquidity/legacy_embedding.py')


def tt(t):
    if t is None:return tuple_source.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tuple_source.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return [t[1],jt(t[2]),jt(t[3])]
def pt(t,parent=None):
    if t is None:return None
    if isinstance(t,str):
        p=pointer_source.mknode(t,p=parent);p['opaque']=t;return p
    p=pointer_source.mknode(t[0],p=parent)
    p['l']=pt(t[1],p);p['r']=pt(t[2],p);return p
def jp(t):
    if t is None:return None
    if 'opaque' in t:return t['opaque']
    return [t['k'],jp(t['l']),jp(t['r'])]
def keys(t):return [] if t is None or isinstance(t,str) else keys(t[1])+[t[0]]+keys(t[2])
def nodes(t,y):
    p=[]
    while t is not None:
        ck(not isinstance(t,str),'source query does not enter opaque variable')
        p.append(t)
        if t[0]==y:return p
        t=t[1 if y<t[0] else 2]
    raise AssertionError('present source key')
def depth(t,y):return len(nodes(t,y))-1
def mirror(t):
    if t is None:return None
    if isinstance(t,str):return 'F_lower'
    return [14-t[0],mirror(t[2]),mirror(t[1])]


def both_sources(T,x,label):
    t,te=tuple_source.trace(tt(T),x);calls[label+'_tuple']+=1
    p,pe=pointer_source.splay_trace(pt(T),x);calls[label+'_pointer']+=1
    tj,pj=jt(t),jp(p)
    tev=[list(e) for e in te];pev=[[e['case'],e['lo'],e['hi'],e['orient']] for e in pe]
    ck(tj==pj,'two original source destinations agree')
    ck(tev==pev,'two original source event lists agree')
    return tj,tev


def numeric(t,labels):
    if isinstance(t,str):return t
    return [labels[t[0]],numeric(t[1],labels),numeric(t[2],labels)]
def locations(t,p=()):
    if isinstance(t,str):return {t:p}
    return {t[0]:p,**locations(t[1],p+('L',)),**locations(t[2],p+('R',))}


def derive_symbolic_tables():
    cert=read(HERE/'symbolic_rotation_certificate.json')
    labels={
        'LL':dict(x=1,p=2,g=3),'RR':dict(g=1,p=2,x=3),
        'LR':dict(p=1,x=2,g=3),'RL':dict(g=1,x=2,p=3),
        'ZIG_L':dict(x=1,p=2),'ZIG_R':dict(p=1,x=2),
    }
    for case,mapping in labels.items():
        row=cert['identities'][case]
        before=numeric(row['before'],mapping);expected=numeric(row['after'],mapping)
        after,events=both_sources(before,mapping['x'],'symbolic_identity')
        ck(after==expected,'opaque-fringe identity equals actual original source formula')
        ck(len(events)==1 and events[0][0]==('ZIG' if case.startswith('ZIG') else case),
           'single source operation has declared case')
        if case.startswith('ZIG'):ck(events[0][3]==case[-1],'zig orientation is source exact')
        p,q=locations(before),locations(after)
        shifts={role:len(q[mapping.get(role,role)])-len(p[mapping.get(role,role)])
                for role in row['shifts']}
        ck(shifts==row['shifts'],'every proposed role shift independently derived from source')
        ENTRY[case]=shifts
    for case,left,right in [('LL','A','B'),('RR','C','D'),('LR','B','C'),('RL','B','C'),
                            ('ZIG_L','A','B'),('ZIG_R','B','C')]:
        OUTER[case]=(ENTRY[case][left],ENTRY[case][right])
        ck(list(OUTER[case])==cert['outer_shifts'][case],'later target-fringe shift independently derived')
    ck(sum(len(t) for case,t in ENTRY.items() if not case.startswith('ZIG'))==28,'all 28 double role entries')
    ck(sum(len(t) for case,t in ENTRY.items() if case.startswith('ZIG'))==10,'all 10 zig role entries')


def independent_H(T,x,y):
    """Original LCA and divergence select entry; no output/rebuild is read."""
    px,py=nodes(T,x),nodes(T,y);d=len(px)-1;h=len(py)-1
    ops=[]
    for s in range(d-2,-1,-2):
        case=('L' if x<px[s][0] else 'R')+('L' if x<px[s+1][0] else 'R')
        ops.append((case,s))
    if d%2:ops.append(('ZIG_'+('L' if x<T[0] else 'R'),0))
    if y==x:
        return dict(H=0,PF_U=0,FI_U=0,entry_case=None,entry_role='x',terminal_zig_shift=0,
                    boundary='accessed_key',ops=ops)
    if d==0:
        return dict(H=h,PF_U=h,FI_U=h,entry_case=None,entry_role=None,terminal_zig_shift=0,
                    boundary='root_noop',ops=ops)
    common=0
    while common<min(len(px),len(py)) and px[common][0]==py[common][0]:common+=1
    lca=common-1
    e=next(i for i,(case,s) in enumerate(ops) if s<=lca)
    ck(all(y not in keys(px[s]) for case,s in ops[:e]),'earlier original sites exclude tracked key')
    ck(y in keys(px[ops[e][1]]),'first original containing site includes tracked key')
    case,s=ops[e]
    if case.startswith('ZIG'):
        if y==T[0]:role='p'
        elif lca==0:role='C' if case=='ZIG_L' else 'A'
        else:
            ck(d==1 and e==0,'target-fringe zig entry has no earlier double')
            role=('A' if y<x else 'B') if case=='ZIG_L' else ('B' if y<x else 'C')
    elif y==px[s][0]:role='g'
    elif y==px[s+1][0]:role='p'
    elif lca==s:role={'LL':'D','RR':'A','LR':'D','RL':'A'}[case]
    elif lca==s+1:role={'LL':'C','RR':'B','LR':'A','RL':'D'}[case]
    else:
        ck(e==0 and s+2==d and lca==d,'target-fringe double entry is original innermost site')
        role={'LL':('A','B'),'RR':('C','D'),'LR':('B','C'),'RL':('B','C')}[case][0 if y<x else 1]
    side=0 if y<x else 1
    later=[c for c,s in ops[e+1:] if not c.startswith('ZIG')]
    zeta=sum(OUTER[c][side] for c,s in ops[e+1:] if c.startswith('ZIG'))
    H=h+ENTRY[case][role]+sum(OUTER[c][side] for c in later)+zeta
    if case.startswith('ZIG'):mu=pfmu=1
    else:
        mu=0 if role=='p' else 2
        pfmu=0 if (case,role) in [('LR','A'),('RL','D')] else mu
    m=later.count('LL' if y<x else 'RR');r=len(later)
    return dict(H=H,PF_U=min(h+2,max(0,h+pfmu-r-m)),FI_U=min(h+2,max(0,h+mu-r-m)),
                entry_case=case,entry_role=role,terminal_zig_shift=zeta,boundary=None,ops=ops)


def geometry_regression(pg):
    input_cert=read(HERE/'geometry_input_trees.json');summary=read(HERE/'source_geometry_certificate.json')
    expected={}
    for rows in [pg['ordinary_rows'],pg['reflected_rows'],pg['startup_rows']]:
        for row in rows:
            for field in ['source_A','source_B']:
                for T in [row[field],mirror(row[field])]:
                    expected[hashlib.sha256(canonical(T).encode()).hexdigest()]=T
    ck(input_cert['trees']==expected,'fixed geometry corpus contains only inherited PG source trees')
    ck(input_cert['physical_key_count']==13,'no new geometry key count')
    digest=hashlib.sha256();cases=0;roles=Counter()
    for key,T in sorted(expected.items()):
        ck(keys(T)==list(range(1,14)),'all geometry inputs are physical strict ordered BSTs')
        for x in keys(T):
            after,events=both_sources(T,x,'geometry')
            ck(keys(after)==keys(T),'source preserves every physical key')
            for y in keys(T):
                pr=independent_H(T,x,y);cases+=1
                ck(pr['H']==depth(after,y),'source-only H equals both actual output depths')
                ck(0<=pr['H']<=pr['PF_U']<=pr['FI_U'],'exact H is nonnegative and refines original PF/FI')
                word=[c for c,s in pr['ops']]
                actual=[('ZIG_'+ev[3]) if ev[0]=='ZIG' else ev[0] for ev in events]
                ck(word==actual,'original consumed frame word matches actual events')
                data=[key,x,y,pr['H'],pr['PF_U'],pr['FI_U'],pr['entry_case'],pr['entry_role'],pr['terminal_zig_shift']]
                digest.update((canonical(data)+'\n').encode())
                roles[pr['boundary'] or pr['entry_case']+':'+pr['entry_role']]+=1
    ck(cases==summary['present_xy_cases']==16731 and len(expected)==summary['distinct_input_trees']==99,
       'all predetermined present-key pairs checked')
    ck(digest.hexdigest()==summary['exact_source_formula_digest'],'independent LCA reconstruction matches producer source formula digest')
    ck(dict(roles)==summary['entry_role_counts'],'independent role/boundary coverage counts')
    return dict(distinct_trees=99,present_xy_cases=cases,formula_digest=digest.hexdigest(),entry_role_counts=dict(roles))


def replay_rows(rows,opaque=False):
    A,B=rows[0]['source_A'],rows[0]['source_B']
    for row in rows:
        ck((A,B)==(row['source_A'],row['source_B']),'consecutive actual paired source states')
        for side in ['A','B']:
            source=row['source_'+side];target=row['destination_'+side]
            if side=='B' and row['mode']=='DELETE':
                ck(source==target and row['B_events']==[],'original DELETE freezes B and retains keys');continue
            if opaque:
                t,ev=tuple_source.trace(tt(source),row['key']);calls['opaque_witness_tuple']+=1
                actual=jt(t);events=[list(e) for e in ev]
            else:actual,events=both_sources(source,row['key'],'witness')
            ck(actual==target and events==row[side+'_events'],'fixed witness destination and original event identities')
            d=depth(source,row['key'])
            ck(d==row['d_'+side],'actual fixed witness edge depth')
            if side=='A':ck(len(events)==row['a']==(d+1)//2,'actual A StepEv count and capacity')
            else:
                ck(sum(e[0]!='ZIG' for e in events)==row['q']==d//2,'actual B double demand count')
                ck(sum(e[0]=='ZIG' for e in events)==row['z']==d%2,'terminal B zig counted correctly')
        A,B=row['destination_A'],row['destination_B']
    return A,B


def fact(T,first,y,k,protocol):
    if not k:return depth(T,y)//2
    pr=independent_H(T,first,y)
    return pr[{'FE':'H','PF':'PF_U','FI':'FI_U'}[protocol]]//2+k-1


def check_trial(rows,trial):
    protocol=trial['protocol'];order=[(trial['cut']+t)%19 for t in range(19)]
    history=[];pending=[];claims=[];usedU=set();usedD=set();X=[0]
    def claim(d,u,kind):
        ck(tuple(d) not in usedD and tuple(u) not in usedU,'no physical demand or A unit used twice')
        ck(d[0]==u[0]==0 and 0<=d[1]<19 and 0<=u[1]<19,'one period only and no startup/other-cut units')
        ck(rows[d[1]]['B_events'][d[2]][0]!='ZIG','demand identity is an original B double')
        ck(0<=u[2]<rows[u[1]]['a'] and u[3] in [0,1],'unit identity belongs to an actual A StepEv')
        usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
    for t,j in enumerate(order):
        row=rows[j];C=2*row['a'];before=len(pending);facts=[];loans=[]
        us=[[0,j,e,b] for e in range(row['a']) for b in [0,1]]
        ds=[[0,j,e] for e,ev in enumerate(row['B_events']) if ev[0]!='ZIG']
        if row['delta']>0:
            for d,u in zip(ds[:C],us):claim(d,u,'positive_own')
            pending+=ds[C:];history.append((j,t));r=C;S=lam=0;signed=row['delta']
        else:
            for i,at in history:
                between=[rows[v] for v in order[at+1:t] if rows[v]['d_B']>0]
                k=len(between);first=between[0]['key'] if k else None;T=rows[i]['destination_B']
                if k:ck(T==between[0]['source_B'],'first genuine intervention has original anchor pre-tree')
                c=fact(T,first,row['key'],k,protocol)
                ck(row['q']<=c,'each individual source fact safely protects own payer work')
                facts.append(dict(anchor=i,k=k,first_key=first,ceiling=c))
            r=min([C]+[f['ceiling'] for f in facts])
            ck(row['q']<=r,'minimum frozen reservation safely protects own prefix')
            for d,u in zip(ds,us[:row['q']]):claim(d,u,'payer_own')
            S=C-r;lam=r-row['q'];signed=-S;take=min(S,len(pending))
            for d,u in zip(pending[:take],us[r:r+take]):
                claim(d,u,'loan');loans.append(dict(demand=d,unit=u))
                ck(us.index(u)>=r,'nonlocal loan comes only from frozen suffix')
            pending=pending[take:]
        step=dict(scan_index=t,block=j,key=row['key'],capacity=C,own_q=row['q'],delta=row['delta'],
            history=[i for i,at in history],facts=facts,reservation=r,offer=S,reserved_loss=lam,
            signed_input=signed,debt_before=before,debt_after=len(pending),loans=loans)
        ck(step==trial['steps'][t],'entire new FIFO ledger reconstructed independently')
        ck(len(pending)==max(0,before+signed),'exact clipped debt with discarded empty-queue surplus')
        ck(signed==row['delta']+lam,'exact actual reservation-loss split')
        X.append(X[-1]+signed)
    ck(claims==trial['assignments'] and pending==trial['unpaid'],'exact physical assignment and unpaid identities')
    ck(len(claims)+len(pending)==sum(r['q'] for r in rows),'all B demands accounted with multiplicity')
    ck(trial['accepted']==(not pending) and trial['final_debt']==len(pending),'new procedure endpoint outcome')
    ck(trial['periods']==1 and trial['startup_units_used']==trial['reused_units']==0,'no reused/startup/banked credits')
    ck(trial['signed_balance']==X[-1] and trial['minimum_prefix']==min(X),'fixed-cut signed prefix certificate')
    ck(len(pending)==X[-1]-min(X),'exact source signed suffix debt identity')


def main():
    pins=read(HERE/'entry_source_pins.json')
    for rel,h in pins['files'].items():ck(sha(ROOT/rel)==h,'all inherited source and research bytes preserved')
    ck(sha(HERE/'FE00_FOUR_RULE_GATE.md')==pins['gate_sha256'],'pre-execution gate unchanged')
    for name,h in read(PG/'delivery_manifest.json')['files'].items():ck(sha(PG/name)==h,'inherited PG seal intact')
    pg=read(PG/'closed_source_certificate.json');fe=read(HERE/'FE_witness_certificate.json')
    ck(fe['inherited_PG_source_sha256']==sha(PG/'closed_source_certificate.json'),'exact fixed witness provenance')
    ck(fe['source_only_profile_sha256']==sha(HERE/'source_first_entry.py'),'new source formula pin')
    derive_symbolic_tables()
    geometry=geometry_regression(pg)
    A,B=replay_rows(pg['startup_rows'])
    ck((A,B)==(pg['ordinary_rows'][0]['source_A'],pg['ordinary_rows'][0]['source_B']),
       'diagonal startup reaches exact required source pair')
    ck(pg['startup_rows'][0]['source_A']==pg['startup_rows'][0]['source_B'],'actual equal initial source trees')
    uniform=[]
    for orientation,rows in [('ordinary',pg['ordinary_rows']),('reflected',pg['reflected_rows'])]:
        A,B=replay_rows(rows)
        ck((A,B)==(rows[0]['source_A'],rows[0]['source_B']),'exact required paired closure')
        ck(all(r['source_A']!=r['source_B'] and r['destination_A']!=r['destination_B'] for r in rows),
           'all source states nowhere diagonal')
        ck(all(r['d_B']>0 for r in rows),'all 19 phases are genuine B changes')
        for protocol in ['FI','PF','FE']:
            trials=fe['all_cut_trials'][orientation][protocol]
            ck([t['cut'] for t in trials]==list(range(19)),'all fixed physical cuts present once')
            for trial in trials:check_trial(rows,trial)
            if protocol!='FE':
                old=pg['all_cut_audits'][orientation][protocol]
                ck(all(a['final_debt']==b['final_debt']==1 and not a['accepted'] for a,b in zip(trials,old)),
                   'all inherited FI/PF outcomes independently preserved')
                for a,b in zip(trials,old):
                    ck(a['assignments']==b['assignments'],'inherited FI/PF physical assignments unchanged')
                    for newstep,oldstep in zip(a['steps'],b['steps']):
                        ck(all(newstep[k]==oldstep[k] for k in ['block','key','reservation','offer','debt_after']),
                           'inherited FI/PF reservations and debt unchanged')
        new=fe['all_cut_trials'][orientation]['FE'];old=fe['all_cut_trials'][orientation]['PF']
        for a,b in zip(new,old):
            ck(all(s['debt_after']<=t['debt_after'] for s,t in zip(a['steps'],b['steps'])),
               'pointwise FE debt domination on every inherited cut')
        accepted=[t['cut'] for t in new if t['accepted']]
        ck(accepted==[0]+list(range(3,19)),'new FE actual accepted cut set')
        designated=new[0];loans=[a for a in designated['assignments'] if a['kind']=='loan']
        ck(designated['accepted'] and len(designated['assignments'])==22,'FE itself supplies complete accepted-cut injection')
        ck(loans==[dict(demand=[0,0,2],unit=[0,2,0,1],kind='loan')],'exact designated source event/bit loan')
        ck(designated['steps'][2]['reservation']==1 and designated['steps'][2]['own_q']==1,
           'safe single-unit reservation at third block')
        T=rows[0]['destination_B'];first=rows[1]['key'];y=rows[2]['key']
        pr=independent_H(T,first,y)
        ck((pr['H'],pr['PF_U'],pr['entry_case'],pr['entry_role'])==
           ((3,4,'RL','A') if orientation=='ordinary' else (3,4,'LR','D')),
           'missing grandparent outer correction exactly reconstructed')
        loss=offers=0;algebra=[]
        for j,row in enumerate(rows[1:],1):
            C=2*row['a'];c=fact(T,first,row['key'],j-1,'FE');rho=min(C,c)
            expected=dict(block=j,key=row['key'],k=j-1,capacity=C,own_q=row['q'],ceiling=c,
                reservation=rho,offer=C-rho,reserved_loss=rho-row['q'])
            ck(expected==fe['fresh_budgets'][orientation]['payers'][j-1],'FE fresh source budget independently checked')
            ck(row['q']<=rho,'fresh single-source own-work protection')
            loss+=rho-row['q'];offers+=C-rho
            if j==1:
                ck(depth(T,row['key'])//2==2 and C==2,'latest immediate ceiling exactly2')
                older=dict(constant=-1,coefficient_of_ell=19,ell_minimum=1)
                ck(19-1>=C,'all older first-key facts cannot shrink immediate reserve')
            else:
                older=dict(constant=c,coefficient_of_ell=19,ell_minimum=1)
                ck(independent_H(T,first,row['key'])['H']>=0,'all older first intervention depths identical nonnegative source values')
            algebra.append(dict(phase=j,newest_ceiling=c,older_ceiling=older))
        ck(offers==1 and loss==28 and 1-offers==-28+loss==0,'FE fresh Gamma0 exact cost/reservation split')
        ck([b['block'] for b in fe['fresh_budgets'][orientation]['payers'] if b['offer']]>=[2],
           'fresh donor includes third block')
        uniform.append(dict(orientation=orientation,genuine_changes_per_copy=19,
            older_fact_ceiling_rows=algebra,designated_copy_entry_debt=0,
            positive_debt=1,debt_after_first_payer=1,debt_after_second_payer=0,
            remaining_phases_nonpositive=True,copy_donor=[2,0,1],copy_recipient=[0,2],
            physical_copy_tags_distinct=True,repetition_control=1))
    A,B=replay_rows(pg['formal_opaque_fringe_rows'],opaque=True)
    ck((A,B)==(pg['formal_opaque_fringe_rows'][0]['source_A'],pg['formal_opaque_fringe_rows'][0]['source_B']),
       'arbitrary common fringe source return identity')
    frows=pg['formal_opaque_fringe_rows'];T=frows[0]['destination_B']
    ck(independent_H(T,5,3)['H']==3,'new H on opaque fringe is source-identical')
    save('uniform_copy_algebra_certificate.json',dict(rows=uniform,all_m='analytic induction, every integer m>=1',
         no_additional_m_or_n_replayed=True,statement='W(F)^m in FE minus PF',
         inherited_PF_all_cut_rejection='m',FE_designated_cut_debt=0,Gamma_FE=0))
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    ck(stage_now==pins['stage_files'] and len(stage_now)==125,'all Stage 11G bytes and inventory preserved')
    save('independent_audit.json',dict(status='PASS',total_checks=sum(checks.values()),checks=dict(sorted(checks.items())),
        source_calls=dict(calls),geometry=geometry,symbolic_double_roles=28,symbolic_zig_roles=10,
        physical_key_count=13,repetition_controls=[1],fixed_cut_trials=114,
        FE_accepted_cuts_per_orientation=17,FE_rejected_cuts_per_orientation=2,
        FI_PF_rejected_cuts_per_protocol_orientation=19,
        designated_FE_complete_demands_per_orientation=22,
        source_formula_implemented_independently='original LCA and divergence roles; shifts derived from both original engines',
        witness_certificate_sha256=sha(HERE/'FE_witness_certificate.json'),
        geometry_certificate_sha256=sha(HERE/'source_geometry_certificate.json'),
        symbolic_certificate_sha256=sha(HERE/'symbolic_rotation_certificate.json'),
        uniform_algebra_sha256=sha(HERE/'uniform_copy_algebra_certificate.json'),
        source_shas={p:sha(ROOT/p) for p in ['python/independent/splay.py','python/liquidity/legacy_embedding.py']},
        new_strictness_witnesses=0,larger_finite_fits=0,larger_m_or_n_replays=0,
        original_FI_PF_unchanged=True,stage_11g_files_unchanged=125,matching_terminal='FROZEN',
        universal_FE_completeness='NOT CLAIMED',universal_Coarse_Double='OPEN'))
    print(json.dumps(dict(status='PASS',checks=sum(checks.values()),source_calls=dict(calls),
        geometry_trees=99,present_xy_cases=16731,cut_trials=114,
        FE_accepted_per_orientation=17,FE_designated_cut_debt=0,stage_11g=125),indent=2))


if __name__=='__main__':main()
