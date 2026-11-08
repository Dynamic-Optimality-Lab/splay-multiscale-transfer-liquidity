"""Complete original H=2 low witnesses, including coarser port prefixes and multiple masks."""
import sys,json,time
from pathlib import Path
from types import SimpleNamespace
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','DO_RESEARCH_REBOOT/M2_SEP01',
 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE','python/independent']
import splay as S
import verify_full_mixed as F
from experiment import D as ED,V as Box
from PC_TYPED_DAG import DAG
from PC_CONCRETIZE import AModel,build_envA,build_envI,build_envW,build_envBT
from PC_ROTATION_INTERPRETER import AState,splay_event,verify_path_dyn,mux_ref,macro_H
from STRICT_LOW_COMPILER import build_slow,shadow7
from terminal_potential import CappedPotential
OUT=Path('DO_RESEARCH_REBOOT/M3_H2R01/original_h2_controls.json')
SSET=set(range(9));MARKS=(0,2,4,6,8);MU=sum(1<<i for i in MARKS)

def prefix_model(t,exposed):
    am=SimpleNamespace(Ss=list(range(9)),sidx={i:i for i in range(9)},V=list(range(9)),
                       slots={},kids={},lo={},hi={},phS={},pz={},sig=[0]*10)
    queue=[(t,0,None,None,0,0,136)];nextid=1
    while queue:
        n,i,p,side,z,l,h=queue.pop(0);k=n[1]
        am.slots[i]={'key':k,'depth':z,'par':p,'side':side};am.lo[i]=l;am.hi[i]=h;kids=[]
        for b,ch in ((0,n[2]),(1,n[3])):
            if ch==S.LEAF:kids.append((2,None))
            elif ch[1] in exposed:
                j=nextid;nextid+=1;kids.append((0,j))
                queue.append((ch,j,i,b,z+1,l if b==0 else k+1,k if b==0 else h))
            else:
                kids.append((1,(i,b)));am.phS[(i,b)]=S.inorder(ch);am.pz[(i,b)]=[0]*10
        am.kids[i]=tuple(kids)
    assert set(v['key'] for v in am.slots.values())==set(exposed)
    return am

def exact_witness(env):
    w=SimpleNamespace()
    for field,suffix in (('p','p'),('kleft','kl'),('cleft','cl'),('kright','kr'),('cright','cr'),
                         ('isS','isS'),('sidx','sidx'),('rank','rank')):
        setattr(w,field,[Box(env[f'MXLw_{suffix}{i}']) for i in range(127)])
    w.nev=Box(env['MXLw_nev']);w.evK=[Box(env[f'MXLw_eK{e}']) for e in range(5)]
    w.evT=[Box(env[f'MXLw_eT{e}']) for e in range(5)];w.evd=[Box(env[f'MXLw_ed{e}']) for e in range(5)]
    w.evpath=[[Box(env[f'MXLw_ep{e}_{k}']) for k in range(5)] for e in range(5)]
    w.evdir=[[Box(env[f'MXLw_edir{e}_{k}']) for k in range(4)] for e in range(5)]
    return w

def alpha_prefix(w,st):
    sh=shadow7(ED,w,st);rows=[]
    for pos in ('root','L','R','LL','LR','RL','RR'):
        if pos=='root':k=0;ref=sh[pos]
        else:kk,ref=sh[pos];k=kk.v
        if k==0:
            ss=bool(mux_ref(ED,w.isS,ref).v);ii=mux_ref(ED,w.sidx,ref).v if ss else 0
        else:ss=False;ii=0
        rows.append([k,int(ss),ii])
    return rows

def state(mu,b,alpha):
    return {'mu':mu,'sigma':[0]*10,'b':{k:b[k] for k in ('root',)+F.FIELDS},'alpha':alpha}

