"""Independent immutable reconstruction of every original witness event.

This checker imports no producer or previous replay. Full physical BSTs are
rebuilt from the original word by functional bottom-up path frames. Cached
interval endpoints are exact structural data, not hashes or projected trees.
"""
import bisect
import gzip
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
START = time.process_time()


@dataclass(frozen=True, slots=True, eq=False)
class Node:
    k: int
    l: object
    r: object
    lo: int
    hi: int


def node(k,l=None,r=None):
    return Node(k,l,r,l.lo if l else k,r.hi if r else k)


def lab(v):
    return (v.lo,v.hi)


def right(v):
    w = v.l
    return node(w.k,w.l,node(v.k,w.r,v.r))


def left(v):
    w = v.r
    return node(w.k,node(v.k,v.l,w.l),w.r)


def rebuild(t,target,emit,double):
    frames = []
    cur = t
    while cur.k != target:
        if target < cur.k:
            frames.append((cur.k,'L',cur.r))
            cur = cur.l
        else:
            frames.append((cur.k,'R',cur.l))
            cur = cur.r
        assert cur is not None
    depth = len(frames)
    step = 0
    while frames:
        step += 1
        pk,ps,sibling = frames.pop()
        p = node(pk,cur,sibling) if ps=='L' else node(pk,sibling,cur)
        if not frames:
            result = right(p) if ps=='L' else left(p)
            demoted = result.r if ps=='L' else result.l
            emit(step,0,'ZIG',cur,p,demoted)
            cur = result
            continue
        gk,gs,other = frames.pop()
        g = node(gk,p,other) if gs=='L' else node(gk,other,p)
        typ = gs+ps
        fullframe = lab(g)
        if gs==ps:
            result = right(g) if gs=='L' else left(g)
            demoted = result.r if gs=='L' else result.l
            first = emit(step,0,typ,p,g,demoted)
            result2 = right(result) if gs=='L' else left(result)
            demoted2 = result2.r if gs=='L' else result2.l
            second = emit(step,1,typ,cur,result,demoted2)
        else:
            result = right(p) if ps=='L' else left(p)
            demoted = result.r if ps=='L' else result.l
            first = emit(step,0,typ,cur,p,demoted)
            upper = node(gk,result,other) if gs=='L' else node(gk,other,result)
            result2 = right(upper) if gs=='L' else left(upper)
            demoted2 = result2.r if gs=='L' else result2.l
            second = emit(step,1,typ,result,upper,demoted2)
        double(step,typ,fullframe,first,second)
        cur = result2
    assert cur.k == target
    return cur,depth


def check_vine(t,n,reflected):
    for k in (range(n,0,-1) if reflected else range(1,n+1)):
        assert t is not None and t.k == k
        assert (t.r if reflected else t.l) is None
        t = t.l if reflected else t.r
    assert t is None


