"""Independent original-source validation of the FE02 paired continuation."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
PG=BASE/'route_c_pf_positive_gap_closure_20261101_v001'
FE=BASE/'route_c_fe01_first_entry_20261101_v001'
OLD=BASE/'route_c_fe02_saturated_return_20261101_v001'
checks=Counter();calls=Counter()


def ck(v,label):
    if not v:raise AssertionError(label)
    checks[label]+=1
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,v):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
tu=load('paired_independent_tuple',ROOT/'python/independent/splay.py')
po=load('paired_independent_pointer',ROOT/'python/liquidity/legacy_embedding.py')


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
def keys(t):return [] if t is None or isinstance(t,str) else keys(t[1])+[t[0]]+keys(t[2])
def path(t,y):
    out=[]
    while t is not None:
        ck(not isinstance(t,str),'source query never enters opaque fringe')
        out.append(t[0])
        if t[0]==y:return out
        t=t[1 if y<t[0] else 2]
    raise AssertionError('present key')
def depth(t,y):return len(path(t,y))-1
def rel(t,u,v):
    return 1 if u in path(t,v)[:-1] else -1 if v in path(t,u)[:-1] else 0
def discord(A,B):
    return {tuple(p) for p in combinations(keys(A),2) if rel(A,*p)!=rel(B,*p)}
def marker_ancestors(t,tag,anc=()):
    if t is None:return None
    if isinstance(t,str):return anc if t==tag else None
    a=marker_ancestors(t[1],tag,anc+(t[0],))
    return a if a is not None else marker_ancestors(t[2],tag,anc+(t[0],))


def both(T,x,label):
    a,ae=tu.trace(tt(T),x);b,be=po.splay_trace(pt(T),x)
    calls[label+'_tuple']+=1;calls[label+'_pointer']+=1
    a,b=jt(a),jp(b);ae=[list(e) for e in ae];be=[[e['case'],e['lo'],e['hi'],e['orient']] for e in be]
    ck(a==b and ae==be,'both unmodified original sources agree')
    return a,ae
def symbolic(T,x):
    a,e=tu.trace(tt(T),x);calls['symbolic_tuple']+=1;return jt(a),[list(v) for v in e]


def verify_rows(rows,opaque=False):
    A,B=rows[0]['source_A'],rows[0]['source_B']
    for row in rows:
        ck((A,B)==(row['source_A'],row['source_B']),'full source chronology and legality')
        for side in ['A','B']:
            T=row['source_'+side]
            if side=='B' and row['mode']=='DELETE':
                ck(row['destination_B']==T and not row['B_events'],'DELETE freezes B with no phantom demands');continue
            out,ev=symbolic(T,row['key']) if opaque else both(T,row['key'],'fixed_rows')
            ck(out==row['destination_'+side] and ev==row[side+'_events'],'full actual source destinations and event indexing')
            d=depth(T,row['key']);ck(d==row['d_'+side],'original source access depth')
            if side=='A':ck(len(ev)==row['a']==(d+1)//2,'actual A StepEvs and two-unit supply')
            else:
                ck(sum(e[0]!='ZIG' for e in ev)==row['q']==d//2,'actual B double demands')
                ck(sum(e[0]=='ZIG' for e in ev)==row['z']==d%2,'terminal B zig and genuine change semantics')
        A,B=row['destination_A'],row['destination_B']
    return A,B


def far_side_geometry():
    corpus=read(FE/'geometry_input_trees.json');cases=0
    ck(len(corpus['trees'])==99,'unchanged 99-tree inherited geometry corpus')
    for T in corpus['trees'].values():
        r=T[0];ck(keys(T)==list(range(1,14)),'same physical13-key geometry corpus')
        for x in keys(T):
            out,ev=both(T,x,'far_side_geometry')
            if x==r:continue
            epsilon=depth(out,r)
            expected=2 if ev[-1][0] in ['LL','RR'] else 1
            ck(epsilon==expected and epsilon in [1,2],'old-root epsilon independently source-derived')
            for y in keys(T):
                if y==r or (y-r)*(x-r)<0:
                    ck(depth(out,y)-depth(T,y)==epsilon,'exact old-root/far-side whole-splay shift')
                    cases+=1
    for a in [1,2]:
        for b in [1,2]:ck(b-2*a<=0 and ((b-2*a==0)==((a,b)==(1,2))),'all paired epsilon cases and unique equality')
    return cases


def verify_deep(orientation,rows,data):
    N=len(rows)
    for rec in data['discordance_steps']:
        j=rec['block'];r=rows[j];before=discord(r['source_A'],r['source_B']);after=discord(r['destination_A'],r['destination_B'])
        x=r['key'];removed={p for p in before if x in p}
        transfer=len([p for p in after if x not in p])-len([p for p in before if x not in p])
        ck(all(x not in p for p in after),'all target-pair disagreements disappear after common splay')
        ck(len(removed)>=abs(r['d_B']-r['d_A']),'target discordance dominates ancestor path-length difference')
        ck((rec['D_before'],rec['D_after'],rec['target_removed'],rec['other_transfer'],rec['change'])==
           (len(before),len(after),len(removed),transfer,len(after)-len(before)),
           'exact target-removal and non-target transfer decomposition')
        ck(len(after)-len(before)==transfer-len(removed),'exact D transition identity')
    for records in data['tracked_source_steps'].values():
        for s in records:verify_step(rows[s['block']],s)
    for ret in data['returns']:
        j=ret['return_block'];y=ret['key'];L=ret['gap'];prev=ret['previous_same_block']
        expected=next(k for k in range(1,N+1) if rows[(j-k)%N]['key']==y)
        ck(L==expected and prev==(j-L)%N,'actual consecutive same-key cyclic return')
        steps=ret['steps'];ck([s['block'] for s in steps]==[(prev+t)%N for t in range(1,L)],'one physical set of source intermediate occurrences')
        for s in steps:verify_step(rows[s['block']],s)
        retreat=all(s['old_root_or_far_side'] for s in steps)
        ck(retreat==ret['retreat_only'],'retreat classification from actual ordered root motions')
        if retreat:
            da=sum(s['epsilon_A'] for s in steps);db=sum(s['epsilon_B'] for s in steps)
            ck((da,db)==(rows[j]['d_A'],rows[j]['d_B']),'exact paired retreat depth sums')
            ck(db<=2*da and rows[j]['delta']<=0,'retreat-only return cannot be a positive block')
            equality=all((s['epsilon_A'],s['epsilon_B'])==(1,2) for s in steps) and L%2==1
            ck((rows[j]['delta']==0)==equality,'complete retreat saturation equality/parity condition')
            witnesses=[]
            for at,s in enumerate(steps):
                pair=s['equality_separator_pair']
                if pair is None:continue
                witnesses.append(tuple(pair))
                r,p=pair
                for later in steps[at:]:
                    row=rows[later['block']]
                    ck(rel(row['destination_A'],r,p)==1 and rel(row['destination_B'],r,p)==-1,
                       'separator inversion persists through every later retreat')
                ck(rel(rows[j]['source_A'],r,p)==1 and rel(rows[j]['source_B'],r,p)==-1,
                   'separator inversion persists to return pre-state')
            ck(len(witnesses)==len(set(witnesses)),'distinct retreat equality separator witnesses')
        if rows[j]['delta']>0:
            g=rows[j]['d_B']-2*rows[j]['d_A'];departure=steps[0]['paired_gap_after']
            gains=[s for s in steps[1:] if s['paired_gap_shift']>0]
            ck(g>=2 and sum(s['paired_gap_shift'] for s in gains)>=g-departure,
               'positive return must restore sufficient paired gap after departure')
            for s in gains:ck(not s['far_side'] and s['A_shift']<=0,'positive gap creation occurs on approach side with nonincreasing A depth')
    r4=data['returns'][4]
    ck(r4['retreat_only'] and (r4['A_return_depth'],r4['B_return_depth'])==(2,3),'block4 donor from strict paired retreat gap')
    target=3 if orientation=='ordinary' else 11
    p=data['tracked_source_steps'][str(target)][1]
    ck((p['A_shift'],p['B_shift'],p['before_A_depth'],p['before_B_depth'],p['after_B_depth'])==(0,0,1,3,3),
       'block2 donor reconstructed from exact paired first-intervention depths')
    ck((p['source_B_profile']['entry_shift'],sum(p['source_B_profile']['later_double_shifts']))==(1,-1),
       'exact grandparent fringe entry plus outer loss for block2')


def verify_step(row,s):
    r=row['source_A'][0];x=row['key'];y=s['key']
    ck(row['source_B'][0]==r,'common source root at actual KEEP macro boundary')
    hA,hB=depth(row['source_A'],y),depth(row['source_B'],y)
    aA,aB=depth(row['destination_A'],y),depth(row['destination_B'],y)
    eA,eB=depth(row['destination_A'],r),depth(row['destination_B'],r)
    ck((s['before_A_depth'],s['before_B_depth'],s['after_A_depth'],s['after_B_depth'])==(hA,hB,aA,aB),
       'all tracked depths independently read from verified original source transitions')
    ck((s['A_shift'],s['B_shift'],s['paired_gap_before'],s['paired_gap_after'],s['paired_gap_shift'])==
       (aA-hA,aB-hB,hB-2*hA,aB-2*aA,(aB-hB)-2*(aA-hA)), 'exact paired tracked shift')
    ck((s['epsilon_A'],s['epsilon_B'])==(eA,eB),'paired epsilon types independently reconstructed')
    far=(y-r)*(x-r)<0
    ck(s['far_side']==far and s['old_root_or_far_side']==(y==r or far),'ordered old-root/far-side predicate')
    if y==r or far:ck(aA-hA==eA and aB-hB==eB and s['paired_gap_shift']<=0,'paired far-side nonincrease exact source theorem')
    pair=s['equality_separator_pair']
    if (eA,eB)==(1,2):
        p=path(row['source_B'],x)[1]
        ck(pair==[r,p] and min(r,x)<p<max(r,x),'separator from original outer B parent and key interval')
        ck(rel(row['source_A'],r,p)==rel(row['source_B'],r,p)==1,'separator pair was originally agreed under shared root')
        ck(rel(row['destination_A'],r,p)==1 and rel(row['destination_B'],r,p)==-1,'equality step creates actual paired ancestor inversion')
    else:ck(pair is None,'no unspecified separator source')


def check_physical(rows,claims,donor):
    usedU=set();usedD=set();loans=[]
    for c in claims:
        d,u=c['demand'],c['unit'];_,j,e=d;_,pool,ae,bit=u
        ck(tuple(d) not in usedD and tuple(u) not in usedU,'no physical donor or demand reused')
        ck(d[0]==u[0]==0 and 0<=j<19 and 0<=pool<19,'one source period no startup or other-cut units')
        ck(0<=ae<rows[pool]['a'] and bit in [0,1] and rows[j]['B_events'][e][0]!='ZIG','actual event and capacity-bit identities')
        usedD.add(tuple(d));usedU.add(tuple(u))
        if pool!=j:loans.append(c);ck((j,e,pool,ae,bit)==(0,2,donor,0,1),'correct distinct source-selected loan')
    ck(len(usedD)==22 and len(loans)==1,'full22-demand injection for each separate donor certificate')


def check_counter(cert):
    rows=cert['actual_closed_rows'];A,B=verify_rows(rows)
    ck(A==B==rows[0]['source_A']==rows[0]['source_B'],'discordance control is a fully reachable closed source history')
    edge=rows[cert['saturated_edge_index']]
    ck((edge['a'],edge['q'],edge['delta'])==(1,2,0),'actual saturated zero-excess counteredge')
    ck(all(r['delta']<=0 for r in rows) and sum(r['delta'] for r in rows)<0,'no CD or FE02 counterexample claimed by diagnostic cycle')
    before=discord(edge['source_A'],edge['source_B']);after=discord(edge['destination_A'],edge['destination_B'])
    ck((len(before),len(after))==(3,4),'marked-core discordance increases on a reachable saturated edge')
    connector=[r['key'] for r in rows[:cert['saturated_edge_index']]]
    ck(connector==cert['A_DELETE_connector']==[5,3,5,1] and all(r['mode']=='DELETE' for r in rows[:4]),
       'actual original DELETE connector; not mislabeled as root-child-only')
    ck(cert['reachability_refinement_sha256']==sha(HERE/'PC00B_REACHABILITY_REFINEMENT_GATE.md'),'provenance refinement gate recorded')
    sym=cert['symbolic_edge']
    for side in ['A','B']:
        out,ev=symbolic(sym['source_'+side],5)
        ck(out==sym['destination_'+side] and ev==sym[side+'_events'],'opaque arbitrary fringe edge is exact original source identity')
    bA=set(marker_ancestors(sym['source_A'],'F'));bB=set(marker_ancestors(sym['source_B'],'F'))
    aA=set(marker_ancestors(sym['destination_A'],'F'));aB=set(marker_ancestors(sym['destination_B'],'F'))
    ck(len(bA^bB)==0 and aA^aB=={1,3},'all fringe descendants generate exactly the two claimed discordances')
    ck(cert['symbolic_D_before']==dict(constant=3,coefficient_of_fringe_size=0) and
       cert['symbolic_D_after']==dict(constant=4,coefficient_of_fringe_size=2),'exact unbounded fringe polynomial, no size fit')
    # Same fixed legal word is a literal closed identity for arbitrary F.
    A=B=sym['source_B']
    for row in rows:
        A,ev=symbolic(A,row['key'])
        if row['mode']=='KEEP':B,ev=symbolic(B,row['key'])
    ck(A==B==sym['source_B'],'arbitrary-fringe diagonal reachability and paired closure')


def main():
    pins=read(HERE/'entry_source_pins.json')
    for rel,h in pins['files'].items():ck(sha(ROOT/rel)==h,'all inherited bytes preserved')
    ck(sha(HERE/'PC00_FOUR_RULE_GATE.md')==pins['gate_sha256'],'original continuation gate preserved')
    pg=read(PG/'closed_source_certificate.json');deep=read(HERE/'walk_deep_certificate.json')
    ck(deep['source_PG_sha256']==sha(PG/'closed_source_certificate.json'),'mandatory source provenance')
    far_cases=far_side_geometry()
    verify_rows(pg['startup_rows'])
    FE_cert=read(FE/'FE_witness_certificate.json');oldroot=read(OLD/'root_return_certificate.json')
    for orientation,rows in [('ordinary',pg['ordinary_rows']),('reflected',pg['reflected_rows'])]:
        A,B=verify_rows(rows);ck((A,B)==(rows[0]['source_A'],rows[0]['source_B']),'unchanged W paired return')
        verify_deep(orientation,rows,deep['data'][orientation])
        check_physical(rows,FE_cert['all_cut_trials'][orientation]['FE'][0]['assignments'],2)
        check_physical(rows,oldroot['regression'][orientation]['direct_injection']['assignments'],4)
    # Generic same-block transfer payment fails already inside W.
    s4=deep['data']['ordinary']['tracked_source_steps']['4'][1]
    s6=deep['data']['ordinary']['tracked_source_steps']['6'][1]
    ck(pg['ordinary_rows'][1]['delta']==0 and (s4['paired_gap_shift'],s6['paired_gap_shift'])==(2,1),
       'saturated source helper can increase paired depth gaps without spare own capacity')
    counter=read(HERE/'discordance_obstruction_certificate.json');check_counter(counter)
    qualitative=read(HERE/'qualitative_return_control.json')
    A,B=verify_rows(qualitative['startup_rows']);ck((A,B)==(qualitative['closed_rows'][0]['source_A'],qualitative['closed_rows'][0]['source_B']),
       'qualitative control reachable from actual diagonal right vine')
    A,B=verify_rows(qualitative['closed_rows']);ck(A==B==qualitative['closed_rows'][0]['source_A'],'qualitative four-key exact closure')
    ck(all(not r['retreat_only'] for r in qualitative['returns']) and not qualitative['FE02_counterexample'],
       'unqualified closure does not force retreat-only interval; no FE02 refutation')
    # Verify the order predicates independently of the producer return routine.
    word=[1,3,2,4]
    for j,y in enumerate(word):
        seq=[word[(j+t)%4] for t in range(1,4)]
        ck(any((y-seq[t-1])*(seq[t]-seq[t-1])>=0 for t in range(1,3)),
           'qualitative return failure checked by exact key-order inequalities')
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    current={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    ck(current==pins['stage_files'] and len(current)==125,'all125 Stage11G files and inventory preserved')
    save('independent_audit.json',dict(status='PASS',checks=dict(checks),total_checks=sum(checks.values()),source_calls=dict(calls),
        existing_geometry_trees=99,existing_geometry_key_count=13,far_side_contexts=far_cases,
        new_counter_control_key_count=5,new_qualitative_control_key_count=4,
        new_control_scope='fixed source falsification, no larger fit or CD counterexample search',
        paired_retreat_lemma='PROVED—UNIVERSAL at stated ordered scope',separator_witnesses='verified',
        discordance_monotonicity='REFUTED—EXACT on reachable saturated transition',
        discordance_unbounded_change='1+2|F|, source symbolic identity',
        actual_FE02_or_CD_counterexample_claimed=False,FE02_CD='OPEN',universal_Coarse_Double='OPEN',
        witness_hashes={n:sha(HERE/n) for n in ['walk_deep_certificate.json','discordance_obstruction_certificate.json','qualitative_return_control.json']},
        original_FE_PG_unchanged=True,matching_terminal='FROZEN',larger_finite_fits=0,larger_repetition_replays=0,
        source_provenance_search='fixed five-core A-only connector; restricted root-child attempt retained; no paired graph used'))
    print(json.dumps(dict(status='PASS',checks=sum(checks.values()),source_calls=dict(calls),far_side_contexts=far_cases,
        paired_retreat_source_theorem='verified',saturated_D_change='1+2|F|',FE02_CD='OPEN',stage_11g=125),indent=2))


if __name__=='__main__':main()
