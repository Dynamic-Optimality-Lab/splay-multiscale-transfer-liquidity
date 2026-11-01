"""Exact evaluation of one frozen uniform formula, not a potential fit.

Only n=6:132 single trees and660 directed primitive rotation arcs. The all-n
refutation is analytic; this file independently makes its smallest registered
control numerically exact and replays a complete original closed Pair Access word.
"""
from pathlib import Path
from functools import lru_cache
from collections import deque
from fractions import Fraction
import sys,json,hashlib,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P
N=6;SCALE=8**(N-1)

def ck(x,msg):
    if not x:raise AssertionError(msg)
def save(name,data):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(data,f,indent=2)
def rat(value):
    v=Fraction(value,SCALE)
    return {'numerator':v.numerator,'denominator':v.denominator}
def serial(t):return None if t==S.LEAF else [t[1],serial(t[2]),serial(t[3])]
def pointer(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],pointer(t[2]),pointer(t[3]))
    if p['l'] is not None:p['l']['p']=p
    if p['r'] is not None:p['r']['p']=p
    return p
def tuple_ptr(t):return S.LEAF if t is None else S.node(t['k'],tuple_ptr(t['l']),tuple_ptr(t['r']))
def dv(t):return tuple(S.lookup(t,k)[1] for k in range(1,N+1))

@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (S.LEAF,)
    return tuple(S.node(x,l,r) for x in range(lo,hi) for l in trees(lo,x) for r in trees(x+1,hi))

def rotations(t):
    if t==S.LEAF:return
    _,p,l,r=t
    if l!=S.LEAF:
        _,x,a,b=l
        yield S.node(x,a,S.node(p,b,r)),(), 'R'
    if r!=S.LEAF:
        _,x,b,c=r
        yield S.node(x,S.node(p,l,b),c),(), 'L'
    if l!=S.LEAF:
        for u,path,direction in rotations(l):yield S.node(p,u,r),(0,)+path,direction
    if r!=S.LEAF:
        for u,path,direction in rotations(r):yield S.node(p,l,u),(1,)+path,direction

def raw_scaled(t,b):return sum(8**(N-1-u)*v for u,v in zip(dv(t),dv(b)))

def source_access(a,b,mode,x):
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None
    aa,ae=S.trace(a,x)
    if mode=='K':bb,be=S.trace(b,x)
    else:bb=b;be=[]
    ap,ape=P.splay_trace(pointer(a),x)
    if mode=='K':bp,bpe=P.splay_trace(pointer(b),x)
    else:bp=pointer(b);bpe=[]
    ck(tuple_ptr(ap)==aa and tuple_ptr(bp)==bb,'two physical engines agree')
    ck([(e['case'],e['lo'],e['hi'],e['orient']) for e in ape]==ae,'A event order')
    ck([(e['case'],e['lo'],e['hi'],e['orient']) for e in bpe]==be,'B event order')
    return aa,bb,{'mode':mode,'key':x,'source_A':serial(a),'source_B':serial(b),
      'destination_A':serial(aa),'destination_B':serial(bb),'dA':da,'dB':db,
      'a':len(ae),'q':sum(e[0]!='ZIG' for e in be),'z':sum(e[0]=='ZIG' for e in be),
      'events_A':ae,'events_B':be}

def splay_word(start,goal):
    if start==goal:return []
    q=deque([start]);parent={start:None}
    while q and goal not in parent:
        t=q.popleft()
        for x in range(1,N+1):
            u=S.trace(t,x)[0]
            if u not in parent:parent[u]=(t,x);q.append(u)
    ck(goal in parent,'fixed six-key source reachability')
    word=[];cur=goal
    while cur!=start:
        prev,x=parent[cur];word.append(x);cur=prev
    return word[::-1]

