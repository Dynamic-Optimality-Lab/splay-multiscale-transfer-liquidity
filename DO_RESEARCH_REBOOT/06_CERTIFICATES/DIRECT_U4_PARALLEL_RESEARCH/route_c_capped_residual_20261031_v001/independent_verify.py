"""Verify capped values, residual duals, source closure and scalar obstruction.

No producer import, matching algorithm, larger corpus or potential fit.
"""
from pathlib import Path
import hashlib,json,sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P

def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def inspect(t):
    if t is None:return [],set()
    l,lc=inspect(t[1]);r,rc=inspect(t[2]);keys=l+[t[0]]+r
    ck(keys==sorted(set(keys)),'valid BST and distinct present keys')
    return keys,lc|rc|{(keys[0],keys[-1])}
def proper(t):
    ks,c=inspect(t)
    if ks:c.remove((ks[0],ks[-1]))
    return sorted(c)
def depth(t,x):
    d=0
    while t is not None:
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2];d+=1
    raise AssertionError('absent source access')
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for k in ('l','r'):
        if p[k] is not None:p[k]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]

def main():
    ck(not (OUT/'independent_audit.json').exists(),'exclusive output')
    path=OUT/'capped_residual_certificate.json';c=json.loads(path.read_text(encoding='utf-8'));gs=c['protected_matching_graphs'];covered=0
    for g in gs:
        lk=proper(g['A']);rk=proper(g['B']);ka,_=inspect(g['A']);kb,_=inspect(g['B'])
        ck(ka==kb and len(lk)==len(rk)==len(ka)-1,'proper same-key graph dimensions')
        ck([list(i) for i in lk]==g['all_left'] and [list(j) for j in rk]==g['all_right'],'all subtree vertices regenerated')
        common=sorted(set(lk)&set(rk));cs=set(common)
        ck([list(i) for i in common]==g['forced_exact_intervals'],'all and only exact common pairs forced')
        left=[i for i in lk if i not in cs];right=[j for j in rk if j not in cs];n=len(left)
        ck(n==len(right) and [list(i) for i in left]==g['left_residual'] and [list(j) for j in right]==g['right_residual'],'residual vertices')
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        ck(adj==g['adjacency'],'every endpoint edge and nonedge regenerated')
        mat=g['matching'];cl=g['cover_left'];cr=g['cover_right']
        ck(len({i for i,j in mat})==len({j for i,j in mat})==len(mat),'one-to-one matching')
        ck(all(type(i) is type(j) is int and 0<=i<n and j in adj[i] for i,j in mat),'genuine matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr) and all(type(i) is int and 0<=i<n for i in cl+cr),'genuine cover vertices')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'all residual edges covered')
        ck(len(mat)==len(cl)+len(cr)==g['mu'],'residual maximum certified by exact dual equality')
        ck(g['protected_rank']==len(common)+g['mu'] and g['Ehat']==len(lk)-g['protected_rank'],'Ehat exact objective')
        covered+=sum(map(len,adj))
    edge_count=0
    def verify(row):
        nonlocal edge_count
        a=row['source_A'];b=row['source_B'];mode=row['mode'];x=row['key'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        pa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':pb,eb=P.splay_trace(ptr(b),x)
        else:pb,eb=ptr(b),[]
        aa=raw(pa);bb=raw(pb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((da,db,ac,q,z)==(row['dA'],row['dB'],row['a'],row['q'],row['z']),'source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source conventions')
        ck(aa==row['destination_A'] and bb==row['destination_B'],'complete physical endpoints')
        for events,saved in [(ea,row['events_A']),(eb,row['events_B'])]:
            ck([[e['case'],e['lo'],e['hi'],e['orient']] for e in events]==saved,'oriented event agreement')
        for sa,sb,key in [(a,b,'source_values'),(aa,b,'after_A_values'),(aa,bb,'destination_values')]:
            v=row[key];g=gs[v['graph_id']];ck(g['A']==sa and g['B']==sb,'residual certificate attached to correct state')
            keys,_=inspect(sa);n=len(keys);f=n-1-len(g['forced_exact_intervals']);eh=g['Ehat'];cap=max(0,n//2-2)
            ck(v=={'F':f,'Ehat':eh,'J':max(eh,f-cap),'cap':cap,'graph_id':v['graph_id']},'all capped values independently recomputed')
            ck(v['J']==f-min(g['mu'],cap) and eh<=v['J']<=f,'cap equivalence and normalized bracket')
        v0=row['source_values'];vm=row['after_A_values'];v1=row['destination_values']
        ck(abs(vm['J']-v0['J'])<=da and row['delta_J']==v1['J']-v0['J'],'A bound and whole difference')
        ck(row['budget']==2*ac-q and row['inequality_holds']==(row['delta_J']<=row['budget']),'whole inequality verdict');edge_count+=1
    for row in c['controls']:verify(row)
    ck(len(c['controls'])==10 and all(r['inequality_holds'] for r in c['controls'][:-1]),'all old controls and derived known starved phase paid')
    oldhook=next(r for r in c['controls'] if r['label']=='reused_hook_vine_full_law_safeguard')
    ck((oldhook['source_values']['J'],oldhook['destination_values']['J'],oldhook['a'],oldhook['q'])==(4,2,0,2),'requested six-key starved KEEP repaired')
    bad=c['controls'][-1]
    ck((bad['source_values']['F'],bad['source_values']['Ehat'],bad['destination_values']['F'],bad['destination_values']['Ehat'])==(4,1,2,2),'new source coordinates')
    ck((bad['source_values']['J'],bad['destination_values']['J'],bad['a'],bad['q'],bad['z'],bad['budget'])==(3,2,0,2,0,-2),'new actual whole failure')
    # Exact forced bounds for the general monotone-aggregation argument.
    opp=c['controls'][0];o=c['monotone_obstruction']
    fp=lambda v:[v['F'],v['Ehat']]
    ck(fp(opp['source_values'])==o['opposite_source']==[5,5] and fp(opp['destination_values'])==o['opposite_destination']==[4,2],'opposite actual coordinates')
    ck(fp(bad['source_values'])==o['padded_source']==[4,1] and fp(bad['destination_values'])==o['padded_destination']==[2,2],'padded actual coordinates')
    ck(opp['a']==bad['a']==0 and opp['q']==bad['q']==2 and o['n']==6,'same-size genuine starved operations')
    upper=5+opp['budget'];lower=2-bad['budget']
    ck(upper==3 and lower==4 and lower>upper,'incompatible forced scalar bounds')
    ck(all(x<=y for x,y in zip(fp(bad['source_values']),fp(opp['destination_values']))),'coordinate order forces reverse compatibility inequality')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];a0=a;b0=b;At=Qt=Zt=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==13,'complete diagonal word')
    for (mode,x),row in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(row['source_A'],row['source_B'],row['mode'],row['key']),'full source-state sharing')
        verify(row);a=row['destination_A'];b=row['destination_B'];At+=row['a'];Qt+=row['q'];Zt+=row['z']
    ck(a==a0 and b==b0 and (At,Qt,Zt)==(15,4,4)==(w['A'],w['Q_B'],w['Z_B']),'exact paired closure and totals')
    r=w['full_replay'][w['failed_edge_index']]
    ck(r['source_A']==bad['source_A'] and r['source_B']==bad['source_B'] and r['delta_J']==-1,'counteredge physically reached')
    result={'status':'PASS','residual_matching_graphs_verified':len(gs),'matching_cover_equalities':len(gs),'residual_edges_covered':covered,
      'all_cap_values_recomputed':True,'old_controls_and_known_starved_phase_pass':True,
      'requested_old_starved_KEEP':{'J_source':4,'J_destination':2,'a':0,'q':2},
      'new_counterexample':{'J_source':3,'J_destination':2,'a':0,'q':2,'z':0,'budget':-2},
      'monotone_aggregation_forced_bounds':{'phi(4,2)_upper':upper,'phi(4,1)_lower':lower,'coordinate_order_verified':True,'contradiction':'4<=phi(4,1)<=phi(4,2)<=3'},
      'monotone_scope':'coordinatewise nondecreasing phi_n(F,Ehat) with Ehat<=phi_n<=F; general proof in CR02',
      'source_controls':10,'complete_source_edges_replayed':edge_count,'all_oriented_events_agree':True,
      'closed_word_accesses':13,'actual_diagonal_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},
      'finite_potential_fits':0,'new_pair_state_graphs':0,'CoarseDouble_refuted':False,
      'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
