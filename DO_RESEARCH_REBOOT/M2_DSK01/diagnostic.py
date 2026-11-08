"""Dirty selected-claimant alias diagnostics; unchanged source operations."""
import sys,json,time,itertools
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'DO_RESEARCH_REBOOT/M2_SEP01'))
from experiment import D,V,FIELDS,pack,unpack
from PC_B_CONTROLLER import BTrace,b_splay_event
OUT=Path('DO_RESEARCH_REBOOT/M2_DSK01/diagnostic.json')
def replay(h,bits,length):
    spine=list(range(8,7-h,-1));period=spine+[19];word=list(bits)+[False,True]
    m={'root':spine[-1],**{f:[f'S.{f}{i}' for i in range(19)] for f in FIELDS}}
    m['kr'][8]=0;m['rr'][8]=19
    for j in range(1,h+1):
        k,r=('kr','rr') if bits[j-1] else ('kl','rl')
        m[k][spine[j]]=0;m[r][spine[j]]=spine[j-1]
    b=pack(m);bt=BTrace(D,'D');bt.bT[0]=V(8);bt.bd[0]=V(length)
    bt.bpath[0]=[V(period[k%len(period)]) for k in range(19)]
    bt.bdir[0]=[V(word[k%len(word)]) for k in range(18)]
    out=unpack(b_splay_event(D,b,bt,0,V(False)))
    links=[]
    for i in range(19):
        for side,k,r in (('L','kl','rl'),('R','kr','rr')):
            child=out[r][i]
            if out[k][i]==0 and isinstance(child,int) and child<19:links.append([i,child,side])
    claims=[link for link in links if link[1]==8]
    graph={i:[] for i in range(19)}
    for a,b,_ in links:graph[a].append(b)
    def find_cycle():
        active=[];done=set()
        def dfs(i):
            if i in active:return active[active.index(i):]+[i]
            if i in done:return None
            active.append(i)
            for j in graph[i]:
                ans=dfs(j)
                if ans:return ans
            active.pop();done.add(i)
        for i in range(19):
            ans=dfs(i)
            if ans:return ans
    cyc=find_cycle()
    return spine,period,word,m,out,claims,cyc
if __name__=='__main__':
    assert not OUT.exists()
    start=time.process_time();rows=[];unresolved=[]
    for h in range(9):
        for bits in itertools.product((False,True),repeat=h):
            for length in range(14,19):
                assert time.process_time()-start<120,'Diagnostic cap: UNKNOWN'
                spine,period,word,m,out,claims,cyc=replay(h,bits,length)
                kind='ROOT_CLAIM' if claims else ('FORCED_CYCLE' if cyc else 'UNRESOLVED')
                row={'h':h,'bits':list(bits),'d':length,'kind':kind,'claims':claims,'cycle':cyc}
                rows.append(row)
                if kind=='UNRESOLVED':unresolved.append({**row,'normal_form':out})
        print(json.dumps({'h_completed':h,'cases':len(rows),'unresolved':len(unresolved),
                          'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    result={'status':'COMPLETE','cases':len(rows),'root_claim_cases':sum(r['kind']=='ROOT_CLAIM' for r in rows),
            'forced_cycle_cases':sum(r['kind']=='FORCED_CYCLE' for r in rows),
            'unresolved_count':len(unresolved),'cpu_seconds':round(time.process_time()-start,3),
            'rows':rows,'unresolved':unresolved}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','unresolved')}),
          'first_unresolved',json.dumps(unresolved[:1]),flush=True)

