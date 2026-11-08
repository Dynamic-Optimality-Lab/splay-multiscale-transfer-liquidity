"""Exact sparse difference relaxation; no full B x A graph is stored."""
import json,time
from collections import deque,Counter
from pathlib import Path
from prefix_profiles import BASE
def main():
    out=BASE/'construction.json';assert not out.exists();start=time.process_time()
    c=json.loads((BASE/'relation.json').read_text());N=c['classes'];opts=c['options'];sh=c['shadows']
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    cc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text())
    psi=[r['psi'] for r in bc['nodes']];roots=[r['tree'][0] for r in bc['nodes']]
    byroot={r:[] for r in range(9)}
    for a,s in enumerate(sh):byroot[s[0][2]].append(a)
    kern=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    h2={(r['entry_core'],r['target']):(r['exit_core'],r['w']) for r in kern['rows'] if r['gap0_childless_at_exit']}
    trans=[];zero_safe=0
    for bi in range(4862):
        t={}
        for x in range(9):
            dep=cc['B_depth'][bi][x]
            if dep:
                bj=cc['B_destination'][bi][x];w=2-dep//2
                if w<0:assert -psi[bj]<=w;zero_safe+=1
                if w<2 and not ((w==1 and psi[bj]>=1) or (w==0 and psi[bj]==2)):t[(1,x)]=(bj,w)
            if (bi,x) in h2:
                bj,w=h2[(bi,x)];assert w>=0
                if w<2 and not ((w==1 and psi[bj]>=1) or (w==0 and psi[bj]==2)):t[(2,x)]=(bj,w)
        trans.append(t)
    labels={};hist={};history=[];queue=deque();queued=set();scans=updates=seeds=pops=0;failure=None;reason=None
    def state(k):
        b,a=divmod(k,N);return {'B':b,'A':a,'alpha':sh[a],'psi':psi[b]}
    def process(key):
        nonlocal scans,updates,pops,failure
        bi,ai=divmod(key,N);du=labels.get(key,-psi[bi]);pops+=1
        if du==0:return
        T=trans[bi]
        for j,o in enumerate(opts[ai]):
            tw=T.get((o['H'],o['target']))
            if tw is None:continue
            scans+=1;bj,w=tw;v=bj*N+o['destination'];alt=du+w
            if alt>=labels.get(v,-psi[bj]):continue
            history.append((key,v,w,j,hist.get(key,-1)));hist[v]=len(history)-1;labels[v]=alt;updates+=1
            if alt< -2:
                rows=[];h=hist[v]
                while h>=0:
                    u,vv,ww,jj,h=history[h];b,a=divmod(u,N);o=opts[a][jj]
                    rows.append({'source':state(u),'destination':state(vv),'w':ww,'H':o['H'],'target':o['target'],
                      'option_index':jj,'witness_index':o['witness'],'A_witness':c['witnesses'][o['witness']]})
                rows.reverse();assert all(x['destination']==y['source'] for x,y in zip(rows,rows[1:]))
                ub=-rows[0]['source']['psi'];assert ub+sum(r['w'] for r in rows)==alt
                failure={'path':rows,'initial_upper_bound':ub,'weight_sum':sum(r['w'] for r in rows),
                  'derived_upper_bound':alt,'required_lower_bound':-2,'original_roots_verified':False,
                  'negative_original_cycle_certified':False}
                return
            if v not in queued:queue.append(v);queued.add(v)
    try:
        for bi,p in enumerate(psi):
            if p==0:continue
            for ai in byroot[roots[bi]]:
                key=bi*N+ai;seeds+=1;process(key)
                while queue and not failure:
                    key=queue.popleft();queued.remove(key);process(key)
                    if time.process_time()-start>=300:raise RuntimeError('CPU cap')
                    if len(labels)+len(hist)+len(queue)+N+len(c['witnesses'])>=2000000:raise RuntimeError('live diagnostic state cap')
                if failure:break
                if time.process_time()-start>=300:raise RuntimeError('CPU cap')
            if failure:break
    except RuntimeError as e:reason=str(e)
    obj={'status':'RANGE_TWO_DEBT_TEMPLATE_REFUTED_EXACT_IN_SUPERRELATION' if failure else ('UNKNOWN_CAP' if reason else 'COMPLETED_UNAUDITED'),
      'source_classes':N,'A_options':c['options_count'],'implicit_synchronized_product_states':sum(len(byroot[r]) for r in roots),
      'live_changed_states':len(labels),'history_records':len(history),'initial_negative_seeds_visited':seeds,
      'row_scans':scans,'updates':updates,'pops':pops,'zero_source_negative_rows_discharged':zero_safe,
      'materialized_B_product_edges':0,'cpu_seconds':round(time.process_time()-start,3),'reason':reason,'obstruction':failure,
      'M3_proved':False,'original_negative_cycle_certified':False}
    if not failure and not reason:
        with (BASE/'potential_sparse.json').open('x',encoding='utf-8') as f:json.dump({'default':'-psi(B)','N':N,'labels':labels},f,separators=(',',':'))
        obj['range']=[min(labels.values(),default=0),0]
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
    print(json.dumps(obj,indent=2),flush=True)
if __name__=='__main__':main()
