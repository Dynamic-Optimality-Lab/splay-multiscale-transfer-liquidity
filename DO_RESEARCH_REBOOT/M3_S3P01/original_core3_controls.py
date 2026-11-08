"""Full original singleton-S3 port witnesses, whole macro controls and a shared-state mixed cycle."""
import sys,json,time
from pathlib import Path
from types import SimpleNamespace
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_S3P01','DO_RESEARCH_REBOOT/M3_H2R01',
             'DO_RESEARCH_REBOOT/M3_G0P01','DO_RESEARCH_REBOOT/M3_H1F01',
             'DO_RESEARCH_REBOOT/M3_FRC01','DO_RESEARCH_REBOOT/M3_PHI01',
             'DO_RESEARCH_REBOOT/M2_SEP01','python/independent']
import splay as S
import verify_full_mixed as V
from PC_TYPED_DAG import DAG
from PC_CONCRETIZE import build_envA,build_envI,build_envW,build_envBT
from PC_ROTATION_INTERPRETER import AState,splay_event,verify_path_dyn,macro_H
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from original_h2_controls import exact_witness,alpha_prefix
from experiment import D as ED,V as Box
from verify_original_compensation import high
from core3_potential import Core3Potential
from certify_core3_v2 import BASE,load
OUT=BASE/'original_core3_controls.json'
def model(A,hidden):
    hidden=set(hidden)
    am=SimpleNamespace(Ss=list(range(9)),sidx={i:i for i in range(9)},V=list(range(-1,9)),
        rank={k:k+1 for k in range(-1,9)},slots={},kids={},lo={},hi={},phS={},pz={},sig=[1]+[0]*9)
    queue=[(A,0,None,None,0,0,136)];nextid=1
    while queue:
        n,i,p,side,z,l,h=queue.pop(0);k=n[1];assert k not in hidden
        am.slots[i]={'key':k,'depth':z,'par':p,'side':side};am.lo[i]=l;am.hi[i]=h;kids=[]
        for b,ch in ((0,n[2]),(1,n[3])):
            if ch==S.LEAF:kids.append((2,None))
            elif ch[1] in hidden or z==6:
                if ch[1] in hidden:assert ch[2:]==(S.LEAF,S.LEAF)
                kids.append((1,(i,b)));keys=S.inorder(ch)
                am.phS[(i,b)]=[x for x in keys if x>=0];am.pz[(i,b)]=[int(-1 in keys)]+[0]*9
            else:
                j=nextid;nextid+=1;kids.append((0,j))
                queue.append((ch,j,i,b,z+1,l if b==0 else am.rank[k]+1,am.rank[k] if b==0 else h))
        am.kids[i]=tuple(kids)
    assert not any(v['key'] in hidden for v in am.slots.values())
    return am
def state(b,alpha):return {'mu':341,'sigma':[1]+[0]*9,'b':{k:b[k] for k in ('root',)+V.FIELDS},'alpha':alpha}
def fill(d,e,obj,b,alpha):
    V.put(d,e,obj.mu,341);V.fillB(d,e,obj.b,b)
    for i,(k,s,x) in enumerate(alpha):V.put(d,e,obj.ak[i],k);V.put(d,e,obj.aS[i],bool(s));V.put(d,e,obj.aI[i],x)
    for n,v in zip(obj.sig,[1]+[0]*9):V.put(d,e,n,v)