def main():
    deps=['python/liquidity/legacy_embedding.py','python/independent/splay.py',
      'DO_RESEARCH_REBOOT/02_PROVED/26AL_generalized_signed_repayment.md',
      'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_analytic_20261030_v001/RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md',
      'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
      'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
      'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
      'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    entry={'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
           'files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in deps}}
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked tree clean')
    save('entry_source_pins.json',entry)
    leaf=S.LEAF;A=S.node(1,leaf,S.node(N,S.balanced(range(2,N)),leaf))
    B=S.node(2,S.node(1,leaf,leaf),S.vine(N)) if False else S.node(2,S.node(1,leaf,leaf),leaf)
    right=leaf
    for x in range(N,2,-1):right=S.node(x,leaf,right)
    B=S.node(2,S.node(1,leaf,leaf),right)
    As=S.trace(A,N)[0];Bp=S.trace(B,1)[0]
    ts=trees(1,N+1);idx={t:i for i,t in enumerate(ts)};adj=[];arc_controls=[]
    for i,t in enumerate(ts):
        row=[]
        for u,path,direction in rotations(t):
            p=pointer(t);at=p
            for side in path:at=at['l'] if side==0 else at['r']
            new=P._rot_right(at) if direction=='R' else P._rot_left(at)
            while new['p'] is not None:new=new['p']
            ck(tuple_ptr(new)==u,'exact primitive rotation graph')
            row.append(idx[u]);arc_controls.append([i,idx[u],list(path),direction])
        ck(len(row)==len(set(row))==N-1,'all and only n-1 primitive rotations')
        adj.append(row)
    ck(len(ts)==132 and len(arc_controls)==660,'fixed evaluation size')
    anchor=idx[A];distance=[-1]*len(ts);parent=[None]*len(ts);distance[anchor]=0;q=deque([anchor])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if distance[v]<0:distance[v]=distance[u]+1;parent[v]=u;q.append(v)
    ck(all(d>=0 for d in distance),'metric connectivity')
    ck(all(abs(distance[u]-distance[v])<=1 for u,row in enumerate(adj) for v in row),'distance edge bounds')
    ck(all(i==anchor or distance[parent[i]]==distance[i]-1 for i in range(len(ts))),'distance path certificates')
    before=[raw_scaled(t,B)-SCALE*d for t,d in zip(ts,distance)]
    after=[raw_scaled(t,Bp)-SCALE*d for t,d in zip(ts,distance)]
    p0=max(before);p1=max(after);att=[i for i,v in enumerate(before) if v==p0]
    ck(all(ts[i][1]!=1 for i in att),'every maximizing auxiliary root differs from accessed key')
    ck(p1-p0>=3*SCALE//4,'analytic envelope increase')
    ck(distance[idx[As]]==1,'the comparison T is one root rotation away')
    raw0=raw_scaled(A,B);rawdelete=raw_scaled(As,B)
    ck(Fraction(rawdelete-raw0,SCALE)==Fraction(21,8),'raw cheap-DELETE failure identity')
    _,_,edge=source_access(A,B,'K',1)
    ck((edge['a'],edge['q'],edge['z'])==(0,0,1),'starved zero-weight B zig')
    edge['candidate_Psi_source']=rat(p0);edge['candidate_Psi_destination']=rat(p1)
    edge['candidate_increase']=rat(p1-p0);edge['required_increase_upper_bound']=0
    # Embed the failed source edge in a complete legal closed paired walk.
    prefix=[('D',x) for x in splay_word(B,A)]
    word=prefix+[('K',1)]+[('D',x) for x in splay_word(A,Bp)]+[('K',x) for x in splay_word(Bp,B)]
    aa=bb=B;rows=[]
    for mode,x in word:
        aa,bb,row=source_access(aa,bb,mode,x);rows.append(row)
    ck(aa==bb==B,'exact paired closure from diagonal')
    ck(rows[len(prefix)]['source_A']==serial(A) and rows[len(prefix)]['source_B']==serial(B),'failed edge actually reached')
    cert={'status':'EXPLICIT_UNIFORM_CANDIDATE_REFUTED','n':N,'r':'1/8','metric_coefficient':1,
      'definition':'max_T(sum_y 8^{-d_T(y)} d_B(y)-rho(A,T))',
      'initial_source_A':serial(A),'initial_source_B':serial(B),'failed_edge':edge,
      'raw_G_DELETE_example':{'operation':['D',N],'a':1,'G_source':rat(raw0),'G_destination':rat(rawdelete),
                            'increase':rat(rawdelete-raw0),'budget':2},
      'metric_anchor_A':serial(A),'metric_certificate':{'trees':[serial(t) for t in ts],
         'adjacency':adj,'primitive_arcs':arc_controls,'distances':distance,'parents':parent},
      'all_exact_scaled_scores_source':before,'all_exact_scaled_scores_destination':after,'scale':SCALE,
      'maximizing_auxiliary_tree_indices_source':att,
      'closed_physical_witness':{'initial_A':serial(B),'initial_B':serial(B),'word':word,'failed_edge_index':len(prefix),
          'full_replay':rows,'A':sum(r['a'] for r in rows),'Q_B':sum(r['q'] for r in rows),
          'Z_B':sum(r['z'] for r in rows),'paired_closure':True},
      'free_parameters_fitted':0,'potential_labels_fitted':0,'larger_graph_search':False,
      'physical_CoarseDouble_counterexample':False,
      'all_size_refutation_basis':'analytic root-exclusion and maximizing-T argument in SP03, not this fixed-size evaluation'}
    save('explicit_potential_countercertificate.json',cert)
    changes=[p for p,h in entry['files'].items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    save('integrity.json',{'status':'PASS' if not changes and not git('status','--porcelain=v1','--untracked-files=no') else 'FAIL',
       'source_changes':changes,'Stage11G_modified':False,'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current')})
    print(json.dumps({'status':cert['status'],'Psi_source':rat(p0),'Psi_destination':rat(p1),
      'increase':rat(p1-p0),'a':edge['a'],'q':edge['q'],'z':edge['z'],
      'single_trees':len(ts),'directed_rotation_arcs':len(arc_controls),
      'closed_walk_accesses':len(word),'closed_walk_A':cert['closed_physical_witness']['A'],
      'closed_walk_Q_B':cert['closed_physical_witness']['Q_B'],'fitted_parameters':0},indent=2))

if __name__=='__main__':main()
