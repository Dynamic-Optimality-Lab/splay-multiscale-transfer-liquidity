from exp02_core import *
from exp01_sources import H,source,ops,reflect


def interrupted_H(p=4,L=3,interrupt=(1,),q=1,copies=1):
    src=H(p,q);n=len(src["initial_A"]["children"])
    prefix=src["operations"][:2*n-1]
    core=prefix+ops("K",range(1,L+1))+ops("K",interrupt)+ops("K",range(L+1,n+1))+ops("K",range(n-1,0,-1))
    return source(f"IH_p{p}_q{q}_L{L}_z{'-'.join(map(str,interrupt))}_c{copies}",n,core*copies,
        family="IH",p=p,q=q,L=L,interrupt=list(interrupt),copies=copies)


def cheap_zero_Q_distortion(n=9,L=4):
    word=ops("K",range(1,L+1))+[["K",L-1]]+ops("K",range(L+1,n+1))+ops("K",range(n-1,0,-1))
    return source(f"zig_distortion_n{n}_L{L}",n,word,family="zig_distortion")


def repeated_nonidentity(p=4,L=3,targets=(1,65),repeats=2):
    src=interrupted_H(p,L,targets)
    src["operations"]=src["operations"]*repeats
    src.update(name=src["name"]+f"_periods{repeats}",family="IH_repeated")
    return src


def new_corpus():
    result=[cheap_zero_Q_distortion()]
    for p in (4,5,6):
        n=2**(p+2)+1
        for L,interruption in ((3,(1,)),(3,(2,)),(3,(n,)),(3,(1,n)),(3,(n,1)),(7,(1,)),(7,(n,))):
            result.append(interrupted_H(p,L,interruption))
    result += [repeated_nonidentity(4,3,(1,65),r) for r in (2,4)]
    result += [reflect(interrupted_H(5,3,(1,129))),reflect(interrupted_H(4,3,(1,)))]
    return result
