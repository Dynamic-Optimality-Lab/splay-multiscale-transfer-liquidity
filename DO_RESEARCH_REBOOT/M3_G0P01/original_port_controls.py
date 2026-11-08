"""Opaque-fringe source witnesses, original low roots and full-state port boundary blocks."""
import sys,json,time
from pathlib import Path
from types import SimpleNamespace
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_G0P01','DO_RESEARCH_REBOOT/M3_H2R01',
             'DO_RESEARCH_REBOOT/M3_H1F01','DO_RESEARCH_REBOOT/M3_FRC01',
             'DO_RESEARCH_REBOOT/M3_PHI01','DO_RESEARCH_REBOOT/M2_SEP01','python/independent']
import splay as S
import verify_full_mixed as V
from PC_TYPED_DAG import DAG
from PC_CONCRETIZE import build_envA,build_envI,build_envBT,build_envW
from PC_ROTATION_INTERPRETER import AState,splay_event,verify_path_dyn,macro_H
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from experiment import D as ED,V as Box
from original_h2_controls import exact_witness,alpha_prefix
from verify_original_compensation import high
from port_potential import PortPotential
from certify_refinement import BASE,load,port_tree,shadow
OUT=BASE/'original_port_controls.json'
def model(A):
    am=SimpleNamespace(Ss=list(range(9)),sidx={i:i for i in range(9)},V=list(range(-1,9)),
                       rank={k:k+1 for k in range(-1,9)},slots={},kids={},lo={},hi={},phS={},pz={},sig=[1]+[0]*9)
    queue=[(A,0,None,None,0,0,136)];nextid=1
    while queue:
        n,i,p,side,z,l,h=queue.pop(0);k=n[1];assert k>=0
        am.slots[i]={'key':k,'depth':z,'par':p,'side':side};am.lo[i]=l;am.hi[i]=h;kids=[]
        for b,ch in ((0,n[2]),(1,n[3])):
            if ch==S.LEAF:kids.append((2,None))
            elif ch[1]==-1 or z==6:
                kids.append((1,(i,b)));keys=S.inorder(ch)
                am.phS[(i,b)]=[x for x in keys if x>=0];am.pz[(i,b)]=[int(-1 in keys)]+[0]*9
            else:
                j=nextid;nextid+=1;kids.append((0,j))
                queue.append((ch,j,i,b,z+1,l if b==0 else am.rank[k]+1,am.rank[k] if b==0 else h))
        am.kids[i]=tuple(kids)
    assert not any(v['key']==-1 for v in am.slots.values())
    return am
def state(b,alpha):return {'mu':341,'sigma':[1]+[0]*9,'b':{k:b[k] for k in ('root',)+V.FIELDS},'alpha':alpha}
def fill(d,e,obj,b,alpha):
    V.put(d,e,obj.mu,341);V.fillB(d,e,obj.b,b)
    for i,(k,s,x) in enumerate(alpha):
        V.put(d,e,obj.ak[i],k);V.put(d,e,obj.aS[i],bool(s));V.put(d,e,obj.aI[i],x)
    for n,v in zip(obj.sig,[1]+[0]*9):V.put(d,e,n,v)
def low(d,L,A,B,word,label):
    am=model(A);e=V.blank(d);build_envA(e,am,set(range(9)),'MXLw');build_envI(e,am,set(range(9)),'MXLv')
    slots={v['key']:i for i,v in am.slots.items()};ac=A;bc=B;aw=[];bw=[];Btrees=[B];H=0
    for mode,x in word:
        ap,ad=V.path(ac,x);assert all(k in slots for k in ap) and len(ad)<=4
        aw.append({'isK':mode=='K','slot':slots[x],'d':len(ad),'path':[slots[k] for k in ap],'dirs':ad})
        H+=(len(ad)+1)//2;ac=S.trace(ac,x)[0]
        bp,bd=V.path(bc,x);bw.append({'T':x,'d':len(bd),'path':bp,'dirs':bd})
        if mode=='K':bc=S.trace(bc,x)[0]
        Btrees.append(bc)
    assert H==1;build_envW(e,aw,'MXLw');build_envBT(e,bw,'MXLbt')
    w=exact_witness(e);st=AState(ED,w);sa=alpha_prefix(w,st);assert macro_H(ED,w).v==1
    for j in range(len(word)):
        assert verify_path_dyn(ED,w,st,j).v;st=splay_event(ED,w,st,j,Box(True))
    ta=alpha_prefix(w,st);bs=V.bmodel(B,True);bt=V.bmodel(bc,True);q=bw[-1]['d']//2;weight=2-q
    e['MXL_H']=1;e['MXL_w']=weight;e['MXLbt_q']=q;fill(d,e,L['s'],bs,sa);fill(d,e,L['t'],bt,ta)
    for j in range(6):V.aux(e,f'MXLsb{j}',V.bmodel(Btrees[min(j,len(Btrees)-1)],True))
    V.bounds(d,e);assert d.ev_ground(L['root'],e),label
    r={'label':label,'kind':'LOW','root':True,'source':state(bs,sa),'destination':state(bt,ta),
       'H':1,'q':q,'w':weight,'word':word,'A_source':V.serial(A),'A_destination':V.serial(ac),
       'B_source':V.serial(B),'B_destination':V.serial(bc),'A_paths':aw,'B_paths':bw,
       'port_inventory':[{'slot':i,'side':b,'hidden_S':am.phS[(i,b)],'population':am.pz[(i,b)]} for i,b in am.phS],
       'environment':{nm:e[nm] for nm in d.vars}}
    return ac,bc,r
