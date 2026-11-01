"""Verify forced pairs, residual optimality, symbolic ports and source replay.

No producer import, matching solver, larger corpus or fit. The arbitrary-fringe
proof is the core rank identity plus a proved one-added-vertex bound.
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
    if t is None:return [],{},set()
    kl,rl,cl=inspect(t[1]);kr,rr,cr=inspect(t[2]);keys=kl+[t[0]]+kr
    ck(keys==sorted(set(keys)),'valid ordered BST')
    pair=(keys[0],keys[-1]);return keys,{**rl,**rr,t[0]:pair},cl|cr|{pair}
def proper(t):
    keys,roots,c=inspect(t)
    if keys:c.remove((keys[0],keys[-1]))
    return sorted(c)
def F(a,b):
    ka,_,ca=inspect(a);kb,_,cb=inspect(b);ck(ka==kb,'same-key source pair')
    return len(ka)-len(ca&cb)
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for k in ('l','r'):
        if p[k] is not None:p[k]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
def depth(t,x):
    d=0
    while t is not None:
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2];d+=1
    raise AssertionError('absent source key')

def verify_boundary(b):
    counts=0;constants={}
    for mode in ('nonempty_distinct','nonempty_coincident','empty'):
        sub={'h':'l'} if mode=='nonempty_coincident' else (b['empty_substitution'] if mode=='empty' else {})
        replace=lambda v:[sub.get(x,x) for x in v]
        low='l';high='l' if mode=='nonempty_coincident' else 'h'
        def port_left(v):return mode!='empty' and v[0]==low
        def port_right(v):return mode!='empty' and v[1]==high
        for r in b['reductions']:
            aa={k:replace(v) for k,v in b['A_tables'][r['A_table']].items()}
            bb={k:replace(v) for k,v in b['B_tables'][r['state']].items()}
            actual=[[i,j] for i,I in aa.items() for j,J in bb.items() if I==J]
            ck(sorted(actual)==sorted(r['forced_core_pairs']),'all exact common core pairs identified')
            ck(len(actual)==r['core_forced_count'],'forced core count')
            for i,j in actual:del aa[i];del bb[j]
            def adj():return {(i,j) for i,I in aa.items() for j,J in bb.items() if I[0]==J[0] or I[1]==J[1]}
            for edge in r['private_edges']:
                i=edge['left'];j=edge['right'];edges=adj();ck((i,j) in edges,'private matching edge exists')
                if edge['private_endpoint']=='left':
                    ck(not port_left(aa[i]) and sum(u==i for u,v in edges)==1,'globally private left vertex including fringe ports')
                else:
                    ck(not port_right(bb[j]) and sum(v==j for u,v in edges)==1,'globally private right vertex including fringe ports')
                del aa[i];del bb[j]
            ck(len(r['private_edges'])==r['private_edge_count'] and not adj(),'no residual core-core edges')
            if mode!='empty':
                ck(sorted(k for k,v in aa.items() if port_left(v))==sorted(r['remaining_left_port_ids']),'only declared left fringe port remains')
                ck(sorted(k for k,v in bb.items() if port_right(v))==sorted(r['remaining_right_port_ids']),'only declared right fringe ports remain')
            else:
                ck(all(i in aa for i in r['remaining_left_port_ids']) and all(j in bb for j in r['remaining_right_port_ids']),'empty-fringe dummy ports are isolated retained vertices')
            constants[r['state']]=(r['core_forced_count']+r['private_edge_count'],r['kernel']);counts+=1
    ck(constants=={'L_before':(3,'LH'),'L_after':(3,'LH'),'R_before':(2,'LH'),'R_after':(4,'L')},'symbolic rank identities')
    return counts

def main():
    ck(not (OUT/'independent_audit.json').exists(),'exclusive output')
    path=OUT/'fixed_exact_pair_certificate.json';c=json.loads(path.read_text(encoding='utf-8'))
    b=json.loads((OUT/'helper_boundary_certificate.json').read_text(encoding='utf-8'))
    boundary_cases=verify_boundary(b);graphs=c['protected_matching_graphs'];covered=0
    for g in graphs:
        left=proper(g['A']);right=proper(g['B']);common=sorted(set(left)&set(right));cs=set(common)
        ck([list(i) for i in left]==g['all_left'] and [list(j) for j in right]==g['all_right'],'all proper subtree vertices regenerated')
        ck([list(i) for i in common]==g['forced_exact_intervals'],'every exact pair is forced, and no other pair is forced')
        lr=[i for i in left if i not in cs];rr=[j for j in right if j not in cs];n=len(lr)
        ck(n==len(rr) and [list(i) for i in lr]==g['left_residual'] and [list(j) for j in rr]==g['right_residual'],'residual vertices after forced pairs')
        ad=[[j for j,J in enumerate(rr) if I[0]==J[0] or I[1]==J[1]] for I in lr]
        ck(ad==g['adjacency'],'all residual endpoint edges and nonedges regenerated')
        mat=g['matching'];cl=g['cover_left'];cr=g['cover_right']
        ck(len({i for i,j in mat})==len({j for i,j in mat})==len(mat),'residual matching one-to-one')
        ck(all(type(i) is type(j) is int and 0<=i<n and j in ad[i] for i,j in mat),'valid residual matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr) and all(type(i) is int and 0<=i<n for i in cl+cr),'valid residual cover vertices')
        ck(all(i in cl or j in cr for i,row in enumerate(ad) for j in row),'all residual edges covered')
        ck(len(mat)==len(cl)+len(cr)==g['mu'],'residual maximum certified by matching-cover equality')
        ck(g['protected_rank']==len(common)+g['mu'] and g['Ehat']==len(left)-g['protected_rank'],'protected objective evaluated exactly')
        ck(0<=g['Ehat']<=F(g['A'],g['B']),'protected value bounds');covered+=sum(map(len,ad))
    source_edges=0;core_tables=0
    def verify(row):
        nonlocal source_edges,core_tables
        a=row['source_A'];bb=row['source_B'];mode=row['mode'];x=row['key']
        da=depth(a,x);db=depth(bb,x) if mode=='K' else None
        pa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':pb,eb=P.splay_trace(ptr(bb),x)
        else:pb,eb=ptr(bb),[]
        aa=raw(pa);dd=raw(pb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((da,db,ac,q,z)==(row['dA'],row['dB'],row['a'],row['q'],row['z']),'source depth and event costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source cost conventions')
        ck(aa==row['destination_A'] and dd==row['destination_B'],'complete physical source endpoints')
        for ev,saved in ((ea,row['events_A']),(eb,row['events_B'])):
            ck([[e['case'],e['lo'],e['hi'],e['orient']] for e in ev]==saved,'every oriented event agrees')
        states=[(a,bb,'graph_source_id','Ehat_source'),(aa,bb,'graph_after_A_id','Ehat_after_A'),(aa,dd,'graph_destination_id','Ehat_destination')]
        for sa,sb,idx,val in states:
            g=graphs[row[idx]];ck(g['A']==sa and g['B']==sb and g['Ehat']==row[val],'protected certificate belongs to correct full state')
        ck((row['F_source'],row['F_destination'])==(F(a,bb),F(aa,dd)),'original F values')
        ck(row['delta_Ehat']==row['Ehat_destination']-row['Ehat_source'] and row['budget']==2*ac-q,'whole source difference and budget')
        ck(row['inequality_holds']==(row['delta_Ehat']<=row['budget']) and abs(row['Ehat_after_A']-row['Ehat_source'])<=da,'inequality status and A motion')
        meta=row.get('meta')
        if meta and not meta['mirror']:
            sm={key:'c'+str(i+1) for i,key in enumerate(meta['core'])};fr=set(meta['fringe_keys'])
            def actual_core(t,side):
                _,rootsets,_=inspect(t);out={}
                for root,(lo,hi) in rootsets.items():
                    if root==t[0] or root not in sm:continue
                    ident=side+str(meta['core'].index(root)+1)
                    out[ident]=['l' if lo in fr else sm[lo],'h' if hi in fr else sm[hi]]
                return out
            for t,side,table in [(a,'a',b['A_tables']['before']),(aa,'a',b['A_tables']['after']),
              (bb,'b',b['B_tables'][meta['family']+'_before']),(dd,'b',b['B_tables'][meta['family']+'_after'])]:
                expected=table if meta['m'] else {k:[b['empty_substitution'].get(v,v) for v in pair] for k,pair in table.items()}
                ck(actual_core(t,side)==expected,'symbolic core endpoint table matches actual source geometry');core_tables+=1
        source_edges+=1
    for row in c['controls']:verify(row)
    positive=c['controls'][:-1];ck(len(positive)==7 and all(r['inequality_holds'] for r in positive),'all registered named-family controls pass')
    bad=c['controls'][-1];ck((bad['a'],bad['q'],bad['z'],bad['Ehat_source'],bad['Ehat_destination'])==(0,2,1,1,2),'independent full-law safeguard failure')
    gs=graphs[bad['graph_source_id']];gd=graphs[bad['graph_destination_id']]
    ck(gs['forced_exact_intervals']==[] and gs['mu']==4 and gd['forced_exact_intervals']==[[2,3],[2,5],[2,6]] and gd['mu']==0,'readable hook certificate ranks')
    w=c['closed_witness'];a=w['initial_A'];bb=w['initial_B'];a0=a;b0=bb;At=Qt=Zt=0
    ck(a==bb and len(w['word'])==len(w['full_replay'])==14,'complete diagonal source word')
    for (mode,x),row in zip(w['word'],w['full_replay']):
        ck((a,bb,mode,x)==(row['source_A'],row['source_B'],row['mode'],row['key']),'full source-state sharing')
        verify(row);a=row['destination_A'];bb=row['destination_B'];At+=row['a'];Qt+=row['q'];Zt+=row['z']
    ck(a==a0 and bb==b0 and (At,Qt,Zt)==(19,5,4)==(w['A'],w['Q_B'],w['Z_B']),'actual paired closure and totals')
    r=w['full_replay'][w['failed_edge_index']]
    ck(r['source_A']==bad['source_A'] and r['source_B']==bad['source_B'] and r['delta_Ehat']==1,'hook counteredge actually reached')
    result={'status':'PASS','protected_graphs_verified':len(graphs),'residual_matching_cover_equalities':len(graphs),
      'residual_edges_covered':covered,'symbolic_core_reductions_verified':boundary_cases,'actual_core_tables_checked':core_tables,
      'symbolic_endpoint_cases':['distinct fringe extrema','coincident fringe extrema','empty fringe'],
      'universal_helper_rank_identities':{'L':'K_before=K_after=c_int+3+mu_LH','R':'K_after-K_before=2+mu_L-mu_LH in {1,2}'},
      'one_added_right_vertex_lemma':'proved analytically in FX03, not inferred from finite controls',
      'source_controls':8,'whole_source_edges_replayed':source_edges,'all_oriented_events_agree':True,
      'full_law_counterexample':{'Ehat_source':1,'Ehat_destination':2,'a':0,'q':2,'delta_Ehat':1,'budget':-2},
      'closed_word_accesses':14,'actual_diagonal_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},
      'finite_potential_fits':0,'new_source_state_graphs':0,'CoarseDouble_refuted':False,
      'source_certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'boundary_certificate_sha256':hashlib.sha256((OUT/'helper_boundary_certificate.json').read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