def low(d,L,A,B,hidden,word,label):
    am=model(A,hidden);e=V.blank(d);build_envA(e,am,set(range(9)),'MXLw');build_envI(e,am,set(range(9)),'MXLv')
    slots={v['key']:i for i,v in am.slots.items()};aw=[];bw=[];ac=A;bc=B;Btrees=[B];H=0
    ix=lambda x:9 if x==-1 else x
    for mode,x in word:
        ap,ad=V.path(ac,x);assert len(ad)<=4 and all(k in slots for k in ap)
        aw.append({'isK':mode=='K','slot':slots[x],'d':len(ad),'path':[slots[k] for k in ap],'dirs':ad})
        H+=(len(ad)+1)//2;ac=S.trace(ac,x)[0]
        bp,bd=V.path(bc,x);bw.append({'T':ix(x),'d':len(bd),'path':[ix(k) for k in bp],'dirs':bd})
        if mode=='K':bc=S.trace(bc,x)[0]
        Btrees.append(bc)
    assert H in (1,2);build_envW(e,aw,'MXLw');build_envBT(e,bw,'MXLbt')
    w=exact_witness(e);st=AState(ED,w);sa=alpha_prefix(w,st);assert macro_H(ED,w).v==H
    for j in range(len(word)):
        assert verify_path_dyn(ED,w,st,j).v;st=splay_event(ED,w,st,j,Box(True))
    ta=alpha_prefix(w,st);bs=V.bmodel(B,True);bt=V.bmodel(bc,True);q=bw[-1]['d']//2;weight=2*H-q
    e['MXL_H']=H;e['MXL_w']=weight;e['MXLbt_q']=q;fill(d,e,L['s'],bs,sa);fill(d,e,L['t'],bt,ta)
    for j in range(6):V.aux(e,f'MXLsb{j}',V.bmodel(Btrees[min(j,len(Btrees)-1)],True))
    V.bounds(d,e);assert d.ev_ground(L['root'],e),label
    inv=[{'slot':i,'side':b,'hidden_S':am.phS[(i,b)],'population':am.pz[(i,b)],
          'lower':am.lo[i] if b==0 else am.rank[am.slots[i]['key']]+1,
          'upper':am.rank[am.slots[i]['key']] if b==0 else am.hi[i]}
         for i,b in am.phS]
    assert any(v['hidden_S']==[3] and v['population']==[0]*10 and v['lower']==4 and v['upper']==5 for v in inv)
    if -1 in hidden:assert any(v['hidden_S']==[] and v['population']==[1]+[0]*9 for v in inv)
    return ac,bc,{'label':label,'kind':'LOW','root':True,'source':state(bs,sa),'destination':state(bt,ta),
        'H':H,'q':q,'w':weight,'word':word,'hidden_leaves':list(hidden),'A_source':V.serial(A),
        'A_destination':V.serial(ac),'B_source':V.serial(B),'B_destination':V.serial(bc),
        'A_paths':aw,'B_paths':bw,'port_inventory':inv,'environment':{nm:e[nm] for nm in d.vars}}
