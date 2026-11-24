"""Complete interleaved, simultaneous-scale sources; no old outputs written."""
import bisect
import importlib.util
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
sys.dont_write_bytecode=True
sys.setrecursionlimit(30000)
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
spec=importlib.util.spec_from_file_location('sealed_lifecycle_utilities',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_LIFECYCLE_20261121_V001/lifecycle.py')
OLD=importlib.util.module_from_spec(spec);spec.loader.exec_module(OLD)
START=time.process_time();TOTAL_ROTATIONS=0


def source(h, radius=2, interleavings=1, copies=2, reflected=False):
    assert h>=1 and radius>=0 and interleavings>=0 and copies>=2
    n=12*(1<<h)-3;r1=6*(1<<h)-3
    tree,nn=OLD.initial(r1,1);assert nn==n
    word=[];current=2;stages=[];probes=[];ends=[]
    a=(1<<(h+1))+1;x=a+1;y=x-2
    def keep(key,phase,walk=True):
        nonlocal current
        if walk:
            sign=2 if key>current else -2
            for k in range(current+sign,key+sign,sign):
                word.append((phase+':A_walk','D',k))
        else:
            assert abs(current-key)<=2
        word.append((phase,'K',key));current=key
        return len(word)
    for copy in range(1,copies+1):
        for i in range(1,h+1):
            r=12*(1<<(h-i))-3;scale=1<<i
            g=(1<<(h+1-i))+1
            op=keep(scale*r,f'copy{copy}:scale{i}:maximum')
            critical=keep(scale*(r-1),f'copy{copy}:scale{i}:critical')
            stages.append({'copy':copy,'depth':i,'r':r,'p':1,'q':(r-5)//4,
                           'maximum_op':op,'critical_op':critical,'g':g,
                           'birth':['B',op,(r-g)//2,0],
                           'label':[a,a+(1<<(i+1))-2]})
            if i<h:
                for rep in range(interleavings):
                    for k in [2,r,4,r-1]:
                        keep(scale*k,f'copy{copy}:scale{i}:interleave{rep}')
                free=list(range(2,r-2,2))+[r-2,r-1,r]
                for k in sorted(free,reverse=True):
                    keep(scale*k,f'copy{copy}:scale{i}:coarsen')
                stages[-1]['coarsen_end']=len(word)
        for rep in range(interleavings):
            for k in [2,9,1,8,4,7]:
                keep((1<<h)*k,f'copy{copy}:final_interleave{rep}')
        keep(y,f'copy{copy}:anchor')
        for _ in range(radius+1):keep(y,f'copy{copy}:pad_before')
        probe=keep(x,f'copy{copy}:probe',walk=False)
        for _ in range(radius+1):keep(x,f'copy{copy}:pad_after')
        probes.append({'copy':copy,'op':probe,'target':x})
        for k in range(r1,0,-1):keep(2*k,f'copy{copy}:fine_restore')
        ends.append(len(word))
    close=list(range(1,n+1))+list(range(n-1,0,-1))+OLD.builder(r1,1)
    word.extend(('outer','K',key) for key in close)
    if reflected:
        tree=OLD.mirror(tree,n)
        word=[(p,m,n+1-key) for p,m,key in word]
        for s in stages:
            lo,hi=s['label'];s['label']=[n+1-hi,n+1-lo]
        for p in probes:p['target']=n+1-p['target']
    return {'h':h,'radius':radius,'interleavings':interleavings,'copies':copies,
            'reflected':reflected,'n':n,'r1':r1,'initial':tree,'prefix':[],
            'word':word,'stages':stages,'probes':probes,'loop_end_ops':ends}


def run(s,save=True):
    global TOTAL_ROTATIONS
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    n=s['n'];A=OLD.Tree(s['initial'],n);B=OLD.Tree(s['initial'],n)
    initial=A.tuple();refs={'A':initial,'B':initial}
    events=[];rows=[];demands=[];clock=phi=0
    births=defaultdict(list);deaths=defaultdict(list)
    presence={lab:0 for lab in A.labels};aruns=defaultdict(list)
    entry={z['maximum_op']:z for z in s['stages']}
    coarsen={z['coarsen_end']:z for z in s['stages'] if 'coarsen_end' in z}
    def phiweight(lab):
        c=lab[1]-lab[0]+1
        return int(c>=3 and not (c&(c+1)))
    def primitive(actor,tree,promoted,op,step,bit,typ,target):
        nonlocal clock,phi
        global TOTAL_ROTATIONS
        clock+=1
        fixed=B if actor=='A' else A
        old=(tree.lo[promoted],tree.hi[promoted]);oldmatch=old in fixed.labels
        demoted,external,direction,removed,created=tree.rotate(promoted)
        newmatch=created in fixed.labels
        if actor=='A':
            psi_delta=int(oldmatch)-int(newmatch)
            delta=phiweight(created)*int(newmatch)-phiweight(removed)*int(oldmatch)
            aruns[removed].append((presence.pop(removed),clock));presence[created]=clock
            assert abs(delta)<=1
            if s['word'][op-1][0]!='outer':
                assert typ=='ZIG' and abs(promoted-demoted)==2
                assert all(lo==1 or hi==n or lo==hi and lo%2 for lo,hi in tree.labels)
        else:
            psi_delta=int(not newmatch)-int(not oldmatch)
            delta=phiweight(removed)*int(not oldmatch)-phiweight(created)*int(not newmatch)
            assert psi_delta in (0,-1) and removed[0]<=target<=removed[1]
            assert not created[0]<=target<=created[1]
            births[created].append((clock,len(events)));deaths[removed].append((clock,len(events)))
            if s['word'][op-1][0]!='outer':assert created[1]-created[0]+1>=3
        e={'id':[actor,op,step,bit],'clock':clock,'type':typ,'target':target,
           'promoted':promoted,'demoted':demoted,'external':external,'direction':direction,
           'removed':removed,'created':created,'psi_delta':psi_delta,
           'phi_before':phi,'phi_delta':delta,'phi_after':phi+delta}
        phi+=delta;events.append(e);TOTAL_ROTATIONS+=1
        assert TOTAL_ROTATIONS<=400000 and time.process_time()-START<=240
        return e
    def splay(actor,tree,target,op,postA):
        step=0
        while tree.parent[target]:
            step+=1;pr=tree.parent[target];gp=tree.parent[pr]
            if not gp:primitive(actor,tree,target,op,step,0,'ZIG',target)
            else:
                frame=(tree.lo[gp],tree.hi[gp])
                a='L' if tree.left[gp]==pr else 'R';b='L' if tree.left[pr]==target else 'R';typ=a+b
                e0=primitive(actor,tree,pr if a==b else target,op,step,0,typ,target)
                e1=primitive(actor,tree,target,op,step,1,typ,target)
                if actor=='B':demands.append({'id':[op,step],'frame':frame,'type':typ,
                    'neutral':e0['psi_delta']==e1['psi_delta']==0,'interior':frame[0]>1 and frame[1]<n,'postA_clock':postA})
        return step
    for op,(phase,mode,target) in enumerate(s['word'],1):
        clock+=1;startphi=phi
        if op in entry:
            st=entry[op];want,nn=OLD.initial(st['r'],st['depth']);assert nn==n
            if s['reflected']:want=OLD.mirror(want,n)
            assert B.tuple()==OLD.frozen(want)
            assert B.depth(target)==st['r']-1
        ad=A.depth(target);before=len(events);ac=splay('A',A,target,op,None)
        refs['A'],refevents=OLD.REF.trace(refs['A'],target)
        assert A.tuple()==refs['A'] and ac==len(refevents)==(ad+1)//2
        clock+=1;postA=clock;phia=phi;middle=len(events)
        bd=B.depth(target) if mode=='K' else 0
        if mode=='K':
            bc=splay('B',B,target,op,postA)
            refs['B'],refevents=OLD.REF.trace(refs['B'],target)
            assert B.tuple()==refs['B'] and bc==len(refevents)==(bd+1)//2
            assert phi==-sum(phiweight(lab) for lab in B.labels-A.labels)
        clock+=1
        rows.append({'id':op,'phase':phase,'mode':mode,'target':target,'a':ac,'a_depth':ad,
                     'q_B':bd//2,'z_B':bd%2,'A_rotations':middle-before,'B_rotations':len(events)-middle,
                     'postA_clock':postA,'end_clock':clock,'phi_start':startphi,'phi_postA':phia,'phi_postB':phi})
        if op in coarsen:
            st=coarsen[op];want,nn=OLD.initial((st['r']-3)//2,st['depth']+1)
            if s['reflected']:want=OLD.mirror(want,n)
            assert nn==n and B.tuple()==OLD.frozen(want)
        if op in s['loop_end_ops']:assert A.tuple()==B.tuple()==initial
    assert A.tuple()==B.tuple()==initial and phi==0
    period=clock
    for lab,start in presence.items():aruns[lab].append((start,period))
    for dem in demands:
        dem['U_int']=False
        if not dem['neutral'] or not dem['interior']:continue
        lab=tuple(dem['frame']);end=dem['postA_clock']
        j=bisect.bisect_left([a for a,_ in births[lab]],end)-1
        gamma,ge=births[lab][j];glap=0 if j>=0 else -1;gamma+=glap*period
        k=bisect.bisect_left([a for a,_ in deaths[lab]],gamma%period)-1
        kap,ke=deaths[lab][k];klap=glap+(0 if k>=0 else -1);kap+=klap*period
        assert kap<gamma<end
        absent=not OLD.overlaps(aruns[lab],kap,end,period)
        dem.update(Gamma=events[ge]['id'],Gamma_clock=gamma,Gamma_lap=glap,
                   kappa=events[ke]['id'],kappa_clock=kap,kappa_lap=klap,
                   full_Pi_A_absent=absent,U_int=absent)
    byevent={tuple(e['id']):e for e in events}
    keepops=[r['id'] for r in rows if r['mode']=='K']
    def gap_units(hit):
        k=bisect.bisect_left(keepops,hit)-1;previous=keepops[k]
        if k<0:previous-=len(rows)
        ops={(t-1)%len(rows)+1 for t in range(previous+1,hit+1)}
        return [e['id'] for e in events if e['id'][0]=='A' and e['id'][3]==0 and e['id'][1] in ops]
    probes=[]
    for probe in s['probes']:
        op=probe['op'];seeds=[]
        for stage in s['stages']:
            if stage['copy']!=probe['copy']:continue
            e=byevent[tuple(stage['birth'])];lab=tuple(stage['label'])
            assert tuple(e['created'])==lab and lab[1]-lab[0]+1==(1<<(stage['depth']+1))-1
            nxt=next((c,idx) for c,idx in deaths[lab] if c>e['clock'])
            assert events[nxt[1]]['id'][1]==op
            assert not any(mode=='K' and lab[0]<=target<=lab[1] for _,mode,target in s['word'][stage['maximum_op']:op-1])
            seeds.append({'birth':e['id'],'label':lab,'depth':stage['depth'],'first_hit':op,
                          'first_death':events[nxt[1]]['id']})
        assert len(seeds)==s['h']
        k=keepops.index(op);window=keepops[k-s['radius']:k+s['radius']+1]
        assert len(window)==2*s['radius']+1
        resources=[]
        for hit in window:resources+=gap_units(hit)
        resources=sorted(set(map(tuple,resources)))
        assert resources==[('A',op,1,0)] and rows[op-1]['a']==1
        chosen=[]
        for j in range(1,(s['h']-1)//2+1):
            dem=next(z for z in demands if z['id']==[op,j]);index=2*j+1
            stage=next(z for z in s['stages'] if z['copy']==probe['copy'] and z['depth']==index)
            assert tuple(dem['frame'])==tuple(stage['label']) and dem['Gamma']==stage['birth']
            if probe['copy']>=2:assert dem['U_int']
            chosen.append(dem)
        probes.append({**probe,'selected_seed_runs':seeds,'allowed_original_KEEP_window':window,
                       'all_real_A_resource_units':resources,'seed_count':len(seeds),'A_capacity_units':len(resources),
                       'forced_internal_U_doubles':chosen,'probe_U_count':sum(z['U_int'] for z in demands if z['id'][0]==op)})
    totals={k:sum(row[k] for row in rows) for k in ['a','q_B','z_B','A_rotations','B_rotations']}
    totals.update(operations=len(rows),real_rotations=len(events),U_int=sum(z['U_int'] for z in demands),
                  inner_leaf_births=0,simultaneous_selected_scales=s['h'],source_pair_closed=True)
    name=f"H{s['h']}_rho{s['radius']}_Y{s['interleavings']}_copies{s['copies']}"+('_mirror' if s['reflected'] else '')
    result={'name':name,'parameters':{k:s[k] for k in ['h','radius','interleavings','copies','reflected','n','r1']},'totals':totals,'probe_certificates':probes}
    if save:
        (HERE/(name+'_complete_witness.json')).write_text(json.dumps({'source':s,'rows':rows,'real_rotations':events,
            'all_B_double_records':demands,'period_clock':period,'result':result},separators=(',',':')),encoding='utf-8')
    print(json.dumps({'name':name,**totals,'seed_to_one_A_load':s['h']}),flush=True)
    return result


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    cases=[(1,0,1,2,False),(2,1,1,2,False),(3,2,1,2,False),
           (4,3,1,2,False),(5,4,1,2,False),(4,2,2,2,False),
           (4,2,1,2,True)]
    results=[run(source(*case)) for case in cases]
    out={'passed':True,'sources':results,'cpu_seconds':time.process_time()-START,'producer_rotations':TOTAL_ROTATIONS,
         'claim':'Finite complete-source audit of a symbolic all-h Hall obstruction, not a universal cost refutation.'}
    (HERE/'SOURCE_AUDIT.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'sources':len(results),'producer_rotations':TOTAL_ROTATIONS,'cpu_seconds':out['cpu_seconds']}))


if __name__=='__main__':main()
