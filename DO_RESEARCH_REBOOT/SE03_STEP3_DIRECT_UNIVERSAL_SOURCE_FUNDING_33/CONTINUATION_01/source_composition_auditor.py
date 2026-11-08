"""Independent finite-word proof checker over an immutable verified kernel."""
def depth_vector(tree,n):
    out=[None]*n
    def visit(t,d):
        if isinstance(t,str):return
        k,l,r=t;out[k-1]=d;visit(l,d+1);visit(r,d+1)
    visit(tree,0);assert all(v is not None for v in out);return out
def check(native,z):
    T=native['trees'];D=native['destination'];H=native['H'];Q=native['Q'];n=len(D[0]);word=z['word'];state=[z['initial_diagonal_index']]*3;rows={r[0]:r for r in z['rows']};lru=[];elru=[];start=charts=None;seen=[];compositions=0
    for copy in range(z['u']+z['L']):
        for local,(mode,x) in enumerate(word,1):
            assert mode in ('K','D') and 1<=x<=n;t=copy*len(word)+local
            if t==z['period'][0]:start=state[:];charts=(lru[:],elru[:])
            before=state[:];state[0]=D[state[0]][x-1];a=H[before[0]][x-1];q=qe=0;compositions+=1
            if mode=='K':
                state[1]=D[state[1]][x-1];q=Q[before[1]][x-1];compositions+=1
                if x in lru:lru.remove(x)
                lru.insert(0,x)
                if x!=n:
                    state[2]=D[state[2]][x-1];qe=Q[before[2]][x-1];compositions+=1
                    if x in elru:elru.remove(x)
                    elru.insert(0,x)
            if t in rows:
                expected=[t,mode,x]+before+state[:]+[a,q,qe];assert expected==rows[t];seen.append(t)
    assert seen==list(rows) and state==start and (lru,elru)==charts and z['period']==[z['u']*len(word)+1,(z['u']+z['L'])*len(word)];assert {r[2] for r in z['rows'] if r[1]=='K' and T[r[4]][0]!=r[2]}==set(range(1,n+1));lo,hi=z['natural_packet'];prev=rows[lo-1];assert prev[1]=='K' and T[prev[4]][0]!=prev[2];seg=[rows[t] for t in range(lo,hi+1)];assert seg[-1][1]=='K' and T[seg[-1][4]][0]!=seg[-1][2] and not any(r[1]=='K' and T[r[4]][0]!=r[2] for r in seg[:-1]);before=[T[i] for i in seg[0][3:5]];after=[T[i] for i in seg[-1][6:8]];assert before[0][0]==before[1][0] and after[0][0]==after[1][0];dA0,dB0=(depth_vector(t,n) for t in before);dA1,dB1=(depth_vector(t,n) for t in after);delta0=[b//2-2*((a+1)//2) for a,b in zip(dA0,dB0)];delta1=[b//2-2*((a+1)//2) for a,b in zip(dA1,dB1)];Hwhole=sum(r[9] for r in seg);Qwhole=sum(r[10] for r in seg);A=sum(r[9] for r in z['rows']);QF=sum(r[10] for r in z['rows']);assert (Hwhole,Qwhole,A,QF)==(z['H'],z['Q'],z['A'],z['QF']) and 2*A-QF>=0
    return {'period':z['period'],'natural_packet':[lo,hi],'H':Hwhole,'Q':Qwhole,'price':2*Hwhole-Qwhole,'CD_margin':2*A-QF,'root_before':before[0][0],'root_after':after[0][0],'delta_before':delta0,'delta_after':delta1,'full_pair_before':seg[0][3:5],'full_pair_after':seg[-1][6:8],'primitive_identity_instantiations_checked':compositions,'terminal_A_cost':seg[-1][9]}