def main():
    assert not OUT.exists();start=time.process_time();V.start=start;V.MU=341;P=PortPotential();c,a=load()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');records=[];variants=[]
    cert=json.loads((BASE/'refinement_certificate.json').read_text());samples=cert['samples']
    # Add one representative for every repaired weight/residual category.
    for j,w in enumerate(a['weights']):
        u=a['source'][j];v=a['destination'][j];su=a['ordinary_a'][u];tv=a['ordinary_a'][v]
        bi=a['ordinary_b'][u];bj=a['ordinary_b'][v];oldP=P.old
        oldsu=oldP.p[a['image_source'][j]] if su<c['old_physical_shadow_count'] else oldP.c['initial_by_B'][bi]
        oldtv=oldP.p[a['image_destination'][j]] if tv<c['old_physical_shadow_count'] else oldP.c['initial_by_B'][bj]
        res=int(w)+oldsu-oldtv
        if res<0:
            key=f'repaired_w{int(w)}_r{res}'
            samples.setdefault(key,{'edge':j,'source_B':bi,'destination_B':bj,**c['family_options'][a['option'][j]]})
    def append(r):
        ps=P.inspect(r['source']);pt=P.inspect(r['destination']);oldr=r['w']+ps['one_gap_joint']-pt['one_gap_joint'];nr=r['w']+ps['port_joint']-pt['port_joint']
        assert nr>=0,(r['label'],nr)
        r.update(potential_source=ps,potential_destination=pt,old_extension_residual=oldr,port_residual=nr)
        if r['kind']=='HIGH':
            r.update(OM_reduced_weight=r['w']+ps['port_joint'],MO_reduced_weight=-pt['port_joint'])
            assert r['OM_reduced_weight']>=0 and r['MO_reduced_weight']>=0
        records.append(r);assert time.process_time()-start<300,'UNKNOWN: original control cap'
        print(json.dumps({'label':r['label'],'w':r['w'],'old_r':oldr,'port_r':nr}),flush=True);return r
    bysample={}
    for label,row in samples.items():
        A=V.insert(P.old.old.old.trees[row['A_core_tree']],-1);B=V.insert(P.old.old.old.trees[row['source_B']],-1)
        ac,bc,r=low(d,L,A,B,[['K',row['target']]],label);r=append(r);bysample[label]=(A,B,ac,bc,r)
        eidx=row['edge'];u=a['source'][eidx];v=a['destination'][eidx]
        assert r['source']['alpha']==c['shadows'][a['ordinary_a'][u]] and r['destination']['alpha']==c['shadows'][a['ordinary_a'][v]]
        assert r['potential_source']['image_table_node']==a['image_source'][eidx] and r['potential_destination']['image_table_node']==a['image_destination'][eidx]
        assert any(p['population'][0]==1 and not p['hidden_S'] for p in r['port_inventory'])
    base=bysample['physical_to_port'];A,B,ac,bc,r0=base;x=r0['word'][0][1]
    _,_,rv=low(d,L,A,B,[['D',x],['K',x]],'whole_H1_port_macro_variant');rv=append(rv)
    assert rv['source']==r0['source'] and rv['destination']==r0['destination'] and rv['w']==r0['w'];variants.append([r0['label'],rv['label']])
    # Fully closed mixed control. Canonical old core cycle with the fringe hidden by a leaf port.
    previous=json.loads(Path('DO_RESEARCH_REBOOT/M3_PHI01/full_mixed_controls.json').read_text());legs=[]
    for j in range(3):
        old=next(z for z in previous['records'] if z['label']==f'cycle_3_p1_low{j}')
        A=V.insert(V.from_serial(old['A_source']),-1);B=V.insert(V.from_serial(old['B_source']),-1)
        if j==0:A0=A;B0=B
        ac,bc,r=low(d,L,A,B,old['word'],'port_cycle_low'+str(j));legs.append(append(r))
    rh=high(dh,H,ac,bc,A0,A0[1],[1]+[0]*9,341,'port_cycle_high')
    env=rh['environment'];rh['source']['alpha']=legs[-1]['destination']['alpha'];rh['destination']['alpha']=legs[0]['source']['alpha']
    for tag,s in (('MXHs',rh['source']),('MXHt',rh['destination'])):
        for j,(k,ss,ii) in enumerate(s['alpha']):env[f'{tag}_ak{j}']=k;env[f'{tag}_aS{j}']=bool(ss);env[f'{tag}_aI{j}']=ii
    V.bounds(dh,env);assert dh.ev_ground(H['root'],env);legs.append(append(rh))
    for l,r in zip(legs,legs[1:]+legs[:1]):assert l['destination']==r['source']
    assert sum(r['w'] for r in legs)==sum(r['port_residual'] for r in legs)==4
    result={'status':'COMPLETE','low_DAG_nodes':len(d.nodes),'high_DAG_nodes':len(dh.nodes),
       'controls':len(records),'original_low_roots':sum(r['kind']=='LOW' for r in records),
       'original_high_roots':sum(r['kind']=='HIGH' for r in records),'macro_variants':variants,
       'closed_mixed_cycle':{'labels':[r['label'] for r in legs],'weight':4,'full_state_closure':True,'shared_midpoint':True},
       'negative_mixed_cycles_certified':0,'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