def main():
    assert not OUT.exists();start=time.process_time();V.start=start;V.MU=341;P=Core3Potential();c,a=load()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');records=[];variants=[]
    cert=json.loads((BASE/'core3_certificate.json').read_text());btrees=P.physical.old.old.trees
    def append(r):
        s=P.inspect(r['source']);t=P.inspect(r['destination']);oldr=r['w']+s['port_joint']-t['port_joint'];newr=r['w']+s['core3_joint']-t['core3_joint']
        assert newr>=0,(r['label'],newr)
        r.update(potential_source=s,potential_destination=t,old_extension_residual=oldr,core3_residual=newr)
        if r['kind']=='HIGH':
            r.update(OM_reduced_weight=r['w']+s['core3_joint'],MO_reduced_weight=-t['core3_joint'])
            assert r['OM_reduced_weight']>=0 and r['MO_reduced_weight']>=0
        records.append(r);assert time.process_time()-start<300,'UNKNOWN: original root controls cap'
        print(json.dumps({'label':r['label'],'w':r['w'],'old_r':oldr,'new_r':newr}),flush=True);return r
    samples=defaultdict(list)
    for name,row in cert['samples'].items():samples[row['edge']].append(name)
    byreason={}
    for edge,reasons in samples.items():
        row=cert['samples'][reasons[0]];A=V.from_serial(P.physical.c['A_trees'][row['A_tree']]);B=V.insert(btrees[row['source_B']],-1)
        ac,bc,r=low(d,L,A,B,row['hidden_leaves'],row['word'],'sample_'+reasons[0]);r['reasons']=reasons;r=append(r)
        assert r['w']==row['w'] and r['H']==row['H']
        u=a['source'][edge];v=a['destination'][edge]
        assert r['source']['alpha']==c['shadows'][a['ordinary_a'][u]] and r['destination']['alpha']==c['shadows'][a['ordinary_a'][v]]
        assert r['potential_source']['core3_image_node']==a['image_source'][edge] and r['potential_destination']['core3_image_node']==a['image_destination'][edge]
        for reason in reasons:byreason[reason]=r
    h1=byreason['repaired_H1_w0_r-2'];x=h1['word'][-1][1]
    _,_,r=low(d,L,V.from_serial(h1['A_source']),V.from_serial(h1['B_source']),h1['hidden_leaves'],[['D',x],['K',x]],'whole_H1_core3_port_variant')
    r=append(r);assert r['source']==h1['source'] and r['destination']==h1['destination'] and r['w']==h1['w'];variants.append([h1['label'],r['label']])
    h2=byreason['H2_w0'];x=h2['word'][-1][1]
    for j,word in enumerate(([['D',-1],['K',-1],['K',x]],[['K',-1],['D',x],['K',x]],
                            [['D',-1],['K',-1],['D',x],['K',x]])):
        _,_,r=low(d,L,V.from_serial(h2['A_source']),V.from_serial(h2['B_source']),h2['hidden_leaves'],word,'whole_H2_core3_port_variant_'+str(j))
        r=append(r);assert r['source']==h2['source'] and r['destination']==h2['destination'] and r['w']==h2['w'];variants.append([h2['label'],r['label']])
    # Visible S3 port in both orientations, simultaneously with the old gap0 leaf port.
    z=S.LEAF;A=S.node(2,S.node(0,S.node(-1,z,z),S.node(1,z,z)),
                      S.node(4,S.node(3,z,z),S.balanced(range(5,9))));B=A
    ac,bc,l=low(d,L,A,B,[-1,3],[['K',4]],'both_port_cycle_low');l=append(l)
    h=high(dh,H,ac,bc,A,2,[1]+[0]*9,341,'both_port_cycle_high');env=h['environment']
    assert V.from_serial(h['B_destination'])==B
    h['source']['alpha']=l['destination']['alpha'];h['destination']['alpha']=l['source']['alpha']
    for tag,s in (('MXHs',h['source']),('MXHt',h['destination'])):
        for j,(k,ss,ii) in enumerate(s['alpha']):env[f'{tag}_ak{j}']=k;env[f'{tag}_aS{j}']=bool(ss);env[f'{tag}_aI{j}']=ii
    V.bounds(dh,env);assert dh.ev_ground(H['root'],env);h=append(h)
    assert l['source']==h['destination'] and l['destination']==h['source']
    assert 'S3_RL' in l['potential_source']['core3_rule'] and 'G0_' in l['potential_source']['core3_rule']
    assert 'S3_LR' in l['potential_destination']['core3_rule']
    assert l['w']+h['w']==l['core3_residual']+h['core3_residual']==8
    result={'status':'COMPLETE','controls':len(records),'original_low_roots':sum(r['kind']=='LOW' for r in records),
        'original_high_roots':sum(r['kind']=='HIGH' for r in records),'low_DAG_nodes':len(d.nodes),'high_DAG_nodes':len(dh.nodes),
        'port_S_inventory_exactly_core3':True,'core3_port_rank_interval':[4,5],'macro_variants':variants,
        'closed_mixed_cycle':{'labels':[l['label'],h['label']],'weight':8,'full_state_closure':True,
                              'shared_midpoint':True,'both_core3_orientations':True,'both_ports_together':True},
        'negative_mixed_cycles_certified':0,'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':
    from collections import defaultdict
    main()
