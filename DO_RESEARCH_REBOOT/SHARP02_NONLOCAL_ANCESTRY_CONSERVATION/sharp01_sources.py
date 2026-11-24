"""Complete physical source constructors; historical words are never edited."""
from sharp01_oracle import vine, Tree, Replay


def ops(tag, keys):
    return [[tag,k] for k in keys]


def source(name, n, word, state=None, **metadata):
    state = state or vine(range(1,n+1))
    return {"name":name,"initial_A":state,"initial_B":state,
        "operations":word,"reaching_prefix":[],"reachability":"common diagonal, empty prefix",**metadata}


def H(p,q=1):
    n=2**(p+1)*(q+1)+1
    marks={n+1-2**j for j in range(p+1)}
    word=ops("D",range(2,n+1))+[["K" if k in marks else "D",k] for k in range(n,0,-1)]
    word+=ops("K",range(1,n+1))+ops("K",range(n-1,0,-1))
    return source(f"H_{p}_{q}",n,word,family="H",p=p,q=q)


def W(p,q=1,hit=None):
    n=2**(p+1)*(q+1)+1
    marks={n+1-2**j for j in range(p+1)}
    m=min(marks)
    word=ops("D",range(2,n+1))+[["K" if k in marks else "D",k] for k in range(n,m-1,-1)]
    if hit is not None:
        word.append(["K",hit])
    word+=ops("K",range(1,n+1))+ops("K",range(n-1,0,-1))
    return source(f"W_{p}_{q}"+(f"_hit_{hit}" if hit is not None else ""),n,word,family="W",p=p,q=q,hit=hit)


def G(p=4,q=1,L=31,r=1,reset=1):
    src=H(p,q)
    n=len(src["initial_A"]["children"])
    src["operations"][2*n-1:2*n-1]=sum((ops("K",range(1,L+1))+[["K",reset]] for _ in range(r)),[])
    src.update(name=f"G_{p}_{q}_L{L}_r{r}_z{reset}",family="G",L=L,r=r,reset=reset)
    return src


def detour_H(p=4,q=1,positions=(31,),copies=1):
    src=H(p,q)
    n=len(src["initial_A"]["children"])
    word=src["operations"][:2*n-1]
    detours=[]
    for k in range(1,n+1):
        word.append(["K",k])
        if k in positions:
            for _ in range(copies):
                detours.append([len(word)+1,len(word)+2])
                word.extend([["K",k-1],["K",k]])
    word+=ops("K",range(n-1,0,-1))
    src.update(name=f"DH_{p}_{q}_at{'-'.join(map(str,positions))}_c{copies}",family="DH",
        operations=word,detours=detours,positions=list(positions),copies=copies)
    return src


def W_star():
    src=H(3)
    P=ops("D",[1,2])+ops("D",range(1,34))+[["D",32]]
    Q=ops("D",[11,10,1,2])+ops("D",range(1,34))+ops("D",range(32,0,-1))
    word=src["operations"]
    src.update(name="W_star",family="W_star",operations=word[:34]+P+word[34:65]+Q+word[65:])
    return src


def H_dec():
    src=H(3)
    src["operations"][67:67]=ops("D",[11,10])
    src.update(name="H_dec",family="H_dec")
    return src


def lifted_H(p,q=1,r=2):
    core=H(p,q)
    n=len(core["initial_A"]["children"])
    ch={}
    for i in range(1,n+1):
        ch[str(2*i)]=[2*i-1,2*(i+1) if i<n else 2*n+1]
        ch[str(2*i-1)]=[None,None]
    for k in range(2*n+1,2*n+4):
        ch[str(k)]=[None,k+1 if k<2*n+3 else None]
    state={"root":2,"children":ch}
    inner=[[tag,2*x] for tag,x in core["operations"]]
    Z=ops("K",range(1,2*n+4))+ops("K",range(2*n+2,0,-1))+[["K",2*n+1]]
    for k in range(1,n+1):
        Z+=ops("K",range(2*k,1,-2))
    return source(f"lifted_H_{p}_{q}_r{r}",2*n+3,inner*r+Z,state,
        family="lifted_H",p=p,q=q,r=r,inner_length=len(inner),closing_length=len(Z))


def I_m_Z(m):
    # Original 21-key I^m Z is N=9 active indices: the initial max is
    # preceded by A-only ascending prep and exactly three dyadic marked hits.
    src=lifted_H(1,1,m)
    src.update(name=f"I^{m}Z",family="I_m_Z")
    return src