def verify(file):
    with gzip.open(file,'rt',encoding='utf-8') as f:
        w = json.load(f)
    s = w['source']; p,q,n = s['p'],s['q'],s['n']; mirrored=s['reflected']
    assert n == 2**(p+1)*(q+1)+1 and s['prefix']==[]
    t = None
    for k in (range(1,n+1) if mirrored else range(n,0,-1)):
        t = node(k,t,None) if mirrored else node(k,None,t)
    trees = {'A':t,'B':t}
    raw = [('prep','D',k) for k in range(2,n+1)]
    marked = {n+1-2**j for j in range(p+1)}
    raw += [('critical','K' if k in marked else 'D',k) for k in range(n,0,-1)]
    raw += [('forward','K',k) for k in range(1,n+1)]
    raw += [('reverse','K',k) for k in range(n-1,0,-1)]
    expected = [(phase,mode,n+1-k if mirrored else k) for phase,mode,k in raw]
    assert expected == [tuple(z) for z in s['word']]
    assert {x for _,mode,x in expected if mode=='K'} == set(range(1,n+1))
    saved = w['real_rotations']; pos=clock=A=Q=DB=psi=0
    bset={(1,k) if mirrored else (k,n) for k in range(1,n+1)}
    a_signs=Counter()
    births,deaths,changes = defaultdict(list),defaultdict(list),defaultdict(list)
    doubles=[]; aevents=[]; nontrivial=set()
    for op,(phase,mode,target) in enumerate(expected,1):
        clock += 1; ac=qc=0
        for actor in ('A','B') if mode=='K' else ('A',):
            if actor=='B':
                clock += 1; postA=clock
            oldroot = trees[actor].k
            def emit(step,bit,typ,promoted,pivot,demoted):
                nonlocal clock,pos,DB,psi
                clock += 1
                e=saved[pos]; pos+=1
                ident=[actor,op,step,bit]
                assert e['id']==ident and e['clock']==clock
                assert (e['type'],e['target'],e['promoted'],e['demoted']) == (typ,target,promoted.k,pivot.k)
                assert tuple(e['removed'])==lab(promoted) and tuple(e['created'])==lab(demoted)
                if actor=='A':
                    assert typ=='ZIG' and step==1 and bit==0 and pivot.k==oldroot and abs(target-oldroot)==1
                    assert e['old_root']==oldroot and e['new_root']==target
                    changes[lab(promoted)].append((clock,False,ident))
                    changes[lab(demoted)].append((clock,True,ident))
                    aevents.append((ident,oldroot,target))
                    delta=int(lab(promoted) in bset)-int(lab(demoted) in bset)
                    assert e['psi_delta']==delta
                    a_signs[delta]+=1;psi+=delta;assert psi>=0
                    return 0
                nontrivial.add(op)
                lo,hi=lab(demoted);r=trees['A'].k
                common=(lo==1 and hi<r) or (hi==n and lo>r) or (lo,hi)==(1,n)
                delta=-int(common)
                assert e['psi_delta']==delta
                assert promoted.lo<=target<=promoted.hi and not lo<=target<=hi
                DB-=delta
                psi+=delta;assert psi>=0
                assert lab(promoted) in bset and lab(demoted) not in bset
                bset.remove(lab(promoted));bset.add(lab(demoted))
                births[(lo,hi)].append((clock,ident))
                deaths[lab(promoted)].append((clock,ident))
                return delta
            def double(step,typ,frame,a,b):
                if actor=='B':
                    doubles.append({'id':[op,step],'type':typ,'frame':frame,
                                    'neutral':a==b==0,'postA_clock':postA})
            trees[actor],depth=rebuild(trees[actor],target,emit,double)
            if actor=='A':
                ac=(depth+1)//2;A+=ac
                assert depth in (0,1)
            else:
                qc=depth//2;Q+=qc
        if mode!='K':
            clock+=1;postA=clock
        clock+=1
        row=w['rows'][op-1]
        assert (row['op'],row['a'],row['q_B'],row['postA_clock'],row['end_clock'])==(op,ac,qc,postA,clock)
        assert time.process_time()-START<=240
    assert pos==len(saved) and clock==w['period_clock']
    for tree in trees.values():
        check_vine(tree,n,mirrored)
    assert A==4*(n-1) and len(aevents)==A and psi==0
    assert a_signs[1]-a_signs[-1]==DB and sum(a_signs.values())==A
    period=clock
    def previous(seq,boundary):
        cycle,local=divmod(boundary,period)
        idx=bisect.bisect_left([c for c,_ in seq],local)-1
        if idx<0:cycle-=1;idx=len(seq)-1
        c,eid=seq[idx]
        return c+cycle*period,eid
    def a_at(lab,t):
        local=t%period
        idx=bisect.bisect_right([c for c,_,_ in changes[lab]],local)-1
        if idx>=0:return changes[lab][idx][1]
        return lab[0]==1 if mirrored else lab[1]==n
    records={tuple(z['id']):z for z in w['all_B_double_records']}
    assert len(records)==len(doubles)
    counts=Counter();alphas=[];betas=[]
    for d in doubles:
        z=records[tuple(d['id'])]
        for k in ('id','type','neutral','postA_clock'):
            assert z[k]==d[k]
        assert tuple(z['frame'])==d['frame']
        kind='nonneutral'
        if d['neutral']:
            interval=d['frame'];end=d['postA_clock']
            assert interval!=(1,n)
            gamma,gid=previous(births[interval],end)
            kap,kid=previous(deaths[interval],gamma)
            assert 0<end-kap<=period and not a_at(interval,kap) and not a_at(interval,end)
            assert (z['Gamma_clock'],z['kappa_clock'],z['Gamma'],z['kappa'])==(gamma,kap,gid,kid)
            enters=[(c+lap*period,ident) for c,present,ident in changes[interval] for lap in (-1,0) if present and kap<c+lap*period<=end]
            if enters:
                ca,alpha=max(enters)
                cb,beta=min((c+lap*period,ident) for c,present,ident in changes[interval] for lap in (-1,0) if not present and ca<c+lap*period<=end)
                assert z['alpha']==alpha and z['beta']==beta
                alphas.append(tuple(alpha));betas.append(tuple(beta));kind='exposed'
            else:
                kind='U_bd' if interval[0]==1 or interval[1]==n else 'U_int'
        assert z['class']==kind
        counts[kind]+=1
    assert len(alphas)==len(set(alphas)) and len(betas)==len(set(betas))
    assert counts['nonneutral']<=DB<=2*A and counts['exposed']<=A and counts['U_bd']<=2*len(nontrivial)<=2*A
    assert Q<=6*A+counts['U_int']
    result=w['result'];neighbors=set();selected=result['selected']
    assert len(selected)==p*q
    for d in selected:
        i,j=d['i'],d['j'];a=n+2-2**(p+1)*(i+1);b=n-2**(j-1)
        ident=(n-1+2**j,2**(p-j)*(i+1)-1)
        interval=(a,b) if not mirrored else (n+1-b,n+1-a)
        assert tuple(d['id'])==ident and tuple(d['frame'])==interval
        z=records[ident];assert z['class']=='U_int' and tuple(z['frame'])==interval
        assert (d['Gamma'],d['kappa'])==(z['Gamma'],z['kappa'])
        predicted={a-1,2*n+1-a,2*n-1+a,4*n-a,b,2*n-b,2*n+b,4*n-1-b}
        # Complete two-vine induction: the actual initial vine plus ONLY
        # adjacent root zigs above proves this for every physical A snapshot.
        def region(root):
            lo,hi=interval
            return -1 if root<lo else 1 if root>hi else 0
        actual={tuple(eid) for eid,r0,r1 in aevents if region(r0)!=region(r1)}
        assert actual=={('A',op,1,0) for op in predicted}=={tuple(e) for e in d['donors']}
        assert len(actual)==8
        neighbors.update(actual)
    assert len(neighbors)==4*(p+q)
    opt=(p*q+4*(p+q)-1)//(4*(p+q))
    assert result['optimal_capacity']==opt
    assigned={};load=Counter()
    for idx,eid in result['assignment']:
        assert idx not in assigned and tuple(eid) in {tuple(a) for a in selected[idx]['donors']}
        assigned[idx]=tuple(eid);load[tuple(eid)]+=1
    assert len(assigned)==p*q and max(load.values())<=opt
    if opt>1:assert p*q>(opt-1)*len(neighbors)
    assert (result['A'],result['Q_B'],result['D_B'],result['K_B'],result['partition'])==(A,Q,DB,len(nontrivial),dict(counts))
    assert (result['P_A'],result['N_A'],result['T_A'])==(a_signs[1],a_signs[-1],a_signs[0])
    out={'file':file.name,'p':p,'q':q,'reflected':mirrored,'n':n,'original_ops':len(expected),
         'original_real_rotations':pos,'A':A,'Q_B':Q,'partition':dict(counts),
         'selected_original_U':p*q,'all_period_cover_neighbors':len(neighbors),'exact_optimum_K':opt,
         'complete_full_pair_closure':True,'all_original_events':True,'full_cyclic_Pi':True,
         'actual_SET_sign_telescope':True,
         'independent_integer_assignment_and_lower_bound':True}
    print(json.dumps(out),flush=True)
    return out


def main():
    out=[verify(p) for p in sorted(HERE.glob('H_*.json.gz'))]
    assert len(out)==5
    result={'passed':True,'implementation':'Independent immutable functional full BST replay; no producer imports; same-agent implementation independence, not external/formal certification.',
            'cases':out,'total_ops':sum(x['original_ops'] for x in out),
            'total_real_rotations':sum(x['original_real_rotations'] for x in out),
            'cpu_seconds':time.process_time()-START}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}))


if __name__=='__main__':
    main()
