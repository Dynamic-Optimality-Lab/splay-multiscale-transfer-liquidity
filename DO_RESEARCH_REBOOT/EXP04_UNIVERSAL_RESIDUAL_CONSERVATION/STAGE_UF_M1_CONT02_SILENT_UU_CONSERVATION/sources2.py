from base2 import *
from coercion import coerce,advance

def padded(k,L):
    assert k>=3 and L>=1
    m=2;blocks=[];pos=3
    for i in range(1,k+1):
        p=pos;pos+=1;extras=list(range(pos,pos+2*L-1));pos+=len(extras)
        z,y,x=pos,pos+1,pos+2;pos+=3
        blocks.append({'i':i,'p':p,'extra':extras,'z':z,'y':y,'x':x})
    low,high=1,pos;n=high
    ac={str(j):[None,None] for j in range(1,n+1)}
    ac[str(m)][0]=low;prev=m
    for b in blocks:
        p,z,y,x=b['p'],b['z'],b['y'],b['x'];ts=b['extra']
        ac[str(prev)][1]=p;ac[str(p)][1]=ts[0]
        for a,c in zip(ts,ts[1:]):ac[str(a)][1]=c
        ac[str(z)][0]=prev;ac[str(y)][0]=z;ac[str(x)][0]=y;prev=x
    M=prev;ac[str(M)][1]=high;a0={'root':M,'children':ac}
    bc={str(j):[None,None] for j in range(1,n+1)}
    bc[str(low)][1]=high;bc[str(high)][0]=m;bc[str(m)][1]=blocks[-1]['p']
    for i,b in enumerate(blocks):
        p,z,y,x=b['p'],b['z'],b['y'],b['x'];ts=b['extra']
        bc[str(p)]=[blocks[i-1]['p'] if i else None,ts[0]]
        for a,c in zip(ts,ts[1:]+[z]):bc[str(a)][1]=c
        bc[str(z)][1]=x;bc[str(x)][0]=y
    b0={'root':low,'children':bc}
    reach,reachstats=coerce(b0,a0)
    body=[];critical=[];enclosers=[]
    for b in reversed(blocks):
        critical.append(len(body)+1);body.append(['K',b['x']])
        enclosers.append(len(body)+1);body.append(['K',b['y']])
    b,_=advance(b0,[x for tag,x in body]);corekeys=list(range(m,high))
    visit=[low]+corekeys+[high,low];b,_=advance(b,visit);back,backstats=coerce(b,b0)
    def guard(x):
        if x==low:return [['D',m],['K',x],['D',m]]
        if x==high:return [['D',M],['K',x],['D',M]]
        return [['K',x]]
    word=body+[q for x in visit+back for q in guard(x)]
    a,_=advance(a0,[x for tag,x in word])
    assert a['children'][str(m)][0]==low and a['children'][str(M)][1]==high
    core={'root':a['root'],'children':{j:[None if x in (low,high) else x for x in cs]
        for j,cs in a['children'].items() if int(j) not in (low,high)}}
    target={'root':a0['root'],'children':{j:[None if x in (low,high) else x for x in cs]
        for j,cs in a0['children'].items() if int(j) not in (low,high)}}
    repair,repairstats=coerce(core,target);word += [['D',x] for x in repair]
    assert advance(a0,[x for tag,x in word])[0]==a0
    assert advance(b0,[x for tag,x in word if tag=='K'])[0]==b0
    return {'name':f'M1C2_padded_silent_chain_k{k}_L{L}','family':'lower_B_spine_padded_silent_UU',
        'k':k,'L':L,'blocks':blocks,'critical_operations':critical,'enclosure_operations':enclosers,
        'critical_g':m,'low_guard':low,'high_guard':high,'max_core':M,'initial_A':a0,'initial_B':b0,
        'diagonal_initial':b0,'reaching_prefix':[['D',x] for x in reach],'operations':word,
        'prefix_stats':reachstats,'B_return_stats':backstats,'A_repair_stats':repairstats,
        'expected_population':k*(2*L+3)+3,'expected_late_critical_index':L+1,
        'expected_incoming_A_at_later_critical':1,'guarded_entire_period':True}

def sources():return [padded(k,L) for k,L in ((4,1),(4,2),(4,4),(16,4),(32,6),(64,6))]