def warm_local(L=15,repeats=4,outer=9):
    # Legal prefix from a diagonal, then a genuinely recurrent lower scan.
    n=L+outer
    initial=vine(range(1,n+1))
    a,b=Tree(initial),Tree(initial)
    prefix=ops("K",range(1,L+1))+[["K",1]]
    for tag,x in prefix:
        Replay.plain_splay(a,x)
        Replay.plain_splay(b,x)
    period=(ops("K",range(1,L+1))+[["K",1]])*repeats
    return {"name":f"warm_local_{L}_{repeats}_{outer}","family":"warm_local",
        "initial_A":a.state(),"initial_B":b.state(),"operations":period,
        "reaching_prefix":prefix,"diagonal_initial":initial,
        "reachability":"explicit all-KEEP prefix from saved diagonal; prefix excluded"}


def warm_marked(p=4,q=1,repeats=3):
    n=2**(p+1)*(q+1)+1
    marks={n+1-2**j for j in range(p+1)}
    m=min(marks)
    packet=[["K" if k in marks else "D",k] for k in range(n,m-1,-1)]
    suffix=ops("D",range(m+1,n+1))
    prefix=ops("D",range(2,n+1))+packet+suffix
    initial=vine(range(1,n+1))
    a,b=Tree(initial),Tree(initial)
    for tag,x in prefix:
        Replay.plain_splay(a,x)
        if tag=="K":
            Replay.plain_splay(b,x)
    return {"name":f"warm_marked_{p}_{q}_r{repeats}","family":"warm_marked",
        "initial_A":a.state(),"initial_B":b.state(),"operations":(packet+suffix)*repeats,
        "reaching_prefix":prefix,"diagonal_initial":initial,
        "reachability":"explicit saved preparation/packet/warmup from common vine; prefix excluded"}


def cyclic_cut(src,replay,cut):
    assert 0<cut<len(src["operations"])
    boundary=replay.boundaries[cut-1]
    return {"name":src["name"]+f"_cut{cut}","family":"cut_"+src["family"],
        "initial_A":boundary["post_A"],"initial_B":boundary["post_B"],
        "operations":src["operations"][cut:]+src["operations"][:cut],
        "diagonal_initial":src["initial_A"],"reaching_prefix":src["operations"][:cut],
        "original_source":src["name"],"original_cut_after_operation":cut,
        "reachability":"saved original prefix from common diagonal; period IDs are the new cut's IDs"}


def campaign15():
    import json
    from pathlib import Path
    parent=Path(__file__).resolve().parent.parent/"SE03_STEP3_UNIFORM_DONOR_GROUPING_15"
    result=[]
    for file in ("leaf_source_certificates2.json","zero_run_source_certificates.json"):
        records=json.loads((parent/file).read_text())["reports"]
        for report in records:
            ch={}
            def convert(t):
                if not isinstance(t,list):
                    return None  # Instantiate every symbolic free gap as empty.
                k,l,r=t
                ch[str(k)]=[convert(l),convert(r)]
                return k
            state={"root":convert(report["initial_A_BF"]),"children":ch}
            name=f"C15_{'zero' if file.startswith('zero') else 'owner'}_r{report['r']}_mirror{report['mirrored']}"
            result.append(source(name,len(ch),report["word"],state,family="C15",
                historical_fixture=str((parent/file).relative_to(parent.parent.parent)),
                fixture_instantiation="all symbolic F gaps empty; owner maps untouched"))
    return result


def reflect(src):
    keys=sorted(int(k) for k in src["initial_A"]["children"])
    mp=dict(zip(keys,reversed(keys)))
    def st(state):
        return {"root":mp[state["root"]],"children":{str(mp[int(k)]):[mp.get(r),mp.get(l)] for k,(l,r) in state["children"].items()}}
    ans={**src,"name":src["name"]+"_reflected","family":src["family"]+"_reflected",
        "initial_A":st(src["initial_A"]),"initial_B":st(src["initial_B"]),
        "operations":[[tag,mp[x]] for tag,x in src["operations"]],
        "reaching_prefix":[[tag,mp[x]] for tag,x in src.get("reaching_prefix",[])]}
    if "diagonal_initial" in src:
        ans["diagonal_initial"]=st(src["diagonal_initial"])
    return ans
