"""Fresh physical/SET model; immutable tuple checks bind every operation.

Forest construction is not performed here. Complete child-pointer state codes
are injective encodings, not hashes or physically contracted trees.
"""
from base0 import *
from fast_physics import FullTree
from independent_path_audit import checked_access
sys.path.insert(0,str(REPO/'python'))
from independent import splay as ind

def to_tuple(st):
    out={None:ind.LEAF};stack=[(st['root'],False)]
    while stack:
        k,done=stack.pop();l,r=st['children'][str(k)]
        if done:out[k]=ind.node(k,out[l],out[r])
        else:
            stack.append((k,True))
            if l is not None:stack.append((l,False))
            if r is not None:stack.append((r,False))
    return out[st['root']]

def tuple_data(t,bits):
    labs={};ranges={};stack=[(t,False)]
    while stack:
        z,done=stack.pop()
        if z==ind.LEAF:continue
        _,k,l,r=z
        if not done:stack.extend([(z,True),(l,False),(r,False)]);continue
        labs[k]=bits.get(k,0)|(labs[l[1]] if l!=ind.LEAF else 0)|(labs[r[1]] if r!=ind.LEAF else 0)
        ranges[k]=(ranges[l[1]][0] if l!=ind.LEAF else k,ranges[r[1]][1] if r!=ind.LEAF else k)
    return labs,ranges

