"""Present-key parent-first source identities with arbitrary rigid gap terms."""
def N(k,l,r):return (k,l,r)
def node(t):return isinstance(t,tuple)
def inorder(t):return inorder(t[1])+[t[0]]+inorder(t[2]) if node(t) else [t]
def path(t,x):
    p=''
    while node(t):
        if t[0]==x:return p
        c='L' if x<t[0] else 'R';p+=c;t=t[1 if c=='L' else 2]
    raise AssertionError(('absent or attempted entry of free gap',x,t))
def at(t,p):
    for c in p:t=t[1 if c=='L' else 2]
    return t
def put(t,p,v):
    if not p:return v
    k,l,r=t
    return N(k,put(l,p[1:],v),r) if p[0]=='L' else N(k,l,put(r,p[1:],v))
def event(t,word):
    g,l,r=t
    if word=='LL':p,(x,a,b),c=l;return N(x,a,N(p,b,N(g,c,r)))
    if word=='RR':p,b,(x,c,d)=r;return N(x,N(p,N(g,l,b),c),d)
    if word=='LR':p,a,(x,b,c)=l;return N(x,N(p,a,b),N(g,c,r))
    if word=='RL':p,(x,b,c),d=r;return N(x,N(g,l,b),N(p,c,d))
    if word=='L':x,a,b=l;return N(x,a,N(g,b,r))
    if word=='R':x,a,b=r;return N(x,N(g,l,a),b)
    raise AssertionError(word)
def trace(t,x):
    original=path(t,x);p=original;events=[]
    while len(p)>=2:
        pre,w=p[:-2],p[-2:];s=at(t,pre)
        parent=s[1 if w[0]=='L' else 2][0]
        t=put(t,pre,event(s,w));events.append({'case':w,'G':s[0],'P':parent,'target':x,'kind':'DOUBLE'});p=pre
    if p:
        s=t;t=event(t,p);events.append({'case':p,'P':s[0],'target':x,'kind':'ZIG'})
    assert t[0]==x and len(events)==(len(original)+1)//2
    return t,original,events
def vine(n):
    t='F'+str(n)
    for k in range(n,0,-1):t=N(k,'F'+str(k-1),t)
    return t
def core(t,marks):
    if not node(t):return None
    l,r=core(t[1],marks),core(t[2],marks)
    return (t[0],l,r) if t[0] in marks or l is not None or r is not None else None
def labels(t):return set() if t is None else {t[0]}|labels(t[1])|labels(t[2])
def shadow(t,scores):
    result={}
    for p in ('','L','R','LL','LR','RL','RR'):
        u=t
        for c in p:
            if not node(u):break
            u=u[1 if c=='L' else 2]
        result[p]={'kind':0,'isS':True,'index':scores.index(u[0]),'key':u[0]} if node(u) and u[0] in scores else {'not_a_known_ScoreAt':True}
    return result
def chart(t,marks):
    q=core(t,set(marks));s=sorted(labels(q));idx={k:i for i,k in enumerate(s)}
    def conv(u):return None if u is None else (idx[u[0]],conv(u[1]),conv(u[2]))
    return {'marks':sorted(marks),'Scores':s,'tree':conv(q),'size':len(s)}
def operations(mode,keys):return [(mode,k) for k in keys]
def omega_plus():
    w=operations('K',[3,5,7,9,11,9,7,5,3,1])
    w+=operations('K',[3])+operations('D',[1,4,1,11,1,11,3,1])
    w+=operations('K',[1,11,1])+operations('D',[2,4,11,1,2,1])
    w+=operations('K',[3,5,7,9,11,9,7,5,3,1])
    assert len(w)==38
    return w
def gamma_pair():
    w=operations('K',[3,5,7,9,11,9,7,5,3])+operations('D',[11,1])+operations('K',[1,11,1])
    w+=operations('D',[11,2,11,1])+operations('K',[3,5,7,9,11,9,7,5,3,1])
    assert len(w)==28
    return w
SCAN=list(range(1,12))+list(range(10,0,-1))
def singleton_sigma():
    w=operations('K',[9,1,3,5,3,1])
    w+=operations('K',[11,1,3,5,9,11,9,5,3,1])
    w+=operations('K',[3])+operations('D',SCAN)+operations('D',[4,1,7,1,7,3,1])+operations('K',[1,7])
    w+=operations('D',SCAN+[7])+operations('K',[1,3,5,7,5,3,1])
    assert len(w)==76
    return w