def fill_state(d,env,obj,mu,b,alpha):
    F.put(d,env,obj.mu,mu);F.fillB(d,env,obj.b,b)
    for i,(k,s,x) in enumerate(alpha):
        F.put(d,env,obj.ak[i],k);F.put(d,env,obj.aS[i],bool(s));F.put(d,env,obj.aI[i],x)
    for n in obj.sig:F.put(d,env,n,0)

def control(d,L,P,A,B,word,mu,label,exposed=None):
    am=AModel(A,SSET) if exposed is None else prefix_model(A,exposed)
    env=F.blank(d);build_envA(env,am,SSET,'MXLw');build_envI(env,am,SSET,'MXLv')
    slots={v['key']:i for i,v in am.slots.items()};aw=[];bw=[];ac=A;bc=B;Btrees=[B];H=0
    for mode,x in word:
        ap,ad=F.path(ac,x);assert len(ad)<=4 and all(k in slots for k in ap)
        aw.append({'isK':mode=='K','slot':slots[x],'d':len(ad),'path':[slots[k] for k in ap],'dirs':ad})
        H+=(len(ad)+1)//2;ac=S.trace(ac,x)[0]
        bp,bd=F.path(bc,x);bw.append({'T':x,'d':len(bd),'path':bp,'dirs':bd})
        if mode=='K':bc=S.trace(bc,x)[0]
        Btrees.append(bc)
    assert H==2
    build_envW(env,aw,'MXLw');build_envBT(env,bw,'MXLbt')
    ew=exact_witness(env);st=AState(ED,ew);srcalpha=alpha_prefix(ew,st)
    assert macro_H(ED,ew).v==2
    for e in range(len(word)):
        assert verify_path_dyn(ED,ew,st,e).v
        st=splay_event(ED,ew,st,e,Box(True))
    dstalpha=alpha_prefix(ew,st)
    source=F.bmodel(B,True);dest=F.bmodel(bc,True);q=bw[-1]['d']//2;weight=4-q
    env['MXL_H']=2;env['MXL_w']=weight;env['MXLbt_q']=q
    fill_state(d,env,L['s'],mu,source,srcalpha);fill_state(d,env,L['t'],mu,dest,dstalpha)
    for j in range(6):F.aux(env,f'MXLsb{j}',F.bmodel(Btrees[min(j,len(Btrees)-1)],True))
    F.bounds(d,env);assert d.ev_ground(L['root'],env),label
    s=state(mu,source,srcalpha);t=state(mu,dest,dstalpha);ps=P.inspect(s);pt=P.inspect(t)
    before=Btrees[-2];preid=P.ids[before];hterm=S.lookup(before,word[-1][1])[1]
    assert hterm==bw[-1]['d'] and q in (3,4) and pt['psi']>=P.psi[preid]+q-2
    assert pt['capped_joint']<=2-q and pt['capped_joint']-ps['capped_joint']<=weight
    assert F.phi(s)==F.phi(t)==-3
    record={'label':label,'original_low_root':True,'source':s,'destination':t,
            'word':word,'H':2,'q':q,'w':weight,'A_source_physical':F.serial(A),'A_destination_physical':F.serial(ac),
            'B_source':F.serial(B),'B_destination':F.serial(bc),'B_preterminal':F.serial(before),
            'macro_entry_B_depth_of_terminal_target':S.lookup(B,word[-1][1])[1],
            'terminal_B_depth':hterm,'preterminal_core_tree_id':preid,'preterminal_psi':P.psi[preid],
            'potential_source':ps,'potential_destination':pt,
            'reduced_weight':weight-(pt['capped_joint']-ps['capped_joint']),
            'source_has_port_shadow':any(r[0]==1 for r in srcalpha),
            'destination_has_port_shadow':any(r[0]==1 for r in dstalpha),
            'prefix_mode':'canonical_depth6' if exposed is None else 'path_and_ports',
            'A_paths':aw,'B_paths':bw,'environment':{nm:env[nm] for nm in d.vars}}
    print(json.dumps({'control':label,'q':q,'w':weight,'potential':[ps['capped_joint'],pt['capped_joint']],
                      'port_shadow':[record['source_has_port_shadow'],record['destination_has_port_shadow']]}),flush=True)
    return record

