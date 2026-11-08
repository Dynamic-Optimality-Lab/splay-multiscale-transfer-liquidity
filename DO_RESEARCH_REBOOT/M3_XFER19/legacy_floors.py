"""Literal lower-floor translation of completed XFER01-13 predicates.

No new debt fit. All conditions are on the original core and alpha/mu
fields; PORT and EMPTY stay distinct. This file requires an independent
guard/source audit before any complete Step4 promotion.
"""
import z3
from target_floor import N,dp,AND,OR,only_v,v_exact
ANY='*'
def shape(t,p):
    if p==ANY:return True
    if t is None or p is None:return t is p
    return t[0]==p[0] and shape(t[1],p[1]) and shape(t[2],p[2])
def cr(t,p=()):
    for b in p:
        if t is None:return None
        t=t[1+b]
    return None if t is None else t[0]
def minpair(m,a,b):
    return AND(m[a],m[b],*(z3.Not(m[k]) for k in range(b) if k!=a)) if a<b else z3.BoolVal(False)
def exactmask(m,keys):return AND(*(m[k] if k in keys else z3.Not(m[k]) for k in range(9)))
def legacy_floor(t,A,m,level):
    r=t[0];d=dp(t);caps=[]
    sc=lambda i,k:A[i]==k
    real=lambda i:A[i]<=9
    nr=lambda i:A[i]>=10 # observation resolves G; nonreal10/12 only
    port=lambda i:A[i]==10
    anon=lambda i:A[i]==9
    upper=only_v(A,m,set(range(4,9)))
    def add(guard,**meta):caps.append(guard)
    def h(guard,x):
        if d[x]<=(7 if level==1 else 5):add(guard)
    # XFER01, fixed source other-position guard includes kind2 EMPTY.
    for i in (1,2):
        for x in range(9):
            if x!=r:h(AND(sc(i,x),m[x],*(nr(j) for j in range(1,7) if j!=i)),x)
    # XFER02 and03, exact PORT guards (never a normalized nonreal).
    for a in range(9):
        for b in range(a+1,9):
            pair=minpair(m,a,b)
            if r==b:h(AND(pair,port(2),OR(sc(1,a),sc(4,a)),v_exact(A,m,{a})),a)
            if r==a:h(AND(pair,sc(2,b),port(6),v_exact(A,m,{b})),b)
            if b in (4,5):
                if level==1 and r==b and d[a]<=3:add(AND(pair,sc(3,a)))
                if r==a and d[b]<=3:add(AND(pair,sc(6,b),v_exact(A,m,{b})))
                if r==b:add(AND(pair,sc(3,a),v_exact(A,m,{a}),port(2)))
    J5=N(5,N(4,ANY,None),N(8,N(6,None,N(7)),None))
    J6=N(6,N(4,ANY,N(5)),N(8,N(7),None))
    J7=N(7,N(4,ANY,N(6,N(5),None)),N(8))
    B6=N(6,N(5,N(4,ANY,None),None),N(7,None,N(8)))
    B7=N(7,N(5,N(4,ANY,None),N(6)),N(8))
    B8=N(8,N(5,N(4,ANY,None),N(7,N(6),None)),None)
    B6p=N(6,N(5,N(4,ANY,None),None),N(8,N(7),None))
    direct=shape(t,J5) or shape(t,J6)
    buried=any(shape(t,p) for p in (B6,B7,B8))
    rbcore=buried or shape(t,B6p)
    C5=N(5,N(4,ANY,None),N(6,None,N(8,N(7),None)))
    F6=N(4,ANY,N(5,None,N(6,None,N(7,None,N(8)))))
    F8=N(4,ANY,N(5,None,N(8,N(7,N(6),None),None)))
    H8=N(8,N(7,N(6,N(5,N(4,ANY,None),None),None),None),None)
    Cx5=N(5,N(4,ANY,None),N(7,N(6),N(8)))
    Cx6=N(6,N(4,ANY,N(5)),N(7,None,N(8)))
    for a in range(4):
        pair=minpair(m,a,4)
        separator=OR(anon(3),*(AND(sc(3,k),z3.Not(m[k])) for k in range(a+1,4)))
        separated=OR(AND(sc(1,4),separator),AND(real(1),sc(3,4)))
        #04 J,05 Z,06 N: all are cap2, hence imply either threshold.
        if direct:
            add(AND(pair,sc(1,4),OR(*(AND(sc(3,k),z3.Not(m[k])) for k in range(a+1,4))),upper))
            add(AND(pair,real(1),sc(3,4),upper))
            add(AND(pair,sc(1,4),anon(3),upper))
        #05 K/C,07 Kx/Cx,08 KB/RB/CB/TB one-credit sources.
        if level==1:
            if r==a:
                for c in (5,6,7,8):
                    if d[4]<=3 and d[c]<=3:
                        if c==5:add(AND(pair,m[5],sc(2,4),sc(6,5)))
                        if c in (5,6):add(AND(pair,m[c],m[7],sc(2,4),sc(6,c)))
                        if c in (6,7,8):add(AND(pair,m[c],sc(2,4),sc(6,c)))
            if shape(t,C5):add(AND(pair,sc(1,4)))
            if shape(t,Cx5) or shape(t,Cx6):add(AND(pair,m[7],sc(1,4)))
            if rbcore and d[a]<=5:add(AND(pair,OR(AND(sc(1,4),sc(3,a)),AND(real(1),sc(3,4)))))
            if (shape(t,F6) or shape(t,F8)) and d[a]<=3:add(pair)
            if shape(t,H8) and d[a]<=7:add(AND(pair,upper))
        #07 G7 and08 GB cap2.
        if shape(t,J7):add(AND(pair,upper,separated))
        if buried and d[a]<=5:add(AND(pair,upper,separated))
        #12 boundary and relay cap2 predicates.
        if direct or (buried and d[a]<=5):add(AND(pair,real(1),sc(3,4)))
        if any(shape(t,p) for p in (J5,J6,J7)) and d[a]<=2:add(AND(pair,sc(1,4),sc(3,a)))
        if shape(t,N(8,N(4,ANY,ANY),None)) and d[a]<=2:add(AND(pair,sc(1,4),sc(3,a)))
        if shape(t,N(8,N(4,ANY,N(7,N(5,None,N(6)),None)),None)) and d[a]<=2:
            add(AND(exactmask(m,{a,4,5,6,8}),sc(1,5),sc(3,4)))
        if r==4 and cr(t,(0,))==a:
            if shape(t,N(4,ANY,N(5,None,ANY))):add(AND(pair,m[5],sc(1,a),sc(2,5)))
            if shape(t,N(4,ANY,N(8,ANY,None))):add(AND(pair,m[8],sc(1,a),sc(2,8)))
        if r==a and shape(t,N(a,ANY,N(4,ANY,N(8,ANY,None)))):
            add(AND(pair,m[8],sc(2,4),sc(6,8)))
    #09 opaque interval child, reflected call gives I_R.
    for x in range(r):h(AND(m[x],sc(1,x),nr(3),nr(2),v_exact(A,m,{x})),x)
    #10 root-unmarked clauses are FALSE at every LOW target P.
    #11 J/G and12 K/G45 have the first two marks a<b4/5.
    for b in (4,5):
        for a in range(b):
            pair=minpair(m,a,b)
            for c in range(b+1,9):
                if r==a and cr(t,(1,))==b and cr(t,(1,1))==c and c-b<=3:
                    add(AND(pair,m[c],sc(2,b),sc(6,c)))
                if r==c and cr(t,(0,))==b and d[a] in (4,5):
                    add(AND(pair,m[c],sc(1,b),sc(3,a),nr(4),nr(2)))
                if r==a and cr(t,(1,))==c:
                    first=cr(t,(1,0))==b
                    q=cr(t,(1,0));second=q is not None and a<q<b and cr(t,(1,0,1))==b
                    if first or second:add(AND(pair,m[c],sc(2,b),sc(6,c)))
    #13 exact-mask non-extremal exposure predicates, including boundary
    # floors that need no fresh source and therefore no V filter.
    mask=exactmask(m,{0,2,4,5,8})
    LA=N(0,None,N(2,N(1),N(3)))
    LB=N(2,N(1,N(0),None),N(3))
    GG=N(5,N(4,N(3,N(0,None,N(1,None,N(2))),None),None),ANY)
    TT=N(2,N(1,N(0),None),N(5,N(3,None,N(4)),ANY))
    RR=N(0,None,N(1,None,N(2,None,N(5,N(3,None,N(4)),ANY))))
    if shape(t,TT):add(AND(mask,sc(2,4),sc(6,5)))
    if shape(t,GG):add(AND(mask,sc(1,4),sc(3,2),nr(4),nr(2)))
    if level==1:
        if shape(t,B8):add(AND(mask,real(1),sc(3,4)))
        if shape(t,RR):
            add(AND(mask,real(2),sc(6,2)))
            add(AND(mask,sc(2,2),sc(6,4)))
        if shape(t,N(8,N(5,N(4,LA,None),N(7,N(6),None)),None)):
            add(AND(mask,sc(1,4),sc(3,2)))
        if shape(t,N(4,LA,N(5,None,ANY))):add(AND(mask,sc(1,2),sc(3,0)))
        if shape(t,N(4,LB,N(5,None,ANY))):add(AND(mask,sc(1,2),sc(2,5)))
    return OR(*caps)
