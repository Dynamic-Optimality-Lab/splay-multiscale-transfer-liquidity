"""Exact check of a root-pinned repair on the existing six-key metric certificate.

No new pair graph or fitted coefficients. One extra132-node metric BFS checks
DELETE at the changed A root. General no-go theorems are analytic, not extrapolated.
"""
from pathlib import Path
from fractions import Fraction
from collections import deque
import sys,json,hashlib,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P
PRIOR=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_potential_20261031_v001'

def ck(x,msg):
    if not x:raise AssertionError(msg)
def save(name,data):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(data,f,indent=2)
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def enc(t):return None if t==S.LEAF else [t[1],enc(t[2]),enc(t[3])]
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    if p['l'] is not None:p['l']['p']=p
    if p['r'] is not None:p['r']['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
def rat(v,scale):return str(Fraction(v,scale))

def source(a,b,mode,x):
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None
    ap,ae=S.trace(a,x)
    if mode=='K':bp,be=S.trace(b,x)
    else:bp=b;be=[]
    pa,ea=P.splay_trace(ptr(enc(a)),x)
    if mode=='K':pb,eb=P.splay_trace(ptr(enc(b)),x)
    else:pb=ptr(enc(b));eb=[]
    ck(raw(pa)==enc(ap) and raw(pb)==enc(bp),'pointer/frame full states')
    ck(len(ea)==len(ae) and len(eb)==len(be),'source event counts')
    r={'mode':mode,'key':x,'source_A':enc(a),'source_B':enc(b),'destination_A':enc(ap),'destination_B':enc(bp),
       'dA':da,'dB':db,'a':len(ae),'q':sum(e[0]!='ZIG' for e in be),'z':sum(e[0]=='ZIG' for e in be),
       'events_A':ae,'events_B':be}
    return ap,bp,r

def splay_word(start,goal,n):
    if start==goal:return []
    queue=deque([start]);parent={start:None}
    while queue and goal not in parent:
        a=queue.popleft()
        for x in range(1,n+1):
            b=S.trace(a,x)[0]
            if b not in parent:parent[b]=(a,x);queue.append(b)
    ck(goal in parent,'fixed six-key source connector exists')
    word=[];a=goal
    while a!=start:
        a0,x=parent[a];word.append(x);a=a0
    return word[::-1]

def main():
    dep=[ROOT/'python/liquidity/legacy_embedding.py',ROOT/'python/independent/splay.py',
       ROOT/'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
       PRIOR/'explicit_potential_countercertificate.json',PRIOR/'independent_audit.json',
       PRIOR/'SP02_RAW_GEOMETRIC_RESERVE_LEMMAS.md',PRIOR/'SP03_ENVELOPE_LAW_AND_ALL_SIZE_REFUTATION.md',
       ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
       ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
       ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    pins={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in dep}
    entry={'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'files':pins}
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked tree clean')
    save('entry_source_pins.json',entry)
    c=json.loads((PRIOR/'explicit_potential_countercertificate.json').read_text(encoding='utf-8'))
    ck(json.loads((PRIOR/'independent_audit.json').read_text(encoding='utf-8'))['status']=='PASS','inherited exact metric audit')
    n=c['n'];scale=c['scale'];metric=c['metric_certificate'];ts=[dec(t) for t in metric['trees']];ids={t:i for i,t in enumerate(ts)}
    A=dec(c['initial_source_A']);B=dec(c['initial_source_B']);Ad=S.trace(A,n)[0];Bk=S.trace(B,1)[0]
    adj=metric['adjacency'];start=ids[Ad];dist=[-1]*len(ts);parents=[None]*len(ts);dist[start]=0;q=deque([start])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if dist[v]<0:dist[v]=dist[u]+1;parents[v]=u;q.append(v)
    ck(all(d>=0 for d in dist),'additional metric BFS complete')
    ck(all(abs(dist[u]-dist[v])<=1 for u,row in enumerate(adj) for v in row),'all edge metric bounds')
    ck(all(i==start or (parents[i] in adj[i] and dist[parents[i]]==dist[i]-1) for i in range(len(ts))),'actual metric paths')
    def g(t,b):return sum(8**(n-1-S.lookup(t,x)[1])*S.lookup(b,x)[1] for x in range(1,n+1))
    before=c['all_exact_scaled_scores_source'];afterK=c['all_exact_scaled_scores_destination']
    afterD=[g(t,B)-scale*d for t,d in zip(ts,dist)]
    U0=max(before);UK=max(afterK);UD=max(afterD)
    L0=max(v for t,v in zip(ts,before) if t[1]==A[1])
    LK=max(v for t,v in zip(ts,afterK) if t[1]==A[1])
    LD=max(v for t,v in zip(ts,afterD) if t[1]==Ad[1])
    ck(Fraction(L0,scale)==Fraction(197,128),'root-pinned source')
    ck(Fraction(LD,scale)==Fraction(533,128) and Fraction(LD-L0,scale)==Fraction(21,8),'root-pinned DELETE failure')
    ck(Fraction(LK,scale)==Fraction(2801,4096),'root-pinned KEEP value')
    ck(UD-U0==scale,'unrestricted DELETE law saturated')
    _,_,delete=source(A,B,'D',n);_,_,keep=source(A,B,'K',1)
    ck(delete['a']==1 and keep['a']==keep['q']==0 and keep['z']==1,'same source two required tests')
    # A full diagonal closed DELETE-only witness for the root-pinned failure.
    prefix=[('D',x) for x in splay_word(B,A,n)]
    word=prefix+[('D',n)]+[('D',x) for x in splay_word(Ad,B,n)]
    aa=bb=B;rows=[]
    for mode,x in word:aa,bb,row=source(aa,bb,mode,x);rows.append(row)
    ck(aa==bb==B,'exact source paired closure')
    ck(rows[len(prefix)]['source_A']==enc(A) and rows[len(prefix)]['source_B']==enc(B),'failed DELETE reached')
    # These are exact constraints from n6 only, not a fit or a sufficiency claim.
    lower=Fraction(LD-L0-2*scale,(LD-L0)-(UD-U0))
    upper=Fraction(-(LK-L0),(UK-U0)-(LK-L0))
    ck(lower==Fraction(5,13) and upper==Fraction(3503,7168) and lower<upper,'honest finite overlap')
    result={'status':'ROOT_PINNED_REPAIR_REFUTED','r':'1/8','n':n,'initial_source_A':enc(A),'initial_source_B':enc(B),
      'values':{'L_source':rat(L0,scale),'L_after_DELETE':rat(LD,scale),'L_after_KEEP':rat(LK,scale),
                'U_source':rat(U0,scale),'U_after_DELETE':rat(UD,scale),'U_after_KEEP':rat(UK,scale)},
      'increments':{'L_DELETE':rat(LD-L0,scale),'L_KEEP':rat(LK-L0,scale),
                    'U_DELETE':rat(UD-U0,scale),'U_KEEP':rat(UK-U0,scale)},
      'delete_edge':delete,'keep_edge':keep,
      'new_metric_row':{'anchor_index':start,'distances':dist,'parents':parents},
      'all_exact_scaled_DELETE_scores':afterD,'metric_input':'prior explicit_potential_countercertificate.json',
      'closed_DELETE_only_witness':{'initial_A':enc(B),'initial_B':enc(B),'word':word,'failed_edge_index':len(prefix),
          'full_replay':rows,'paired_closure':True,'A':sum(r['a'] for r in rows),'Q_B':sum(r['q'] for r in rows)},
      'n6_necessary_theta_interval':{'lower_from_DELETE':str(lower),'upper_from_KEEP':str(upper),
                                   'nonempty':True,'not_sufficient':True,'coefficient_fitted':False},
      'analytic_all_size_claim':'root-pinned class fails DELETE for n>=7; convex blends fail both-law necessity for every n>=13',
      'analytic_claim_proved_by':'AL02 and AL03 source inequalities; not extrapolated from this n6 interval',
      'single_tree_states_reused':132,'directed_rotation_arcs_reused':660,'new_pair_graphs':0,'fitted_parameters':0}
    save('root_aligned_countercertificate.json',result)
    changes=[p for p,h in pins.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    save('integrity.json',{'status':'PASS' if not changes and not git('status','--porcelain=v1','--untracked-files=no') else 'FAIL',
       'source_changes':changes,'Stage11G_modified':False,'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current')})
    print(json.dumps({'status':result['status'],'values':result['values'],'increments':result['increments'],
      'n6_theta_interval':result['n6_necessary_theta_interval'],'closed_word_accesses':len(word),'fitted_parameters':0},indent=2))

if __name__=='__main__':main()
