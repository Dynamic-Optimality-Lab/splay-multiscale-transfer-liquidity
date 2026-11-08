"""Complete unchanged source roots; key codes16*i are mapped to S indices i."""
import sys
from types import SimpleNamespace
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_ACL01')
from original_controls import S,V,DAG,build_slow,build_shigh,build_envA,build_envI,build_envW,build_envBT,exact_witness,AState,ED,alpha_prefix,splay_event,Box,macro_H
from framework_v2 import iscore
SC={16*i for i in range(9)}
def gap(k):return k//16+1
def ix(k):return k//16 if iscore(k) else 9+gap(k)
def bmodel(t):
    b={'root':ix(t[1]),'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    crank=lambda i:2*i+1 if i<9 else 2*(i-9)
    lo=[crank(i) for i in range(19)];hi=list(lo);par=[19]*19;dep=[0]*19
    def go(n,l,h,p,d):
        i=ix(n[1]);assert l<=crank(i)<=h;lo[i]=l;hi[i]=h;par[i]=p;dep[i]=d
        for side,kf,rf,ch in ((0,'kl','rl',n[2]),(1,'kr','rr',n[3])):
            if ch[0]!='leaf':b[kf][i]=0;b[rf][i]=ix(ch[1]);go(ch,l if side==0 else crank(i)+1,crank(i)-1 if side==0 else h,i,d+1)
    go(t,0,18,19,0)
    b.update(lo=lo,hi=hi,bpar=par,bdep=dep);return b
def model(A,cuts):
    keys=S.inorder(A);assert SC<=set(keys);cuts=set(map(tuple,cuts));rank={k:i for i,k in enumerate(keys)};sig=[0]*10
    for k in keys:
        if k not in SC:sig[gap(k)]+=1
    am=SimpleNamespace(Ss=sorted(SC),sidx={16*i:i for i in range(9)},V=keys,rank=rank,slots={},kids={},lo={},hi={},phS={},pz={},sig=sig)
    todo=[(A,0,None,None,0,0,136)];nextid=1
    while todo:
        n,i,p,side,d,l,h=todo.pop(0);k=n[1];am.slots[i]={'key':k,'depth':d,'par':p,'side':side};am.lo[i]=l;am.hi[i]=h;ch=[]
        for b,cc in enumerate(n[2:]):
            if (k,b) in cuts or (cc[0]!='leaf' and d==6):
                ch.append((1,(i,b)));ks=S.inorder(cc);am.phS[(i,b)]=[x for x in ks if x in SC];z=[0]*10
                for x in ks:
                    if x not in SC:z[gap(x)]+=1
                am.pz[(i,b)]=z
            elif cc[0]=='leaf':ch.append((2,None))
            else:
                j=nextid;nextid+=1;ch.append((0,j));todo.append((cc,j,i,b,d+1,l if b==0 else rank[k]+1,rank[k] if b==0 else h))
        am.kids[i]=tuple(ch)
    return am
def state(mu,sig,b,a):return {'mu':mu,'sigma':sig,'b':{f:b[f] for f in ('root',)+V.FIELDS},'alpha':a}
def fill(d,e,obj,mu,sig,b,a):
    V.put(d,e,obj.mu,mu);V.fillB(d,e,obj.b,b)
    for i,(k,s,x) in enumerate(a):V.put(d,e,obj.ak[i],k);V.put(d,e,obj.aS[i],bool(s));V.put(d,e,obj.aI[i],x)
    for var,x in zip(obj.sig,sig):V.put(d,e,var,x)
def low(d,L,A,B,cuts,word,label,mu):
    am=model(A,cuts);e=V.blank(d);build_envA(e,am,SC,'MXLw');build_envI(e,am,SC,'MXLv');slots={v['key']:i for i,v in am.slots.items()}
    aw=[];bw=[];ac=A;bc=B;bs=[B];cost=0
    for mode,x in word:
        ap,ad=V.path(ac,x);assert len(ad)<=4 and all(k in slots for k in ap);aw.append({'isK':mode=='K','slot':slots[x],'d':len(ad),'path':[slots[k] for k in ap],'dirs':ad})
        cost+=(len(ad)+1)//2;ac=S.trace(ac,x)[0];bx=x if iscore(x) else 16*gap(x)-8;bp,bd=V.path(bc,bx)
        bw.append({'T':ix(bx),'d':len(bd),'path':[ix(k) for k in bp],'dirs':bd})
        if mode=='K':bc=S.trace(bc,bx)[0]
        bs.append(bc)
    assert cost in (1,2);build_envW(e,aw,'MXLw');build_envBT(e,bw,'MXLbt');w=exact_witness(e);st=AState(ED,w);sa=alpha_prefix(w,st)
    for j in range(len(word)):st=splay_event(ED,w,st,j,Box(True))
    ta=alpha_prefix(w,st);q=bw[-1]['d']//2;weight=2*cost-q;e['MXL_H']=cost;e['MXL_w']=weight;e['MXLbt_q']=q
    sb=bmodel(B);tb=bmodel(bc);fill(d,e,L['s'],mu,am.sig,sb,sa);fill(d,e,L['t'],mu,am.sig,tb,ta)
    for j in range(6):V.aux(e,f'MXLsb{j}',bmodel(bs[min(j,len(bs)-1)]))
    V.bounds(d,e);assert d.ev_ground(L['root'],e),label
    inv=[{'slot':i,'side':b,'hidden_S_indices':[k//16 for k in am.phS[(i,b)]],'population':list(am.pz[(i,b)]),
      'lower':am.lo[i] if b==0 else rankkey(am,i)+1,'upper':rankkey(am,i) if b==0 else am.hi[i]} for i,b in am.phS]
    return ac,bc,{'label':label,'kind':'LOW','root':True,'source':state(mu,am.sig,sb,sa),'destination':state(mu,am.sig,tb,ta),
      'H':cost,'q':q,'w':weight,'word_codes':word,'A_source_codes':V.serial(A),'A_destination_codes':V.serial(ac),
      'B_source_codes':V.serial(B),'B_destination_codes':V.serial(bc),'A_paths':aw,'B_paths':bw,'port_inventory':inv,
      'environment':{nm:e[nm] for nm in d.vars}}
def rankkey(am,i):return am.rank[am.slots[i]['key']]
def high(d,H,B,x,s,t,label):
    mu=s['mu'];sig=s['sigma'];e=V.blank(d);Bd=S.trace(B,x)[0];bs=bmodel(B);bt=bmodel(Bd)
    assert s['b']=={f:bs[f] for f in ('root',)+V.FIELDS} and t['b']=={f:bt[f] for f in ('root',)+V.FIELDS}
    fill(d,e,H['s'],mu,sig,bs,s['alpha']);fill(d,e,H['t'],mu,sig,bt,t['alpha']);V.put(d,e,H['g'].mu,mu);V.fillB(d,e,H['g'].b,bt)
    for var,y in zip(H['g'].sig,sig):V.put(d,e,var,y)
    V.put(d,e,H['g'].v,t['alpha'][0][2]);V.aux(e,'MXHsbs',bs);V.aux(e,'MXHsbt',bt);V.aux(e,'MXHsbg',bt)
    path,dirs=V.path(B,x);h=len(dirs);e['MXHbt_bT0']=ix(x);e['MXHbt_bd0']=h
    for j,k in enumerate(path):e[f'MXHbt_bp0_{j}']=ix(k)
    for j,b in enumerate(dirs):e[f'MXHbt_bdir0_{j}']=b
    V.put(d,e,H['q'],h//2);V.put(d,e,H['w1'],6-h//2);V.bounds(d,e);assert d.ev_ground(H['root'],e),label
    return {'label':label,'kind':'HIGH','root':True,'source':s,'destination':t,'q':h//2,'w':6-h//2,
      'shared_midpoint':{'mu':mu,'sigma':sig,'b':t['b'],'v':t['alpha'][0][2]},'environment':{nm:e[nm] for nm in d.vars}}
