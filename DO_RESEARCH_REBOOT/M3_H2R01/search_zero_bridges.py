"""Bounded countercandidate search: H=1 zero/negative returns after an H=2 exception."""
import sys,json,time
from pathlib import Path
from collections import deque
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
from verify_full_mixed import from_serial
BASE=Path('DO_RESEARCH_REBOOT/M3_H2R01');OUT=BASE/'zero_bridge_search.json'
def main():
    assert not OUT.exists();start=time.process_time()
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    ts=[from_serial(n['tree']) for n in c['nodes']];ids={t:i for i,t in enumerate(ts)}
    moves=[]
    for t in ts:
        out=[]
        for x in range(9):
            h=S.lookup(t,x)[1]
            if h>=4:out.append((x,ids[S.trace(t,x)[0]],h,h//2-2))
        moves.append(out)
    failures=json.loads((BASE/'fringe_kernel_certificate.json').read_text())['failures']
    masks=[(0,2,4,6,8),(0,1,2,4,6),(0,2,3,5,6)];rows=[];scans=0
    for f,M in zip(failures,masks):
        initial=(f['exit_core'],0);queue=deque([initial]);prev={initial:None};found=None
        while queue:
            b,deficit=queue.popleft()
            if b==f['entry_core'] and deficit==2:found=(b,deficit);break
            for x,v,h,d in moves[b]:
                if x not in M:continue
                scans+=1;assert scans<=400000 and time.process_time()-start<120,'UNKNOWN: zero-bridge cap'
                key=(v,min(2,deficit+d))
                if key not in prev:
                    prev[key]=((b,deficit),{'source':b,'destination':v,'target':x,'depth':h,'w':-d})
                    queue.append(key)
        path=[]
        if found:
            cur=found
            while prev[cur] is not None:cur,e=prev[cur];path.append(e)
            path.reverse()
        rows.append({'exception':f,'mask':list(M),'visited_states':len(prev),
                     'found_negative_return':found is not None,'return_path':path,
                     'candidate_weight':f['w']+sum(e['w'] for e in path) if found else None})
    result={'status':'COMPLETE','edge_scans':scans,'cases':rows,
            'negative_B_candidates':sum(r['found_negative_return'] for r in rows),
            'cpu_seconds':round(time.process_time()-start,3),
            'scope':'A-unfiltered B candidates only; no original cycle without full-state lifting'}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
