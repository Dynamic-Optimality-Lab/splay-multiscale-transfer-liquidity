"""New FE02 source audit; previous FE01 check counts are not reused."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
PG=BASE/'route_c_pf_positive_gap_closure_20261101_v001'
FE=BASE/'route_c_fe01_first_entry_20261101_v001'
checks=Counter();calls=Counter()


def ck(v,label):
    if not v:raise AssertionError(label)
    checks[label]+=1
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


tu=load('fe02_original_tuple',ROOT/'python/independent/splay.py')
po=load('fe02_original_pointer',ROOT/'python/liquidity/legacy_embedding.py')
inherited_fe=load('frozen_fe01_source',FE/'source_first_entry.py')
under_test=load('new_root_formula_under_test',HERE/'source_root_budget.py')


def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return [t[1],jt(t[2]),jt(t[3])]
def pt(t,parent=None):
    if t is None:return None
    p=po.mknode(t[0],p=parent);p['l']=pt(t[1],p);p['r']=pt(t[2],p);return p
def jp(t):return None if t is None else [t['k'],jp(t['l']),jp(t['r'])]
def nodes(t,y):
    p=[]
    while t is not None:
        ck(not isinstance(t,str),'queried source path stays outside opaque fringe')
        p.append(t)
        if t[0]==y:return p
        t=t[1 if y<t[0] else 2]
    raise AssertionError('present source key')
def depth(t,y):return len(nodes(t,y))-1
def keys(t):return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])


def both(t,x,label):
    a,ae=tu.trace(tt(t),x);b,be=po.splay_trace(pt(t),x)
    calls[label+'_tuple']+=1;calls[label+'_pointer']+=1
    ja,jb=jt(a),jp(b)
    ea=[list(e) for e in ae];eb=[[e['case'],e['lo'],e['hi'],e['orient']] for e in be]
    ck(ja==jb and ea==eb,'both original engines agree on states and event identities')
    return ja,ea


def root_law_corpus():
    corpus=read(FE/'geometry_input_trees.json');counts=Counter()
    ck(len(corpus['trees'])==99 and corpus['physical_key_count']==13,'fixed inherited geometry corpus dimensions')
    for t in corpus['trees'].values():
        ck(keys(t)==list(range(1,14)),'root-law physical source is a strict BST')
        root=t[0]
        for x in keys(t):
            predicted=under_test.old_root_departure(t,x)
            output,events=both(t,x,'root_law')
            actual=depth(output,root)
            if x==root:
                expected=0;counts['root_noop']+=1
                ck(not events and predicted['eta'] is None,'root-noop boundary')
            else:
                last=events[-1][0]
                expected=2 if last in ['LL','RR'] else 1
                counts['nontrivial']+=1;counts[last]+=1
                ck(last in ['LL','RR','LR','RL','ZIG'],'last source operation is exhaustive')
                ck(predicted['eta']==1-expected//2,'departure flag comes from actual last source operation')
            ck(actual==expected==predicted['old_root_depth'],'exact old-root depth independently source-verified')
            ck(inherited_fe.profile(t,x,root)['H']==expected,'new old-root corollary agrees with frozen exact H')
    ck(counts['root_noop']==99 and counts['nontrivial']==1188,'all predeclared root-law contexts tested')
    return dict(counts)


def replay(rows,opaque=False):
    A,B=rows[0]['source_A'],rows[0]['source_B']
    for row in rows:
        ck((A,B)==(row['source_A'],row['source_B']),'original physical paired source chronology')
        for side in ['A','B']:
            T=row['source_'+side]
            if side=='B' and row['mode']=='DELETE':
                ck(T==row['destination_B'] and row['B_events']==[],'DELETE truly freezes B');continue
            if opaque:
                out,ev=tu.trace(tt(T),row['key']);calls['opaque_control_tuple']+=1
                out=jt(out);ev=[list(e) for e in ev]
            else:out,ev=both(T,row['key'],'control')
            ck(out==row['destination_'+side] and ev==row[side+'_events'],'control original states and actual event identities')
            d=depth(T,row['key']);ck(d==row['d_'+side],'actual pre-access source depth')
            if side=='A':ck(len(ev)==row['a']==(d+1)//2,'actual A StepEvs, not depth-plus-one cost')
            else:
                ck(sum(e[0]!='ZIG' for e in ev)==row['q']==d//2,'actual B double count')
                ck(sum(e[0]=='ZIG' for e in ev)==row['z']==d%2,'genuine zero-double zig counted')
        A,B=row['destination_A'],row['destination_B']
    return A,B


def independent_return_rows(rows):
    N=len(rows);occ=defaultdict(list)
    for j,r in enumerate(rows):occ[r['key']].append(j)
    result={}
    for key,indices in occ.items():
        for at,j in enumerate(indices):
            prev=indices[at-1];L=(j-prev)%N or N;depart=(prev+1)%N;dr=rows[depart]
            ck(dr['source_B'][0]==key,'previous root is actual departure B root')
            eps=depth(dr['destination_B'],key)
            ck(eps in [1,2],'nontrivial departure leaves old root shallow')
            eta=1-eps//2;bound=L-1-eta;C=2*rows[j]['a']
            p=nodes(dr['source_B'],dr['key']);dirs=['L' if p[k+1][0]<p[k][0] else 'R' for k in range(len(p)-1)]
            profile=dict(access_depth=len(p)-1,original_first_directions=dirs[:2],old_root_depth=eps,eta=eta,
                reason='even_outer_same_side' if dr['B_events'][-1][0] in ['LL','RR'] else 'final_zig_or_outer_cross')
            result[j]=dict(block=j,key=key,previous_same_block=prev,cyclic_gap=L,departure_block=depart,
                departure_source_profile=profile,eta=eta,B_double_source_bound=bound,actual_a=rows[j]['a'],
                actual_q=rows[j]['q'],capacity=C,forced_unused_capacity=C-min(C,bound),short_gap_donor=bound<C)
            ck(rows[j]['q']<=bound,'return source-depth bound safely dominates actual B work')
        ck(sum(result[j]['cyclic_gap'] for j in indices)==N,'each key cyclic gaps partition one period')
    output=[result[j] for j in range(N)]
    ck(sum(r['cyclic_gap'] for r in output)==len(occ)*N,'exact global cyclic gap count')
    ck(sorted(r['departure_block'] for r in output)==list(range(N)),'departure map is a physical occurrence permutation')
    return output


def check_direct(rows,trial,budget):
    usedU=set();usedD=set();loans=[]
    for c in trial['assignments']:
        d,u=c['demand'],c['unit'];_,j,be=d;_,pool,ae,bit=u
        ck(tuple(d) not in usedD and tuple(u) not in usedU,'direct injection never reuses demand or credit')
        ck(d[0]==u[0]==0 and 0<=j<19 and 0<=pool<19,'direct injection only one physical period')
        ck(0<=ae<rows[pool]['a'] and bit in [0,1],'direct credit is a real A event bit')
        ck(0<=be<len(rows[j]['B_events']) and rows[j]['B_events'][be][0]!='ZIG','direct demand is an actual B double')
        usedD.add(tuple(d));usedU.add(tuple(u))
        if c['kind']=='own':ck(j==pool,'own demand paid from same source block')
        else:
            loans.append(c);ck((j,be,pool,ae,bit)==(0,2,4,0,1),'new source-return donor has exact physical identity')
            ck(budget[4]['cyclic_gap']==3 and budget[4]['eta']==1 and budget[4]['B_double_source_bound']==1,
               'donor chosen from original root departure and return bound')
            ck(rows[4]['q']<=1<2*rows[4]['a'],'source-derived spare last unit is genuine')
    demands={(0,j,e) for j,r in enumerate(rows) for e,ev in enumerate(r['B_events']) if ev[0]!='ZIG'}
    ck(usedD==demands and len(usedD)==22 and len(loans)==1,'all 22 original B demands paid exactly once')
    ck(len(usedU)==22 and trial['unused_units']==50-22==28,'distinct capacity and unused units count')
    ck(trial['startup_units_used']==trial['reused_units']==0,'no startup or reused-period injection units')


def FE_regression(rows,trial):
    ck(trial['cut']==0 and trial['periods']==1,'inherited FE regression uses designated one-period cut')
    pending=[];history=[];claims=[]
    for j,row in enumerate(rows):
        C=2*row['a'];units=[[0,j,e,b] for e in range(row['a']) for b in [0,1]]
        demands=[[0,j,e] for e,ev in enumerate(row['B_events']) if ev[0]!='ZIG']
        if row['delta']>0:
            for d,u in zip(demands[:C],units):claims.append(dict(demand=d,unit=u,kind='positive_own'))
            pending+=demands[C:];history.append(j);reserve=C;offer=0
        else:
            cs=[]
            for i in history:
                between=[r for r in rows[i+1:j] if r['d_B']>0];k=len(between);T=rows[i]['destination_B']
                c=depth(T,row['key'])//2 if not k else inherited_fe.profile(T,between[0]['key'],row['key'])['H']//2+k-1
                cs.append(c);ck(row['q']<=c,'frozen FE source bound still protects actual work')
            reserve=min([C]+cs);offer=C-reserve
            for d,u in zip(demands,units[:row['q']]):claims.append(dict(demand=d,unit=u,kind='payer_own'))
            take=min(offer,len(pending))
            for d,u in zip(pending[:take],units[reserve:reserve+take]):claims.append(dict(demand=d,unit=u,kind='loan'))
            pending=pending[take:]
        ck(reserve==trial['steps'][j]['reservation'] and offer==trial['steps'][j]['offer'] and len(pending)==trial['steps'][j]['debt_after'],
           'unchanged FE reservation and FIFO regression')
    ck(not pending and trial['accepted'] and trial['final_debt']==0 and claims==trial['assignments'],
       'inherited FE cut remains exactly successful')


def mixed_timing(rows):
    certificates=[]
    for j in [0,1]:
        base=rows[j];x=base['key'];A,B=base['source_A'],base['source_B'];A_events=[];B_events=[];trace=[]
        for request,mode in enumerate(['DELETE','DELETE','KEEP','DELETE','KEEP']):
            beforeA,beforeB=A,B;A,ae=both(A,x,'mixed_timing')
            if mode=='KEEP':B,be=both(B,x,'mixed_timing')
            else:be=[];ck(B==beforeB,'mixed DELETE does not secretly execute B splay')
            trace.append(dict(request=request,mode=mode,key=x,source_A=beforeA,source_B=beforeB,
                destination_A=A,destination_B=B,A_events=ae,B_events=be))
            A_events+=ae;B_events+=be
        ck(A==base['destination_A'] and B==base['destination_B'],'mixed block canonical boundary pair is preserved')
        ck(A_events==base['A_events'] and B_events==base['B_events'],'mixed block complete event lists and costs preserved')
        ck(trace[0]['A_events'] and not trace[0]['B_events'],'mixed leader creates A units before any B work')
        ck(not trace[2]['A_events'] and trace[2]['B_events'],'first KEEP B work has its own later physical occurrence')
        ck(all(not t['A_events'] for t in trace[1:]) and not trace[4]['B_events'],'same-root followers genuinely create no extra pools')
        certificates.append(dict(original_block=j,mode_pattern=['DELETE','DELETE','KEEP','DELETE','KEEP'],
            A_unit_owner_request=0,B_demand_owner_request=2,trace=trace,
            a=base['a'],q=base['q'],delta=base['delta'],scope='isolated semantic block check, not a new closed witness'))
    return certificates


def main():
    pins=read(HERE/'entry_source_pins.json')
    for rel,h in pins['files'].items():ck(sha(ROOT/rel)==h,'all inherited source/research files preserved')
    ck(sha(HERE/'FE02_00_FOUR_RULE_GATE.md')==pins['gate_sha256'],'pre-execution FE02 gate unchanged')
    for name,h in read(FE/'delivery_manifest.json')['files'].items():ck(sha(FE/name)==h,'complete FE01 delivery seal intact')
    prior=read(FE/'independent_audit.json');ck(prior['status']=='PASS' and prior['total_checks']==350259,'FE01 completion verified as inherited evidence')
    extra=['DO_RESEARCH_REBOOT/02_PROVED/DIRECT_NFKS_RT2_three_keep_key_coarse_double.md',
           'DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CD_K4_four_keep_key_coarse_double.md']
    save('additional_dependency_pins.json',dict(files={p:sha(ROOT/p) for p in extra},
        status='read-only inherited small-support proof reports; old complete matrices not rerun'))
    root_counts=root_law_corpus()
    pg=read(PG/'closed_source_certificate.json');cert=read(HERE/'root_return_certificate.json')
    ck(cert['original_PG_sha256']==sha(PG/'closed_source_certificate.json'),'mandatory regression source provenance')
    ck(cert['original_FE_sha256']==sha(FE/'FE_witness_certificate.json'),'mandatory FE regression provenance')
    ck(cert['source_formula_sha256']==sha(HERE/'source_root_budget.py'),'new root formula pinned')
    A,B=replay(pg['startup_rows'])
    ck((A,B)==(pg['ordinary_rows'][0]['source_A'],pg['ordinary_rows'][0]['source_B']),'actual diagonal startup reaches recurrent pair')
    for orientation,rows in [('ordinary',pg['ordinary_rows']),('reflected',pg['reflected_rows'])]:
        A,B=replay(rows)
        ck((A,B)==(rows[0]['source_A'],rows[0]['source_B']),'exact original paired closure')
        ck([j for j,r in enumerate(rows) if r['delta']>0]==[0] and (rows[0]['a'],rows[0]['q'])==(1,3),'control has precisely one positive of required type')
        ck(sum(r['a'] for r in rows)==25 and sum(r['q'] for r in rows)==22,'control actual A25 Q22')
        ck(sum(r['delta'] for r in rows)==22-2*25==-28,'exact signed block arithmetic')
        ck(sum(-r['delta'] for r in rows if r['delta']<0)==29,'control genuine nonsaturated slack is29')
        budget=independent_return_rows(rows);rc=cert['regression'][orientation]
        ck(budget==rc['return_rows'],'root gap certificate independently reconstructed from original outputs')
        check_direct(rows,rc['direct_injection'],budget)
        FE_regression(rows,rc['inherited_FE_cut0'])
    mixed=mixed_timing(pg['ordinary_rows']);save('mixed_timing_certificate.json',dict(blocks=mixed,new_closed_witness=False))
    A,B=replay(pg['formal_opaque_fringe_rows'],opaque=True)
    ck((A,B)==(pg['formal_opaque_fringe_rows'][0]['source_A'],pg['formal_opaque_fringe_rows'][0]['source_B']),
       'unchanged arbitrary common fringe source identity')
    formal=cert['formal_budget_noncontradiction_signature']
    ck(formal['source_tree_status'].startswith('NONE PROVIDED'),'numeric signature never presented as source witness')
    ck(all(q<=L-1-eta for q,L,eta in zip(formal['q'],formal['L'],formal['eta'])),'formal signature satisfies return inequalities only')
    ck(sum(formal['L'])==formal['s']*formal['N'] and sum(formal['q'])-2*sum(formal['a'])==1,
       'formal signature demonstrates root budget alone lacks a contradiction')
    ck(cert['FE02_rigidity']==cert['FE02_CD']=='OPEN' and not cert['actual_saturated_return_found'],
       'principal theorem remains open; no source counterexample claimed')
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    ck(stage_now==pins['stage_files'] and len(stage_now)==125,'all125 Stage11G files and inventory preserved')
    save('independent_audit.json',dict(status='PASS',total_checks=sum(checks.values()),checks=dict(sorted(checks.items())),
        source_calls=dict(calls),root_departure_cases=root_counts,physical_key_count=13,root_input_trees=99,
        root_access_cases=1287,new_FE02_verification=True,inherited_FE01_checks_not_recounted=350259,
        actual_closed_positive_controls=2,control_words='ordinary W and reflection, one period each',
        mixed_semantic_block_controls=2,mixed_closed_witnesses=0,
        direct_injections=dict(demands_per_orientation=22,source_forced_donor_block=4),
        FE01_designated_cuts_preserved=True,all_m_FE01_regression='inherited analytic theorem only; m>1 is outside FE02 one-positive class',
        root_return_certificate_sha256=sha(HERE/'root_return_certificate.json'),mixed_certificate_sha256=sha(HERE/'mixed_timing_certificate.json'),
        root_law='PROVED—UNIVERSAL source corollary; fixed audit supporting evidence',
        FE02_rigidity='OPEN',FE02_CD='OPEN',universal_Coarse_Double='OPEN',
        actual_saturated_return_found=False,larger_finite_fits=0,new_key_counts=0,source_searches=0,
        larger_repetition_replays=0,stage_11g_files_preserved=125,matching_terminal='FROZEN'))
    print(json.dumps(dict(status='PASS',checks=sum(checks.values()),source_calls=dict(calls),
        root_cases=1287,mixed_controls=2,control_A=25,control_Q=22,direct_donor_block=4,
        FE02_rigidity='OPEN',FE02_CD='OPEN',stage_11g=125),indent=2))


if __name__=='__main__':main()
