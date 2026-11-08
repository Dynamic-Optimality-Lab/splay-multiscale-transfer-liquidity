"""Independent exact rational and actual-source audit; no optimizer imported."""
import hashlib,importlib.util,json,pickle,sys,time
from fractions import Fraction
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None;M=set(range(1000,8000,1000))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def node(t):return isinstance(t,tuple)
def bare(t):return (t[0],bare(t[1]),bare(t[2])) if node(t) else None
def keys(t):return [] if not node(t) else keys(t[1])+[t[0]]+keys(t[2])
def reduced(t):
    if not node(t):return None
    l,r=reduced(t[1]),reduced(t[2])
    if t[0] in M:return (t[0],l,r)
    if l is None:return r
    if r is None:return l
    return (t[0],l,r)
def parts(t):
    marked=[];unmarked=[];leaf=0
    def go(u):
        nonlocal leaf
        if u is None:return frozenset()
        l,r=go(u[1]),go(u[2]);v=l|r|({u[0]} if u[0] in M else set());assert v
        (marked if u[0] in M else unmarked).append(frozenset(v))
        if u[0] in M and not l and not r:leaf+=1
        return v
    go(t);return marked,unmarked,leaf
def lcdepth(t,interval):
    lo,hi=min(interval),max(interval);d=0
    while True:
        if hi<t[0]:t=t[1];d+=1
        elif lo>t[0]:t=t[2];d+=1
        else:return d
def features(A,B):
    A=reduced(A);am,au,al=parts(A);bm,bu,bl=parts(B)
    return [sum(lcdepth(A,s) for s in bm),sum(lcdepth(A,s) for s in bu),
      sum(lcdepth(B,s) for s in am),sum(lcdepth(B,s) for s in au),len(set(am+au)&set(bm+bu)),
      sum(s in set(am) for s in bm),sum(s in set(am) for s in bu),
      sum(s in set(au) for s in bm),sum(s in set(au) for s in bu),
      sum(lcdepth(A,{k}) for k in M),sum(lcdepth(B,{k}) for k in M),len(au),al,bl]
def fill(t,K):
    present=set(keys(t))
    def vine(v):return None if not v else (v[0],None,vine(v[1:]))
    def go(u,lo,hi):
        if not node(u):return vine([k for k in K if lo<k<hi and k not in present])
        return (u[0],go(u[1],lo,u[0]),go(u[2],u[0],hi))
    return go(t,0,8000)
def scale(t):return None if not node(t) else (1000*((t[0]+1)//2)+(500 if t[0]%2==0 else 0),scale(t[1]),scale(t[2]))
def main():
    global V
    spec=importlib.util.spec_from_file_location('JC35_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    result=json.loads((F/'joint_cluster_linear_result.json').read_text());cert=result['exact_rational_certificate'];assert cert
    a=json.loads((F/'branch_H1_r7.json').read_text());a2=json.loads((F/'branch_H2_r7.json').read_text());b=json.loads((F/'maximal_B_grammar.json').read_text())
    with (F/'real_leaf_profile_packets.pkl').open('rb') as f:pm=pickle.load(f)
    old=json.loads((F/'independent_leaf_profile_refutation.json').read_text());acache={};bcache={};reused=0
    def code(t,k):return (tup(t),k)
    for c in old['controls']:
        for r in c['actual_rows']:
            acache[code(r['A_before'],r['key'])]=(tup(r['A_after']),r['a'],r['A_events'])
            if r['kind']=='K':bcache[code(r['BF_before'],r['key'])]=(tup(r['BF_after']),r['qF'])
    def act(t,k,isA):
        nonlocal reused
        cache=acache if isA else bcache;key=code(t,k)
        if key in cache:reused+=1;return cache[key]
        z=V.Mutable(t);h,q,ev=z.splay(k,isA);out=(tup(z.snapshot()),h,ev) if isA else (tup(z.snapshot()),q);cache[key]=out;return out
    sums=[Fraction(0)]*len(result['features']);price=Fraction(0);mass=Fraction(0);controls=[]
    for i,row in enumerate(cert['rows']):
        pid,h,key,j,s,t=row['reference'];p=pm['packets'][pid];ss,tt,w=pm['groups'][tuple(key)][j];assert (ss,tt)==(s,t)
        if w[0]=='single':_,hh,rid=w;extra=[]
        else:_,hh,rid,h2,y,mid=w;extra=[1000*(y+1)]
        sw=(a if hh==1 else a2)['witnesses'][rid];start=tup(sw['source']);ops=sw.get('accesses',[1000*(key[3]+1)])+extra
        core=scale(bare(tup(b['trees'][p['source']])));K=sorted(set(keys(start))|set(keys(core)));A,BF=fill(start,K),fill(core,K)
        assert set(keys(A))==set(keys(BF))==set(K)
        f0=features(A,core);rows=[];H=Q=0;firstlen=len(ops)-len(extra)
        for j,k in enumerate(ops):
            keep=j==firstlen-1 or j>=firstlen;ab,bb=A,BF;A,aa,events=act(A,k,True);q=0
            if keep:assert bb[0]!=k;BF,q=act(BF,k,False)
            H+=aa;Q+=q;rows.append({'t':j+1,'key':k,'kind':'K' if keep else 'D','a':aa,'qF':q,
              'A_before':ab,'BF_before':bb,'A_after':A,'BF_after':BF,'A_events':events})
        endcore=scale(bare(tup(b['trees'][p['target']])));f1=features(A,endcore);delta=[v-u for u,v in zip(f0,f1)]
        assert delta==row['delta'] and H==h and Q==p['Q'] and 2*H-Q==row['weight']
        lam=Fraction(row['lambda']);assert lam>0;mass+=lam;price+=lam*row['weight'];sums=[u+lam*v for u,v in zip(sums,delta)]
        controls.append({'reference':row['reference'],'lambda':row['lambda'],'source_features':f0,'target_features':f1,
          'delta':delta,'H':H,'Q':Q,'weight':2*H-Q,'actual_rows':rows,'physical_keys':K,
          'separate_closed_embedding':'accepted A realization over source-closed B strong component; no numerical Gamma replay claimed'})
    assert mass==1 and not any(sums) and price==Fraction(cert['weighted_price'])<0
    out={'status':'PASS_EXACT_SOURCE_FARKAS_CERTIFICATE','features':result['features'],'source_rows':len(controls),
      'coefficient_sum':str(mass),'weighted_price':str(price),'feature_residual':[str(x) for x in sums],
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'reused_exact_source_actions':reused,'controls':controls,
      'JR35':'OPEN','not_one_concatenated_source_cycle':True,'not_Coarse_Double_refutation':True,
      'input_sha256':{p:sha(F/p) for p in ('joint_cluster_linear_result.json','real_leaf_profile_packets.pkl','independent_leaf_profile_refutation.json','JOINT_CLUSTER_POTENTIAL_BOX.md')}}
    with (F/'independent_joint_cluster_alternative.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('features','controls','input_sha256','feature_residual')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify113_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
