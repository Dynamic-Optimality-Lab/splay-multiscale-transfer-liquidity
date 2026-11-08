"""Original roots and full shared-state compensation blocks, including fringe high exit."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_FRC01','DO_RESEARCH_REBOOT/M3_H2R01',
             'DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as F
from original_fringe_controls import ashape
from compensated_potential import CompensatedPotential
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
OUT=Path('DO_RESEARCH_REBOOT/M3_FRC01/original_compensation_controls.json')

def high(d,L,A,B,Ad,x,sig,mu,label):
    Bd=S.trace(B,x)[0];source=F.bmodel(B,True);dest=F.bmodel(Bd,True);env=F.blank(d)
    F.MU=mu
    F.fillState(d,env,L['s'],A,source,sig);F.fillState(d,env,L['t'],Ad,dest,sig)
    F.put(d,env,L['g'].mu,mu);F.fillB(d,env,L['g'].b,dest)
    for n,v in zip(L['g'].sig,sig):F.put(d,env,n,v)
    F.put(d,env,L['g'].v,Ad[1]);F.aux(env,'MXHsbs',source);F.aux(env,'MXHsbt',dest);F.aux(env,'MXHsbg',dest)
    bp,bd=F.path(B,x);length=len(bd);ix=lambda k:k if k>=0 else 9
    env['MXHbt_bT0']=x;env['MXHbt_bd0']=length
    for k,v in enumerate(bp):env[f'MXHbt_bp0_{k}']=ix(v)
    for k,v in enumerate(bd):env[f'MXHbt_bdir0_{k}']=v
    F.put(d,env,L['q'],length//2);F.put(d,env,L['w1'],6-length//2)
    F.bounds(d,env);assert d.ev_ground(L['root'],env),label
    s=F.state(A,source,sig);t=F.state(Ad,dest,sig)
    return {'label':label,'kind':'HIGH','root':True,'source':s,'destination':t,'d':length,
            'q':length//2,'w':6-length//2,'target':x,
            'A_source':F.serial(A),'A_destination':F.serial(Ad),'B_source':F.serial(B),'B_destination':F.serial(Bd),
            'shared_midpoint':{'mu':mu,'sigma':sig,'b':t['b'],'v':Ad[1]},
            'environment':{nm:env[nm] for nm in d.vars}}

def main():
    assert not OUT.exists();start=time.process_time();F.start=start;P=CompensatedPotential()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    assert len(d.nodes)<4000000 and len(dh.nodes)<4000000
    records=[];blocks=[];seeds=[]
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    def append(r):
        assert time.process_time()-start<300,'UNKNOWN: full original controls cap'
        a=P.inspect(r['source']);b=P.inspect(r['destination'])
        oldr=r['w']-b['capped_joint']+a['capped_joint'];newr=r['w']-b['compensated_joint']+a['compensated_joint']
        r.update(potential_source=a,potential_destination=b,old_reduced_weight=oldr,new_reduced_weight=newr)
        assert newr>=0,(r['label'],newr)
        if r['kind']=='HIGH':
            r.update(midpoint_correction=0,OM_reduced_weight=r['w']+a['compensated_joint'],
                     MO_reduced_weight=-b['compensated_joint'])
            assert r['OM_reduced_weight']>=0 and r['MO_reduced_weight']>=0
        records.append(r);print(json.dumps({'control':r['label'],'w':r['w'],'old_r':oldr,'new_r':newr}),flush=True)
        return r
    def block(legs,label):
        for a,b in zip(legs,legs[1:]):assert a['destination']==b['source'],label
        r={'label':label,'labels':[e['label'] for e in legs],'full_shared_states':True,
           'old_reduced_weight':sum(e['old_reduced_weight'] for e in legs),
           'new_reduced_weight':sum(e['new_reduced_weight'] for e in legs),
           'weight':sum(e['w'] for e in legs),'closed':legs[-1]['destination']==legs[0]['source']}
        assert r['old_reduced_weight']>=0 and r['new_reduced_weight']>=0
        blocks.append(r)
    for j,row in enumerate(kernel['failures']):
        B=F.insert(P.old.trees[row['entry_core']],-1);A=ashape(B[1],row['target'])
        mu=(47,87,109)[j]
        if j==2:
            z=S.LEAF;A=S.node(5,S.node(-1,z,S.node(3,S.balanced(range(3)),S.node(4,z,z))),
                                  S.node(6,z,S.node(7,z,S.node(8,z,z))))
        F.MU=mu
        ac,bc,r=F.low(d,L,A,B,[('K',-1),('K',row['target'])],True,'repaired_exception_'+str(row['entry_core']))
        r=append(r);assert r['H']==2 and r['w']==1 and r['old_reduced_weight']==-1 and r['new_reduced_weight']==0
        legs=[r];seeds.append((ac,bc,r,mu))
        if j==2:
            assert S.lookup(ac,6)[1]<=2
            ac,bc,zr=F.low(d,L,ac,bc,[('K',6)],True,'pattern3_zero_delay_2141_to_2965')
            zr=append(zr);assert zr['H']==1 and zr['w']==0 and zr['old_reduced_weight']==0
            assert zr['potential_destination']['core_tree_id']==2965;legs.append(zr)
        target=(0,4,5)[j]
        assert 1<=S.lookup(ac,target)[1]<=2,(j,target,S.lookup(ac,target))
        ac,bc,exitrow=F.low(d,L,ac,bc,[('K',target)],True,'pattern_'+str(j+1)+'_repaying_H1_exit')
        exitrow=append(exitrow);assert exitrow['H']==1 and exitrow['old_reduced_weight']>=1
        if j==1:assert exitrow['w']==0 and exitrow['potential_destination']['psi']>=1
        legs.append(exitrow);block(legs,'pattern_'+str(j+1)+'_full_compensation_block')
    # A high exit from precisely the same full post-exception state (positive sigma).
    ac,bc,seed,mu=seeds[2];target=5;ad=S.trace(ac,target)[0]
    hi=append(high(dh,H,ac,bc,ad,target,seed['destination']['sigma'],mu,'pattern3_original_high_exit'))
    assert seed['destination']==hi['source'];block([seed,hi],'pattern3_mixed_compensation_block')
    result={'status':'COMPLETE','low_DAG_nodes':len(d.nodes),'high_DAG_nodes':len(dh.nodes),
            'original_low_roots':sum(r['kind']=='LOW' for r in records),
            'original_high_roots':sum(r['kind']=='HIGH' for r in records),'queries':len(records),
            'masks':sorted({r['source']['mu'] for r in records}),'repaired_exception_controls':3,
            'blocks':blocks,'zero_delay_full_state_shared':True,'high_midpoint_shared':True,
            'negative_mixed_cycles_certified':0,'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert result['cpu_seconds']<300
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
