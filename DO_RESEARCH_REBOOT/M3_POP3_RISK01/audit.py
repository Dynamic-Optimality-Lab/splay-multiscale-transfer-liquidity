"""Independent ordered-key enumeration; does not import the population DP."""
import sys,json,time,hashlib
from pathlib import Path
from itertools import product
from collections import Counter
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01')
import reference as R
BASE=Path('DO_RESEARCH_REBOOT/M3_POP3_RISK01')
MARGINS=json.loads((BASE/'risk_selector.json').read_text())['minimum_margins']
CORE=set(16*i for i in range(9))
def shape(helper,word):
    t=R.universe();required={()};forced={():None}
    for j,path in enumerate(word):
        required.update(R.at(t,path[:i])[0] for i in range(len(path)+1));at=R.at(t,path)[0]
        forced[at]=helper if j<len(word)-1 else None;t=R.splay(t,at)
    observed=set(R.SHADOW)|{R.at(t,p)[0] for p in R.SHADOW};owner=R.find(t,());observed.update(n[0] for n in owner[1:] if R.real(n));observed|=required
    for p in tuple(observed):observed.update(p[:i] for i in range(len(p)))
    return observed,required,forced,t[0]
def label_at(code,path):
    def skip(i):
        c=code[i];i+=1
        if c not in 'ab':i=skip(skip(i))
        return i
    i=0
    for side in path:
        assert code[i] not in 'ab','required static ancestor must be real'
        i+=1
        if side:i=skip(i)
    assert code[i] not in 'ab';return int(code[i],16)

