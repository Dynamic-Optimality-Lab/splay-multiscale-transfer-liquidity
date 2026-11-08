"""Complete unchanged original roots for arbitrary/empty port controls."""
import sys,json,time,copy
from pathlib import Path
from types import SimpleNamespace
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_ACL01','DO_RESEARCH_REBOOT/M3_S3P01',
 'DO_RESEARCH_REBOOT/M3_G0P01','DO_RESEARCH_REBOOT/M3_H1F01',
 'DO_RESEARCH_REBOOT/M3_FRC01','DO_RESEARCH_REBOOT/M3_H2R01',
 'DO_RESEARCH_REBOOT/M3_PHI01','DO_RESEARCH_REBOOT/M2_SEP01','python/independent']
from canonical_completion_v2 import S,V,rho,CompleteOneGapPotential
from PC_TYPED_DAG import DAG
from PC_CONCRETIZE import build_envA,build_envI,build_envW,build_envBT
from PC_ROTATION_INTERPRETER import AState,splay_event,verify_path_dyn,macro_H
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from original_h2_controls import exact_witness,alpha_prefix
from experiment import D as ED,V as Box
from verify_original_compensation import high
BASE=Path('DO_RESEARCH_REBOOT/M3_ACL01')

def model(A,cuts):
    keys=tuple(S.inorder(A));assert all(k in keys for k in range(9));cuts=set(map(tuple,cuts))
    ranks={k:i for i,k in enumerate(keys)};sig=[sum(k<0 for k in keys)]+[0]*9
    assert all(k<9 for k in keys)
    am=SimpleNamespace(Ss=list(range(9)),sidx={i:i for i in range(9)},V=list(keys),rank=ranks,
      slots={},kids={},lo={},hi={},phS={},pz={},sig=sig)
    queue=[(A,0,None,None,0,0,136)];nextid=1
    while queue:
        n,i,p,side,z,l,h=queue.pop(0);k=n[1]
        am.slots[i]={'key':k,'depth':z,'par':p,'side':side};am.lo[i]=l;am.hi[i]=h;kids=[]
        for b,ch in ((0,n[2]),(1,n[3])):
            if (k,b) in cuts or (ch!=S.LEAF and z==6):
                kids.append((1,(i,b)));content=S.inorder(ch)
                am.phS[(i,b)]=[x for x in content if x>=0];am.pz[(i,b)]=[sum(x<0 for x in content)]+[0]*9
            elif ch==S.LEAF:kids.append((2,None))
            else:
                j=nextid;nextid+=1;kids.append((0,j));queue.append((ch,j,i,b,z+1,
                  l if b==0 else ranks[k]+1,ranks[k] if b==0 else h))
        am.kids[i]=tuple(kids)
    return am

def state(mu,sig,b,a):return {'mu':mu,'sigma':sig,'b':{k:b[k] for k in ('root',)+V.FIELDS},'alpha':a}
def fill(d,e,obj,mu,sig,b,a):
    V.put(d,e,obj.mu,mu);V.fillB(d,e,obj.b,b)
    for i,(k,s,x) in enumerate(a):V.put(d,e,obj.ak[i],k);V.put(d,e,obj.aS[i],bool(s));V.put(d,e,obj.aI[i],x)
    for n,v in zip(obj.sig,sig):V.put(d,e,n,v)

def low(d,L,A,B,cuts,word,label,mu=341,junk=False,padding=False):
    am=model(A,cuts);e=V.blank(d);build_envA(e,am,set(range(9)),'MXLw');build_envI(e,am,set(range(9)),'MXLv')
    slots={v['key']:i for i,v in am.slots.items()};aw=[];bw=[];ac=A;bc=B;Btrees=[B];H=0
    ix=lambda x:9 if x<0 else x
    for mode,x in word:
        ap,ad=V.path(ac,x);assert len(ad)<=4 and all(k in slots for k in ap)
        aw.append({'isK':mode=='K','slot':slots[x],'d':len(ad),'path':[slots[k] for k in ap],'dirs':ad})
        H+=(len(ad)+1)//2;ac=S.trace(ac,x)[0]
        bx=-1 if x<0 else x;bp,bd=V.path(bc,bx);bw.append({'T':ix(x),'d':len(bd),'path':[ix(k) for k in bp],'dirs':bd})
        if mode=='K':bc=S.trace(bc,bx)[0]
        Btrees.append(bc)
    assert H in (1,2);build_envW(e,aw,'MXLw');build_envBT(e,bw,'MXLbt')
    w=exact_witness(e);st=AState(ED,w);sa=alpha_prefix(w,st);assert macro_H(ED,w).v==H
    for j in range(len(word)):
        assert verify_path_dyn(ED,w,st,j).v;st=splay_event(ED,w,st,j,Box(True))
    ta=alpha_prefix(w,st)
    if junk:
        for a in (sa,ta):
            a[0][0]=2
            for p in range(1,7):
                if a[p][0]!=0:a[p][1]=1;a[p][2]=8
                elif not a[p][1]:a[p][2]=8
    bs=V.bmodel(B,True);bt=V.bmodel(bc,True)
    if padding:
        # Absent gap intervals are unconstrained apart from containing their rank.
        for b in (bs,bt):b['lo'][10]=0;b['hi'][10]=18
        # Type-3 non-real pair in an off-path core side; arbitrary ref is not a node edge.
        for b in (bs,bt):
            if b['kl'][7]==2:b['kl'][7]=3;b['rl'][7]=13
    q=bw[-1]['d']//2;weight=2*H-q;e['MXL_H']=H;e['MXL_w']=weight;e['MXLbt_q']=q
    fill(d,e,L['s'],mu,am.sig,bs,sa);fill(d,e,L['t'],mu,am.sig,bt,ta)
    for j in range(6):
        bj=V.bmodel(Btrees[min(j,len(Btrees)-1)],True)
        if padding:
            bj['lo'][10]=0;bj['hi'][10]=18
            if bj['kl'][7]==2:bj['kl'][7]=3;bj['rl'][7]=13
        V.aux(e,f'MXLsb{j}',bj)
    V.bounds(d,e);assert d.ev_ground(L['root'],e),label
    inv=[{'slot':i,'side':b,'hidden_S':am.phS[(i,b)],'population':am.pz[(i,b)],
       'lower':am.lo[i] if b==0 else am.rank[am.slots[i]['key']]+1,
       'upper':am.rank[am.slots[i]['key']] if b==0 else am.hi[i]} for i,b in am.phS]
    return ac,bc,{'label':label,'kind':'LOW','root':True,'source':state(mu,am.sig,bs,sa),'destination':state(mu,am.sig,bt,ta),
      'H':H,'q':q,'w':weight,'word':word,'cuts':list(cuts),'A_source':V.serial(A),'A_destination':V.serial(ac),
      'B_source':V.serial(B),'B_destination':V.serial(bc),'A_paths':aw,'B_paths':bw,'port_inventory':inv,
      'unused_alpha_junk':junk,'B_padding_variant':padding,'environment':{nm:e[nm] for nm in d.vars}}
