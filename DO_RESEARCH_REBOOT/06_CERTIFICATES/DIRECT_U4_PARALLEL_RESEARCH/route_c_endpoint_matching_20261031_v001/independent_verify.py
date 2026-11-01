"""Verify graph optimality by matchings/covers and replay frozen source events.

No augmenting-path solver, producer import, source graph search or finite fit.
"""
from pathlib import Path
import json,hashlib,sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P

def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def inspect(t):
    if t is None:return [],set()
    lk,lc=inspect(t[1]);rk,rc=inspect(t[2]);keys=lk+[t[0]]+rk
    ck(keys==sorted(set(keys)),'valid ordered BST and distinct keys')
    return keys,lc|rc|{(keys[0],keys[-1])}
def proper(t):
    keys,c=inspect(t)
    if keys:c.remove((keys[0],keys[-1]))
    return sorted(c)
def F(a,b):
    ka,ca=inspect(a);kb,cb=inspect(b);ck(ka==kb,'same-key pair')
    return len(ka)-len(ca&cb)
def depth(t,x):
    d=0
    while t is not None:
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2];d+=1
    raise AssertionError('absent source key')
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for k in ('l','r'):
        if p[k] is not None:p[k]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]

def main():
    target=OUT/'independent_audit.json';ck(not target.exists(),'exclusive output')
    path=OUT/'endpoint_matching_countercertificate.json';c=json.loads(path.read_text(encoding='utf-8'))
    graphs=c['matching_graphs'];edges=0
    for g in graphs:
        left=proper(g['A']);right=proper(g['B']);keysA,_=inspect(g['A']);keysB,_=inspect(g['B'])
        ck(keysA==keysB and len(left)==len(right)==len(keysA)-1,'proper graph dimensions')
        ck([list(i) for i in left]==g['left_intervals'] and [list(j) for j in right]==g['right_intervals'],'all graph vertices regenerated')
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        ck(adj==g['adjacency'],'every endpoint edge and nonedge regenerated')
        matching=g['matching'];cl=g['cover_left'];cr=g['cover_right'];n=len(left)
        ck(len({i for i,j in matching})==len({j for i,j in matching})==len(matching),'matching one-to-one capacity')
        ck(all(type(i) is type(j) is int and 0<=i<n and j in adj[i] for i,j in matching),'genuine matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr) and all(type(i) is int and 0<=i<n for i in cl+cr),'genuine cover vertices')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'all endpoint edges covered')
        ck(len(matching)==len(cl)+len(cr)==g['nu'],'matching-cover exact equality proves maximum')
        ck(g['E']==n-g['nu'],'exact matching deficit')
        edges+=sum(map(len,adj))
    def verify(row):
        a=row['source_A'];b=row['source_B'];mode=row['mode'];x=row['key']
        da=depth(a,x);db=depth(b,x) if mode=='K' else None
        pa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':pb,eb=P.splay_trace(ptr(b),x)
        else:pb,eb=ptr(b),[]
        aa=raw(pa);bb=raw(pb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((da,db,ac,q,z)==(row['dA'],row['dB'],row['a'],row['q'],row['z']),'source exact costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'cost conventions')
        ck(aa==row['destination_A'] and bb==row['destination_B'],'complete source destination trees')
        for ev,saved in [(ea,row['events_A']),(eb,row['events_B'])]:
            ck([[e['case'],e['lo'],e['hi'],e['orient']] for e in ev]==saved,'oriented source events')
        states=[(a,b,'matching_source_id','E_source'),(aa,b,'matching_after_A_id','E_after_A'),(aa,bb,'matching_destination_id','E_destination')]
        for sa,sb,idx,value in states:
            g=graphs[row[idx]];ck(g['A']==sa and g['B']==sb and g['E']==row[value],'matching value belongs to correct full physical state')
        f0=F(a,b);fm=F(aa,b);f1=F(aa,bb)
        ck((f0,fm,f1)==(row['F_source'],row['F_after_A'],row['F_destination']),'old F exact counts')
        e0=row['E_source'];em=row['E_after_A'];e1=row['E_destination']
        ck((row['repair_source'],row['repair_destination'])==(e0-f0,e1-f1),'nonlinear correction values')
        ck(abs(em-e0)<=da and row['delta_E']==e1-e0,'A motion and whole difference')
        ck(row['required_upper_bound']==2*ac-q and row['inequality_holds']==(e1-e0<=2*ac-q),'whole inequality verdict')
    for row in c['controls']:verify(row)
    bad=c['controls'][-1]
    ck((bad['a'],bad['q'],bad['z'],bad['E_source'],bad['E_after_A'],bad['E_destination'])==(1,2,0,1,2,2),'exact zero-helper violation')
    ck(bad['F_source']==4 and bad['F_destination']==3 and bad['delta_E']==1 and bad['required_upper_bound']==0,'old F succeeds while E fails')
    # Check the small hand-readable certificate used in EM03 as well.
    manual=[
      (bad['matching_source_id'],[([1,1],[1,3]),([1,5],[1,4]),([3,5],[3,3]),([4,5],[1,5])],[[1,1],[1,5],[3,5]],[[1,5]]),
      (bad['matching_destination_id'],[([1,1],[1,1]),([3,5],[3,3]),([3,6],[6,6])],[[1,1],[3,5],[3,6]],[])]
    for index,matching,cl,cr in manual:
        g=graphs[index];l=g['left_intervals'];r=g['right_intervals'];ad=g['adjacency']
        mi=[(l.index(i),r.index(j)) for i,j in matching];li=[l.index(i) for i in cl];ri=[r.index(j) for j in cr]
        ck(len(set(i for i,j in mi))==len(set(j for i,j in mi))==len(mi)==len(li)+len(ri)==g['nu'],'hand certificate cardinality')
        ck(all(j in ad[i] for i,j in mi) and all(i in li or j in ri for i,row in enumerate(ad) for j in row),'hand matching and cover valid')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];a0=a;b0=b;At=Qt=Zt=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==11,'full diagonal closed word dimension')
    for (mode,x),row in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(row['source_A'],row['source_B'],row['mode'],row['key']),'full shared source-state chain')
        verify(row);a=row['destination_A'];b=row['destination_B'];At+=row['a'];Qt+=row['q'];Zt+=row['z']
    ck(a==a0 and b==b0 and (At,Qt,Zt)==(16,4,2)==(w['A'],w['Q_B'],w['Z_B']),'exact paired closure and costs')
    r=w['full_replay'][w['failed_edge_index']]
    ck(r['source_A']==bad['source_A'] and r['source_B']==bad['source_B'] and r['delta_E']==1,'counteredge actually reached')
    ck(c['stop']['further_helper_variants_run']==c['stop']['port_embedding_search_run']==c['stop']['hook_vine_control_run']==False,'first-obstruction stop preserved')
    result={'status':'PASS','matching_graphs_verified':len(graphs),'matching_edges_and_nonedges_regenerated':True,
      'graph_edges_covered':edges,'matching_cover_equalities_verified':len(graphs),'hand_readable_certificates_verified':2,
      'source_controls':3,'full_source_edges_replayed':14,'all_oriented_events_agree':True,
      'opposite_vine_controls':[[r['E_source'],r['E_destination'],r['q']] for r in c['controls'][:2]],
      'helper_failure':{'E_source':1,'E_after_A':2,'E_destination':2,'delta_E':1,'budget':0,'a':1,'q':2},
      'closed_word_accesses':11,'actual_diagonal_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},
      'finite_fits':0,'new_source_state_graphs':0,'CoarseDouble_refuted':False,
      'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    with target.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
