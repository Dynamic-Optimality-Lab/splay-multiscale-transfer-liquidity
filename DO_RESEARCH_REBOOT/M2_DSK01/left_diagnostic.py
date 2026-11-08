"""Left-claimant successor orbit, with literal slot-0 alias positions covered."""
import sys,json,time,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from diagnostic import D,V,FIELDS,pack,unpack
from PC_B_CONTROLLER import BTrace,b_splay_event
OUT=Path('DO_RESEARCH_REBOOT/M2_DSK01/left_diagnostic.json')
def replay_left(h,s,bits,zero_mode,length):
    n=h+s
    zero_position=(max((j+1 for j,v in enumerate(bits) if v),default=0)
                   if zero_mode=='ON' else None)
    used=list(range(1,9));a=[];b=[]
    for j in range(h+1):
        a.append(0 if j==zero_position else used.pop(0))
    for j in range(s):b.append(used.pop(0))
    target=a[0];c=b[0];period=a+[19]+b;word=list(bits)+[False]*(s+1)+[True]
    assert len(period)==len(word)==n+2
    m={'root':a[-1],**{f:[f'S.{f}{i}' for i in range(19)] for f in FIELDS}}
    for j in range(1,h+1):
        k,r=('kr','rr') if bits[j-1] else ('kl','rl')
        m[k][a[j]]=0;m[r][a[j]]=a[j-1]
    m['kl'][c]=0;m['rl'][c]=19
    for j in range(1,s):m['kl'][b[j]]=0;m['rl'][b[j]]=b[j-1]
    m['kr'][target]=0;m['rr'][target]=b[-1]
    state=pack(m);bt=BTrace(D,'L');bt.bT[0]=V(target);bt.bd[0]=V(length)
    bt.bpath[0]=[V(period[k%len(period)]) for k in range(19)]
    bt.bdir[0]=[V(word[k%len(word)]) for k in range(18)]
    out=unpack(b_splay_event(D,state,bt,0,V(False)))
    claims=[]
    links=[]
    for i in range(19):
        for side,k,r in (('L','kl','rl'),('R','kr','rr')):
            child=out[r][i]
            if out[k][i]==0 and isinstance(child,int) and child<19:
                links.append([i,child,side])
                if child==target:claims.append([i,child,side])
    return a,b,period,word,m,out,claims,links
if __name__=='__main__':
    assert not OUT.exists()
    start=time.process_time();rows=[];unresolved=[]
    for n in range(1,9):
        for h in range(n):
            s=n-h
            for bits in itertools.product((False,True),repeat=h):
                for mode in (('ON','OFF') if n<=7 else ('ON',)):
                    for length in range(14,19):
                        assert time.process_time()-start<120,'Diagnostic cap: UNKNOWN'
                        a,b,p,w,m,out,claims,links=replay_left(h,s,bits,mode,length)
                        row={'h':h,'s':s,'bits':list(bits),'zero_mode':mode,
                             'd':length,'target':a[0],'claimant':b[0],
                             'root_claims':claims,'root':out['root']}
                        rows.append(row)
                        if not claims:unresolved.append({**row,'normal_form':out,'links':links})
        print(json.dumps({'union_depth':n,'cases':len(rows),'unresolved':len(unresolved),
                          'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    result={'status':'COMPLETE','cases':len(rows),'root_claim_cases':len(rows)-len(unresolved),
            'unresolved_count':len(unresolved),'cpu_seconds':round(time.process_time()-start,3),
            'rows':rows,'unresolved':unresolved}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','unresolved')}),
          'first_unresolved',json.dumps(unresolved[:1]),flush=True)

