"""Immutable primitive reconstruction, independent of pointer ancestry logs."""
from collections import defaultdict
from sharp01_validate import tuple_state,ref,validate

def path(t,x):
    ans=[]
    while t!=ref.LEAF:
        _,v,l,r=t;ans.append(v)
        if v==x:return ans
        t=l if x<v else r
    raise AssertionError('absent physical key')

def state(t):
    children={};todo=[] if t==ref.LEAF else [t]
    while todo:
        _,v,l,r=todo.pop();children[str(v)]=[None if l==ref.LEAF else l[1],None if r==ref.LEAF else r[1]]
        todo.extend(c for c in (l,r) if c!=ref.LEAF)
    return {'root':None if t==ref.LEAF else t[1],'children':dict(sorted(children.items(),key=lambda z:int(z[0])))}

def pairs(t):
    result=set();todo=[] if t==ref.LEAF else [(t,())]
    while todo:
        tr,anc=todo.pop();_,x,l,r=tr;result.update((v,x) for v in anc)
        todo.extend((c,anc+(x,)) for c in (l,r) if c!=ref.LEAF)
    return result

def rotate(t,p,side):
    _,x,l,r=t
    if p!=x:return ref.node(x,rotate(l,p,side),r) if p<x else ref.node(x,l,rotate(r,p,side))
    child=(l,r)[side];assert child!=ref.LEAF
    _,v,cl,cr=child
    return ref.node(v,cl,ref.node(x,cr,r)) if side==0 else ref.node(v,ref.node(x,l,cl),cr)

def verify(ledger):
    src=ledger['source'];validate(src,ledger)
    a,b=tuple_state(src['initial_A']),tuple_state(src['initial_B']);before_pair=(a,b)
    unit_events={};states={};saved={};byop=defaultdict(list);checked=0
    for e in ledger['events']:byop[e['id'][0],e['id'][1]].append(e)
    def save(t):
        # Pure tuple keys establish exact tree equality without a hash assumption.
        if t not in saved:
            sid=f'V{len(saved)}';saved[t]=sid;states[sid]=state(t)
        return saved[t]
    for op,(tag,x) in enumerate(src['operations'],1):
        for actor in ('A','B') if tag=='K' else ('A',):
            t=a if actor=='A' else b;expected,frame_steps=ref.trace(t,x);events=iter(byop[actor,op]);step=0
            while len(path(t,x))>1:
                pp=path(t,x);step+=1;p=pp[-2];g=pp[-3] if len(pp)>2 else None;s=int(x>p)
                if g is None:plan=[(p,s)]
                else:
                    z=int(p>g);plan=[(g,z),(p,s)] if z==s else [(p,s),(g,z)]
                for bit,(pivot,side) in enumerate(plan):
                    e=next(events);assert e['id']==[actor,op,step,bit] and e['pivot']==pivot and e['side']==side
                    pre=t;old=pairs(t);t=rotate(t,pivot,side);new=pairs(t)
                    add=new-old;lost=old-new
                    assert lost=={(e['ancestry_removed'][0],v) for v in e['ancestry_removed'][1]}
                    assert add=={(e['ancestry_added'][0],v) for v in e['ancestry_added'][1]}
                    if actor=='A':unit_events[tuple(e['id'])]={'id':e['id'],'pre_A':save(pre),'post_A':save(t),
                        'created_pairs':[list(z) for z in sorted(add)],'lost_pairs':[list(z) for z in sorted(lost)]}
                    checked+=1
            assert t==expected and next(events,None) is None
            if actor=='A':a=t
            else:b=t
        row=ledger['operations'][op-1]
        assert a==tuple_state(ledger['states'][row['post'][0]]) and b==tuple_state(ledger['states'][row['post'][1]])
    assert (a,b)==before_pair
    return {'status':'PASS','primitive_rotations_checked':checked,'A_real_rotation_geometry':list(unit_events.values()),
            'complete_A_states':states,'implementation':'pure immutable primitive rotations plus separate original immutable frame replay'}