def projected_prefixes(counts,helper,word,stats):
    observed,required,forced,terminal_address=shape(helper,word);keys=tuple(sorted(CORE|{16*g-8+j for g,n in enumerate(counts) for j in range(n)}))
    def rec(p,values):
        hasanon=any(x not in CORE for x in values)
        if p not in observed:
            if not hasanon:yield 'a'
            return
        if p not in required and not hasanon:
            yield 'a'
            if not values:yield 'b'
        for i,x in enumerate(values):
            if p in forced:
                typ=forced[p]
                if typ is None and x not in CORE:continue
                if typ is not None and (x in CORE or x//16+1!=typ):continue
            label=format(x//16,'x') if x in CORE else '9'
            for l in rec(p+(0,),values[:i]):
                for r in rec(p+(1,),values[i+1:]):
                    if p==():
                        stats['root_productions']+=1
                        target=int(label,16) if not terminal_address else label_at(l if terminal_address[0]==0 else r,terminal_address[1:])
                        margin=MARGINS['H1' if helper is None else str(helper)][str(int(label,16))+','+str(target)]
                        if margin is None or margin>=2:stats['analytic_rejections']+=1;continue
                    yield label+l+r
    return rec((),keys)
def replay(code,word):
    chars=iter(code);labels={}
    def parse(address):
        c=next(chars)
        if c=='a':return None
        if c=='b':return R.GHOST
        labels[address]=int(c,16);return (address,parse(address+(0,)),parse(address+(1,)))
    t=parse(());assert next(chars,None) is None
    def observe(t):
        owner=R.find(t,());assert owner is not None;out=[]
        for path in R.SHADOW:
            n=t
            for side in path:
                if n is None:break
                if n==R.GHOST:n=owner
                n=n[1+side]
            if n is None:out.append((1,0,0))
            else:
                if n==R.GHOST:n=owner
                k=labels[n[0]];out.append((0,1,k) if k<9 else (0,0,0))
        return tuple(out)
    src=observe(t)
    for j,path in enumerate(word):
        target=R.at(t,path)[0]
        if j<len(word)-1:assert labels[target]==9
        else:assert labels[target]<9
        t=R.splay(t,target)
    return src,observe(t),labels[t[0]]
def main():
    sigma=tuple(map(int,sys.argv[1:11]));folder=BASE/('s'+''.join(map(str,sigma)));out=folder/'audit.json';assert not out.exists();start=time.process_time()
    c=json.loads((folder/'relation.json').read_text());p=json.loads((folder/'potential.json').read_text());B=json.loads(Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01/B_bank.json').read_text());N=c['classes']
    sid={R.frozen(a):i for i,a in enumerate(c['shadows'])};assert len(sid)==N;expected={};num=0
    for a,opts in enumerate(c['options']):
        for H,x,aa,helper,fi,code in opts:
            key=(a,H,x,aa,helper);assert key not in expected;expected[key]=num;num+=1
            assert len(c['families'][fi]['word'])==H and c['families'][fi]['helper']==helper
    matched=bytearray(num);queries=private=0;families=[];grammar_stats={'root_productions':0,'analytic_rejections':0}
    words=[(None,(path,)) for path in R.PATHS]
    for gap in (0,9):
        if sigma[gap]:words.extend((gap,(a,b)) for a,b in product(R.PATHS,repeat=2))
    for helper,word in words:
        seen=set();raw=0
        for counts in product(*(range(n+1) for n in sigma)):
            for code in projected_prefixes(counts,helper,word,grammar_stats):
                private+=1;raw+=1
                if code in seen:continue
                seen.add(code);sa,ta,x=replay(code,word);key=(sid[sa],len(word),x,sid[ta],helper);matched[expected[key]]=1;queries+=1
                if queries%4096==0:
                    assert queries<=1000000 and time.process_time()-start<120,'UNKNOWN independent query/CPU cap'
                    assert len(seen)+len(sid)+len(p['values'])<2000000,'UNKNOWN independent live-state cap'
        if seen:families.append({'helper':helper,'word':[list(path) for path in word],'count':len(seen),'private_assignment_visits':raw})
        print(json.dumps({'sigma':sigma,'helper':helper,'word':word,'canonical_queries':queries,'private_visits':private,'CPU':round(time.process_time()-start,3)}),flush=True)
    assert queries==c['queries'] and sum(matched)==num==c['option_count']
    assert [{k:v for k,v in r.items() if k!='private_assignment_visits'} for r in families]==c['families'];del expected,matched
    psi=B['psi'];values={int(k):v for k,v in p['values'].items()};assert p['N']==N and p['default']=='-psi(B)'
    byroot={r:[] for r in range(9)}
    for a,s in enumerate(c['shadows']):byroot[s[0][2]].append(a)
    for k,v in values.items():
        b,a=divmod(k,N);assert c['shadows'][a][0][2]==B['trees'][b][0] and -2<=v<=-psi[b]
    checks=states=zero=0;hist=Counter();auto=Counter()
    for b,t in enumerate(B['trees']):
        for a in byroot[t[0]]:
            states+=1;du=values.get(b*N+a,-psi[b])
            if du==0:zero+=1;continue
            for H,x,aa,helper,fi,code in c['options'][a]:
                if H==1:
                    dep=B['depths'][b][x]
                    if dep==0:auto['nongenuine']+=1;continue
                    bb=B['destinations'][b][x];w=2-dep//2
                else:
                    pair=B['kernels'][str(helper)][b][x]
                    if pair is None:auto['nonchildless_exit']+=1;continue
                    bb,w=pair
                if w>=2:auto['range']+=1;continue
                dv=values.get(bb*N+aa,-psi[bb]);res=w-dv+du;assert res>=0,(sigma,b,a,H,x,du,dv,w);hist[res]+=1;checks+=1
        assert time.process_time()-start<120,'UNKNOWN independent residual CPU cap'
    for b in range(4862):
        for x in range(9):
            w=2-B['depths'][b][x]//2
            if w<0:assert -psi[B['destinations'][b][x]]<=w
    for gap in (0,9):
        assert all(pair is None or pair[1]>=0 for row in B['kernels'][str(gap)] for pair in row)
    report={'status':'INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS','sigma':sigma,'canonical_transition_queries':queries,'private_assignment_visits':private,
      'independent_root_productions':grammar_stats['root_productions'],'analytic_root_productions_rejected':grammar_stats['analytic_rejections'],'duplicate_private_assignments_quotiented':private-queries,'families':families,'classes':N,'access_options':num,'J_range':[-2,0],
      'changed_states':len(values),'explicit_residuals':checks,'minimum_residual':min(hist),'residual_histogram':dict(hist),'product_states_streamed':states,
      'zero_source_states_discharged':zero,'analytic':dict(auto),'cpu_seconds':round(time.process_time()-start,3),
      'potential_sha256':hashlib.sha256((folder/'potential.json').read_bytes()).hexdigest(),'analytic_fiber_coverage':'REPRESENTATION_PROOF.md and independent selector audit','source_family_audit_pending':True,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='families'},indent=2),flush=True)
if __name__=='__main__':main()
