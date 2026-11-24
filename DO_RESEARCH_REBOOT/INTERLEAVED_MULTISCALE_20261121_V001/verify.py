"""Immutable original-event verification; does not import the new producer.

Uses pinned, read-only immutable primitive helpers from the earlier checkpoint.
Recomputes full trees, SETs, costs, potentials, cyclic exposures and Hall cuts.
"""
import bisect
import importlib.util
import json
import sys
import time
from collections import Counter,defaultdict
from pathlib import Path
sys.dont_write_bytecode=True
sys.setrecursionlimit(30000)
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
spec=importlib.util.spec_from_file_location('sealed_immutable_primitives',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_LIFECYCLE_20261121_V001/verify.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
START=time.process_time()


def nu(z):
    z=abs(z);assert z
    return (z&-z).bit_length()-1


def depth(lab,origin):
    width=lab[1]-lab[0]+2
    if width<4 or width&(width-1) or (lab[0]-origin-1)%width:return None
    return width.bit_length()-2


def verify(file):
    w=json.loads(file.read_text(encoding='utf-8'));s=w['source']
    n=s['n'];h=s['h'];assert n==12*(1<<h)-3 and s['r1']==6*(1<<h)-3
    assert s['prefix']==[] and s['copies']>=2
    init,nn=V.expected_tree(s['r1'],1);assert nn==n
    if s['reflected']:init=V.reflected(init,n)
    assert V.tupleize(s['initial'])==init
    word=s['word'];assert {x for _,m,x in word if m=='K'}==set(range(1,n+1))
    trees={'A':init,'B':init};sets={a:V.label_set(t) for a,t in trees.items()};initial_A=sets['A'].copy()
    saved=w['real_rotations'];cursor=clock=Atotal=Qtotal=Ztotal=0
    a_changes=defaultdict(list);bb=defaultdict(list);bd=defaultdict(list);positive_A=defaultdict(list);doubles=[]
    entry={z['maximum_op']:z for z in s['stages']};coarsen={z['coarsen_end']:z for z in s['stages'] if 'coarsen_end' in z}
    for op,(phase,mode,target) in enumerate(word,1):
        clock+=1
        if op in entry:
            st=entry[op];wanted,nn=V.expected_tree(st['r'],st['depth'])
            if s['reflected']:wanted=V.reflected(wanted,n)
            assert nn==n and trees['B']==wanted
        before_phi=V.score(sets['A'],sets['B']);postA=None
        ac=qc=zc=0
        for actor in ['A','B'] if mode=='K' else ['A']:
            if actor=='B':clock+=1;postA=clock;post_phi=V.score(sets['A'],sets['B'])
            tr=V.path(trees[actor],target);ed=len(tr)-1
            if actor=='A':ac=(ed+1)//2;Atotal+=ac
            else:qc,zc=ed//2,ed%2;Qtotal+=qc;Ztotal+=zc
            step=0
            while len(tr)>1:
                step+=1
                if len(tr)==2:typ='ZIG';pivots=[target];frame=None
                else:
                    gp,pr,x=tr[-3:];aa='L' if gp[1] is pr else 'R';b='L' if pr[1] is x else 'R';typ=aa+b
                    pivots=[pr[0],target] if aa==b else [target,target]
                    frame=max(V.label_set(gp),key=lambda z:z[1]-z[0])
                ds=[]
                for bit,pivot in enumerate(pivots):
                    clock+=1;e=saved[cursor];identifier=[actor,op,step,bit]
                    assert e['id']==identifier and e['clock']==clock and e['type']==typ and e['promoted']==pivot and e['target']==target
                    ptr=V.path(trees[actor],pivot);parent=ptr[-2]
                    side='R' if parent[1] is not None and parent[1][0]==pivot else 'L'
                    assert parent[0]==e['demoted'] and e['direction']==('RIGHT' if side=='R' else 'LEFT')
                    phi0=V.score(sets['A'],sets['B']);psi0=len(sets['B']-sets['A']);old=sets[actor]
                    trees[actor]=V.turn(trees[actor],parent[0],side);sets[actor]=V.label_set(trees[actor])
                    lost,born=old-sets[actor],sets[actor]-old;assert len(lost)==len(born)==1
                    lost,born=next(iter(lost)),next(iter(born));assert tuple(e['removed'])==lost and tuple(e['created'])==born
                    phi1=V.score(sets['A'],sets['B']);delta=len(sets['B']-sets['A'])-psi0
                    assert (phi0,phi1,phi1-phi0,delta)==(e['phi_before'],e['phi_after'],e['phi_delta'],e['psi_delta'])
                    ds.append(delta)
                    if actor=='A':
                        a_changes[lost].append((clock,False));a_changes[born].append((clock,True))
                        if bit==0:positive_A[op].append(identifier)
                        if phase!='outer':assert typ=='ZIG' and abs(pivot-parent[0])==2 and all(lo==1 or hi==n or lo==hi and lo%2 for lo,hi in sets['A'])
                    else:
                        assert lost[0]<=target<=lost[1] and not born[0]<=target<=born[1]
                        bb[born].append((clock,identifier));bd[lost].append((clock,identifier))
                        if phase!='outer':assert born[1]-born[0]+1>=3
                    cursor+=1
                if actor=='B' and frame is not None:doubles.append({'id':[op,step],'frame':frame,'type':typ,'neutral':ds==[0,0],
                       'interior':frame[0]>1 and frame[1]<n,'postA_clock':postA})
                tr=V.path(trees[actor],target)
        if mode!='K':clock+=1;postA=clock;post_phi=V.score(sets['A'],sets['B'])
        clock+=1;row=w['rows'][op-1]
        assert (ac,qc,zc,postA,clock)==(row['a'],row['q_B'],row['z_B'],row['postA_clock'],row['end_clock'])
        assert (before_phi,post_phi,V.score(sets['A'],sets['B']))==(row['phi_start'],row['phi_postA'],row['phi_postB'])
        if op in coarsen:
            st=coarsen[op];wanted,nn=V.expected_tree((st['r']-3)//2,st['depth']+1)
            if s['reflected']:wanted=V.reflected(wanted,n)
            assert nn==n and trees['B']==wanted
        if op in s['loop_end_ops']:assert trees['A']==trees['B']==init
        assert time.process_time()-START<=240
    assert cursor==len(saved) and clock==w['period_clock'] and trees['A']==trees['B']==init
    period=clock;records={tuple(z['id']):z for z in w['all_B_double_records']};assert len(records)==len(doubles)
    all_u=[]
    for dem in doubles:
        rec=records[tuple(dem['id'])]
        for key in ['frame','type','neutral','interior','postA_clock']:assert V.tupleize(dem[key])==V.tupleize(rec[key])
        eligible=False
        if dem['neutral'] and dem['interior']:
            lab=dem['frame'];end=dem['postA_clock']
            gamma,gid=max((t+lap*period,ident) for t,ident in bb[lab] for lap in (-1,0) if t+lap*period<end)
            kap,kid=max((t+lap*period,ident) for t,ident in bd[lab] for lap in (-2,-1,0) if t+lap*period<gamma)
            assert (gamma,kap,gid,kid)==(rec['Gamma_clock'],rec['kappa_clock'],rec['Gamma'],rec['kappa'])
            changes=a_changes[lab];j=bisect.bisect_right([t for t,_ in changes],kap%period)-1
            present=changes[j][1] if j>=0 else lab in initial_A
            has_birth=any(flag and kap<t+lap*period<=end for t,flag in changes for lap in (-2,-1,0))
            eligible=not (present or has_birth)
            assert eligible==rec['full_Pi_A_absent']
        assert eligible==rec['U_int']
        if eligible:all_u.append(rec)
    keepops=[i for i,(_,m,_) in enumerate(word,1) if m=='K']
    gaps={}
    for j,hit in enumerate(keepops):
        previous=keepops[j-1]-(len(word) if j==0 else 0)
        gaps[hit]=[unit for op in range(previous+1,hit+1) for unit in positive_A[(op-1)%len(word)+1]]
    def firsthit(birth):
        lab=tuple(birth['created']);t=birth['clock']
        death,ident=min((c+lap*period,eid) for c,eid in bd[lab] for lap in (0,1) if c+lap*period>t)
        op=ident[1];assert gaps[op]
        return op,ident
    event_lookup={tuple(z['id']):z for z in saved}
    for probe in w['result']['probe_certificates']:
        hit=probe['op'];wanted=[]
        for stage in s['stages']:
            if stage['copy']!=probe['copy']:continue
            birth=event_lookup[tuple(stage['birth'])];assert birth['created']==stage['label']
            assert stage['g']==(1<<(h+1-stage['depth']))+1 and stage['birth'][2]==(stage['r']-stage['g'])//2
            retired,dead=firsthit(birth);assert retired==hit
            assert not any(mode=='K' and birth['created'][0]<=key<=birth['created'][1] for _,mode,key in word[stage['maximum_op']:hit-1])
            wanted.append({'birth':birth['id'],'label':tuple(birth['created']),'depth':stage['depth'],'first_hit':hit,'first_death':dead})
        assert len(wanted)==len(probe['selected_seed_runs'])
        for actual,record in zip(wanted,probe['selected_seed_runs']):
            assert actual.keys()==record.keys()
            assert all(V.tupleize(actual[key])==V.tupleize(record[key]) for key in actual)
        k=keepops.index(hit);window=keepops[k-s['radius']:k+s['radius']+1]
        resource=sorted({tuple(unit) for op in window for unit in gaps[op]})
        assert window==probe['allowed_original_KEEP_window'] and resource==[('A',hit,1,0)]
        assert V.tupleize(resource)==V.tupleize(probe['all_real_A_resource_units'])
        for j,dem in enumerate(probe['forced_internal_U_doubles'],1):
            actual=records[(hit,j)]
            assert actual==dem and tuple(actual['frame'])==wanted[2*j]['label']
            if probe['copy']>=2:assert actual['U_int']
    # Derived bounded-alignment diagnostic: a single origin per source, not one
    # independently chosen origin for each demand or size.
    origin=n+1 if s['reflected'] else 0
    birth_band={k:Counter() for k in range(5)};U_band={k:Counter() for k in range(5)}
    for birth in saved:
        if birth['id'][0]!='B':continue
        d=depth(birth['created'],origin)
        if d is None:continue
        hit,_=firsthit(birth);delta=d-nu(word[hit-1][2]-origin);assert delta>=0
        for cap in range(5):
            if delta<=cap:birth_band[cap][tuple(gaps[hit][0])]+=1
    for dem in all_u:
        d=depth(dem['frame'],origin)
        if d is None:continue
        hit=dem['id'][0];delta=d-nu(word[hit-1][2]-origin);assert delta>=0
        for cap in range(5):
            if delta<=cap:U_band[cap][tuple(gaps[hit][0])]+=1
    bands=[]
    for cap in range(5):
        assert max(birth_band[cap].values(),default=0)<=cap+1 and max(U_band[cap].values(),default=0)<=cap+1
        bands.append({'alignment_cap':cap,'canonical_birth_count':sum(birth_band[cap].values()),'birth_A_load':max(birth_band[cap].values(),default=0),
                      'original_U_frame_count':sum(U_band[cap].values()),'U_A_load':max(U_band[cap].values(),default=0)})
    assert (Atotal,Qtotal,Ztotal,len(all_u))==tuple(w['result']['totals'][k] for k in ['a','q_B','z_B','U_int'])
    return {'file':file.name,'h':h,'n':n,'operations':len(word),'real_rotations':cursor,'A':Atotal,'Q_B':Qtotal,
            'U_int':len(all_u),'seed_to_one_A_Hall_demand':h,'Hall_A_units':1,
            'forced_genuine_U_in_copy2':(h-1)//2,'full_cyclic_Pi_independently_verified':True,
            'exact_pair_closure':True,'all_stage_full_tree_coarsenings_verified':True,'alignment_band_audit':bands}


def main():
    results=[verify(f) for f in sorted(HERE.glob('*_complete_witness.json'))]
    out={'passed':True,'sources':results,'cpu_seconds':time.process_time()-START,
         'total_original_operations':sum(z['operations'] for z in results),'total_original_rotations':sum(z['real_rotations'] for z in results),
         'limitations':'Same-agent independent immutable event code, using previously sealed immutable primitive helpers. Not external peer review or a proof assistant.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'sources':len(results),'operations':out['total_original_operations'],'real_rotations':out['total_original_rotations'],'cpu_seconds':out['cpu_seconds']}))


if __name__=='__main__':main()