def replay(s,store_states=True):
    n=len(s['initial_B']['children']);assert set(map(int,s['initial_B']['children']))==set(range(1,n+1))
    a=FullTree(s['initial_A']);b=FullTree(s['initial_B'])
    aa=to_tuple(s['initial_A']);bb=to_tuple(s['initial_B']);a0,b0=a.code,b.code
    # Root changes determine genuine KEEP occurrences, with no approximation.
    last=b.root;M=set()
    for tag,x in s['operations']:
        if tag=='K':
            if x!=last:M.add(x)
            last=x
    S=set()
    for x in M:S.update(b.path(x))
    bits={k:1<<(k-1) for k in S};Sbits=sum(bits.values())
    masks=[(1<<i)-1 for i in range(n+1)]
    def label(tree,k):return Sbits&(masks[tree.hi[k]]^masks[tree.lo[k]-1])
    counts={id(tree):Counter(label(tree,k) for k in range(1,n+1) if label(tree,k)) for tree in (a,b)}
    events=[];doubles={};boundaries=[];A=Q=0;pool={};states=[]
    def sid(code):
        if not store_states:return None
        if code not in pool:pool[code]=len(states);states.append(format(code,'x'))
        return pool[code]
    current={};old_rotate=FullTree.rotate
    def tracked(tree,u,side,other,actor):
        k=current['cursor'];expect=current['expected'][k];current['cursor']+=1
        j,bit,case,pivot,direction,promoted,frame=expect
        assert (u,side,actor)==(pivot,direction,current['actor'])
        v=(tree.r if side else tree.l)[u];c=tree.p[u] or None
        middle=(tree.l if side else tree.r)[v] or None
        assert v==promoted
        deleted={(u,v,side)};added={(v,u,1-side)}
        if c is not None:deleted.add((c,u,int(tree.r[c]==u)));added.add((c,v,int(tree.r[c]==u)))
        if middle is not None:deleted.add((v,middle,1-side));added.add((u,middle,side))
        before=[label(tree,u),label(tree,v)]
        candidate=set(before);ct=counts[id(tree)];before_present={lab for lab in candidate if lab and ct[lab]}
        precode=tree.code
        old_rotate(tree,u,side,other,actor)
        after=[label(tree,u),label(tree,v)];candidate.update(after)
        before_present.update(lab for lab in after if lab and ct[lab])
        for lab in before:
            if lab:ct[lab]-=1
        for lab in after:
            if lab:ct[lab]+=1
        assert all(ct[x]>=0 for x in candidate)
        post_present={lab for lab in candidate if lab and ct[lab]}
        lost=before_present-post_present;created=post_present-before_present
        others=counts[id(other)]
        sign=(sum(others[x]>0 for x in lost)-sum(others[x]>0 for x in created)) if actor=='A' else (
              sum(others[x]==0 for x in created)-sum(others[x]==0 for x in lost))
        if actor=='B':assert sign<=0
        ev={'id':[actor,current['t'],j,bit],'time':len(events)+1,'actor':actor,
            'case':case,'target':current['x'],'pivot':u,'promoted':v,'external':c,'middle':middle,
            'side':side,'deleted':sorted(deleted),'added':sorted(added),'lost':sorted(lost),
            'created':sorted(created),'sign':sign,'demoted_label':label(tree,u),'frame':frame}
        events.append(ev)
        if actor=='B' and case!='ZIG':
            p=(current['t'],j);z=doubles[p]
            z['events'].append(ev['time']);z['signs'].append(sign)
            if bit==0:z['pre_step_state']=sid(precode)
            if bit==1:z['post_step_state']=sid(tree.code)
        return sign
    def access(tree,tu,x,other,actor,t):
        path=tree.path(x);depth=len(path)-1;expected=[]
        for j in range(1,depth//2+1):
            g,p=path[-1-2*j],path[-2*j]
            side=int(x>p);z=int(p>g);case=('R' if z else 'L')+('R' if side else 'L')
            F=label(tree,g)
            rotations=[(g,z,p),(p,side,x)] if side==z else [(p,side,x),(g,z,x)]
            for bit,(u,ss,v) in enumerate(rotations):expected.append((j,bit,case,u,ss,v,F))
            if actor=='B':
                doubles[t,j]={'id':(t,j),'g':g,'p':p,'F':F,'case':case,'events':[],'signs':[],
                    'physical_frame_interval':[tree.lo[g],tree.hi[g]],'target':x}
        if depth%2:
            expected.append((depth//2+1,0,'ZIG',path[0],int(x>path[0]),x,None))
        current.update(cursor=0,expected=expected,actor=actor,t=t,x=x)
        out,steps,q,guard,_,_=checked_access(tree,tu,x,other,actor)
        assert current['cursor']==len(expected)
        labs,ranges=tuple_data(out,bits)
        assert all(ranges[k]==(tree.lo[k],tree.hi[k]) for k in range(1,n+1))
        assert Counter(v for v in labs.values() if v)==+counts[id(tree)]
        if actor=='B':
            for j in range(1,q+1):
                d=doubles[t,j];g=d['g'];p=d['p']
                d['J']=labs[g];d['P_output']=labs[p]
                d['physical_J_interval']=list(ranges[g]);d['physical_P_interval']=list(ranges[p])
                for tt in d['events']:
                    ev=events[tt-1];assert ev['demoted_label']==labs[ev['pivot']]
        return out,steps,q,path
    FullTree.rotate=tracked
    try:
        for t,(tag,x) in enumerate(s['operations'],1):
            start=len(events);apre=sid(a.code);bpre=sid(b.code)
            aa,steps,_,apath=access(a,aa,x,b,'A',t);A+=steps;postA=len(events)
            postaa=sid(a.code);bpath=None;q=0
            if tag=='K':
                # Bind each original pre-B frame to the independent immutable tree.
                prelabs,_=tuple_data(bb,bits)
                bb,_,q,bpath=access(b,bb,x,a,'B',t);Q+=q
                for j in range(1,q+1):assert doubles[t,j]['F']==prelabs[doubles[t,j]['g']]
                assert not q or set(bpath)<=S
            boundaries.append({'t':t,'tag':tag,'x':x,'start_time':start,'post_A_time':postA,
                'end_time':len(events),'a':steps,'q':q,'A_path':apath,'B_path':bpath,
                'pre_A_state':apre,'post_A_state':postaa,'pre_B_state':bpre,'post_B_state':sid(b.code)})
        assert (a.code,b.code)==(a0,b0),(s['name'],'not complete paired closure')
    finally:FullTree.rotate=old_rotate
    assert sum(e['actor']=='A' for e in events)<=2*A
    if 'A' in s:assert A==s['A'] and Q==s['Q_B']
    if 'trace_hash' in s:assert digest(events)==s['trace_hash'],s['name']
    r=SimpleNamespace(source=s,ops=s['operations'],events=events,doubles=doubles,
        boundaries=boundaries,A=A,Q=Q,T=len(events),bits=bits,S=S,M=M)
    r.label_keys=lambda lab:[k for k in range(1,n+1) if bits.get(k,0)&lab]
    return r,{'format':'exact complete labelled child-pointer codes','n':n,'bits_per_pointer':(n+1).bit_length(),
        'code_definition':'root at bit2*n*b; child k left/right at bit(2*k-2)*b/(2*k-1)*b; zero is null; all codes hexadecimal',
        'states':states,'all_complete_operation_states_checked_against_immutable_engine':True,
        'all_S_carrier_SETS_checked_at_every_actor_boundary':True,'original_event_sha256':digest(events)}

def prefix_check(s):
    diagonal=s.get('diagonal_initial')
    if diagonal is None:
        assert s['initial_A']==s['initial_B'] and not s.get('reaching_prefix')
        diagonal=s['initial_A']
    a=FullTree(diagonal);b=FullTree(diagonal)
    aa=to_tuple(diagonal);bb=aa;A=0
    for t,(tag,x) in enumerate(s.get('reaching_prefix',[]),1):
        aa,steps,_,_,_,_=checked_access(a,aa,x,b,'A');A+=steps
        if tag=='K':bb,*_=checked_access(b,bb,x,a,'B')
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    return {'operations':len(s.get('reaching_prefix',[])),'actual_A_StepEv_excluded':A,
            'complete_reached_pair_verified':True}
