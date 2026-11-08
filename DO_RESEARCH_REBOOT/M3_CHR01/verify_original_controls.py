"""Full original low/high controls for retained cheap-reset debt and mixed closure."""
import sys,json,time
from pathlib import Path
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','DO_RESEARCH_REBOOT/M3_LDR01','python/independent']
import verify_full_mixed as V
import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from fragment_graph import load,BASE,CATALOG
OUT=BASE/'original_controls.json'

class Potential:
    def __init__(self):
        c,a=load();self.c=c;self.p=array('i');self.p.frombytes((BASE/'potential.bin').read_bytes())
        if c['byteorder']!=sys.byteorder:self.p.byteswap()
        self.trees=[V.from_serial(n['tree']) for n in json.loads(CATALOG.read_text())['nodes']]
        self.bid={t:i for i,t in enumerate(self.trees)}
        self.aid={tuple(tuple(row) for row in V.shadow(self.trees[g[0]])):i for i,g in enumerate(c['A_groups'])}
        self.local={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])}
    def __call__(self,s):
        if s['mu']!=341 or any(s['sigma']) or V.phi(s)!=-3:return 0
        aid=self.aid.get(tuple(tuple(row) for row in s['alpha']))
        if aid is None:return 0
        b=s['b'];seen=set()
        def core(i):
            assert i<9 and i not in seen;seen.add(i)
            kids=[]
            for k,r in (('kl','rl'),('kr','rr')):
                kids.append(core(b[r][i]) if b[k][i]==0 and b[r][i]<9 else S.LEAF)
            return S.node(i,*kids)
        t=core(b['root']);assert seen==set(range(9))
        bid=self.bid[t];base=self.c['B_bases'][bid]
        if base<0 or self.c['shadows'][aid][0]!=t[1]:return 0
        return self.p[base+self.local[aid]]

def main():
    assert not OUT.exists();start=time.process_time();V.start=start
    P=Potential();d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    assert len(d.nodes)<4000000 and len(dh.nodes)<4000000
    records=[];root_evaluations=0
    def append(r):
        s=P(r['source']);t=P(r['destination']);assert -2<=s<=0 and -2<=t<=0
        r.update(joint_potential_source=s,joint_potential_destination=t,
                 extended_reduced_weight=r['w']-(t-s))
        assert r['extended_reduced_weight']>=0
        if r['kind']=='HIGH':
            r.update(midpoint_potential=0,OM_reduced_weight=r['w']+s,MO_reduced_weight=-t)
            assert r['OM_reduced_weight']>=0 and r['MO_reduced_weight']>=0
        records.append(r);return r
    reset=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/zero_reset_control.json').read_text())['record']
    prior=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/full_run_controls.json').read_text())
    plus=next(r for r in prior['records'] if r['label']=='helper_reset_1')
    for label,old in (('zero_reset_debt_retained',reset),('plus1_reset_debt_retained',plus)):
        _,_,r=V.low(d,L,V.from_serial(old['A_source']),V.from_serial(old['B_source']),old['word'],True,label)
        root_evaluations+=1;append(r)
    assert records[0]['w']==0 and (records[0]['joint_potential_source'],records[0]['joint_potential_destination'])==(-2,-2)
    assert records[1]['w']==1 and (records[1]['joint_potential_source'],records[1]['joint_potential_destination'])==(-2,-1)
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_PHI01/full_mixed_controls.json').read_text())
    cycle=[];firstA=firstB=None;ac=bc=None
    for j in range(3):
        z=next(r for r in old['records'] if r['label']==f'cycle_3_p1_low{j}')
        srcA=V.from_serial(z['A_source']);srcB=V.from_serial(z['B_source'])
        if j==0:firstA=srcA;firstB=srcB
        ac,bc,r=V.low(d,L,srcA,srcB,z['word'],True,f'mixed_zero_cycle_low{j}')
        root_evaluations+=1;cycle.append(append(r))
    r=V.high(dh,H,ac,bc,firstA,firstB,True,'mixed_zero_cycle_high');root_evaluations+=1;cycle.append(append(r))
    for l,r in zip(cycle,cycle[1:]+cycle[:1]):assert l['destination']==r['source']
    assert sum(r['w'] for r in cycle)==4
    a=S.balanced(range(9));_,_,r=V.low(d,L,a,a,[('D',0),('K',0)],True,'expensive_H2_DELETE_KEEP')
    root_evaluations+=1;assert r['H']==2 and r['w']>=2;append(r)
    # A legal noncanonical high witness and an abstract-only destination shadow.
    b=S.LEAF
    for i in reversed(range(9)):b=S.node(i,S.LEAF,b)
    a=S.node(0,S.LEAF,S.balanced(range(1,9)));ad=S.node(8,S.balanced(range(8)),S.LEAF)
    bd=S.trace(b,8)[0];r=V.high(dh,H,a,b,ad,bd,True,'noncanonical_high_to_abstract_shadow')
    root_evaluations+=1;env=r['environment'];env['MXHbt_bd0']=9;env['MXHbt_bp0_9']=19;env['MXHbt_bdir0_8']=False
    alpha=[[0,1,8]]+[[2,0,0] for _ in range(6)]
    for j,(k,s,i) in enumerate(alpha):
        env[f'MXHt_ak{j}']=k;env[f'MXHt_aS{j}']=bool(s);env[f'MXHt_aI{j}']=i
    V.bounds(dh,env);assert dh.ev_ground(H['root'],env);root_evaluations+=1
    r['destination']['alpha']=alpha;r['d']=9;r['root']=True;r['noncanonical_declared_depth']=True
    r['abstract_only_destination_shadow']=True;append(r)
    assert time.process_time()-start<300
    result={'status':'COMPLETE','controls':len(records),'original_root_evaluations':root_evaluations,
            'low_DAG_nodes':len(d.nodes),'high_DAG_nodes':len(dh.nodes),
            'mixed_closed_cycle':{'labels':[r['label'] for r in cycle],'weight':4,
                                  'full_state_closure':True,'high_midpoint_shared':True},
            'cheap_resets_repaid_by_joint_labels':True,
            'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':main()
