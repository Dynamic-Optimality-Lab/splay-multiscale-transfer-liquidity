"""Physical-only trace compiler; no observer fits or core-size computations.

Uses the sealed original mutable tree primitive read-only. Carrier/Pi replay is
separate. Every complete original source, every real bit and closure remain.
"""
import sys
import time
from collections import Counter
sys.dont_write_bytecode=True
import bank_rule as B
K=B.K


def compile_source(source,width=5):
    keys=sorted(map(int,source['initial_A']['children']));assert keys==sorted(map(int,source['initial_B']['children']))
    blocks=[keys[j:j+width] for j in range(0,len(keys),width)];owner={x:i for i,p in enumerate(blocks) for x in p};trees={a:K.OLD.Tree(source['initial_'+a],keys) for a in ('A','B')}
    diagonal=source.get('diagonal')
    if diagonal is None:assert source['initial_A']==source['initial_B'] and not source.get('prefix')
    else:
        reach={a:K.OLD.Tree(diagonal,keys) for a in ('A','B')}
        for mode,x in source.get('prefix',[]):
            K.OLD.plain(reach['A'],x)
            if mode=='K':K.OLD.plain(reach['B'],x)
        assert all(reach[a].state()==source['initial_'+a] for a in trees)
    steps=[];ops=[];A=Q=KB=rot=0
    for op,(mode,x) in enumerate(source['operations'],1):
        start=len(steps);k=int(mode=='K' and trees['B'].root!=x);KB+=k;a=q=0
        for actor in ('A','B') if mode=='K' else ('A',):
            t=trees[actor];step=0
            while t.parent[x] is not None:
                step+=1;p=t.parent[x];g=t.parent[p]
                typ='ZIG' if g is None else ('L' if p<g else 'R')+('L' if x<p else 'R')
                pivots=[x] if g is None else [p,x] if typ in ('LL','RR') else [x,x];bits=[];scope=set()
                for bit,y in enumerate(pivots):
                    p=t.parent[y];g=t.parent[p];middle=t.ch[y][int(y<p)]
                    footprint=sorted({owner[v] for v in (p,y,g,middle) if v is not None});scope.update(footprint)
                    bits.append({'id':[actor,op,step,bit],'promoted':y,'demoted':p,'grandparent':g,'middle':middle,'footprint':footprint})
                    t.rotate(y);rot+=1
                aa=int(actor=='A');qq=int(actor=='B' and len(pivots)==2);a+=aa;q+=qq
                steps.append({'id':[actor,op,step],'actor':actor,'target':x,'type':typ,'a':aa,'q':qq,'k':0,'scope':sorted(scope),'bits':bits})
        A+=a;Q+=q;ops.append({'id':op,'mode':mode,'target':x,'a':a,'q':q,'k':k,'steps':[start,len(steps)]})
    assert all(trees[a].state()==source['initial_'+a] for a in trees)
    assert KB<=A and rot==sum(len(s['bits']) for s in steps)
    if source.get('expected_A') is not None:assert A==source['expected_A']
    if source.get('expected_Q') is not None:assert Q==source['expected_Q']
    return {'schema':'physical-only-original-bank-trace.v1','source':source,'blocks':blocks,'steps':steps,'operations':ops,'A':A,'Q_B':Q,'K_B':KB,'real_rotations':rot,'full_pair_closure':True,'reaching_prefix_checked':True,'original_Pi':'Not recomputed by this physical-only compiler; independent event verification required for any reported obstruction.'}


def mirror(s):
    keys=sorted(map(int,s['initial_A']['children']));lo,hi=keys[0],keys[-1];f=lambda x:None if x is None else lo+hi-x
    def tree(t):return {'root':f(t['root']),'children':{str(f(int(k))):[f(r),f(l)] for k,(l,r) in t['children'].items()}}
    out=s.copy();out['name']='mirror__'+s['name'];out['initial_A']=tree(s['initial_A']);out['initial_B']=tree(s['initial_B']);out['diagonal']=tree(s['diagonal']) if s.get('diagonal') else None
    out['operations']=[[m,f(x)] for m,x in s['operations']];out['prefix']=[[m,f(x)] for m,x in s.get('prefix',[])];return out


def population():
    seq=[]
    for p in range(1,10):seq.append(K.PARAM.H(p,5))
    for p in (2,3,4,5,6,7):seq.append(K.PARAM.H(p,17))
    for q in (65,257):seq.append(K.PARAM.H(3,q))
    for q in (1,5,17,65):seq.append(K.PARAM.compressed(q))
    # Reflections matter because the frozen secondary priority is physical
    # increasing key order. Do not silently assume reflection symmetry.
    for p,q in ((3,7),(3,25),(5,5),(6,17)):seq.append(mirror(K.PARAM.H(p,q)))
    for i in range(3):
        old=K.load(B.PREV.parent/'GSO_ENGINE_20261121_V001/run_001'/f'flow_case_{i}.json');seq.append(mirror(K.SOURCES.canonical(old['ref'])))
    return seq


def run():
    start=time.perf_counter();summary=[];rotations=0
    for i,s in enumerate(population()):
        z=compile_source(s);rotations+=z['real_rotations'];assert rotations<=3000000 and time.perf_counter()-start<=300
        B.write(f'scaling_001/trace_{i:02d}.json.gz',z)
        results=[]
        for H in (5,8,16,32):
            r=B.cyclic(z,H);B.write(f'scaling_001/source_{i:02d}_H{H}.json.gz',r);results.append({'H':H,'paid':r['paid'],'unpaid':len(r['failures']),'passes':len(r['period_passes'])})
        row={'index':i,'name':s['name'],'keys':len(s['initial_A']['children']),'operations':len(s['operations']),'A':z['A'],'Q_B':z['Q_B'],'real_rotations':z['real_rotations'],'capacities':results};summary.append(row);print(row,flush=True)
    B.write('scaling_001/SUMMARY.json',{'cases':summary,'real_rotations':rotations,'seconds':time.perf_counter()-start,'scope':'Complete source construction and physical costs/closure. Pi must be independently checked on each reported obstruction. No universal fit is inferred.','root_status':'OPEN'})


if __name__=='__main__':run()