def path_tree(path,extras=None):
    extras=extras or {};t=S.LEAF
    for j in reversed(range(len(path))):
        k=path[j];l,r=extras.get(k,(S.LEAF,S.LEAF))
        if t!=S.LEAF:
            if t[1]<k:l=t
            else:r=t
        t=S.node(k,l,r)
    return t

def main():
    assert not OUT.exists();start=time.process_time();P=CappedPotential();d=DAG();L=build_slow(d,'MXL')
    assert len(d.nodes)<4000000;z=S.LEAF;records=[]
    def add(*args,**kwargs):
        assert time.process_time()-start<300,'UNKNOWN: original control cap'
        records.append(control(d,L,P,*args,**kwargs))
    A=S.node(0,z,S.node(6,S.node(2,S.node(1,z,z),S.node(4,S.node(3,z,z),S.node(5,z,z))),S.node(8,S.node(7,z,z),z)))
    B0=path_tree([0,8,1,7,2,6,3,5,4])
    B1=path_tree([0,8,1,7,2,5,4],{4:(S.node(3,z,z),z),5:(z,S.node(6,z,z))})
    add(A,B0,[('K',4)],MU,'single_KEEP_zero_ports',exposed={0,6,2,4})
    add(A,B1,[('K',4)],MU,'single_KEEP_plus1_ports',exposed={0,6,2,4})
    add(A,B0,[('K',4)],MU,'single_KEEP_zero_full_prefix')
    AD=S.node(8,S.node(4,S.node(0,z,S.balanced(range(1,4))),S.balanced(range(5,8))),z)
    BD0=path_tree(list(reversed(range(9))))
    BD1=path_tree([8,7,6,5,2,1,0],{2:(z,S.node(3,z,S.node(4,z,z)))})
    add(AD,BD0,[('D',4),('K',0)],MU,'DELETE_KEEP_zero')
    add(AD,BD1,[('D',4),('K',0)],MU,'DELETE_KEEP_plus1')
    AK=S.node(0,z,S.node(1,z,S.node(8,S.balanced(range(2,8)),z)))
    BK=path_tree(list(range(9)))
    add(AK,BK,[('K',1),('K',8)],MU,'unmarked_KEEP_KEEP_plus1')
    add(AK,BK,[('D',1),('K',1),('K',8)],MU,'DELETE_zeroKEEP_KEEP_plus1')
    AK0=S.node(1,S.node(0,z,z),S.node(8,S.balanced(range(2,8)),z))
    BK0=S.node(1,S.node(0,z,z),path_tree(list(range(2,9))))
    mu2=sum(1<<i for i in (1,2,4,6,8))
    add(AK0,BK0,[('K',0),('K',8)],mu2,'unmarked_KEEP_KEEP_zero_other_mask')
    assert len(records)==8 and all(r['w'] in (0,1) for r in records)
    assert records[0]['source_has_port_shadow'] and records[0]['destination_has_port_shadow']
    assert records[-1]['macro_entry_B_depth_of_terminal_target']==7 and records[-1]['terminal_B_depth']==8
    assert records[5]['macro_entry_B_depth_of_terminal_target']==8 and records[5]['terminal_B_depth']==7
    assert records[5]['destination']==records[6]['destination'] and records[5]['source']==records[6]['source']
    elapsed=round(time.process_time()-start,3);assert elapsed<300
    result={'status':'COMPLETE','controls':len(records),'low_DAG_nodes':len(d.nodes),
            'zero_controls':sum(r['w']==0 for r in records),'plus1_controls':sum(r['w']==1 for r in records),
            'masks':sorted(set(r['source']['mu'] for r in records)),
            'port_shadow_controls':sum(r['source_has_port_shadow'] or r['destination_has_port_shadow'] for r in records),
            'cpu_seconds':elapsed,'records':records}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':main()
