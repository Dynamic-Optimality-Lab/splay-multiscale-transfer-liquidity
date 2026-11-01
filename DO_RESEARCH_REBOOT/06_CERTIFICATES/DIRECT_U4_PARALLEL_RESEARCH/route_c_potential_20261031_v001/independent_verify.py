"""Verify the fixed formula's exact metric/evaluation/source countercertificate.

No fitted potential labels, new source-pair graph or parameter search. The
integer distances are certified by edge Lipschitz bounds and actual parent paths.
"""
from pathlib import Path
from fractions import Fraction
from math import comb
import sys,json,hashlib
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P
from independent import splay as S

def ck(x,msg):
    if not x:raise AssertionError(msg)
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def enc(t):return None if t==S.LEAF else [t[1],enc(t[2]),enc(t[3])]
def ptr(t):
    if t is None:return None
    q=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    if q['l'] is not None:q['l']['p']=q
    if q['r'] is not None:q['r']['p']=q
    return q
def rawptr(t):return None if t is None else [t['k'],rawptr(t['l']),rawptr(t['r'])]
def depths(t):return {k:S.lookup(t,k)[1] for k in S.inorder(t)}

def main():
    target=OUT/'independent_audit.json';ck(not target.exists(),'append-only output')
    source=OUT/'explicit_potential_countercertificate.json';c=json.loads(source.read_text(encoding='utf-8'))
    n=c['n'];m=c['metric_certificate'];ts=[dec(t) for t in m['trees']];ids={t:i for i,t in enumerate(ts)}
    ck(n==6 and len(ts)==len(ids)==comb(2*n,n)//(n+1)==132,'complete distinct valid BST set')
    for t in ts:ck(S.is_valid(t) and S.inorder(t)==list(range(1,n+1)),'valid ordered source tree')
    adjacency=[];arcs=0
    for raw in m['trees']:
        row=set()
        for x in range(1,n+1):
            for child,rotation in (('l',P._rot_right),('r',P._rot_left)):
                q=ptr(raw);_,path=P._depth_to(q,x);p=path[-1]
                if p[child] is None:continue
                top=rotation(p)
                while top['p'] is not None:top=top['p']
                row.add(ids[dec(rawptr(top))]);arcs+=1
        adjacency.append(row)
    ck(arcs==660 and all(set(old)==new for old,new in zip(m['adjacency'],adjacency)),'all original primitive arcs')
    A=dec(c['initial_source_A']);B=dec(c['initial_source_B']);anchor=ids[A]
    ds=m['distances'];parents=m['parents']
    ck(ds[anchor]==0 and parents[anchor] is None,'distance origin')
    ck(all(type(d) is int and d>=0 for d in ds),'exact finite metric values')
    for i,d in enumerate(ds):
        if i!=anchor:ck(parents[i] in adjacency[i] and ds[parents[i]]==d-1,'actual path upper bound')
        for j in adjacency[i]:ck(abs(d-ds[j])<=1,'all-path lower bound')
    x=c['failed_edge']['key'];Bp=S.trace(B,x)[0];scale=c['scale']
    ck(scale==8**(n-1),'exact rational scale')
    def g(t,b):
        da=depths(t);db=depths(b)
        return sum(8**(n-1-da[k])*db[k] for k in da)
    before=[g(t,B)-scale*d for t,d in zip(ts,ds)]
    after=[g(t,Bp)-scale*d for t,d in zip(ts,ds)]
    ck(before==c['all_exact_scaled_scores_source'] and after==c['all_exact_scaled_scores_destination'],'all candidate terms regenerated')
    p0=Fraction(max(before),scale);p1=Fraction(max(after),scale)
    ck(p0==Fraction(405,128) and p1==Fraction(16625,4096) and p1-p0==Fraction(3665,4096),'exact candidate failure')
    ck(all(ts[i][1]!=1 for i,v in enumerate(before) if v==max(before)),'maximizer root exclusion')
    closed=c['closed_physical_witness'];a=dec(closed['initial_A']);b=dec(closed['initial_B']);aa0=a;bb0=b
    A_total=Q=Z=0
    for j,((mode,x),r) in enumerate(zip(closed['word'],closed['full_replay'])):
        ck(enc(a)==r['source_A'] and enc(b)==r['source_B'],'full physical shared state')
        da=S.lookup(a,x)[1];a,ae=S.trace(a,x)
        if mode=='K':db=S.lookup(b,x)[1];b,be=S.trace(b,x)
        else:db=None;be=[]
        a_cost=len(ae);q=sum(e[0]!='ZIG' for e in be);z=sum(e[0]=='ZIG' for e in be)
        ck((da,db,a_cost,q,z)==(r['dA'],r['dB'],r['a'],r['q'],r['z']),'independent source costs')
        ck(enc(a)==r['destination_A'] and enc(b)==r['destination_B'],'independent source destinations')
        A_total+=a_cost;Q+=q;Z+=z
    ck(a==aa0 and b==bb0 and aa0==bb0,'exact closed walk from diagonal')
    ck((A_total,Q,Z)==(closed['A'],closed['Q_B'],closed['Z_B']),'closed totals')
    bad=closed['full_replay'][closed['failed_edge_index']]
    ck(bad['source_A']==c['initial_source_A'] and bad['source_B']==c['initial_source_B'],'counteredge reached inside original walk')
    ck((bad['a'],bad['q'],bad['z'])==(0,0,1),'zero reward but dynamically active zig')
    summary={'status':'PASS','single_trees':132,'source_rotation_arcs_checked':660,
      'rotation_distance_certificate_verified':True,'all_candidate_terms_checked':264,
      'source_Psi':str(p0),'destination_Psi':str(p1),'increase':str(p1-p0),
      'source_costs':{'a':0,'q':0,'z':1},'closed_word_accesses':len(closed['word']),
      'closed_totals':{'A':A_total,'Q_B':Q,'Z_B':Z},'actual_pair_closure':True,
      'potential_parameters_fitted':0,'CoarseDouble_refuted':False,
      'certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
    with target.open('x',encoding='utf-8') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
