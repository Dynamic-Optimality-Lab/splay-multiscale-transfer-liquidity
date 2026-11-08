"""Exact sparse integer construction for one three-unit signature."""
import json,time,sys
from pathlib import Path
from collections import deque
BASE=Path('DO_RESEARCH_REBOOT/M3_POP3_ALL01')
def main():
    sigma=tuple(map(int,sys.argv[1:11]));folder=BASE/('s'+''.join(map(str,sigma)));out=folder/'construction.json';assert not out.exists();start=time.process_time()
    c=json.loads((folder/'relation.json').read_text());B=json.loads(Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01/B_bank.json').read_text());N=c['classes'];psi=B['psi'];opts=c['options']
    byroot={r:[] for r in range(9)}
    for a,s in enumerate(c['shadows']):byroot[s[0][2]].append(a)
    trans=[]
    for b in range(4862):
        row={}
        for x in range(9):
            dep=B['depths'][b][x];bb=B['destinations'][b][x];w=2-dep//2
            if w<0:assert -psi[bb]<=w
            if dep and w<2 and not ((w==1 and psi[bb]>=1) or (w==0 and psi[bb]==2)):row[(1,x,None)]=(bb,w)
            for gap in (0,9):
                if not sigma[gap]:continue
                pair=B['kernels'][str(gap)][b][x]
                if pair is not None:
                    bb,w=pair;assert w>=0
                    if w<2 and not ((w==1 and psi[bb]>=1) or (w==0 and psi[bb]==2)):row[(2,x,gap)]=(bb,w)
        trans.append(row)
    values={};latest={};history=[];queue=deque();queued=set();scans=updates=seeds=pops=peak=0;failure=None;reason=None
    def process(key):
        nonlocal scans,updates,pops,failure,peak
        b,a=divmod(key,N);du=values.get(key,-psi[b]);pops+=1
        if du==0:return
        T=trans[b]
        for oi,o in enumerate(opts[a]):
            H,x,aa,gap,fam,code=o;pair=T.get((H,x,gap))
            if pair is None:continue
            bb,w=pair;v=bb*N+aa;scans+=1;alt=du+w
            if alt>=values.get(v,-psi[bb]):continue
            history.append((key,v,w,oi,latest.get(key,-1)));latest[v]=len(history)-1;values[v]=alt;updates+=1
            if alt< -2:
                path=[];idx=latest[v]
                while idx>=0:
                    u,vv,ww,oo,idx=history[idx];ub,ua=divmod(u,N);op=opts[ua][oo]
                    path.append({'source_B':ub,'source_A':ua,'source_alpha':c['shadows'][ua],'destination_B':vv//N,'destination_A':vv%N,
                      'destination_alpha':c['shadows'][vv%N],'w':ww,'option':op,'family':c['families'][op[4]]})
                path.reverse();initial=-psi[path[0]['source_B']];assert initial+sum(e['w'] for e in path)==alt
                failure={'path':path,'initial_upper_bound':initial,'derived_upper_bound':alt,'floor':-2,'original_cycle_certified':False};return
            if v not in queued:queue.append(v);queued.add(v)
            resident=N+len(values)+len(latest)+len(history)+2*len(queue);peak=max(peak,resident)
            if resident>=2000000:raise RuntimeError('live diagnostic state cap')
    try:
        for b,p in enumerate(psi):
            if p==0:continue
            for a in byroot[B['trees'][b][0]]:
                seeds+=1;process(b*N+a)
                while queue and not failure:
                    k=queue.popleft();queued.remove(k);process(k)
                    if time.process_time()-start>=300:raise RuntimeError('CPU cap')
                if failure:break
                if time.process_time()-start>=300:raise RuntimeError('CPU cap')
            if failure:break
    except RuntimeError as e:reason=str(e)
    obj={'status':'RANGE_TWO_DEBT_TEMPLATE_REFUTED_IN_SUPERRELATION' if failure else ('UNKNOWN_CAP' if reason else 'CONSTRUCTED_UNAUDITED'),
      'sigma':sigma,'classes':N,'changed_states':len(values),'updates':updates,'history_records':len(history),'queue_pops':pops,
      'initial_seeds':seeds,'row_scans':scans,'peak_conservative_resident_records':peak,'B_product_edges_stored':0,
      'cpu_seconds':round(time.process_time()-start,3),'obstruction':failure,'reason':reason,'full_M3_proved':False}
    if not failure and not reason:
        with (folder/'potential.json').open('x',encoding='utf-8') as f:json.dump({'N':N,'default':'-psi(B)','values':values},f,separators=(',',':'))
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
    print(json.dumps(obj,indent=2),flush=True)
if __name__=='__main__':main()