def core10_control():
    f=['F'+str(i) for i in range(11)]
    s=N(9,N(6,N(1,f[0],N(2,f[1],N(5,N(4,N(3,f[2],f[3]),f[4]),f[5]))),N(8,N(7,f[6],f[7]),f[8])),N(10,f[9],f[10]))
    return s,operations('K',[3,7,1,9,5,7,1,9,10,9])
def replay(initial,word,erased=None,erased_start=None):
    a=b=initial;e=initial if erased_start is None else erased_start;rows=[];initial_order=inorder(initial)
    for occurrence,(mode,x) in enumerate(word,1):
        before=(a,b,e);a,pa,ea=trace(a,x)
        pb='';eb=[];pe='';ee=[];genuine=mode=='K' and x!=b[0]
        if mode=='K':b,pb,eb=trace(b,x)
        if mode=='K' and x!=erased:e,pe,ee=trace(e,x)
        assert inorder(a)==inorder(b)==inorder(e)==initial_order
        rows.append({'occurrence':occurrence,'mode':mode,'target':x,'genuine_F':genuine,
            'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ee,
            'a':len(ea),'qF':sum(q['kind']=='DOUBLE' for q in eb),'qE':sum(q['kind']=='DOUBLE' for q in ee),
            'before':before,'after':(a,b,e)})
    return rows,(a,b,e)
def packets(rows):
    ends=[r['occurrence'] for r in rows if r['genuine_F']];macros=[];n=len(rows)
    for j,end in enumerate(ends):
        prev=ends[j-1];seg=rows[prev:end] if prev<end else rows[prev:]+rows[:end]
        assert seg
        macros.append({'start_after':prev,'end':end,'H':sum(r['a'] for r in seg),'Q':rows[end-1]['qF'],
            'occurrences':[r['occurrence'] for r in seg]})
    covered=set();result=[]
    for j,m in enumerate(macros):
        if m['Q']!=5:continue
        k=(j+1)%len(macros);assert macros[k]['Q']==1 and j not in covered and k not in covered
        covered|={j,k}
        H=m['H']+macros[k]['H'];result.append({'macro_indices':[j,k],'H':H,'Q':6,'w':2*min(H,4)-6,
            'start_after':m['start_after'],'end':macros[k]['end'],'occurrences':m['occurrences']+macros[k]['occurrences']})
    for j,m in enumerate(macros):
        if j not in covered:
            assert m['Q']<=4
            result.append({'macro_indices':[j],'H':m['H'],'Q':m['Q'],'w':2*min(m['H'],4)-m['Q'],
                'start_after':m['start_after'],'end':m['end'],'occurrences':m['occurrences']})
    result.sort(key=lambda p:min(p['macro_indices']))
    assert sum(p['H'] for p in result)==sum(r['a'] for r in rows)
    assert sum(p['Q'] for p in result)==sum(r['qF'] for r in rows)
    return result
def cyclic_path_min(ps):
    best=0;witness=[]
    for i in range(len(ps)):
        total=0
        for k in range(len(ps)):
            total+=ps[(i+k)%len(ps)]['w']
            if total<best:best=total;witness=[(i+j)%len(ps) for j in range(k+1)]
    return {'minimum':best,'packet_indices':witness,'whole_period_price':sum(p['w'] for p in ps),
        'scope':'all contiguous cyclic paths of at most one packet period in this actual witness only'}
def cyclic_lru(rows):
    result=[]
    for r in reversed(rows):
        if r['mode']=='K' and r['target'] not in result:result.append(r['target'])
    return result
def charts(rows,marks):
    lru=cyclic_lru(rows);answer=[]
    assert set(lru)==set(marks)
    for r in rows:
        old=lru[:];old_chart=chart(r['before'][1],old[:5])
        if r['mode']=='K':lru.remove(r['target']);lru.insert(0,r['target'])
        new_chart=chart(r['after'][1],lru[:5])
        answer.append({'occurrence':r['occurrence'],'recent_before':old,'recent_after':lru[:],
            'cold':r['mode']=='K' and r['target'] not in old[:5],'old_chart':old_chart,'new_chart':new_chart})
    assert lru==cyclic_lru(rows)
    return answer
